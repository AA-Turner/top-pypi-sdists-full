from orionis.test.cases.asynchronous import AsyncTestCase
from orionis.support.facades.workers import Workers
from orionis.test.exceptions import OrionisTestValueError
from orionis.test.validators import *

class TestTestingDumper(AsyncTestCase):

    async def testValidWorkers(self) -> None:
        """
        Tests the ValidWorkers validator for correct validation of worker counts.

        This method verifies that ValidWorkers accepts valid worker counts within the allowed range,
        and raises OrionisTestValueError for invalid values such as zero, negative numbers, values
        exceeding the maximum allowed, and non-integer types.

        Returns
        -------
        None
            This method does not return any value. It asserts expected behavior using test assertions.
        """
        # Get the maximum allowed number of workers from the Workers facade
        max_allowed = Workers.calculate()

        # Valid cases: should return the input value if within allowed range
        self.assertEqual(ValidWorkers(1), 1)
        self.assertEqual(ValidWorkers(max_allowed), max_allowed)

        # Invalid cases: should raise OrionisTestValueError for out-of-range or wrong type
        with self.assertRaises(OrionisTestValueError):
            ValidWorkers(0)  # Zero is not allowed
        with self.assertRaises(OrionisTestValueError):
            ValidWorkers(max_allowed + 1)  # Exceeds maximum allowed
        with self.assertRaises(OrionisTestValueError):
            ValidWorkers(-5)  # Negative value is not allowed
        with self.assertRaises(OrionisTestValueError):
            ValidWorkers("not_an_int")  # Non-integer type is not allowed

    async def testValidBasePath(self) -> None:
        """
        Tests the ValidBasePath validator for correct validation of base path inputs.

        This method checks that ValidBasePath accepts valid path strings and Path objects,
        returning a pathlib.Path instance. It also verifies that invalid inputs such as empty strings,
        None, and non-path types raise OrionisTestValueError.

        Parameters
        ----------
        None

        Returns
        -------
        None
            This method does not return any value. It asserts expected behavior using test assertions.
        """
        from orionis.test.validators import ValidBasePath
        from pathlib import Path

        # Valid cases: should return a Path instance for valid string or Path input
        self.assertIsInstance(ValidBasePath("/tmp"), Path)
        self.assertIsInstance(ValidBasePath(Path("/tmp")), Path)

        # Invalid cases: should raise OrionisTestValueError for empty string, None, or non-path type
        with self.assertRaises(OrionisTestValueError):
            ValidBasePath("")
        with self.assertRaises(OrionisTestValueError):
            ValidBasePath(None)
        with self.assertRaises(OrionisTestValueError):
            ValidBasePath(123)

    async def testValidExecutionMode(self) -> None:
        """
        Tests the ValidExecutionMode validator for correct validation of execution mode inputs.

        This method verifies that ValidExecutionMode accepts valid execution mode strings and enum values,
        returning the corresponding string value. It also checks that invalid inputs such as unknown strings
        and non-enum types raise OrionisTestValueError.

        Parameters
        ----------
        None

        Returns
        -------
        None
            This method does not return any value. It asserts expected behavior using test assertions.
        """
        from orionis.test.validators import ValidExecutionMode
        from orionis.foundation.config.testing.enums.mode import ExecutionMode

        # Valid cases: should return the string value for valid mode string or enum input
        self.assertEqual(ValidExecutionMode("parallel"), ExecutionMode.PARALLEL.value)
        self.assertEqual(ValidExecutionMode(ExecutionMode.SEQUENTIAL), ExecutionMode.SEQUENTIAL.value)

        # Invalid cases: should raise OrionisTestValueError for unknown string or non-enum type
        with self.assertRaises(OrionisTestValueError):
            ValidExecutionMode("INVALID")  # Unknown execution mode string
        with self.assertRaises(OrionisTestValueError):
            ValidExecutionMode(123)        # Non-enum type

    async def testValidFailFast(self) -> None:
        """
        Tests the ValidFailFast validator for correct validation of fail-fast configuration.

        This method verifies that ValidFailFast accepts valid boolean inputs, returning the corresponding
        boolean value. It also checks that invalid inputs, such as non-boolean types or None, raise
        OrionisTestValueError.

        Parameters
        ----------
        None

        Returns
        -------
        None
            This method does not return any value. It asserts expected behavior using test assertions.
        """
        from orionis.test.validators import ValidFailFast

        # Valid cases: should return True or False for boolean input
        self.assertTrue(ValidFailFast(True))
        self.assertFalse(ValidFailFast(False))

        # Invalid cases: should raise OrionisTestValueError for non-boolean or None input
        with self.assertRaises(OrionisTestValueError):
            ValidFailFast("not_bool")
        with self.assertRaises(OrionisTestValueError):
            ValidFailFast(None)

    async def testValidFolderPath(self) -> None:
        """
        Tests the ValidFolderPath validator for correct validation of folder path inputs.

        This method checks that ValidFolderPath accepts valid folder path strings, including those
        with leading or trailing whitespace, and returns the normalized string path. It also verifies
        that invalid inputs such as empty strings, None, or non-string types raise OrionisTestValueError.

        Returns
        -------
        None
            This method does not return any value. It asserts expected behavior using test assertions.
        """
        from orionis.test.validators import ValidFolderPath

        # Valid cases: should return the normalized string path for valid input
        self.assertEqual(ValidFolderPath("/tmp"), "/tmp")
        self.assertEqual(ValidFolderPath("  /tmp  "), "/tmp")

        # Invalid cases: should raise OrionisTestValueError for empty string, None, or non-string type
        with self.assertRaises(OrionisTestValueError):
            ValidFolderPath("")
        with self.assertRaises(OrionisTestValueError):
            ValidFolderPath(None)
        with self.assertRaises(OrionisTestValueError):
            ValidFolderPath(123)

    async def testValidModuleName(self) -> None:
        """
        Tests the ValidModuleName validator for correct validation of module name inputs.

        This method verifies that ValidModuleName accepts valid non-empty string module names,
        returning the normalized string value. It also checks that invalid inputs such as empty strings,
        None, or non-string types raise OrionisTestValueError.

        Parameters
        ----------
        None

        Returns
        -------
        None
            This method does not return any value. It asserts expected behavior using test assertions.
        """
        from orionis.test.validators import ValidModuleName

        # Valid case: should return the normalized string for a valid module name
        self.assertEqual(ValidModuleName("mod"), "mod")

        # Invalid cases: should raise OrionisTestValueError for empty string, None, or non-string type
        with self.assertRaises(OrionisTestValueError):
            ValidModuleName("")
        with self.assertRaises(OrionisTestValueError):
            ValidModuleName(None)
        with self.assertRaises(OrionisTestValueError):
            ValidModuleName(123)

    async def testValidNamePattern(self) -> None:
        """
        Tests the ValidNamePattern validator for correct validation of name pattern inputs.

        This method verifies that ValidNamePattern accepts valid non-empty string patterns and None,
        returning the normalized string pattern or None. It also checks that invalid inputs such as
        empty strings or non-string types raise OrionisTestValueError.

        Parameters
        ----------
        None

        Returns
        -------
        None
            This method does not return any value. It asserts expected behavior using test assertions.
        """
        from orionis.test.validators import ValidNamePattern

        # Valid case: should return the normalized string for a valid pattern
        self.assertEqual(ValidNamePattern("test_*"), "test_*")

        # Valid case: should return None when input is None
        self.assertIsNone(ValidNamePattern(None))

        # Invalid cases: should raise OrionisTestValueError for empty string or non-string type
        with self.assertRaises(OrionisTestValueError):
            ValidNamePattern("")
        with self.assertRaises(OrionisTestValueError):
            ValidNamePattern(123)

    async def testValidPattern(self) -> None:
        """
        Tests the ValidPattern validator for correct validation of pattern string inputs.

        This method verifies that ValidPattern accepts valid non-empty string patterns,
        returning the normalized string value. It also checks that invalid inputs such as
        empty strings, None, or non-string types raise OrionisTestValueError.

        Returns
        -------
        None
            This method does not return any value. It asserts expected behavior using test assertions.
        """
        from orionis.test.validators import ValidPattern

        # Valid case: should return the normalized string for a valid pattern
        self.assertEqual(ValidPattern("abc"), "abc")

        # Invalid cases: should raise OrionisTestValueError for empty string, None, or non-string type
        with self.assertRaises(OrionisTestValueError):
            ValidPattern("")
        with self.assertRaises(OrionisTestValueError):
            ValidPattern(None)
        with self.assertRaises(OrionisTestValueError):
            ValidPattern(123)

    async def testValidPersistentDriver(self) -> None:
        """
        Tests the ValidPersistentDriver validator for correct validation of persistent driver inputs.

        This method verifies that ValidPersistentDriver accepts valid persistent driver names as strings
        and enum values, returning the corresponding normalized string value. It also checks that invalid
        inputs, such as unknown driver names or non-enum types, raise OrionisTestValueError.

        Parameters
        ----------
        None

        Returns
        -------
        None
            This method does not return any value. It asserts expected behavior using test assertions.
        """
        from orionis.test.validators import ValidPersistentDriver
        from orionis.foundation.config.testing.enums.drivers import PersistentDrivers

        # Valid cases: should return the normalized string for valid driver name or enum input
        self.assertEqual(ValidPersistentDriver("sqlite"), "sqlite")
        self.assertEqual(ValidPersistentDriver(PersistentDrivers.SQLITE), "sqlite")

        # Invalid cases: should raise OrionisTestValueError for unknown driver name or non-enum type
        with self.assertRaises(OrionisTestValueError):
            ValidPersistentDriver("invalid")
        with self.assertRaises(OrionisTestValueError):
            ValidPersistentDriver(123)

    async def testValidPersistent(self) -> None:
        """
        Tests the ValidPersistent validator for correct validation of persistent configuration values.

        This method verifies that ValidPersistent accepts valid boolean inputs, returning the corresponding
        boolean value. It also checks that invalid inputs, such as non-boolean types or None, raise
        OrionisTestValueError.

        Parameters
        ----------
        None

        Returns
        -------
        None
            This method does not return any value. It asserts expected behavior using test assertions.
        """
        from orionis.test.validators import ValidPersistent

        # Valid cases: should return True or False for boolean input
        self.assertTrue(ValidPersistent(True))
        self.assertFalse(ValidPersistent(False))

        # Invalid cases: should raise OrionisTestValueError for non-boolean or None input
        with self.assertRaises(OrionisTestValueError):
            ValidPersistent("not_bool")
        with self.assertRaises(OrionisTestValueError):
            ValidPersistent(None)

    async def testValidPrintResult(self) -> None:
        """
        Tests the ValidPrintResult validator for correct validation of print result configuration.

        This method verifies that ValidPrintResult accepts valid boolean inputs, returning the corresponding
        boolean value. It also checks that invalid inputs, such as non-boolean types or None, raise
        OrionisTestValueError.

        Parameters
        ----------
        None

        Returns
        -------
        None
            This method does not return any value. It asserts expected behavior using test assertions.
        """
        from orionis.test.validators import ValidPrintResult

        # Valid cases: should return True or False for boolean input
        self.assertTrue(ValidPrintResult(True))
        self.assertFalse(ValidPrintResult(False))

        # Invalid cases: should raise OrionisTestValueError for non-boolean or None input
        with self.assertRaises(OrionisTestValueError):
            ValidPrintResult("not_bool")
        with self.assertRaises(OrionisTestValueError):
            ValidPrintResult(None)

    async def testValidTags(self) -> None:
        """
        Tests the ValidTags validator for correct validation of tag list inputs.

        This method verifies that ValidTags accepts a list of non-empty string tags, normalizes whitespace,
        and returns a list of cleaned tag strings. It also checks that None is accepted and returns None.
        Invalid cases, such as empty lists, lists containing empty strings or non-string types, and non-list
        inputs, should raise OrionisTestValueError.

        Returns
        -------
        None
            This method does not return any value. It asserts expected behavior using test assertions.
        """
        from orionis.test.validators import ValidTags

        # Valid case: should return a list of normalized tag strings
        self.assertEqual(ValidTags(["a", "b ", " c"]), ["a", "b", "c"])

        # Valid case: should return None when input is None
        self.assertIsNone(ValidTags(None))

        # Invalid case: should raise OrionisTestValueError for empty list
        with self.assertRaises(OrionisTestValueError):
            ValidTags([])

        # Invalid case: should raise OrionisTestValueError for list containing empty string
        with self.assertRaises(OrionisTestValueError):
            ValidTags([""])

        # Invalid case: should raise OrionisTestValueError for list containing non-string type
        with self.assertRaises(OrionisTestValueError):
            ValidTags([123])

        # Invalid case: should raise OrionisTestValueError for non-list input
        with self.assertRaises(OrionisTestValueError):
            ValidTags("not_a_list")

    async def testValidThrowException(self) -> None:
        """
        Tests the ValidThrowException validator for correct validation of throw exception configuration.

        This method verifies that ValidThrowException accepts valid boolean inputs, returning the corresponding
        boolean value. It also checks that invalid inputs, such as non-boolean types or None, raise
        OrionisTestValueError.

        Parameters
        ----------
        None

        Returns
        -------
        None
            This method does not return any value. It asserts expected behavior using test assertions.
        """
        from orionis.test.validators import ValidThrowException

        # Valid cases: should return True or False for boolean input
        self.assertTrue(ValidThrowException(True))
        self.assertFalse(ValidThrowException(False))

        # Invalid cases: should raise OrionisTestValueError for non-boolean or None input
        with self.assertRaises(OrionisTestValueError):
            ValidThrowException("not_bool")
        with self.assertRaises(OrionisTestValueError):
            ValidThrowException(None)

    async def testValidVerbosity(self) -> None:
        """
        Tests the ValidVerbosity validator for correct validation of verbosity mode inputs.

        This method verifies that ValidVerbosity accepts valid verbosity mode enum values and their corresponding
        integer values, returning the normalized integer value. It also checks that invalid inputs such as
        negative values, unknown integers, or non-integer types raise OrionisTestValueError.

        Returns
        -------
        None
            This method does not return any value. It asserts expected behavior using test assertions.
        """
        from orionis.test.validators import ValidVerbosity
        from orionis.foundation.config.testing.enums.verbosity import VerbosityMode

        # Valid cases: should return the integer value for valid enum or integer input
        self.assertEqual(ValidVerbosity(VerbosityMode.MINIMAL), VerbosityMode.MINIMAL.value)
        self.assertEqual(ValidVerbosity(VerbosityMode.DETAILED.value), VerbosityMode.DETAILED.value)

        # Invalid cases: should raise OrionisTestValueError for negative, unknown, or non-integer input
        with self.assertRaises(OrionisTestValueError):
            ValidVerbosity(-1)
        with self.assertRaises(OrionisTestValueError):
            ValidVerbosity("not_int")
        with self.assertRaises(OrionisTestValueError):
            ValidVerbosity(999)

    async def testValidWebReport(self) -> None:
        """
        Tests the ValidWebReport validator for correct validation of web report configuration.

        This method verifies that ValidWebReport accepts valid boolean inputs, returning the corresponding
        boolean value. It also checks that invalid inputs, such as non-boolean types or None, raise
        OrionisTestValueError.

        Returns
        -------
        None
            This method does not return any value. It asserts expected behavior using test assertions.
        """
        from orionis.test.validators import ValidWebReport

        # Valid cases: should return True or False for boolean input
        self.assertTrue(ValidWebReport(True))
        self.assertFalse(ValidWebReport(False))

        # Invalid cases: should raise OrionisTestValueError for non-boolean or None input
        with self.assertRaises(OrionisTestValueError):
            ValidWebReport("not_bool")
        with self.assertRaises(OrionisTestValueError):
            ValidWebReport(None)