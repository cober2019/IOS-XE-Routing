.. image:: https://travis-ci.com/cober2019/IOS-XE-Routing.svg?branch=main
    :target: https://travis-ci.com/cober2019/IOS-XE-Routing
.. image:: https://img.shields.io/badge/IOS--XE-required-blue
    :target: -
.. image:: https://img.shields.io/badge/Fugi_IOS_XE_v16.09.04-passing-green
    :target: -
.. image:: https://img.shields.io/badge/Fugi_IOS_XE_v16.07.02-passing-green
    :target: -
.. image:: https://img.shields.io/badge/DevnetSandbox-passing-green
    :target: -
IOS-XE-Routing
================

  This program gets the routing table for devices running IOS-XE software. On top of getting the routes it also allows you to get the route details from CLI     with one click. ***This program uses a popup window so ensure your browser isn't blocking them.**

App Access
-----------

    + Use http://127.0.0.1:5000/ to access the app login page
    
Routing Table
--------------

    + The routing table will load once login is complete and the home pages loads. The routes are fetch and saved into a local datbase. In turn, the DB is read and routes presented
    
.. image:: https://github.com/cober2019/IOS-XE-Routing/blob/main/images/RoutingTable.PNG

Route Details
--------------

    + You can get more details on any route with the "More Details" button. Depending on protocol, certain commands will be executed to get a CLI view of the route table and the DB that the protocol is associated with. The example below shows the EIGRP topology entry and the show ip route entry from CLI.

.. image:: https://github.com/cober2019/IOS-XE-Routing/blob/main/images/routeDetials.PNG

    
    
