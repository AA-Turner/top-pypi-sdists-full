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
        Executes the version command to display the current Orionis framework version.

        This method retrieves the version number from the framework metadata and prints it
        in a formatted, bold, and successful style to the console. If an unexpected error occurs
        during execution, it raises a CLIOrionisRuntimeError with the original exception message.

        Parameters
        ----------
        None

        Returns
        -------
        None
            This method does not return any value. It outputs the version information to the console.

        Raises
        ------
        CLIOrionisRuntimeError
            If an unexpected error occurs during execution, a CLIOrionisRuntimeError is raised
            with the original exception message.
        """

        # Print the Orionis framework version in a bold, success style
        try:
            self.textSuccessBold(f"Orionis Framework v{VERSION}")

        # Raise a custom runtime error if any exception occurs
        except Exception as e:
            raise CLIOrionisRuntimeError(f"An unexpected error occurred: {e}") from e
