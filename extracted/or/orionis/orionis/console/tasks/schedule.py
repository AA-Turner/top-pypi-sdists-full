import asyncio
import logging
from datetime import datetime
from typing import List, Optional
import pytz
from apscheduler.schedulers.asyncio import AsyncIOScheduler as APSAsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from apscheduler.triggers.date import DateTrigger
from apscheduler.triggers.interval import IntervalTrigger
from orionis.app import Orionis
from orionis.console.contracts.reactor import IReactor
from orionis.console.exceptions import CLIOrionisRuntimeError
from orionis.services.log.contracts.log_service import ILogger

class Scheduler():

    def __init__(
        self,
        reactor: IReactor
    ) -> None:
        """
        Initialize a new instance of the Scheduler class.

        This constructor sets up the internal state required for scheduling commands,
        including references to the application instance, AsyncIOScheduler, the
        command reactor, and job tracking structures. It also initializes properties
        for managing the current scheduling context.

        Parameters
        ----------
        reactor : IReactor
            An instance of a class implementing the IReactor interface, used to
            retrieve available commands and execute scheduled jobs.

        Returns
        -------
        None
            This method does not return any value. It initializes the Scheduler instance.
        """

        # Store the application instance for configuration access.
        self.__app = Orionis()

        # Initialize AsyncIOScheduler instance with timezone configuration.
        self.__scheduler: APSAsyncIOScheduler = APSAsyncIOScheduler(
            timezone=pytz.timezone(self.__app.config('app.timezone', 'UTC'))
        )

        # Clear the APScheduler logger to prevent conflicts with other loggers.
        # This is necessary to avoid duplicate log messages or conflicts with other logging configurations.
        logging.getLogger("apscheduler").handlers.clear()
        logging.getLogger("apscheduler").propagate = False

        # Initialize the logger from the application instance.
        self.__logger: ILogger = self.__app.make('x-orionis.services.log.log_service')

        # Store the reactor instance for command management.
        self.__reactor = reactor

        # Retrieve and store all available commands from the reactor.
        self.__available_commands = self.__getCommands()

        # Dictionary to hold all scheduled jobs and their details.
        self.__jobs: dict = {}

        # Properties to track the current scheduling context.
        self.__command: str = None      # The command signature to be scheduled.
        self.__args: List[str] = None   # Arguments for the command.
        self.__purpose: str = None      # Purpose or description of the scheduled job.

        # Log the initialization of the Scheduler.
        self.__logger.info("Scheduler initialized.")

    def __getCommands(
        self
    ) -> dict:
        """
        Retrieve available commands from the reactor and return them as a dictionary.

        This method queries the reactor for all available jobs/commands, extracting their
        signatures and descriptions. The result is a dictionary where each key is the command
        signature and the value is another dictionary containing the command's signature and
        its description.

        Returns
        -------
        dict
            A dictionary mapping command signatures to their details. Each value is a dictionary
            with 'signature' and 'description' keys.
        """

        # Initialize the commands dictionary
        commands = {}

        # Iterate over all jobs provided by the reactor's info method
        for job in self.__reactor.info():

            # Store each job's signature and description in the commands dictionary
            commands[job['signature']] = {
                'signature': job['signature'],
                'description': job.get('description', '')
            }

        # Return the commands dictionary
        return commands

    def __isAvailable(
        self,
        signature: str
    ) -> bool:
        """
        Check if a command with the given signature is available.

        This method iterates through the available commands and determines
        whether the provided signature matches any registered command.

        Parameters
        ----------
        signature : str
            The signature of the command to check for availability.

        Returns
        -------
        bool
            True if the command with the specified signature exists and is available,
            False otherwise.
        """

        # Iterate through all available command signatures
        for command in self.__available_commands.keys():

            # Return True if the signature matches an available command
            if command == signature:
                return True

        # Return False if the signature is not found among available commands
        return False

    def __getDescription(
        self,
        signature: str
    ) -> Optional[str]:
        """
        Retrieve the description of a command given its signature.

        This method looks up the available commands dictionary and returns the description
        associated with the provided command signature. If the signature does not exist,
        it returns None.

        Parameters
        ----------
        signature : str
            The unique signature identifying the command.

        Returns
        -------
        Optional[str]
            The description of the command if found; otherwise, None.
        """

        # Attempt to retrieve the command entry from the available commands dictionary
        command_entry = self.__available_commands.get(signature)

        # Return the description if the command exists, otherwise return None
        return command_entry['description'] if command_entry else None

    def __reset(
        self
    ) -> None:
        """
        Reset the internal state of the Scheduler instance.

        This method clears the current command, arguments, and purpose attributes, 
        effectively resetting the scheduler's configuration to its initial state. 
        This can be useful for preparing the scheduler for a new command or job 
        scheduling without retaining any previous settings.

        Returns
        -------
        None
            This method does not return any value. It modifies the internal state of the Scheduler.
        """

        self.__command = None
        self.__args = None
        self.__purpose = None

    def command(
        self,
        signature: str,
        args: Optional[List[str]] = None
    ) -> 'Scheduler':
        """
        Register a command to be scheduled with the specified signature and optional arguments.

        This method validates the provided command signature and arguments, checks if the command
        is available in the list of registered commands, and stores the command details internally
        for scheduling. The command's description is also retrieved and stored for reference.

        Parameters
        ----------
        signature : str
            The unique signature identifying the command to be scheduled. Must be a non-empty string.
        args : Optional[List[str]], optional
            A list of string arguments to be passed to the command. If not provided, an empty list is used.

        Returns
        -------
        Scheduler
            Returns the current instance of the Scheduler to allow method chaining.

        Raises
        ------
        ValueError
            If the signature is not a non-empty string, if the arguments are not a list or None,
            or if the command signature is not available among registered commands.
        """

        # Validate that the command signature is a non-empty string
        if not isinstance(signature, str) or not signature.strip():
            raise ValueError("Command signature must be a non-empty string.")

        # Ensure that arguments are either a list of strings or None
        if args is not None and not isinstance(args, list):
            raise ValueError("Arguments must be a list of strings or None.")

        # Check if the command is available in the registered commands
        if not self.__isAvailable(signature):
            raise ValueError(f"The command '{signature}' is not available or does not exist.")

        # Store the command signature
        self.__command = signature

        # If purpose is not already set, retrieve and set the command's description
        if self.__purpose is None:
            self.__purpose = self.__getDescription(signature)

        # Store the provided arguments or default to an empty list
        self.__args = args if args is not None else []

        # Return self to support method chaining
        return self

    def purpose(
        self,
        purpose: str
    ) -> 'Scheduler':
        """
        Set the purpose or description for the scheduled command.

        This method assigns a human-readable purpose or description to the command
        that is being scheduled. The purpose must be a non-empty string. This can
        be useful for documentation, logging, or displaying information about the
        scheduled job.

        Parameters
        ----------
        purpose : str
            The purpose or description to associate with the scheduled command.
            Must be a non-empty string.

        Returns
        -------
        Scheduler
            Returns the current instance of the Scheduler to allow method chaining.

        Raises
        ------
        ValueError
            If the provided purpose is not a non-empty string.
        """

        # Validate that the purpose is a non-empty string
        if not isinstance(purpose, str) or not purpose.strip():
            raise ValueError("The purpose must be a non-empty string.")

        # Set the internal purpose attribute
        self.__purpose = purpose

        # Return self to support method chaining
        return self

    def onceAt(
        self,
        date: datetime
    ) -> bool:
        """
        Schedule a command to run once at a specific date and time.

        This method schedules the currently registered command to execute exactly once at the
        specified datetime using the AsyncIOScheduler. The job is registered internally and 
        added to the scheduler instance.

        Parameters
        ----------
        date : datetime.datetime
            The date and time at which the command should be executed. Must be a valid `datetime` instance.

        Returns
        -------
        bool
            Returns True if the job was successfully scheduled.

        Raises
        ------
        CLIOrionisRuntimeError
            If the provided date is not a `datetime` instance or if there is an error while scheduling the job.
        """

        try:

            # Ensure the provided date is a valid datetime instance.
            if not isinstance(date, datetime):
                raise CLIOrionisRuntimeError(
                    "The date must be an instance of datetime."
                )

            # Register the job details internally.
            self.__jobs[self.__command] = {
                'signature': self.__command,
                'args': self.__args,
                'purpose': self.__purpose,
                'trigger': 'once_at',
                'start_at': date.strftime('%Y-%m-%d %H:%M:%S'),
                'end_at': date.strftime('%Y-%m-%d %H:%M:%S')
            }

            # Add the job to the scheduler.
            self.__scheduler.add_job(
                func= lambda command=self.__command, args=list(self.__args): self.__reactor.call(
                    command,
                    args
                ),
                trigger=DateTrigger(
                    run_date=date
                ),
                id=self.__command,
                name=self.__command,
                replace_existing=True
            )

            # Log the scheduling of the command.
            self.__logger.info(
                f"Scheduled command '{self.__command}' to run once at {date.strftime('%Y-%m-%d %H:%M:%S')}"
            )

            # Reset the internal state for future scheduling.
            self.__reset()

            # Return True to indicate successful scheduling.
            return True

        except Exception as e:

            # Reraise known CLIOrionisRuntimeError exceptions.
            if isinstance(e, CLIOrionisRuntimeError):
                raise e

            # Wrap and raise any other exceptions as CLIOrionisRuntimeError.
            raise CLIOrionisRuntimeError(f"Error scheduling the job: {str(e)}")

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

        # Start the AsyncIOScheduler to handle asynchronous jobs.
        try:

            # Ensure we're in an asyncio context
            asyncio.get_running_loop()

            # Start the scheduler
            if not self.__scheduler.running:
                self.__logger.info(f"Orionis Scheduler started. {len(self.__jobs)} jobs scheduled.")
                self.__scheduler.start()

            # Keep the event loop alive to process scheduled jobs
            try:

                # Wait for the scheduler to start and keep it running
                while True:
                    await asyncio.sleep(1)

            except KeyboardInterrupt:

                # Handle graceful shutdown on keyboard interrupt
                await self.shutdown()

        except Exception as e:

            # Handle exceptions that may occur during scheduler startup
            raise CLIOrionisRuntimeError(f"Failed to start the scheduler: {str(e)}")

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

        # Validate that the wait parameter is a boolean.
        if not isinstance(wait, bool):
            raise ValueError("The 'wait' parameter must be a boolean value.")

        try:

            # Shut down the AsyncIOScheduler, waiting for jobs if specified.
            if self.__scheduler.running:

                # For AsyncIOScheduler, shutdown can be called normally
                # but we await any pending operations
                self.__scheduler.shutdown(wait=wait)

                # Give a small delay to ensure proper cleanup
                if wait:
                    await asyncio.sleep(0.1)

            # Log the shutdown of the scheduler
            self.__logger.info("Orionis Scheduler has been shut down.")

        except Exception:

            # AsyncIOScheduler may not be running or may have issues in shutdown
            pass

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

        # Validate that the signature is a non-empty string
        if not isinstance(signature, str) or not signature.strip():
            raise ValueError("Signature must be a non-empty string.")

        try:

            # Remove from the scheduler
            self.__scheduler.remove_job(signature)

            # Remove from internal jobs dictionary
            if signature in self.__jobs:
                del self.__jobs[signature]

            # Give a small delay to ensure proper cleanup
            await asyncio.sleep(0.01)

            # Log the removal of the job
            self.__logger.info(f"Job '{signature}' has been removed from the scheduler.")

            # Return True to indicate successful removal
            return True

        except Exception:

            # Job not found or other error
            return False

    def jobs(self) -> dict:
        """
        Retrieve all scheduled jobs currently managed by the Scheduler.

        This method returns a dictionary containing information about all jobs that have been
        registered and scheduled through this Scheduler instance. Each entry in the dictionary
        represents a scheduled job, where the key is the command signature and the value is a
        dictionary with details such as the signature, arguments, purpose, type, trigger, start time,
        and end time.

        Returns
        -------
        dict
            A dictionary mapping command signatures to their corresponding job details. Each value
            is a dictionary containing information about the scheduled job.
        """

        # Return the internal dictionary holding all scheduled jobs and their details.
        return self.__jobs