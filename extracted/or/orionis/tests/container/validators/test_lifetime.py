from orionis.container.validators.lifetime import LifetimeValidator
from orionis.container.enums.lifetimes import Lifetime
from orionis.container.exceptions.type import OrionisContainerTypeError
from orionis.test.cases.asynchronous import AsyncTestCase

class TestLifetimeValidator(AsyncTestCase):

    async def testValidLifetimeEnumValues(self) -> None:
        """
        Validate that LifetimeValidator correctly accepts Lifetime enum values.

        This test checks that the validator returns the corresponding Lifetime enum
        when provided with valid enum values.

        Returns
        -------
        None
            This method does not return anything. It asserts correctness via test assertions.
        """
        # Assert that each Lifetime enum value is accepted and returned as expected
        self.assertEqual(LifetimeValidator(Lifetime.TRANSIENT), Lifetime.TRANSIENT)
        self.assertEqual(LifetimeValidator(Lifetime.SINGLETON), Lifetime.SINGLETON)
        self.assertEqual(LifetimeValidator(Lifetime.SCOPED), Lifetime.SCOPED)

    async def testValidLifetimeStringValues(self) -> None:
        """
        Validate that LifetimeValidator correctly accepts valid string representations.

        This test verifies that the validator returns the correct Lifetime enum when
        provided with valid string representations, including different cases and extra whitespace.

        Returns
        -------
        None
            This method does not return anything. It asserts correctness via test assertions.
        """
        # Assert that valid uppercase string representations are accepted
        self.assertEqual(LifetimeValidator("TRANSIENT"), Lifetime.TRANSIENT)
        self.assertEqual(LifetimeValidator("SINGLETON"), Lifetime.SINGLETON)
        self.assertEqual(LifetimeValidator("SCOPED"), Lifetime.SCOPED)

        # Assert that lowercase and mixed case strings are accepted
        self.assertEqual(LifetimeValidator("transient"), Lifetime.TRANSIENT)
        self.assertEqual(LifetimeValidator("Singleton"), Lifetime.SINGLETON)
        self.assertEqual(LifetimeValidator("scoped"), Lifetime.SCOPED)

        # Assert that strings with extra whitespace are accepted
        self.assertEqual(LifetimeValidator(" TRANSIENT "), Lifetime.TRANSIENT)
        self.assertEqual(LifetimeValidator("  singleton  "), Lifetime.SINGLETON)

    async def testInvalidLifetimeStringValue(self) -> None:
        """
        Validate that LifetimeValidator raises an error for invalid string values.

        This test ensures that the validator raises OrionisContainerTypeError when
        provided with an invalid string representation, and that the error message
        contains information about valid options.

        Returns
        -------
        None
            This method does not return anything. It asserts correctness via test assertions.
        """
        # Attempt to validate an invalid string and check for the expected exception
        with self.assertRaises(OrionisContainerTypeError) as context:
            LifetimeValidator("INVALID_LIFETIME")

        # Assert that the error message contains relevant information
        self.assertIn("Invalid lifetime 'INVALID_LIFETIME'", str(context.exception))
        self.assertIn("Valid options are:", str(context.exception))
        self.assertIn("TRANSIENT", str(context.exception))
        self.assertIn("SINGLETON", str(context.exception))
        self.assertIn("SCOPED", str(context.exception))

    async def testInvalidLifetimeType(self) -> None:
        """
        Validate that LifetimeValidator raises an error for invalid input types.

        This test checks that the validator raises OrionisContainerTypeError when
        provided with values of types other than str or Lifetime enum.

        Returns
        -------
        None
            This method does not return anything. It asserts correctness via test assertions.
        """
        # List of invalid types to test
        invalid_values = [
            123,
            3.14,
            None,
            True,
            False,
            [],
            {},
            (),
            set()
        ]

        # Assert that each invalid type raises the expected exception
        for value in invalid_values:
            with self.assertRaises(OrionisContainerTypeError) as context:
                LifetimeValidator(value)

            expected_msg = f"Lifetime must be of type str or Lifetime enum, got {type(value).__name__}."
            self.assertEqual(str(context.exception), expected_msg)