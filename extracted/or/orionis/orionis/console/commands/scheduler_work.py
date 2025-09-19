from rich.console import Console
from rich.panel import Panel
from orionis.console.base.command import BaseCommand
from orionis.console.contracts.schedule import ISchedule
from orionis.console.enums.listener import ListeningEvent
from orionis.console.exceptions import CLIOrionisRuntimeError
from orionis.foundation.contracts.application import IApplication
from orionis.services.introspection.instances.reflection import ReflectionInstance

class ScheduleWorkCommand(BaseCommand):
    """
    Runs the application's scheduled tasks worker.

    This command initializes and starts the scheduler worker, which executes all tasks registered in the application's scheduler. It ensures the scheduler is properly configured, registers event listeners if available, and provides feedback to the user via the console. Errors during initialization or execution are reported as CLIOrionisRuntimeError.

    Attributes
    ----------
    timestamps : bool
        Indicates whether timestamps will be shown in the command output.
    signature : str
        Command signature for invocation.
    description : str
        Brief description of the command.

    Returns
    -------
    bool
        True if the scheduler worker starts successfully.

    Raises
    ------
    CLIOrionisRuntimeError
        If the scheduler is not properly defined or an unexpected error occurs.
    """

    # Indicates whether timestamps will be shown in the command output
    timestamps: bool = False

    # Command signature and description
    signature: str = "schedule:work"

    # Command description
    description: str = "Executes the scheduled tasks defined in the application."

    async def handle(self, app: IApplication, console: Console) -> bool:
        """
        Executes the scheduled tasks defined in the application's scheduler.

        This method retrieves the Scheduler instance from the application, registers scheduled tasks
        with the ISchedule service, and starts the scheduler worker asynchronously. It provides user
        feedback via the console and handles errors by raising CLIOrionisRuntimeError exceptions.

        Parameters
        ----------
        app : IApplication
            The application instance providing configuration and service resolution.
        console : Console
            The Rich console instance used for displaying output to the user.

        Returns
        -------
        bool
            True if the scheduler worker starts successfully.

        Raises
        ------
        CLIOrionisRuntimeError
            If the scheduler module, class, or tasks method cannot be found, or if any unexpected error occurs.
        """
        try:

            # Retrieve the Scheduler instance from the application
            scheduler = app.getScheduler()

            # Create an instance of ReflectionInstance
            rf_scheduler = ReflectionInstance(scheduler)

            # If the Scheduler class does not define the 'tasks' method, raise an error
            if not rf_scheduler.hasMethod("tasks"):
                raise CLIOrionisRuntimeError(
                    "The 'tasks' method was not found in the Scheduler class. "
                    "Please ensure your Scheduler class defines a 'tasks(self, schedule: ISchedule)' method "
                    "to register scheduled tasks."
                )

            # Create an instance of the ISchedule service
            schedule_service: ISchedule = app.make(ISchedule)

            # Register scheduled tasks using the Scheduler's tasks method
            app.call(scheduler, 'tasks', schedule_service)

            # Retrieve the list of scheduled jobs/events
            list_tasks = schedule_service.events()

            # Display a message if no scheduled jobs are found
            if not list_tasks:

                # Print a message indicating no scheduled jobs are found
                console.line()
                console.print(Panel("No scheduled jobs found.", border_style="green"))
                console.line()

                # Return True indicating the command completed successfully
                return True

            # If there are scheduled jobs and the scheduler has an onStarted method
            if rf_scheduler.hasMethod("onStarted"):
                schedule_service.setListener(ListeningEvent.SCHEDULER_STARTED, scheduler.onStarted)

            # If the scheduler has an onPaused method
            if rf_scheduler.hasMethod("onPaused"):
                schedule_service.setListener(ListeningEvent.SCHEDULER_PAUSED, scheduler.onPaused)

            # If the scheduler has an onResumed method
            if rf_scheduler.hasMethod("onResumed"):
                schedule_service.setListener(ListeningEvent.SCHEDULER_RESUMED, scheduler.onResumed)

            # If the scheduler has an onFinalized method
            if rf_scheduler.hasMethod("onFinalized"):
                schedule_service.setListener(ListeningEvent.SCHEDULER_SHUTDOWN, scheduler.onFinalized)

            # If the scheduler has an onError method
            if rf_scheduler.hasMethod("onError"):
                schedule_service.setListener(ListeningEvent.SCHEDULER_ERROR, scheduler.onError)

            # Start the scheduler worker asynchronously
            await schedule_service.start()

            # Flag to indicate the scheduler is running
            return True

        except Exception as e:

            # Raise any unexpected exceptions as CLIOrionisRuntimeError
            raise CLIOrionisRuntimeError(
                f"An unexpected error occurred while starting the scheduler worker: {e}"
            )