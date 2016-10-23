from django.dispatch import Signal


privateurl_ok = Signal(providing_args=['request', 'obj', 'action'])
privateurl_fail = Signal(providing_args=['request', 'obj', 'action'])
