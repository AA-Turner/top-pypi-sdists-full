# Copyright © 2026 Contrast Security, Inc.
# See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
import importlib
from importlib.metadata import PackageNotFoundError

from contrast.agent.assess.rules.dataflow_rule import DataflowRule
from contrast.agent.policy.registry import register_trigger_rule


DISALLOWED_TAGS = [
    "CUSTOM_ENCODED_TRUST_BOUNDARY_VIOLATION",
    "CUSTOM_VALIDATED_TRUST_BOUNDARY_VIOLATION",
    "CUSTOM_VALIDATED",
    "LIMITED_CHARS",
    "BASE64_ENCODED",
    "CSS_ENCODED",
    "CSV_ENCODED",
    "HTML_ENCODED",
    "JAVASCRIPT_ENCODED",
    "JAVA_ENCODED",
    "LDAP_ENCODED",
    "OS_ENCODED",
    "SQL_ENCODED",
    "URL_ENCODED",
    "VBSCRIPT_ENCODED",
    "XML_ENCODED",
    "XPATH_ENCODED",
]


trust_boundary_violation_triggers = [
    {
        # Used by bottle for sessions. No keyword arguments
        "module": "bottle_session",
        "class_name": "Session",
        "method_name": "__setitem__",
        "source": "ARG_1",
    },
    {
        # WSGI pluggable for sessions. No keyword arguments
        "module": "beaker.session",
        "class_name": "Session",
        "method_name": "__setitem__",
        "source": "ARG_1",
    },
    {
        # WSGI pluggable for sessions. No keyword arguments
        "module": "beaker.session",
        "class_name": "Session",
        "method_name": "setdefault",
        "source": "ARG_1",
    },
    {
        "module": "django.contrib.sessions.backends.base",
        "class_name": "SessionBase",
        "method_name": ["__setitem__", "setdefault"],
        # no keyword arguments
        "source": "ARG_1",
    },
    {
        "module": "flask.sessions",
        "class_name": "SecureCookieSession",
        "method_name": ["__setitem__", "setdefault"],
        # no keyword arguments
        "source": "ARG_1",
    },
    {
        "module": "pyramid.session",
        "class_name": "CookieSession",
        "method_name": ["__setitem__", "setdefault"],
        # no keyword arguments
        "source": "ARG_1",
        "policy_patch": False,
    },
    {
        # No kwargs. This is a fake node used for triggering trust-boundary-
        # -violation for proxied dictionaries returned by
        # starlette.requests.Request.session. class_name is sort of nonsense
        # here. see starlette_patches.py
        "module": "starlette.sessions",
        "class_name": "dict",
        "method_name": "__setitem__",
        "source": "ARG_1",
        "policy_patch": False,
    },
    {
        # Used by aiohttp for sessions. No keyword arguments
        "module": "aiohttp_session",
        "class_name": "Session",
        "method_name": "__setitem__",
        "source": "ARG_1",
    },
]

# Newer versions of Quart more closely mirror Flask. Based on TestTrustBoundaryViolationTrigger, they don't require
# these patches and trying to back them out is actually problematic for our testing.
# TODO: PYT-3115 if we no longer reverse patches/ check for it, this can just always be added. Scope should handle any
#   issues from double patching.
try:
    if importlib.metadata.version("quart") < "0.19":
        trust_boundary_violation_triggers.append(
            {
                "module": "quart.sessions",
                "class_name": "SecureCookieSession",
                "method_name": "__setitem__",
                # no keyword arguments
                "source": "ARG_1",
            }
        )
        trust_boundary_violation_triggers.append(
            {
                "module": "quart.sessions",
                "class_name": "SecureCookieSession",
                "method_name": "setdefault",
                # no keyword arguments
                "source": "ARG_1",
            }
        )
except PackageNotFoundError:
    # If quart doesn't exist in the app, we don't need to patch
    pass

register_trigger_rule(
    DataflowRule.from_nodes(
        "trust-boundary-violation",
        trust_boundary_violation_triggers,
        disallowed_tags=DISALLOWED_TAGS,
    )
)
