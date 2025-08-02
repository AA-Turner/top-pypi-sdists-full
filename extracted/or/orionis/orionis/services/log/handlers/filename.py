import os
from datetime import datetime
from pathlib import Path

class FileNameLogger:

    def __init__(self, path: str) -> None:
        """
        Initialize the FileNameLogger.

        Parameters
        ----------
        path : str
            The original file path for the log file.

        Raises
        ------
        ValueError
            If the provided path is not a non-empty string.
        """
        # Validate that the path is a non-empty string
        if not isinstance(path, str) or not path:
            raise ValueError("The 'path' parameter must be a non-empty string.")

        # Store the stripped path as a private instance variable
        self.__path = path.strip()

    def generate(self) -> str:
        """
        Generate a new log file path with a timestamp prefix.

        The method constructs a new file path by prefixing the original file name
        with a timestamp in the format 'YYYYMMDD_HHMMSS'. It also ensures that the
        directory for the log file exists, creating it if necessary.

        Returns
        -------
        str
            The full path to the log file with a timestamped file name.

        Notes
        -----
        - The timestamp is generated using the current date and time.
        - The directory for the log file is created if it does not exist.
        """
        # Split the original path into components based on the separator
        if '/' in self.__path:
            parts = self.__path.split('/')
        elif '\\' in self.__path:
            parts = self.__path.split('\\')
        else:
            parts = self.__path.split(os.sep)

        # Extract the base file name and its extension
        filename, ext = os.path.splitext(parts[-1])

        # Reconstruct the directory path (excluding the file name)
        path = os.path.join(*parts[:-1]) if len(parts) > 1 else ''

        # Generate a timestamp prefix for the file name
        prefix = datetime.now().strftime("%Y%m%d_%H%M%S")

        # Build the full file path with the timestamped file name
        full_path = os.path.join(path, f"{prefix}_{filename}{ext}")

        # Ensure the log directory exists; create it if it does not
        log_dir = Path(full_path).parent
        if not log_dir.exists():
            log_dir.mkdir(parents=True, exist_ok=True)

        # Return the full path to the timestamped log file
        return full_path