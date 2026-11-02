# Copyright © 2026 Contrast Security, Inc.
# See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
from contrast.agent.policy.registry import register_propagation_nodes
from contrast.agent.policy.utils import CompositeNode

os_propagators = [
    CompositeNode(
        {
            "module": "os",
        },
        [
            {
                "method_name": "scandir",
                "source": "ARG_0,KWARG:path",
                "action": "SPLAT",
                "target": "RETURN",
                "policy_patch": False,
            },
        ],
    )
]

register_propagation_nodes(os_propagators)
