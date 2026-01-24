# Copyright © 2026 Contrast Security, Inc.
# See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
from contrast.agent.agent_state import detected_deprecated_middleware
from contrast.asgi.middleware import ASGIMiddleware
from contrast.wsgi.middleware import WSGIMiddleware


def deprecated_wsgi(framework: str):
    class DeprecatedWSGIMiddleware(WSGIMiddleware):
        def __init__(self, *args, **kwargs):
            detected_deprecated_middleware(framework=framework, is_asgi=False)
            super().__init__(*args, **kwargs, framework_name=framework)

    return DeprecatedWSGIMiddleware


def deprecated_asgi(framework: str):
    class DeprecatedASGIMiddleware(ASGIMiddleware):
        def __init__(self, *args, **kwargs):
            detected_deprecated_middleware(framework=framework, is_asgi=True)
            super().__init__(*args, **kwargs, framework_name=framework)

    return DeprecatedASGIMiddleware
