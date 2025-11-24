==========================
eea.api.redirector
==========================
.. image:: https://ci.eionet.europa.eu/buildStatus/icon?job=eea/eea.api.redirector/develop
  :target: https://ci.eionet.europa.eu/job/eea/job/eea.api.redirector/job/develop/display/redirect
  :alt: Develop
.. image:: https://ci.eionet.europa.eu/buildStatus/icon?job=eea/eea.api.redirector/master
  :target: https://ci.eionet.europa.eu/job/eea/job/eea.api.redirector/job/master/display/redirect
  :alt: Master

The eea.api.redirector is a Plone add-on that extends Plone's native redirect system with Redis-based URL redirects, enabling high-performance redirect lookups and external redirect management.

.. contents::


Main features
=============

1. **Redis-backed redirects**: Store and retrieve URL redirects from Redis in addition to Plone's database
2. **Fallback mechanism**: Automatically checks Redis when redirects are not found in Plone storage
3. **Graceful error handling**: Redis connection failures don't break the redirection system
4. **API endpoint support**: Intelligent hierarchical URL matching for API services and endpoints
5. **Proper HTTP status codes**: Returns 410 Gone for permanently deleted resources
6. **Redirect loop prevention**: Built-in protection against circular redirects
7. **Easy configuration**: Simple environment variable setup for Redis connections
8. **Non-intrusive**: Extends existing Plone functionality without replacing it


Install
=======

* Via pip::

    $ pip install eea.api.redirector

* Or via docker-compose::

    $ docker-compose up -d

This will start both Plone 6 and Redis services with the add-on pre-configured.

* Install *eea.api.redirector* within Site Setup > Add-ons


Configuration
=============

Redis connection settings are configured via environment variables:

* ``REDIS_SERVER`` - Redis server hostname (default: ``localhost``)
* ``REDIS_PORT`` - Redis server port (default: ``6379``)
* ``REDIS_DB`` - Redis database index (default: ``0``)
* ``REDIS_TIMEOUT`` - Connection timeout in seconds (default: ``5``)

The included ``docker-compose.yml`` demonstrates how to configure these settings. The Plone service connects to Redis using::

    environment:
      REDIS_SERVER: "redis"
      REDIS_PORT: "6379"
      REDIS_DB: "0"
      REDIS_TIMEOUT: "5"


How it works
============

The add-on extends Plone's built-in ``plone.app.redirector`` by:

1. **Storage Integration**: Adds a Redis storage utility alongside Plone's database storage
2. **Fallback Lookup**: When a redirect is not found in Plone's database, it checks Redis
3. **API Support**: Custom error handling for API endpoints with hierarchical URL matching
4. **Non-blocking**: If Redis is unavailable, the system continues using Plone's standard redirects

This design allows you to:

* Manage redirects externally via Redis while maintaining Plone's UI-based redirect management
* Share redirects across multiple Plone instances using a common Redis server
* Achieve faster redirect lookups for high-traffic sites
* Store temporary or dynamic redirects that don't need to persist in Plone's database


Source code
===========

- `Plone 6 on github <https://github.com/eea/eea.api.redirector>`_


Eggs repository
===============

- https://pypi.python.org/pypi/eea.api.redirector
- http://eggrepo.eea.europa.eu/simple


Plone versions
==============
It has been developed and tested for Plone 6. See section above.


How to contribute
=================
See the `contribution guidelines (CONTRIBUTING.md) <https://github.com/eea/eea.api.redirector/blob/master/CONTRIBUTING.md>`_.

Copyright and license
=====================

eea.api.redirector (the Original Code) is free software; you can
redistribute it and/or modify it under the terms of the
GNU General Public License as published by the Free Software Foundation;
either version 2 of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful, but
WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY
or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License
for more details.

You should have received a copy of the GNU General Public License along
with this program; if not, write to the Free Software Foundation, Inc., 59
Temple Place, Suite 330, Boston, MA 02111-1307 USA.

The Initial Owner of the Original Code is European Environment Agency (EEA).
Portions created by Eau de Web are Copyright (C) 2009 by
European Environment Agency. All Rights Reserved.


Funding
=======

EEA_ - European Environment Agency (EU)

.. _EEA: https://www.eea.europa.eu/
.. _`EEA Web Systems Training`: http://www.youtube.com/user/eeacms/videos?view=1
