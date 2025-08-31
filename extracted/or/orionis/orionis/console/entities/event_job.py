from dataclasses import dataclass
from datetime import datetime
from typing import Any, Callable, Optional, Tuple

@dataclass(kw_only=True)
class EventJob:
    """
    Represents the main properties and configuration of a scheduled job in APScheduler.

    Parameters
    ----------
    id : str
        Unique identifier for the job.
    code : int, optional
        Numeric code representing the job status or type. Defaults to 0.
    name : Optional[str], optional
        Human-readable name for the job. Defaults to None.
    func : Callable[..., Any], optional
        The function or coroutine to be executed by the job. Defaults to None.
    args : Tuple[Any, ...], optional
        Positional arguments to be passed to the function. Defaults to empty tuple.
    trigger : Any, optional
        The trigger that determines the job's execution schedule (e.g., IntervalTrigger, CronTrigger). Defaults to None.
    executor : str, optional
        Alias of the executor that will run the job. Defaults to 'default'.
    jobstore : str, optional
        Alias of the job store where the job is stored. Defaults to 'default'.
    misfire_grace_time : Optional[int], optional
        Grace period in seconds for handling missed executions. If None, no grace period is applied. Defaults to None.
    max_instances : int, optional
        Maximum number of concurrent instances of the job allowed. Defaults to 1.
    coalesce : bool, optional
        Whether to merge pending executions into a single execution. Defaults to False.
    next_run_time : Optional[datetime], optional
        The next scheduled execution time of the job. Can be None if the job is paused or unscheduled. Defaults to None.
    exception : Optional[BaseException], optional
        Exception raised during the last job execution, if any. Defaults to None.
    traceback : Optional[str], optional
        String representation of the traceback if an exception occurred. Defaults to None.
    retval : Optional[Any], optional
        Return value from the last job execution. Defaults to None.
    purpose : Optional[str], optional
        Description of the job's purpose. Defaults to None.
    start_date : Optional[datetime], optional
        The earliest possible run time for the job. Defaults to None.
    end_date : Optional[datetime], optional
        The latest possible run time for the job. Defaults to None.
    details : Optional[str], optional
        Additional details or metadata about the job. Defaults to None.

    Returns
    -------
    None
        This class is a data container and does not return any value upon instantiation.
    """
    id: str                                         # Unique identifier for the job
    code: int = 0                                   # Numeric code for job status/type
    name: Optional[str] = None                      # Human-readable job name
    func: Callable[..., Any] = None                 # Function or coroutine to execute
    args: Tuple[Any, ...] = ()                      # Positional arguments for the function
    trigger: Any = None                             # Scheduling trigger (e.g., interval, cron)
    executor: str = 'default'                       # Executor alias
    jobstore: str = 'default'                       # Job store alias
    misfire_grace_time: Optional[int] = None        # Grace period for missed executions
    max_instances: int = 1                          # Max concurrent job instances
    coalesce: bool = False                          # Merge pending executions if True
    next_run_time: Optional[datetime] = None        # Next scheduled execution time
    exception: Optional[BaseException] = None       # Exception from last execution
    traceback: Optional[str] = None                 # Traceback string if exception occurred
    retval: Optional[Any] = None                    # Return value from last execution
    purpose: Optional[str] = None                   # Description of job's purpose
    start_date: Optional[datetime] = None           # Earliest run time
    end_date: Optional[datetime] = None             # Latest run time
    details: Optional[str] = None                   # Additional job details or metadata