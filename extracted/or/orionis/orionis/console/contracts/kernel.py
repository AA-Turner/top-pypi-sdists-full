from abc import ABC, abstractmethod

class IKernelCLI(ABC):
    """
    Interface for the Kernel CLI.
    """

    @abstractmethod
    def handle(self, args: list) -> None:
        """
        Handle the command line arguments.

        :param args: List of command line arguments (e.g., sys.argv).
        """
        raise NotImplementedError("This method should be overridden by subclasses.")