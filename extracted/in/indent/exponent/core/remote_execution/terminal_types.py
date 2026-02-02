"""Type definitions for terminal output streaming."""

from typing import Literal

import msgspec


class TerminalOutput(msgspec.Struct, tag="terminal_output"):
    """Terminal output data from CLI to web client."""

    session_id: str
    data: str
    timestamp: float


class TerminalStatus(msgspec.Struct, tag="terminal_status"):
    """Terminal status update from CLI to web client."""

    session_id: str
    status: Literal["started", "exited"]
    message: str
    exit_code: int | None = None
    name: str | None = None


class TerminalResetSessions(msgspec.Struct, tag="terminal_reset_sessions"):
    """Sent from CLI when terminal session manager starts to clear stale sessions."""

    # No fields needed - just a signal


TerminalMessage = TerminalOutput | TerminalStatus | TerminalResetSessions
