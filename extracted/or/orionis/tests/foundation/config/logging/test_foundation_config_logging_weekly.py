from orionis.foundation.config.logging.entities.weekly import Weekly
from orionis.foundation.config.logging.enums.levels import Level
from orionis.foundation.exceptions.integrity import OrionisIntegrityException
from orionis.test.cases.asynchronous import AsyncTestCase

class TestFoundationConfigLoggingWeekly(AsyncTestCase):
    """
    Test cases for the Weekly logging configuration class.

    This class contains unit tests for the `Weekly` logging configuration entity,
    including validation of default values, attribute validation, dictionary conversion,
    hashability, and keyword-only initialization.

    Attributes
    ----------
    None

    Methods
    -------
    testDefaultValues()
        Test that Weekly instance is created with correct default values.
    testPathValidation()
        Test path attribute validation.
    testLevelValidation()
        Test level attribute validation with different input types.
    testRetentionWeeksValidation()
        Test retention_weeks attribute validation.
    testWhitespaceHandling()
        Test whitespace handling in path and level attributes.
    testToDictMethod()
        Test that toDict returns proper dictionary representation.
    testCustomValuesToDict()
        Test that custom values are properly included in dictionary.
    testHashability()
        Test that Weekly maintains hashability due to unsafe_hash=True.
    testKwOnlyInitialization()
        Test that Weekly enforces keyword-only initialization.
    """

    async def testDefaultValues(self):
        """
        Test that Weekly instance is created with correct default values.

        Verifies that the default `path`, `level`, and `retention_weeks` attributes
        of a `Weekly` instance match the expected values.

        Returns
        -------
        None
        """
        weekly = Weekly()
        self.assertEqual(weekly.path, "storage/log/weekly.log")
        self.assertEqual(weekly.level, Level.INFO.value)
        self.assertEqual(weekly.retention_weeks, 4)

    async def testPathValidation(self):
        """
        Test path attribute validation.

        Verifies that empty or non-string `path` values raise exceptions,
        and that a valid path does not raise an exception.

        Returns
        -------
        None
        """
        with self.assertRaises(OrionisIntegrityException):
            Weekly(path="")
        with self.assertRaises(OrionisIntegrityException):
            Weekly(path=123)
        try:
            Weekly(path="custom/log/path.log")
        except OrionisIntegrityException:
            self.fail("Valid path should not raise exception")

    async def testLevelValidation(self):
        """
        Test level attribute validation with different input types.

        Checks that the `level` attribute accepts string, integer, and enum values,
        and raises exceptions for invalid types or values.

        Returns
        -------
        None
        """
        # Test string level
        weekly = Weekly(level="debug")
        self.assertEqual(weekly.level, Level.DEBUG.value)

        # Test int level
        weekly = Weekly(level=Level.WARNING.value)
        self.assertEqual(weekly.level, Level.WARNING.value)

        # Test enum level
        weekly = Weekly(level=Level.ERROR)
        self.assertEqual(weekly.level, Level.ERROR.value)

        # Test invalid cases
        with self.assertRaises(OrionisIntegrityException):
            Weekly(level="invalid")
        with self.assertRaises(OrionisIntegrityException):
            Weekly(level=999)
        with self.assertRaises(OrionisIntegrityException):
            Weekly(level=[])

    async def testRetentionWeeksValidation(self):
        """
        Test retention_weeks attribute validation.

        Ensures that valid `retention_weeks` values are accepted and invalid
        values raise exceptions.

        Returns
        -------
        None
        """
        # Test valid values
        try:
            Weekly(retention_weeks=1)
            Weekly(retention_weeks=12)
            Weekly(retention_weeks=6)
        except OrionisIntegrityException:
            self.fail("Valid retention_weeks should not raise exception")

        # Test invalid values
        with self.assertRaises(OrionisIntegrityException):
            Weekly(retention_weeks=0)
        with self.assertRaises(OrionisIntegrityException):
            Weekly(retention_weeks=13)
        with self.assertRaises(OrionisIntegrityException):
            Weekly(retention_weeks=-1)
        with self.assertRaises(OrionisIntegrityException):
            Weekly(retention_weeks="4")

    async def testWhitespaceHandling(self):
        """
        Test whitespace handling in path and level attributes.

        Verifies that leading and trailing whitespace in `path` and `level`
        attributes are handled as expected.

        Returns
        -------
        None
        """
        with self.assertRaises(OrionisIntegrityException):
            weekly = Weekly(path="  logs/app.log  ", level="  debug  ")
            self.assertEqual(weekly.path, "  logs/app.log  ")
            self.assertEqual(weekly.level, Level.DEBUG.value)

    async def testToDictMethod(self):
        """
        Test that toDict returns proper dictionary representation.

        Ensures that the `toDict` method returns a dictionary with the correct
        keys and values for a default `Weekly` instance.

        Returns
        -------
        None
        """
        weekly = Weekly()
        weekly_dict = weekly.toDict()
        self.assertIsInstance(weekly_dict, dict)
        self.assertEqual(weekly_dict['path'], "storage/log/weekly.log")
        self.assertEqual(weekly_dict['level'], Level.INFO.value)
        self.assertEqual(weekly_dict['retention_weeks'], 4)

    async def testCustomValuesToDict(self):
        """
        Test that custom values are properly included in dictionary.

        Checks that custom attribute values are correctly represented in the
        dictionary returned by `toDict`.

        Returns
        -------
        None
        """
        custom_weekly = Weekly(
            path="custom/logs/app.log",
            level="warning",
            retention_weeks=8
        )
        weekly_dict = custom_weekly.toDict()
        self.assertEqual(weekly_dict['path'], "custom/logs/app.log")
        self.assertEqual(weekly_dict['level'], Level.WARNING.value)
        self.assertEqual(weekly_dict['retention_weeks'], 8)

    async def testHashability(self):
        """
        Test that Weekly maintains hashability due to unsafe_hash=True.

        Verifies that `Weekly` instances are hashable and can be used in sets,
        and that identical instances are considered equal.

        Returns
        -------
        None
        """
        weekly1 = Weekly()
        weekly2 = Weekly()
        weekly_set = {weekly1, weekly2}

        self.assertEqual(len(weekly_set), 1)

        custom_weekly = Weekly(path="custom.log")
        weekly_set.add(custom_weekly)
        self.assertEqual(len(weekly_set), 2)

    async def testKwOnlyInitialization(self):
        """
        Test that Weekly enforces keyword-only initialization.

        Ensures that providing positional arguments to the `Weekly` constructor
        raises a TypeError.

        Returns
        -------
        None
        """
        with self.assertRaises(TypeError):
            Weekly("path.log", "info", 4)