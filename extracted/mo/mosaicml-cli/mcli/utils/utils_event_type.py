"""Utilities for interpreting event type"""
from __future__ import annotations

from enum import Enum

__all__ = ['EventType']


class EventType(Enum):
    """Possible types of event during a run
    """

    #: The run has been created and is waiting to be scheduled
    CREATED = 'CREATED'

    #: The run has passed preflight check
    CHECK_PASSED = 'CHECK_PASSED'

    #: The run has failed preflight check
    CHECK_FAILED = 'CHECK_FAILED'

    #: The run status has changed from pending/queued to running
    STARTED = 'STARTED'

    #: The train data has been validated
    DATA_VALIDATED = 'DATA_VALIDATED'

    #: The model has been initialized
    MODEL_INITIALIZED = 'MODEL_INITIALIZED'

    #: A batch of training data has been processed
    TRAIN_UPDATED = 'TRAIN_UPDATED'

    #: The model has finished training, checkpoint uploading has begun
    TRAIN_FINISHED = 'TRAIN_FINISHED'

    #: The run has finished without any errors
    COMPLETED = 'COMPLETED'

    #: User has manually stopped a run from mcli or in Morc
    STOPPED = 'STOPPED'

    #: User has manually stopped a run from mcli/databricks_genai API
    CANCELED = 'CANCELED'

    #: The run has failed
    FAILED = 'FAILED'

    # Reason for the run failure
    FAILED_EXCEPTION = 'FAILED_EXCEPTION'

    #: Checkpoint has been saved
    CHECKPOINT_SAVED = 'CHECKPOINT_SAVED'

    #: The run has begun training
    TRAIN_STARTED = 'TRAIN_STARTED'

    #: The run has been automatically requested by Morc
    REQUEUED = 'REQUEUED'

    def __str__(self) -> str:
        return self.value
