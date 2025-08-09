from abc import ABC, abstractmethod
from orionis.test.contracts.unit_test import IUnitTest

class ITestKernel(ABC):
    """
    Interface for test kernel implementations in the Orionis testing framework.

    The test kernel manages the application context, validates and handles test configuration,
    orchestrates test discovery and execution, and provides a unified interface for test operations.
    """

    @abstractmethod
    def handle(self) -> IUnitTest:
        """
        Configure and execute unit tests according to the current configuration.

        Returns
        -------
        IUnitTest
            An instance representing the configured and executed unit test.
        """
        pass
