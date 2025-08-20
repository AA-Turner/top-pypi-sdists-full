import os
from datetime import datetime, timedelta

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

    def __splitDirectory(
        self
    ) -> tuple[str, str, str]:
        """
        Split the original file path into directory, file name, and extension.

        This private method processes the stored file path, separating it into its
        directory path, base file name (without extension), and file extension. It
        also ensures that the directory exists, creating it if necessary.

        Returns
        -------
        tuple of str
            A tuple containing:
            - The directory path as a string.
            - The base file name (without extension) as a string.
            - The file extension (including the dot) as a string.

        Notes
        -----
        - The method handles both forward slash ('/') and backslash ('\\') as path separators.
        - If the directory does not exist, it will be created.
        """

        # Determine the path separator and split the path into components
        if '/' in self.__path:
            parts = self.__path.split('/')
        elif '\\' in self.__path:
            parts = self.__path.split('\\')
        else:
            parts = self.__path.split(os.sep)

        # Extract the base file name and its extension from the last component
        filename, ext = os.path.splitext(parts[-1])

        # Reconstruct the directory path (excluding the file name)
        path = os.path.join(*parts[:-1]) if len(parts) > 1 else ''

        # Ensure the directory exists; create it if it does not
        if not os.path.isdir(path):
            os.makedirs(path, exist_ok=True)

        # Return the directory path, file name, and extension as a tuple
        return path, filename, ext

    def __listFilesInDirectory(
        self,
        directory: str
    ) -> list[str]:
        """
        List all files in the specified directory.

        This private method retrieves all files in the given directory, returning
        their names as a list. It does not include subdirectories or hidden files.

        Parameters
        ----------
        directory : str
            The path to the directory from which to list files.

        Returns
        -------
        list of dict
            A list of dictionaries, each containing:

        Notes
        -----
        - The method does not check for file types; it returns all files regardless of extension.
        - If the directory does not exist, an empty list is returned.
        """

        # Check if the directory exists; if not, return an empty list
        if not os.path.isdir(directory):
            return []

        # List all files in the directory and return their names
        files = []
        for f in os.listdir(directory):
            if os.path.isfile(os.path.join(directory, f)):
                files.append({
                    'name': f,
                    'path': os.path.join(directory, f),
                    'size': os.path.getsize(os.path.join(directory, f)),
                    'modified': datetime.fromtimestamp(os.path.getmtime(os.path.join(directory, f)))
                })

        # Return the list of file names
        return files

    def __stack(
        self,
        path: str,
        filename: str,
        ext: str
    ) -> str:
        """
        Construct the log file path for the 'stack' channel.

        This private method generates the full file path for a log file when the
        'stack' channel is specified. It combines the provided directory path,
        base file name, and file extension to create the complete file path.

        Parameters
        ----------
        path : str
            The directory path where the log file should be stored.
        filename : str
            The base name of the log file (without extension).
        ext : str
            The file extension, including the dot (e.g., '.log').

        Returns
        -------
        str
            The full file path for the log file in the specified directory.

        Notes
        -----
        - This method does not modify or create any directories; it only constructs the path.
        - The resulting path is platform-independent.
        """

        # Join the directory path, file name, and extension to form the full file path
        return os.path.join(path, f"{filename}{ext}")

    def __hourly(
        self,
        directory: str,
        filename: str,
        ext: str
    ) -> str:
        """
        Construct the log file path for the 'hourly' channel.

        This private method generates the full file path for a log file when the
        'hourly' channel is specified. If a log file has already been created within
        the last hour, it returns its path; otherwise, it creates a new file name
        with a timestamp.

        Parameters
        ----------
        directory : str
            The directory path where the log file should be stored.
        filename : str
            The base name of the log file (without extension).
        ext : str
            The file extension, including the dot (e.g., '.log').

        Returns
        -------
        str
            The full file path for the log file in the specified directory.
        """

        now = datetime.now()
        one_hour_ago = now - timedelta(hours=1)
        files = self.__listFilesInDirectory(directory)

        # Find the most recent file created within the last hour
        recent_file = None
        for file in sorted(files, key=lambda x: x['modified'], reverse=True):
            if file['modified'] >= one_hour_ago and 'hourly' in file['name']:
                recent_file = file['path']
                break

        # If a recent file is found, return its path
        if recent_file:
            return recent_file

        # No recent file found, create a new one with timestamp
        timestamp = now.strftime("%Y%m%d_%H%M%S")

        # Ensure the filename starts with 'hourly_' if not already present
        if 'hourly' not in filename:
            filename = f"hourly_{filename}"

        # Construct the new file name with the timestamp prefix
        new_filename = f"{timestamp}_{filename}{ext}"
        return os.path.join(directory, new_filename)

    def __daily(
        self,
        directory: str,
        filename: str,
        ext: str
    ) -> str:
        """
        Construct the log file path for the 'daily' channel.

        This private method generates the full file path for a log file when the
        'daily' channel is specified. If a log file has already been created for
        the current day, it returns its path; otherwise, it creates a new file name
        with the current date and a high-resolution timestamp to ensure uniqueness.

        Parameters
        ----------
        directory : str
            The directory path where the log file should be stored.
        filename : str
            The base name of the log file (without extension).
        ext : str
            The file extension, including the dot (e.g., '.log').

        Returns
        -------
        str
            The full file path for the log file in the specified directory. If a log
            file for the current day already exists, its path is returned; otherwise,
            a new file path is generated with the current date and a unique timestamp.

        Notes
        -----
        - The method checks for existing log files for the current day and reuses them if found.
        - If no such file exists, a new file name is generated using the current date and a Unix timestamp.
        - The resulting path is platform-independent.
        """

        # Get the current date in YYYY_MM_DD format
        date = datetime.now().strftime("%Y_%m_%d")

        # List all files in the target directory
        files = self.__listFilesInDirectory(directory)

        # Search for the most recent file created today
        recent_file = None
        for file in sorted(files, key=lambda x: x['modified'], reverse=True):
            if str(file['name']).startswith(date) and 'daily' in file['name']:
                recent_file = file['path']
                break

        # If a file for today exists, return its path
        if recent_file:
            return recent_file

        # Prefix the filename with 'daily_' if not already present
        if 'daily' not in filename:
            filename = f"daily_{filename}"

        # Generate a unique filename using the current date and Unix timestamp
        unix_time = int(datetime.now().timestamp())
        new_filename = f"{date}_{unix_time}_{filename}{ext}"
        return os.path.join(directory, new_filename)

    def __weekly(
        self,
        directory: str,
        filename: str,
        ext: str
    ) -> str:
        """
        Construct the log file path for the 'weekly' channel.

        This private method generates the full file path for a log file when the
        'weekly' channel is specified. If a log file has already been created for
        the current week, it returns its path; otherwise, it creates a new file name
        with the current year, ISO week number, and a Unix timestamp to ensure uniqueness.

        Parameters
        ----------
        directory : str
            The directory path where the log file should be stored.
        filename : str
            The base name of the log file (without extension).
        ext : str
            The file extension, including the dot (e.g., '.log').

        Returns
        -------
        str
            The full file path for the log file in the specified directory. If a log
            file for the current week already exists, its path is returned; otherwise,
            a new file path is generated using the current year, ISO week number, and a unique timestamp.

        Notes
        -----
        - The method checks for existing log files for the current week and reuses them if found.
        - If no such file exists, a new file name is generated using the current year, ISO week number, and Unix timestamp.
        - The resulting path is platform-independent.
        """

        # Get the current week number and year using ISO calendar
        now = datetime.now()
        year, week_num, _ = now.isocalendar()
        week = f"{year}_W{week_num:02d}"

        # List all files in the target directory
        files = self.__listFilesInDirectory(directory)

        # Search for the most recent file created this week with 'weekly' in its name
        recent_file = None
        for file in sorted(files, key=lambda x: x['modified'], reverse=True):
            if str(file['name']).startswith(week) and 'weekly' in file['name']:
                recent_file = file['path']
                break

        # If a file for this week exists, return its path
        if recent_file:
            return recent_file

        # Prefix the filename with 'weekly_' if not already present
        if 'weekly' not in filename:
            filename = f"weekly_{filename}"

        # Generate a unique filename using the current year, week, and Unix timestamp
        unix_time = int(datetime.now().timestamp())
        new_filename = f"{week}_{unix_time}_{filename}{ext}"

        # Return the full path to the new weekly log file
        return os.path.join(directory, new_filename)

    def __monthly(
        self,
        directory: str,
        filename: str,
        ext: str
    ) -> str:
        """
        Construct the log file path for the 'monthly' channel.

        This private method generates the full file path for a log file when the
        'monthly' channel is specified. If a log file has already been created for
        the current month, it returns its path; otherwise, it creates a new file name
        with the current year, month, and a Unix timestamp to ensure uniqueness.

        Parameters
        ----------
        directory : str
            The directory path where the log file should be stored.
        filename : str
            The base name of the log file (without extension).
        ext : str
            The file extension, including the dot (e.g., '.log').

        Returns
        -------
        str
            The full file path for the log file in the specified directory. If a log
            file for the current month already exists, its path is returned; otherwise,
            a new file path is generated using the current year, month, and a unique timestamp.

        Notes
        -----
        - The method checks for existing log files for the current month and reuses them if found.
        - If no such file exists, a new file name is generated using the current year, month, and Unix timestamp.
        - The resulting path is platform-independent.
        """

        # Get the current year and month
        now = datetime.now()
        year = now.year
        month = now.month
        month_str = f"{year}_M{month:02d}"

        # List all files in the target directory
        files = self.__listFilesInDirectory(directory)

        # Search for the most recent file created this month with 'monthly' in its name
        recent_file = None
        for file in sorted(files, key=lambda x: x['modified'], reverse=True):
            if str(file['name']).startswith(month_str) and 'monthly' in file['name']:
                recent_file = file['path']
                break

        # If a file for this month exists, return its path
        if recent_file:
            return recent_file

        # Prefix the filename with 'monthly_' if not already present
        if 'monthly' not in filename:
            filename = f"monthly_{filename}"

        # Generate a unique filename using the current year, month, and Unix timestamp
        unix_time = int(datetime.now().timestamp())
        new_filename = f"{month_str}_{unix_time}_{filename}{ext}"

        # Return the full path to the new monthly log file
        return os.path.join(directory, new_filename)

    def __chunked(
        self,
        directory: str,
        filename: str,
        ext: str,
        max_bytes: int = 5242880
    ) -> str:
        """
        Construct the log file path for the 'chunked' channel.

        This private method generates the full file path for a log file when the
        'chunked' channel is specified. It checks for the most recent log file
        in the specified directory with 'chunked' in its name and a size less than
        the specified maximum number of bytes. If such a file exists, its path is
        returned. Otherwise, a new file name is generated using the current Unix
        timestamp and the 'chunked_' prefix.

        Parameters
        ----------
        directory : str
            The directory path where the log file should be stored.
        filename : str
            The base name of the log file (without extension).
        ext : str
            The file extension, including the dot (e.g., '.log').
        max_bytes : int, optional
            The maximum allowed size in bytes for a chunked log file. Default is 5 MB (5242880 bytes).

        Returns
        -------
        str
            The full file path for the chunked log file in the specified directory.
            If a suitable file exists (with 'chunked' in its name and size less than
            `max_bytes`), its path is returned. Otherwise, a new file path is generated
            with a unique timestamp and returned.

        Notes
        -----
        - The method checks for existing chunked log files and reuses them if their size
          is below the specified threshold.
        - If no such file exists, a new file name is generated using the current Unix timestamp.
        - The resulting path is platform-independent.
        """

        # List all files in the target directory
        files = self.__listFilesInDirectory(directory)

        # Search for the most recent file with 'chunked' in its name and size less than max_bytes
        recent_file = None
        for file in sorted(files, key=lambda x: x['modified'], reverse=True):
            if 'chunked' in file['name'] and file['size'] < max_bytes:
                recent_file = file['path']
                break

        # If a suitable chunked file exists, return its path
        if recent_file:
            return recent_file

        # Prefix the filename with 'chunked_' if not already present
        if 'chunked' not in filename:
            filename = f"chunked_{filename}"

        # Generate a unique filename using the current Unix timestamp
        unix_time = int(datetime.now().timestamp())
        new_filename = f"{unix_time}_{filename}{ext}"

        # Return the full path to the new chunked log file
        return os.path.join(directory, new_filename)

    def generate(self, channel: str, max_bytes: int = 5242880) -> str:
        """
        Generate the appropriate log file path based on the specified channel.

        This method determines the log file naming strategy according to the given
        channel type. It delegates the file path construction to the corresponding
        private method for each channel. For the 'chunked' channel, the maximum
        allowed file size can be specified.

        Parameters
        ----------
        channel : str
            The log channel type. Supported values are:
            'stack', 'hourly', 'daily', 'weekly', 'monthly', 'chunked'.
        max_bytes : int, optional
            The maximum allowed size in bytes for a chunked log file. Only used
            when `channel` is 'chunked'. Default is 5 MB (5242880 bytes).

        Returns
        -------
        str
            The full file path for the log file according to the specified channel.

        Raises
        ------
        ValueError
            If the provided channel is not supported.

        Notes
        -----
        - The method uses the original file path provided during initialization.
        - For all channels except 'chunked', `max_bytes` is ignored.
        - The resulting file path is platform-independent.
        """

        # Select the appropriate file path generation strategy based on the channel
        if channel == 'stack':
            return self.__stack(*self.__splitDirectory())
        elif channel == 'hourly':
            return self.__hourly(*self.__splitDirectory())
        elif channel == 'daily':
            return self.__daily(*self.__splitDirectory())
        elif channel == 'weekly':
            return self.__weekly(*self.__splitDirectory())
        elif channel == 'monthly':
            return self.__monthly(*self.__splitDirectory())
        elif channel == 'chunked':
            return self.__chunked(*self.__splitDirectory(), max_bytes=max_bytes)
        else:
            raise ValueError(
                f"Unknown channel: {channel}. Supported channels are: "
                "'stack', 'hourly', 'daily', 'weekly', 'monthly', 'chunked'."
            )