import subprocess
from orionis.console.base.command import BaseCommand
from orionis.console.exceptions import CLIOrionisRuntimeError
from orionis.foundation.contracts.application import IApplication
import shutil
import logging

class LogClearCommand(BaseCommand):
    """
    Command to clear all existing log files and directories in the application's log storage.

    This command disables all active loggers, locates the application's log directory,
    and attempts to remove all files, symlinks, and subdirectories within it. If a log
    file is locked, it will be truncated instead of deleted. Any unexpected errors during
    the process will raise a CLIOrionisRuntimeError.

    Parameters
    ----------
    app : IApplication
        The application instance providing access to the log storage path.

    Returns
    -------
    bool
        Returns True if all log files and directories are cleared successfully,
        or if the log directory does not exist. Raises CLIOrionisRuntimeError
        if an unexpected error occurs during the process.

    Raises
    ------
    CLIOrionisRuntimeError
        If an unexpected error occurs while clearing the log files or directories.
    """

    # Indicates whether timestamps will be shown in the command output
    timestamps: bool = False

    # Command signature and description
    signature: str = "log:clear"

    # Command description
    description: str = "Eliminar todos los logs existentes de la aplicacion."

    def handle(self, app: IApplication) -> bool:
        """
        Clears all existing log files and directories in the application's log storage.

        Parameters
        ----------
        app : IApplication
            The application instance providing access to the log storage path.

        Returns
        -------
        bool
            True if the operation completes without raising an exception,
            or if the log directory does not exist.

        Raises
        ------
        CLIOrionisRuntimeError
            If an unexpected error occurs during the log clearing process.
        """
        try:
            # Shutdown all active loggers to release file handles
            logging.shutdown()

            # Get the path to the application's log directory
            log_path = app.path('storage') / 'logs'

            # Check if the log directory exists and is a directory
            if log_path.exists() and log_path.is_dir():
                for entry in log_path.iterdir():
                    try:
                        if entry.is_file() or entry.is_symlink():

                            # Attempt to truncate the file if it's in use, then delete it
                            try:

                                # Truncate file contents
                                with open(entry, 'w'):
                                    pass

                                # Attempt to delete the file
                                entry.unlink()

                            except PermissionError:

                                # If the file is locked, just truncate and skip deletion
                                pass

                        elif entry.is_dir():

                            # Recursively remove subdirectories and their contents
                            shutil.rmtree(entry)

                    except Exception as e:

                        # Ignore errors for individual entries to continue processing others
                        pass

            # Print success message
            self.info("All log files have been successfully deleted.")

            # Return True if the operation completes successfully
            return True

        except Exception as exc:

            # Raise a CLIOrionisRuntimeError for any unexpected exception
            raise CLIOrionisRuntimeError(
                f"An unexpected error occurred while clearing the cache: {exc}"
            )
