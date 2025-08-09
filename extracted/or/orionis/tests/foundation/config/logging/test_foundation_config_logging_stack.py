from orionis.foundation.config.logging.entities.stack import Stack
from orionis.foundation.config.logging.enums.levels import Level
from orionis.foundation.exceptions.integrity import OrionisIntegrityException
from orionis.test.cases.asynchronous import AsyncTestCase

class TestFoundationConfigLoggingStack(AsyncTestCase):
    """
    Asynchronous unit tests for the Stack logging configuration class.

    This test class validates the behavior of the Stack class, including default values,
    attribute validation, dictionary conversion, hashability, and enforcement of keyword-only
    initialization.
    """

    async def testDefaultValues(self):
        """
        Test that Stack initializes with correct default values.

        Checks that the default path and level attributes of a Stack instance match
        the expected class defaults.

        Returns
        -------
        None
        """
        stack = Stack()
        self.assertEqual(stack.path, "storage/log/stack.log")
        self.assertEqual(stack.level, Level.INFO.value)

    async def testPathValidation(self):
        """
        Validate the path attribute for correct type and non-emptiness.

        Ensures that providing an empty string or a non-string value for the path
        raises an OrionisIntegrityException, while a valid string path is accepted.

        Raises
        ------
        OrionisIntegrityException
            If the path is empty or not a string.
        """
        # Test empty path
        with self.assertRaises(OrionisIntegrityException):
            Stack(path="")
        # Test non-string path
        with self.assertRaises(OrionisIntegrityException):
            Stack(path=123)
        # Test valid path
        try:
            Stack(path="custom/log/path.log")
        except OrionisIntegrityException:
            self.fail("Valid path should not raise exception")

    async def testLevelValidation(self):
        """
        Validate the level attribute with various input types.

        Verifies that the level attribute accepts string, integer, and enum values
        corresponding to valid logging levels, and raises exceptions for invalid values.

        Raises
        ------
        OrionisIntegrityException
            If the level is invalid or of an unsupported type.
        """
        # Test string level
        stack = Stack(level="debug")
        self.assertEqual(stack.level, Level.DEBUG.value)

        # Test int level
        stack = Stack(level=Level.WARNING.value)
        self.assertEqual(stack.level, Level.WARNING.value)

        # Test enum level
        stack = Stack(level=Level.ERROR)
        self.assertEqual(stack.level, Level.ERROR.value)

        # Test invalid string level
        with self.assertRaises(OrionisIntegrityException):
            Stack(level="invalid")

        # Test invalid int level
        with self.assertRaises(OrionisIntegrityException):
            Stack(level=999)

        # Test invalid type
        with self.assertRaises(OrionisIntegrityException):
            Stack(level=[])

    async def testWhitespaceHandling(self):
        """
        Test handling of whitespace in path and level attributes.

        Ensures that leading or trailing whitespace in the path attribute is not accepted
        and raises an OrionisIntegrityException.

        Raises
        ------
        OrionisIntegrityException
            If the path contains leading or trailing whitespace.
        """
        with self.assertRaises(OrionisIntegrityException):
            spaced_path = "  logs/app.log  "
            stack = Stack(path=spaced_path)
            self.assertEqual(stack.path, spaced_path)

    async def testToDictMethod(self):
        """
        Test the toDict method for correct dictionary representation.

        Verifies that the dictionary returned by toDict contains the correct path and
        level values for a Stack instance with default attributes.

        Returns
        -------
        None
        """
        stack = Stack()
        stack_dict = stack.toDict()

        self.assertIsInstance(stack_dict, dict)
        self.assertEqual(stack_dict['path'], "storage/log/stack.log")
        self.assertEqual(stack_dict['level'], Level.INFO.value)

    async def testCustomValuesToDict(self):
        """
        Test dictionary representation with custom attribute values.

        Ensures that custom path and level values are accurately reflected in the
        dictionary returned by toDict.

        Returns
        -------
        None
        """
        custom_stack = Stack(
            path="custom/logs/app.log",
            level="warning"
        )
        stack_dict = custom_stack.toDict()
        self.assertEqual(stack_dict['path'], "custom/logs/app.log")
        self.assertEqual(stack_dict['level'], Level.WARNING.value)

    async def testHashability(self):
        """
        Test that Stack instances are hashable.

        Verifies that Stack instances can be added to sets and used as dictionary keys,
        and that instances with identical attributes are considered equal.

        Returns
        -------
        None
        """
        stack1 = Stack()
        stack2 = Stack()
        stack_set = {stack1, stack2}

        self.assertEqual(len(stack_set), 1)

        custom_stack = Stack(path="custom.log")
        stack_set.add(custom_stack)
        self.assertEqual(len(stack_set), 2)

    async def testKwOnlyInitialization(self):
        """
        Test enforcement of keyword-only initialization for Stack.

        Ensures that attempting to initialize Stack with positional arguments raises
        a TypeError.

        Raises
        ------
        TypeError
            If positional arguments are used for initialization.
        """
        with self.assertRaises(TypeError):
            Stack("path.log", "info")