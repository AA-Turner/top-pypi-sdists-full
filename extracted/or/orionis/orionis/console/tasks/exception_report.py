from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.traceback import Traceback

class ScheduleErrorReporter:
    """Handles and displays errors and warnings with rich formatting using the Rich library.

    This class provides methods to output formatted error and warning messages to the console,
    enhancing readability and debugging using the Rich library's features.

    Attributes
    ----------
    console : Console
        Rich Console object used for rendering formatted output to the terminal.
    """

    def __init__(self):
        """
        Initialize the ErrorReporter instance.

        This constructor creates a new Console object from the Rich library and assigns it to the 'console' attribute,
        which is used for rendering formatted output to the terminal.

        Returns
        -------
        None
            This constructor does not return any value.
        """
        self.console = Console()

    def reportException(self, job_id: str, exception: Exception, traceback: str = None):
        """
        Display a formatted error message for an exception that occurred during a job execution.

        This method prints a visually enhanced error panel to the console, including the job identifier and the exception message.
        If a traceback string is provided, it is rendered below the error panel for detailed debugging information.

        Parameters
        ----------
        job_id : str
            The identifier of the job where the exception occurred.
        exception : Exception
            The exception instance that was raised.
        traceback : str, optional
            The string representation of the traceback. If provided, it will be displayed after the error message.

        Returns
        -------
        None
            This method does not return any value. It outputs formatted error information to the console.
        """
        title = f"[bold red]Job Execution Error[/bold red]"
        message = Text.assemble(
            ("An exception occurred during the execution of job ", "white"),
            (f"'{job_id}'", "bold cyan"),
            (":\n", "white"),
            (f"{type(exception).__name__}: {exception}", "red")
        )

        self.console.print(Panel(message, title=title, border_style="red", padding=(1, 2)))
        if traceback:
            tb = Traceback.from_string(traceback)
            self.console.print(tb)
        self.console.line()


    def reportMissed(self, job_id: str, scheduled_time):
        """
        Display a formatted warning message for a missed job execution.

        This method prints a warning panel to the console, indicating that a scheduled job was missed and showing its scheduled time.

        Parameters
        ----------
        job_id : str
            The identifier of the missed job.
        scheduled_time : Any
            The time the job was scheduled to run.

        Returns
        -------
        None
            This method does not return any value. It outputs a warning message to the console.
        """
        title = f"[bold yellow]Missed Scheduled Job[/bold yellow]"
        msg = Text.assemble(
            ("The scheduled job ", "white"),
            (f"'{job_id}'", "bold cyan"),
            (" was not executed as planned.\nScheduled time: ", "white"),
            (f"{scheduled_time}", "bold green")
        )
        self.console.print(Panel(msg, title=title, border_style="yellow", padding=(1, 2)))
        self.console.line()
