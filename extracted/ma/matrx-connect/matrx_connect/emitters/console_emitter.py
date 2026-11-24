from __future__ import annotations

import asyncio
import datetime
import json
import os
from pathlib import Path
from typing import Any

from matrx_utils import vcprint
from matrx_utils.fancy_prints.truncation import content_logging_enabled

from matrx_connect.context.data_types import DataPayload
from matrx_connect.context.events import GENERIC_ERROR_MESSAGE
from matrx_connect.context.graph_ops import GraphOpEvent
from matrx_connect.context.events import (
    END_REASON_CANCELLED,
    END_REASON_ERROR,
    CitationPayload,
    ContextAnalysisPayload,
    ContextStatePayload,
    ContextTrimmedPayload,
    InfoPayload,
    InjectionConsumedPayload,
    ProviderRetryPayload,
    ReasoningState,
    RecordReservedPayload,
    RecordUpdatePayload,
    ResourceAction,
    ResourceChangedPayload,
    StructuredOutputPayload,
    ToolEventPayload,
    WarningPayload,
)
from matrx_connect.context.operations import CompletionPayload, InitPayload
from matrx_connect.context.phases import Phase
from matrx_connect.emitters.error_guard import ErrorEmissionGuard
from matrx_connect.emitters._turn_thinking import turn_thinking_clock


#: The identifying keys a one-line summary names (never content: no inputs, outputs, arguments or results).
_SUMMARY_KEYS = (
    "event", "run_id", "step", "node_id", "item_index", "tool_name", "call_id",
    "operation", "operation_id", "status", "error_type", "code",
)
#: Longest value a summary prints, and longest summary line (review 6h, M2).
SUMMARY_VALUE_MAX = 80
SUMMARY_LINE_MAX = 300


def _cap(text: str, limit: int) -> str:
    return text if len(text) <= limit else text[: limit - 1] + "…"


def _summary(kind: str, dump: Any, *, message_max: int = 0) -> str:
    """One line naming a payload (its event, run, step, node, tool, status… when it has them), no content.

    ``message_max`` > 0 also prints a capped ``message`` (an error's own diagnostic text)."""
    if not isinstance(dump, dict):
        return f"{kind}: {type(dump).__name__}"
    named = [
        f"{key}={_cap(str(dump[key]), SUMMARY_VALUE_MAX)}"
        for key in _SUMMARY_KEYS
        if dump.get(key) not in (None, "")
    ]
    if message_max and dump.get("message"):
        named.append(f"message={_cap(str(dump['message']), message_max)!r}")
    if not named:
        # Keys of mixed types (an int and a str) cannot be sorted against each other.
        named = [f"keys={sorted(str(key) for key in dump)[:8]}"]
    return _cap(f"{kind}: " + " ".join(named), SUMMARY_LINE_MAX)


def _data_summary(dump: Any) -> str:
    """One line naming a data payload (its event, run, step and node when it has them), no content."""
    return _summary("data", dump)


DEFAULT_SAVE_DIR = Path(os.environ.get("MATRX_TEMP_DIR", "temp")) / "emitter_responses"


