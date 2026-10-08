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
    """Who emitted a log line.

    Attributes:
        USER: The user's own code.
        SETUP: The install and build commands that prepare the run.
        RUNNER: The platform's bootstrap around the user's code.
        UNKNOWN: A source this SDK version does not know.
    """

    USER = "user"
    SETUP = "setup"
    RUNNER = "runner"
    UNKNOWN = "unknown"


class LogStage(StrEnum):
    """Which stage of the run a log line belongs to.

    Attributes:
        BUILD: Preparing the environment the code runs in.
        RUN: Executing the code.
        UNKNOWN: A stage this SDK version does not know.
    """

    BUILD = "build"
    RUN = "run"
    UNKNOWN = "unknown"


class LogIoStream(StrEnum):
    """The stream a log line was written to.

    Attributes:
        STDOUT: Standard output.
        STDERR: Standard error.
        OTHER: Neither, such as a structured log record.
        UNKNOWN: A stream this SDK version does not know.
    """

    STDOUT = "stdout"
    STDERR = "stderr"
    OTHER = "other"
    UNKNOWN = "unknown"


@dataclass(frozen=True)
class LogLine:
    """One line a run emitted.

    Attributes:
        content: What was written.
        line_num: Its position in the run's log.
        source: Who emitted it.
        stage: Which stage of the run it belongs to.
        io_stream: The stream it was written to.
        reported_at: When the producer reported it.
    """

    content: str
    line_num: int
    source: LogSource
    stage: LogStage
    io_stream: LogIoStream
    reported_at: datetime

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
