from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class PrivateURLConfig(AppConfig):
    name = 'privateurl'
    verbose_name = _('Django Private URL')
