"""Utility functions for models"""
from __future__ import annotations

import logging
from enum import Enum

from mcli.utils.utils_run_status import CLI_STATUS_OPTIONS

logger = logging.getLogger(__name__)


class SubmissionType(Enum):
    """Types of submissions on MPlat
    """

    TRAINING = "Run"
    FINETUNING = "Fine-tuning"
    INFERENCE = "Inference Deployment"
    PRETRAINING = "Pre-training"

    @classmethod
    def get_status_options(cls, val: SubmissionType):
        if val is SubmissionType.TRAINING:
            return CLI_STATUS_OPTIONS
        else:
            return ["Pending", "Starting", "Ready", "Failed", "Stopped"]

    @classmethod
    def from_mapi(cls, value: str) -> SubmissionType:
        try:
            extracted = SubmissionType[value]
        except KeyError:
            logger.warning('Received invalid value for Submission Type. Defaulting to TRAINING')
            extracted = SubmissionType.TRAINING
        return extracted

    def __eq__(self, other: object) -> bool:
        assert isinstance(other, SubmissionType)
        return self.name == other.name
