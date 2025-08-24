from dataclasses import dataclass
from datetime import datetime
from orionis.console.entities.job_event_data import JobEventData

@dataclass(kw_only=True)
class JobSubmitted(JobEventData):
    """
    Represents an event triggered when a job is submitted to an executor.

    This class extends `JobEventData` and includes additional information 
    about the scheduled execution time of the job.

    Attributes
    ----------
    run_time : datetime
        The datetime when the job is scheduled to run.

    Returns
    -------
    None
        This class does not return a value; it is used to encapsulate event data.
    """
    # The datetime when the job is scheduled to run
    run_time: datetime
