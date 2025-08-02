from orionis.foundation.config.logging.entities.hourly import Hourly
from orionis.foundation.config.logging.enums.levels import Level
from orionis.foundation.exceptions.integrity import OrionisIntegrityException
from orionis.test.cases.asynchronous import AsyncTestCase

class TestFoundationConfigLoggingHourly(AsyncTestCase):
    """
    Test cases for the Hourly logging configuration class.

    This class contains unit tests for the `Hourly` logging configuration entity,
    verifying its default values, attribute validation, dictionary representation,
    hashability, and keyword-only initialization enforcement.
    """

    async def testDefaultValues(self):
        """
        Test that Hourly instance is created with correct default values.

        Verifies that the default `path`, `level`, and `retention_hours` attributes
        of the Hourly instance match the expected values.

        Returns
        -------
        None
        """
        hourly = Hourly()
        self.assertEqual(hourly.path, "storage/log/hourly.log")
        self.assertEqual(hourly.level, Level.INFO.value)
        self.assertEqual(hourly.retention_hours, 24)

    async def testPathValidation(self):
        """
        Test path attribute validation.

        Ensures that invalid values for the `path` attribute, such as empty strings
        or non-string types, raise an `OrionisIntegrityException`. Also verifies that
        valid paths do not raise exceptions.

        Returns
        -------
        None
        """
        with self.assertRaises(OrionisIntegrityException):
            Hourly(path="")
        with self.assertRaises(OrionisIntegrityException):
            Hourly(path=123)
        try:
            Hourly(path="custom/log/path.log")
        except OrionisIntegrityException:
            self.fail("Valid path should not raise exception")

    async def testLevelValidation(self):
        """
        Test level attribute validation with different input types.

        Checks that the `level` attribute accepts string, integer, and enum values,
        and that invalid values raise an `OrionisIntegrityException`.

        Returns
        -------
        None
        """
        # Test string level
        hourly = Hourly(level="debug")
        self.assertEqual(hourly.level, Level.DEBUG.value)

        # Test int level
        hourly = Hourly(level=Level.WARNING.value)
        self.assertEqual(hourly.level, Level.WARNING.value)

        # Test enum level
        hourly = Hourly(level=Level.ERROR)
        self.assertEqual(hourly.level, Level.ERROR.value)

        # Test invalid cases
        with self.assertRaises(OrionisIntegrityException):
            Hourly(level="invalid")
        with self.assertRaises(OrionisIntegrityException):
            Hourly(level=999)
        with self.assertRaises(OrionisIntegrityException):
            Hourly(level=[])

    async def testRetentionHoursValidation(self):
        """
        Test retention_hours attribute validation.

        Ensures that valid values for `retention_hours` are accepted and invalid
        values raise an `OrionisIntegrityException`.

        Returns
        -------
        None
        """
        # Test valid values
        try:
            Hourly(retention_hours=1)
            Hourly(retention_hours=168)
            Hourly(retention_hours=72)
        except OrionisIntegrityException:
            self.fail("Valid retention_hours should not raise exception")

        # Test invalid values
        with self.assertRaises(OrionisIntegrityException):
            Hourly(retention_hours=0)
        with self.assertRaises(OrionisIntegrityException):
            Hourly(retention_hours=169)
        with self.assertRaises(OrionisIntegrityException):
            Hourly(retention_hours=-1)
        with self.assertRaises(OrionisIntegrityException):
            Hourly(retention_hours="24")

    async def testWhitespaceHandling(self):
        """
        Test whitespace handling in path and level attributes.

        Returns
        -------
        None
        """

        with self.assertRaises(OrionisIntegrityException):
            hourly = Hourly(path="  logs/app.log  ", level="  debug  ")
            self.assertEqual(hourly.path, "  logs/app.log  ")
            self.assertEqual(hourly.level, Level.DEBUG.value)

    async def testToDictMethod(self):
        """
        Test that toDict returns proper dictionary representation.

        Ensures that the `toDict` method returns a dictionary with the correct
        attribute values.

        Returns
        -------
        None
        """
        hourly = Hourly()
        hourly_dict = hourly.toDict()
        self.assertIsInstance(hourly_dict, dict)
        self.assertEqual(hourly_dict['path'], "storage/log/hourly.log")
        self.assertEqual(hourly_dict['level'], Level.INFO.value)
        self.assertEqual(hourly_dict['retention_hours'], 24)

    async def testCustomValuesToDict(self):
        """
        Test that custom values are properly included in dictionary.

        Verifies that custom values provided to the Hourly instance are correctly
        reflected in the dictionary returned by `toDict`.

        Returns
        -------
        None
        """
        custom_hourly = Hourly(
            path="custom/logs/app.log",
            level="warning",
            retention_hours=48
        )
        hourly_dict = custom_hourly.toDict()
        self.assertEqual(hourly_dict['path'], "custom/logs/app.log")
        self.assertEqual(hourly_dict['level'], Level.WARNING.value)
        self.assertEqual(hourly_dict['retention_hours'], 48)

    async def testHashability(self):
        """
        Test that Hourly maintains hashability due to unsafe_hash=True.

        Ensures that Hourly instances can be added to a set and that their
        hashability is preserved.

        Returns
        -------
        None
        """
        hourly1 = Hourly()
        hourly2 = Hourly()
        hourly_set = {hourly1, hourly2}
        self.assertEqual(len(hourly_set), 1)
        custom_hourly = Hourly(path="custom.log")
        hourly_set.add(custom_hourly)
        self.assertEqual(len(hourly_set), 2)

    async def testKwOnlyInitialization(self):
        """
        Test that Hourly enforces keyword-only initialization.

        Verifies that attempting to initialize Hourly with positional arguments
        raises a TypeError.

        Returns
        -------
        None
        """
        with self.assertRaises(TypeError):
            Hourly("path.log", "info", 24)