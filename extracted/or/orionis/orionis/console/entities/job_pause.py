from dataclasses import dataclass
from orionis.console.entities.job_event_data import JobEventData

@dataclass(kw_only=True)
class JobPause(JobEventData):
    """
    Represents an event triggered when a job is paused in the job store.

    This class extends `JobEventData` to provide additional context or
    functionality specific to the pausing of a job.

    Attributes
    ----------
    (Inherited from JobEventData)

    Returns
    -------
    JobPause
        An instance of the `JobPause` class representing the pause event.
    """
    # This class does not define additional attributes or methods.
    # It serves as a specialized event type for job pausing.