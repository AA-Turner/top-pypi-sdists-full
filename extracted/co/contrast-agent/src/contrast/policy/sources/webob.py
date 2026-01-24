# Copyright © 2026 Contrast Security, Inc.
# See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
from contrast.agent.policy.registry import register_source_nodes
from contrast.agent.policy.utils import CompositeNode


webob_sources = [
    CompositeNode(
        {
            "module": "webob.multidict",
            "class_name": "MultiDict",
        },
        [
            {
                "method_name": ["__getitem__", "getall", "mixed", "dict_of_lists"],
                "node_type": "PARAMETER",
                "tags": ["CROSS_SITE"],
            },
        ],
    ),
    CompositeNode(
        {
            "module": "webob.request",
            "class_name": "BaseRequest",
        },
        [
            {
                "method_name": "query_string",
                "node_type": "QUERYSTRING",
                "tags": ["NO_NEWLINES", "CROSS_SITE"],
            },
            {
                "method_name": "host_url",
                "node_type": "URI",
                "tags": ["NO_NEWLINES", "CROSS_SITE"],
            },
        ],
    ),
    {
        "module": "webob.headers",
        "class_name": "EnvironHeaders",
        "method_name": "__getitem__",
        "node_type": "HEADER",
        "tags": ["NO_NEWLINES"],
    },
    {
        "module": "webob.cookies",
        "class_name": "RequestCookies",
        "method_name": "__getitem__",
        "node_type": "COOKIE",
        "tags": ["NO_NEWLINES"],
    },
]


register_source_nodes(webob_sources)
