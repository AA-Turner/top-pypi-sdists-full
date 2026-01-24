# Copyright © 2026 Contrast Security, Inc.
# See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
from contrast.agent.assess.rules.dataflow_rule import DataflowRule
from contrast.agent.policy.registry import register_trigger_rule
from contrast.agent.policy.utils import CompositeNode


DISALLOWED_TAGS = [
    "CUSTOM_ENCODED_TRUST_BOUNDARY_VIOLATION",
    "CUSTOM_ENCODED",
    "CUSTOM_VALIDATED_TRUST_BOUNDARY_VIOLATION",
    "CUSTOM_VALIDATED",
    "LIMITED_CHARS",
]

unsafe_code_execution_triggers = [
    CompositeNode(
        {
            "module": "builtins",
            "policy_patch": False,
        },
        [
            {
                "method_name": ["exec", "eval"],
                # Takes no keyword arguments
                "source": "ARG_0",
            },
            {
                "method_name": "compile",
                "source": "ARG_0,KWARG:source",
            },
        ],
    ),
    {
        "module": "importlib",
        "method_name": "__import__",
        "source": "ARG_0,KWARG:name",
        # Not patched by policy since it's also instrumented for library analysis
        "policy_patch": False,
    },
]


register_trigger_rule(
    DataflowRule.from_nodes(
        "unsafe-code-execution",
        unsafe_code_execution_triggers,
        disallowed_tags=DISALLOWED_TAGS,
    )
)
