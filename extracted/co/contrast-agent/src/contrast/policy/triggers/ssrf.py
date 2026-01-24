# Copyright © 2026 Contrast Security, Inc.
# See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
from contrast.agent.assess.rules.dataflow_rule import DataflowRule
from contrast.agent.policy.registry import register_trigger_rule
from contrast.agent.policy.utils import CompositeNode


DISALLOWED_TAGS = [
    "CUSTOM_ENCODED_SSRF",
    "CUSTOM_ENCODED",
    "CUSTOM_VALIDATED_SSRF",
    "CUSTOM_VALIDATED",
    "LIMITED_CHARS",
]

ssrf_triggers = [
    CompositeNode(
        {
            "action": "SSRF",
        },
        [
            {
                "module": "urllib.request",
                "method_name": "urlopen",
                "source": "ARG_0,KWARG:url",
                "protect_mode": True,
            },
            {
                # Serves to trigger both sync and async http.get, http.post, etc
                "module": "httpx._client",
                "class_name": "BaseClient",
                "method_name": "build_request",
                "source": "ARG_1,KWARG:url",
                "protect_mode": True,
            },
            {
                "module": "aiohttp",
                "class_name": "ClientSession",
                "method_name": "_request",
                # ARG_0 is HTTP method. They're all defined in their file hdrs.py.
                # ARG_1 is the url. Could be both string and 'URL' class which comes from a yarl module
                "source": "ARG_0,ARG_1,KWARG:method,KWARG:str_or_url",
                "protect_mode": True,
            },
        ],
    ),
    {
        "module": "http.client",
        "class_name": "HTTPConnection",
        "method_name": "__init__",
        "source": "ARG_0,KWARG:host",
        "action": "DEFAULT",
    },
    {
        # This also serves as a trigger for the request method
        "module": "http.client",
        "class_name": "HTTPConnection",
        "method_name": "putrequest",
        # ARG_0 is HTTP method, so no regex is used to evaluate
        # ARG_1 is a path + querystring only, which isn't vulnerable to SSRF
        "source": "ARG_0,KWARG:method",
        "action": "DEFAULT",
        "protect_mode": True,
    },
    {
        # This is the underlying call for functions like requests.get, etc.
        # This function calls Session.request under the hood, so it's
        # technically duplicated by the Session.request node below, but it
        # might lead to better storytelling to keep it.
        "module": "requests.api",
        "method_name": "request",
        "source": "ARG_1,KWARG:url",
        "action": "SSRF",
    },
    {
        # This is the underlying call for methods like Session.get, etc.
        "module": "requests.sessions",
        "class_name": "Session",
        "method_name": "request",
        "source": "ARG_1,KWARG:url",
        "action": "SSRF",
    },
    {
        "module": "requests.models",
        "class_name": "Request",
        "method_name": "__init__",
        "source": "ARG_1,KWARG:url",
        "action": "SSRF",
    },
]

register_trigger_rule(
    DataflowRule.from_nodes(
        "ssrf",
        ssrf_triggers,
        disallowed_tags=DISALLOWED_TAGS,
    )
)
