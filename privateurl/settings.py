from django.conf import settings

PRIVATEURL_URL_NAMESPACE = getattr(settings, 'PRIVATEURL_URL_NAMESPACE', 'privateurl')
PRIVATEURL_DEFAULT_TOKEN_SIZE = getattr(settings, 'PRIVATEURL_DEFAULT_TOKEN_SIZE', (8, 64))
PRIVATEURL_DEFAULT_TOKEN_DASHED_PIECE_SIZE = getattr(settings, 'PRIVATEURL_DEFAULT_TOKEN_DASHED_PIECE_SIZE', 12)
