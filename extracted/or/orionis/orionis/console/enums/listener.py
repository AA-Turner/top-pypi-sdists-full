from enum import Enum

class ListeningEvent(Enum):
    """
    Enumeration of events related to a scheduler and its jobs.

    This class defines various events that can occur during the lifecycle of a scheduler
    and its associated jobs. These events can be used to monitor and respond to changes
    in the scheduler's state or the execution of jobs.

    Attributes
    ----------
    SCHEDULER_STARTED : str
        Event triggered when the scheduler starts.
    SCHEDULER_SHUTDOWN : str
        Event triggered when the scheduler shuts down.
    SCHEDULER_PAUSED : str
        Event triggered when the scheduler is paused.
    SCHEDULER_RESUMED : str
        Event triggered when the scheduler is resumed.
    SCHEDULER_ERROR : str
        Event triggered when the scheduler encounters an error.
    JOB_BEFORE : str
        Event triggered before a job is executed.
    JOB_AFTER : str
        Event triggered after a job is executed.
    JOB_ON_SUCCESS : str
        Event triggered when a job completes successfully.
    JOB_ON_FAILURE : str
        Event triggered when a job fails.
    JOB_ON_MISSED : str
        Event triggered when a job is missed.
    JOB_ON_MAXINSTANCES : str
        Event triggered when a job exceeds its maximum allowed instances.
    JOB_ON_PAUSED : str
        Event triggered when a job is paused.
    JOB_ON_RESUMED : str
        Event triggered when a paused job is resumed.
    JOB_ON_REMOVED : str
        Event triggered when a job is removed.

    Returns
    -------
    str
        The string representation of the event name.
    """

    # Scheduler-related events
    SCHEDULER_STARTED = "schedulerStarted"                  # Triggered when the scheduler starts
    SCHEDULER_SHUTDOWN = "schedulerShutdown"                # Triggered when the scheduler shuts down
    SCHEDULER_PAUSED = "schedulerPaused"                    # Triggered when the scheduler is paused
    SCHEDULER_RESUMED = "schedulerResumed"                  # Triggered when the scheduler is resumed
    SCHEDULER_ERROR = "schedulerError"                      # Triggered when the scheduler encounters an error

    # Job-related events
    JOB_BEFORE = "before"                                   # Triggered before a job is executed
    JOB_AFTER = "after"                                     # Triggered after a job is executed
    JOB_ON_FAILURE = "onFailure"                            # Triggered when a job fails
    JOB_ON_MISSED = "onMissed"                              # Triggered when a job is missed
    JOB_ON_MAXINSTANCES = "onMaxInstances"                  # Triggered when a job exceeds its max instances
    JOB_ON_PAUSED = "onPaused"                              # Triggered when a job is paused
    JOB_ON_RESUMED = "onResumed"                            # Triggered when a paused job is resumed
    JOB_ON_REMOVED = "onRemoved"                            # Triggered when a job is removed