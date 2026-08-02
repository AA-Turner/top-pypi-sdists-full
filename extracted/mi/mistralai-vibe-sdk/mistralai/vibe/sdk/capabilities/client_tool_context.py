"""Execution context for client-handled tool callbacks."""

from contextvars import ContextVar, Token
from dataclasses import dataclass
from typing import Literal

from mistralai.vibe.sdk.transports.events import CallbackCallEvent

ClientToolCallMode = Literal["async", "sync"]
ClientToolStatus = Literal["running", "completed", "failed", "canceled"]


@dataclass(slots=True)
class ClientToolExecutionContext:
    event: CallbackCallEvent
    call_mode: ClientToolCallMode
    status: ClientToolStatus = "running"
    failure_stage: str | None = None
    error_type: str | None = None

    @property
    def span_name(self) -> str:
        return f"execute_tool {self.event.payload.name}"

    def record_result(
        self,
        *,
        failure_stage: str | None,
        error_type: str | None = None,
    ) -> None:
        if failure_stage is None:
            self.status = "completed"
            return
        self.status = "failed"
        self.failure_stage = failure_stage
        self.error_type = error_type or failure_stage

    def mark_canceled(self) -> None:
        if self.status == "failed":
            return
        self.status = "canceled"
        self.failure_stage = None
        self.error_type = None

    def mark_send_failed(self, exc: Exception | None = None) -> None:
        self.status = "failed"
        self.failure_stage = "send_message"
        self.error_type = _exception_type(exc) if exc is not None else "send_message"

    def attributes(self) -> dict[str, object]:
        attributes: dict[str, object] = {
            "tool_name": self.event.payload.name,
            "gen_ai.operation.name": "execute_tool",
            "gen_ai.tool.call.id": self.event.payload.id,
            "gen_ai.tool.name": self.event.payload.name,
            "gen_ai.tool.type": "function",
            "callback_id": self.event.payload.id,
            "callback_path_length": len(self.event.payload.path or []),
            "call_mode": self.call_mode,
            "status": self.status,
        }
        if self.failure_stage is not None:
            attributes["failure_stage"] = self.failure_stage
        if self.error_type is not None:
            attributes["error.type"] = self.error_type
        return attributes

    def log_context(self) -> dict[str, object]:
        return {
            "tool_name": self.event.payload.name,
            "callback_id": self.event.payload.id,
            "call_mode": self.call_mode,
        }


def exception_type(exc: Exception) -> str:
    return _exception_type(exc)


def _exception_type(exc: Exception) -> str:
    exc_type = type(exc)
    if exc_type.__module__ == "builtins":
        return exc_type.__qualname__
    return f"{exc_type.__module__}.{exc_type.__qualname__}"


_current_client_tool_context: ContextVar[ClientToolExecutionContext | None] = ContextVar(
    "current_client_tool_context",
    default=None,
)


def current_client_tool_context() -> ClientToolExecutionContext | None:
    return _current_client_tool_context.get()


def set_client_tool_context(
    context: ClientToolExecutionContext,
) -> Token[ClientToolExecutionContext | None]:
    return _current_client_tool_context.set(context)


def reset_client_tool_context(
    token: Token[ClientToolExecutionContext | None],
) -> None:
    _current_client_tool_context.reset(token)
