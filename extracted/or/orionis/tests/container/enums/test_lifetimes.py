from orionis.container.enums.lifetimes import Lifetime
from orionis.test.cases.asynchronous import AsyncTestCase

class TestLifetime(AsyncTestCase):

    async def testLifetimeValuesExist(self) -> None:
        """
        Checks that the `Lifetime` enum contains the expected lifecycle values.

        This test verifies the presence of the following enum members:
        - `TRANSIENT`
        - `SINGLETON`
        - `SCOPED`

        Returns
        -------
        None
            This method does not return any value. It asserts the existence of enum members.
        """

        # Assert that each expected enum member exists in Lifetime
        self.assertIn(Lifetime.TRANSIENT, Lifetime)
        self.assertIn(Lifetime.SINGLETON, Lifetime)
        self.assertIn(Lifetime.SCOPED, Lifetime)

    async def testLifetimeValuesAreUnique(self) -> None:
        """
        Ensures that all `Lifetime` enum values are unique.

        This test collects the integer values of all enum members and checks that
        there are no duplicates.

        Returns
        -------
        None
            This method does not return any value. It asserts uniqueness of enum values.
        """

        # Gather all enum values
        values = [member.value for member in Lifetime]

        # Assert that all values are unique
        self.assertEqual(len(values), len(set(values)))

    async def testLifetimeCount(self) -> None:
        """
        Validates that the `Lifetime` enum defines exactly three lifecycle types.

        This test ensures that no additional or missing enum members exist.

        Returns
        -------
        None
            This method does not return any value. It asserts the count of enum members.
        """

        # Assert that there are exactly three members in the Lifetime enum
        self.assertEqual(len(list(Lifetime)), 3)

    async def testLifetimeStringRepresentation(self) -> None:
        """
        Verifies the string representation of `Lifetime` enum members.

        This test checks that converting each enum member to a string yields the expected format.

        Returns
        -------
        None
            This method does not return any value. It asserts string representations.
        """

        # Assert that string representations match expected format
        self.assertEqual(str(Lifetime.TRANSIENT), "Lifetime.TRANSIENT")
        self.assertEqual(str(Lifetime.SINGLETON), "Lifetime.SINGLETON")
        self.assertEqual(str(Lifetime.SCOPED), "Lifetime.SCOPED")

    async def testLifetimeComparison(self) -> None:
        """
        Tests comparison operations between `Lifetime` enum members.

        This test verifies that each enum member is only equal to itself and not to others.

        Returns
        -------
        None
            This method does not return any value. It asserts comparison results.
        """

        # Assert that different enum members are not equal
        self.assertNotEqual(Lifetime.TRANSIENT, Lifetime.SINGLETON)
        self.assertNotEqual(Lifetime.SINGLETON, Lifetime.SCOPED)
        self.assertNotEqual(Lifetime.TRANSIENT, Lifetime.SCOPED)

        # Assert that each enum member is equal to itself
        self.assertEqual(Lifetime.TRANSIENT, Lifetime.TRANSIENT)
        self.assertEqual(Lifetime.SINGLETON, Lifetime.SINGLETON)
        self.assertEqual(Lifetime.SCOPED, Lifetime.SCOPED)