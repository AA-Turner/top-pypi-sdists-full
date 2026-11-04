"""Tool errors: what the model sees when a tool, a client tool's answer or ``on_client_tool`` raises."""

import asyncio
import logging
from collections.abc import Mapping
from typing import Literal

from pydantic import BaseModel, JsonValue

from mistralai.vibe_agents.sdk.authoring.tool_result import ToolResult

type ToolErrors = Literal["hide", "show", "raise"]
"""What an unexpected exception from a tool does: ``Agent(tool_errors=...)``."""

DEFAULT_TOOL_ERRORS: ToolErrors = "hide"

UNEXPECTED_TOOL_ERROR_TEXT = "The tool failed with an unexpected error."
"""What the model reads, with ``tool_errors="hide"``, when a tool raises anything but ``ToolError``."""

logger = logging.getLogger(__name__)


class ToolError(Exception):
    """Fail the tool call with a message the model sees as written.

    Raise it in a tool, a client tool's answer or ``on_client_tool``. The model gets a failed call
    with ``message`` only, whatever ``Agent(tool_errors=...)`` says, and can act on it, for example
    by asking the user or calling the tool again with other arguments. ``structured_content`` and
    ``meta`` go with the failed result as they do with ``ToolResult``; the model never sees ``meta``.
    ``ToolResult.error(message)``, returned instead, does the same. Both check ``structured_content``
    and ``meta`` where they are built: a value that is not JSON raises ``pydantic.ValidationError``
    there, in your code.
    """

    def __init__(
        self,
        message: str,
        *,
        structured_content: JsonValue | BaseModel = None,
        meta: Mapping[str, JsonValue] | None = None,
    ) -> None:
        # Built now, as ToolResult.error is: a value that is not JSON fails at the raise site, in the
        # author's code, rather than later where the SDK answers the call.
        self._result = ToolResult.error(message, structured_content=structured_content, meta=meta)
        super().__init__(message)
        self.message = message
        self.structured_content = structured_content
        self.meta: dict[str, JsonValue] = dict(meta or {})

    def _to_tool_result(self) -> ToolResult:
        """The failed result the model gets."""

        return self._result


type ToolCodeError = Exception | asyncio.CancelledError
"""What the author's code can raise that follows ``tool_errors``: any exception, and a ``CancelledError``
that nobody cancelling the call caused (see ``call_is_cancelling``)."""


class ToolFunctionError(Exception):
    """Internal: the author's function raised ``error``, or returned a value that cannot be sent; the SDK's
    checks of the model's arguments did not.

    Only an exception of the author's own code follows ``tool_errors``: an argument the model got
    wrong still reaches the model as written, so it can correct the call.
    """

    def __init__(self, error: ToolCodeError) -> None:
        super().__init__(error)
        self.error = error


def call_is_cancelling() -> bool:
    """Whether the task running a tool call is being cancelled: tell this from a ``CancelledError`` the
    tool's own code raised.

    Tool code can raise ``CancelledError`` while nobody cancels its call: it awaited a task or a
    future that something else cancelled, or a library raised it. That is the code's error, and it
    follows ``tool_errors``. Re-raised, it would end the call as cancelled, and the turn would wait
    for the call's result with no end. A call that is being cancelled (``interrupt()``, ``cancel()``,
    the end of a run) still ends cancelled.
    """

    task = asyncio.current_task()
    return task is not None and task.cancelling() > 0


def failed_tool_result(error: ToolCodeError, *, tool_errors: ToolErrors, tool_id: str) -> ToolResult:
    """The failed result the model gets for ``error``, by ``tool_errors``.

    ``ToolError`` keeps its message. Any other exception is logged with its traceback, and the model
    reads ``UNEXPECTED_TOOL_ERROR_TEXT`` (``"hide"``) or ``<type>: <message>`` (``"show"``). With
    ``"raise"`` the caller ends the turn instead; it gets this result only where it cannot.
    """

    if isinstance(error, ToolError):
        return error._to_tool_result()  # noqa: SLF001
    logger.error("Tool %s raised %s", tool_id, type(error).__name__, exc_info=error)
    if tool_errors == "show":
        return ToolResult.error(f"{type(error).__name__}: {error}")
    return ToolResult.error(UNEXPECTED_TOOL_ERROR_TEXT)


__all__ = [
    "DEFAULT_TOOL_ERRORS",
    "UNEXPECTED_TOOL_ERROR_TEXT",
    "ToolError",
    "ToolCodeError",
    "ToolErrors",
    "ToolFunctionError",
    "call_is_cancelling",
    "failed_tool_result",
]
