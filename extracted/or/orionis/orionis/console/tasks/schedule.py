import asyncio
from datetime import datetime
import logging
from typing import Dict, List, Optional, Union
import pytz
from apscheduler.triggers.date import DateTrigger
from apscheduler.events import (
    EVENT_SCHEDULER_STARTED,
    EVENT_SCHEDULER_PAUSED,
    EVENT_SCHEDULER_RESUMED,
    EVENT_SCHEDULER_SHUTDOWN,
    EVENT_JOB_ERROR,
    EVENT_JOB_SUBMITTED,
    EVENT_JOB_EXECUTED,
    EVENT_JOB_MISSED,
    EVENT_JOB_MAX_INSTANCES,
    EVENT_JOB_MODIFIED,
    EVENT_JOB_REMOVED
)
from apscheduler.schedulers.asyncio import AsyncIOScheduler as APSAsyncIOScheduler
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from orionis.console.contracts.event import IEvent
from orionis.console.contracts.reactor import IReactor
from orionis.console.contracts.schedule import ISchedule
from orionis.console.contracts.schedule_event_listener import IScheduleEventListener
from orionis.console.entities.job_error import JobError
from orionis.console.entities.job_executed import JobExecuted
from orionis.console.entities.job_max_instances import JobMaxInstances
from orionis.console.entities.job_missed import JobMissed
from orionis.console.entities.job_modified import JobModified
from orionis.console.entities.job_removed import JobRemoved
from orionis.console.entities.job_submitted import JobSubmitted
from orionis.console.entities.scheduler_paused import SchedulerPaused
from orionis.console.entities.scheduler_resumed import SchedulerResumed
from orionis.console.entities.scheduler_shutdown import SchedulerShutdown
from orionis.console.entities.scheduler_started import SchedulerStarted
from orionis.console.enums.listener import ListeningEvent
from orionis.console.enums.event import Event as EventEntity
from orionis.console.exceptions import CLIOrionisRuntimeError
from orionis.console.exceptions.cli_orionis_value_error import CLIOrionisValueError
from orionis.console.output.contracts.console import IConsole
from orionis.foundation.contracts.application import IApplication
from orionis.services.log.contracts.log_service import ILogger

