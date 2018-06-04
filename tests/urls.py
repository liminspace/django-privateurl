import django
from django.contrib import admin


if django.VERSION >= (2, 0):
    from django.urls import path, include
    urlpatterns = [
        path('admin/', admin.site.urls),
        path('private/', include(('privateurl.urls', 'privateurl'), namespace='purl')),
    ]
else:
    from django.conf.urls import include, url
    urlpatterns = [
        url(r'^admin/', include(admin.site.urls)),
        url(r'^private/', include('privateurl.urls', namespace='purl')),
    ]
