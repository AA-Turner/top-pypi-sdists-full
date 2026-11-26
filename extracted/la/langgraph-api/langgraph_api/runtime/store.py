import threading
from typing import Any

from langgraph_grpc_common.store import GrpcStore

import langgraph_api.config as api_config
from langgraph_api.encryption.context import get_encryption_context
from langgraph_api.graph import resolve_embeddings

_STORE_CONFIG: api_config.StoreConfig = {}


def set_store_config(config: api_config.StoreConfig) -> None:
    global _STORE_CONFIG
    _STORE_CONFIG = config.copy()
    if "index" not in _STORE_CONFIG or not _STORE_CONFIG["index"]:
        return
    _STORE_CONFIG["index"]["embed"] = resolve_embeddings(_STORE_CONFIG["index"])


_STORE = threading.local()


def start_store() -> None:
    _STORE.store = GrpcStore(
        api_config.LSD_GRPC_SERVER_ADDRESS,
        index=_STORE_CONFIG.get("index"),
        ttl=_STORE_CONFIG.get("ttl"),
        encryption_context_provider=get_encryption_context
        if api_config.LANGGRAPH_ENCRYPTION
        else None,
        max_receive_message_bytes=api_config.GRPC_CLIENT_MAX_RECV_MSG_BYTES,
        max_send_message_bytes=api_config.GRPC_CLIENT_MAX_SEND_MSG_BYTES,
    )


def get_store_config() -> api_config.StoreConfig:
    return _STORE_CONFIG


def Store(*args: Any, **kwargs: Any) -> GrpcStore:
    if not hasattr(_STORE, "store"):
        if not _STORE_CONFIG and api_config.STORE_CONFIG:
            set_store_config(api_config.STORE_CONFIG)
        start_store()
    return _STORE.store
