from django.http.response import Http404, HttpResponseRedirect
from .models import PrivateUrl
from .signals import privateurl_ok, privateurl_fail


def privateurl_view(request, action, token):
    obj = PrivateUrl.objects.get_or_none(action, token)
    ok = False
    if not obj or not obj.is_available():
        results = privateurl_fail.send(PrivateUrl, request=request, obj=obj, action=action)
    else:
        results = privateurl_ok.send(PrivateUrl, request=request, obj=obj, action=action)
        obj.hit_counter_inc()
        ok = True
    for receiver, result in results:
        if isinstance(result, dict):
            if 'response' in result:
                return result['response']
    if not ok:
        raise Http404
    return HttpResponseRedirect('/')
