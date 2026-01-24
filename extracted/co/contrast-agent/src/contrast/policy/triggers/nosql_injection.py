# Copyright © 2026 Contrast Security, Inc.
# See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
from contrast.agent.assess.rules.dataflow_rule import DataflowRule
from contrast.agent.policy.registry import register_trigger_rule
from contrast.agent.policy.utils import CompositeNode


DISALLOWED_TAGS = [
    "CUSTOM_ENCODED_NOSQL_INJECTION",
    "CUSTOM_ENCODED",
    "CUSTOM_VALIDATED_NOSQL_INJECTION",
    "CUSTOM_VALIDATED",
    "LIMITED_CHARS",
    "JS_ENCODED",
]


nosql_triggers = [
    CompositeNode(
        {
            "module": "pymongo.collection",
            "protect_mode": True,
            "action": "PYMONGO",
        },
        [
            {
                "class_name": "Collection",
                "method_name": "find",
                "source": "ARG_0,KWARG:filter",
            },
            {
                "module": "pymongo.collection",
                "class_name": "Collection",
                "method_name": "insert_one",
                "source": "ARG_0,KWARG:document",
            },
            {
                "module": "pymongo.collection",
                "class_name": "Collection",
                "method_name": "insert_many",
                "source": "ARG_0,KWARG:documents",
            },
            {
                "module": "pymongo.collection",
                "class_name": "Collection",
                "method_name": "_delete_retryable",
                "source": "ARG_0,KWARG:criteria",
            },
            {
                "module": "pymongo.collection",
                "class_name": "Collection",
                "method_name": "_update_retryable",
                "source": "ARG_1,KWARG:document",
            },
        ],
    ),
]


register_trigger_rule(
    DataflowRule.from_nodes(
        "nosql-injection",
        nosql_triggers,
        disallowed_tags=DISALLOWED_TAGS,
    )
)
