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
    """
    Types of notebooks.
    """

    STANDALONE = "plain"
    CODESPACE = "codespace"


class RunType(StrEnum):
    """
    Types of notebook job runs.
    """

    SCHEDULED = "scheduled"
    MANUAL = "manual"
    PIPELINE = "pipeline"


class ManualRunType(StrEnum):
    """
    A subset of :py:class:`RunType <datarobot.models.notebooks.enums.RunType>`
    To be used in API schemas.
    """

    MANUAL = "manual"
    PIPELINE = "pipeline"


class SessionType(StrEnum):
    """
    Types of notebook sessions. Triggered sessions include notebook job runs whether manually triggered or scheduled.
    """

    INTERACTIVE = "interactive"
    TRIGGERED = "triggered"


class ScheduleStatus(StrEnum):
    """
    Possible statuses for notebook schedules.
    """

    ENABLED = "enabled"
    DISABLED = "disabled"


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
    """
    Permissions for notebooks.
    """

    CAN_READ = "CAN_READ"
    CAN_UPDATE = "CAN_UPDATE"
    CAN_DELETE = "CAN_DELETE"
    CAN_SHARE = "CAN_SHARE"
    CAN_COPY = "CAN_COPY"
    CAN_EXECUTE = "CAN_EXECUTE"


class NotebookStatus(StrEnum):
    """
    Possible statuses for notebook sessions.
    """

    STOPPING = "stopping"
    STOPPED = "stopped"
    STARTING = "starting"
    RUNNING = "running"
    RESTARTING = "restarting"
    DEAD = "dead"
    DELETED = "deleted"


class KernelExecutionStatus(StrEnum):
    """
    Possible statuses for kernel execution.
    """

    BUSY = "busy"
    IDLE = "idle"


class CellType(StrEnum):
    """
    Types of cells in a notebook.
    """

    CODE = "code"
    MARKDOWN = "markdown"


class RuntimeLanguage(StrEnum):
    """
    Languages as used in notebook jupyter kernels.
    """

    PYTHON = "python3"
    R = "ir"


class ImageLanguage(StrEnum):
    """
    Languages as used and supported in notebook images.
    """

    PYTHON = "Python"
    R = "R"


class KernelSpec(StrEnum):
    """
    Kernel specifications for Jupyter notebook kernels.
    """

    PYTHON = "python3"
    R = "ir"

    @classmethod
    def from_image_language(cls, image_language: ImageLanguage) -> KernelSpec:
        if image_language == ImageLanguage.R:
            return cls.R
        return cls.PYTHON


class KernelState(StrEnum):
    """
    Possible states for notebook kernels.
    """

    CONNECTING = "connecting"
    DISCONNECTED = "disconnected"
    CONNECTED = "connected"
    STARTING = "starting"
    IDLE = "idle"
    BUSY = "busy"
    INTERRUPTING = "interrupting"
    RESTARTING = "restarting"
    NOT_RUNNING = "not_running"
