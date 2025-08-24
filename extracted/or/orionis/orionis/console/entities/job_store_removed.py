from dataclasses import dataclass
from orionis.console.entities.scheduler_event_data import SchedulerEventData

@dataclass(kw_only=True)
class JobstoreRemoved(SchedulerEventData):
    """
    Represents an event triggered when a job store is removed.

    This event is typically used to notify the system or other components
    that a specific job store has been removed, allowing for any necessary
    cleanup or updates.

    Attributes
    ----------
    alias : str
        The alias (unique identifier) of the removed job store.

    Returns
    -------
    None
        This class does not return a value; it is used to encapsulate event data.
    """

    # The alias of the removed job store
    alias: str