class ConsoleEmitter:
    #: Nothing this emitter receives reaches a person's response stream, so a model call
    #: under it never stamps the request latency clock (``request_latency.reaches_wire``).
    reaches_wire = False

    def __init__(
        self,
        label: str = "console",
        debug: bool = False,
        accumulate: bool = True,
        save_dir: Path | None = None,
    ):
        self.label = label
        self.debug = debug
        self.accumulate = accumulate
        self.cancelled = False
        self._save_dir = save_dir or DEFAULT_SAVE_DIR
        self._turn_text_acc: list[str] = []
        self._error_guard = ErrorEmissionGuard("ConsoleEmitter")

        if self.accumulate:
            self._accumulated: dict[str, list[Any]] = {
                "chunks": [],
                "phases": [],
                "data": [],
                "completions": [],
                "errors": [],
                "tool_events": [],
            }
            self._full_text = ""

    def _log(self, kind: str, dump: Any, color: str, *, message_max: int = 0) -> None:
        """The whole payload under ``debug`` or local content logging; otherwise ONE line naming it (CASA 6.5.1:
        a server log never carries a person's content — tool arguments and results, step data, completions)."""
        if self.debug or content_logging_enabled():
            vcprint(data=dump, verbose=True, title=f"[{self.label}] {kind}", color=color)
        else:
            vcprint(f"[{self.label}] {_summary(kind, dump, message_max=message_max)}", verbose=True, color=color)

    def reset_turn_text(self) -> None:
        self._turn_text_acc = []
        self._turn_reasoning_chars = 0
        turn_thinking_clock(self).reset()

    def get_turn_text(self) -> str:
        return "".join(self._turn_text_acc)

    def get_turn_thinking_ms(self) -> int:
        """This provider call's thinking time (reasoning-start frame -> stop, or now): bills hidden thinking."""
        return turn_thinking_clock(self).elapsed_ms()

    def get_turn_reasoning_chars(self) -> int:
        return getattr(self, "_turn_reasoning_chars", 0)

    async def send_chunk(self, text: str) -> None:
        # CASA 6.5.1: a chunk is model output about a person's content; it reaches the log
        # only on a local machine (MATRX_LOG_CONTENT=1). Server-side runs use this emitter.
        if content_logging_enabled():
            vcprint(data=text, verbose=True, color="green", chunks=True)
        self._turn_text_acc.append(text)
        if self.accumulate:
            self._full_text += text
            self._accumulated["chunks"].append(text)

    async def send_reasoning_chunk(self, text: str) -> None:
        if isinstance(text, str):
            self._turn_reasoning_chars = self.get_turn_reasoning_chars() + len(text)
        if content_logging_enabled():
            vcprint(data=text, verbose=True, color="magenta", chunks=True)
        if self.accumulate:
            self._accumulated["chunks"].append({"reasoning": text})

    async def send_reasoning_state(self, state: ReasoningState) -> None:
        turn_thinking_clock(self).signal(state)
        vcprint(data={"state": state}, verbose=True, title=f"[{self.label}] reasoning", color="magenta")
        if self.accumulate:
            self._accumulated.setdefault("reasoning_states", []).append(state)

    async def send_phase(self, phase: Phase) -> None:
        vcprint(data={"phase": phase}, verbose=True, title=f"[{self.label}] phase", color="cyan")
        if self.accumulate:
            self._accumulated["phases"].append(phase)

    async def send_warning(self, payload: WarningPayload) -> None:
        dump = payload.model_dump()
        color = "red" if payload.level == "high" else "yellow"
        vcprint(data=dump, verbose=True, title=f"[{self.label}] warning", color=color)
        if self.accumulate:
            self._accumulated.setdefault("warnings", []).append(dump)

    async def send_info(self, payload: InfoPayload) -> None:
        dump = payload.model_dump()
        self._log("info", dump, "blue")
        if self.accumulate:
            self._accumulated.setdefault("infos", []).append(dump)

    async def send_data(self, payload: DataPayload | dict[str, Any] | Any) -> None:
        if isinstance(payload, DataPayload):
            dump = payload.model_dump()
        elif isinstance(payload, dict):
            dump = payload
        else:
            dump = {"value": payload}
        # CASA 6.5.1, like a chunk: a data payload carries a person's content (step inputs and outputs), so a
        # server log gets one line naming it. The whole dump also cost every workflow event a pretty-print on
        # the event loop (L-SPEED 6c: ~28k log lines per search child run).
        self._log("data", dump, "green")
        if self.accumulate:
            self._accumulated["data"].append(dump)

    async def send_init(self, payload: InitPayload) -> None:
        dump = payload.model_dump()
        vcprint(data=dump, verbose=True, title=f"[{self.label}] init", color="blue")
        if self.accumulate:
            self._accumulated.setdefault("inits", []).append(dump)

    async def send_completion(self, payload: CompletionPayload) -> None:
        dump = payload.model_dump()
        self._log("completion", dump, "green")
        if self.accumulate:
            self._accumulated["completions"].append(dump)

    async def send_error(
        self,
        error_type: str,
        message: str,
        user_message: str | None = None,
        code: str | None = None,
        details: dict[str, Any] | None = None,
    ) -> None:
        if not self._error_guard.claim(error_type):
            return
        error = {
            "error_type": error_type,
            "message": message,
            # Only a sentence written for a person; none → the generic line (never `message`).
            "user_message": (user_message or "").strip() or GENERIC_ERROR_MESSAGE,
            "code": code,
            "details": details,
        }
        # A caller refusal (``details.caller_refusal``, set from the refusal's type by the
        # producer) is an expected answer — a spend hold, a run approval — not a server failure.
        refused = isinstance(details, dict) and bool(details.get("caller_refusal"))
        self._log("caller_refused" if refused else "error", error, "yellow" if refused else "red", message_max=160)
        if self.accumulate:
            self._accumulated["errors"].append(error)

    async def send_tool_event(self, event_data: ToolEventPayload | dict[str, Any]) -> None:
        if isinstance(event_data, dict):
            dump = event_data
        else:
            dump = event_data.model_dump()
        self._log("tool_event", dump, "cyan")
        if self.accumulate:
            self._accumulated["tool_events"].append(dump)

    async def send_record_reserved(self, payload: RecordReservedPayload) -> None:
        dump = payload.model_dump()
        vcprint(data=dump, verbose=True, title=f"[{self.label}] record_reserved", color="blue")

    async def send_record_update(self, payload: RecordUpdatePayload) -> None:
        dump = payload.model_dump()
        # A record's status change is a notification, not the failure: a failed run's error is
        # reported once, at ERROR, by ``send_error`` / ``fatal_error``. Logging the record's
        # ``failed`` status red as well filed every failure twice — and every expected caller
        # refusal as a server error (2026-11-12).
        color = "green" if payload.status in ("active", "completed") else "yellow"
        vcprint(data=dump, verbose=True, title=f"[{self.label}] record_update", color=color)

    async def send_resource_changed(
        self,
        *,
        kind: str,
        action: ResourceAction,
        resource_id: str,
        sandbox_id: str | None = None,
        user_id: str | None = None,
        metadata: dict[str, Any] | None = None,
    ) -> None:
        # Validate via the same Pydantic model so console + stream behave
        # identically; emitter dev-mode shouldn't accept payloads the
        # production stream would reject.
        payload = ResourceChangedPayload(
            kind=kind,
            action=action,
            resource_id=resource_id,
            sandbox_id=sandbox_id,
            user_id=user_id,
            metadata=metadata or {},
        )
        vcprint(
            data=payload.model_dump(),
            verbose=True,
            title=f"[{self.label}] resource_changed",
            color="cyan",
        )

    async def send_graph_op(self, payload: GraphOpEvent) -> None:
        vcprint(
            data=payload.model_dump(exclude_none=True),
            verbose=True,
            title=f"[{self.label}] graph_op {payload.phase}",
            color="cyan",
        )

    async def send_structured_output(self, payload: StructuredOutputPayload) -> None:
        dump = payload.model_dump()
        vcprint(
            data={
                "schema_name": dump["schema_name"],
                "success": dump["success"],
                "match_count": dump["match_count"],
                "agent_name": dump["agent_name"],
                "operation_id": dump["operation_id"],
            },
            verbose=True,
            title=f"[{self.label}] structured_output",
            color="green" if payload.success else "yellow",
        )
        if self.accumulate:
            self._accumulated.setdefault("structured_output", []).append(dump)

    async def send_injection_consumed(self, payload: InjectionConsumedPayload) -> None:
        dump = payload.model_dump()
        vcprint(
            data={"conversation_id": dump["conversation_id"], "count": dump["count"]},
            verbose=True,
            title=f"[{self.label}] injection_consumed",
            color="cyan",
        )
        if self.accumulate:
            self._accumulated.setdefault("injection_consumed", []).append(dump)

    async def send_provider_retry(self, payload: ProviderRetryPayload) -> None:
        dump = payload.model_dump()
        vcprint(
            data=dump,
            verbose=True,
            title=f"[{self.label}] provider_retry",
            color="yellow" if payload.state != "recovered" else "green",
        )
        if self.accumulate:
            self._accumulated.setdefault("provider_retry", []).append(dump)

    async def send_citation(self, payload: CitationPayload) -> None:
        dump = payload.model_dump()
        vcprint(
            data={
                "block_index": dump["block_index"],
                "kind": (dump.get("citation") or {}).get("kind"),
                "title": (dump.get("citation") or {}).get("title"),
            },
            verbose=True,
            title=f"[{self.label}] citation",
            color="cyan",
        )
        if self.accumulate:
            self._accumulated.setdefault("citation", []).append(dump)

    async def send_context_analysis(self, payload: ContextAnalysisPayload) -> None:
        dump = payload.model_dump()
        vcprint(
            data={
                "provider": dump["provider"],
                "model": dump["model"],
                "iteration": dump["iteration"],
                "url": dump["url"],
                "body_size_bytes": dump["body_size_bytes"],
                "is_streaming": dump["is_streaming"],
            },
            verbose=True,
            title=f"[{self.label}] context_analysis",
            color="magenta",
        )
        if self.accumulate:
            self._accumulated.setdefault("context_analysis", []).append(dump)

    async def send_context_state(self, payload: ContextStatePayload) -> None:
        dump = payload.model_dump()
        vcprint(
            data={
                "conversation_id": dump["conversation_id"],
                "total_chars": dump["total_chars_visible_to_model"],
                "msgs": dump["message_count_visible"],
                "input_tokens": dump["last_request_input_tokens"],
                "cached_tokens": dump["last_request_cached_tokens"],
            },
            verbose=True,
            title=f"[{self.label}] context_state",
            color="cyan",
        )
        if self.accumulate:
            self._accumulated.setdefault("context_state", []).append(dump)

    async def send_context_trimmed(self, payload: ContextTrimmedPayload) -> None:
        dump = payload.model_dump()
        ts = dump.get("trim_summary") or {}
        vcprint(
            data={
                "conversation_id": dump["conversation_id"],
                "blocks_rewritten": ts.get("blocks_rewritten"),
                "freed_chars": ts.get("freed_chars"),
                "skipped_reason": ts.get("eligible_but_skipped_reason"),
            },
            verbose=True,
            title=f"[{self.label}] context_trimmed",
            color="yellow",
        )
        if self.accumulate:
            self._accumulated.setdefault("context_trimmed", []).append(dump)

    async def send_end(self, reason: str = "complete") -> None:
        vcprint(
            data=f"End of transmission (reason={reason})",
            verbose=True,
            title=f"[{self.label}] end",
            color="green",
        )
        if self.accumulate:
            await self._save_accumulated()

    async def send_cancelled(self) -> None:
        await self.send_error(
            error_type="task_cancelled",
            message="Task was canceled.",
            user_message="Your request was canceled.",
        )
        await self.send_end(reason=END_REASON_CANCELLED)

    async def fatal_error(
        self,
        error_type: str,
        message: str,
        user_message: str | None = None,
        code: str | None = None,
        details: dict[str, Any] | None = None,
    ) -> None:
        from matrx_connect.reservations import try_get_tracker
        tracker = try_get_tracker()
        if tracker:
            try:
                await tracker.fail_all_pending(self)
            except Exception as tracker_exc:
                vcprint(
                    f"[ConsoleEmitter] fail_all_pending raised during fatal_error: {tracker_exc}",
                    color="yellow",
                )
        await self.send_error(error_type, message, user_message, code, details)
        # Same rule as StreamEmitter: a fatal error never ends "complete".
        await self.send_end(reason=END_REASON_ERROR)

    async def _save_accumulated(self) -> None:
        if not self.accumulate:
            return

        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S_%f")[:-3]
        filename = f"{self.label}_{timestamp}.json"
        filepath = self._save_dir / filename

        os.makedirs(self._save_dir, exist_ok=True)

        output = {
            "metadata": {
                "label": self.label,
                "timestamp": datetime.datetime.now().isoformat(),
                "text_length": len(self._full_text),
                "counts": {k: len(v) for k, v in self._accumulated.items()},
            },
            "text": self._full_text,
            "events": self._accumulated,
        }

        try:
            def _write() -> None:
                with open(filepath, "w", encoding="utf-8") as f:
                    json.dump(output, f, indent=2, ensure_ascii=False, default=str)

            await asyncio.to_thread(_write)
            vcprint(f"[ConsoleEmitter] Saved to {filepath}", color="pink")
        except Exception as e:
            vcprint(f"[ConsoleEmitter] Failed to save: {e}", color="red")
