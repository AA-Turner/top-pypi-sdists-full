from abc import ABC, abstractmethod

class ITestDumper(ABC):
    """
    Abstract base class for debugging output utilities.

    This interface specifies methods for outputting debugging information,
    capturing the caller's file, method, and line number, and utilizing a
    Debug class to display or log the information.
    """

    @abstractmethod
    def dd(self, *args) -> None:
        """
        Output debugging information using the Debug class.

        Captures the caller's file and line number, then uses the Debug class
        to display or log the provided arguments for debugging purposes.

        Parameters
        ----------
        *args : tuple
            Variable length argument list containing the data to be output.

        Returns
        -------
        None
        """
        pass

    @abstractmethod
    def dump(self, *args) -> None:
        """
        Output debugging information using the Debug class.

        Captures the caller's file, method, and line number, and uses the
        Debug class to output the provided arguments for debugging purposes.

        Parameters
        ----------
        *args : tuple
            Variable length argument list containing the data to be output.

        Returns
        -------
        None
        """
        pass
