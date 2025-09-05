from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any, Dict, List, Optional
from orionis.foundation.config.testing.enums import ExecutionMode
from orionis.foundation.config.testing.enums.drivers import PersistentDrivers
from orionis.foundation.config.testing.enums.verbosity import VerbosityMode

class IUnitTest(ABC):

    @abstractmethod
    def run(self) -> Dict[str, Any]:
        """
        Execute all discovered tests.

        Returns
        -------
        dict
            Results of the test execution.
        """
        pass

    @abstractmethod
    def getTestNames(self) -> List[str]:
        """
        Retrieve the list of discovered test names.

        Returns
        -------
        list of str
            Names of all discovered tests.
        """
        pass

    @abstractmethod
    def getTestCount(self) -> int:
        """
        Get the total number of discovered tests.

        Returns
        -------
        int
            Number of discovered tests.
        """
        pass

    @abstractmethod
    def clearTests(self) -> None:
        """
        Remove all discovered tests from the runner.
        """
        pass

    @abstractmethod
    def getResult(self) -> dict:
        """
        Retrieve the results of the last test run.

        Returns
        -------
        dict
            Results of the last test execution.
        """
        pass

    @abstractmethod
    def getOutputBuffer(self) -> int:
        """
        Get the size or identifier of the output buffer.

        Returns
        -------
        int
            Output buffer size or identifier.
        """
        pass

    @abstractmethod
    def printOutputBuffer(self) -> None:
        """
        Print the contents of the output buffer to the console.
        """
        pass

    @abstractmethod
    def getErrorBuffer(self) -> int:
        """
        Get the size or identifier of the error buffer.

        Returns
        -------
        int
            Error buffer size or identifier.
        """
        pass

    @abstractmethod
    def printErrorBuffer(self) -> None:
        """
        Print the contents of the error buffer to the console.
        """
        pass