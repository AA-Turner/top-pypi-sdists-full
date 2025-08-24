from dataclasses import dataclass
from orionis.console.entities.scheduler_event_data import SchedulerEventData

@dataclass(kw_only=True)
class AllJobsRemoved(SchedulerEventData):
    """
    Represents an event triggered when all jobs are removed from a specific job store.

    This event is typically used to notify that a job store has been cleared of all its jobs.

    Attributes
    ----------
    jobstore : str
        The alias or identifier of the job store from which all jobs were removed.

    Returns
    -------
    None
        This class does not return a value; it is used to encapsulate event data.
    """

    # The alias of the job store from which jobs were removed
    jobstore: str