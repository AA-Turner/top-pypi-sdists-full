# Copyright © 2026 Contrast Security, Inc.
# See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
from contrast.agent.policy.registry import register_propagation_nodes
from contrast.agent.policy.utils import CompositeNode


encodings_propagators = [
    {
        "module": [
            f"encodings.{name}"
            for name in [
                "ascii",
                "latin_1",
                "unicode_escape",
                "raw_unicode_escape",
                "unicode_internal",
                "utf8",
            ]
        ],
        "class_name": "Codec",
        # None of these methods have keyword arguments
        "method_name": ["encode", "decode"],
        "instance_method": False,
        "policy_patch": False,
        "source": "ARG_0",
        "target": "RETURN",
        "action": "CODECS_SPLAT",
    },
    CompositeNode(
        {
            "module": "binascii",
            "target": "RETURN",
            "action": "SPLAT",
        },
        [
            {
                "method_name": "a2b_base64",
                "untags": ["BASE64_ENCODED"],
                # no keyword arguments
                "source": "ARG_0",
            },
            {
                "method_name": "b2a_base64",
                "tags": ["BASE64_ENCODED"],
                # no keyword arguments
                "source": "ARG_0",
            },
            {
                "method_name": ["hexlify", "unhexlify", "b2a_hex", "a2b_hex"],
                # no keyword arguments
                "source": "ARG_0",
            },
        ],
    ),
    CompositeNode(
        {
            "module": "base64",
            "target": "RETURN",
            "action": "SPLAT",
        },
        [
            {
                # In Py3.10 this has been renamed to _b32decode
                "method_name": "b32decode",
                "source": "ARG_0,KWARG:s",
                "untags": ["BASE64_ENCODED"],
            },
            {
                # In Py3.10 this has been renamed to _b32encode
                "method_name": "b32encode",
                "source": "ARG_0,KWARG:s",
                "tags": ["BASE64_ENCODED"],
            },
            {
                "method_name": "_b32decode",
                "source": "ARG_1,KWARG:s",
                "untags": ["BASE64_ENCODED"],
            },
            {
                "method_name": "_b32encode",
                "source": "ARG_1,KWARG:s",
                "tags": ["BASE64_ENCODED"],
            },
            {
                "method_name": "a85decode",
                "source": "ARG_0,KWARG:b",
                "untags": ["BASE64_ENCODED"],
            },
            {
                "method_name": "a85encode",
                "source": "ARG_0,KWARG:b",
                "tags": ["BASE64_ENCODED"],
            },
            {
                "method_name": "b85decode",
                "source": "ARG_0,KWARG:b",
                "untags": ["BASE64_ENCODED"],
            },
            {
                "method_name": "b85encode",
                "source": "ARG_0,KWARG:b",
                "tags": ["BASE64_ENCODED"],
            },
        ],
    ),
]

register_propagation_nodes(encodings_propagators)
