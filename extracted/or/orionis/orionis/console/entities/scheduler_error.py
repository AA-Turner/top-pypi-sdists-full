from dataclasses import dataclass
from typing import Optional
from orionis.console.entities.scheduler_event_data import SchedulerEventData

@dataclass(kw_only=True)
class SchedulerError(SchedulerEventData):
    """
    Represents an event triggered when the scheduler is paused.

    This class is a data structure that inherits from `SchedulerEventData` 
    and is used to encapsulate information related to the scheduler pause event.

    Attributes
    ----------
    (Inherited from SchedulerEventData)
    """

    exception: Optional[BaseException] = None  # Exception that caused the scheduler error
    traceback: Optional[str] = None  # Traceback information related to the scheduler error