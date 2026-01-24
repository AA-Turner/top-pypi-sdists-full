# Copyright © 2026 Contrast Security, Inc.
# See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
from contrast.agent.assess.rules.triggers.httponly_rule import HttpOnlyRule
from contrast.agent.policy.registry import register_trigger_rule


httponly_triggers = [
    {
        "module": "pyramid.session",
        "method_name": "BaseCookieSessionFactory",
        "source": "KWARG:httponly",
        "policy_patch": False,
        "unsafe_default": True,
    },
    {
        # WSGI pluggable for sessions",
        "module": "beaker.session",
        "class_name": "Session",
        "method_name": "__init__",
        "source": "KWARG:httponly",
        "unsafe_default": True,
    },
    {
        # Used by bottle for sessions
        "module": "bottle_session",
        "class_name": "Session",
        "method_name": "__init__",
        "source": "ARG_4,KWARG:cookie_httponly",
        "unsafe_default": True,
    },
    {
        # Used by fastapi for cookies
        "module": "starlette.responses",
        "class_name": "Response",
        "method_name": "set_cookie",
        "source": "ARG_8,KWARG:httponly",
        "unsafe_default": True,
    },
    {
        # Sets custom response cookie and set its secure attribute
        "module": "falcon",
        "class_name": "Response",
        "method_name": "set_cookie",
        "source": "KWARG:http_only",
    },
    {
        # Sets custom response cookie and set its secure attribute
        "module": "aiohttp.web",
        "class_name": "Response",
        "method_name": "set_cookie",
        "source": "KWARG:httponly",
    },
]


register_trigger_rule(
    HttpOnlyRule.from_nodes(
        "httponly",
        httponly_triggers,
    )
)
