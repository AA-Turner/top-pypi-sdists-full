from orionis.container.validators.is_valid_alias import IsValidAlias
from orionis.container.exceptions.type import OrionisContainerTypeError
from orionis.test.cases.asynchronous import AsyncTestCase

class TestIsValidAlias(AsyncTestCase):

    async def testValidAliases(self) -> None:
        """
        Validates that the IsValidAlias validator accepts valid alias strings.

        This test iterates over a list of valid alias strings and ensures that
        the IsValidAlias validator does not raise any exceptions for these values.
        Valid aliases include strings with letters, numbers, and underscores.

        Returns
        -------
        None
            This method does not return any value. It passes if no exception is raised.
        """
        valid_aliases = [
            "valid",
            "valid_alias",
            "validAlias",
            "valid123",
            "valid_123",
            "v",
            "1",
            "_",
            "valid_alias_with_underscores",
            "ValidAliasWithMixedCase",
            "VALID_UPPERCASE_ALIAS"
        ]

        # Ensure each valid alias passes validation without raising an exception
        for alias in valid_aliases:
            IsValidAlias(alias)

    async def testInvalidAliasTypes(self) -> None:
        """
        Ensures that IsValidAlias raises an exception for non-string types.

        This test checks that passing values of types other than string (such as
        integers, floats, None, booleans, lists, dictionaries, tuples, and sets)
        to the IsValidAlias validator results in an OrionisContainerTypeError.

        Returns
        -------
        None
            This method does not return any value. It passes if the expected exception is raised.
        """
        invalid_types = [
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

        # Ensure each invalid type raises the expected exception
        for value in invalid_types:
            with self.assertRaises(OrionisContainerTypeError) as context:
                IsValidAlias(value)

    async def testAliasWithInvalidCharacters(self) -> None:
        """
        Verifies that aliases containing invalid characters are rejected.

        This test iterates over a list of alias strings containing whitespace,
        control characters, and special symbols, and asserts that the
        IsValidAlias validator raises an OrionisContainerTypeError for each.
        It also checks that the exception message is descriptive.

        Returns
        -------
        None
            This method does not return any value. It passes if the expected exception and message are raised.
        """
        invalid_aliases = [
            "invalid alias",  # space
            "invalid\talias",  # tab
            "invalid\nalias",  # newline
            "invalid@alias",   # special character
            "invalid#alias",   # special character
            "invalid$alias",   # special character
            "invalid%alias",   # special character
            "invalid&alias",   # special character
            "invalid*alias",   # special character
            "invalid(alias)",  # parentheses
            "invalid[alias]",  # brackets
            "invalid{alias}",  # braces
            "invalid;alias",   # semicolon
            "invalid:alias",   # colon
            "invalid,alias",   # comma
            "invalid/alias",   # slash
            "invalid\\alias",  # backslash
            "invalid<alias>",  # angle brackets
            "invalid|alias",   # pipe
            "invalid`alias",   # backtick
            'invalid"alias',   # double quote
            "invalid'alias"    # single quote
        ]

        # Ensure each invalid alias raises the expected exception and message
        for alias in invalid_aliases:
            with self.assertRaises(OrionisContainerTypeError) as context:
                IsValidAlias(alias)

            expected_msg_start = f"Alias '{alias}' contains invalid characters."
            # Check that the exception message starts as expected
            self.assertTrue(str(context.exception).startswith(expected_msg_start))
            # Check that the message contains additional guidance
            self.assertIn("Aliases must not contain whitespace or special symbols", str(context.exception))

    async def testEmptyAlias(self) -> None:
        """
        Checks that empty or whitespace-only aliases are rejected.

        This test verifies that passing an empty string or a string containing
        only whitespace to the IsValidAlias validator raises an
        OrionisContainerTypeError with the correct error message.

        Returns
        -------
        None
            This method does not return any value. It passes if the expected exception and message are raised.
        """
        # Empty string should be rejected
        with self.assertRaises(OrionisContainerTypeError) as context:
            IsValidAlias("")

        self.assertEqual(
            str(context.exception),
            "Alias cannot be None, empty, or whitespace only."
        )

        # Whitespace-only string should also be rejected
        with self.assertRaises(OrionisContainerTypeError) as context:
            IsValidAlias("   ")

        self.assertEqual(
            str(context.exception),
            "Alias cannot be None, empty, or whitespace only."
        )