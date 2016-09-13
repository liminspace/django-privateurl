*****************
django-privateurl
*****************

.. figure:: https://travis-ci.org/liminspace/django-privateurl.svg?branch=develop
  :target: https://travis-ci.org/liminspace/django-privateurl

This application helps You easy and flexibility implement different features that need use private url
for users like registration confirmation, password recovery, access to paid content and so on.

Low level API provides You full control and allow:

* limiting private url by time and hits
* auto removing urls that won't be used
* knowing number of hits, date of first and last hit for each url
* controlling token generator
* saving additional data in JSON format and using it at url hits
* processing succeeded or failed hits using django signals and controlling server responses

============
Installation
============

**Requirements:**

* Django v1.8+

**\1\. Install** ``django-privateurl``.

* Via pip::

  $ pip install django-privateurl

* Via setuptools::

  $ easy_install django-privateurl
  
 For install development version use ``git+https://github.com/liminspace/django-privateurl.git@develop``
 instead ``django-privateurl``.

**\2\. Set up** ``settings.py`` **in your django project.** ::

  INSTALLED_APPS = (
    ...,
    'privateurl',
  )

**\3\. Run migrate**::

  $ manage.py migrate

=====
Usage
=====
