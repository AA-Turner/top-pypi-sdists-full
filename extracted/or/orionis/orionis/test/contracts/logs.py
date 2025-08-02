from abc import ABC, abstractmethod
from typing import Dict, List, Optional, Tuple

class ITestLogs(ABC):
    """
    Interface for test logs persistence using a relational database.
    """

    @abstractmethod
    def create(self, report: Dict) -> bool:
        """
        Store a new test report in the database.

        Parameters
        ----------
        report : Dict
            Must include the following keys:
            - json (str): JSON-serialized report.
            - total_tests (int)
            - passed (int)
            - failed (int)
            - errors (int)
            - skipped (int)
            - total_time (float)
            - success_rate (float)
            - timestamp (str)

        Returns
        -------
        bool
            True if the report was stored successfully.

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
        Drop the reports table, removing all test history.

        Returns
        -------
        bool
            True if the table was dropped or did not exist.

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
        first : Optional[int]
            Number of earliest reports (ascending by id).
        last : Optional[int]
            Number of latest reports (descending by id).

        Returns
        -------
        List[Tuple]
            Each tuple: (id, json, total_tests, passed, failed, errors, skipped, total_time, success_rate, timestamp)

        Raises
        ------
        OrionisTestValueError
            If both 'first' and 'last' are specified, or if either is not a positive integer.
        OrionisTestPersistenceError
            If a database error occurs.
        """
        pass
