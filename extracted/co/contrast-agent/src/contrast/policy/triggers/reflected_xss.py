# Copyright © 2026 Contrast Security, Inc.
# See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
from contrast.agent.assess.rules.dataflow_rule import DataflowRule
from contrast.agent.policy.registry import register_trigger_rule


register_trigger_rule(
    DataflowRule.from_nodes(
        "reflected-xss",
        [],
        disallowed_tags=[
            "CUSTOM_ENCODED_REFLECTED_XSS",
            "CUSTOM_ENCODED",
            "CUSTOM_VALIDATED_REFLECTED_XSS",
            "CUSTOM_VALIDATED",
            "LIMITED_CHARS",
            "BASE64_ENCODED",
            "CSS_ENCODED",
            "CSV_ENCODED",
            "HTML_ENCODED",
            "JAVASCRIPT_ENCODED",
            "JAVA_ENCODED",
            "LDAP_ENCODED",
            "OS_ENCODED",
            "SQL_ENCODED",
            "URL_ENCODED",
            "VBSCRIPT_ENCODED",
            "XML_ENCODED",
            "XPATH_ENCODED",
            "XSS_ENCODED",
        ],
        required_tags=["CROSS_SITE"],
    )
)
