from django.contrib import admin
from django.utils.translation import gettext, ugettext_lazy as _
from .models import PrivateUrl


class PrivateUrlAdmin(admin.ModelAdmin):
    list_display = ('action_with_token', 'user', 'created', 'expire', 'used', 'available')
    list_filter = ('action',)
    list_select_related = ('user',)
    raw_id_fields = ('user',)

    def __init__(self, *args, **kwargs):
        super(PrivateUrlAdmin, self).__init__(*args, **kwargs)

    def action_with_token(self, obj):
        return '{}/{}'.format(obj.action, obj.token)
    action_with_token.short_description = _('action/token')

    def used(self, obj):
        return '{} / {}'.format(obj.hit_counter, obj.hits_limit or gettext('unlimited'))
    used.short_description = _('used')

    def available(self, obj):
        return obj.is_available()
    used.short_description = _('available')
    available.boolean = True


admin.site.register(PrivateUrl, PrivateUrlAdmin)
