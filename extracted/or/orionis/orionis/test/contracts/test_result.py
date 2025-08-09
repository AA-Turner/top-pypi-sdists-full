import unittest
from abc import ABC, abstractmethod
from typing import List, Dict, Optional, Tuple
from orionis.test.entities.result import TestResult

class IOrionisTestResult(ABC):
    """
    Interface for a custom test result collector that extends unittest's TextTestResult,
    providing detailed execution metadata for each test case.

    This interface defines properties and methods for capturing test outcomes,
    execution times, error tracebacks, and related metadata for each test case.
    """

    @property
    @abstractmethod
    def test_results(self) -> List[TestResult]:
        """
        List of detailed results for each executed test case.

        Returns
        -------
        List[TestResult]
            Each element contains metadata such as status, execution time, method name,
            module, file, and optional error information.
        """
        pass

    @property
    @abstractmethod
    def _test_timings(self) -> Dict[unittest.case.TestCase, float]:
        """
        Mapping of test cases to their execution durations in seconds.

        Returns
        -------
        Dict[unittest.case.TestCase, float]
            Keys are test case instances, values are elapsed times in seconds.
        """
        pass

    @property
    @abstractmethod
    def _current_test_start(self) -> Optional[float]:
        """
        Timestamp marking the start of the currently running test.

        Returns
        -------
        Optional[float]
            Start time in seconds, or None if no test is running.
        """
        pass

    @abstractmethod
    def startTest(self, test: unittest.case.TestCase) -> None:
        """
        Record the start time for a test case before execution.

        Parameters
        ----------
        test : unittest.case.TestCase
            The test case about to be executed.
        """
        pass

    @abstractmethod
    def stopTest(self, test: unittest.case.TestCase) -> None:
        """
        Calculate and store the execution time for a test case after execution.

        Parameters
        ----------
        test : unittest.case.TestCase
            The test case that has finished execution.
        """
        pass

    @abstractmethod
    def addSuccess(self, test: unittest.case.TestCase) -> None:
        """
        Append a successful test result to the results list.

        Parameters
        ----------
        test : unittest.case.TestCase
            The test case that completed successfully.
        """
        pass

    @abstractmethod
    def addFailure(self, test: unittest.case.TestCase, err: Tuple[BaseException, BaseException, object]) -> None:
        """
        Append a failed test result, including traceback and error message.

        Parameters
        ----------
        test : unittest.case.TestCase
            The test case that failed.
        err : tuple
            Tuple containing exception type, exception instance, and traceback object.
        """
        pass

    @abstractmethod
    def addError(self, test: unittest.case.TestCase, err: Tuple[BaseException, BaseException, object]) -> None:
        """
        Append an errored test result, including traceback and error message.

        Parameters
        ----------
        test : unittest.case.TestCase
            The test case that encountered an error.
        err : tuple
            Tuple containing exception type, exception instance, and traceback object.
        """
        pass

    @abstractmethod
    def addSkip(self, test: unittest.case.TestCase, reason: str) -> None:
        """
        Append a skipped test result with the provided reason.

        Parameters
        ----------
        test : unittest.case.TestCase
            The test case that was skipped.
        reason : str
            Reason for skipping the test.
        """
        pass
