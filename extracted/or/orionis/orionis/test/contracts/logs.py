from abc import ABC, abstractmethod
from typing import Dict, List, Optional, Tuple

class ITestLogs(ABC):
    """
    Abstract interface for persisting and retrieving test logs in a relational database.
    """

    @abstractmethod
    def create(self, report: Dict) -> bool:
        """
        Store a new test report in the database.

        Parameters
        ----------
        report : dict
            Dictionary containing the test report data. Required keys:
            'json' (str), 'total_tests' (int), 'passed' (int), 'failed' (int),
            'errors' (int), 'skipped' (int), 'total_time' (float),
            'success_rate' (float), 'timestamp' (str).

        Returns
        -------
        bool
            True if the report was stored successfully, otherwise False.

        Raises
        ------
        OrionisTestValueError
            If required fields are missing or invalid.
        OrionisTestPersistenceError
            If a database error occurs.
        """
        pass

    @abstractmethod
    def reset(self) -> bool:
        """
        Remove all test reports from the database.

        Returns
        -------
        bool
            True if the reports table was dropped or did not exist.

        Raises
        ------
        OrionisTestPersistenceError
            If a database error occurs.
        """
        pass

    @abstractmethod
    def get(
        self,
        first: Optional[int] = None,
        last: Optional[int] = None
    ) -> List[Tuple]:
        """
        Retrieve test reports from the database.

        Parameters
        ----------
        first : int, optional
            Number of earliest reports to retrieve, ordered by ascending ID.
        last : int, optional
            Number of latest reports to retrieve, ordered by descending ID.

        Returns
        -------
        list of tuple
            Each tuple contains:
            (id, json, total_tests, passed, failed, errors, skipped, total_time, success_rate, timestamp).

        Raises
        ------
        OrionisTestValueError
            If both 'first' and 'last' are specified, or if either is not a positive integer.
        OrionisTestPersistenceError
            If a database error occurs.
        """
        pass
