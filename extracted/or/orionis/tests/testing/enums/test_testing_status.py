from enum import Enum
from orionis.test.cases.asynchronous import AsyncTestCase
from orionis.test.enums.status import TestStatus

class TestTestStatus(AsyncTestCase):

    async def testHasEnumMembers(self):
        """
        Test that the TestStatus enum contains the expected members.

        Checks for the presence of the 'PASSED', 'FAILED', 'ERRORED', and 'SKIPPED' members in the TestStatus enum.

        Returns
        -------
        None
        """
        # Assert that each expected member exists in TestStatus
        self.assertTrue(hasattr(TestStatus, "PASSED"))
        self.assertTrue(hasattr(TestStatus, "FAILED"))
        self.assertTrue(hasattr(TestStatus, "ERRORED"))
        self.assertTrue(hasattr(TestStatus, "SKIPPED"))

    async def testEnumValuesAreUnique(self):
        """
        Test that all TestStatus enum member values are unique.

        Collects all values from the TestStatus enum and asserts that there are no duplicate values.

        Returns
        -------
        None
        """
        # Gather all enum values
        values = [status.value for status in TestStatus]
        # Assert that the number of values equals the number of unique values
        self.assertEqual(len(values), len(set(values)))

    async def testEnumIsInstanceOfEnum(self):
        """
        Test that TestStatus is a subclass of Enum.

        Asserts that TestStatus inherits from the Enum base class.

        Returns
        -------
        None
        """
        # Assert that TestStatus inherits from Enum
        self.assertTrue(issubclass(TestStatus, Enum))

    async def testEnumMembersType(self):
        """
        Test that each member of TestStatus is an instance of TestStatus.

        Iterates through all members of TestStatus and asserts their type.

        Returns
        -------
        None
        """
        # Assert that each enum member is an instance of TestStatus
        for status in TestStatus:
            self.assertIsInstance(status, TestStatus)
