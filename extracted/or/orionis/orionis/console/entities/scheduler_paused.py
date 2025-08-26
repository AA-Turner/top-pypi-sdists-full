from dataclasses import dataclass
from orionis.console.entities.scheduler_event_data import SchedulerEventData

@dataclass(kw_only=True)
class SchedulerPaused(SchedulerEventData):
    """
    Represents an event triggered when the scheduler is paused.

    This class is a data structure that inherits from `SchedulerEventData` 
    and is used to encapsulate information related to the scheduler pause event.

    Attributes
    ----------
    (Inherited from SchedulerEventData)
    """

    time: str  # Time when the scheduler was paused