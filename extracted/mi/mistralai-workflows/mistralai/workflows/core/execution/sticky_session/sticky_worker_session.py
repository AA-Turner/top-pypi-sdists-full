from typing import Callable

import structlog
from pydantic import BaseModel

logger = structlog.get_logger(__name__)

# This is checked during worker registration to determine task queue routing.
_ACTIVITY_STICKY_TO_WORKER_ATTR_NAME = "__wf_activity_sticky_to_worker"


class StickyWorkerSession(BaseModel):
    """
    Used to route activities to a specific worker instance
    """

    task_queue: str


def set_activity_as_sticky_to_worker(activity: Callable) -> None:
    """
    Activities marked as sticky are registered on the worker's unique
    task queue and routed via context_var_task_queue.
    """
    setattr(activity, _ACTIVITY_STICKY_TO_WORKER_ATTR_NAME, True)


def check_activity_is_sticky_to_worker(activity: Callable) -> bool:
    return getattr(activity, _ACTIVITY_STICKY_TO_WORKER_ATTR_NAME, False)
