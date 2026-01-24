import json

from typing import Dict, Final, Optional

from cffi import FFI

from .lib.node import *
from .lib.clib import clib


ffi = FFI()

LANGUAGE: Final[str] = "python"

def create(
        variable_values: Dict,
        fallback_init_data: Optional[Dict],
        token: Optional[str],
        init_query: Dict,
        query: Dict,
        branch_name: Optional[str] = None,
        init_data_refresh_interval_ms: Optional[int] = None,
        logs_flush_interval_ms: Optional[int] = None,
        edge_base_url: Optional[str] = None,
        remote_logging_base_url: Optional[str] = None,
    ) -> NodeProps:
    return NodeProps(clib.create(
        ffi.new("char[]", json.dumps(variable_values).encode()),
        ffi.new("char[]", json.dumps(fallback_init_data).encode()) if fallback_init_data else ffi.NULL,
        ffi.new("char[]", token.encode()) if token else ffi.NULL,
        ffi.new("char[]", json.dumps(init_query).encode()),
        ffi.new("char[]", json.dumps(query).encode()),
        ffi.new("char[]", json.dumps({
            "branch_name": branch_name,
            "init_data_refresh_interval_ms": init_data_refresh_interval_ms,
            "logs_flush_interval_ms": logs_flush_interval_ms,
            "edge_base_url": edge_base_url,
            "remote_logging_base_url": remote_logging_base_url,
            "language": LANGUAGE,
        }).encode()),
    ))
