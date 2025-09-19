from orionis.console.base.command import BaseCommand
from orionis.console.contracts.reactor import IReactor
from orionis.console.exceptions import CLIOrionisRuntimeError
from rich.console import Console
from rich.panel import Panel

class WorkFlowGithubCommand(BaseCommand):
    """
    Runs the test suite and displays the results in the Orionis CLI workflow.

    This command executes the project's test suite using the provided reactor. If any tests fail or errors occur,
    it displays a summary panel and prevents further workflow actions by raising an exception.

    Attributes
    ----------
    timestamps : bool
        Indicates whether timestamps will be shown in the command output.
    signature : str
        Command signature for invocation.
    description : str
        Brief description of the command's purpose.
    """

    # Indicates whether timestamps will be shown in the command output
    timestamps: bool = False

    # Command signature and description
    signature: str = "__workflow__"

    # Command description
    description: str = "Displays usage information, examples, and a list of available commands in the Orionis CLI."

    def handle(self, reactor: IReactor) -> None:
        """
        Displays usage information and a list of available commands for the Orionis CLI.

        Parameters
        ----------
        reactor : IReactor
            The reactor instance providing command metadata via the `info()` method.

        Returns
        -------
        None
            This method does not return any value. It prints help information to the console.

        Raises
        ------
        CLIOrionisRuntimeError
            If an unexpected error occurs during help information generation or display.
        """
        try:

            # Execute  test suite
            response: dict = reactor.call("test")

            # Determinar si existieron errores en el test suite
            failed = response.get("failed", 0)
            errors = response.get("errors", 0)

            # If there are any failed tests, print a warning message
            if failed > 0 or errors > 0:
                console = Console()
                console.print(
                    Panel(
                        f"Tests failed: {failed}, Errors: {errors}",
                        title="Test Suite Results",
                        style="bold red"
                    )
                )

                # If there are failed tests, we do not proceed with the publishing
                raise CLIOrionisRuntimeError(
                    "Test suite failed. Please fix the issues before proceeding with the workflow."
                )

        except Exception as e:

            # Raise a custom runtime error if any exception occurs
            raise CLIOrionisRuntimeError(f"An unexpected error occurred: {e}") from e
