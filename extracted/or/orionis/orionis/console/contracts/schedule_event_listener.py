from abc import ABC, abstractmethod
from orionis.console.entities.job_error import JobError
from orionis.console.entities.job_executed import JobExecuted
from orionis.console.entities.job_max_instances import JobMaxInstances
from orionis.console.entities.job_missed import JobMissed
from orionis.console.entities.job_pause import JobPause
from orionis.console.entities.job_removed import JobRemoved
from orionis.console.entities.job_resume import JobResume
from orionis.console.entities.job_submitted import JobSubmitted

class IScheduleEventListener(ABC):
    """
    Interface for event listeners that handle various stages of event processing.
    """

    @abstractmethod
    async def before(self, event: JobSubmitted, schedule):
        """
        Hook method called before the main event handling logic.

        This method is invoked prior to processing the event, allowing for any
        pre-processing or setup tasks to be performed. It can be overridden to
        implement custom logic that should execute before the event is handled.

        Parameters
        ----------
        event : JobSubmitted
            The event object that is about to be processed. This contains
            information about the job submission.
        schedule : ISchedule
            The schedule object associated with the event. This provides
            context about the scheduling system.

        Returns
        -------
        None
            This method does not return any value.

        Notes
        -----
        Override this method to define actions or checks that should occur
        before the event is processed.
        """

        # This is an abstract method, so it does not contain any implementation.
        # Subclasses must override this method to provide specific behavior.
        pass

    @abstractmethod
    async def after(self, event: JobExecuted, schedule):
        """
        Hook method called after an event is processed.

        This method is invoked once the event processing is complete, allowing
        for any post-processing or cleanup tasks to be performed. It can be
        overridden to implement custom logic that should execute after the
        event is handled.

        Parameters
        ----------
        event : JobExecuted
            The event object that was processed. This contains information
            about the job execution, such as its status and metadata.
        schedule : ISchedule
            The schedule object associated with the event. This provides
            context about the scheduling system and its state.

        Returns
        -------
        None
            This method does not return any value.

        Notes
        -----
        Override this method to define actions or checks that should occur
        after the event is processed, such as logging, resource cleanup, or
        triggering subsequent tasks.
        """

        # This is an abstract method, so it does not contain any implementation.
        # Subclasses must override this method to provide specific behavior.
        pass

    @abstractmethod
    async def onFailure(self, event: JobError, schedule):
        """
        Handle the event when a failure occurs during event processing.

        This method is invoked whenever an error or failure occurs during the
        processing of an event. It allows for custom error handling logic to be
        implemented, such as logging the error, notifying relevant parties, or
        performing cleanup tasks. Subclasses should override this method to
        define specific actions to take in response to failures.

        Parameters
        ----------
        event : JobError
            The event object containing detailed information about the failure,
            including the error message, stack trace, and any relevant metadata.
        schedule : ISchedule
            The schedule object associated with the event, providing context
            about the scheduling system and its state at the time of the failure.

        Returns
        -------
        None
            This method does not return any value. It is intended for handling
            side effects or performing actions in response to the failure.

        Notes
        -----
        Override this method to implement specific error handling logic that
        aligns with the application's requirements.
        """

        # This is an abstract method, so it does not contain any implementation.
        # Subclasses must override this method to provide specific behavior.
        pass

    @abstractmethod
    async def onMissed(self, event: JobMissed, schedule):
        """
        Handle the event triggered when an expected job execution is missed.

        This method is invoked whenever a scheduled job is missed, allowing for
        custom handling logic to be implemented. Subclasses should override this
        method to define specific actions to take in response to missed events,
        such as logging, notifications, or corrective measures.

        Parameters
        ----------
        event : JobMissed
            The event object containing details about the missed job, including
            its metadata and the reason it was missed.
        schedule : ISchedule
            The schedule object associated with the event, providing context
            about the scheduling system and its state at the time of the missed event.

        Returns
        -------
        None
            This method does not return any value. It is intended for handling
            side effects or performing actions in response to the missed event.

        Notes
        -----
        Override this method to implement specific logic that aligns with the
        application's requirements for handling missed job executions.
        """

        # Abstract method: Subclasses must provide an implementation for this.
        pass

    @abstractmethod
    async def onMaxInstances(self, event: JobMaxInstances, schedule):
        """
        Handle the event triggered when a job exceeds the maximum allowed instances.

        This method is invoked whenever a job attempts to run but is blocked
        because it has reached its maximum number of concurrent instances.
        Subclasses should override this method to define specific actions to
        take in response to this event, such as logging, notifications, or
        implementing backoff strategies.

        Parameters
        ----------
        event : JobMaxInstances
            The event object containing details about the job that exceeded
            its maximum instances, including its metadata and the configured limit.
        schedule : ISchedule
            The schedule object associated with the event, providing context
            about the scheduling system and its state at the time of the event.

        Returns
        -------
        None
            This method does not return any value. It is intended for handling
            side effects or performing actions in response to the max instances event.

        Notes
        -----
        Override this method to implement specific logic that aligns with the
        application's requirements for handling jobs that exceed their maximum instances.
        """

        # Abstract method: Subclasses must provide an implementation for this.
        pass

    @abstractmethod
    async def onPaused(self, event: JobPause, schedule):
        """
        Handle the event triggered when the scheduler is paused.

        This method is invoked whenever the scheduler is paused, allowing for
        custom handling logic to be implemented. Subclasses should override this
        method to define specific actions to take in response to the pause event,
        such as logging, notifications, or resource management.

        Parameters
        ----------
        event : JobPause
            The event object containing details about the pause event.
        schedule : ISchedule
            The schedule object associated with the event, providing context
            about the scheduling system and its state at the time of the pause event.

        Returns
        -------
        None
            This method does not return any value. It is intended for handling
            side effects or performing actions in response to the pause event.

        Notes
        -----
        Override this method to implement specific logic that aligns with the
        application's requirements for handling scheduler pause events.
        """

        # Abstract method: Subclasses must provide an implementation for this.
        pass

    @abstractmethod
    async def onResumed(self, event: JobResume, schedule):
        """
        Handle the event triggered when the scheduler is resumed.

        This method is invoked whenever the scheduler is resumed, allowing for
        custom handling logic to be implemented. Subclasses should override this
        method to define specific actions to take in response to the resume event,
        such as logging, notifications, or resource management.

        Parameters
        ----------
        event : JobResume
            The event object containing details about the resume event.
        schedule : ISchedule
            The schedule object associated with the event, providing context
            about the scheduling system and its state at the time of the resume event.

        Returns
        -------
        None
            This method does not return any value. It is intended for handling
            side effects or performing actions in response to the resume event.

        Notes
        -----
        Override this method to implement specific logic that aligns with the
        application's requirements for handling scheduler resume events.
        """

        # Abstract method: Subclasses must provide an implementation for this.
        pass

    @abstractmethod
    async def onRemoved(self, event: JobRemoved, schedule):
        """
        Handle the event triggered when a job is removed from the scheduler.

        This method is invoked whenever a job is removed, allowing for custom
        handling logic to be implemented. Subclasses should override this method
        to define specific actions to take in response to the job removal event,
        such as logging, notifications, or resource cleanup.

        Parameters
        ----------
        event : JobRemoved
            The event object containing details about the removed job.
        schedule : ISchedule
            The schedule object associated with the event, providing context
            about the scheduling system and its state at the time of the job removal.

        Returns
        -------
        None
            This method does not return any value. It is intended for handling
            side effects or performing actions in response to the job removal event.

        Notes
        -----
        Override this method to implement specific logic that aligns with the
        application's requirements for handling job removal events.
        """

        # Abstract method: Subclasses must provide an implementation for this.
        pass