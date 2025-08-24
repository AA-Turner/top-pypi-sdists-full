from dataclasses import dataclass
from orionis.console.entities.job_event_data import JobEventData

@dataclass(kw_only=True)
class JobAdded(JobEventData):
    """
    Represents an event triggered when a job is added to a job store.

    This class extends the `JobEventData` base class, inheriting its attributes
    and functionality. It is used to encapsulate data related to the addition
    of a job in the system.

    Attributes
    ----------
    Inherits all attributes from the `JobEventData` base class.

    Returns
    -------
    JobAdded
        An instance of the `JobAdded` class containing data about the added job.
    """

    # This class currently does not define additional attributes or methods.
    # It serves as a specialized event type for job addition events.
