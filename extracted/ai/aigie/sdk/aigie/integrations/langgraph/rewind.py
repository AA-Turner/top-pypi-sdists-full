"""LangGraph checkpoint rewind support."""

from __future__ import annotations

import logging
from dataclasses import dataclass
from typing import Any

from aigie.rewind.protocol import Corrective, RewindHandle, RewindOutcome, ToolCallOverride

logger = logging.getLogger(__name__)


def _append_message(values: dict[str, Any], message: Any) -> None:
    values["messages"] = [*(values.get("messages") or []), message]


def _last_tool_call_message(state: dict[str, Any] | None) -> Any | None:
    for message in reversed((state or {}).get("messages") or []):
        if getattr(message, "tool_calls", None):
            return message
    return None


def _select_call(calls: list[dict[str, Any]], override: ToolCallOverride) -> tuple[int, str | None]:
    """Locate the failed call among an assistant turn's parallel calls.

    Never falls back to a positional guess when several calls are present:
    redirecting the wrong one breaks a working call and leaves the failed one
    untouched, which is worse than declining.
    """
    if override.source_call_id:
        matches = [i for i, call in enumerate(calls) if call.get("id") == override.source_call_id]
        # An id we cannot find means our identification is wrong, not that some
        # other call is fair game.
        return (matches[0], None) if matches else (-1, "no_tool_call")
    if override.source_tool:
        matches = [i for i, call in enumerate(calls) if call.get("name") == override.source_tool]
        if len(matches) == 1:
            return matches[0], None
        if matches:
            return -1, "ambiguous_tool_call"
    if len(calls) == 1:
        return 0, None
    return -1, "ambiguous_tool_call"


@dataclass(frozen=True)
class LangGraphCheckpoint:
    """LangGraph app plus checkpoint pointer."""

    app: Any
    thread_id: str
    checkpoint_id: str
    checkpoint_ns: str = ""


