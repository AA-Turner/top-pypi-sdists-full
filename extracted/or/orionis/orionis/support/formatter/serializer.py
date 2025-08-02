from orionis.support.formatter.exceptions.parser import ExceptionParser

class Parser:

    @staticmethod
    def exception(exception: Exception) -> ExceptionParser:
        """
        Creates and returns an ExceptionParser instance for the given exception.
        Args:
            exception (Exception): The exception to be parsed.
        Returns:
            ExceptionParser: An instance of ExceptionParser initialized with the provided exception.
        """

        return ExceptionParser(exception)