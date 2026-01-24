# Copyright © 2026 Contrast Security, Inc.
# See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
from contrast.agent.policy.registry import register_propagation_nodes
from contrast.agent.policy.utils import CompositeNode

re_propagators = [
    CompositeNode(
        {
            "module": "re",
            "target": "RETURN",
            # May be overridden by some individual nodes
            "policy_patch": False,
        },
        [
            {
                "method_name": "split",
                "source": "ARG_1,KWARG:string",
                "action": "REGEX_SPLIT",
                "policy_patch": True,
            },
            {
                "class_name": "Pattern",
                "method_name": "split",
                "source": "ARG_0,KWARG:string",
                "action": "REGEX_SPLIT",
            },
            {
                "method_name": ["sub", "subn"],
                "class_name": [None, "Pattern"],
                "source": "ARG_0,KWARG:string",
                "action": "NONE",
            },
            {
                # re.findall is a simple wrapper around re.Pattern.findall so this single
                # propagation node accounts for both
                "class_name": "Pattern",
                "method_name": "findall",
                "source": "ARG_0,KWARG:string",
                "action": "REGEX_FINDALL",
            },
            {
                "method_name": "escape",
                "source": "ARG_0,KWARG:pattern",
                "action": "SPLAT",
                "policy_patch": True,
            },
            {
                "class_name": "Match",
                "method_name": ["group", "groups", "groupdict"],
                "source": "OBJ",
                "action": "NONE",
            },
        ],
    )
]

register_propagation_nodes(re_propagators)
