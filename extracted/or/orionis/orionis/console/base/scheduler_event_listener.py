from orionis.console.contracts.schedule_event_listener import IScheduleEventListener
from orionis.console.entities.job_error import JobError
from orionis.console.entities.job_executed import JobExecuted
from orionis.console.entities.job_max_instances import JobMaxInstances
from orionis.console.entities.job_missed import JobMissed
from orionis.console.entities.job_pause import JobPause
from orionis.console.entities.job_removed import JobRemoved
from orionis.console.entities.job_resume import JobResume
from orionis.console.entities.job_submitted import JobSubmitted

class BaseScheduleEventListener(IScheduleEventListener):
    """
    Base implementation of the IScheduleEventListener interface.

    This class provides method definitions for handling various job events in a
    scheduling system. Subclasses should override these methods to implement
    specific behavior for each event type.
    """

    async def before(self, event: JobSubmitted, schedule):
        """
        Called before processing a job submission event.

        Parameters
        ----------
        event : JobSubmitted
            The job submission event.
        schedule : ISchedule
            The associated schedule.
        """
        pass

    async def after(self, event: JobExecuted, schedule):
        """
        Called after processing a job execution event.

        Parameters
        ----------
        event : JobExecuted
            The job execution event.
        schedule : ISchedule
            The associated schedule.
        """
        pass

    async def onSuccess(self, event: JobExecuted, schedule):
        """
        Called when a job is successfully executed.

        Parameters
        ----------
        event : JobExecuted
            The successful job execution event.
        schedule : ISchedule
            The associated schedule.
        """
        pass

    async def onFailure(self, event: JobError, schedule):
        """
        Called when a job execution fails.

        Parameters
        ----------
        event : JobError
            The job error event.
        schedule : ISchedule
            The associated schedule.
        """
        pass

    async def onMissed(self, event: JobMissed, schedule):
        """
        Called when a job execution is missed.

        Parameters
        ----------
        event : JobMissed
            The missed job event.
        schedule : ISchedule
            The associated schedule.
        """
        pass

    async def onMaxInstances(self, event: JobMaxInstances, schedule):
        """
        Called when a job exceeds the maximum allowed instances.

        Parameters
        ----------
        event : JobMaxInstances
            The max instances event.
        schedule : ISchedule
            The associated schedule.
        """
        pass

    async def onPaused(self, event: JobPause, schedule):
        """
        Called when the scheduler is paused.

        Parameters
        ----------
        event : JobPause
            The pause event.
        schedule : ISchedule
            The associated schedule.
        """
        pass

    async def onResumed(self, event: JobResume, schedule):
        """
        Called when the scheduler is resumed.

        Parameters
        ----------
        event : JobResume
            The resume event.
        schedule : ISchedule
            The associated schedule.
        """
        pass

    async def onRemoved(self, event: JobRemoved, schedule):
        """
        Called when a job is removed from the scheduler.

        Parameters
        ----------
        event : JobRemoved
            The job removal event.
        schedule : ISchedule
            The associated schedule.
        """
        pass
