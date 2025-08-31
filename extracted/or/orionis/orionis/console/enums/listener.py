from enum import Enum

class ListeningEvent(Enum):
    """
    Enumeration of scheduler and job-related events.

    This enumeration defines the various events that can occur during the lifecycle of a scheduler
    and its associated jobs. These events are intended to be used for monitoring, logging, or
    triggering actions in response to changes in the scheduler's state or job execution.

    Attributes
    ----------
    SCHEDULER_STARTED : str
        Triggered when the scheduler starts.
    SCHEDULER_SHUTDOWN : str
        Triggered when the scheduler shuts down.
    SCHEDULER_PAUSED : str
        Triggered when the scheduler is paused.
    SCHEDULER_RESUMED : str
        Triggered when the scheduler is resumed.
    SCHEDULER_ERROR : str
        Triggered when the scheduler encounters an error.
    JOB_BEFORE : str
        Triggered before a job is executed.
    JOB_AFTER : str
        Triggered after a job is executed.
    JOB_ON_FAILURE : str
        Triggered when a job fails.
    JOB_ON_MISSED : str
        Triggered when a job is missed.
    JOB_ON_MAXINSTANCES : str
        Triggered when a job exceeds its maximum allowed instances.
    JOB_ON_PAUSED : str
        Triggered when a job is paused.
    JOB_ON_RESUMED : str
        Triggered when a paused job is resumed.
    JOB_ON_REMOVED : str
        Triggered when a job is removed.

    Returns
    -------
    str
        The string value representing the event name.
    """

    # Scheduler-related events
    SCHEDULER_STARTED = "schedulerStarted"      # Triggered when the scheduler starts
    SCHEDULER_SHUTDOWN = "schedulerShutdown"    # Triggered when the scheduler shuts down
    SCHEDULER_PAUSED = "schedulerPaused"        # Triggered when the scheduler is paused
    SCHEDULER_RESUMED = "schedulerResumed"      # Triggered when the scheduler is resumed
    SCHEDULER_ERROR = "schedulerError"          # Triggered when the scheduler encounters an error

    # Job-related events
    JOB_BEFORE = "before"                       # Triggered before a job is executed
    JOB_AFTER = "after"                         # Triggered after a job is executed
    JOB_ON_FAILURE = "onFailure"                # Triggered when a job fails
    JOB_ON_MISSED = "onMissed"                  # Triggered when a job is missed
    JOB_ON_MAXINSTANCES = "onMaxInstances"      # Triggered when a job exceeds its max instances
    JOB_ON_PAUSED = "onPaused"                  # Triggered when a job is paused
    JOB_ON_RESUMED = "onResumed"                # Triggered when a paused job is resumed
    JOB_ON_REMOVED = "onRemoved"                # Triggered when a job is removed
