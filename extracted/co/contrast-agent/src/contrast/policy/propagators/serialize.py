# Copyright © 2026 Contrast Security, Inc.
# See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
from contrast.agent.policy.registry import register_propagation_nodes


serialize_propagators = [
    {
        "module": ["json", "simplejson"],
        "method_name": "dumps",
        "source": "ARG_0,KWARG:obj",
        "target": "RETURN",
        "action": "JSON",
    },
    {
        "module": ["json", "simplejson"],
        "method_name": "loads",
        "source": "ARG_0,KWARG:s",
        "target": "RETURN",
        "action": "JSON",
    },
    {
        "module": "pickle",
        "method_name": "dumps",
        "source": "ARG_0,KWARG:obj",
        "target": "RETURN",
        "action": "SPLAT",
    },
    {
        "module": "yaml",
        "method_name": "dump",
        "source": "ARG_0,KWARG:data",
        "target": "RETURN",
        "action": "SPLAT",
    },
    {
        "module": "yaml",
        "method_name": "dump_all",
        "source": "ARG_0,KWARG:documents",
        "target": "RETURN",
        "action": "SPLAT",
    },
]


register_propagation_nodes(serialize_propagators)
