from abc import ABC, abstractmethod
from orionis.test.contracts.unit_test import IUnitTest

class ITestKernel(ABC):
    """
    Abstract interface for test kernel implementations.

    This contract defines the required methods that any test kernel implementation
    must provide for the Orionis testing framework. It ensures consistent behavior
    across different test kernel implementations.

    The test kernel is responsible for:
    - Managing application context for testing
    - Validating and handling test configuration
    - Orchestrating test discovery and execution
    - Providing a unified interface for test operations
    """

    @abstractmethod
    def handle(self) -> IUnitTest:
        """
        Configure and execute the unit tests based on the current configuration.

        Returns
        -------
        IUnitTest
            The configured and executed unit test instance.
        """
        pass
