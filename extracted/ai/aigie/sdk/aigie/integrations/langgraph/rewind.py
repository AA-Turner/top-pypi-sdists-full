"""LangGraph checkpoint rewind support."""

from __future__ import annotations

import logging
from dataclasses import dataclass
from typing import Any

from aigie.rewind.protocol import Corrective, RewindHandle, RewindOutcome

logger = logging.getLogger(__name__)


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
            cfg = await self._apply_corrective(payload.app, cfg, corrective)
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

    async def _apply_corrective(
        self, app: Any, cfg: dict[str, Any], corrective: Corrective
    ) -> dict[str, Any]:
        values: dict[str, Any] = dict(corrective.state_patch or {})
        if corrective.prompt:
            self._merge_prompt(app, cfg, values, corrective.prompt)
        if not values:
            return cfg
        return await self._update_state(app, cfg, values)

    def _merge_prompt(
        self, app: Any, cfg: dict[str, Any], values: dict[str, Any], prompt: str
    ) -> None:
        if "messages" not in values and not self._state_has_messages(app, cfg):
            logger.debug("rewind prompt corrective skipped: no 'messages' state key")
            return
        try:
            from langchain_core.messages import HumanMessage
        except ImportError:
            logger.debug("rewind prompt corrective skipped: langchain_core missing")
            return
        existing = values.get("messages") or []
        values["messages"] = [*existing, HumanMessage(content=prompt)]

    def _state_has_messages(self, app: Any, cfg: dict[str, Any]) -> bool:
        try:
            state = app.get_state(cfg)
        except Exception:  # noqa: BLE001
            return False
        current = getattr(state, "values", None)
        return isinstance(current, dict) and "messages" in current

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
