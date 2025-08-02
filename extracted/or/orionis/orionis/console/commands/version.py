from orionis.console.base.command import BaseCommand
from orionis.console.exceptions import CLIOrionisRuntimeError
from orionis.metadata.framework import VERSION

class VersionCommand(BaseCommand):
    """
    Command class to display the current version of the Orionis framework.

    This command prints the version number of the framework in use.
    """

    signature: str = "version"

    description: str = "Prints the version of the framework in use."

    def handle(self) -> None:
        """
        Execute the version command.

        This method retrieves and prints the version of the Orionis framework.

        Raises
        ------
        ValueError
            If an unexpected error occurs during execution, a ValueError is raised
            with the original exception message.
        """
        try:
            self.textSuccessBold(f"Orionis Framework v{VERSION}")
        except Exception as e:
            raise CLIOrionisRuntimeError(f"An unexpected error occurred: {e}") from e
