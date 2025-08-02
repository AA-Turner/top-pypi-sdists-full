from abc import ABC, abstractmethod
from typing import Any, Dict
from orionis.test.entities.result import TestResult

class ITestPrinter(ABC):

    @abstractmethod
    def print(
        self,
        value: Any
    ) -> None:
        """Prints a value to the console using the rich console."""
        pass

    @abstractmethod
    def startMessage(
        self,
        *,
        length_tests: int,
        execution_mode: str,
        max_workers: int
    ):
        """Displays a formatted start message for the test execution session."""
        pass

    @abstractmethod
    def finishMessage(
        self,
        *,
        summary: Dict[str, Any]
    ) -> None:
        """Display a summary message for the test suite execution."""
        pass

    @abstractmethod
    def executePanel(
        self,
        *,
        flatten_test_suite: list,
        callable: callable
    ):
        """Executes a test suite panel with optional live console output."""
        pass

    @abstractmethod
    def linkWebReport(
        self,
        path: str
    ):
        """Prints an invitation to view the test results, with an underlined path."""
        pass

    @abstractmethod
    def summaryTable(
        self,
        summary: Dict[str, Any]
    ) -> None:
        """Prints a summary table of test results using the Rich library."""
        pass

    @abstractmethod
    def displayResults(
        self,
        *,
        summary: Dict[str, Any]
    ) -> None:
        """Display the results of the test execution, including a summary table and details."""
        pass

    @abstractmethod
    def unittestResult(
        self,
        test_result: TestResult
    ) -> None:
        """Display the result of a single unit test in a formatted manner."""
        pass
