# Copyright © 2026 Contrast Security, Inc.
# See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
from contrast.agent.assess.rules.dataflow_rule import DataflowRule
from contrast.agent.policy.registry import register_trigger_rule

DISALLOWED_TAGS = [
    "CUSTOM_ENCODED_XXE",
    "CUSTOM_ENCODED",
    "CUSTOM_VALIDATED_XXE",
    "CUSTOM_VALIDATED",
    "LIMITED_CHARS",
    "XMLIF_VALIDATED_XXE",
]

xxe_triggers = [
    {
        "module": "lxml.etree",
        "method_name": "fromstring",
        "source": "ARG_0,KWARG:text",
        "action": "FROMSTRING",
        "protect_mode": True,
    },
    {
        "module": "xml.dom.pulldom",
        "method_name": "parseString",
        "source": "ARG_0,KWARG:string",
        "protect_mode": True,
    },
    {
        "module": "xml.sax",
        "method_name": "parseString",
        "source": "ARG_0,KWARG:string",
        "protect_mode": True,
    },
]

register_trigger_rule(
    DataflowRule.from_nodes(
        "xxe",
        xxe_triggers,
        disallowed_tags=DISALLOWED_TAGS,
    )
)
