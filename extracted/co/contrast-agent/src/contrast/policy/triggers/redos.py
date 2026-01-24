# Copyright © 2026 Contrast Security, Inc.
# See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
from contrast.agent.assess.rules.dataflow_rule import DataflowRule
from contrast.agent.policy.registry import register_trigger_rule
from contrast.agent.policy.utils import CompositeNode


DISALLOWED_TAGS = [
    "CUSTOM_ENCODED_REDOS",
    "CUSTOM_ENCODED",
    "CUSTOM_VALIDATED_REDOS",
    "CUSTOM_VALIDATED",
    "LIMITED_CHARS",
]


# This rule, like SSRF, has an accompanying action to enforce an extra level
# of assertion on the violation, so it may not always report, depending on the
# value reported.
# Like the propagation methods for Re::Match, it also requires custom patching
# to instrument properly.
# For all of these methods, ARG_0 is the pattern passed in to the re method,
# which we verify against the REDOS action for exploitability but we do not
# care about its origin so it doesn't matter if it's tracked.
redos_triggers = [
    CompositeNode(
        {
            "module": "re",
            "action": "REDOS",
        },
        [
            {
                "method_name": "match",
                # ARG_1 is the user input which we track and verify if untrusted
                "source": "ARG_1,KWARG:string",
            },
            {
                "module": "re",
                "class_name": "Pattern",
                "method_name": "match",
                # ARG_1 is the user input which we track and verify if untrusted
                # NOTE: because the redos action needs ARG_0 to analyze the pattern, the fact
                # this is an instance method node is ignored in the trigger logic.
                "source": "ARG_1,KWARG:string,KWARG:pattern",
                "policy_patch": False,
            },
            {
                "module": "re",
                "method_name": "search",
                # ARG_1 is the user input which we track and verify if untrusted
                "source": "ARG_1,KWARG:string",
            },
            {
                "module": "re",
                "class_name": "Pattern",
                "method_name": "search",
                # ARG_1 is the user input which we track and verify if untrusted
                # NOTE: because the redos action needs ARG_0 to analyze the pattern, the fact
                # this is an instance method node is ignored in the trigger logic.
                "source": "ARG_1,KWARG:string,KWARG:pattern",
                "policy_patch": False,
            },
            {
                "module": "re",
                "method_name": "finditer",
                # ARG_1 is the user input which we track and verify if untrusted
                "source": "ARG_1,KWARG:string",
            },
            {
                "module": "re",
                "class_name": "Pattern",
                "method_name": "finditer",
                # ARG_1 is the user input which we track and verify if untrusted
                # NOTE: because the redos action needs ARG_0 to analyze the pattern, the fact
                # this is an instance method node is ignored in the trigger logic.
                "source": "ARG_1,KWARG:string",
                "policy_patch": False,
            },
            {
                "module": "re",
                "method_name": "findall",
                # ARG_1 is the user input which we track and verify if untrusted
                "source": "ARG_1,KWARG:string",
            },
            {
                "module": "re",
                "class_name": "Pattern",
                "method_name": "findall",
                # ARG_1 is the user input which we track and verify if untrusted
                # NOTE: because the redos action needs ARG_0 to analyze the pattern, the fact
                # this is an instance method node is ignored in the trigger logic.
                "source": "ARG_1,KWARG:string,KWARG:source",
                "policy_patch": False,
            },
            {
                "module": "re",
                "method_name": "fullmatch",
                # ARG_1 is the user input which we track and verify if untrusted
                "source": "ARG_1,KWARG:string",
            },
            {
                "module": "re",
                "class_name": "Pattern",
                "method_name": "fullmatch",
                # NOTE: because the redos action needs ARG_0 to analyze the pattern, the fact
                # this is an instance method node is ignored in the trigger logic.
                "source": "ARG_1,KWARG:string",
                "policy_patch": False,
            },
            {
                "module": "re",
                "method_name": "sub",
                # ARG_2 is the user input which we track and verify if untrusted
                "source": "ARG_2,KWARG:string",
                "policy_patch": False,
            },
            {
                "module": "re",
                "class_name": "Pattern",
                "method_name": "sub",
                # NOTE: because the redos action needs ARG_0 to analyze the pattern, the fact
                # this is an instance method node is ignored in the trigger logic.
                "source": "ARG_2,KWARG:string",
                "policy_patch": False,
            },
            {
                "module": "re",
                "method_name": "subn",
                # ARG_2 is the user input which we track and verify if untrusted
                "source": "ARG_2,KWARG:string",
                "policy_patch": False,
            },
            {
                "module": "re",
                "class_name": "Pattern",
                "method_name": "subn",
                # NOTE: because the redos action needs ARG_0 to analyze the pattern, the fact
                # this is an instance method node is ignored in the trigger logic.
                "source": "ARG_2,KWARG:string",
                "policy_patch": False,
            },
            {
                "module": "re",
                "method_name": "split",
                "source": "ARG_1,KWARG:string,KWARG:source",
            },
            {
                "module": "re",
                "class_name": "Pattern",
                "method_name": "split",
                # NOTE: because the redos action needs ARG_0 to analyze the pattern, the fact
                # this is an instance method node is ignored in the trigger logic.
                "source": "ARG_1,KWARG:string",
                "policy_patch": False,
            },
        ],
    )
]


register_trigger_rule(
    DataflowRule.from_nodes(
        "redos",
        redos_triggers,
        disallowed_tags=DISALLOWED_TAGS,
    )
)
