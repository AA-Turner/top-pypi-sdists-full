# Copyright © 2026 Contrast Security, Inc.
# See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
from contrast.agent.assess.rules.dataflow_rule import DataflowRule
from contrast.agent.policy.registry import register_trigger_rule


DISALLOWED_TAGS = [
    "CUSTOM_VALIDATED",
]


prompt_injection_triggers = [
    {
        "module": "openai",
        "class_name": "ChatCompletion",
        "method_name": ["create", "acreate"],
        "action": "OPENAI",
        "source": "KWARG:messages",
    },
    {
        "module": "openai",
        "class_name": "Completion",
        "method_name": ["create", "acreate"],
        "action": "OPENAI",
        "source": "KWARG:prompt",
    },
]


register_trigger_rule(
    DataflowRule.from_nodes(
        "prompt-injection",
        prompt_injection_triggers,
        disallowed_tags=DISALLOWED_TAGS,
    )
)
