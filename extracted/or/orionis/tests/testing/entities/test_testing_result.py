from orionis.test.cases.asynchronous import AsyncTestCase
from orionis.test.entities.result import TestResult
from orionis.test.enums import TestStatus

class TestTestingResult(AsyncTestCase):

    async def testDefaultValues(self) -> None:
        """
        Ensures that optional fields in a TestResult instance are set to None when not provided during initialization.

        This test checks the default behavior for the following optional fields:
            - error_message
            - traceback
            - class_name
            - method
            - module
            - file_path

        The method asserts that each of these fields is None after instantiating TestResult with only required arguments.

        Parameters
        ----------
        self : TestTestingResult
            The test case instance.

        Returns
        -------
        None
            This method does not return any value. It performs assertions to validate default field values.

        Notes
        -----
        This test verifies that the TestResult dataclass correctly initializes optional fields to None when they are omitted.
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
        Validates that TestResult enforces the presence of all required fields during initialization.

        This test attempts to instantiate TestResult without required fields and expects a TypeError to be raised.

        Parameters
        ----------
        self : TestTestingResult
            The test case instance.

        Returns
        -------
        None
            This method does not return any value. It performs assertions to validate required field enforcement.

        Notes
        -----
        - Attempts to instantiate TestResult with no arguments.
        - Attempts to instantiate TestResult missing the 'id' field.
        - Expects a TypeError to be raised in both cases.
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
        Tests the immutability of TestResult instances.

        Ensures that TestResult, implemented as a frozen dataclass, does not allow modification of its attributes after instantiation.

        Parameters
        ----------
        self : TestTestingResult
            The test case instance.

        Returns
        -------
        None
            This method does not return any value. It performs assertions to validate immutability.

        Raises
        ------
        Exception
            If an attempt is made to modify an attribute of a frozen TestResult instance.

        Notes
        -----
        Attempts to modify the 'name' attribute of a TestResult instance and expects an exception to be raised.
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
        Verifies that all possible values of the TestStatus enum can be assigned to the status field of a TestResult instance.

        Iterates over each TestStatus value, assigns it to a TestResult, and asserts that the status is set correctly.

        Parameters
        ----------
        self : TestTestingResult
            The test case instance.

        Returns
        -------
        None
            This method does not return any value. It performs assertions to validate status assignment.

        Notes
        -----
        This test ensures that the status field in TestResult supports all enum values defined in TestStatus.
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
        Verifies that the error_message and traceback fields are correctly stored in the TestResult object when provided.

        This test initializes a TestResult with error_message and traceback values and asserts that they are set as expected.

        Parameters
        ----------
        self : TestTestingResult
            The test case instance.

        Returns
        -------
        None
            This method does not return any value. It performs assertions to validate error field assignment.

        Notes
        -----
        This test ensures that error-related fields are properly assigned and retrievable from the TestResult instance.
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