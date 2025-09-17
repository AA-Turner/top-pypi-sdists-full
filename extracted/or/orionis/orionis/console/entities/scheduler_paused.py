from dataclasses import dataclass
from datetime import datetime
from orionis.console.entities.scheduler_event_data import SchedulerEventData

@dataclass(kw_only=True)
class SchedulerPaused(SchedulerEventData):
    """
    Represents an event triggered when the scheduler is paused.

    This data class extends `SchedulerEventData` and encapsulates information
    related to the scheduler pause event, such as the time at which the pause occurred.

    Parameters
    ----------
    time : str or datetime, optional
        The time when the scheduler was paused. Can be a string or a `datetime` object.
        Defaults to None.
    (Other parameters are inherited from SchedulerEventData.)

    Attributes
    ----------
    time : str or datetime
        The time when the scheduler was paused.
    (Other attributes are inherited from SchedulerEventData.)

    Returns
    -------
    SchedulerPaused
        An instance of `SchedulerPaused` containing information about the pause event.
    """

    # The time when the scheduler was paused; can be a string or datetime object
    time: str | datetime = None
