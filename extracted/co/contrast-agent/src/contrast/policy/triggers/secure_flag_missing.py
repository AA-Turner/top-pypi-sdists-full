# Copyright © 2026 Contrast Security, Inc.
# See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
from contrast.agent.assess.rules.triggers.secure_flag_missing_rule import (
    SecureFlagMissingRule,
)
from contrast.agent.policy.registry import register_trigger_rule


secure_flag_missing_triggers = [
    {
        "module": "pyramid.session",
        "method_name": "BaseCookieSessionFactory",
        "source": "KWARG:secure",
        "unsafe_default": True,
        "policy_patch": False,
    },
    {
        # WSGI pluggable for sessions
        "module": "beaker.session",
        "class_name": "Session",
        "method_name": "__init__",
        "source": "KWARG:secure",
        "unsafe_default": True,
    },
    {
        # Set custom response cookie and set its secure attribute
        "module": "falcon",
        "class_name": "Response",
        "method_name": "set_cookie",
        "source": "KWARG:secure",
        "unsafe_default": True,
    },
    {
        # Used by bottle for sessions
        "module": "bottle_session",
        "class_name": "Session",
        "method_name": "__init__",
        "source": "ARG_4,KWARG:cookie_secure",
        "unsafe_default": True,
    },
    {
        # Used by fastapi for cookies
        "module": "starlette.responses",
        "class_name": "Response",
        "method_name": "set_cookie",
        "source": "ARG_7,KWARG:secure",
        "unsafe_default": True,
    },
    {
        # Set custom response cookie and set its secure attribute
        "module": "aiohttp.web",
        "class_name": "Response",
        "method_name": "set_cookie",
        "source": "KWARG:secure",
        "unsafe_default": True,
    },
]


register_trigger_rule(
    SecureFlagMissingRule.from_nodes(
        "secure-flag-missing",
        secure_flag_missing_triggers,
    )
)
