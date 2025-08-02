import unittest
from abc import ABC, abstractmethod
from typing import List, Dict, Optional, Tuple
from orionis.test.entities.result import TestResult

class IOrionisTestResult(ABC):
    """
    Interface for OrionisTestResult, a custom test result collector that extends
    unittest's TextTestResult to include rich execution metadata such as
    execution time, error tracebacks, and reflection-based information.

    Classes implementing this interface are responsible for capturing detailed
    information about each test case execution, including success, failure,
    error, and skip states.
    """

    @property
    @abstractmethod
    def test_results(self) -> List[TestResult]:
        """
        A list containing the detailed results of each executed test case.

        Each entry is an instance of `TestResult`, storing metadata such as
        status, execution time, method name, module, file, and optional error info.
        """
        pass

    @property
    @abstractmethod
    def _test_timings(self) -> Dict[unittest.case.TestCase, float]:
        """
        Internal mapping from each test case to its execution duration in seconds.
        Used to compute elapsed time between `startTest()` and `stopTest()`.
        """
        pass

    @property
    @abstractmethod
    def _current_test_start(self) -> Optional[float]:
        """
        Timestamp (in seconds) marking the beginning of the currently running test.
        Used internally to calculate duration.
        """
        pass

    @abstractmethod
    def startTest(self, test: unittest.case.TestCase) -> None:
        """
        Called before the test is run.

        Records the current start time for the test case in `_current_test_start`.
        """
        pass

    @abstractmethod
    def stopTest(self, test: unittest.case.TestCase) -> None:
        """
        Called after the test has run.

        Calculates and stores the execution time for the test in `_test_timings`.
        """
        pass

    @abstractmethod
    def addSuccess(self, test: unittest.case.TestCase) -> None:
        """
        Called when a test case completes successfully.

        Appends a `TestResult` instance with status `PASSED` to `test_results`.
        """
        pass

    @abstractmethod
    def addFailure(self, test: unittest.case.TestCase, err: Tuple[BaseException, BaseException, object]) -> None:
        """
        Called when a test case fails due to an assertion failure.

        Captures and appends a `TestResult` instance with status `FAILED`, along
        with traceback and error message.
        """
        pass

    @abstractmethod
    def addError(self, test: unittest.case.TestCase, err: Tuple[BaseException, BaseException, object]) -> None:
        """
        Called when a test case encounters an unexpected error or exception.

        Captures and appends a `TestResult` instance with status `ERRORED`, along
        with traceback and error message.
        """
        pass

    @abstractmethod
    def addSkip(self, test: unittest.case.TestCase, reason: str) -> None:
        """
        Called when a test case is skipped.

        Appends a `TestResult` instance with status `SKIPPED` and reason to `test_results`.
        """
        pass
