import asyncio
from datetime import datetime
import logging
from typing import Any, Awaitable, Callable, Dict, List, Optional, Union
import pytz
from apscheduler.events import (
    EVENT_JOB_ERROR,
    EVENT_JOB_EXECUTED,
    EVENT_JOB_MAX_INSTANCES,
    EVENT_JOB_MISSED,
    EVENT_JOB_REMOVED,
    EVENT_JOB_SUBMITTED,
    EVENT_SCHEDULER_PAUSED,
    EVENT_SCHEDULER_RESUMED,
    EVENT_SCHEDULER_SHUTDOWN,
    EVENT_SCHEDULER_STARTED,
)
from apscheduler.schedulers.asyncio import AsyncIOScheduler as APSAsyncIOScheduler
from apscheduler.triggers.date import DateTrigger
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from orionis.console.contracts.event import IEvent
from orionis.console.contracts.reactor import IReactor
from orionis.console.contracts.schedule import ISchedule
from orionis.console.contracts.schedule_event_listener import IScheduleEventListener
from orionis.console.entities.event_job import EventJob
from orionis.console.entities.scheduler_error import SchedulerError
from orionis.console.entities.scheduler_paused import SchedulerPaused
from orionis.console.entities.scheduler_resumed import SchedulerResumed
from orionis.console.entities.scheduler_shutdown import SchedulerShutdown
from orionis.console.entities.scheduler_started import SchedulerStarted
from orionis.console.entities.event import Event as EventEntity
from orionis.console.enums.listener import ListeningEvent
from orionis.console.exceptions import CLIOrionisRuntimeError
from orionis.console.exceptions.cli_orionis_value_error import CLIOrionisValueError
from orionis.console.request.cli_request import CLIRequest
from orionis.failure.contracts.catch import ICatch
from orionis.foundation.contracts.application import IApplication
from orionis.services.log.contracts.log_service import ILogger

