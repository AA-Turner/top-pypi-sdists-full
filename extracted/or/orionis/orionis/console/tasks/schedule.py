import asyncio
import logging
from typing import Dict, List, Optional
import pytz
from apscheduler.events import EVENT_JOB_MISSED, EVENT_JOB_ERROR, EVENT_ALL, EVENT_SCHEDULER_STARTED
from apscheduler.schedulers.asyncio import AsyncIOScheduler as APSAsyncIOScheduler
from orionis.console.contracts.reactor import IReactor
from orionis.console.contracts.schedule import ISchedule
from orionis.console.exceptions import CLIOrionisRuntimeError
from orionis.console.output.contracts.console import IConsole
from orionis.console.tasks.event import Event
from orionis.console.tasks.exception_report import ScheduleErrorReporter
from orionis.foundation.contracts.application import IApplication
from orionis.services.log.contracts.log_service import ILogger

class Scheduler(ISchedule):

    def __init__(
        self,
        reactor: IReactor,
        app: IApplication,
        console: IConsole,
        error_reporter: ScheduleErrorReporter
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
        self.__app = app

        # Store the console instance for output operations.
        self.__console = console

        # Store the error reporter instance for handling exceptions.
        self.__error_reporter = error_reporter

        # Initialize AsyncIOScheduler instance with timezone configuration.
        self.__scheduler: APSAsyncIOScheduler = APSAsyncIOScheduler(
            timezone=pytz.timezone(self.__app.config('app.timezone', 'UTC'))
        )

        # Clear the APScheduler logger to prevent conflicts with other loggers.
        # This is necessary to avoid duplicate log messages or conflicts with other logging configurations.
        for name in ["apscheduler", "apscheduler.scheduler", "apscheduler.executors.default"]:
            logger = logging.getLogger(name)
            logger.handlers.clear()
            logger.propagate = False
            logger.disabled = True

        # Initialize the logger from the application instance.
        self.__logger: ILogger = self.__app.make('x-orionis.services.log.log_service')

        # Store the reactor instance for command management.
        self.__reactor = reactor

        # Retrieve and store all available commands from the reactor.
        self.__available_commands = self.__getCommands()

        # Initialize the jobs dictionary to keep track of scheduled jobs.
        self.__events: Dict[str, Event] = {}

        # Initialize the jobs list to keep track of all scheduled jobs.
        self.__jobs: List[dict] = []

        # Add a listener to the scheduler to capture job events such as missed jobs or errors.
        if self.__app.config('app.debug', False):
            self.__scheduler.add_listener(self.__listener, EVENT_ALL)

    def __listener(self, event):
        """
        Handle job events by logging errors and missed jobs.

        This method acts as a listener for job events emitted by the scheduler. It processes
        two main types of events: job execution errors and missed job executions. When a job
        raises an exception during execution, the method logs the error and delegates reporting
        to the error reporter. If a job is missed (i.e., not executed at its scheduled time),
        the method logs a warning and notifies the error reporter accordingly.

        Parameters
        ----------
        event : apscheduler.events.JobEvent
            The job event object containing information about the job execution, such as
            job_id, exception, traceback, code, and scheduled_run_time.

        Returns
        -------
        None
            This method does not return any value. It performs logging and error reporting
            based on the event type.
        """

        # If the event contains an exception, log the error and report it
        if event.exception:
            self.__logger.error(f"Job {event.job_id} raised an exception: {event.exception}")
            self.__error_reporter.reportException(
                job_id=event.job_id,
                exception=event.exception,
                traceback=event.traceback
            )

        # If the event indicates a missed job, log a warning and report it
        elif event.code == EVENT_JOB_MISSED:
            self.__logger.warning(f"Job {event.job_id} was missed, scheduled for {event.scheduled_run_time}")
            self.__error_reporter.reportMissed(
                job_id=event.job_id,
                scheduled_time=event.scheduled_run_time
            )

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

    def __loadEvents(
        self
    ) -> None:
        """
        Load all scheduled events from the AsyncIOScheduler into the internal jobs dictionary.

        This method retrieves all jobs currently managed by the AsyncIOScheduler and populates
        the internal jobs dictionary with their details, including signature, arguments, purpose,
        type, trigger, start date, and end date.

        Returns
        -------
        None
            This method does not return any value. It updates the internal jobs dictionary.
        """

        # Only load events if the jobs list is empty
        if not self.__jobs:

            # Iterate through all scheduled jobs in the AsyncIOScheduler
            for signature, event in self.__events.items():

                # Convert the event to its entity representation
                entity = event.toEntity()

                # Add the job to the internal jobs list
                self.__jobs.append(entity.toDict())

                # Create a unique key for the job based on its signature
                self.__scheduler.add_job(
                    func= lambda command=signature, args=list(entity.args): self.__reactor.call(
                        command,
                        args
                    ),
                    trigger=entity.trigger,
                    id=signature,
                    name=signature,
                    replace_existing=True
                )

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

        # Validate that the command signature is a non-empty string
        if not isinstance(signature, str) or not signature.strip():
            raise ValueError("Command signature must be a non-empty string.")

        # Ensure that arguments are either a list of strings or None
        if args is not None and not isinstance(args, list):
            raise ValueError("Arguments must be a list of strings or None.")

        # Check if the command is available in the registered commands
        if not self.__isAvailable(signature):
            raise ValueError(f"The command '{signature}' is not available or does not exist.")

        # Store the command and its arguments for scheduling
        self.__events[signature] = Event(
            signature=signature,
            args=args or [],
            purpose=self.__getDescription(signature)
        )

        # Return the Event instance for further scheduling configuration
        return self.__events[signature]

    def addListenerOnSchedulerStarted(
        self,
        listener: callable
    ) -> None:
        """
        Add a listener for the scheduler started event.

        This method allows you to register a callback function that will be called
        when the scheduler starts. The callback should accept a single argument, which
        is the event object containing details about the scheduler start event.

        Parameters
        ----------
        listener : callable
            A function that will be called when the scheduler starts.
            It should accept one parameter, which is the event object.
        """
        # Register the listener for the scheduler started event
        self.__scheduler.add_listener(listener, EVENT_SCHEDULER_STARTED)

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

            # Load existing events into the scheduler
            self.events()

            # Ensure we're in an asyncio context
            asyncio.get_running_loop()

            # Start the scheduler
            if not self.__scheduler.running:
                self.__logger.info(f"Orionis Scheduler started. {len(self.__jobs)} jobs scheduled.")
                self.__scheduler.start()

            # Keep the event loop alive to process scheduled jobs
            try:
                while self.__scheduler.running and self.__scheduler.get_jobs():
                    await asyncio.sleep(1)
            except (KeyboardInterrupt, asyncio.CancelledError):
                # Handle graceful shutdown on keyboard interrupt or cancellation
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

        # Ensure all events are loaded into the internal jobs list
        self.__loadEvents()

        # Initialize a list to hold details of each scheduled job
        events: list = []

        # Iterate over each job in the internal jobs list
        for job in self.__jobs:
            # Append a dictionary with relevant job details to the events list
            events.append({
                'signature': job['signature'],
                'args': job['args'],
                'purpose': job['purpose'],
                'random_delay': job['random_delay'],
                'start_date': job['start_date'].strftime('%Y-%m-%d %H:%M:%S') if job['start_date'] else None,
                'end_date': job['end_date'].strftime('%Y-%m-%d %H:%M:%S') if job['end_date'] else None,
                'details': job['details']
            })

        # Return the list of scheduled job details
        return events