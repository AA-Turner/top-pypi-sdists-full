# Copyright © 2026 Contrast Security, Inc.
# See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
from contrast.agent.assess.rules.triggers.session_timeout_rule import SessionTimeoutRule
from contrast.agent.policy.registry import register_trigger_rule


session_timeout_triggers = [
    {
        # default value is 1200s which is safe
        "module": "pyramid.session",
        "method_name": "BaseCookieSessionFactory",
        "source": "KWARG:timeout",
        "policy_patch": False,
    },
    {
        # WSGI pluggable for sessions
        "module": "beaker.session",
        "class_name": "Session",
        "method_name": "__init__",
        "source": "KWARG:timeout",
        "unsafe_default": True,
    },
    {
        # Used by bottle for sessions
        "module": "bottle_session",
        "class_name": "Session",
        "method_name": "__init__",
        "source": "ARG_2,KWARG:cookie_lifetime",
        "unsafe_default": True,
    },
    {
        "module": "falcon",
        "class_name": "Response",
        "method_name": "set_cookie",
        "source": "KWARG:max_age,KWARG:expires",
    },
    {
        # Used by fastapi for cookies
        "module": "starlette.responses",
        "class_name": "Response",
        "method_name": "set_cookie",
        "source": "KWARG:expires,KWARG:max_age",
    },
    {
        "module": "starlette.middleware.sessions",
        "class_name": "SessionMiddleware",
        "method_name": "__init__",
        "source": "KWARG:max_age",
        "unsafe_default": True,
    },
    {
        # Set custom response cookie and set its expires or max_age attribute
        "module": "aiohttp.web",
        "class_name": "Response",
        "method_name": "set_cookie",
        "source": "KWARG:expires,KWARG:max_age",
        "unsafe_default": True,
    },
]


register_trigger_rule(
    SessionTimeoutRule.from_nodes("session-timeout", session_timeout_triggers)
)
