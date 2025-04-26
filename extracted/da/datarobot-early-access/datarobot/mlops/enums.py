#
# Copyright 2024 DataRobot, Inc. and its affiliates.
#
# All rights reserved.
#
# DataRobot, Inc.
#
# This is proprietary source code of DataRobot, Inc. and its
# affiliates.
#
# Released under the terms of DataRobot Tool and Utility Agreement.
from enum import Enum
from typing import List


class RemoteEventType(Enum):
    MODERATION_METRIC_CREATION_ERROR = "moderationMetricCreationError"
    MODERATION_METRIC_REPORTING_ERROR = "moderationMetricReportingError"
    MODERATION_MODEL_CONFIG_ERROR = "moderationModelConfigError"
    MODERATION_MODEL_RUNTIME_ERROR = "moderationModelRuntimeError"
    MODERATION_MODEL_SCORING_ERROR = "moderationModelScoringError"

    @classmethod
    def moderation_event_types(cls) -> List[str]:
        return [
            cls.MODERATION_METRIC_CREATION_ERROR.value,
            cls.MODERATION_METRIC_REPORTING_ERROR.value,
            cls.MODERATION_MODEL_CONFIG_ERROR.value,
            cls.MODERATION_MODEL_RUNTIME_ERROR.value,
            cls.MODERATION_MODEL_SCORING_ERROR.value,
        ]


class EventStatusType(Enum):
    """Defines the status for the MLOps event."""

    SUCCESS = "success"
    FAILURE = "failure"
    WARNING = "warning"
    INFO = "info"

    @classmethod
    def all(cls) -> List[str]:
        return [cls.SUCCESS.value, cls.FAILURE.value, cls.WARNING.value, cls.INFO.value]
