from dataclasses import dataclass
from orionis.console.entities.job_event_data import JobEventData

@dataclass(kw_only=True)
class JobResume(JobEventData):
    """
    Represents an event triggered when a job is resumed from a paused state.

    This class extends `JobEventData` to provide additional context or 
    functionality specific to the resumption of a job.

    Attributes
    ----------
    (Inherited from JobEventData)
        All attributes from the parent class `JobEventData` are available 
        in this class.

    Returns
    -------
    JobResume
        An instance of the `JobResume` class representing the resumption event.
    """

    # This class does not define additional attributes or methods.
    # It serves as a specialized event type for job resumption.