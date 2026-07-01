"""Public exception hierarchy raised by the SDK.

Callers can branch on the kind of failure they care about:

    try:
        out = await session.call_tool("foo", {...})
    except SessionTerminatedError:
        # Session is gone or unrecoverable — tear down and start over.
    except TransportError:
        # Network/infra problem — abort or escalate to outer retry.
    except ToolCallError:
        # Call was malformed — tell the model so it can reformulate.
    except ToolFailed:
        # Tool reached the server but failed past the transport.
        # The session has also been marked dead — subsequent calls
        # will raise SessionTerminatedError.
"""

from __future__ import annotations

from typing import Literal, Optional


class OpenRewardError(Exception):
    """Base class for all SDK errors."""


# ── Session lifecycle ───────────────────────────────────────────────────

class SessionTerminatedError(OpenRewardError):
    """Session is gone or unrecoverable.

    Raised either because the server signalled termination (404/410 on a
    session-bearing call, or a ping that returned a terminal error) or
    because a prior ToolFailed marked the session dead client-side.
    """

    def __init__(
        self,
        reason: str,
        *,
        sid: Optional[str] = None,
        kind: Optional[str] = None,
    ) -> None:
        self.reason = reason
        self.sid = sid
        self.kind = kind
        super().__init__(f"{kind} session terminated (sid={sid!r}): {reason}")


# ── Transport ───────────────────────────────────────────────────────────

class TransportError(OpenRewardError):
    """Network or protocol failure independent of user code."""


class MaxRetriesError(TransportError):
    """SDK exhausted its retry budget on a transient transport failure."""

    def __init__(self, message: str, errors: Optional[list[Exception]] = None) -> None:
        self.errors = errors or []
        detail = f"{message}\n  Encountered {len(self.errors)} error(s):"
        for i, err in enumerate(self.errors, 1):
            detail += f"\n    [{i}] {type(err).__name__}: {err}"
        super().__init__(detail)


class HeartbeatTimeoutError(TransportError):
    """No frame received from the server within the heartbeat window."""


class HTTPStatusError(TransportError):
    """Non-retryable HTTP status from the server."""

    def __init__(self, status: int, body: Optional[str] = None) -> None:
        self.status = status
        self.body = body
        msg = f"HTTP {status}"
        if body:
            msg += f": {body}"
        super().__init__(msg)


# ── Tool-call outcomes ──────────────────────────────────────────────────

ToolCallErrorReason = Literal[
    "not_found",
    "name_collision",
    "input_validation",
    "bad_input_shape",
]


class ToolCallError(OpenRewardError):
    """Tool call was malformed — won't succeed by retrying the same args.

    The ``reason`` discriminates between the specific malformation, so the
    caller can phrase the feedback to the model appropriately.
    """

    def __init__(self, reason: ToolCallErrorReason, detail: str) -> None:
        self.reason = reason
        self.detail = detail
        super().__init__(f"{reason}: {detail}")


class ToolFailed(OpenRewardError):
    """Tool reached the server but failed past the transport.

    Covers user @tool functions that raised and tools that returned a
    non-ToolOutput value. The SDK does not retry these — tools are
    expected to handle their own retrying internally.

    Whenever the SDK raises this, the originating session has also been
    marked dead; subsequent calls on the same session will raise
    SessionTerminatedError. Callers should treat this as an end-of-rollout
    signal and tear down.
    """

    def __init__(self, message: str) -> None:
        self.message = message
        super().__init__(message)
