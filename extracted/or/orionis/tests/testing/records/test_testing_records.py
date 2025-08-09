import json
import tempfile
from orionis.test.cases.asynchronous import AsyncTestCase
from orionis.test.exceptions import OrionisTestValueError
from orionis.test.records.logs import TestLogs

class TestTestingRecords(AsyncTestCase):

    async def testCreateAndGetReport(self):
        """
        Test the creation and retrieval of a test report.

        Creates a test report with all required fields, stores it using the
        TestLogs class, and retrieves the most recent report to verify its
        contents.

        Returns
        -------
        None
        """
        with tempfile.TemporaryDirectory() as tmpdir:
            logs = TestLogs(tmpdir)

            # Prepare a complete test report dictionary
            report = {
                "total_tests": 5,
                "passed": 4,
                "failed": 1,
                "errors": 0,
                "skipped": 0,
                "total_time": 1.23,
                "success_rate": 0.8,
                "timestamp": "2024-06-01T12:00:00"
            }

            # Serialize the report to JSON and add to the dictionary
            report["json"] = json.dumps(report)

            # Store the report in the logs
            result = logs.create(report)
            self.assertTrue(result)

            # Retrieve the most recent report
            reports = logs.get(first=1)
            self.assertEqual(len(reports), 1)

            # Validate the contents of the retrieved report
            self.assertEqual(json.loads(reports[0][1])["total_tests"], 5)

    async def testCreateMissingFields(self):
        """
        Test error handling for missing required fields in report creation.

        Attempts to create a report without the required 'timestamp' field and
        expects an OrionisTestValueError to be raised.

        Returns
        -------
        None
        """
        with tempfile.TemporaryDirectory() as tmpdir:
            logs = TestLogs(tmpdir)

            # Prepare a report missing the 'timestamp' field
            report = {
                "total_tests": 5,
                "passed": 4,
                "failed": 1,
                "errors": 0,
                "skipped": 0,
                "total_time": 1.23,
                "success_rate": 0.8,
            }
            report["json"] = json.dumps(report)

            # Expect an error when creating the report
            with self.assertRaises(OrionisTestValueError):
                logs.create(report)

    async def testResetDatabase(self):
        """
        Test the reset functionality of the test logs database.

        Creates a report, stores it, and then resets the logs database.
        Verifies that the reset operation returns True.

        Returns
        -------
        None
        """
        with tempfile.TemporaryDirectory() as tmpdir:
            logs = TestLogs(tmpdir)

            # Create and store a single report
            report = {
                "total_tests": 1,
                "passed": 1,
                "failed": 0,
                "errors": 0,
                "skipped": 0,
                "total_time": 0.1,
                "success_rate": 1.0,
                "timestamp": "2024-06-01T12:00:00"
            }
            report["json"] = json.dumps(report)
            logs.create(report)

            # Reset the logs database and verify success
            self.assertTrue(logs.reset())

    async def testGetReportsInvalidParams(self):
        """
        Test error handling for invalid parameters in TestLogs.get().

        Checks that passing mutually exclusive or invalid values to get()
        raises an OrionisTestValueError.

        Returns
        -------
        None
        """
        with tempfile.TemporaryDirectory() as tmpdir:
            logs = TestLogs(tmpdir)

            # Both 'first' and 'last' should not be provided together
            with self.assertRaises(OrionisTestValueError):
                logs.get(first=1, last=1)

            # 'first' must be greater than zero
            with self.assertRaises(OrionisTestValueError):
                logs.get(first=0)

            # 'last' must be greater than zero
            with self.assertRaises(OrionisTestValueError):
                logs.get(last=-1)

    async def testGetLastReports(self):
        """
        Test retrieval of the last N reports and their order.

        Creates multiple reports, retrieves the last two, and checks that the
        reports are returned in descending order by their identifier.

        Returns
        -------
        None
        """
        with tempfile.TemporaryDirectory() as tmpdir:
            logs = TestLogs(tmpdir)

            # Create and store three reports with increasing 'total_tests'
            for i in range(3):
                report = {
                    "total_tests": i+1,
                    "passed": i,
                    "failed": 1,
                    "errors": 0,
                    "skipped": 0,
                    "total_time": 0.1 * (i+1),
                    "success_rate": 0.5,
                    "timestamp": f"2024-06-01T12:00:0{i}"
                }
                report["json"] = json.dumps(report)
                logs.create(report)

            # Retrieve the last two reports
            reports = logs.get(last=2)
            self.assertEqual(len(reports), 2)

            # Ensure the reports are ordered by descending identifier
            self.assertTrue(reports[0][0] > reports[1][0])
