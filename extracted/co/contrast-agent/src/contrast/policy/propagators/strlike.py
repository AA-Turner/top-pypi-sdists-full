# Copyright © 2026 Contrast Security, Inc.
# See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
from contrast.agent.policy.registry import register_propagation_nodes
from contrast.agent.policy.utils import CompositeNode

strlike_propagators = [
    CompositeNode(
        {
            "module": "builtins",
            "class_name": ["str", "bytes", "bytearray"],
            "policy_patch": False,
            "instance_method": True,
            "source": "OBJ",  # This is the default, some specific nodes may override it
            "target": "RETURN",
        },
        [
            {
                "method_name": [
                    # `repeat` is string multiplication.
                    # TODO: PYT-1345 SPLAT makes `repeat` prone to FPs.
                    "repeat",
                    "translate",
                ],
                "action": "SPLAT",
            },
            {
                "method_name": [
                    "capitalize",
                    "casefold",
                    "lower",
                    "swapcase",
                    "title",
                    "upper",
                ],
                "action": "KEEP",
            },
            {
                "method_name": "ljust",
                "action": "APPEND",
            },
            {
                "method_name": ["zfill", "rjust"],
                "action": "PREPEND",
            },
            {
                "method_name": "center",
                "action": "CENTER",
            },
            {
                # replace() takes `count` (ARG_2) as a kwarg in python 3.13+ only
                "method_name": "replace",
                "source": "OBJ,ARG_1",
                "action": "REPLACE",
            },
            {
                "method_name": [
                    "strip",
                    "lstrip",
                    "rstrip",
                    "removeprefix",
                    "removesuffix",
                ],
                "action": "REMOVE",
            },
            {
                "method_name": ["subscript", "__getitem__"],
                "action": "SLICE",
            },
            {
                # join() takes no keyword arguments
                "method_name": "join",
                "source": "OBJ,ARG_0",
                "action": "JOIN",
            },
            {
                "method_name": [
                    "split",
                    "splitlines",
                    "rsplit",
                    "partition",
                    "rpartition",
                ],
                "source": "OBJ",
                "action": "SPLIT",
            },
            {
                # This is str(), bytes(), or bytearray().
                "instance_method": False,
                "method_name": "CAST",
                "source": "ARG_0,KWARG:object",
                "action": "SPLAT",
            },
            {
                "method_name": "__repr__",
                "action": "REPR",
            },
        ],
    ),
    CompositeNode(
        {
            "module": "builtins",
            "class_name": "str",
            "policy_patch": False,
            "instance_method": True,
            "target": "RETURN",
        },
        [
            {
                "method_name": "encode",
                "source": "OBJ",
                "action": "KEEP",
            },
            {
                "method_name": "format",
                "source": "OBJ,ALL_ARGS,ALL_KWARGS",
                "action": "FORMAT",
            },
            {
                # format_map() takes no keyword arguments
                "method_name": "format_map",
                "source": "OBJ,ALL_ARGS",
                "action": "FORMAT",
            },
        ],
    ),
    CompositeNode(
        {
            "module": "builtins",
            "class_name": ["bytes", "bytearray"],
            "policy_patch": False,
            "instance_method": True,
            "source": "OBJ",  # This is the default, some specific nodes may override it
            "target": "RETURN",
        },
        [
            {
                "method_name": "decode",
                "action": "KEEP",
            },
            {
                "method_name": "hex",
                "action": "SPLAT",
            },
            {
                # bytes.fromhex / bytearray.fromhex is called like a classmethod. It
                # isn't clear whether or not this should be an "instance_method" here -
                # but it also doesn't actually matter, because the string propagation
                # patches don't use that policy attribute. Wrapt handles this for us.
                "method_name": "fromhex",
                "source": "ARG_0",
                "action": "SPLAT",
            },
        ],
    ),
    {
        "module": "builtins",
        "class_name": "bytearray",
        "policy_patch": False,
        "instance_method": True,
        "method_name": "extend",
        "source": "OBJ,ARG_0",
        "target": "OBJ",
        "action": "APPEND",
    },
    {
        "module": "builtins",
        "class_name": "bytearray",
        "policy_patch": False,
        "instance_method": True,
        "method_name": "take_bytes",
        "source": "OBJ",
        "target": "RETURN",
        "action": "NONE",  # custom patch
    },
    CompositeNode(
        {
            "module": "operator",
            "target": "RETURN",
            "policy_patch": False,
        },
        [
            {
                "method_name": ["add", "iadd"],  # aka concat
                "source": "ARG_0,ARG_1",
                "action": "APPEND",
            },
            {
                "method_name": "mod",  # aka cformat
                "source": "ARG_0,ARG_1",
                "action": "FORMAT",
            },
        ],
    ),
    {
        "module": "builtins",
        "method_name": ["ascii", "format"],  # TODO: PYT-4064 - remove `format`
        # No keyword arguments
        "source": "ARG_0",
        "target": "RETURN",
        "action": "REPR",
    },
]

register_propagation_nodes(strlike_propagators)
