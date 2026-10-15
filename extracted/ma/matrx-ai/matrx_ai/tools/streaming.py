from __future__ import annotations

import json
import time
from typing import TYPE_CHECKING, Any, Literal

from matrx_connect.context.tool_event_data import (
    ToolCompletedData,
    ToolErrorData,
    ToolProgressData,
    ToolResultPreviewData,
    ToolStartedData,
    ToolStepData,
)
from pydantic import BaseModel, Field

from matrx_ai.context.emitter_protocol import Emitter

if TYPE_CHECKING:
    from matrx_ai.tools.models import ToolResult


class ToolStreamEvent(BaseModel):
    event: Literal[
        "tool_started",
        "tool_progress",
        "tool_step",
        "tool_result_preview",
        "tool_completed",
        "tool_error",
    ]
    call_id: str
    tool_name: str
    timestamp: float = Field(default_factory=time.time)
    message: str | None = None
    show_spinner: bool = True
    data: dict[str, Any] = Field(default_factory=dict)


class ToolStreamManager:
    def __init__(
        self,
        emitter: Emitter | None,
        call_id: str,
        tool_name: str,
        row_id: str | None = None,
    ):
        self.emitter = emitter
        # chat.tool_call.id of this call, when known (lets the client fetch detail by id).
        self.row_id = row_id
        self.call_id = call_id
        self.tool_name = tool_name
        self._events: list[ToolStreamEvent] = []

    async def emit(self, event: ToolStreamEvent, wire_event: ToolStreamEvent | None = None) -> None:
        # `_events` is what gets persisted (execution_events) and stays complete;
        # `wire_event`, when given, is the slimmer copy that goes over the stream.
        self._events.append(event)
        if self.emitter is not None:
            try:
                await self.emitter.send_tool_event((wire_event or event).model_dump())
            except Exception:
                pass

    # ------------------------------------------------------------------
    # EXECUTOR-ONLY: started / completed / error
    # ------------------------------------------------------------------

    async def started(
        self,
        message: str = "Starting...",
        arguments: dict[str, Any] | None = None,
        display_name: str | None = None,
    ) -> None:
        typed_data = ToolStartedData(arguments=arguments or {}, display_name=display_name)
        await self.emit(
            ToolStreamEvent(
                event="tool_started",
                call_id=self.call_id,
                tool_name=self.tool_name,
                message=message,
                data=typed_data.model_dump(),
            )
        )

    async def completed(
        self,
        message: str = "Done",
        result: ToolResult | None = None,
    ) -> None:
        from matrx_ai.tools.models import to_json_safe

        parsed_result: Any = None
        if result is not None:
            output = result.output
            if isinstance(output, dict):
                parsed_result = output
            elif isinstance(output, str):
                try:
                    parsed_result = json.loads(output)
                except (json.JSONDecodeError, TypeError):
                    parsed_result = output
            elif output is not None:
                parsed_result = output

        # Completion events are persisted independently of ToolResult. Keep
        # this copy PostgreSQL-safe even if a caller skipped the executor's
        # prepare_metadata boundary.
        from matrx_ai.persistence.postgres_text import sanitize_postgres_text

        parsed_result = sanitize_postgres_text(
            parsed_result,
            path="tool_completed.result",
        ).value

        safe_result = to_json_safe(parsed_result)
        typed_data = ToolCompletedData(result=safe_result)
        full_event = ToolStreamEvent(
            event="tool_completed",
            call_id=self.call_id,
            tool_name=self.tool_name,
            message=message,
            show_spinner=False,
            data=typed_data.model_dump(),
        )
        wire_event = self._slim_completed_for_wire(
            full_event,
            safe_result,
            output_chars=getattr(result, "output_chars", None),
            has_surface_write=getattr(result, "surface_write", None) is not None,
        )
        await self.emit(full_event, wire_event=wire_event)

    def _slim_completed_for_wire(
        self,
        full_event: ToolStreamEvent,
        safe_result: Any,
        *,
        output_chars: int | None,
        has_surface_write: bool,
    ) -> ToolStreamEvent | None:
        """Lazy tool calls (S6): a non-pinned tool's big result never rides the stream.

        Returns the slim wire copy, or None when the full frame goes as is. The
        persisted copy (execution_events) and chat.tool_call.output are untouched.
        """
        from matrx_ai.tools.pinned_tools import (
            RESULT_INLINE_MAX_BYTES,
            RESULT_PREVIEW_MAX_CHARS,
            is_pinned,
            lazy_tool_results_enabled,
        )

        if not lazy_tool_results_enabled():
            return None
        if is_pinned(self.tool_name, safe_result, has_surface_write=has_surface_write):
            return None
        try:
            serialized = json.dumps(safe_result, default=str, ensure_ascii=False)
        except (TypeError, ValueError):
            serialized = str(safe_result)
        if len(serialized.encode("utf-8")) <= RESULT_INLINE_MAX_BYTES:
            return None
        slim = ToolCompletedData(
            result=None,
            result_omitted=True,
            result_preview=serialized[:RESULT_PREVIEW_MAX_CHARS],
            output_chars=output_chars if output_chars else len(serialized),
            tool_call_id=self.row_id,
        )
        return full_event.model_copy(update={"data": slim.model_dump()})

    async def error(self, message: str, error_type: str = "execution") -> None:
        typed_data = ToolErrorData(error_type=error_type)
        await self.emit(
            ToolStreamEvent(
                event="tool_error",
                call_id=self.call_id,
                tool_name=self.tool_name,
                message=message,
                show_spinner=False,
                data=typed_data.model_dump(),
            )
        )

    # ------------------------------------------------------------------
    # TOOL-CALLABLE: progress / step / result_preview
    # ------------------------------------------------------------------

    async def progress(self, message: str, data: dict[str, Any] | None = None) -> None:
        typed_data = ToolProgressData(metadata=data or {})
        await self.emit(
            ToolStreamEvent(
                event="tool_progress",
                call_id=self.call_id,
                tool_name=self.tool_name,
                message=message,
                data=typed_data.model_dump(),
            )
        )

    async def step(
        self, step_name: str, message: str, data: dict[str, Any] | None = None
    ) -> None:
        typed_data = ToolStepData(step=step_name, metadata=data or {})
        await self.emit(
            ToolStreamEvent(
                event="tool_step",
                call_id=self.call_id,
                tool_name=self.tool_name,
                message=message,
                data=typed_data.model_dump(),
            )
        )

    async def result_preview(self, preview: str) -> None:
        typed_data = ToolResultPreviewData(preview=preview[:500])
        await self.emit(
            ToolStreamEvent(
                event="tool_result_preview",
                call_id=self.call_id,
                tool_name=self.tool_name,
                message="Preview available",
                data=typed_data.model_dump(),
            )
        )

    # ------------------------------------------------------------------

    def get_events_for_persistence(self) -> list[dict[str, Any]]:
        return [e.model_dump() for e in self._events]
