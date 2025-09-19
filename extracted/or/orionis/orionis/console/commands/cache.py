import subprocess
from orionis.console.base.command import BaseCommand
from orionis.console.exceptions import CLIOrionisRuntimeError

class CacheClearCommand(BaseCommand):
    """
    Command to clear Python bytecode cache files (.pyc) and __pycache__ directories in the Orionis application.

    This command helps maintain a clean development environment by removing all Python cache artifacts
    from the current working directory, preventing issues related to stale or invalid bytecode.

    Attributes
    ----------
    timestamps : bool
        Whether to display timestamps in the command output.
    signature : str
        The CLI signature to invoke this command.
    description : str
        A brief summary of the command's functionality.

    Methods
    -------
    handle() -> bool
        Executes the cache clearing process using the `pyclean .` utility. Returns True if successful,
        otherwise raises CLIOrionisRuntimeError on failure.
    """

    # Indicates whether timestamps will be shown in the command output
    timestamps: bool = True

    # Command signature and description
    signature: str = "cache:clear"

    # Command description
    description: str = "Clears the cache for the Orionis application."

    def handle(self) -> bool:
        """
        Clears all `.pyc` files and `__pycache__` directories in the current directory using the `pyclean` utility.

        This method invokes the `pyclean .` command to recursively remove Python bytecode cache files and directories,
        helping to ensure a clean state for the Orionis application. If the command fails or an unexpected error occurs,
        a `CLIOrionisRuntimeError` is raised with the relevant error message.

        Returns
        -------
        bool
            Returns True if the cache was cleared successfully. Raises an exception otherwise.

        Raises
        ------
        CLIOrionisRuntimeError
            If the cache clearing process fails or an unexpected error occurs.
        """

        try:

            # Run the 'pyclean .' command to remove .pyc files and __pycache__ directories
            process = subprocess.run(['pyclean', '.'], capture_output=True, text=True)
            if process.returncode != 0:

                # If the command failed, extract the error message and raise a custom exception
                error_message = process.stderr.strip() or "Unknown error occurred."
                raise CLIOrionisRuntimeError(f"Cache clearing failed: {error_message}")

            # If the command was successful, print the output
            self.textSuccess("Cache cleared successfully.")

            # If the command was successful, return True
            return True  # Cache cleared successfully

        except Exception as exc:

            # Catch any unexpected exceptions and raise as a CLIOrionisRuntimeError
            raise CLIOrionisRuntimeError(f"An unexpected error occurred while clearing the cache: {exc}")
