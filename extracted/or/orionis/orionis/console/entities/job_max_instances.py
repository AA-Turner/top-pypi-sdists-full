from dataclasses import dataclass
from datetime import datetime
from orionis.console.entities.job_event_data import JobEventData

@dataclass(kw_only=True)
class JobMaxInstances(JobEventData):
    """
    Represents an event triggered when a job exceeds its maximum allowed instances.

    This class is a specialized event data structure that inherits from `JobEventData`. 
    It is used to capture and store information about the event when a job exceeds 
    the maximum number of instances it is allowed to run.

    Attributes
    ----------
    run_time : datetime
        The datetime when the job was scheduled to run. This indicates the time 
        the job was supposed to execute before exceeding the instance limit.

    Returns
    -------
    JobMaxInstances
        An instance of the `JobMaxInstances` class containing the event details.
    """

    # The time the job was scheduled to run
    run_time: datetime