# -*- encoding: utf-8 -*-

from flask import jsonify, render_template, redirect, request, url_for, flash
from flask_login import (
    current_user,
    login_required,
    login_user,
    logout_user
)
from app import db, login_manager
from app.base import blueprint
from app.base.forms import LoginForm
import string
from app.base.models import User
from app.base.util import verify_pass
from app.Modules.ProjectRouting.Software import IOSXE
import app.Modules.ProjectRouting.Database.DB_queries as Db_queries
import app.Modules.ProjectRouting.Database.DatabaseOps as DB
import app.Modules.connection as ConnectWith
import app.Modules.GetWithNetmiko as GetInfo
import sqlite3
import logging
import os

device = None
username = None
password = None
netconf_port = None
ssh_port = None
netmiko_session = None


@blueprint.route('/')
def route_default():
    return redirect(url_for('base_blueprint.login'))


@blueprint.route('/login', methods=['GET', 'POST'])
def login():
    global device, username, password,netmiko_session, ssh_port

    login_form = LoginForm(request.form)
    if 'login' in request.form:

        device = request.form['device']
        username = request.form['username']
        password = request.form['password']
        ssh_port = request.form['ssh']

        if not ssh_port:
            ssh_port = 22

        if device and username and password:

            netmiko_session = ConnectWith.creat_netmiko_connection(request.form['username'], request.form['password'],
                                                                   request.form['device'], ssh_port)

            if netmiko_session == 'Authenitcation Error':
                flash("Authentication Failure")
                return redirect(url_for('base_blueprint.login'))
            elif netmiko_session == 'ssh_exception' or netmiko_session == 'Connection Timeout':
                flash("Check Device Connectivity")
                return redirect(url_for('base_blueprint.login'))
            else:
                return redirect(url_for('base_blueprint.get_routing'))

        return render_template('accounts/login.html', msg='Wrong user or password', form=login_form)

    if not current_user.is_authenticated:
        return render_template('accounts/login.html',
                               form=login_form)
    return redirect(url_for('home_blueprint.index'))


@blueprint.route('/logout')
def logout():
    """User logout and re-login"""

    logout_user()
    return redirect(url_for('base_blueprint.login'))


@blueprint.route('/routing')
def get_routing():
    """Gets all things routing, arp, interfaces, routing protocols"""

    # Create Nemiko session object, connect to local DB and get IOS_XE routing table
    routing_session = ConnectWith.creat_netmiko_connection(username, password, device, ssh_port)
    mydb = sqlite3.connect("app/Modules/ProjectRouting/Database/Routing")
    cursor = mydb.cursor()
    db_obj = DB.RoutingDatabase(mydb, cursor)
    IOSXE.RoutingIos(routing_session, db_obj, mydb, cursor)

    return render_template('routing.html', route_table=Db_queries.view_routes_ios(cursor))


@blueprint.route('/route_details', methods=['POST'])
def route_details():
    """Request route details"""

    #Get and split route w/ CIDR and protocol identifier
    details = request.form.get('details').split('-')
    route_details = GetInfo.get_route_detials(netmiko_session, details[0].split('/')[0], details[1], with_mask=details[0])

    return render_template('route_detials.html', route=route_details[0], route_detials=route_details[1])


@blueprint.route('/about')
def about():
    """Program info"""

    return render_template('about.html')
