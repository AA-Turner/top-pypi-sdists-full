from orionis.foundation.config.logging.entities.channels import Channels
from orionis.foundation.config.logging.entities.stack import Stack
from orionis.foundation.config.logging.entities.hourly import Hourly
from orionis.foundation.config.logging.entities.daily import Daily
from orionis.foundation.config.logging.entities.weekly import Weekly
from orionis.foundation.config.logging.entities.monthly import Monthly
from orionis.foundation.config.logging.entities.chunked import Chunked
from orionis.foundation.exceptions.integrity import OrionisIntegrityException
from orionis.test.cases.asynchronous import AsyncTestCase

class TestFoundationConfigLoggingChannels(AsyncTestCase):
    """
    Unit tests for the `Channels` logging configuration class.

    This test class validates the correct initialization, type enforcement,
    custom configuration, dictionary conversion, hashability, and keyword-only
    initialization of the `Channels` class.

    Methods
    -------
    testDefaultValues()
        Verify that a Channels instance is initialized with the correct default values.
    testStackValidation()
        Ensure that only Stack instances are accepted for the stack attribute.
    testHourlyValidation()
        Ensure that only Hourly instances are accepted for the hourly attribute.
    testDailyValidation()
        Ensure that only Daily instances are accepted for the daily attribute.
    testWeeklyValidation()
        Ensure that only Weekly instances are accepted for the weekly attribute.
    testMonthlyValidation()
        Ensure that only Monthly instances are accepted for the monthly attribute.
    testChunkedValidation()
        Ensure that only Chunked instances are accepted for the chunked attribute.
    testCustomConfigurations()
        Validate that custom channel configurations are correctly assigned and validated.
    testToDictMethod()
        Check that the toDict method returns the correct dictionary representation.
    testHashability()
        Confirm that Channels instances are hashable due to unsafe_hash=True.
    testKwOnlyInitialization()
        Ensure that Channels enforces keyword-only initialization.
    """

    async def testDefaultValues(self):
        """
        Verify that a Channels instance is initialized with the correct default values.

        Ensures that all channel configuration attributes are instances of their
        respective classes upon default initialization.

        Returns
        -------
        None
        """
        channels = Channels()
        self.assertIsInstance(channels.stack, Stack)
        self.assertIsInstance(channels.hourly, Hourly)
        self.assertIsInstance(channels.daily, Daily)
        self.assertIsInstance(channels.weekly, Weekly)
        self.assertIsInstance(channels.monthly, Monthly)
        self.assertIsInstance(channels.chunked, Chunked)

    async def testStackValidation(self):
        """
        Ensure that only Stack instances are accepted for the stack attribute.

        Raises
        ------
        OrionisIntegrityException
            If the stack attribute is not a Stack instance.
        """
        with self.assertRaises(OrionisIntegrityException):
            Channels(stack="not_a_stack_instance")
        with self.assertRaises(OrionisIntegrityException):
            Channels(stack=123)
        try:
            Channels(stack=Stack())
        except OrionisIntegrityException:
            self.fail("Valid Stack instance should not raise exception")

    async def testHourlyValidation(self):
        """
        Ensure that only Hourly instances are accepted for the hourly attribute.

        Raises
        ------
        OrionisIntegrityException
            If the hourly attribute is not an Hourly instance.
        """
        with self.assertRaises(OrionisIntegrityException):
            Channels(hourly="not_an_hourly_instance")
        try:
            Channels(hourly=Hourly())
        except OrionisIntegrityException:
            self.fail("Valid Hourly instance should not raise exception")

    async def testDailyValidation(self):
        """
        Ensure that only Daily instances are accepted for the daily attribute.

        Raises
        ------
        OrionisIntegrityException
            If the daily attribute is not a Daily instance.
        """
        with self.assertRaises(OrionisIntegrityException):
            Channels(daily="not_a_daily_instance")
        try:
            Channels(daily=Daily())
        except OrionisIntegrityException:
            self.fail("Valid Daily instance should not raise exception")

    async def testWeeklyValidation(self):
        """
        Ensure that only Weekly instances are accepted for the weekly attribute.

        Raises
        ------
        OrionisIntegrityException
            If the weekly attribute is not a Weekly instance.
        """
        with self.assertRaises(OrionisIntegrityException):
            Channels(weekly="not_a_weekly_instance")
        try:
            Channels(weekly=Weekly())
        except OrionisIntegrityException:
            self.fail("Valid Weekly instance should not raise exception")

    async def testMonthlyValidation(self):
        """
        Ensure that only Monthly instances are accepted for the monthly attribute.

        Raises
        ------
        OrionisIntegrityException
            If the monthly attribute is not a Monthly instance.
        """
        with self.assertRaises(OrionisIntegrityException):
            Channels(monthly="not_a_monthly_instance")
        try:
            Channels(monthly=Monthly())
        except OrionisIntegrityException:
            self.fail("Valid Monthly instance should not raise exception")

    async def testChunkedValidation(self):
        """
        Ensure that only Chunked instances are accepted for the chunked attribute.

        Raises
        ------
        OrionisIntegrityException
            If the chunked attribute is not a Chunked instance.
        """
        with self.assertRaises(OrionisIntegrityException):
            Channels(chunked="not_a_chunked_instance")
        try:
            Channels(chunked=Chunked())
        except OrionisIntegrityException:
            self.fail("Valid Chunked instance should not raise exception")

    async def testCustomConfigurations(self):
        """
        Validate that custom channel configurations are correctly assigned and validated.

        Ensures that custom channel instances are properly set and their properties
        are accurately assigned.

        Returns
        -------
        None
        """
        custom_stack = Stack(path="custom/stack.log")
        custom_hourly = Hourly(path="custom/hourly.log")
        custom_daily = Daily(path="custom/daily.log")
        custom_weekly = Weekly(path="custom/weekly.log")
        custom_monthly = Monthly(path="custom/monthly.log")
        custom_chunked = Chunked(path="custom/chunked.log")

        channels = Channels(
            stack=custom_stack,
            hourly=custom_hourly,
            daily=custom_daily,
            weekly=custom_weekly,
            monthly=custom_monthly,
            chunked=custom_chunked
        )
        self.assertEqual(channels.stack.path, "custom/stack.log")
        self.assertEqual(channels.hourly.path, "custom/hourly.log")
        self.assertEqual(channels.daily.path, "custom/daily.log")
        self.assertEqual(channels.weekly.path, "custom/weekly.log")
        self.assertEqual(channels.monthly.path, "custom/monthly.log")
        self.assertEqual(channels.chunked.path, "custom/chunked.log")

    async def testToDictMethod(self):
        """
        Check that the toDict method returns the correct dictionary representation.

        Ensures that the `toDict` method produces a dictionary with the expected
        structure and types for each channel.

        Returns
        -------
        None
        """
        channels = Channels()
        channels_dict = channels.toDict()
        self.assertIsInstance(channels_dict, dict)
        self.assertIsInstance(channels_dict['stack'], dict)
        self.assertIsInstance(channels_dict['hourly'], dict)
        self.assertIsInstance(channels_dict['daily'], dict)
        self.assertIsInstance(channels_dict['weekly'], dict)
        self.assertIsInstance(channels_dict['monthly'], dict)
        self.assertIsInstance(channels_dict['chunked'], dict)

    async def testHashability(self):
        """
        Confirm that Channels instances are hashable due to unsafe_hash=True.

        Ensures that Channels objects can be used in sets and as dictionary keys.

        Returns
        -------
        None
        """
        channels1 = Channels()
        channels2 = Channels()
        channels_set = {channels1, channels2}

        self.assertEqual(len(channels_set), 1)

        custom_channels = Channels(stack=Stack(path="custom.log"))
        channels_set.add(custom_channels)
        self.assertEqual(len(channels_set), 2)

    async def testKwOnlyInitialization(self):
        """
        Ensure that Channels enforces keyword-only initialization.

        Raises
        ------
        TypeError
            If positional arguments are used instead of keyword arguments.
        """
        with self.assertRaises(TypeError):
            Channels(Stack(), Hourly(), Daily(), Weekly(), Monthly(), Chunked())