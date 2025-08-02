from enum import Enum
from orionis.test.cases.asynchronous import AsyncTestCase
from orionis.test.enums.status import TestStatus

class TestTestStatus(AsyncTestCase):

    async def testHasEnumMembers(self):
        """
        Checks that the TestStatus enum contains the expected members.

        This test verifies the presence of the following enum members:
        'PASSED', 'FAILED', 'ERRORED', and 'SKIPPED'.

        Returns
        -------
        None
            This method does not return a value. It asserts the existence of enum members.
        """
        # Assert that each expected member exists in TestStatus
        self.assertTrue(hasattr(TestStatus, "PASSED"))
        self.assertTrue(hasattr(TestStatus, "FAILED"))
        self.assertTrue(hasattr(TestStatus, "ERRORED"))
        self.assertTrue(hasattr(TestStatus, "SKIPPED"))

    async def testEnumValuesAreUnique(self):
        """
        Ensures that all TestStatus enum member values are unique.

        This test collects all values from the TestStatus enum and checks for uniqueness.

        Returns
        -------
        None
            This method does not return a value. It asserts the uniqueness of enum values.
        """
        # Gather all enum values
        values = [status.value for status in TestStatus]
        # Assert that the number of values equals the number of unique values
        self.assertEqual(len(values), len(set(values)))

    async def testEnumIsInstanceOfEnum(self):
        """
        Validates that TestStatus is a subclass of Enum.

        This test checks the inheritance of TestStatus from the Enum base class.

        Returns
        -------
        None
            This method does not return a value. It asserts the subclass relationship.
        """
        # Assert that TestStatus inherits from Enum
        self.assertTrue(issubclass(TestStatus, Enum))

    async def testEnumMembersType(self):
        """
        Confirms that each member of TestStatus is an instance of TestStatus.

        This test iterates through all members of TestStatus and checks their type.

        Returns
        -------
        None
            This method does not return a value. It asserts the type of each enum member.
        """
        # Assert that each enum member is an instance of TestStatus
        for status in TestStatus:
            self.assertIsInstance(status, TestStatus)
