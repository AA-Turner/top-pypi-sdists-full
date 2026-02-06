"""Middleware to handle ensuring you can access the store with get_store() in your app."""

from langchain_core.runnables.config import RunnableConfig, var_child_runnable_config
from langgraph.constants import CONF
from starlette.types import ASGIApp, Receive, Scope, Send

from langgraph_api import feature_flags
from langgraph_api.store import get_store as api_get_store


class EnsureStoreAccessible:
    def __init__(self, app: ASGIApp):
        self.app = app

    async def __call__(self, scope: Scope, receive: Receive, send: Send):
        global _CONFIG
        if _CONFIG is None:
            _CONFIG = await _get_partial_conf()

        var_child_runnable_config.set(_CONFIG)
        await self.app(scope, receive, send)


async def _get_partial_conf() -> RunnableConfig:
    store_instance = await api_get_store()
    if feature_flags.USE_RUNTIME_CONTEXT_API:
        from langgraph._internal._constants import CONFIG_KEY_RUNTIME
        from langgraph.runtime import Runtime

        return {CONF: {CONFIG_KEY_RUNTIME: Runtime(store=store_instance)}}
    else:
        from langgraph.constants import CONFIG_KEY_STORE

        return {CONF: {CONFIG_KEY_STORE: store_instance}}


_CONFIG = None
