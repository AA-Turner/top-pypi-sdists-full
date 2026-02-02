"""Types for container build log streaming."""

from typing import Literal

import msgspec


class BuildLogOutput(msgspec.Struct, tag="container_build_log_output"):
    """A single log line from a container build."""

    container_image_uuid: str
    data: str
    timestamp: float
    phase: Literal[
        "verification", "setup_repo", "build_script", "run_script", "complete_build"
    ] = "build_script"
    level: Literal["info", "error", "warning"] = "info"
    command: str | None = None


class BuildLogStatus(msgspec.Struct, tag="container_build_log_status"):
    """Status update for a container build."""

    container_image_uuid: str
    status: Literal["started", "completed", "failed"]
    timestamp: float
    message: str | None = None


BuildLogMessage = BuildLogOutput | BuildLogStatus
