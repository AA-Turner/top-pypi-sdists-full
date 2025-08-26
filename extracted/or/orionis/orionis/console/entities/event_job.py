from dataclasses import dataclass
from datetime import datetime
from typing import Any, Callable, Dict, Optional, Tuple

@dataclass(kw_only=True)
class EventJob:
    """
    Represents the main properties of a job in APScheduler.

    Attributes
    ----------
    id : str
        Unique identifier for the job.
    name : Optional[str]
        Human-readable name for the job. Can be None if not specified.
    func : Callable[..., Any]
        The function or coroutine to be executed by the job.
    args : Tuple[Any, ...]
        Positional arguments to be passed to the function.
    trigger : Any
        The trigger that determines the job's execution schedule
        (e.g., IntervalTrigger, CronTrigger, etc.).
    executor : str
        Alias of the executor that will run the job.
    jobstore : str
        Alias of the job store where the job is stored.
    misfire_grace_time : Optional[int]
        Grace period in seconds for handling missed executions.
        If None, no grace period is applied.
    max_instances : int
        Maximum number of concurrent instances of the job allowed.
    coalesce : bool
        Whether to merge pending executions into a single execution.
    next_run_time : Optional[datetime]
        The next scheduled execution time of the job. Can be None if the job is paused or unscheduled.

    Returns
    -------
    None
        This class is a data container and does not return any value.
    """
    id: str
    code: int = 0
    name: Optional[str] = None
    func: Callable[..., Any] = None
    args: Tuple[Any, ...] = ()
    trigger: Any = None
    executor: str = 'default'
    jobstore: str = 'default'
    misfire_grace_time: Optional[int] = None
    max_instances: int = 1
    coalesce: bool = False
    next_run_time: Optional[datetime] = None
    exception: Optional[BaseException] = None
    traceback: Optional[str] = None
    retval: Optional[Any] = None
    purpose: Optional[str] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    details: Optional[str] = None