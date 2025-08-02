from orionis.foundation.config.logging.entities.stack import Stack
from orionis.foundation.config.logging.enums.levels import Level
from orionis.foundation.exceptions.integrity import OrionisIntegrityException
from orionis.test.cases.asynchronous import AsyncTestCase

class TestFoundationConfigLoggingStack(AsyncTestCase):
    """
    Test cases for the Stack logging configuration class.

    This class contains asynchronous unit tests for the Stack class, 
    validating default values, attribute validation, dictionary representation, 
    hashability, and keyword-only initialization.
    """

    async def testDefaultValues(self):
        """
        Test default values of Stack.

        Ensures that a Stack instance is created with the correct default values.
        Verifies that the default path and level match the expected values from the class definition.
        """
        stack = Stack()
        self.assertEqual(stack.path, "storage/log/stack.log")
        self.assertEqual(stack.level, Level.INFO.value)

    async def testPathValidation(self):
        """
        Test validation of the path attribute.

        Checks that empty or non-string paths raise exceptions, and that valid paths are accepted.

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
        Test validation of the level attribute with different input types.

        Verifies that string, int, and enum level values are properly handled.

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
        """

        with self.assertRaises(OrionisIntegrityException):
            spaced_path = "  logs/app.log  "
            stack = Stack(path=spaced_path)
            self.assertEqual(stack.path, spaced_path)

    async def testToDictMethod(self):
        """
        Test the toDict method for dictionary representation.

        Ensures that both path and level are correctly included in the dictionary.

        Returns
        -------
        dict
            Dictionary representation of the Stack instance.
        """
        stack = Stack()
        stack_dict = stack.toDict()

        self.assertIsInstance(stack_dict, dict)
        self.assertEqual(stack_dict['path'], "storage/log/stack.log")
        self.assertEqual(stack_dict['level'], Level.INFO.value)

    async def testCustomValuesToDict(self):
        """
        Test custom values in dictionary representation.

        Ensures that custom path and level values are properly included in the dictionary.
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
        Test hashability of Stack instances.

        Ensures that Stack instances can be used in sets and as dictionary keys due to unsafe_hash=True.
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
        Test enforcement of keyword-only initialization.

        Ensures that Stack cannot be initialized with positional arguments.

        Raises
        ------
        TypeError
            If positional arguments are used for initialization.
        """
        with self.assertRaises(TypeError):
            Stack("path.log", "info")