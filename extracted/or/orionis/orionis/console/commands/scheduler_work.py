import importlib
import os
from datetime import datetime
from pathlib import Path
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from orionis.console.base.command import BaseCommand
from orionis.console.contracts.schedule import ISchedule
from orionis.console.exceptions import CLIOrionisRuntimeError
from orionis.foundation.contracts.application import IApplication

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

    async def handle(self, orionis: IApplication, console: Console) -> bool:
        """
        Executes the scheduled tasks defined in the application's scheduler.

        This method dynamically loads the scheduler module specified in the application's configuration,
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
        try:
            # Get the absolute path to the scheduler module from the application configuration
            scheduler_path = orionis.path('console_scheduler')

            # Resolve the base path (current working directory)
            base_path = Path(os.getcwd()).resolve()
            scheduler_path = Path(scheduler_path).resolve()

            # Compute the relative path from the base path to the scheduler module
            rel_path = scheduler_path.relative_to(base_path)

            # Convert the relative path to a Python module name (dot notation, no .py extension)
            module_name = ".".join(rel_path.with_suffix('').parts)

            # Dynamically import the scheduler module
            scheduler_module = importlib.import_module(module_name)

            # Retrieve the Scheduler class from the imported module
            Scheduler = getattr(scheduler_module, "Scheduler", None)
            if Scheduler is None:
                raise CLIOrionisRuntimeError(f"Scheduler class not found in module {module_name}")

            # Create an instance of the Scheduler class
            Scheduler = Scheduler()

            # Retrieve the 'tasks' method from the Scheduler class
            task_method = getattr(Scheduler, "tasks", None)
            if task_method is None:
                raise CLIOrionisRuntimeError(f"Method 'tasks' not found in Scheduler class in module {module_name}")

            # Create an instance of the ISchedule service
            schedule_serice: ISchedule = orionis.make(ISchedule)

            # Register scheduled tasks using the Scheduler's tasks method
            task_method(schedule_serice)

            # Register event listeners for the scheduler
            onSchedulerStarted = getattr(Scheduler, "onSchedulerStarted", None)
            if onSchedulerStarted:
                schedule_serice.addListenerOnSchedulerStarted(onSchedulerStarted)

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

        except Exception as exc:
            # Raise any unexpected exceptions as CLIOrionisRuntimeError
            raise CLIOrionisRuntimeError(f"An unexpected error occurred while clearing the cache: {exc}")
