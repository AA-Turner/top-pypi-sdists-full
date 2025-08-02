from abc import ABC, abstractmethod

class ILoggerService(ABC):

    @abstractmethod
    def info(self, message: str) -> None:
        """
        Logs an informational message.

        Parameters
        ----------
        message : str
            The message to be logged as informational.

        Returns
        -------
        None
            This method does not return any value.
        """
        # To be implemented by subclasses
        pass

    @abstractmethod
    def error(self, message: str) -> None:
        """
        Logs an error message.

        Parameters
        ----------
        message : str
            The message to be logged as an error.

        Returns
        -------
        None
            This method does not return any value.
        """
        # To be implemented by subclasses
        pass

    @abstractmethod
    def warning(self, message: str) -> None:
        """
        Logs a warning message.

        Parameters
        ----------
        message : str
            The message to be logged as a warning.

        Returns
        -------
        None
            This method does not return any value.
        """
        # To be implemented by subclasses
        pass

    @abstractmethod
    def debug(self, message: str) -> None:
        """
        Logs a debug message.

        Parameters
        ----------
        message : str
            The message to be logged for debugging purposes.

        Returns
        -------
        None
            This method does not return any value.
        """
        # To be implemented by subclasses
        pass