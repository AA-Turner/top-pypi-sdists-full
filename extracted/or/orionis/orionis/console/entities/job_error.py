from dataclasses import dataclass
from datetime import datetime
from orionis.console.entities.job_event_data import JobEventData

@dataclass(kw_only=True)
class JobError(JobEventData):
    """
    Represents an event triggered when a job raises an exception during execution.

    This class is used to encapsulate information about an error that occurred
    during the execution of a scheduled job, including the time the job was
    scheduled to run, the exception raised, and the traceback details.

    Attributes
    ----------
    scheduled_run_time : datetime
        The datetime when the job was scheduled to run.
    exception : Exception
        The exception instance raised by the job during execution.
    traceback : str
        The traceback string providing details about where the exception occurred.

    Returns
    -------
    JobError
        An instance of the `JobError` class containing details about the job error event.
    """
    # The time the job was scheduled to run
    scheduled_run_time: datetime

    # The exception raised during the job's execution
    exception: Exception

    # The traceback string providing details about the exception
    traceback: str