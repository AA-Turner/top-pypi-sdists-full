from abc import ABC, abstractmethod
from datetime import datetime
from typing import List, Optional, Union
from orionis.console.contracts.event import IEvent
from orionis.console.contracts.schedule_event_listener import IScheduleEventListener
from orionis.console.enums.listener import ListeningEvent

class ISchedule(ABC):

    @abstractmethod
    def command(
        self,
        signature: str,
        args: Optional[List[str]] = None
    ) -> 'IEvent':
        """
        Prepare an Event instance for a given command signature and its arguments.

        This method validates the provided command signature and arguments, ensuring
        that the command exists among the registered commands and that the arguments
        are in the correct format. If validation passes, it creates and returns an
        Event object representing the scheduled command, including its signature,
        arguments, and description.

        Parameters
        ----------
        signature : str
            The unique signature identifying the command to be scheduled. Must be a non-empty string.
        args : Optional[List[str]], optional
            A list of string arguments to be passed to the command. Defaults to None.

        Returns
        -------
        Event
            An Event instance containing the command signature, arguments, and its description.

        Raises
        ------
        ValueError
            If the command signature is not a non-empty string, if the arguments are not a list
            of strings or None, or if the command does not exist among the registered commands.
        """
        pass

    @abstractmethod
    def setListener(
        self,
        event: Union[str, ListeningEvent],
        listener: Union[IScheduleEventListener, callable]
    ) -> None:
        """
        Register a listener callback for a specific scheduler event.

        This method registers a listener function or an instance of IScheduleEventListener
        to be invoked when the specified scheduler event occurs. The event can be a global
        event name (e.g., 'scheduler_started') or a specific job ID. The listener must be
        callable and should accept the event object as a parameter.

        Parameters
        ----------
        event : str
            The name of the event to listen for. This can be a global event name (e.g., 'scheduler_started')
            or a specific job ID.
        listener : IScheduleEventListener or callable
            A callable function or an instance of IScheduleEventListener that will be invoked
            when the specified event occurs. The listener should accept one parameter, which
            will be the event object.

        Returns
        -------
        None
            This method does not return any value. It registers the listener for the specified event.

        Raises
        ------
        ValueError
            If the event name is not a non-empty string or if the listener is not callable
            or an instance of IScheduleEventListener.
        """
        pass

    @abstractmethod
    def pause(
        self,
        at: datetime
    ) -> None:
        """
        Schedule the scheduler to pause all operations at a specific datetime.

        This method allows you to schedule a job that will pause the AsyncIOScheduler
        at the specified datetime. The job is added to the scheduler with a 'date'
        trigger, ensuring it executes exactly at the given time.

        Parameters
        ----------
        at : datetime
            The datetime at which the scheduler should be paused. Must be a valid
            datetime object.

        Returns
        -------
        None
            This method does not return any value. It schedules a job to pause the
            scheduler at the specified datetime.

        Raises
        ------
        ValueError
            If the 'at' parameter is not a valid datetime object.
        """
        pass

    @abstractmethod
    def resume(
        self,
        at: datetime
    ) -> None:
        """
        Schedule the scheduler to resume all operations at a specific datetime.

        This method allows you to schedule a job that will resume the AsyncIOScheduler
        at the specified datetime. The job is added to the scheduler with a 'date'
        trigger, ensuring it executes exactly at the given time.

        Parameters
        ----------
        at : datetime
            The datetime at which the scheduler should be resumed. Must be a valid
            datetime object.

        Returns
        -------
        None
            This method does not return any value. It schedules a job to resume the
            scheduler at the specified datetime.

        Raises
        ------
        ValueError
            If the 'at' parameter is not a valid datetime object.
        """
        pass

    @abstractmethod
    async def start(self) -> None:
        """
        Start the AsyncIO scheduler instance and keep it running.

        This method initiates the AsyncIOScheduler which integrates with asyncio event loops
        for asynchronous job execution. It ensures the scheduler starts properly within
        an asyncio context and maintains the event loop active to process scheduled jobs.

        Returns
        -------
        None
            This method does not return any value. It starts the AsyncIO scheduler and keeps it running.
        """
        pass

    @abstractmethod
    async def shutdown(self, wait=True) -> None:
        """
        Shut down the AsyncIO scheduler instance asynchronously.

        This method gracefully stops the AsyncIOScheduler that manages asynchronous job execution.
        It ensures proper cleanup in asyncio environments and allows for an optional wait period
        to complete currently executing jobs before shutting down.

        Parameters
        ----------
        wait : bool, optional
            If True, the method waits until all currently executing jobs are completed before shutting down the scheduler.
            If False, the scheduler shuts down immediately without waiting for running jobs to finish. Default is True.

        Returns
        -------
        None
            This method does not return any value. It performs the shutdown operation for the AsyncIO scheduler.

        Raises
        ------
        ValueError
            If the 'wait' parameter is not a boolean value.
        CLIOrionisRuntimeError
            If an error occurs during the shutdown process.
        """
        pass

    @abstractmethod
    def pauseTask(self, signature: str) -> bool:
        """
        Pause a scheduled job in the AsyncIO scheduler.

        This method pauses a job in the AsyncIOScheduler identified by its unique signature.
        It validates the provided signature to ensure it is a non-empty string and attempts
        to pause the job. If the operation is successful, it logs the action and returns True.
        If the job cannot be paused (e.g., it does not exist), the method returns False.

        Parameters
        ----------
        signature : str
            The unique signature (ID) of the job to pause. This must be a non-empty string.

        Returns
        -------
        bool
            True if the job was successfully paused.
            False if the job does not exist or an error occurred.

        Raises
        ------
        CLIOrionisValueError
            If the `signature` parameter is not a non-empty string.
        """
        pass

    @abstractmethod
    def resumeTask(self, signature: str) -> bool:
        """
        Resume a paused job in the AsyncIO scheduler.

        This method attempts to resume a job that was previously paused in the AsyncIOScheduler.
        It validates the provided job signature, ensures it is a non-empty string, and then
        resumes the job if it exists and is currently paused. If the operation is successful,
        it logs the action and returns True. If the job cannot be resumed (e.g., it does not exist),
        the method returns False.

        Parameters
        ----------
        signature : str
            The unique signature (ID) of the job to resume. This must be a non-empty string.

        Returns
        -------
        bool
            True if the job was successfully resumed, False if the job does not exist or an error occurred.

        Raises
        ------
        CLIOrionisValueError
            If the `signature` parameter is not a non-empty string.
        """
        pass

    @abstractmethod
    def removeTask(self, signature: str) -> bool:
        """
        Remove a scheduled job from the AsyncIO scheduler.

        This method removes a job from the AsyncIOScheduler using its unique signature (ID).
        It validates the provided signature to ensure it is a non-empty string, attempts to
        remove the job from the scheduler, and updates the internal jobs list accordingly.
        If the operation is successful, it logs the action and returns True. If the job
        cannot be removed (e.g., it does not exist), the method returns False.

        Parameters
        ----------
        signature : str
            The unique signature (ID) of the job to remove. This must be a non-empty string.

        Returns
        -------
        bool
            True if the job was successfully removed from the scheduler.
            False if the job does not exist or an error occurred.

        Raises
        ------
        CLIOrionisValueError
            If the `signature` parameter is not a non-empty string.
        """
        pass

    @abstractmethod
    def events(self) -> list:
        """
        Retrieve all scheduled jobs currently managed by the Scheduler.

        This method loads and returns a list of dictionaries, each representing a scheduled job
        managed by this Scheduler instance. Each dictionary contains details such as the command
        signature, arguments, purpose, random delay, start and end dates, and additional job details.

        Returns
        -------
        list of dict
            A list where each element is a dictionary containing information about a scheduled job.
            Each dictionary includes the following keys:
                - 'signature': str, the command signature.
                - 'args': list, the arguments passed to the command.
                - 'purpose': str, the description or purpose of the job.
                - 'random_delay': any, the random delay associated with the job (if any).
                - 'start_date': str or None, the formatted start date and time of the job, or None if not set.
                - 'end_date': str or None, the formatted end date and time of the job, or None if not set.
                - 'details': any, additional details about the job.
        """
        pass

    @abstractmethod
    def isRunning(self) -> bool:
        """
        Determine if the scheduler is currently active and running.

        This method checks the internal state of the AsyncIOScheduler instance to determine
        whether it is currently running. The scheduler is considered running if it has been
        started and has not been paused or shut down.

        Returns
        -------
        bool
            True if the scheduler is running, False otherwise.
        """
        pass

    @abstractmethod
    def isPaused(self) -> bool:
        """
        Check if the scheduler is currently paused.

        This method determines whether the scheduler is in a paused state by checking if there are
        any jobs that were paused using the `pause` method. If there are jobs in the internal set
        `__pausedByPauseEverything`, it indicates that the scheduler has been paused.

        Returns
        -------
        bool
            True if the scheduler is currently paused (i.e., there are jobs in the paused set);
            False otherwise.
        """
        pass

    @abstractmethod
    def forceStop(self) -> None:
        """
        Forcefully stop the scheduler immediately without waiting for jobs to complete.

        This method shuts down the AsyncIOScheduler instance without waiting for currently
        running jobs to finish. It is intended for emergency situations where an immediate
        stop is required. The method also signals the internal stop event to ensure that
        the scheduler's main loop is interrupted and the application can proceed with
        shutdown procedures.

        Returns
        -------
        None
            This method does not return any value. It forcefully stops the scheduler and
            signals the stop event.
        """
        pass

    @abstractmethod
    def stop(self) -> None:
        """
        Stop the scheduler synchronously by setting the stop event.

        This method signals the scheduler to stop by setting the internal stop event.
        It can be called from non-async contexts to initiate a shutdown. If the asyncio
        event loop is running, the stop event is set in a thread-safe manner. Otherwise,
        the stop event is set directly.

        Returns
        -------
        None
            This method does not return any value. It signals the scheduler to stop.
        """
        pass