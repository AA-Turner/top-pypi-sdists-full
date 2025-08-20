import importlib
import os
from pathlib import Path
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from orionis.console.base.command import BaseCommand
from orionis.console.contracts.schedule import ISchedule
from orionis.console.exceptions import CLIOrionisRuntimeError
from orionis.foundation.contracts.application import IApplication

class ScheduleListCommand(BaseCommand):
    """
    Command class to display usage information for the Orionis CLI.

    Methods
    -------
    handle(orionis: IApplication, console: Console) -> bool
        Displays a table of scheduled tasks defined in the application.
        Imports the scheduler module, retrieves scheduled jobs, and prints them
        in a formatted table using the rich library.

    Returns
    -------
    bool
        Returns True if the scheduled jobs are listed successfully or if no jobs are found.
        Raises CLIOrionisRuntimeError if an error occurs during execution.
    """

    # Indicates whether timestamps will be shown in the command output
    timestamps: bool = False

    # Command signature and description
    signature: str = "schedule:list"

    # Command description
    description: str = "Executes the scheduled tasks defined in the application."

    def handle(self, orionis: IApplication, console: Console) -> bool:
        """
        Displays a table of scheduled jobs defined in the application.

        This method dynamically imports the scheduler module, retrieves the list of
        scheduled jobs using the ISchedule service, and prints the jobs in a formatted
        table. If no jobs are found, a message is displayed. Handles and reports errors
        encountered during the process.

        Parameters
        ----------
        orionis : IApplication
            The application instance providing configuration and service resolution.
        console : Console
            The rich Console instance used for output.

        Returns
        -------
        bool
            Returns True if the scheduled jobs are listed successfully or if no jobs are found.
            Raises CLIOrionisRuntimeError if an error occurs during execution.
        """

        try:

            # Get the absolute path of the scheduler from the application configuration
            scheduler_path = orionis.path('console_scheduler')

            # Get the base path from the current working directory
            base_path = Path(os.getcwd()).resolve()
            scheduler_path = Path(scheduler_path).resolve()
            rel_path = scheduler_path.relative_to(base_path)

            # Convert the path to a module name (replace separators with dots, remove .py)
            module_name = ".".join(rel_path.with_suffix('').parts)

            # Dynamically import the scheduler module
            scheduler_module = importlib.import_module(module_name)

            # Retrieve the Scheduler class from the imported module
            Scheduler = getattr(scheduler_module, "Scheduler", None)

            # Raise an error if the Scheduler class is not found
            if Scheduler is None:
                raise CLIOrionisRuntimeError(f"Scheduler class not found in module {module_name}")

            # Retrieve the 'tasks' method from the Scheduler class
            task_method = getattr(Scheduler, "tasks", None)

            # Raise an error if the 'tasks' method is not found
            if task_method is None:
                raise CLIOrionisRuntimeError(f"Method 'tasks' not found in Scheduler class in module {module_name}")

            # Create an instance of ISchedule using the application container
            schedule_serice: ISchedule = orionis.make(ISchedule)

            # Initialize the scheduled tasks by calling the 'tasks' method
            task_method(schedule_serice)

            # Retrieve the list of scheduled jobs/events
            list_tasks = schedule_serice.events()

            # Display a message if no scheduled jobs are found
            if not list_tasks:
                console.line()
                console.print(Panel("No scheduled jobs found.", border_style="green"))
                console.line()
                return True

            # Create and configure a table to display scheduled jobs
            table = Table(title="Scheduled Jobs", show_lines=True)
            table.add_column("Signature", style="cyan", no_wrap=True)
            table.add_column("Arguments", style="magenta")
            table.add_column("Purpose", style="green")
            table.add_column("Random Delay", style="yellow")
            table.add_column("Start Date", style="white")
            table.add_column("End Date", style="white")
            table.add_column("Details", style="dim")

            # Populate the table with job details
            for job in list_tasks:
                signature = str(job.get("signature", ""))
                args = ", ".join(map(str, job.get("args", [])))
                purpose = str(job.get("purpose", ""))
                random_delay = str(job.get("random_delay", ""))
                start_date = str(job.get("start_date", "")) if job.get("start_date") else "-"
                end_date = str(job.get("end_date", "")) if job.get("end_date") else "-"
                details = str(job.get("details", ""))

                table.add_row(signature, args, purpose, random_delay, start_date, end_date, details)

            # Print the table to the console
            console.line()
            console.print(table)
            console.line()
            return True

        except Exception as exc:

            # Catch any unexpected exceptions and raise as a CLIOrionisRuntimeError
            raise CLIOrionisRuntimeError(f"An unexpected error occurred while clearing the cache: {exc}")
