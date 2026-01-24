# Copyright © 2026 Contrast Security, Inc.
# See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
from contrast.agent.assess.rules.dataflow_rule import DataflowRule
from contrast.agent.policy.registry import register_trigger_rule


DISALLOWED_TAGS = [
    "CUSTOM_ENCODED_CMD_INJECTION",
    "CUSTOM_ENCODED",
    "CUSTOM_VALIDATED_CMD_INJECTION",
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
]


cmd_injection_triggers = [
    {
        "module": "os",
        "method_name": "popen",
        "source": "ARG_0,KWARG:cmd",
        "protect_mode": True,
    },
    {
        "module": "os",
        "method_name": "system",
        "source": "ARG_0,KWARG:command",
        "protect_mode": True,
    },
    {
        "module": "subprocess",
        "method_name": ["call", "check_call", "check_output"],
        "source": "ARG_0,KWARG:args",
        "action": "SUBPROCESS",
        "protect_mode": True,
    },
    {
        "module": "subprocess",
        "class_name": "Popen",
        "method_name": "__init__",
        "instance_method": True,
        "source": "ARG_0,KWARG:args",
        "action": "SUBPROCESS",
        "protect_mode": True,
    },
    {
        "module": "os",
        "method_name": ["spawnv", "spawnvp", "spawnve", "spawnvpe"],
        "source": "ARG_1,KWARG:file,ARG_2,KWARG:args",
        "protect_mode": True,
    },
    {
        "module": "os",
        "method_name": ["execv", "execvp", "execve", "execvpe"],
        "source": "ARG_0,KWARG:file,ARG_1,KWARG:args",
        "protect_mode": True,
    },
]


register_trigger_rule(
    DataflowRule.from_nodes(
        "cmd-injection",
        cmd_injection_triggers,
        disallowed_tags=DISALLOWED_TAGS,
    )
)
