# Copyright © 2026 Contrast Security, Inc.
# See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
from contrast.agent.policy.registry import register_source_nodes


cgi_sources = [
    {
        # We actually track attributes of the resulting FieldStorage object, so the
        # target and type here aren't really accurate. See the explicit patch
        "module": "cgi",
        "class_name": ["FieldStorage", "MiniFieldStorage"],
        "method_name": "__init__",
        "policy_patch": False,
        "target": "OBJ",
        "node_type": "MULTIPART_FORM_DATA",
        "tags": ["CROSS_SITE"],
    },
]


register_source_nodes(cgi_sources)
