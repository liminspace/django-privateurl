from django.conf.urls import url
from . import views


urlpatterns = [
    url(
        r'^(?P<action>[\-_a-zA-Z0-9]{1,40})/(?P<token>[\-a-zA-Z0-9]{1,64})$',
        views.privateurl_view,
        name='privateurl'
    ),
]