class Schedule(ISchedule):

    def __init__(
        self,
        reactor: IReactor,
        app: IApplication,
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
        self.__app: IApplication = app

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
        self.__reactor: IReactor = reactor

        # Retrieve and store all available commands from the reactor.
        self.__available_commands = self.__getCommands()

        # Initialize the jobs dictionary to keep track of scheduled jobs.
        self.__events: Dict[str, IEvent] = {}

        # Initialize the jobs list to keep track of all scheduled jobs.
        self.__jobs: List[EventEntity] = []

        # Initialize the listeners dictionary to manage event listeners.
        self.__listeners: Dict[str, callable] = {}

        # Initialize set to track jobs paused by pauseEverythingAt
        self.__pausedByPauseEverything: set = set()

        # Add this line to the existing __init__ method
        self._stopEvent: Optional[asyncio.Event] = None

        # Retrieve and initialize the catch instance from the application container.
        self.__catch: ICatch = app.make('x-orionis.failure.catch')

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

        # Log the timezone assignment for debugging purposes
        self.__logger.info(f"Timezone assigned to the scheduler: {self.__app.config("app.timezone", "UTC")}")

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
                'description': job.get('description', 'No description available.')
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
        if self.isRunning():
            self.__raiseException(CLIOrionisValueError("Cannot add new commands while the scheduler is running."))

        # Validate that the command signature is a non-empty string
        if not isinstance(signature, str) or not signature.strip():
            raise CLIOrionisValueError("Command signature must be a non-empty string.")

        # Ensure that arguments are either a list of strings or None
        if args is not None and not isinstance(args, list):
            raise CLIOrionisValueError("Arguments must be a list of strings or None.")

        # Check if the command is available in the registered commands
        if not self.__isAvailable(signature):
            raise CLIOrionisValueError(f"The command '{signature}' is not available or does not exist.")

        # Import Event here to avoid circular dependency issues
        from orionis.console.fluent.event import Event

        # Store the command and its arguments for scheduling
        self.__events[signature] = Event(
            signature=signature,
            args=args or [],
            purpose=self.__getDescription(signature)
        )

        # Return the Event instance for further scheduling configuration
        return self.__events[signature]

    def __getTaskFromSchedulerById(
        self,
        id: str,
        code: int = None
    ) -> Optional[EventJob]:
        """
        Retrieve a scheduled job from the AsyncIOScheduler by its unique ID.

        This method fetches a job from the AsyncIOScheduler using its unique identifier (ID).
        It extracts the job's attributes and creates a `Job` entity containing the relevant
        details. If the job does not exist, the method returns `None`.

        Parameters
        ----------
        id : str
            The unique identifier (ID) of the job to retrieve. This must be a non-empty string.

        Returns
        -------
        Optional[Job]
            A `Job` entity containing the details of the scheduled job if it exists.
            If the job does not exist, returns `None`.
        """

        # Extract event data from the internal events list if available
        event_data: dict = {}
        for job in self.events():
            if id == job.get('signature'):
                event_data = job
                break

        # Retrieve the job data from the scheduler using the provided job ID
        data = self.__scheduler.get_job(id)

        # If no job is found, return EventJob with default values
        _id = data.id if data and hasattr(data, 'id') else None
        if not _id and code in (EVENT_JOB_MISSED, EVENT_JOB_REMOVED):
            _id = event_data.get('signature', None)
        elif not _id:
            return EventJob()

        # Extract the job name if available
        _name = data.name if data and hasattr(data, 'name') else None

        # Extract the job function if available
        _func = data.func if data and hasattr(data, 'func') else None

        # Extract the job arguments if available
        _args = data.args if data and hasattr(data, 'args') else tuple(event_data.get('args', []))

        # Extract the job trigger if available
        _trigger = data.trigger if data and hasattr(data, 'trigger') else None

        # Extract the job executor if available
        _executor = data.executor if data and hasattr(data, 'executor') else None

        # Extract the job jobstore if available
        _jobstore = data.jobstore if data and hasattr(data, 'jobstore') else None

        # Extract the job misfire_grace_time if available
        _misfire_grace_time = data.misfire_grace_time if data and hasattr(data, 'misfire_grace_time') else None

        # Extract the job max_instances if available
        _max_instances = data.max_instances if data and hasattr(data, 'max_instances') else 0

        # Extract the job coalesce if available
        _coalesce = data.coalesce if data and hasattr(data, 'coalesce') else False

        # Extract the job next_run_time if available
        _next_run_time = data.next_run_time if data and hasattr(data, 'next_run_time') else None

        # Extract additional event data if available
        _purpose = event_data.get('purpose', None)

        # Extract additional event data if available
        _start_date = event_data.get('start_date', None)

        # Extract additional event data if available
        _end_date = event_data.get('end_date', None)

        # Extract additional event data if available
        _details = event_data.get('details', None)

        # Create and return a Job entity based on the retrieved job data
        return EventJob(
            id=_id,
            code=code if code is not None else 0,
            name=_name,
            func=_func,
            args=_args,
            trigger=_trigger,
            executor=_executor,
            jobstore=_jobstore,
            misfire_grace_time=_misfire_grace_time,
            max_instances=_max_instances,
            coalesce=_coalesce,
            next_run_time=_next_run_time,
            exception = None,
            traceback = None,
            retval = None,
            purpose = _purpose,
            start_date = _start_date,
            end_date = _end_date,
            details = _details
        )

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
        self.__scheduler.add_listener(self.__shutdownListener, EVENT_SCHEDULER_SHUTDOWN)
        self.__scheduler.add_listener(self.__errorListener, EVENT_JOB_ERROR)
        self.__scheduler.add_listener(self.__submittedListener, EVENT_JOB_SUBMITTED)
        self.__scheduler.add_listener(self.__executedListener, EVENT_JOB_EXECUTED)
        self.__scheduler.add_listener(self.__missedListener, EVENT_JOB_MISSED)
        self.__scheduler.add_listener(self.__maxInstancesListener, EVENT_JOB_MAX_INSTANCES)
        self.__scheduler.add_listener(self.__removedListener, EVENT_JOB_REMOVED)

    def __globalCallableListener(
        self,
        event_data: Optional[Union[SchedulerStarted, SchedulerPaused, SchedulerResumed, SchedulerShutdown, SchedulerError]],
        listening_vent: ListeningEvent
    ) -> None:
        """
        Invoke registered listeners for global scheduler events.

        This method handles global scheduler events such as when the scheduler starts, pauses, resumes,
        or shuts down. It checks if a listener is registered for the specified event and invokes it if callable.
        The listener can be either a coroutine or a regular function.

        Parameters
        ----------
        event_data : Optional[Union[SchedulerStarted, SchedulerPaused, SchedulerResumed, SchedulerShutdown, ...]]
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
            self.__raiseException(CLIOrionisValueError("The event must be an instance of ListeningEvent."))

        # Retrieve the global identifier for the event from the ListeningEvent enum
        scheduler_event = listening_vent.value

        # Check if a listener is registered for the specified event
        if scheduler_event in self.__listeners:

            # Get the listener for the specified event
            listener = self.__listeners[scheduler_event]

            # If is Callable
            if callable(listener):

                # Invoke the listener, handling both coroutine and regular functions
                try:
                    self.__app.invoke(listener, event_data, self)
                except BaseException as e:
                    self.__raiseException(e)

    def __taskCallableListener(
        self,
        event_data: EventJob,
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
        event_data : EventJob
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
            self.__raiseException(CLIOrionisValueError("The event must be an instance of ListeningEvent."))

        # Validate that event_data is not None and has a id attribute
        if not isinstance(event_data, EventJob) or not hasattr(event_data, 'id') or not event_data.id:
            return

        # Retrieve the global identifier for the event from the ListeningEvent enum
        scheduler_event = listening_vent.value

        # Check if a listener is registered for the specific job ID in the event data
        if event_data.id in self.__listeners:

            # Retrieve the listener for the specific job ID
            listener = self.__listeners[event_data.id]

            # Check if the listener is an instance of IScheduleEventListener
            if issubclass(listener, IScheduleEventListener):

                try:

                    # Initialize the listener if it's a class
                    if isinstance(listener, type):
                        listener = self.__app.make(listener)

                    # Check if the listener has a method corresponding to the event type
                    if hasattr(listener, scheduler_event) and callable(getattr(listener, scheduler_event)):
                        self.__app.call(listener, scheduler_event, event_data, self)

                except BaseException as e:

                    # If an error occurs while invoking the listener, raise an exception
                    self.__raiseException(e)

            else:

                # If the listener is not a subclass of IScheduleEventListener, raise an exception
                self.__raiseException(CLIOrionisValueError(f"The listener for job ID '{event_data.id}' must be a subclass of IScheduleEventListener."))

    def __startedListener(
        self,
        event
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
        event_data = SchedulerStarted(
            code=event.code if hasattr(event, 'code') else 0,
            time=now,
            tasks=self.events()
        )

        # If a listener is registered for this event, invoke the listener with the event details
        self.__globalCallableListener(event_data, ListeningEvent.SCHEDULER_STARTED)

        # Log an informational message indicating that the scheduler has started
        self.__logger.info(f"Orionis Scheduler started successfully at {now}.")

    def __shutdownListener(
        self,
        event
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

        # Check if a listener is registered for the scheduler shutdown event
        event_data = SchedulerShutdown(
            code=event.code if hasattr(event, 'code') else 0,
            time=now,
            tasks=self.events()
        )
        self.__globalCallableListener(event_data, ListeningEvent.SCHEDULER_SHUTDOWN)

        # Log an informational message indicating that the scheduler has shut down
        self.__logger.info(f"Orionis Scheduler shut down successfully at {now}.")

    def __errorListener(
        self,
        event
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
        # Log an error message indicating that the job raised an exception
        self.__logger.error(f"Task '{event.job_id}' raised an exception: {event.exception}")

        # If a listener is registered for this job ID, invoke the listener with the event details
        job_event_data = self.__getTaskFromSchedulerById(event.job_id)
        job_event_data.code = event.code if hasattr(event, 'code') else 0
        job_event_data.exception = event.exception if hasattr(event, 'exception') else None
        job_event_data.traceback = event.traceback if hasattr(event, 'traceback') else None

        # Call the task-specific listener for job errors
        self.__taskCallableListener(job_event_data, ListeningEvent.JOB_ON_FAILURE)

        # Check if a listener is registered for the scheduler error event
        event_data = SchedulerError(
            code=event.code if hasattr(event, 'code') else 0,
            exception=event.exception if hasattr(event, 'exception') else None,
            traceback=event.traceback if hasattr(event, 'traceback') else None,
        )
        self.__globalCallableListener(event_data, ListeningEvent.SCHEDULER_ERROR)

        # Catch any exceptions that occur during command handling
        self.__raiseException(event.exception)

    def __submittedListener(
        self,
        event
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

        # Log an informational message indicating that the job has been submitted
        self.__logger.info(f"Task '{event.job_id}' submitted to executor.")

        # Create entity for job submitted event
        data_event = self.__getTaskFromSchedulerById(event.job_id, event.code)

        # If a listener is registered for this job ID, invoke the listener with the event details
        self.__taskCallableListener(data_event, ListeningEvent.JOB_BEFORE)

    def __executedListener(
        self,
        event
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

        # Log an informational message indicating that the job has been executed
        self.__logger.info(f"Task '{event.job_id}' executed.")

        # Create entity for job executed event
        data_event = self.__getTaskFromSchedulerById(event.job_id, event.code)

        # If a listener is registered for this job ID, invoke the listener with the event details
        self.__taskCallableListener(data_event, ListeningEvent.JOB_AFTER)

    def __missedListener(
        self,
        event
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

        # Log a warning indicating that the job was missed
        self.__logger.warning(f"Task '{event.job_id}' was missed. It was scheduled to run at {event.scheduled_run_time}.")

        # Create entity for job missed event
        data_event = self.__getTaskFromSchedulerById(event.job_id, event.code)

        # If a listener is registered for this job ID, invoke the listener with the event details
        self.__taskCallableListener(data_event, ListeningEvent.JOB_ON_MISSED)

    def __maxInstancesListener(
        self,
        event
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

        # Log an error message indicating that the job exceeded maximum instances
        self.__logger.error(f"Task '{event.job_id}' exceeded maximum instances")

        # Create entity for job max instances event
        data_event = self.__getTaskFromSchedulerById(event.job_id, event.code)

        # If a listener is registered for this job ID, invoke the listener with the event details
        self.__taskCallableListener(data_event, ListeningEvent.JOB_ON_MAXINSTANCES)

    def __removedListener(
        self,
        event
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

        # Log the removal of the job
        self.__logger.info(f"Task '{event.job_id}' has been removed.")

        # Create entity for job removed event
        data_event = self.__getTaskFromSchedulerById(event.job_id, event.code)

        # If a listener is registered for this job ID, invoke the listener with the event details
        self.__taskCallableListener(data_event, ListeningEvent.JOB_ON_REMOVED)

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

                try:
                    # Convert the event to its entity representation
                    entity: EventEntity = event.toEntity()

                    # Add the job to the internal jobs list
                    self.__jobs.append(entity)

                    # Create a unique key for the job based on its signature
                    def create_job_func(cmd, args_list):
                        return lambda: self.__reactor.call(cmd, args_list)

                    # Add the job to the scheduler with the specified trigger and parameters
                    self.__scheduler.add_job(
                        func=create_job_func(signature, list(entity.args)),
                        trigger=entity.trigger,
                        id=signature,
                        name=signature,
                        replace_existing=True,
                        max_instances=entity.max_instances,
                        misfire_grace_time=entity.misfire_grace_time
                    )

                    # If a listener is associated with the event, register it
                    if entity.listener:
                        self.setListener(signature, entity.listener)

                    # Log the successful loading of the scheduled event
                    self.__logger.debug(f"Scheduled event '{signature}' loaded successfully.")

                except Exception as e:

                    # Construct the error message
                    error_msg = f"Failed to load scheduled event '{signature}': {str(e)}"

                    # Log the error message
                    self.__logger.error(error_msg)

                    # Raise a runtime error if loading the scheduled event fails
                    raise CLIOrionisRuntimeError(error_msg)

    def __raiseException(
        self,
        exception: BaseException
    ) -> None:
        """
        Handle and propagate exceptions through the application's error handling system.

        This private method serves as a centralized exception handler for the scheduler,
        delegating exception processing to the application's error catching mechanism.
        It ensures that all exceptions occurring within the scheduler context are
        properly handled according to the application's error handling policies.

        The method acts as a bridge between the scheduler's internal operations and
        the application's global exception handling system, providing consistent
        error handling behavior across the entire application.

        Parameters
        ----------
        exception : BaseException
            The exception instance that was raised during command execution. This can be
            any type of exception that inherits from BaseException, including system
            exceptions, custom application exceptions, and runtime errors.

        Returns
        -------
        None
            This method does not return any value. It delegates exception handling
            to the application's error catching mechanism and may re-raise the
            exception depending on the configured error handling behavior.

        Notes
        -----
        This method is intended for internal use within the scheduler and should not
        be called directly by external code. The error catching mechanism may perform
        various actions such as logging, reporting, or re-raising the exception based
        on the application's configuration.
        """

        # Delegate exception handling to the application's error catching mechanism
        # This ensures consistent error handling across the entire application
        self.__catch.exception(self, CLIRequest(command="schedule:work", args={}), exception)

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
        CLIOrionisValueError
            If the event name is not a non-empty string or if the listener is not callable
            or an instance of IScheduleEventListener.
        """

        # If the event is an instance of ListeningEvent, extract its value
        if isinstance(event, ListeningEvent):
            event = event.value

        # Validate that the event name is a non-empty string
        if not isinstance(event, str) or not event.strip():
            raise CLIOrionisValueError("Event name must be a non-empty string.")

        # Validate that the listener is either callable or an instance of IScheduleEventListener
        if not callable(listener) and not isinstance(listener, IScheduleEventListener):
            raise CLIOrionisValueError("Listener must be a callable function or an instance of IScheduleEventListener.")

        # Register the listener for the specified event in the internal listeners dictionary
        self.__listeners[event] = listener

    def wrapAsyncFunction(
        self,
        func: Callable[..., Awaitable[Any]]
    ) -> Callable[..., Any]:
        """
        Wrap an asynchronous function to be executed in a synchronous context.

        This method creates a synchronous wrapper around an asynchronous function (coroutine)
        that enables its execution within non-async contexts. The wrapper leverages the
        Coroutine utility class to handle the complexities of asyncio event loop management
        and provides proper error handling with detailed logging and custom exception
        propagation.

        The wrapper is particularly useful when integrating asynchronous functions with
        synchronous APIs or frameworks that do not natively support async operations,
        such as the APScheduler job execution environment.

        Parameters
        ----------
        func : Callable[..., Awaitable[Any]]
            The asynchronous function (coroutine) to be wrapped. This function must be
            defined using the `async def` syntax and return an awaitable object. The
            function can accept any number of positional and keyword arguments.

        Returns
        -------
        Callable[..., Any]
            A synchronous wrapper function that executes the original asynchronous
            function and returns its result. The wrapper function accepts the same
            arguments as the original async function and forwards them appropriately.
            The return type depends on what the wrapped asynchronous function returns.

        Raises
        ------
        CLIOrionisRuntimeError
            If the asynchronous function execution fails or if the provided `func`
            parameter is not a valid asynchronous function. The original exception
            is wrapped to provide additional context for debugging.

        Notes
        -----
        This method relies on the Coroutine utility class from the orionis.services.asynchrony
        module to handle the execution of the wrapped asynchronous function. The wrapper
        uses the instance logger for comprehensive error reporting and debugging information.
        """

        def sync_wrapper(*args, **kwargs) -> Any:
            """
            Synchronous wrapper function that executes asynchronous functions in a thread-safe manner.

            This wrapper provides a uniform interface for executing asynchronous functions within
            synchronous contexts by leveraging the Coroutine utility class. It handles the complexity
            of managing async/await patterns and provides proper error handling with detailed logging
            and custom exception propagation.

            The wrapper is particularly useful when integrating asynchronous functions with
            synchronous APIs or frameworks that do not natively support async operations.

            Parameters
            ----------
            *args : tuple
            Variable length argument list to pass to the wrapped asynchronous function.
            These arguments are forwarded directly to the original function.
            **kwargs : dict
            Arbitrary keyword arguments to pass to the wrapped asynchronous function.
            These keyword arguments are forwarded directly to the original function.

            Returns
            -------
            Any
            The return value from the executed asynchronous function. The type depends
            on what the wrapped function returns and can be any Python object.

            Raises
            ------
            CLIOrionisRuntimeError
            When the asynchronous function execution fails, wrapping the original
            exception with additional context and error details for better debugging.

            Notes
            -----
            This function relies on the Coroutine utility class to handle the execution
            of the wrapped asynchronous function and uses the instance logger for comprehensive
            error reporting and debugging information.
            """

            # Execute the asynchronous function using the container's invoke method
            try:
                self.__app.invoke(func, *args, **kwargs)

            # If an error occurs during execution, raise a custom exception
            except Exception as e:
                self.__raiseException(e)

        # Return the synchronous wrapper function
        return sync_wrapper

    def pauseEverythingAt(
        self,
        at: datetime
    ) -> None:
        """
        Schedule the scheduler to pause all operations at a specific datetime.

        This method schedules a job that pauses the AsyncIOScheduler at the specified datetime.
        The job is added to the scheduler with a 'date' trigger, ensuring it executes exactly
        at the given time. If a pause job already exists, it is replaced to avoid conflicts.

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
            If the 'at' parameter is not a valid datetime object or is not in the future.
        CLIOrionisRuntimeError
            If the scheduler is not running or if an error occurs during job scheduling.
        """

        # Validate that the 'at' parameter is a datetime object
        if not isinstance(at, datetime):
            CLIOrionisValueError("The 'at' parameter must be a datetime object.")

        # Define an async function to pause the scheduler
        async def schedule_pause():

            # Only pause jobs if the scheduler is currently running
            if self.isRunning():

                # Clear the set of previously paused jobs
                self.__pausedByPauseEverything.clear()

                # Get all jobs from the scheduler
                all_jobs = self.__scheduler.get_jobs()

                # Filter out system jobs (pause, resume, shutdown tasks)
                system_job_ids = {
                    "scheduler_pause_at",
                    "scheduler_resume_at",
                    "scheduler_shutdown_at"
                }

                # Pause only user jobs, not system jobs
                for job in all_jobs:

                    # Check if the job is not a system job
                    if job.id not in system_job_ids:

                        try:

                            # Pause the job in the scheduler
                            self.__scheduler.pause_job(job.id)
                            self.__pausedByPauseEverything.add(job.id)

                            # Get the current time in the configured timezone
                            now = self.__getCurrentTime()

                            # Log an informational message indicating that the job has been paused
                            self.__taskCallableListener(
                                self.__getTaskFromSchedulerById(job.id),
                                ListeningEvent.JOB_ON_PAUSED
                            )

                            # Log the pause action
                            self.__logger.info(f"Job '{job.id}' paused successfully at {now}.")

                        except Exception as e:

                            # If an error occurs while pausing the job, raise an exception
                            self.__raiseException(e)

                # Execute the global callable listener after all jobs are paused
                self.__globalCallableListener(SchedulerPaused(
                    code=EVENT_SCHEDULER_PAUSED,
                    time=self.__getCurrentTime()
                ), ListeningEvent.SCHEDULER_PAUSED)

                # Log that all user jobs have been paused
                self.__logger.info("All user jobs have been paused. System jobs remain active.")

        try:

            # Remove any existing pause job to avoid conflicts
            try:
                self.__scheduler.remove_job("scheduler_pause_at")

            # If the job doesn't exist, it's fine to proceed
            except:
                pass

            # Add a job to the scheduler to pause it at the specified datetime
            self.__scheduler.add_job(
                func=self.wrapAsyncFunction(schedule_pause),    # Function to pause the scheduler
                trigger=DateTrigger(run_date=at),               # Trigger type is 'date' for one-time execution
                id="scheduler_pause_at",                        # Unique job ID for pausing the scheduler
                name="Pause Scheduler",                         # Descriptive name for the job
                replace_existing=True                           # Replace any existing job with the same ID
            )

            # Log the scheduled pause
            self.__logger.info(f"Scheduler pause scheduled for {at.strftime('%Y-%m-%d %H:%M:%S')}")

        except Exception as e:

            # Handle exceptions that may occur during job scheduling
            raise CLIOrionisRuntimeError(f"Failed to schedule scheduler pause: {str(e)}") from e

    def resumeEverythingAt(
        self,
        at: datetime
    ) -> None:
        """
        Schedule the scheduler to resume all operations at a specific datetime.

        This method schedules a job that resumes the AsyncIOScheduler at the specified datetime.
        The job is added to the scheduler with a 'date' trigger, ensuring it executes exactly
        at the given time. If a resume job already exists, it is replaced to avoid conflicts.

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
            If the 'at' parameter is not a valid datetime object or is not in the future.
        CLIOrionisRuntimeError
            If the scheduler is not running or if an error occurs during job scheduling.
        """

        # Validate that the 'at' parameter is a datetime object
        if not isinstance(at, datetime):
            raise CLIOrionisValueError("The 'at' parameter must be a datetime object.")

        # Define an async function to resume the scheduler
        async def schedule_resume():

            # Only resume jobs if the scheduler is currently running
            if self.isRunning():

                # Resume only jobs that were paused by pauseEverythingAt
                if self.__pausedByPauseEverything:

                    # Iterate through the set of paused job IDs and resume each one
                    for job_id in list(self.__pausedByPauseEverything):

                        try:

                            # Resume the job and log the action
                            self.__scheduler.resume_job(job_id)

                            # Invoke the listener for the resumed job
                            self.__taskCallableListener(
                                self.__getTaskFromSchedulerById(job_id),
                                ListeningEvent.JOB_ON_RESUMED
                            )

                            # Log an informational message indicating that the job has been resumed
                            self.__logger.info(f"User job '{job_id}' has been resumed.")

                        except Exception as e:

                            # If an error occurs while resuming the job, raise an exception
                            self.__raiseException(e)

                    # Clear the set after resuming all jobs
                    self.__pausedByPauseEverything.clear()

                    # Execute the global callable listener after all jobs are resumed
                    self.__globalCallableListener(SchedulerResumed(
                        code=EVENT_SCHEDULER_RESUMED,
                        time=self.__getCurrentTime()
                    ), ListeningEvent.SCHEDULER_RESUMED)

                    # Get the current time in the configured timezone
                    now = self.__getCurrentTime()

                    # Log an informational message indicating that the scheduler has been resumed
                    self.__logger.info(f"Orionis Scheduler resumed successfully at {now}.")

                    # Log that all previously paused jobs have been resumed
                    self.__logger.info("All previously paused user jobs have been resumed.")

        try:

            # Remove any existing resume job to avoid conflicts
            try:
                self.__scheduler.remove_job("scheduler_resume_at")

            # If the job doesn't exist, it's fine to proceed
            except:
                pass

            # Add a job to the scheduler to resume it at the specified datetime
            self.__scheduler.add_job(
                func=self.wrapAsyncFunction(schedule_resume),   # Function to resume the scheduler
                trigger=DateTrigger(run_date=at),               # Trigger type is 'date' for one-time execution
                id="scheduler_resume_at",                       # Unique job ID for resuming the scheduler
                name="Resume Scheduler",                        # Descriptive name for the job
                replace_existing=True                           # Replace any existing job with the same ID
            )

            # Log the scheduled resume
            self.__logger.info(f"Scheduler resume scheduled for {at.strftime('%Y-%m-%d %H:%M:%S')}")

        except Exception as e:

            # Handle exceptions that may occur during job scheduling
            raise CLIOrionisRuntimeError(f"Failed to schedule scheduler resume: {str(e)}") from e

    def shutdownEverythingAt(
        self,
        at: datetime,
        wait: bool = True
    ) -> None:
        """
        Schedule the scheduler to shut down all operations at a specific datetime.

        This method schedules a job that shuts down the AsyncIOScheduler at the specified datetime.
        The job is added to the scheduler with a 'date' trigger, ensuring it executes exactly
        at the given time. If a shutdown job already exists, it is replaced to avoid conflicts.

        Parameters
        ----------
        at : datetime
            The datetime at which the scheduler should be shut down. Must be a valid
            datetime object.
        wait : bool, optional
            Whether to wait for currently running jobs to complete before shutdown.
            Default is True.

        Returns
        -------
        None
            This method does not return any value. It schedules a job to shut down the
            scheduler at the specified datetime.

        Raises
        ------
        ValueError
            If the 'at' parameter is not a valid datetime object or 'wait' is not boolean,
            or if the scheduled time is not in the future.
        CLIOrionisRuntimeError
            If the scheduler is not running or if an error occurs during job scheduling.
        """

        # Validate that the 'at' parameter is a datetime object
        if not isinstance(at, datetime):
            raise ValueError("The 'at' parameter must be a datetime object.")

        # Validate that the 'wait' parameter is a boolean
        if not isinstance(wait, bool):
            raise ValueError("The 'wait' parameter must be a boolean value.")

        # Define an async function to shut down the scheduler
        async def schedule_shutdown():
            # Only shut down the scheduler if it is currently running
            if self.isRunning():
                try:

                    # Log the shutdown initiation
                    self.__logger.info("Initiating scheduled shutdown...")

                    # Call the async shutdown method
                    await self.shutdown(wait=wait)

                except Exception as e:

                    # Log any errors that occur during shutdown
                    self.__logger.error(f"Error during scheduled shutdown: {str(e)}")

                    # Force stop if graceful shutdown fails
                    self.forceStop()

        try:

            # Remove any existing shutdown job to avoid conflicts
            try:
                self.__scheduler.remove_job("scheduler_shutdown_at")

            # If the job doesn't exist, it's fine to proceed
            except:
                pass

            # Add a job to the scheduler to shut it down at the specified datetime
            self.__scheduler.add_job(
                func=self.wrapAsyncFunction(schedule_shutdown),  # Function to shut down the scheduler
                trigger=DateTrigger(run_date=at),               # Trigger type is 'date' for one-time execution
                id="scheduler_shutdown_at",                     # Unique job ID for shutting down the scheduler
                name="Shutdown Scheduler",                      # Descriptive name for the job
                replace_existing=True                           # Replace any existing job with the same ID
            )

            # Log the scheduled shutdown
            self.__logger.info(f"Scheduler shutdown scheduled for {at.strftime('%Y-%m-%d %H:%M:%S')} (wait={wait})")

        except Exception as e:

            # Handle exceptions that may occur during job scheduling
            raise CLIOrionisRuntimeError(f"Failed to schedule scheduler shutdown: {str(e)}") from e

    async def start(self) -> None:
        """
        Start the AsyncIO scheduler instance and keep it running.

        This method initializes and starts the AsyncIOScheduler, which integrates with the asyncio event loop
        to manage asynchronous job execution. It ensures that all scheduled events are loaded, listeners are
        subscribed, and the scheduler is started within an asyncio context. The method keeps the scheduler
        running until a stop signal is received, handling graceful shutdowns and interruptions.

        Returns
        -------
        None
            This method does not return any value. It starts the AsyncIO scheduler, keeps it running, and
            ensures proper cleanup during shutdown.

        Raises
        ------
        CLIOrionisRuntimeError
            If the scheduler fails to start due to missing an asyncio event loop or other runtime issues.
        """
        try:

            # Ensure the method is called within an asyncio event loop
            loop = asyncio.get_running_loop()

            # Create an asyncio event to manage clean shutdowns
            self._stop_event = asyncio.Event()

            # Load all scheduled events into the internal jobs list
            self.__loadEvents()

            # Subscribe to scheduler events for monitoring and handling
            self.__subscribeListeners()

            # Start the scheduler if it is not already running
            if not self.isRunning():
                self.__scheduler.start()

            # Log that the scheduler is now active and waiting for events
            self.__logger.info("Orionis Scheduler is now active and waiting for events...")

            try:
                # Wait for the stop event to be set, which signals a shutdown
                # This avoids using a busy loop and is more efficient
                await self._stop_event.wait()

            except (KeyboardInterrupt, asyncio.CancelledError):

                # Handle graceful shutdown when an interruption signal is received
                self.__logger.info("Received shutdown signal, stopping scheduler...")
                await self.shutdown(wait=True)

            except Exception as e:

                # Log and raise any unexpected exceptions during scheduler operation
                self.__logger.error(f"Error during scheduler operation: {str(e)}")
                raise CLIOrionisRuntimeError(f"Scheduler operation failed: {str(e)}") from e

            finally:

                # Ensure the scheduler is shut down properly, even if an error occurs
                if self.__scheduler.running:
                    await self.shutdown(wait=False)

        except RuntimeError as e:

            # Handle the case where no asyncio event loop is running
            if "no running event loop" in str(e):
                raise CLIOrionisRuntimeError("Scheduler must be started within an asyncio event loop") from e
            raise CLIOrionisRuntimeError(f"Failed to start the scheduler: {str(e)}") from e

        except Exception as e:

            # Raise a runtime error for any other issues during startup
            raise CLIOrionisRuntimeError(f"Failed to start the scheduler: {str(e)}") from e

    async def shutdown(self, wait: bool = True) -> None:
        """
        Shut down the AsyncIO scheduler instance asynchronously.

        This method gracefully stops the AsyncIOScheduler and signals the main event loop
        to stop waiting, allowing for clean application shutdown.

        Parameters
        ----------
        wait : bool, optional
            If True, waits for currently executing jobs to complete. Default is True.

        Returns
        -------
        None

        Raises
        ------
        ValueError
            If the 'wait' parameter is not a boolean value.
        CLIOrionisRuntimeError
            If an error occurs during the shutdown process.
        """

        # Validate the wait parameter
        if not isinstance(wait, bool):
            self.__raiseException(CLIOrionisValueError("The 'wait' parameter must be a boolean value."))

        # If the scheduler is not running, there's nothing to shut down
        if not self.isRunning():
            return

        try:

            # Log the shutdown process
            self.__logger.info(f"Shutting down scheduler (wait={wait})...")

            # Shut down the AsyncIOScheduler
            self.__scheduler.shutdown(wait=wait)

            # Signal the stop event to break the wait in start()
            if self._stop_event and not self._stop_event.is_set():
                self._stop_event.set()

            # Allow time for cleanup if waiting
            if wait:
                await asyncio.sleep(0.1)

            # Log the successful shutdown
            self.__logger.info("Scheduler shutdown completed successfully.")

        except Exception as e:

            # Handle exceptions that may occur during shutdown
            self.__raiseException(CLIOrionisRuntimeError(f"Failed to shut down the scheduler: {str(e)}"))

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

        # Validate that the signature is a non-empty string
        if not isinstance(signature, str) or not signature.strip():
            self.__raiseException(CLIOrionisValueError("Signature must be a non-empty string."))

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

        # Validate that the signature is a non-empty string
        if not isinstance(signature, str) or not signature.strip():
            self.__raiseException(CLIOrionisValueError("Signature must be a non-empty string."))

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

        # Validate that the signature is a non-empty string
        if not isinstance(signature, str) or not signature.strip():
            self.__raiseException(CLIOrionisValueError("Signature must be a non-empty string."))

        try:

            # Attempt to remove the job from the scheduler using its signature
            self.__scheduler.remove_job(signature)

            # Iterate through the internal jobs list to find and remove the job
            for job in self.__jobs:
                if job.signature == signature:
                    self.__jobs.remove(job)  # Remove the job from the internal list
                    break

            # Log the successful removal of the job
            self.__logger.info(f"Job '{signature}' has been removed from the scheduler.")

            # Return True to indicate the job was successfully removed
            return True

        except Exception:

            # Return False if the job could not be removed (e.g., it does not exist)
            return False

    def events(self) -> List[Dict]:
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

            signature = job.signature
            args = job.args
            purpose = job.purpose
            random_delay = job.random_delay if job.random_delay else 0
            start_date = job.start_date.strftime('%Y-%m-%d %H:%M:%S') if job.start_date else 'Not Applicable'
            end_date = job.end_date.strftime('%Y-%m-%d %H:%M:%S') if job.end_date else 'Not Applicable'
            details = job.details if job.details else 'Not Available'

            # Append a dictionary with relevant job details to the events list
            events.append({
                'signature': signature,
                'args': args,
                'purpose': purpose,
                'random_delay': random_delay,
                'start_date': start_date,
                'end_date': end_date,
                'details': details
            })

        # Return the list of scheduled job details
        return events

    def cancelScheduledPause(self) -> bool:
        """
        Cancel a previously scheduled pause operation.

        This method attempts to remove a job from the scheduler that was set to pause
        the scheduler at a specific time. If the job exists, it is removed, and a log entry
        is created to indicate the cancellation. If no such job exists, the method returns False.

        Returns
        -------
        bool
            True if the scheduled pause job was successfully cancelled.
            False if no pause job was found or an error occurred during the cancellation process.
        """
        try:

            # Remove any listener associated with the pause event
            listener = ListeningEvent.SCHEDULER_PAUSED.value
            if listener in self.__listeners:
                del self.__listeners[listener]

            # Attempt to remove the pause job with the specific ID
            # if it exists
            try:
                self.__scheduler.remove_job("scheduler_pause_at")
            finally:
                pass

            # Log the successful cancellation of the pause operation
            self.__logger.info("Scheduled pause operation cancelled.")

            # Return True to indicate the pause job was successfully cancelled
            return True

        except:
            # Return False if the pause job does not exist or an error occurred
            return False

    def cancelScheduledResume(self) -> bool:
        """
        Cancel a previously scheduled resume operation.

        This method attempts to remove a job from the scheduler that was set to resume
        the scheduler at a specific time. If the job exists, it is removed, and a log entry
        is created to indicate the cancellation. If no such job exists, the method returns False.

        Returns
        -------
        bool
            True if the scheduled resume job was successfully cancelled.
            False if no resume job was found or an error occurred during the cancellation process.
        """
        try:

            # Remove any listener associated with the resume event
            listener = ListeningEvent.SCHEDULER_RESUMED.value
            if listener in self.__listeners:
                del self.__listeners[listener]

            # Attempt to remove the resume job with the specific ID
            # if it exists
            try:
                self.__scheduler.remove_job("scheduler_resume_at")
            finally:
                pass

            # Log the successful cancellation of the resume operation
            self.__logger.info("Scheduled resume operation cancelled.")

            # Return True to indicate the resume job was successfully cancelled
            return True

        except:

            # Return False if the resume job does not exist or an error occurred
            return False

    def cancelScheduledShutdown(self) -> bool:
        """
        Cancel a previously scheduled shutdown operation.

        This method attempts to remove a job from the scheduler that was set to shut down
        the scheduler at a specific time. If the job exists, it is removed, and a log entry
        is created to indicate the cancellation. If no such job exists, the method returns False.

        Returns
        -------
        bool
            True if the scheduled shutdown job was successfully cancelled.
            False if no shutdown job was found or an error occurred during the cancellation process.
        """
        try:

            # Remove any listener associated with the shutdown event
            listener = ListeningEvent.SCHEDULER_SHUTDOWN.value
            if listener in self.__listeners:
                del self.__listeners[listener]

            # Attempt to remove the shutdown job with the specific ID
            # if it exists
            try:
                self.__scheduler.remove_job("scheduler_shutdown_at")
            finally:
                pass

            # Log the successful cancellation of the shutdown operation
            self.__logger.info("Scheduled shutdown operation cancelled.")

            # Return True to indicate the shutdown job was successfully cancelled
            return True

        except:

            # Return False if the shutdown job does not exist or an error occurred
            return False

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

        # Return the running state of the scheduler
        return self.__scheduler.running

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

        # Check if the scheduler is currently running
        if self.__scheduler.running:
            # Shut down the scheduler immediately without waiting for jobs to complete
            self.__scheduler.shutdown(wait=False)

        # Check if the stop event exists and has not already been set
        if self._stop_event and not self._stop_event.is_set():
            # Signal the stop event to interrupt the scheduler's main loop
            self._stop_event.set()

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
        # Check if the stop event exists and has not already been set
        if self._stop_event and not self._stop_event.is_set():

            try:

                # Try to get the current running event loop
                loop = asyncio.get_running_loop()

                # If the event loop is running, set the stop event in a thread-safe manner
                loop.call_soon_threadsafe(self._stop_event.set)

            except RuntimeError:

                # No running event loop, set the stop event directly
                self._stop_event.set()

            except Exception as e:

                # Log the error but still try to set the event
                self.__logger.warning(f"Error setting stop event through event loop: {str(e)}")
                self._stop_event.set()