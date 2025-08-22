from datetime import datetime
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from orionis.console.base.command import BaseCommand
from orionis.console.contracts.schedule import ISchedule
from orionis.console.exceptions import CLIOrionisRuntimeError
from orionis.container.exceptions.exception import OrionisContainerException
from orionis.foundation.contracts.application import IApplication
from orionis.foundation.exceptions.runtime import OrionisRuntimeError

class ScheduleWorkCommand(BaseCommand):
    """
    Executes the scheduled tasks defined in the application's scheduler.

    This command dynamically loads the scheduler module specified in the application's configuration,
    retrieves the `Scheduler` class and its `tasks` method, registers the scheduled tasks with the
    ISchedule service, and starts the scheduler worker. It provides user feedback via the console and
    handles errors by raising CLIOrionisRuntimeError exceptions.

    Parameters
    ----------
    orionis : IApplication
        The application instance providing configuration and service resolution.
    console : Console
        The Rich console instance used for displaying output to the user.

    Returns
    -------
    bool
        Returns True if the scheduler worker starts successfully. If an error occurs during the process,
        a CLIOrionisRuntimeError is raised.

    Raises
    ------
    CLIOrionisRuntimeError
        If the scheduler module, class, or tasks method cannot be found, or if any unexpected error occurs.
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
            Scheduler = app.getScheduler()

            # Create an instance of the ISchedule service
            schedule_serice: ISchedule = app.make(ISchedule)

            # Register scheduled tasks using the Scheduler's tasks method
            Scheduler.tasks(schedule_serice)

            # Retrieve the list of scheduled jobs/events
            list_tasks = schedule_serice.events()

            # Display a message if no scheduled jobs are found
            if not list_tasks:
                console.line()
                console.print(Panel("No scheduled jobs found.", border_style="green"))
                console.line()
                return True

            # Display a start message for the scheduler worker
            console.line()
            start_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            panel_content = Text.assemble(
                (" Orionis Scheduler Worker ", "bold white on green"),
                ("\n\n", ""),
                ("The scheduled tasks worker has started successfully.\n", "white"),
                (f"Started at: {start_time}\n", "dim"),
                ("To stop the worker, press ", "white"),
                ("Ctrl+C", "bold yellow"),
                (".", "white")
            )
            console.print(
                Panel(panel_content, border_style="green", padding=(1, 2))
            )
            console.line()

            # Start the scheduler worker asynchronously
            await schedule_serice.start()
            return True

        except Exception as e:

            # If the exception is already a CLIOrionisRuntimeError or OrionisContainerException, re-raise it
            if isinstance(e, (OrionisRuntimeError, OrionisContainerException)):
                raise

            # Raise any unexpected exceptions as CLIOrionisRuntimeError
            raise CLIOrionisRuntimeError(
                f"An unexpected error occurred while starting the scheduler worker: {e}"
            )
