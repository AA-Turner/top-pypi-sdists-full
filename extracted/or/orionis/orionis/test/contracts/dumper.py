from abc import ABC, abstractmethod

class ITestDumper(ABC):
    """
    Interface for standard output debugging utilities.

    This interface defines methods for dumping debugging information,
    capturing the caller's file, method, and line number, and utilizing
    a Debug class to output the information.

    Implementations
    --------------
    Implementations should provide mechanisms to output or log the
    provided arguments for debugging purposes.
    """

    @abstractmethod
    def dd(self, *args) -> None:
        """
        Outputs debugging information using the Debug class.

        This method captures the caller's file and line number, then
        utilizes the Debug class to display or log the provided arguments
        for debugging purposes.

        Parameters
        ----------
        *args : tuple
            Variable length argument list containing the data to be dumped.

        Returns
        -------
        None
            This method does not return any value. Its purpose is to output
            or log the debugging information.
        """
        pass

    @abstractmethod
    def dump(self, *args) -> None:
        """
        Dumps debugging information using the Debug class.

        This method captures the caller's file, method, and line number,
        and uses the Debug class to output debugging information.

        Parameters
        ----------
        *args : tuple
            Variable length argument list to be dumped.
        """
        pass