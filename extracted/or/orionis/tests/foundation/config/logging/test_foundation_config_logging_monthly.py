from orionis.foundation.config.logging.entities.monthly import Monthly
from orionis.foundation.config.logging.enums.levels import Level
from orionis.foundation.exceptions.integrity import OrionisIntegrityException
from orionis.test.cases.asynchronous import AsyncTestCase

class TestFoundationConfigLoggingMonthly(AsyncTestCase):
    """
    Test suite for the `Monthly` logging configuration class.

    This class contains asynchronous test cases to validate the behavior of the
    `Monthly` logging configuration, including default values, attribute validation,
    dictionary conversion, hashability, and keyword-only initialization.
    """

    async def testDefaultValues(self):
        """
        Test the default attribute values of a Monthly instance.

        Returns
        -------
        None

        Asserts
        -------
        - The default path is "storage/log/monthly.log".
        - The default level is `Level.INFO.value`.
        - The default retention_months is 4.
        """
        monthly = Monthly()
        self.assertEqual(monthly.path, "storage/log/monthly.log")
        self.assertEqual(monthly.level, Level.INFO.value)
        self.assertEqual(monthly.retention_months, 4)

    async def testPathValidation(self):
        """
        Validate the `path` attribute for correct and incorrect values.

        Returns
        -------
        None

        Asserts
        -------
        - Raises OrionisIntegrityException for empty or non-string paths.
        - Does not raise for valid string paths.
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
        Validate the `level` attribute with various input types.

        Returns
        -------
        None

        Asserts
        -------
        - Accepts string, int, and enum values for level.
        - Raises OrionisIntegrityException for invalid level values.
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
        Validate the `retention_months` attribute for correct and incorrect values.

        Returns
        -------
        None

        Asserts
        -------
        - Accepts valid integer values for retention_months.
        - Raises OrionisIntegrityException for invalid values.
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
        Test handling of leading and trailing whitespace in `path` and `level` attributes.

        Returns
        -------
        None

        Asserts
        -------
        - Raises OrionisIntegrityException if whitespace is not properly handled.
        """
        with self.assertRaises(OrionisIntegrityException):
            monthly = Monthly(path="  logs/app.log  ", level="  debug  ")
            self.assertEqual(monthly.path, "  logs/app.log  ")
            self.assertEqual(monthly.level, Level.DEBUG.value)

    async def testToDictMethod(self):
        """
        Test the `toDict` method for correct dictionary representation.

        Returns
        -------
        None

        Asserts
        -------
        - The output is a dictionary with correct keys and values.
        """
        monthly = Monthly()
        monthly_dict = monthly.toDict()
        self.assertIsInstance(monthly_dict, dict)
        self.assertEqual(monthly_dict['path'], "storage/log/monthly.log")
        self.assertEqual(monthly_dict['level'], Level.INFO.value)
        self.assertEqual(monthly_dict['retention_months'], 4)

    async def testCustomValuesToDict(self):
        """
        Test that custom attribute values are reflected in the dictionary output.

        Returns
        -------
        None

        Asserts
        -------
        - Custom path, level, and retention_months are present in the output dictionary.
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
        Test that Monthly instances are hashable and can be used in sets.

        Returns
        -------
        None

        Asserts
        -------
        - Monthly instances with identical attributes are considered equal in a set.
        - Monthly instances with different attributes are considered distinct.
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

        Returns
        -------
        None

        Asserts
        -------
        - Raises TypeError when positional arguments are used.
        """
        with self.assertRaises(TypeError):
            Monthly("path.log", "info", 4)