# Copyright © 2026 Contrast Security, Inc.
# See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
from contrast.asgi.middleware import ASGIMiddleware


class FastApiMiddleware(ASGIMiddleware):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs, framework_name="fastapi")