class Scheduler(ISchedule):

    def __init__(
        self,
        reactor: IReactor,
        app: IApplication,
        console: IConsole,
        rich_console: Console
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

        # Store the rich console instance for advanced output formatting.
        self.__rich_console = rich_console

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
        self.__events: Dict[str, IEvent] = {}

        # Initialize the jobs list to keep track of all scheduled jobs.
        self.__jobs: List[EventEntity] = []

        # Initialize the listeners dictionary to manage event listeners.
        self.__listeners: Dict[str, callable] = {}

    def __getCurrentTime(
        self
    ) -> str:
        """
        Get the current date and time formatted as a string.

        This method retrieves the current date and time in the timezone configured
        for the application and formats it as a string in the "YYYY-MM-DD HH:MM:SS" format.

        Returns
        -------
        str
            A string representing the current date and time in the configured timezone,
            formatted as "YYYY-MM-DD HH:MM:SS".
        """

        # Get the current time in the configured timezone
        tz = pytz.timezone(self.__app.config("app.timezone", "UTC"))
        now = datetime.now(tz)

        # Format the current time as a string
        return now.strftime("%Y-%m-%d %H:%M:%S")

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

        # Prevent adding new commands while the scheduler is running
        if self.__scheduler.running:
            raise CLIOrionisRuntimeError("Cannot add new commands while the scheduler is running.")

        # Validate that the command signature is a non-empty string
        if not isinstance(signature, str) or not signature.strip():
            raise CLIOrionisValueError("Command signature must be a non-empty string.")

        # Ensure that arguments are either a list of strings or None
        if args is not None and not isinstance(args, list):
            raise CLIOrionisValueError("Arguments must be a list of strings or None.")

        # Check if the command is available in the registered commands
        if not self.__isAvailable(signature):
            raise CLIOrionisValueError(f"The command '{signature}' is not available or does not exist.")

        # Store the command and its arguments for scheduling
        from orionis.console.tasks.event import Event
        self.__events[signature] = Event(
            signature=signature,
            args=args or [],
            purpose=self.__getDescription(signature)
        )

        # Return the Event instance for further scheduling configuration
        return self.__events[signature]

    def __subscribeListeners(
        self
    ) -> None:
        """
        Subscribe to scheduler events for monitoring and handling.

        This method sets up event listeners for the AsyncIOScheduler instance to monitor
        various scheduler events such as scheduler start, shutdown, pause, resume, job submission,
        execution, missed jobs, and errors. Each listener is associated with a specific event type
        and is responsible for handling the corresponding event.

        The listeners log relevant information, invoke registered callbacks, and handle errors
        or missed jobs as needed. This ensures that the scheduler's state and job execution
        are monitored effectively.

        Returns
        -------
        None
            This method does not return any value. It configures event listeners on the scheduler.
        """

        self.__scheduler.add_listener(self.__startedListener, EVENT_SCHEDULER_STARTED)
        self.__scheduler.add_listener(self.__pausedListener, EVENT_SCHEDULER_PAUSED)
        self.__scheduler.add_listener(self.__resumedListener, EVENT_SCHEDULER_RESUMED)
        self.__scheduler.add_listener(self.__shutdownListener, EVENT_SCHEDULER_SHUTDOWN)
        self.__scheduler.add_listener(self.__errorListener, EVENT_JOB_ERROR)
        self.__scheduler.add_listener(self.__submittedListener, EVENT_JOB_SUBMITTED)
        self.__scheduler.add_listener(self.__executedListener, EVENT_JOB_EXECUTED)
        self.__scheduler.add_listener(self.__missedListener, EVENT_JOB_MISSED)
        self.__scheduler.add_listener(self.__maxInstancesListener, EVENT_JOB_MAX_INSTANCES)
        self.__scheduler.add_listener(self.__modifiedListener, EVENT_JOB_MODIFIED)
        self.__scheduler.add_listener(self.__removedListener, EVENT_JOB_REMOVED)

    def __globalCallableListener(
        self,
        event_data: Optional[Union[SchedulerStarted, SchedulerPaused, SchedulerResumed, SchedulerShutdown, JobError]],
        listening_vent: ListeningEvent
    ) -> None:
        """
        Invoke registered listeners for global scheduler events.

        This method handles global scheduler events such as when the scheduler starts, pauses, resumes,
        or shuts down. It checks if a listener is registered for the specified event and invokes it if callable.
        The listener can be either a coroutine or a regular function.

        Parameters
        ----------
        event_data : Optional[Union[SchedulerStarted, SchedulerPaused, SchedulerResumed, SchedulerShutdown, JobError]]
            The event data associated with the global scheduler event. This can include details about the event,
            such as its type and context. If no specific data is available, this parameter can be None.
        listening_vent : ListeningEvent
            An instance of the ListeningEvent enum representing the global scheduler event to handle.

        Returns
        -------
        None
            This method does not return any value. It invokes the registered listener for the specified event,
            if one exists.

        Raises
        ------
        CLIOrionisValueError
            If the provided `listening_vent` is not an instance of ListeningEvent.
        """

        # Validate that the provided event is an instance of ListeningEvent
        if not isinstance(listening_vent, ListeningEvent):
            raise CLIOrionisValueError("The event must be an instance of ListeningEvent.")

        # Retrieve the global identifier for the event from the ListeningEvent enum
        scheduler_event = listening_vent.value

        # Check if a listener is registered for the specified event
        if scheduler_event in self.__listeners:
            listener = self.__listeners[scheduler_event]

            # Ensure the listener is callable before invoking it
            if callable(listener):
                try:
                    # If the listener is a coroutine, schedule it as an asyncio task
                    if asyncio.iscoroutinefunction(listener):
                        asyncio.create_task(listener(event_data, self))
                    # Otherwise, invoke the listener directly as a regular function
                    else:
                        listener(event_data, self)
                except Exception as e:
                    # Log any exceptions that occur during listener invocation
                    self.__logger.error(f"Error invoking global listener for event '{scheduler_event}': {str(e)}")

    def __taskCallableListener(
        self,
        event_data: Optional[Union[JobError, JobExecuted, JobSubmitted, JobMissed, JobMaxInstances]],
        listening_vent: ListeningEvent
    ) -> None:
        """
        Invoke registered listeners for specific task/job events.

        This method handles task/job-specific events such as job errors, executions, submissions,
        missed jobs, and max instance violations. It checks if a listener is registered for the
        specific job ID associated with the event and invokes the appropriate method on the listener
        if callable. The listener can be either a coroutine or a regular function.

        Parameters
        ----------
        event_data : Optional[Union[JobError, JobExecuted, JobSubmitted, JobMissed, JobMaxInstances]]
            The event data associated with the task/job event. This includes details about the job,
            such as its ID, exception (if any), and other context. If no specific data is available,
            this parameter can be None.
        listening_vent : ListeningEvent
            An instance of the ListeningEvent enum representing the task/job event to handle.

        Returns
        -------
        None
            This method does not return any value. It invokes the registered listener for the
            specified job event, if one exists.

        Raises
        ------
        CLIOrionisValueError
            If the provided `listening_vent` is not an instance of ListeningEvent.
        """

        # Validate that the provided event is an instance of ListeningEvent
        if not isinstance(listening_vent, ListeningEvent):
            raise CLIOrionisValueError("The event must be an instance of ListeningEvent.")

        # Validate that event_data is not None and has a job_id attribute
        if event_data is None or not hasattr(event_data, 'job_id'):
            return

        # Retrieve the global identifier for the event from the ListeningEvent enum
        scheduler_event = listening_vent.value

        # Check if a listener is registered for the specific job ID in the event data
        if event_data.job_id in self.__listeners:

            # Retrieve the listener for the specific job ID
            listener = self.__listeners[event_data.job_id]

            # Check if the listener is an instance of IScheduleEventListener
            if isinstance(listener, IScheduleEventListener):

                # Check if the listener has a method corresponding to the event type
                if hasattr(listener, scheduler_event) and callable(getattr(listener, scheduler_event)):
                    listener_method = getattr(listener, scheduler_event)

                    try:
                        # Invoke the listener method, handling both coroutine and regular functions
                        if asyncio.iscoroutinefunction(listener_method):
                            # Schedule the coroutine listener method as an asyncio task
                            asyncio.create_task(listener_method(event_data, self))
                        else:
                            # Call the regular listener method directly
                            listener_method(event_data, self)
                    except Exception as e:
                        # Log any exceptions that occur during listener invocation
                        self.__logger.error(f"Error invoking listener method '{scheduler_event}' for job '{event_data.job_id}': {str(e)}")

    def __startedListener(
        self,
        event: SchedulerStarted
    ) -> None:
        """
        Handle the scheduler started event for logging and invoking registered listeners.

        This method is triggered when the scheduler starts. It logs an informational
        message indicating that the scheduler has started successfully and displays
        a formatted message on the rich console. If a listener is registered for the
        scheduler started event, it invokes the listener with the event details.

        Parameters
        ----------
        event : SchedulerStarted
            An event object containing details about the scheduler start event.

        Returns
        -------
        None
            This method does not return any value. It performs logging, displays
            a message on the console, and invokes any registered listener for the
            scheduler started event.
        """

        # Get the current time in the configured timezone
        now = self.__getCurrentTime()

        # Log an informational message indicating that the scheduler has started
        self.__logger.info(f"Orionis Scheduler started successfully at {now}.")

        # Display a start message for the scheduler worker on the rich console
        # Add a blank line for better formatting
        self.__rich_console.line()
        panel_content = Text.assemble(
            (" Orionis Scheduler Worker ", "bold white on green"),                      # Header text with styling
            ("\n\n", ""),                                                               # Add spacing
            ("The scheduled tasks worker has started successfully.\n", "white"),        # Main message
            (f"Started at: {now}\n", "dim"),                                            # Display the start time in dim text
            ("To stop the worker, press ", "white"),                                    # Instruction text
            ("Ctrl+C", "bold yellow"),                                                  # Highlight the key combination
            (".", "white")                                                              # End the instruction
        )

        # Display the message in a styled panel
        self.__rich_console.print(
            Panel(panel_content, border_style="green", padding=(1, 2))
        )

        # Add another blank line for better formatting
        self.__rich_console.line()

        # Check if a listener is registered for the scheduler started event
        self.__globalCallableListener(event, ListeningEvent.SCHEDULER_STARTED)

    def __pausedListener(
        self,
        event: SchedulerPaused
    ) -> None:
        """
        Handle the scheduler paused event for logging and invoking registered listeners.

        This method is triggered when the scheduler is paused. It logs an informational
        message indicating that the scheduler has been paused successfully and displays
        a formatted message on the rich console. If a listener is registered for the
        scheduler paused event, it invokes the listener with the event details.

        Parameters
        ----------
        event : SchedulerPaused
            An event object containing details about the scheduler paused event.

        Returns
        -------
        None
            This method does not return any value. It performs logging, displays
            a message on the console, and invokes any registered listener for the
            scheduler paused event.
        """

        # Get the current time in the configured timezone
        now = self.__getCurrentTime()

        # Create a paused message
        message = f"Orionis Scheduler paused successfully at {now}."

        # Log an informational message indicating that the scheduler has been paused
        self.__logger.info(message)

        # Check if a listener is registered for the scheduler paused event
        self.__globalCallableListener(event, ListeningEvent.SCHEDULER_PAUSED)

    def __resumedListener(
        self,
        event: SchedulerResumed
    ) -> None:
        """
        Handle the scheduler resumed event for logging and invoking registered listeners.

        This method is triggered when the scheduler resumes from a paused state. It logs an informational
        message indicating that the scheduler has resumed successfully and displays a formatted message
        on the rich console. If a listener is registered for the scheduler resumed event, it invokes
        the listener with the event details.

        Parameters
        ----------
        event : SchedulerResumed
            An event object containing details about the scheduler resumed event.

        Returns
        -------
        None
            This method does not return any value. It performs logging, displays
            a message on the console, and invokes any registered listener for the
            scheduler resumed event.
        """

        # Get the current time in the configured timezone
        now = self.__getCurrentTime()

        # Create a resumed message
        message = f"Orionis Scheduler resumed successfully at {now}."

        # Log an informational message indicating that the scheduler has resumed
        self.__logger.info(message)

        # Check if a listener is registered for the scheduler resumed event
        self.__globalCallableListener(event, ListeningEvent.SCHEDULER_RESUMED)

    def __shutdownListener(
        self,
        event: SchedulerShutdown
    ) -> None:
        """
        Handle the scheduler shutdown event for logging and invoking registered listeners.

        This method is triggered when the scheduler shuts down. It logs an informational
        message indicating that the scheduler has shut down successfully and displays
        a formatted message on the rich console. If a listener is registered for the
        scheduler shutdown event, it invokes the listener with the event details.

        Parameters
        ----------
        event : SchedulerShutdown
            An event object containing details about the scheduler shutdown event.

        Returns
        -------
        None
            This method does not return any value. It performs logging, displays
            a message on the console, and invokes any registered listener for the
            scheduler shutdown event.
        """

        # Get the current time in the configured timezone
        now = self.__getCurrentTime()

        # Create a shutdown message
        message = f"Orionis Scheduler shut down successfully at {now}."

        # Log an informational message indicating that the scheduler has shut down
        self.__logger.info(message)

        # Check if a listener is registered for the scheduler shutdown event
        self.__globalCallableListener(event, ListeningEvent.SCHEDULER_SHUTDOWN)

    def __errorListener(
        self,
        event: JobError
    ) -> None:
        """
        Handle job error events for logging and error reporting.

        This method is triggered when a job execution results in an error. It logs an error
        message indicating the job ID and the exception raised. If the application is in
        debug mode, it also reports the error using the error reporter. Additionally, if a
        listener is registered for the errored job, it invokes the listener with the event details.

        Parameters
        ----------
        event : JobError
            An instance of the JobError event containing details about the errored job,
            including its ID and the exception raised.

        Returns
        -------
        None
            This method does not return any value. It performs logging, error reporting,
            and listener invocation for the job error event.
        """

        # Create an error message
        message = f"Task {event.job_id} raised an exception: {event.exception}"

        # Log an error message indicating that the job raised an exception
        self.__logger.error(message)

        # If a listener is registered for this job ID, invoke the listener with the event details
        self.__taskCallableListener(event, ListeningEvent.JOB_ON_FAILURE)

        # Check if a listener is registered for the scheduler started event
        self.__globalCallableListener(event, ListeningEvent.SCHEDULER_ERROR)

    def __submittedListener(
        self,
        event: JobSubmitted
    ) -> None:
        """
        Handle job submission events for logging and error reporting.

        This method is triggered when a job is submitted to its executor. It logs an informational
        message indicating that the job has been submitted successfully. If the application is in
        debug mode, it also displays a message on the console. Additionally, if a listener is
        registered for the submitted job, it invokes the listener with the event details.

        Parameters
        ----------
        event : JobSubmitted
            An instance of the JobSubmitted containing details about the submitted job,
            including its ID and scheduled run times.

        Returns
        -------
        None
            This method does not return any value. It performs logging, error reporting,
            and listener invocation for the job submission event.
        """

        # Create a submission message
        message = f"Task {event.job_id} submitted to executor."

        # Log an informational message indicating that the job has been submitted
        self.__logger.info(message)

        # If a listener is registered for this job ID, invoke the listener with the event details
        self.__taskCallableListener(event, ListeningEvent.JOB_BEFORE)

    def __executedListener(
        self,
        event: JobExecuted
    ) -> None:
        """
        Handle job execution events for logging and error reporting.

        This method is triggered when a job is executed by its executor. It logs an informational
        message indicating that the job has been executed successfully. If the application is in
        debug mode, it also displays a message on the console. If the job execution resulted in
        an exception, it logs the error and reports it using the error reporter. Additionally,
        if a listener is registered for the executed job, it invokes the listener with the event details.

        Parameters
        ----------
        event : JobExecuted
            An instance of the JobExecuted containing details about the executed job,
            including its ID, return value, exception (if any), and traceback.

        Returns
        -------
        None
            This method does not return any value. It performs logging, error reporting,
            and listener invocation for the job execution event.
        """

        # Create an execution message
        message = f"Task {event.job_id} executed."

        # Log an informational message indicating that the job has been executed
        self.__logger.info(message)

        # If a listener is registered for this job ID, invoke the listener with the event details
        self.__taskCallableListener(event, ListeningEvent.JOB_AFTER)

    def __missedListener(
        self,
        event: JobMissed
    ) -> None:
        """
        Handle job missed events for debugging and error reporting.

        This method is triggered when a scheduled job is missed. It logs a warning
        message indicating the missed job and its scheduled run time. If the application
        is in debug mode, it reports the missed job using the error reporter. Additionally,
        if a listener is registered for the missed job, it invokes the listener with the
        event details.

        Parameters
        ----------
        event : JobMissed
            An instance of the JobMissed event containing details about the missed job,
            including its ID and scheduled run time.

        Returns
        -------
        None
            This method does not return any value. It performs logging, error reporting,
            and listener invocation for the missed job event.
        """

        # Create a missed job message
        message = f"Task {event.job_id} was missed. It was scheduled to run at {event.scheduled_run_time}."

        # Log a warning indicating that the job was missed
        self.__logger.warning(message)

        # If a listener is registered for this job ID, invoke the listener with the event details
        self.__taskCallableListener(event, ListeningEvent.JOB_ON_MISSED)

    def __maxInstancesListener(
        self,
        event: JobMaxInstances
    ) -> None:
        """
        Handle job max instances events for logging and error reporting.

        This method is triggered when a job execution exceeds the maximum allowed
        concurrent instances. It logs an error message indicating the job ID and
        the exception raised. If the application is in debug mode, it also reports
        the error using the error reporter. Additionally, if a listener is registered
        for the job that exceeded max instances, it invokes the listener with the event details.

        Parameters
        ----------
        event : JobMaxInstances
            An instance of the JobMaxInstances event containing details about the job that
            exceeded max instances, including its ID and the exception raised.

        Returns
        -------
        None
            This method does not return any value. It performs logging, error reporting,
            and listener invocation for the job max instances event.
        """

        # Create a max instances error message
        message = f"Task {event.job_id} exceeded maximum instances"

        # Log an error message indicating that the job exceeded maximum instances
        self.__logger.error(message)

        # If a listener is registered for this job ID, invoke the listener with the event details
        self.__taskCallableListener(event, ListeningEvent.JOB_ON_MAXINSTANCES)

    def __modifiedListener(
        self,
        event: JobModified
    ) -> None:
        """
        Handle job modified events for logging and error reporting.

        This method is triggered when a job is modified. It logs an informational
        message indicating that the job has been modified successfully. If the application
        is in debug mode, it also displays a message on the console. Additionally, if a
        listener is registered for the modified job, it invokes the listener with the
        event details.

        Parameters
        ----------
        event : JobModified
            An instance of the JobModified event containing details about the modified job,
            including its ID and other relevant information.

        Returns
        -------
        None
            This method does not return any value. It performs logging, error reporting,
            and listener invocation for the job modified event.
        """

        # Create a modified message
        message = f"Task {event.job_id} has been modified."

        # Log an informational message indicating that the job has been modified
        self.__logger.info(message)

        # If a listener is registered for this job ID, invoke the listener with the event details
        if event.next_run_time is None:
            self.__taskCallableListener(event, ListeningEvent.JOB_ON_PAUSED)
        else:
            self.__taskCallableListener(event, ListeningEvent.JOB_ON_RESUMED)

    def __removedListener(
        self,
        event: JobRemoved
    ) -> None:
        """
        Handle job removal events for logging and invoking registered listeners.

        This method is triggered when a job is removed from the scheduler. It logs an informational
        message indicating that the job has been removed successfully. If the application is in debug
        mode, it displays a message on the console. Additionally, if a listener is registered for the
        removed job, it invokes the listener with the event details.

        Parameters
        ----------
        event : JobRemoved
            An instance of the JobRemoved event containing details about the removed job,
            including its ID and other relevant information.

        Returns
        -------
        None
            This method does not return any value. It performs logging and invokes any registered
            listener for the job removal event.
        """

        # Create a message indicating that the job has been removed
        message = f"Task {event.job_id} has been removed."

        # Log the removal of the job
        self.__logger.info(message)

        # If a listener is registered for this job ID, invoke the listener with the event details
        self.__taskCallableListener(event, ListeningEvent.JOB_ON_REMOVED)

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
                self.__jobs.append(entity)

                # Create a unique key for the job based on its signature
                def create_job_func(cmd, args_list):
                    return lambda: self.__reactor.call(cmd, args_list)

                self.__scheduler.add_job(
                    func=create_job_func(signature, list(entity.args)),
                    trigger=entity.trigger,
                    id=signature,
                    name=signature,
                    replace_existing=True
                )

                # If a listener is associated with the event, register it
                if entity.listener:
                    self.setListener(signature, entity.listener)

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

        # If the event is an instance of ListeningEvent, extract its value
        if isinstance(event, ListeningEvent):
            event = event.value

        # Validate that the event name is a non-empty string
        if not isinstance(event, str) or not event.strip():
            raise ValueError("Event name must be a non-empty string.")

        # Validate that the listener is either callable or an instance of IScheduleEventListener
        if not callable(listener) and not isinstance(listener, IScheduleEventListener):
            raise ValueError("Listener must be a callable function or an instance of IScheduleEventListener.")

        # Register the listener for the specified event in the internal listeners dictionary
        self.__listeners[event] = listener

    def pauseEverythingAt(
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

        # Validate that the 'at' parameter is a datetime object
        if not isinstance(at, datetime):
            raise ValueError("The 'at' parameter must be a datetime object.")

        # Add a job to the scheduler to pause it at the specified datetime
        self.__scheduler.add_job(
            func=self.__scheduler.pause,                    # Function to pause the scheduler
            trigger=DateTrigger(run_date=at),               # Trigger type is 'date' for one-time execution
            id=f"pause_scheduler_at_{at.isoformat()}",      # Unique job ID based on the datetime
            name=f"Pause Scheduler at {at.isoformat()}",    # Descriptive name for the job
            replace_existing=True                           # Replace any existing job with the same ID
        )

    def resumeEverythingAt(
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

        # Validate that the 'at' parameter is a datetime object
        if not isinstance(at, datetime):
            raise ValueError("The 'at' parameter must be a datetime object.")

        # Add a job to the scheduler to resume it at the specified datetime
        self.__scheduler.add_job(
            func=self.__scheduler.resume,                   # Function to resume the scheduler
            trigger=DateTrigger(run_date=at),               # Trigger type is 'date' for one-time execution
            id=f"resume_scheduler_at_{at.isoformat()}",     # Unique job ID based on the datetime
            name=f"Resume Scheduler at {at.isoformat()}",   # Descriptive name for the job
            replace_existing=True                           # Replace any existing job with the same ID
        )

    def shutdownEverythingAt(
        self,
        at: datetime
    ) -> None:
        """
        Schedule the scheduler to shut down all operations at a specific datetime.

        This method allows you to schedule a job that will shut down the AsyncIOScheduler
        at the specified datetime. The job is added to the scheduler with a 'date'
        trigger, ensuring it executes exactly at the given time.

        Parameters
        ----------
        at : datetime
            The datetime at which the scheduler should be shut down. Must be a valid
            datetime object.

        Returns
        -------
        None
            This method does not return any value. It schedules a job to shut down the
            scheduler at the specified datetime.

        Raises
        ------
        ValueError
            If the 'at' parameter is not a valid datetime object.
        """

        # Validate that the 'at' parameter is a datetime object
        if not isinstance(at, datetime):
            raise ValueError("The 'at' parameter must be a datetime object.")

        # Add a job to the scheduler to shut it down at the specified datetime
        self.__scheduler.add_job(
            func=self.__scheduler.shutdown,                 # Function to shut down the scheduler
            trigger=DateTrigger(run_date=at),               # Trigger type is 'date' for one-time execution
            id=f"shutdown_scheduler_at_{at.isoformat()}",   # Unique job ID based on the datetime
            name=f"Shutdown Scheduler at {at.isoformat()}", # Descriptive name for the job
            replace_existing=True                           # Replace any existing job with the same ID
        )

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

            # Ensure all events are loaded into the internal jobs list
            self.__loadEvents()

            # Subscribe to scheduler events for monitoring and handling
            self.__subscribeListeners()

            # Ensure we're in an asyncio context
            asyncio.get_running_loop()

            # Start the scheduler
            if not self.__scheduler.running:
                self.__scheduler.start()

            # Keep the event loop alive to process scheduled jobs
            try:

                # Run indefinitely until interrupted
                while self.__scheduler.running:
                    await asyncio.sleep(1)

            except (KeyboardInterrupt, asyncio.CancelledError):
                await self.shutdown()
            except Exception as e:
                raise CLIOrionisRuntimeError(f"Failed to start the scheduler: {str(e)}") from e


        except Exception as e:

            # Handle exceptions that may occur during scheduler startup
            raise CLIOrionisRuntimeError(f"Failed to start the scheduler: {str(e)}")

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

        # Ensure the 'wait' parameter is a boolean value.
        if not isinstance(wait, bool):
            raise ValueError("The 'wait' parameter must be a boolean value.")

        # If the scheduler is not running, there is nothing to shut down.
        if not self.__scheduler.running:
            return

        try:
            # Shut down the AsyncIOScheduler. If 'wait' is True, it waits for currently executing jobs to finish.
            self.__scheduler.shutdown(wait=wait)

            # If 'wait' is True, allow a small delay to ensure proper cleanup of resources.
            if wait:
                await asyncio.sleep(0)

        except Exception as e:

            # Raise a runtime error if the shutdown process fails.
            raise CLIOrionisRuntimeError(f"Failed to shut down the scheduler: {str(e)}") from e

    def pause(self, signature: str) -> bool:
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

        # Validate that the signature is a non-empty string
        if not isinstance(signature, str) or not signature.strip():
            raise CLIOrionisValueError("Signature must be a non-empty string.")

        try:

            # Attempt to pause the job with the given signature
            self.__scheduler.pause_job(signature)

            # Log the successful pausing of the job
            self.__logger.info(f"Job '{signature}' has been paused.")

            # Return True to indicate the job was successfully paused
            return True

        except Exception:

            # Return False if the job could not be paused (e.g., it does not exist)
            return False

    def resume(self, signature: str) -> bool:
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

        # Validate that the signature is a non-empty string
        if not isinstance(signature, str) or not signature.strip():
            raise CLIOrionisValueError("Signature must be a non-empty string.")

        try:
            # Attempt to resume the job with the given signature
            self.__scheduler.resume_job(signature)

            # Log the successful resumption of the job
            self.__logger.info(f"Job '{signature}' has been resumed.")

            # Return True to indicate the job was successfully resumed
            return True

        except Exception:

            # Return False if the job could not be resumed (e.g., it does not exist)
            return False

    def remove(self, signature: str) -> bool:
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

        # Validate that the signature is a non-empty string
        if not isinstance(signature, str) or not signature.strip():
            raise CLIOrionisValueError("Signature must be a non-empty string.")

        try:

            # Attempt to remove the job from the scheduler using its signature
            self.__scheduler.remove_job(signature)

            # Iterate through the internal jobs list to find and remove the job
            for job in self.__jobs:
                if job['signature'] == signature:
                    self.__jobs.remove(job)  # Remove the job from the internal list
                    break

            # Log the successful removal of the job
            self.__logger.info(f"Job '{signature}' has been removed from the scheduler.")

            # Return True to indicate the job was successfully removed
            return True

        except Exception:

            # Return False if the job could not be removed (e.g., it does not exist)
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
                'signature': job.signature,
                'args': job.args,
                'purpose': job.purpose,
                'random_delay': job.random_delay,
                'start_date': job.start_date.strftime('%Y-%m-%d %H:%M:%S') if job.start_date else None,
                'end_date': job.end_date.strftime('%Y-%m-%d %H:%M:%S') if job.end_date else None,
                'details': job.details
            })

        # Return the list of scheduled job details
        return events