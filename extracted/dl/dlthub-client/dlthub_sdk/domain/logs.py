"""Log lines — what a run printed, historic or live."""

from __future__ import annotations

# Python internals
from dataclasses import dataclass
from datetime import datetime
from typing import TYPE_CHECKING, Any

# Current package
from dlthub_sdk._glue.context import _Ctx
from dlthub_sdk._glue.enums import StrEnum

if TYPE_CHECKING:
    # Typing only: domain never imports _gen at runtime.
    # Current package
    from dlthub_sdk._gen.logs.models import LogLine as LogLinePayload


class LogSource(StrEnum):
    """Who emitted a log line."""

    USER = "user"
    """The user's own code."""
    SETUP = "setup"
    """The install and build commands that prepare the run."""
    RUNNER = "runner"
    """The platform's bootstrap around the user's code."""
    UNKNOWN = "unknown"
    """A source this SDK version does not know."""


class LogStage(StrEnum):
    """Which stage of the run a log line belongs to."""

    BUILD = "build"
    """Preparing the environment the code runs in."""
    RUN = "run"
    """Executing the code."""
    UNKNOWN = "unknown"
    """A stage this SDK version does not know."""


class LogIoStream(StrEnum):
    """The stream a log line was written to."""

    STDOUT = "stdout"
    """Standard output."""
    STDERR = "stderr"
    """Standard error."""
    OTHER = "other"
    """Neither: an info channel of the compute backend, or a line stored before the
    stream was recorded.
    """
    UNKNOWN = "unknown"
    """A stream this SDK version does not know."""


@dataclass(frozen=True)
class LogLine:
    """One line a run emitted."""

    content: str
    """Contents of the log message."""
    line_num: int
    """Position of the line in the run's log."""
    source: LogSource
    """Who emitted the line."""
    stage: LogStage
    """Stage of the run the line belongs to: `build` (installing dependencies before the
    job starts) or `run` (the job's execution).
    """
    io_stream: LogIoStream
    """Stream the line was written to: `stdout`, `stderr`, or `other` (a provider's info
    channel, or a line stored before streams were kept).
    """
    reported_at: datetime
    """Timestamp when the log was reported."""

    @staticmethod
    def _from_payload(_ctx: _Ctx[Any], payload: LogLinePayload) -> LogLine:
        return LogLine(
            content=payload.content,
            line_num=payload.line_num,
            source=LogSource(str(payload.source)),
            stage=LogStage(str(payload.stage)),
            io_stream=LogIoStream(str(payload.io_stream)),
            reported_at=payload.reported_at,
        )
