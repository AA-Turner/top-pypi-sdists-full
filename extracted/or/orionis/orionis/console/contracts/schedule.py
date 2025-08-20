from abc import ABC, abstractmethod
from typing import List, Optional
from orionis.console.tasks.event import Event

class ISchedule(ABC):

    @abstractmethod
    def command(
        self,
        signature: str,
        args: Optional[List[str]] = None
    ) -> 'Event':
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

        This method gracefully stops the AsyncIOScheduler that handles asynchronous job execution.
        Using async ensures proper cleanup in asyncio environments.

        Parameters
        ----------
        wait : bool, optional
            If True, the method will wait until all currently executing jobs are completed before shutting down the scheduler.
            If False, the scheduler will be shut down immediately without waiting for running jobs to finish. Default is True.

        Returns
        -------
        None
            This method does not return any value. It shuts down the AsyncIO scheduler.
        """
        pass

    @abstractmethod
    async def remove(self, signature: str) -> bool:
        """
        Remove a scheduled job from the AsyncIO scheduler asynchronously.

        This method removes a job with the specified signature from both the internal
        jobs dictionary and the AsyncIOScheduler instance. Using async ensures proper
        cleanup in asyncio environments.

        Parameters
        ----------
        signature : str
            The signature of the command/job to remove from the scheduler.

        Returns
        -------
        bool
            Returns True if the job was successfully removed, False if the job was not found.

        Raises
        ------
        ValueError
            If the signature is not a non-empty string.
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