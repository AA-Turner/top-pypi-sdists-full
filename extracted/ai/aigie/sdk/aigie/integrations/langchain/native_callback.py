"""LangChain callback binding with tool-catalog stamping."""

from __future__ import annotations

from typing import Any

from aigie.decision.tool_catalog import bind_trace_hash, register_catalog
from aigie.integrations.langchain._runtime import get_runtime
from aigie.integrations.langchain.event_classifier import LangChainEventClassifier
from aigie.tracing.lc_callback_base import LangChainCallbackBase

_DEFAULT_WORKFLOW_NAME = "LangChain Workflow"

# Stateless, shared across every per-run handler instance.
_CLASSIFIER = LangChainEventClassifier()


def _tool_name_desc(tool: Any) -> dict[str, str] | None:
    """Return name/description from flat or OpenAI-style tool specs."""
    if not isinstance(tool, dict):
        return None
    fn = tool.get("function")
    src = fn if isinstance(fn, dict) else tool
    name = src.get("name")
    if not name:
        return None
    return {"name": str(name), "description": str(src.get("description") or "")}


def _tools_from_invocation_params(params: Any) -> list[dict[str, str]]:
    """Extract tool specs from ``invocation_params``."""
    if not isinstance(params, dict):
        return []
    out: list[dict[str, str]] = []
    for key in ("tools", "functions"):
        val = params.get(key)
        if isinstance(val, list):
            out.extend(nd for nd in (_tool_name_desc(t) for t in val) if nd)
    return out


class LangChainNativeCallback(LangChainCallbackBase):
    """Callback-driven LangChainCallbackBase bound to LangChain."""

    framework_name = "langchain"
    callback_driven = True

    def __init__(self) -> None:
        rt = get_runtime()
        super().__init__(
            emitter=rt.emitter,
            workflow_name=_DEFAULT_WORKFLOW_NAME,
            classifier=_CLASSIFIER,
            config=rt.config,
        )
        # Read by the base boundary when the root span closes.
        self._aigie_tool_registry_hash: str | None = None

    def on_chat_model_start(self, *args: Any, **kwargs: Any) -> None:
        super().on_chat_model_start(*args, **kwargs)
        if self._aigie_tool_registry_hash is None:
            self._stamp_tool_catalog(_tools_from_invocation_params(kwargs.get("invocation_params")))

    def on_tool_start(self, serialized: dict[str, Any] | None, *args: Any, **kwargs: Any) -> None:
        super().on_tool_start(serialized, *args, **kwargs)
        if self._aigie_tool_registry_hash is None:
            nd = _tool_name_desc(serialized)
            self._stamp_tool_catalog([nd] if nd else [])

    def _stamp_tool_catalog(self, tools: list[dict[str, str]]) -> None:
        """Register tools and bind the hash to this trace."""
        if not tools:
            return
        try:
            digest = register_catalog(tools)
            if digest:
                self._aigie_tool_registry_hash = digest
                bind_trace_hash(self._trace_id, digest)
        except Exception:  # noqa: BLE001 — tracing must stay fail-open
            return
