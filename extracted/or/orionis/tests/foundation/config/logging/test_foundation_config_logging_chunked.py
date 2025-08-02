from orionis.foundation.config.logging.entities.chunked import Chunked
from orionis.foundation.config.logging.enums.levels import Level
from orionis.foundation.exceptions.integrity import OrionisIntegrityException
from orionis.test.cases.asynchronous import AsyncTestCase

class TestFoundationConfigLoggingChunked(AsyncTestCase):
    """
    Test cases for the Chunked logging configuration class.

    Notes
    -----
    These tests validate the integrity, default values, and behavior of the
    `Chunked` logging configuration entity, including its attributes and methods.
    """

    async def testDefaultValues(self):
        """
        Test default values of Chunked instance.

        Ensures that a `Chunked` instance is created with the correct default values
        for `path`, `level`, `mb_size`, and `files`.

        Returns
        -------
        None
        """
        chunked = Chunked()
        self.assertEqual(chunked.path, "storage/log/chunked.log")
        self.assertEqual(chunked.level, Level.INFO.value)
        self.assertEqual(chunked.mb_size, 10)
        self.assertEqual(chunked.files, 5)

    async def testPathValidation(self):
        """
        Test validation of the `path` attribute.

        Verifies that empty or non-string paths raise `OrionisIntegrityException`.
        Also checks that a valid path does not raise an exception.

        Returns
        -------
        None
        """
        with self.assertRaises(OrionisIntegrityException):
            Chunked(path="")
        with self.assertRaises(OrionisIntegrityException):
            Chunked(path=123)
        try:
            Chunked(path="custom/log/path.log")
        except OrionisIntegrityException:
            self.fail("Valid path should not raise exception")

    async def testLevelValidation(self):
        """
        Test validation of the `level` attribute.

        Checks that the `level` can be set using a string, integer, or enum,
        and that invalid values raise `OrionisIntegrityException`.

        Returns
        -------
        None
        """
        # Test string level
        chunked = Chunked(level="debug")
        self.assertEqual(chunked.level, Level.DEBUG.value)

        # Test int level
        chunked = Chunked(level=Level.WARNING.value)
        self.assertEqual(chunked.level, Level.WARNING.value)

        # Test enum level
        chunked = Chunked(level=Level.ERROR)
        self.assertEqual(chunked.level, Level.ERROR.value)

        # Test invalid cases
        with self.assertRaises(OrionisIntegrityException):
            Chunked(level="invalid")
        with self.assertRaises(OrionisIntegrityException):
            Chunked(level=999)
        with self.assertRaises(OrionisIntegrityException):
            Chunked(level=[])

    async def testMbSizeValidation(self):
        """
        Test validation of the `mb_size` attribute.

        Returns
        -------
        None
        """
        chunked = Chunked(mb_size=10)
        self.assertEqual(chunked.mb_size, 10)

        chunked = Chunked(mb_size=1000)
        self.assertEqual(chunked.mb_size, 1000)

        with self.assertRaises(OrionisIntegrityException):
            chunked = Chunked(mb_size=2048)
            self.assertEqual(chunked.mb_size, 2048)

    async def testFilesValidation(self):
        """
        Test validation of the `files` attribute.

        Ensures that valid integer values are accepted, and invalid values raise
        `OrionisIntegrityException`.

        Returns
        -------
        None
        """
        # Test valid values
        try:
            Chunked(files=1)
            Chunked(files=10)
        except OrionisIntegrityException:
            self.fail("Valid files count should not raise exception")

        # Test invalid values
        with self.assertRaises(OrionisIntegrityException):
            Chunked(files=0)
        with self.assertRaises(OrionisIntegrityException):
            Chunked(files=-1)
        with self.assertRaises(OrionisIntegrityException):
            Chunked(files="5")

    async def testWhitespaceHandling(self):
        """
        Test handling of whitespace in `path` and `level` attributes.

        Returns
        -------
        None
        """
        with self.assertRaises(OrionisIntegrityException):
            chunked = Chunked(path="  logs/app.log  ", level="  debug  ")
            self.assertEqual(chunked.path, "  logs/app.log  ")
            self.assertEqual(chunked.level, Level.DEBUG.value)

    async def testToDictMethod(self):
        """
        Test the `toDict` method.

        Ensures that `toDict` returns a dictionary representation of the instance
        with correct values.

        Returns
        -------
        None
        """
        chunked = Chunked()
        chunked_dict = chunked.toDict()

        self.assertIsInstance(chunked_dict, dict)
        self.assertEqual(chunked_dict['path'], "storage/log/chunked.log")
        self.assertEqual(chunked_dict['level'], Level.INFO.value)
        self.assertEqual(chunked_dict['mb_size'], 10)
        self.assertEqual(chunked_dict['files'], 5)

    async def testCustomValuesToDict(self):
        """
        Test `toDict` with custom values.

        Ensures that custom values provided to the constructor are correctly
        reflected in the dictionary representation.

        Returns
        -------
        None
        """
        custom_chunked = Chunked(
            path="custom/logs/app.log",
            level="warning",
            mb_size=20,
            files=10
        )
        chunked_dict = custom_chunked.toDict()
        self.assertEqual(chunked_dict['path'], "custom/logs/app.log")
        self.assertEqual(chunked_dict['level'], 30)
        self.assertEqual(chunked_dict['mb_size'], 20)
        self.assertEqual(chunked_dict['files'], 10)

    async def testHashability(self):
        """
        Test hashability of Chunked instances.

        Ensures that `Chunked` instances are hashable and can be used in sets,
        due to `unsafe_hash=True`.

        Returns
        -------
        None
        """
        chunked1 = Chunked()
        chunked2 = Chunked()
        chunked_set = {chunked1, chunked2}

        self.assertEqual(len(chunked_set), 1)

        custom_chunked = Chunked(path="custom.log")
        chunked_set.add(custom_chunked)
        self.assertEqual(len(chunked_set), 2)

    async def testKwOnlyInitialization(self):
        """
        Test enforcement of keyword-only initialization.

        Ensures that `Chunked` cannot be initialized with positional arguments,
        and raises a `TypeError` if attempted.

        Returns
        -------
        None
        """
        with self.assertRaises(TypeError):
            Chunked("path.log", "info", 10, 5)