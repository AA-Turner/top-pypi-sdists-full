from datetime import datetime
from orionis.console.base.contracts.scheduler import IBaseScheduler
from orionis.console.contracts.schedule import ISchedule

class BaseScheduler(IBaseScheduler):

    # Pause Global Scheduler at a specific time
    PAUSE_AT: datetime = None

    # Resume Global Scheduler at a specific time
    RESUME_AT: datetime = None

    # Finalize Global Scheduler at a specific time
    FINALIZE_AT: datetime = None

    def tasks(self, schedule: ISchedule):
        """
        Defines and registers scheduled tasks for the application.

        Parameters
        ----------
        schedule : ISchedule
            The schedule object used to define and register scheduled commands.

        Returns
        -------
        None
            This method does not return any value. It is intended to be overridden
            by subclasses to specify scheduled tasks.
        """
        # Placeholder for task registration logic
        pass

    def onStarted(self):
        """
        Called when the scheduler is started.

        Returns
        -------
        None
            This method does not return any value.

        Notes
        -----
        Intended to be overridden by subclasses to implement custom behavior that should
        occur when the scheduler starts running.
        """
        # Placeholder for logic to execute when the scheduler starts
        pass

    def onPaused(self):
        """
        Called when the scheduler is paused.

        Returns
        -------
        None
            This method does not return any value.

        Notes
        -----
        Should be overridden to define custom behavior that occurs when the scheduler
        enters a paused state.
        """
        # Placeholder for logic to execute when the scheduler is paused
        pass

    def onResumed(self):
        """
        Called when the scheduler is resumed from a paused state.

        Returns
        -------
        None
            This method does not return any value.

        Notes
        -----
        Should be overridden to implement any actions that need to occur when the
        scheduler resumes operation.
        """
        # Placeholder for logic to execute when the scheduler is resumed
        pass

    def onFinalized(self):
        """
        Called when the scheduler has completed its execution and is being finalized.

        Returns
        -------
        None
            This method does not return any value.

        Notes
        -----
        Can be overridden to perform any necessary cleanup or finalization tasks.
        """
        # Placeholder for logic to execute when the scheduler is finalized
        pass

    def onError(self, error: Exception):
        """
        Handles errors that occur within the scheduler.

        Parameters
        ----------
        error : Exception
            The exception instance representing the error that occurred.

        Returns
        -------
        None
            This method does not return any value.

        Notes
        -----
        Can be overridden to implement custom error handling logic for the scheduler.
        """
        # Placeholder for logic to handle errors in the scheduler
        pass