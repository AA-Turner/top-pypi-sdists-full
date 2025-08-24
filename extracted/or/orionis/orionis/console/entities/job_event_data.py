from dataclasses import dataclass
from typing import Optional
from orionis.console.entities.scheduler_event_data import SchedulerEventData

@dataclass(kw_only=True)
class JobEventData(SchedulerEventData):
    """
    Represents the base class for events related to jobs in the scheduler system.

    This class extends `SchedulerEventData` and provides additional attributes
    specific to job-related events, such as the job's identifier and the job store
    where it resides.

    Attributes
    ----------
    code : int
        A numeric code that uniquely identifies the type of event within the
        scheduler system. (Inherited from `SchedulerEventData`)
    alias : str, optional
        An optional string providing additional context or identifying specific
        components (e.g., executors or job stores) related to the event.
        (Inherited from `SchedulerEventData`)
    job_id : str
        The unique identifier of the job associated with the event.
    jobstore : str, optional
        The name of the job store where the job is located. If not specified,
        it defaults to `None`.

    Returns
    -------
    JobEventData
        An instance of the `JobEventData` class containing information about
        the job-related event.
    """

    # The unique identifier of the job
    job_id: str

    # The name of the job store where the job resides (optional)
    jobstore: Optional[str] = None
