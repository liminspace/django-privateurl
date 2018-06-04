import json
import random
import datetime
from django.conf import settings
try:
    from django.urls import reverse
except ImportError:
    from django.core.urlresolvers import reverse
from django.core.validators import RegexValidator
from django.db import models, IntegrityError
from django.db import transaction
from django.utils import timezone
from django.utils.crypto import get_random_string
from django.utils.translation import ugettext_lazy as _
from . import settings as purl_settings


class PrivateUrlManager(models.Manager):
    def get_or_none(self, action, token):
        try:
            return self.select_related('user').get(action=action, token=token)
        except self.model.DoesNotExist:
            pass


class PrivateUrl(models.Model):
    TOKEN_MIN_SIZE = 8
    TOKEN_MAX_SIZE = 64

    user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_('user'), null=True, blank=True,
                             on_delete=models.CASCADE)
    action = models.SlugField(verbose_name=_('action'), max_length=40, db_index=True,
                              validators=[RegexValidator(r'^[-_a-zA-Z0-9]+$')])
    token = models.SlugField(verbose_name=_('token'), max_length=TOKEN_MAX_SIZE,
                             validators=[RegexValidator(r'^[-a-zA-Z0-9]+$')])
    expire = models.DateTimeField(verbose_name=_('expire'), null=True, blank=True, db_index=True)
    data = models.TextField(verbose_name=_('data'), blank=True)
    created = models.DateTimeField(verbose_name=_('created'), auto_now_add=True, db_index=True)
    hits_limit = models.PositiveIntegerField(verbose_name=_('hits limit'), default=1,
                                             help_text=_('Set 0 to unlimited.'))
    hit_counter = models.PositiveIntegerField(verbose_name=_('hit counter'), default=0)
    first_hit = models.DateTimeField(verbose_name=_('first hit'), null=True, blank=True)
    last_hit = models.DateTimeField(verbose_name=_('last hit'), null=True, blank=True)
    auto_delete = models.BooleanField(verbose_name=_('auto delete'), default=False,
                                      help_text=_('Delete object if it can no longer be used.'))

    objects = PrivateUrlManager()

    class Meta:
        db_table = 'privateurl_privateurl'
        ordering = ('-created',)
        unique_together = ('action', 'token')
        verbose_name = _('private url')
        verbose_name_plural = _('private urls')

    def get_data(self):
        if self.data != '':
            return json.loads(self.data)

    def set_data(self, data):
        if data is None:
            self.data = ''
        else:
            self.data = json.dumps(data, sort_keys=True)

    @classmethod
    def create(cls, action, user=None, expire=None, data=None, hits_limit=1, auto_delete=False,
               token_size=None, replace=False, dashed_piece_size=None):
        """
        Create new object PrivateUrl.
        action - name of action (slug)
        user - user object or None
        expire - expire time, datetime, timedelta or None for disable time limit
        data - additional data that, any object that cant dumps as standard json
        hits_limit - limit of request hits, int (0 - ulimited)
        auto_delete - auto remove when url will be not available, bool
        token_size - length of token, tuple (min, max) or static int,
            None set default value from settings.PRIVATEURL_DEFAULT_TOKEN_SIZE
        replace - remove exist object for user and action before creating, bool
        dashed_piece_size - split token with dash every N symbols, int,
            None set default value from settings.PRIVATEURL_DEFAULT_TOKEN_DASHED_PIECE_SIZE
        """
        if replace and user:
            cls.objects.filter(action=action, user=user).delete()
        if isinstance(expire, datetime.timedelta):
            expire = timezone.now() + expire
        max_tries, n = 20, 0
        while True:
            try:
                token = cls.generate_token(size=token_size, dashed_piece_size=dashed_piece_size)
                obj = PrivateUrl(user=user, action=action, token=token, expire=expire,
                                 hits_limit=hits_limit, auto_delete=auto_delete)
                obj.set_data(data)
                with transaction.atomic():
                    obj.save()
                return obj
            except IntegrityError:
                n += 1
                if n > max_tries:
                    raise RuntimeError("Failed to create PrivateUrl object (action={}, token_size={})".format(
                        action, token_size
                    ))

    def is_available(self, dt=None):
        """
        Return True if object can be used.
        """
        if self.expire and self.expire <= (dt or timezone.now()):
            return False
        if self.hits_limit and self.hits_limit <= self.hit_counter:
            return False
        return True

    def hit_counter_inc(self):
        obj_is_exists = self.pk is not None
        now = timezone.now()
        self.hit_counter += 1
        if self.auto_delete and not self.is_available(dt=now):
            if obj_is_exists:
                self.delete()
            return
        uf = {'hit_counter', 'last_hit'}
        if not self.first_hit:
            self.first_hit = now
            uf.add('first_hit')
        self.last_hit = now
        if obj_is_exists:
            self.save(update_fields=uf)

    @classmethod
    def generate_token(cls, size=None, dashed_piece_size=None):
        """
        Generate new unique token.
        size - length of token, tuple (min, max) or static int,
            None set default value from settings.PRIVATEURL_DEFAULT_TOKEN_SIZE
        dashed_piece_size - split token with dash every N symbols, int,
            None set default value from settings.PRIVATEURL_DEFAULT_TOKEN_DASHED_PIECE_SIZE
        """
        if size is None:
            size = purl_settings.PRIVATEURL_DEFAULT_TOKEN_SIZE

        if dashed_piece_size is None:
            dashed_piece_size = purl_settings.PRIVATEURL_DEFAULT_TOKEN_DASHED_PIECE_SIZE

        if not isinstance(size, (int, list, tuple)):
            raise AttributeError('Attr size must be int, list or tuple.')

        size = (size, size) if isinstance(size, int) else tuple(size)

        if len(size) != 2:
            raise AttributeError('Attr size must contains two values.')

        for v in size:
            if not isinstance(v, int) or not (cls.TOKEN_MIN_SIZE <= v <= cls.TOKEN_MAX_SIZE):
                raise AttributeError('Attr size must contains values between {} and {}.'.format(
                    cls.TOKEN_MIN_SIZE, cls.TOKEN_MAX_SIZE
                ))

        if size[0] > size[1]:
            raise AttributeError('Attr size has incorrect values: first value must be less than second one.')

        if not isinstance(dashed_piece_size, int):
            raise AttributeError('Attr dash_split_each must be int.')
        elif dashed_piece_size < 0:
            raise AttributeError('Attr dash_split_each must be greater or equal 0.')

        if size[0] != size[1]:
            random.seed(get_random_string(length=100))
            _size = random.randint(*size)
        else:
            _size = size[0]

        token = get_random_string(length=_size)
        if dashed_piece_size:
            n = dashed_piece_size
            while n < len(token):
                token = token[:n] + '-' + token[n:]
                n += dashed_piece_size + 1
            token = token[:_size].rstrip('-')

        return token

    def get_absolute_url(self):
        return reverse('{}:privateurl'.format(purl_settings.PRIVATEURL_URL_NAMESPACE),
                       kwargs={'action': self.action, 'token': self.token})
