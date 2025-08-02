from orionis.foundation.config.logging.entities.monthly import Monthly
from orionis.foundation.config.logging.enums.levels import Level
from orionis.foundation.exceptions.integrity import OrionisIntegrityException
from orionis.test.cases.asynchronous import AsyncTestCase

class TestFoundationConfigLoggingMonthly(AsyncTestCase):
    """
    Test cases for the Monthly logging configuration class.

    Notes
    -----
    This test suite verifies the correct behavior of the `Monthly` logging configuration,
    including default values, attribute validation, dictionary conversion, hashability,
    and keyword-only initialization.
    """

    async def testDefaultValues(self):
        """
        Test that Monthly instance is created with correct default values.

        Verifies
        --------
        - Default path is "storage/log/application.log".
        - Default level is `Level.INFO.value`.
        - Default retention_months is 4.
        """
        monthly = Monthly()
        self.assertEqual(monthly.path, "storage/log/monthly.log")
        self.assertEqual(monthly.level, Level.INFO.value)
        self.assertEqual(monthly.retention_months, 4)

    async def testPathValidation(self):
        """
        Test path attribute validation.

        Verifies
        --------
        - Empty or non-string paths raise `OrionisIntegrityException`.
        - Valid string paths do not raise exceptions.
        """
        with self.assertRaises(OrionisIntegrityException):
            Monthly(path="")
        with self.assertRaises(OrionisIntegrityException):
            Monthly(path=123)
        try:
            Monthly(path="custom/log/path.log")
        except OrionisIntegrityException:
            self.fail("Valid path should not raise exception")

    async def testLevelValidation(self):
        """
        Test level attribute validation with different input types.

        Verifies
        --------
        - Accepts string, int, and enum values for level.
        - Invalid level values raise `OrionisIntegrityException`.
        """
        # Test string level
        monthly = Monthly(level="debug")
        self.assertEqual(monthly.level, Level.DEBUG.value)

        # Test int level
        monthly = Monthly(level=Level.WARNING.value)
        self.assertEqual(monthly.level, Level.WARNING.value)

        # Test enum level
        monthly = Monthly(level=Level.ERROR)
        self.assertEqual(monthly.level, Level.ERROR.value)

        # Test invalid cases
        with self.assertRaises(OrionisIntegrityException):
            Monthly(level="invalid")
        with self.assertRaises(OrionisIntegrityException):
            Monthly(level=999)
        with self.assertRaises(OrionisIntegrityException):
            Monthly(level=[])

    async def testRetentionMonthsValidation(self):
        """
        Test retention_months attribute validation.

        Verifies
        --------
        - Accepts valid integer values for retention_months.
        - Invalid values raise `OrionisIntegrityException`.
        """
        # Test valid values
        try:
            Monthly(retention_months=1)
            Monthly(retention_months=12)
            Monthly(retention_months=6)
        except OrionisIntegrityException:
            self.fail("Valid retention_months should not raise exception")

        # Test invalid values
        with self.assertRaises(OrionisIntegrityException):
            Monthly(retention_months=0)
        with self.assertRaises(OrionisIntegrityException):
            Monthly(retention_months=13)
        with self.assertRaises(OrionisIntegrityException):
            Monthly(retention_months=-1)
        with self.assertRaises(OrionisIntegrityException):
            Monthly(retention_months="4")

    async def testWhitespaceHandling(self):
        """
        Test whitespace handling in path and level attributes.
        """

        with self.assertRaises(OrionisIntegrityException):
            monthly = Monthly(path="  logs/app.log  ", level="  debug  ")
            self.assertEqual(monthly.path, "  logs/app.log  ")
            self.assertEqual(monthly.level, Level.DEBUG.value)

    async def testToDictMethod(self):
        """
        Test that toDict returns proper dictionary representation.

        Verifies
        --------
        - Output is a dictionary with correct keys and values.
        """
        monthly = Monthly()
        monthly_dict = monthly.toDict()
        self.assertIsInstance(monthly_dict, dict)
        self.assertEqual(monthly_dict['path'], "storage/log/monthly.log")
        self.assertEqual(monthly_dict['level'], Level.INFO.value)
        self.assertEqual(monthly_dict['retention_months'], 4)

    async def testCustomValuesToDict(self):
        """
        Test that custom values are properly included in dictionary.

        Verifies
        --------
        - Custom path, level, and retention_months are reflected in the output dictionary.
        """
        custom_monthly = Monthly(
            path="custom/logs/app.log",
            level="warning",
            retention_months=6
        )
        monthly_dict = custom_monthly.toDict()
        self.assertEqual(monthly_dict['path'], "custom/logs/app.log")
        self.assertEqual(monthly_dict['level'], Level.WARNING.value)
        self.assertEqual(monthly_dict['retention_months'], 6)

    async def testHashability(self):
        """
        Test that Monthly maintains hashability due to unsafe_hash=True.

        Verifies
        --------
        - Monthly instances can be added to a set and compared by value.
        """
        monthly1 = Monthly()
        monthly2 = Monthly()
        monthly_set = {monthly1, monthly2}

        self.assertEqual(len(monthly_set), 1)

        custom_monthly = Monthly(path="custom.log")
        monthly_set.add(custom_monthly)
        self.assertEqual(len(monthly_set), 2)

    async def testKwOnlyInitialization(self):
        """
        Test that Monthly enforces keyword-only initialization.

        Verifies
        --------
        - Positional arguments raise TypeError.
        """
        with self.assertRaises(TypeError):
            Monthly("path.log", "info", 4)