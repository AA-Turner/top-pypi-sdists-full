# Copyright © 2026 Contrast Security, Inc.
# See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
from contrast.agent.assess.rules.dataflow_rule import DataflowRule
from contrast.agent.policy.registry import register_trigger_rule


DISALLOWED_TAGS = [
    "CUSTOM_ENCODED_TRUST_BOUNDARY_VIOLATION",
    "CUSTOM_ENCODED",
    "CUSTOM_VALIDATED_TRUST_BOUNDARY_VIOLATION",
    "CUSTOM_VALIDATED",
    "LIMITED_CHARS",
]


untrusted_deserialization_triggers = [
    {
        "module": "marshal",
        "method_name": ["load", "loads"],
        # does not accept kwargs
        "source": "ARG_0",
        "protect_mode": True,
    },
    {
        "module": "pickle",
        "method_name": "load",
        "source": "ARG_0,KWARG:file",
        "protect_mode": True,
    },
    {
        "module": "pickle",
        "method_name": "loads",
        "source": "ARG_0,KWARG:data",
        "protect_mode": True,
    },
    {
        "module": "yaml.loader",
        "class_name": "BaseLoader",
        "method_name": "__init__",
        "source": "ARG_0,KWARG:stream",
        "protect_mode": True,
    },
    {
        "module": "yaml.loader",
        "class_name": ["Loader", "UnsafeLoader", "FullLoader"],
        "method_name": "__init__",
        "source": "ARG_0,KWARG:stream",
        "protect_mode": True,
    },
]


register_trigger_rule(
    DataflowRule.from_nodes(
        "untrusted-deserialization",
        untrusted_deserialization_triggers,
        disallowed_tags=DISALLOWED_TAGS,
    )
)
