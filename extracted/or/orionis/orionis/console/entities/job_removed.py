from dataclasses import dataclass
from orionis.console.entities.job_event_data import JobEventData

@dataclass(kw_only=True)
class JobRemoved(JobEventData):
    """
    Represents an event triggered when a job is removed from a job store.

    This class extends `JobEventData` to provide additional context or 
    functionality specific to the removal of a job.

    Attributes
    ----------
    (Inherited from JobEventData)

    Returns
    -------
    JobRemoved
        An instance of the `JobRemoved` class representing the removal event.
    """
    # No additional attributes or methods are defined here; this class 
    # serves as a specialized event type for job removal.