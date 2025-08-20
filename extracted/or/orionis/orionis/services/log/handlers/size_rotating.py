from logging.handlers import RotatingFileHandler
from orionis.services.log.handlers.filename import FileNameLogger

class PrefixedSizeRotatingFileHandler(RotatingFileHandler):

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
            in the format 'YYYYMMDD_HHMMSS'. This ensures uniqueness and chronological ordering
            of rotated log files.

        Notes
        -----
        This method utilizes the FileNameLogger class to construct the prefixed filename.
        The timestamp prefix helps in identifying the creation time of each rotated log file.
        """

        # Import Application to access configuration settings
        from orionis.support.facades.application import Application

        # Generate the new filename using FileNameLogger, which adds a timestamp prefix.
        return FileNameLogger(default_name).generate('chunked', Application.config('logging.channels.chunked.mb_size', 5))