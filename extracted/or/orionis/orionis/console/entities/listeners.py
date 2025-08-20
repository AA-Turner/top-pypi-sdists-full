from dataclasses import dataclass
from datetime import datetime
from typing import Any

# ==============================================================
# Base Events
# ==============================================================

@dataclass
class SchedulerEventData:
    """
    Base class for scheduler-related events.

    Attributes
    ----------
    code : int
        The numeric event code indicating the event type.
    """
    code: int


@dataclass
class JobEventData(SchedulerEventData):
    """
    Base class for job-related events.

    Attributes
    ----------
    code : int
        The numeric event code indicating the event type.
    job_id : str
        The identifier of the job.
    jobstore : str
        The name of the job store where the job is located.
    """
    job_id: str
    jobstore: str


# ==============================================================
# Scheduler Lifecycle Events
# ==============================================================

@dataclass
class SchedulerStarted(SchedulerEventData):
    """
    Event triggered when the scheduler starts running.
    """


@dataclass
class SchedulerShutdown(SchedulerEventData):
    """
    Event triggered when the scheduler shuts down.
    """


@dataclass
class SchedulerPaused(SchedulerEventData):
    """
    Event triggered when the scheduler is paused.
    """


@dataclass
class SchedulerResumed(SchedulerEventData):
    """
    Event triggered when the scheduler is resumed.
    """


# ==============================================================
# Executor and JobStore Events
# ==============================================================

@dataclass
class ExecutorAdded(SchedulerEventData):
    """
    Event triggered when an executor is added.

    Attributes
    ----------
    alias : str
        The alias of the added executor.
    """
    alias: str


@dataclass
class ExecutorRemoved(SchedulerEventData):
    """
    Event triggered when an executor is removed.

    Attributes
    ----------
    alias : str
        The alias of the removed executor.
    """
    alias: str


@dataclass
class JobstoreAdded(SchedulerEventData):
    """
    Event triggered when a job store is added.

    Attributes
    ----------
    alias : str
        The alias of the added job store.
    """
    alias: str


@dataclass
class JobstoreRemoved(SchedulerEventData):
    """
    Event triggered when a job store is removed.

    Attributes
    ----------
    alias : str
        The alias of the removed job store.
    """
    alias: str


@dataclass
class AllJobsRemoved(SchedulerEventData):
    """
    Event triggered when all jobs are removed from a job store.

    Attributes
    ----------
    jobstore : str
        The alias of the job store from which jobs were removed.
    """
    jobstore: str


# ==============================================================
# Job Management Events
# ==============================================================

@dataclass
class JobAdded(JobEventData):
    """
    Event triggered when a job is added to a job store.
    """


@dataclass
class JobRemoved(JobEventData):
    """
    Event triggered when a job is removed from a job store.
    """


@dataclass
class JobModified(JobEventData):
    """
    Event triggered when a job is modified in a job store.
    """


@dataclass
class JobSubmitted(JobEventData):
    """
    Event triggered when a job is submitted to an executor.

    Attributes
    ----------
    run_time : datetime
        The datetime when the job was scheduled to run.
    """
    run_time: datetime


@dataclass
class JobMaxInstances(JobEventData):
    """
    Event triggered when a job exceeds its maximum allowed instances.

    Attributes
    ----------
    run_time : datetime
        The datetime when the job was scheduled to run.
    """
    run_time: datetime


# ==============================================================
# Job Execution Events
# ==============================================================

@dataclass
class JobExecuted(JobEventData):
    """
    Event triggered when a job finishes successfully.

    Attributes
    ----------
    scheduled_run_time : datetime
        The datetime when the job was scheduled to run.
    retval : Any
        The return value of the job function.
    """
    scheduled_run_time: datetime
    retval: Any


@dataclass
class JobError(JobEventData):
    """
    Event triggered when a job raises an exception during execution.

    Attributes
    ----------
    scheduled_run_time : datetime
        The datetime when the job was scheduled to run.
    exception : Exception
        The exception raised by the job.
    traceback : str
        The traceback of the exception.
    """
    scheduled_run_time: datetime
    exception: Exception
    traceback: str


@dataclass
class JobMissed(JobEventData):
    """
    Event triggered when a job run is missed due to scheduler constraints.

    Attributes
    ----------
    scheduled_run_time : datetime
        The datetime when the job was originally scheduled to run.
    """
    scheduled_run_time: datetime
