# Copyright © 2026 Contrast Security, Inc.
# See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
from contrast.agent.policy.registry import register_source_nodes
from contrast.agent.policy.utils import CompositeNode

quart_sources = [
    CompositeNode(
        {
            "module": "quart.wrappers.request",
            "class_name": "Request",
        },
        [
            {
                "method_name": ["base_url", "host_url", "url", "url_root"],
                "node_type": "URI",
                "tags": ["CROSS_SITE"],
            },
            {
                "method_name": "get_data",
                "target": "RETURN",
                "node_type": "BODY",
                "tags": ["CROSS_SITE"],
            },
        ],
    ),
    {
        "module": "quart.wrappers.request",
        "class_name": "Body",
        "method_name": "__anext__",
        "node_type": "BODY",
        "tags": ["CROSS_SITE"],
    },
]


register_source_nodes(quart_sources)
