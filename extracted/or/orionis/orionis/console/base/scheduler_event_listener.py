from orionis.console.contracts.schedule_event_listener import IScheduleEventListener
from orionis.console.entities.event_job import EventJob

class BaseScheduleEventListener(IScheduleEventListener):
    """
    Base implementation of the IScheduleEventListener interface.

    This class provides method definitions for handling various job events in a
    scheduling system. Subclasses should override these methods to implement
    specific behavior for each event type.
    """

    async def before(self, event: EventJob, schedule):
        """
        Called before processing a job submission event.

        Parameters
        ----------
        event : EventJob
            The job submission event containing details about the job.
        schedule : ISchedule
            The associated schedule instance managing the job.

        Returns
        -------
        None
        """
        pass  # Placeholder for pre-job submission logic

    async def after(self, event: EventJob, schedule):
        """
        Called after processing a job execution event.

        Parameters
        ----------
        event : EventJob
            The job execution event containing details about the job.
        schedule : ISchedule
            The associated schedule instance managing the job.

        Returns
        -------
        None
        """
        pass  # Placeholder for post-job execution logic

    async def onFailure(self, event: EventJob, schedule):
        """
        Called when a job execution fails.

        Parameters
        ----------
        event : EventJob
            The job error event containing details about the failure.
        schedule : ISchedule
            The associated schedule instance managing the job.

        Returns
        -------
        None
        """
        pass  # Placeholder for logic to handle job execution failure

    async def onMissed(self, event: EventJob, schedule):
        """
        Called when a job execution is missed.

        Parameters
        ----------
        event : EventJob
            The missed job event containing details about the missed execution.
        schedule : ISchedule
            The associated schedule instance managing the job.

        Returns
        -------
        None
        """
        pass  # Placeholder for logic to handle missed job execution

    async def onMaxInstances(self, event: EventJob, schedule):
        """
        Called when a job exceeds the maximum allowed instances.

        Parameters
        ----------
        event : EventJob
            The max instances event containing details about the job.
        schedule : ISchedule
            The associated schedule instance managing the job.

        Returns
        -------
        None
        """
        pass  # Placeholder for logic to handle max instances exceeded

    async def onPaused(self, event: EventJob, schedule):
        """
        Called when the scheduler is paused.

        Parameters
        ----------
        event : EventJob
            The pause event containing details about the scheduler state.
        schedule : ISchedule
            The associated schedule instance managing the jobs.

        Returns
        -------
        None
        """
        pass  # Placeholder for logic to handle scheduler pause

    async def onResumed(self, event: EventJob, schedule):
        """
        Called when the scheduler is resumed.

        Parameters
        ----------
        event : EventJob
            The resume event containing details about the scheduler state.
        schedule : ISchedule
            The associated schedule instance managing the jobs.

        Returns
        -------
        None
        """
        pass  # Placeholder for logic to handle scheduler resume

    async def onRemoved(self, event: EventJob, schedule):
        """
        Called when a job is removed from the scheduler.

        Parameters
        ----------
        event : EventJob
            The job removal event containing details about the removed job.
        schedule : ISchedule
            The associated schedule instance managing the jobs.

        Returns
        -------
        None
        """
        pass  # Placeholder for logic to handle job removal
