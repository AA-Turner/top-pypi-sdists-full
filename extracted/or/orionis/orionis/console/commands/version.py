from orionis.console.base.command import BaseCommand
from orionis.console.exceptions import CLIOrionisRuntimeError
from rich.console import Console
from rich.panel import Panel
from orionis.metadata import framework

class VersionCommand(BaseCommand):
    """
    VersionCommand is a console command that displays the current version and metadata of the Orionis framework.

    Attributes
    ----------
    timestamps : bool
        Indicates whether timestamps should be included (default: False).
    signature : str
        The command signature used to invoke this command ("version").
    description : str
        A brief description of what the command does.
    """

    # Indicates whether timestamps will be shown in the command output
    timestamps: bool = False

    # Command signature and description
    signature: str = "version"

    # Command description
    description: str = "Displays the current Orionis framework version and metadata, including author, Python requirements, documentation, and repository links."

    def handle(self) -> None:
        """
        Executes the version command to display the current Orionis framework version and metadata.

        This method retrieves the version number and additional metadata from the framework module,
        then prints it in a formatted, styled panel to the console. If an unexpected error occurs
        during execution, it raises a CLIOrionisRuntimeError with the original exception message.

        Parameters
        ----------
        None

        Returns
        -------
        None
            This method does not return any value. It outputs the version and metadata information
            to the console using rich formatting.

        Raises
        ------
        CLIOrionisRuntimeError
            If an unexpected error occurs during execution, a CLIOrionisRuntimeError is raised
            with the original exception message.
        """
        try:
            # Initialize the console for rich output
            console = Console()

            # Compose the main information strings using framework metadata
            title = f"[bold yellow]{framework.NAME.capitalize()} Framework[/bold yellow] [white]v{framework.VERSION}[/white]"
            author = f"[bold]Author:[/bold] {framework.AUTHOR}  |  [bold]Email:[/bold] {framework.AUTHOR_EMAIL}"
            desc = f"[italic]{framework.DESCRIPTION}[/italic]"
            python_req = f"[bold]Python Requires:[/bold] {framework.PYTHON_REQUIRES}"
            docs = f"[bold]Docs:[/bold] [underline blue]{framework.DOCS}[/underline blue]"
            repo = f"[bold]Repo:[/bold] [underline blue]{framework.FRAMEWORK}[/underline blue]"

            # Combine all information into the panel body
            body = "\n".join([desc, "", author, python_req, docs, repo, ""])

            # Create a styled panel with the collected information
            panel = Panel(
                body,
                title=title,
                border_style="bold yellow",
                padding=(1, 6),
                expand=False,
                subtitle="[bold yellow]Orionis CLI[/bold yellow]",
                subtitle_align="right"
            )

            # Print a blank line, the panel, and another blank line for spacing
            console.line()
            console.print(panel)
            console.line()

        except Exception as e:
            # Raise a custom runtime error if any exception occurs
            raise CLIOrionisRuntimeError(f"An unexpected error occurred: {e}") from e
