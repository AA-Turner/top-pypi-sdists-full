#
# Copyright 2025 DataRobot, Inc. and its affiliates.
#
# All rights reserved.
#
# DataRobot, Inc.
#
# This is proprietary source code of DataRobot, Inc. and its
# affiliates.
#
# Released under the terms of DataRobot Tool and Utility Agreement.
from __future__ import annotations

from typing import List

from strenum import StrEnum


class NotebookType(StrEnum):
    STANDALONE = "plain"
    CODESPACE = "codespace"


class RunType(StrEnum):
    SCHEDULED = "scheduled"
    MANUAL = "manual"
    PIPELINE = "pipeline"


class ManualRunType(StrEnum):
    """
    A subset of :py:class:`RunType <datarobot._experimental.models.notebooks.enums.RunType>`
    To be used in API schemas.
    """

    MANUAL = "manual"
    PIPELINE = "pipeline"


class SessionType(StrEnum):
    INTERACTIVE = "interactive"
    TRIGGERED = "triggered"


class ScheduledRunStatus(StrEnum):
    """
    Possible statuses for scheduled notebook runs.
    """

    BLOCKED = "BLOCKED"
    CREATED = "CREATED"
    STARTED = "STARTED"
    EXPIRED = "EXPIRED"
    ABORTED = "ABORTED"
    INCOMPLETE = "INCOMPLETE"
    RUNNING = "RUNNING"
    PAUSED = "PAUSED"
    INITIALIZED = "INITIALIZED"
    COMPLETED = "COMPLETED"
    ERROR = "ERROR"
    COMPLETED_WITH_ERRORS = "COMPLETED_WITH_ERRORS"

    @classmethod
    def terminal_statuses(cls) -> List[str]:
        return [
            cls.ABORTED,
            cls.COMPLETED,
            cls.ERROR,
            cls.COMPLETED_WITH_ERRORS,
        ]


class NotebookPermissions(StrEnum):
    CAN_READ = "CAN_READ"
    CAN_UPDATE = "CAN_UPDATE"
    CAN_DELETE = "CAN_DELETE"
    CAN_SHARE = "CAN_SHARE"
    CAN_COPY = "CAN_COPY"
    CAN_EXECUTE = "CAN_EXECUTE"


class NotebookStatus(StrEnum):
    STOPPING = "stopping"
    STOPPED = "stopped"
    STARTING = "starting"
    RUNNING = "running"
    RESTARTING = "restarting"
    DEAD = "dead"
    DELETED = "deleted"


class KernelExecutionStatus(StrEnum):
    BUSY = "busy"
    IDLE = "idle"


class CellType(StrEnum):
    CODE = "code"
    MARKDOWN = "markdown"


class RuntimeLanguage(StrEnum):
    PYTHON = "python"
    R = "r"


class ImageLanguage(StrEnum):
    PYTHON = "Python"
    R = "R"


class KernelSpec(StrEnum):
    PYTHON = "python3"
    R = "r"

    @classmethod
    def from_image_language(cls, image_language: ImageLanguage) -> KernelSpec:
        if image_language == ImageLanguage.R:
            return cls.R
        return cls.PYTHON


class KernelState(StrEnum):
    CONNECTING = "connecting"
    DISCONNECTED = "disconnected"
    CONNECTED = "connected"
    STARTING = "starting"
    IDLE = "idle"
    BUSY = "busy"
    INTERRUPTING = "interrupting"
    RESTARTING = "restarting"
    NOT_RUNNING = "not_running"
