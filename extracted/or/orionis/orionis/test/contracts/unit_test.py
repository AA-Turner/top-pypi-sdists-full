from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any, Dict, List, Optional
from orionis.foundation.config.testing.enums import ExecutionMode
from orionis.foundation.config.testing.enums.drivers import PersistentDrivers
from orionis.foundation.config.testing.enums.verbosity import VerbosityMode

class IUnitTest(ABC):

    @abstractmethod
    def configure(
        self,
        *,
        verbosity: int | VerbosityMode,
        execution_mode: str | ExecutionMode,
        max_workers: int,
        fail_fast: bool,
        print_result: bool,
        throw_exception: bool,
        persistent: bool,
        persistent_driver: str | PersistentDrivers,
        web_report: bool
    ) -> 'IUnitTest':
        """
        Configure the unit test runner with the provided options.

        Parameters
        ----------
        verbosity : int or VerbosityMode
            Verbosity level for test output.
        execution_mode : str or ExecutionMode
            Execution mode for running tests.
        max_workers : int
            Maximum number of worker threads or processes.
        fail_fast : bool
            Whether to stop on the first test failure.
        print_result : bool
            Whether to print test results to the console.
        throw_exception : bool
            Whether to raise exceptions on test failures.
        persistent : bool
            Whether to enable persistent storage for test results.
        persistent_driver : str or PersistentDrivers
            Persistent storage driver to use.
        web_report : bool
            Whether to generate a web-based test report.

        Returns
        -------
        IUnitTest
            The configured unit test runner instance.
        """
        pass

    @abstractmethod
    def discoverTestsInFolder(
        self,
        *,
        base_path: str | Path,
        folder_path: str,
        pattern: str,
        test_name_pattern: Optional[str] = None,
        tags: Optional[List[str]] = None
    ) -> 'IUnitTest':
        """
        Discover test cases within a specified folder.

        Parameters
        ----------
        base_path : str or Path
            Base directory for test discovery.
        folder_path : str
            Path to the folder containing test files.
        pattern : str
            File pattern to match test files.
        test_name_pattern : str, optional
            Pattern to match test function or class names.
        tags : list of str, optional
            Tags to filter discovered tests.

        Returns
        -------
        IUnitTest
            The unit test runner instance with discovered tests.
        """
        pass

    @abstractmethod
    def discoverTestsInModule(
        self,
        *,
        module_name: str,
        test_name_pattern: Optional[str] = None
    ) -> 'IUnitTest':
        """
        Discover test cases within a specified module.

        Parameters
        ----------
        module_name : str
            Name of the module to search for tests.
        test_name_pattern : str, optional
            Pattern to match test function or class names.

        Returns
        -------
        IUnitTest
            The unit test runner instance with discovered tests.
        """
        pass

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