from abc import ABC, abstractmethod
from typing import Any, Dict
from orionis.test.entities.result import TestResult

class ITestPrinter(ABC):

    @abstractmethod
    def print(
        self,
        value: Any
    ) -> None:
        """
        Print a value to the console using the rich console.

        Parameters
        ----------
        value : Any
            The value to be printed to the console.
        """
        pass

    @abstractmethod
    def startMessage(
        self,
        *,
        length_tests: int,
        execution_mode: str,
        max_workers: int
    ):
        """
        Display a formatted start message for the test execution session.

        Parameters
        ----------
        length_tests : int
            The total number of tests to be executed.
        execution_mode : str
            The mode in which the tests will be executed.
        max_workers : int
            The maximum number of worker threads or processes.
        """
        pass

    @abstractmethod
    def finishMessage(
        self,
        *,
        summary: Dict[str, Any]
    ) -> None:
        """
        Display a summary message for the test suite execution.

        Parameters
        ----------
        summary : dict of str to Any
            A dictionary containing summary information about the test execution.
        """
        pass

    @abstractmethod
    def executePanel(
        self,
        *,
        flatten_test_suite: list,
        callable: callable
    ):
        """
        Execute a test suite panel with optional live console output.

        Parameters
        ----------
        flatten_test_suite : list
            A flattened list representing the test suite to be executed.
        callable : callable
            A callable object to execute each test.
        """
        pass

    @abstractmethod
    def linkWebReport(
        self,
        path: str
    ):
        """
        Print an invitation to view the test results, with an underlined path.

        Parameters
        ----------
        path : str
            The file system or web path to the test results report.
        """
        pass

    @abstractmethod
    def summaryTable(
        self,
        summary: Dict[str, Any]
    ) -> None:
        """
        Print a summary table of test results using the Rich library.

        Parameters
        ----------
        summary : dict of str to Any
            A dictionary containing summary statistics of the test results.
        """
        pass

    @abstractmethod
    def displayResults(
        self,
        *,
        summary: Dict[str, Any]
    ) -> None:
        """
        Display the results of the test execution, including a summary table and details.

        Parameters
        ----------
        summary : dict of str to Any
            A dictionary containing the results and summary of the test execution.
        """
        pass

    @abstractmethod
    def unittestResult(
        self,
        test_result: TestResult
    ) -> None:
        """
        Display the result of a single unit test in a formatted manner.

        Parameters
        ----------
        test_result : TestResult
            The result object of a single unit test.
        """
        pass
