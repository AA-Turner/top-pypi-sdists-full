from dataclasses import dataclass
from datetime import datetime
from typing import Any
from orionis.console.entities.job_event_data import JobEventData

@dataclass(kw_only=True)
class JobExecuted(JobEventData):
    """
    Represents an event triggered when a job completes successfully.

    This class is used to encapsulate information about a successfully executed job, 
    including the time it was scheduled to run and the return value of the job function.

    Attributes
    ----------
    scheduled_run_time : datetime
        The datetime when the job was scheduled to execute.
    retval : Any
        The return value produced by the job function upon successful execution.

    Returns
    -------
    JobExecuted
        An instance of the `JobExecuted` class containing details about the executed job.
    """

    # The datetime when the job was scheduled to run
    scheduled_run_time: datetime

    # The return value of the job function
    retval: Any