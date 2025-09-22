from typing import List
from orionis.console.args.argument import CLIArgument
from orionis.console.base.command import BaseCommand
from orionis.console.exceptions import CLIOrionisRuntimeError
from rich.console import Console
from rich.panel import Panel
from orionis.metadata import framework

class VersionCommand(BaseCommand):
    """
    Displays the current version and metadata of the Orionis framework.

    This command outputs the framework's version, author, Python requirements, documentation, and repository links
    in a formatted panel for the user.

    Attributes
    ----------
    timestamps : bool
        Indicates whether timestamps will be shown in the command output.
    signature : str
        Command signature used to invoke this command ("version").
    description : str
        Description of the command's purpose.
    """

    # Indicates whether timestamps will be shown in the command output
    timestamps: bool = False

    # Command signature and description
    signature: str = "version"

    # Command description
    description: str = "Displays the current Orionis framework version and metadata, including author, Python requirements, documentation, and repository links."

    async def options(self) -> List[CLIArgument]:
        """
        Defines the command-line options available for the `make:command` command.

        This method specifies the arguments that can be passed to the command when it is invoked
        from the CLI. It includes both required and optional arguments, each represented as a
        `CLIArgument` instance.

        Returns
        -------
        List[CLIArgument]
            A list of `CLIArgument` objects representing the available command-line options.
        """

        return [
            CLIArgument(
                flags=["--without-console"],
                type=bool,
                help="Return only the version string, without console output.",
                required=False
            )
        ]

    def handle(self, console: Console) -> str:
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
        str
            The current version of the Orionis framework.

        Raises
        ------
        CLIOrionisRuntimeError
            If an unexpected error occurs during execution, a CLIOrionisRuntimeError is raised
            with the original exception message.
        """
        try:

            # If the --without-console flag is set, return just the version string
            if self.argument("without_console", False):
                return framework.VERSION

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

            # Return the framework version for potential further use
            return framework.VERSION

        except Exception as e:

            # Raise a custom runtime error if any exception occurs
            raise CLIOrionisRuntimeError(f"An unexpected error occurred: {e}") from e
