# Copyright © 2026 Contrast Security, Inc.
# See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
from contrast.patches.middleware.django import initialize_django
from contrast.utils.deprecated_middleware import deprecated_wsgi

WSGIMiddleware = deprecated_wsgi("django")


class DjangoWSGIMiddleware(WSGIMiddleware):
    def __init__(self, *args, **kwargs):
        initialize_django()
        super().__init__(*args, **kwargs)
