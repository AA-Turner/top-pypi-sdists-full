from logging.handlers import TimedRotatingFileHandler
from orionis.services.log.handlers.filename import FileNameLogger

class PrefixedTimedRotatingFileHandler(TimedRotatingFileHandler):

    def rotation_filename(self, default_name) -> str:
        """
        Generates a rotated log filename by prefixing the original filename with a timestamp.

        Parameters
        ----------
        default_name : str
            The original file path that is subject to rotation.

        Returns
        -------
        str
            The new file path as a string, where the base name is prefixed with a timestamp
            in the format 'YYYYMMDD_HHMMSS'. This ensures each rotated log file is uniquely
            identified by its creation time.

        Notes
        -----
        This method utilizes the FileNameLogger class to construct the new filename.
        The timestamp prefix helps in organizing and distinguishing rotated log files.
        """

        # Use FileNameLogger to generate a new filename with a timestamp prefix
        return FileNameLogger(default_name).generate()