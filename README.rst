#################
django-privateurl
#################
.. image:: https://travis-ci.org/liminspace/django-privateurl.svg?branch=master
 :target: https://travis-ci.org/liminspace/django-privateurl
 :alt: build

.. image:: https://img.shields.io/pypi/v/django-privateurl.svg
 :target: https://pypi.org/project/django-privateurl/
 :alt: pypi

This application helps You easy and flexibly implement different features that need use private url
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

**\3\. Add url pattern in** ``urls.py``::

  urlpatterns = [
      ...
      url(r'^private/', include('privateurl.urls', namespace='privateurl')),
  ]

**\4\. Run migrate**::

  $ manage.py migrate

=====
Usage
=====

First you need create PrivateUrl using ``create`` class method::

  PrivateUrl.create(action, user=None, expire=None, data=None, hits_limit=1, auto_delete=False,
                    token_size=None, replace=False, dashed_piece_size=None)

* ``action`` -- is a slug that using in url and allow distinguish one url of another
* ``user`` -- is user instance that you can get in request process
* ``expire`` -- is expiration date for private url. You can set ``datetime`` or ``timedelta``
* ``data`` -- is additional data that will be saved as JSON. Setting a dict object is good idea
* ``hits_limit`` -- is limit of requests. Set 0 for unlimit
* ``auto_delete`` -- set ``True`` if you want remove private url object when it will be not available
* ``token_size`` -- set length of token. You can set number of size or tuple with min and max size. Keep ``None`` for using value from ``settings.PRIVATEURL_DEFAULT_TOKEN_SIZE``
* ``replace`` -- set ``True`` if you want remove old exists private url for user and action before creating one
* ``dashed_piece_size`` -- split token with dash every N symbols. Keep ``None`` for using value from ``settings.PRIVATEURL_DEFAULT_TOKEN_DASHED_PIECE_SIZE``

For example::

  from privateurl.models import PrivateUrl

  purl = PrivateUrl.create('registration-confirmation', user=user)
  user.send_email(
      subject='Registration confirmation',
      body='Follow the link for confirm your registration: {url}'.format(
          url=purl.get_absolute_url(),
      ),
  )

For catch private url request you have to create receiver for ``privateurl_ok`` signal::

  from django.dispatch import receiver
  from dju_privateurl.signals import privateurl_ok, privateurl_fail

  @receiver(privateurl_ok)
  def registration_confirm(request, obj, action, **kwargs):
      if action != 'registration-confirmation':
          return
      if obj.user:
          obj.user.registration_confirm(request=request)

if you want process invalid private url, you can create receiver for ``privateurl_fail`` signal::

  from django.dispatch import receiver
  from dju_privateurl.signals import privateurl_fail

  @receiver(privateurl_fail)
  def registration_confirm_fail(request, obj, action, **kwargs):
      if action != 'registration-confirmation':
          return
      if obj:
          # private url is expired or has exceeded ``hits_limit``
          pass
      else:
          # private url doesn't exists or token in url is not correct
          pass

After processing ``privateurl_ok`` signal will be redirected to root page ``/``.

After processing ``privateurl_fail`` signal will be raised ``Http404`` exception.

If you want change this logic you can return ``dict`` with key ``response`` in receiver::

  from django.shortcuts import redirect, render
  from django.dispatch import receiver
  from dju_privateurl.signals import privateurl_ok, privateurl_fail

  @receiver(privateurl_ok)
  def registration_confirm(request, obj, action, **kwargs):
      if action != 'registration-confirmation':
          return
      if obj.user:
          obj.user.registration_confirm(request=request)
          obj.user.login()
          return {'response': redirect('user_profile')}

  @receiver(privateurl_fail)
  def registration_confirm_fail(request, obj, action, **kwargs):
      if action != 'registration-confirmation':
          return
      return {'response': render(request, 'error_pages/registration_confirm_fail.html', status=404)}

For getting ``data`` you need use method ``get_data()``::

  @receiver(privateurl_ok)
  def registration_confirm(request, obj, action, **kwargs):
      ...
      data = obj.get_data()
      ...

========
Settings
========

``PRIVATEURL_URL_NAMESPACE`` -- namespace that you setted in ``urls.py``. By default it is ``privateurl``.

``PRIVATEURL_DEFAULT_TOKEN_SIZE`` -- default size of token that will be generated using ``create`` or ``generate_token`` methods. By default it is ``(8, 64)``.

``PRIVATEURL_DEFAULT_TOKEN_DASHED_PIECE_SIZE`` -- default number of size of pieces that joined by dash that using in ``create`` or ``generate_token`` methods. By default it is ``12``.
