# Copyright © 2026 Contrast Security, Inc.
# See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
from contrast.agent.assess.rules.dataflow_rule import DataflowRule
from contrast.agent.policy.registry import register_trigger_rule

unvalidated_redirect_triggers = [
    {
        "module": "django.http.response",
        "class_name": "HttpResponseRedirectBase",
        "method_name": "__init__",
        "source": "ARG_0,KWARG:redirect_to",
    },
    {
        # Base class for redirects in pyramid
        "module": "pyramid.httpexceptions",
        "class_name": "_HTTPMove",
        "method_name": "__init__",
        "source": "ARG_0,KWARG:location",
    },
    {
        # Base class for redirects in webob. Not the same as pyramid
        "module": "webob.exc",
        "class_name": "_HTTPMove",
        "method_name": "__init__",
        "source": "ARG_4,KWARG:location",
    },
    {
        "module": ["werkzeug.utils", "quart.utils"],
        "method_name": "redirect",
        "source": "ARG_0,KWARG:location",
    },
    {
        "module": "bottle",
        "method_name": "redirect",
        "source": "ARG_0,KWARG:url",
    },
    {
        "module": "falcon",
        "class_name": [
            "HTTPMovedPermanently",
            "HTTPFound",
            "HTTPSeeOther",
            "HTTPTemporaryRedirect",
            "HTTPPermanentRedirect",
        ],
        "method_name": "__init__",
        "source": "ARG_0,KWARG:location",
    },
    {
        # Used by fastapi for redirect responses
        "module": "starlette.responses",
        "class_name": "RedirectResponse",
        "method_name": "__init__",
        "source": "ARG_0,KWARG:url",
        "action": "STARLETTE_REDIRECT",
    },
    {
        "module": "aiohttp.web_exceptions",
        "class_name": "_HTTPMove",
        "method_name": "__init__",
        "source": "ARG_0,KWARG:location",
    },
]


register_trigger_rule(
    DataflowRule.from_nodes(
        "unvalidated-redirect",
        unvalidated_redirect_triggers,
        disallowed_tags=["URL_ENCODED"],
    )
)
