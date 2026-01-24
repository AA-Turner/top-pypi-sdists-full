# Copyright © 2026 Contrast Security, Inc.
# See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
from contrast.agent.policy.registry import register_propagation_nodes


register_propagation_nodes(
    [
        {
            "module": "glob",
            "method_name": "translate",
            "source": "ARG_0,KWARG:pathname",
            "target": "RETURN",
            "action": "SPLAT",
        },
    ]
)
