from abc import ABC, abstractmethod

class IKernelCLI(ABC):
    """
    Abstract base class for the Kernel Command Line Interface (CLI).

    This interface defines the contract for handling command line arguments
    within the kernel's CLI component.
    """

    @abstractmethod
    def handle(self, args: list) -> None:
        """
        Process the provided command line arguments.

        Parameters
        ----------
        args : list
            List of command line arguments, typically obtained from sys.argv.

        Raises
        ------
        NotImplementedError
            If the method is not implemented by a subclass.
        """

        # This method must be implemented by subclasses.
        raise NotImplementedError("This method should be overridden by subclasses.")