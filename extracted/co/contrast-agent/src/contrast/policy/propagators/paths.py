# Copyright © 2026 Contrast Security, Inc.
# See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
from contrast.agent.policy.registry import register_propagation_nodes

# NOTE: os.path is an alias for posixpath on posix systems and ntpath on windows systems.
path_propagators = [
    {
        "module": "posixpath",
        "method_name": "basename",
        "source": "ARG_0,KWARG:p",
        "target": "RETURN",
        # NOTE: this used to use TAGGER, but that implementation relied on propagation
        # occurring within the original `basename` call itself to handle other tags.
        # Using SPLAT instead means we no longer need to rely on propagation within a
        # propagator, which is better for performance.
        "action": "SPLAT",
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
        "module": "ntpath",
        "method_name": "basename",
        "source": "ARG_0,KWARG:p",
        "target": "RETURN",
        # NOTE: this used to use TAGGER, but that implementation relied on propagation
        # occurring within the original `basename` call itself to handle other tags.
        # Using SPLAT instead means we no longer need to rely on propagation within a
        # propagator, which is better for performance.
        "action": "SPLAT",
        "tags": ["SAFE_PATH"],
    },
    {
        "module": "nt",
        "method_name": ["_getfinalpathname", "_path_normpath", "readlink"],
        "source": "ARG_0,KWARG:path",
        "target": "RETURN",
        "action": "SPLAT",
    },
    {
        "module": "nt",
        "method_name": ["_getfullpathname"],
        "source": "ARG_0,KWARG:path",
        "target": "RETURN",
        "action": "APPEND",
    },
    {
        "module": "ntpath",
        "method_name": ["splitroot"],
        "source": "ARG_0,KWARG:path",
        "target": "RETURN",
        "action": "SPLIT",
    },
    {
        "module": "ntpath",
        "method_name": ["split", "splitdrive"],
        "source": "ARG_0,KWARG:p",
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
