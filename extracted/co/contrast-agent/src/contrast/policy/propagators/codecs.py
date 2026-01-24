# Copyright © 2026 Contrast Security, Inc.
# See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
from contrast.agent.policy.registry import register_propagation_nodes
from contrast.agent.policy.utils import CompositeNode


codecs_propagators = [
    CompositeNode(
        {
            "module": ["_codecs", "codecs"],
            "instance_method": True,
            "target": "RETURN",
        },
        [
            {
                "method_name": ["encode", "decode"],
                "source": "ARG_0,KWARG:obj",
                "action": "SPLAT",
            },
            {
                # No keyword arguments
                "method_name": [
                    "ascii_encode",
                    "charmap_encode",
                    "escape_encode",
                    "latin_1_encode",
                    "raw_unicode_escape_encode",
                    "readbuffer_encode",
                    "unicode_escape_encode",
                    "unicode_escape_decode",
                    "unicode_internal_encode",
                    "utf_16_encode",
                    "utf_16_be_encode",
                    "utf_16_le_encode",
                    "utf_32_encode",
                    "utf_32_be_encode",
                    "utf_32_le_encode",
                    "utf_7_encode",
                    "utf_8_encode",
                    "ascii_decode",
                    "charmap_decode",
                    "escape_decode",
                    "latin_1_decode",
                    "raw_unicode_escape_decode",
                    "unicode_internal_decode",
                    "utf_16_decode",
                    "utf_16_be_decode",
                    "utf_16_le_decode",
                    "utf_32_decode",
                    "utf_32_be_decode",
                    "utf_32_le_decode",
                    "utf_7_decode",
                    "utf_8_decode",
                ],
                "source": "ARG_0",
                "action": "CODECS_SPLAT",
            },
        ],
    ),
]


register_propagation_nodes(codecs_propagators)
