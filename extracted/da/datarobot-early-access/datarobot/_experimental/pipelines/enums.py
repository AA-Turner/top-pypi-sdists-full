#
# Copyright 2026 DataRobot, Inc. and its affiliates.
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

from strenum import StrEnum


class PipelineMode(StrEnum):
    DRAFT = "draft"
    LOCKED = "locked"


class PipelineVersionStatus(StrEnum):
    PENDING = "PENDING"
    READY = "READY"
    FAILED = "FAILED"


class PipelineDispatchStatus(StrEnum):
    PENDING = "PENDING"
    RUNNING = "RUNNING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"
    CANCELLED = "CANCELLED"
    ERRORED = "ERRORED"


class PipelineDispatchTrigger(StrEnum):
    API = "api"
    SCHEDULE = "schedule"


class PipelineInputState(StrEnum):
    VALID = "VALID"
    INVALID = "INVALID"


class PipelineScheduleStatus(StrEnum):
    ACTIVE = "ACTIVE"
    PAUSED = "PAUSED"
    DELETED = "DELETED"


class PipelineImageStatus(StrEnum):
    CREATING = "CREATING"
    READY = "READY"
    ERROR = "ERROR"
