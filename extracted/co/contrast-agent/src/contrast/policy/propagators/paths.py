# Copyright © 2026 Contrast Security, Inc.
# See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
from contrast.agent.policy.registry import register_propagation_nodes


path_propagators = [
    {
        # os.path is just an alias for posixpath
        "module": "posixpath",
        "method_name": "basename",
        "source": "ARG_0,KWARG:p",
        "target": "RETURN",
        # We rely on rewrites to perform the actual propagation
        "action": "TAGGER",
        "tags": ["SAFE_PATH"],
    },
    {
        "module": "posix",
        "method_name": ["_path_normpath", "readlink"],
        "source": "ARG_0,KWARG:path",
        "target": "RETURN",
        "action": "SPLAT",
    },
    {
        "module": "posixpath",
        "method_name": ["splitroot"],
        "source": "ARG_0,KWARG:path",
        "target": "RETURN",
        "action": "SPLIT",
    },
    {
        "module": "urllib.parse",
        "method_name": ["quote", "quote_plus"],
        "source": "ARG_0,KWARG:string",
        "target": "RETURN",
        "action": "SPLAT",
        "tags": ["URL_ENCODED"],
    },
    {
        "module": "urllib.parse",
        "method_name": ["unquote", "unquote_plus"],
        "source": "ARG_0,KWARG:string",
        "target": "RETURN",
        "action": "SPLAT",
        "untags": ["URL_ENCODED"],
    },
    {
        "module": "urllib3.util.url",
        "method_name": ["_encode_invalid_chars"],
        "source": "ARG_0,KWARG:component",
        "target": "RETURN",
        "action": "SPLAT",
    },
]


register_propagation_nodes(path_propagators)
