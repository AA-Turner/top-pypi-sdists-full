from orionis.console.contracts.base_scheduler import IBaseScheduler
from orionis.console.contracts.schedule import ISchedule
from orionis.console.entities.scheduler_error import SchedulerError
from orionis.console.entities.scheduler_paused import SchedulerPaused
from orionis.console.entities.scheduler_resumed import SchedulerResumed
from orionis.console.entities.scheduler_shutdown import SchedulerShutdown
from orionis.console.entities.scheduler_started import SchedulerStarted

class BaseScheduler(IBaseScheduler):

    async def tasks(self, schedule: ISchedule):
        """
        Defines and registers scheduled tasks for the application.

        This method is responsible for setting up the tasks that the scheduler will execute.
        It uses the provided `schedule` object to define the properties and behavior of each task.

        Parameters
        ----------
        schedule : ISchedule
            The schedule object used to define and register scheduled commands.

        Returns
        -------
        None
            This method does not return any value. It is used solely for task registration.

        Notes
        -----
        Subclasses must override this method to implement their specific task scheduling logic.
        The method should define the tasks, their execution intervals, and any additional
        properties or constraints required for the tasks.
        """
        pass

    async def onStarted(self, event: SchedulerStarted, schedule: ISchedule):
        """
        Handles the event triggered when the scheduler has started successfully.

        This method is invoked when the scheduler begins its operation. It processes
        the `SchedulerStarted` event and performs any necessary initialization or logging
        tasks associated with the start of the scheduler.

        Parameters
        ----------
        event : SchedulerStarted
            The event object containing details about the scheduler start event.
        schedule : ISchedule
            The schedule instance associated with the started scheduler.

        Returns
        -------
        None
            This method does not return any value. It is used for handling the
            scheduler start event and performing related actions.

        Notes
        -----
        This method calls the parent class's `onStarted` method to ensure that
        any base functionality is executed.
        """
        pass

    async def onPaused(self, event: SchedulerPaused, schedule: ISchedule):
        """
        Handles the event triggered when the scheduler is paused.

        This method is invoked when the scheduler pauses its operation. It processes
        the `SchedulerPaused` event and performs any necessary actions or logging
        tasks associated with the pause of the scheduler.

        Parameters
        ----------
        event : SchedulerPaused
            The event object containing details about the scheduler pause event.
        schedule : ISchedule
            The schedule instance associated with the paused scheduler.

        Returns
        -------
        None
            This method does not return any value. It is used for handling the
            scheduler pause event and performing related actions.

        Notes
        -----
        This method calls the parent class's `onPaused` method to ensure that
        any base functionality is executed.
        """
        pass

    async def onResumed(self, event: SchedulerResumed, schedule: ISchedule):
        """
        Handles the event triggered when the scheduler is resumed.

        This method is invoked when the scheduler resumes its operation after being paused.
        It processes the `SchedulerResumed` event and performs any necessary actions or logging
        tasks associated with the resumption of the scheduler.

        Parameters
        ----------
        event : SchedulerResumed
            The event object containing details about the scheduler resumption, such as the
            timestamp of the resumption and any relevant metadata.
        schedule : ISchedule
            The schedule instance associated with the resumed scheduler, which can be used
            to interact with or modify the scheduler's tasks.

        Returns
        -------
        None
            This method does not return any value. It is used for handling the scheduler
            resumption event and performing related actions.

        Notes
        -----
        This method calls the parent class's `onResumed` method to ensure that any base
        functionality is executed. This allows the scheduler to maintain its default behavior
        while enabling additional custom actions during the resumption process.
        """
        pass

    async def onFinalized(self, event: SchedulerShutdown, schedule: ISchedule):
        """
        Handles the event triggered when the scheduler has been finalized.

        This method is invoked after the scheduler has completed its shutdown process.
        It processes the `SchedulerShutdown` event and performs any necessary cleanup
        or logging tasks associated with the finalization of the scheduler.

        Parameters
        ----------
        event : SchedulerShutdown
            The event object containing details about the scheduler shutdown, such as
            the timestamp of the shutdown and any relevant metadata.
        schedule : ISchedule
            The schedule instance associated with the finalized scheduler, which can be
            used to interact with or inspect the scheduler's tasks.

        Returns
        -------
        None
            This method does not return any value. It is used for handling the scheduler
            shutdown event and performing related actions.

        Notes
        -----
        This method calls the parent class's `onFinalized` method to ensure that any base
        functionality is executed. This allows the scheduler to maintain its default behavior
        while enabling additional custom actions during the finalization process.
        """
        pass

    async def onError(self, event: SchedulerError, schedule: ISchedule):
        """
        Handles the event triggered when a job encounters an error during execution.

        This method is invoked when a job fails due to an exception. It processes the `SchedulerError`
        event and performs any necessary actions, such as logging the error details or notifying
        relevant systems about the failure.

        Parameters
        ----------
        event : SchedulerError
            The event object containing details about the job error, including the job ID,
            the exception that occurred, and any relevant metadata.
        schedule : ISchedule
            The schedule instance associated with the job, which can be used to interact with
            or modify the scheduler's tasks.

        Returns
        -------
        None
            This method does not return any value. It is used for handling the job error event
            and performing related actions, such as logging or cleanup.

        Notes
        -----
        This method calls the parent class's `onError` method to ensure that any base functionality
        is executed. This allows the scheduler to maintain its default behavior while enabling
        additional custom actions during error handling.
        """
        pass