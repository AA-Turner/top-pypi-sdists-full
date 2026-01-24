# Copyright © 2026 Contrast Security, Inc.
# See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
from contrast.agent.assess.rules.dataflow_rule import DataflowRule
from contrast.agent.policy.registry import register_trigger_rule


DISALLOWED_TAGS = [
    "CUSTOM_ENCODED_XPATH_INJECTION",
    "CUSTOM_ENCODED",
    "CUSTOM_VALIDATED_XPATH_INJECTION",
    "CUSTOM_VALIDATED",
    "LIMITED_CHARS",
    "XPATH_ENCODED",
]


xpath_injection_triggers = [
    {
        "module": "xml.etree.ElementTree",
        "class_name": "Element",
        "method_name": ["find", "findall", "findtext"],
        "source": "ARG_0",
    },
    {
        "module": "lxml.etree",
        "class_name": "_Element",
        "method_name": ["find", "findall", "findtext", "xpath"],
        "source": "ARG_0",
    },
    {
        "module": "lxml.etree",
        "class_name": "_ElementTree",
        "method_name": "xpath",
        "source": "ARG_0",
    },
    {
        "module": "lxml.etree",
        "class_name": "XPath",
        "method_name": "__init__",
        "source": "ARG_0",
        "policy_patch": False,
    },
    {
        "module": "lxml.etree",
        "class_name": "XPathElementEvaluator",
        "method_name": "__call__",
        "source": "ARG_0",
        "policy_patch": False,
    },
    {
        "module": "lxml.etree",
        "class_name": "XPathDocumentEvaluator",
        "method_name": "__call__",
        "source": "ARG_0",
        "policy_patch": False,
    },
]


register_trigger_rule(
    DataflowRule.from_nodes(
        "xpath-injection",
        xpath_injection_triggers,
        disallowed_tags=DISALLOWED_TAGS,
    )
)