class LangGraphRewindCapability:
    """Capture and replay LangGraph checkpoints."""

    framework = "langgraph"

    def build_handle(
        self, span_id: str, trace_id: str, app: Any, config: dict | None
    ) -> RewindHandle | None:
        """Capture the checkpoint visible at this node's start."""
        try:
            snapshot = app.get_state(config)
        except Exception:  # noqa: BLE001 — capture must never break a run
            logger.debug("rewind capture: get_state failed", exc_info=True)
            return None
        cfg = getattr(snapshot, "config", None)
        conf = cfg.get("configurable", {}) if isinstance(cfg, dict) else {}
        thread_id = conf.get("thread_id")
        checkpoint_id = conf.get("checkpoint_id")
        if not thread_id or not checkpoint_id:
            return None
        payload = LangGraphCheckpoint(
            app=app,
            thread_id=str(thread_id),
            checkpoint_id=str(checkpoint_id),
            checkpoint_ns=str(conf.get("checkpoint_ns", "")),
        )
        return RewindHandle(
            framework=self.framework, trace_id=trace_id, span_id=span_id, payload=payload
        )

    def on_evict(self, handle: RewindHandle) -> None:
        """Delete checkpoints only for Aigie-injected savers."""
        payload = handle.payload
        if not isinstance(payload, LangGraphCheckpoint):
            return
        saver = getattr(payload.app, "_aigie_injected_checkpointer", None)
        if saver is None or not payload.thread_id:
            return
        delete = getattr(saver, "delete_thread", None)
        if delete is None:
            return
        try:
            delete(payload.thread_id)
        except Exception:  # noqa: BLE001 — cleanup must never break a run
            logger.debug("rewind cleanup: delete_thread failed", exc_info=True)

    def supports(self, handle: RewindHandle) -> bool:
        payload = handle.payload
        if not isinstance(payload, LangGraphCheckpoint):
            return False
        if getattr(payload.app, "checkpointer", None) is None:
            return False
        return bool(payload.thread_id and payload.checkpoint_id)

    async def capture(self, span_id: str, trace_id: str, context: Any) -> RewindHandle | None:
        app = context.get("app") if isinstance(context, dict) else None
        if app is None:
            return None
        config = context.get("config")
        return self.build_handle(span_id, trace_id, app, config)

    async def rewind(self, handle: RewindHandle, corrective: Corrective | None) -> RewindOutcome:
        payload = handle.payload
        cfg = self._base_config(payload)
        if corrective is not None and not corrective.is_empty:
            values, declined = self._corrective_values(payload.app, cfg, corrective)
            if declined is not None:
                return RewindOutcome.skipped(declined, handle=handle)
            if values:
                cfg = await self._update_state(payload.app, cfg, values)
        await self._invoke(payload.app, cfg)
        return RewindOutcome.ok(handle)

    def _base_config(self, payload: LangGraphCheckpoint) -> dict[str, Any]:
        # LangGraph update_state indexes checkpoint_ns directly.
        return {
            "configurable": {
                "thread_id": payload.thread_id,
                "checkpoint_id": payload.checkpoint_id,
                "checkpoint_ns": payload.checkpoint_ns,
            }
        }

    def _corrective_values(
        self, app: Any, cfg: dict[str, Any], corrective: Corrective
    ) -> tuple[dict[str, Any], str | None]:
        values: dict[str, Any] = dict(corrective.state_patch or {})
        state = (
            self._state_values(app, cfg)
            if corrective.prompt or corrective.tool_call is not None
            else None
        )
        if corrective.prompt:
            self._merge_prompt(state, values, corrective.prompt)
        if corrective.tool_call is not None:
            message, declined = self._rewrite_tool_call(state, corrective.tool_call)
            if declined is not None:
                return values, declined
            _append_message(values, message)
        return values, None

    def _state_values(self, app: Any, cfg: dict[str, Any]) -> dict[str, Any] | None:
        try:
            state = app.get_state(cfg)
        except Exception:  # noqa: BLE001 — a missing checkpoint is a skip, not a crash
            logger.debug("rewind corrective: get_state failed", exc_info=True)
            return None
        values = getattr(state, "values", None)
        return values if isinstance(values, dict) else None

    def _rewrite_tool_call(
        self, state: dict[str, Any] | None, override: ToolCallOverride
    ) -> tuple[Any, str | None]:
        message = _last_tool_call_message(state)
        if message is None:
            return None, "no_tool_call"
        calls = list(message.tool_calls)
        index, declined = _select_call(calls, override)
        if declined is not None:
            return None, declined
        target = dict(calls[index])
        missing = override.missing_required(target.get("args"))
        if missing:
            return None, "unmappable_args"
        target["name"] = override.name
        target["args"] = override.resolve_args(target.get("args"))
        calls[index] = target
        return self._copy_with_tool_calls(message, calls), None

    def _copy_with_tool_calls(self, message: Any, calls: list[dict[str, Any]]) -> Any:
        copy = getattr(message, "model_copy", None) or message.copy  # pydantic v2 / v1
        return copy(update={"tool_calls": calls})

    def _merge_prompt(
        self, state: dict[str, Any] | None, values: dict[str, Any], prompt: str
    ) -> None:
        if "messages" not in values and not (state is not None and "messages" in state):
            logger.debug("rewind prompt corrective skipped: no 'messages' state key")
            return
        try:
            from langchain_core.messages import HumanMessage
        except ImportError:
            logger.debug("rewind prompt corrective skipped: langchain_core missing")
            return
        _append_message(values, HumanMessage(content=prompt))

    async def _update_state(
        self, app: Any, cfg: dict[str, Any], values: dict[str, Any]
    ) -> dict[str, Any]:
        aupdate = getattr(app, "aupdate_state", None)
        if aupdate is not None:
            return await aupdate(cfg, values)  # type: ignore[no-any-return]
        return app.update_state(cfg, values)  # type: ignore[no-any-return]

    async def _invoke(self, app: Any, cfg: dict[str, Any]) -> Any:
        ainvoke = getattr(app, "ainvoke", None)
        if ainvoke is not None:
            return await ainvoke(None, cfg)
        return app.invoke(None, cfg)
