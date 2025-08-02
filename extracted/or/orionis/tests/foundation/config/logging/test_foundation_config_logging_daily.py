from datetime import time
from orionis.foundation.config.logging.entities.daily import Daily
from orionis.foundation.config.logging.enums.levels import Level
from orionis.foundation.exceptions.integrity import OrionisIntegrityException
from orionis.test.cases.asynchronous import AsyncTestCase

class TestFoundationConfigLoggingDaily(AsyncTestCase):
    """
    Test cases for the Daily logging configuration class.

    This class contains unit tests for the `Daily` logging configuration entity,
    validating its default values, attribute validation, dictionary conversion,
    hashability, and keyword-only initialization.
    """

    async def testDefaultValues(self):
        """
        Test creation of Daily instance with default values.

        Ensures that the default path, level, retention_days, and at time
        are set as expected.

        Returns
        -------
        None
        """
        daily = Daily()
        self.assertEqual(daily.path, "storage/log/daily.log")
        self.assertEqual(daily.level, Level.INFO.value)
        self.assertEqual(daily.retention_days, 7)
        self.assertEqual(daily.at, "00:00")

    async def testPathValidation(self):
        """
        Test validation of the path attribute.

        Verifies that empty or non-string paths raise exceptions, and that
        valid paths are accepted.

        Returns
        -------
        None
        """
        with self.assertRaises(OrionisIntegrityException):
            Daily(path="")
        with self.assertRaises(OrionisIntegrityException):
            Daily(path=123)
        try:
            Daily(path="custom/log/path.log")
        except OrionisIntegrityException:
            self.fail("Valid path should not raise exception")

    async def testLevelValidation(self):
        """
        Test validation of the level attribute.

        Checks that string, integer, and enum values are accepted for level,
        and that invalid values raise exceptions.

        Returns
        -------
        None
        """
        # Test string level
        daily = Daily(level="debug")
        self.assertEqual(daily.level, Level.DEBUG.value)

        # Test int level
        daily = Daily(level=Level.WARNING.value)
        self.assertEqual(daily.level, Level.WARNING.value)

        # Test enum level
        daily = Daily(level=Level.ERROR)
        self.assertEqual(daily.level, Level.ERROR.value)

        # Test invalid cases
        with self.assertRaises(OrionisIntegrityException):
            Daily(level="invalid")
        with self.assertRaises(OrionisIntegrityException):
            Daily(level=999)
        with self.assertRaises(OrionisIntegrityException):
            Daily(level=[])

    async def testRetentionDaysValidation(self):
        """
        Test validation of the retention_days attribute.

        Ensures that valid values are accepted and invalid values raise exceptions.

        Returns
        -------
        None
        """
        # Test valid values
        try:
            Daily(retention_days=1)
            Daily(retention_days=90)
            Daily(retention_days=30)
        except OrionisIntegrityException:
            self.fail("Valid retention_days should not raise exception")

        # Test invalid values
        with self.assertRaises(OrionisIntegrityException):
            Daily(retention_days=0)
        with self.assertRaises(OrionisIntegrityException):
            Daily(retention_days=91)
        with self.assertRaises(OrionisIntegrityException):
            Daily(retention_days=-1)
        with self.assertRaises(OrionisIntegrityException):
            Daily(retention_days="7")

    async def testAtTimeValidation(self):
        """
        Test validation and conversion of the at attribute.

        Checks that a `datetime.time` object is properly converted and that
        invalid types raise exceptions.

        Returns
        -------
        None
        """
        # Test time object
        daily = Daily(at=time(12, 30))
        self.assertEqual(daily.at, "12:30")

        # Test invalid type
        with self.assertRaises(OrionisIntegrityException):
            Daily(at="12:00:00")
        with self.assertRaises(OrionisIntegrityException):
            Daily(at=1200)

    async def testWhitespaceHandling(self):
        """
        Test handling of whitespace in path and level attributes.

        Returns
        -------
        None
        """

        with self.assertRaises(OrionisIntegrityException):
            daily = Daily(path="  logs/app.log  ", level="  debug  ")
            self.assertEqual(daily.path, "  logs/app.log  ")
            self.assertEqual(daily.level, Level.DEBUG.value)

    async def testToDictMethod(self):
        """
        Test the toDict method for correct dictionary representation.

        Ensures that the dictionary returned by toDict contains the correct
        default values.

        Returns
        -------
        None
        """
        daily = Daily()
        daily_dict = daily.toDict()

        self.assertIsInstance(daily_dict, dict)
        self.assertEqual(daily_dict['path'], "storage/log/daily.log")
        self.assertEqual(daily_dict['level'], Level.INFO.value)
        self.assertEqual(daily_dict['retention_days'], 7)
        self.assertEqual(daily_dict['at'], "00:00")

    async def testCustomValuesToDict(self):
        """
        Test toDict method with custom values.

        Ensures that custom values are correctly represented in the dictionary.

        Returns
        -------
        None
        """
        custom_daily = Daily(
            path="custom/logs/app.log",
            level="warning",
            retention_days=14,
            at=time(23, 59)
        )
        daily_dict = custom_daily.toDict()
        self.assertEqual(daily_dict['path'], "custom/logs/app.log")
        self.assertEqual(daily_dict['level'], Level.WARNING.value)
        self.assertEqual(daily_dict['retention_days'], 14)
        self.assertEqual(daily_dict['at'], "23:59")

    async def testHashability(self):
        """
        Test hashability of Daily instances.

        Ensures that Daily instances are hashable and can be used in sets.

        Returns
        -------
        None
        """
        daily1 = Daily()
        daily2 = Daily()
        daily_set = {daily1, daily2}

        self.assertEqual(len(daily_set), 1)

        custom_daily = Daily(path="custom.log")
        daily_set.add(custom_daily)
        self.assertEqual(len(daily_set), 2)

    async def testKwOnlyInitialization(self):
        """
        Test enforcement of keyword-only initialization.

        Ensures that positional arguments raise a TypeError.

        Returns
        -------
        None
        """
        with self.assertRaises(TypeError):
            Daily("path.log", "info", 7, time(0, 0))