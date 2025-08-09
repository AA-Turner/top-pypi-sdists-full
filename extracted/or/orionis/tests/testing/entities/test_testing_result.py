from orionis.test.cases.asynchronous import AsyncTestCase
from orionis.test.entities.result import TestResult
from orionis.test.enums import TestStatus

class TestTestingResult(AsyncTestCase):

    async def testDefaultValues(self) -> None:
        """
        Test that optional fields in TestResult are set to None by default.

        Checks that the fields `error_message`, `traceback`, `class_name`, `method`, `module`, and `file_path`
        are None when not provided during initialization.

        Parameters
        ----------
        self : TestTestingResult
            The test case instance.

        Returns
        -------
        None
        """
        # Create a TestResult instance with only required fields
        result = TestResult(
            id=1,
            name="Sample Test",
            status=TestStatus.PASSED,
            execution_time=0.5
        )
        # Assert that all optional fields are set to None by default
        self.assertIsNone(result.error_message)
        self.assertIsNone(result.traceback)
        self.assertIsNone(result.class_name)
        self.assertIsNone(result.method)
        self.assertIsNone(result.module)
        self.assertIsNone(result.file_path)

    async def testRequiredFields(self) -> None:
        """
        Test that TestResult enforces required fields during initialization.

        Verifies that omitting required fields raises a TypeError.

        Parameters
        ----------
        self : TestTestingResult
            The test case instance.

        Returns
        -------
        None
        """
        # Attempt to create TestResult with no arguments; should raise TypeError
        with self.assertRaises(TypeError):
            TestResult()  # Missing all required fields

        # Attempt to create TestResult missing the 'id' field; should raise TypeError
        with self.assertRaises(TypeError):
            TestResult(
                name="Sample Test",
                status=TestStatus.PASSED,
                execution_time=0.5
            )

    async def testImmutable(self) -> None:
        """
        Test that TestResult instances are immutable.

        Ensures that modifying an attribute of a TestResult instance raises an exception.

        Parameters
        ----------
        self : TestTestingResult
            The test case instance.

        Returns
        -------
        None
        """
        # Create a TestResult instance
        result = TestResult(
            id=1,
            name="Sample Test",
            status=TestStatus.PASSED,
            execution_time=0.5
        )
        # Attempt to modify an attribute; should raise an exception due to immutability
        with self.assertRaises(Exception):
            result.name = "Modified Name"

    async def testStatusValues(self) -> None:
        """
        Test that all TestStatus enum values can be assigned to TestResult.

        Iterates through each TestStatus value and checks assignment to the status field.

        Parameters
        ----------
        self : TestTestingResult
            The test case instance.

        Returns
        -------
        None
        """
        # Iterate through all possible TestStatus values
        for status in TestStatus:
            # Create a TestResult instance with the current status
            result = TestResult(
                id=1,
                name="Status Test",
                status=status,
                execution_time=0.1
            )
            # Assert that the status field matches the assigned value
            self.assertEqual(result.status, status)

    async def testErrorFields(self) -> None:
        """
        Test that error_message and traceback fields are stored correctly in TestResult.

        Verifies that providing values for error_message and traceback sets them as expected.

        Parameters
        ----------
        self : TestTestingResult
            The test case instance.

        Returns
        -------
        None
        """
        error_msg = "Test failed"
        traceback = "Traceback info"
        # Create a TestResult instance with error fields
        result = TestResult(
            id=1,
            name="Failing Test",
            status=TestStatus.FAILED,
            execution_time=0.2,
            error_message=error_msg,
            traceback=traceback
        )
        # Assert that error_message and traceback fields are set correctly
        self.assertEqual(result.error_message, error_msg)
        self.assertEqual(result.traceback, traceback)
