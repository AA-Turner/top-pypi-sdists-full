from orionis.test.cases.asynchronous import AsyncTestCase
from orionis.foundation.config.cache.entities.cache import Cache
from orionis.foundation.config.cache.enums.drivers import Drivers
from orionis.foundation.exceptions.integrity import OrionisIntegrityException
from orionis.foundation.config.cache.entities.stores import Stores

class TestFoundationConfigCache(AsyncTestCase):
    """
    Test suite for the Cache configuration entity.

    This class contains asynchronous unit tests for the Cache entity,
    validating default values, driver validation, type checking,
    dictionary conversion, and Stores instance validation.
    """

    async def testDefaultValues(self):
        """
        Test that the Cache instance is created with the correct default values.

        Ensures that the default values of the Cache instance match the expected
        defaults from the class definition.

        Returns
        -------
        None
        """
        cache = Cache()
        self.assertEqual(cache.default, Drivers.MEMORY.value)
        self.assertIsInstance(cache.stores, Stores)

    async def testDriverValidation(self):
        """
        Test validation and conversion of the default driver attribute.

        Verifies that string drivers are converted to enum values and that
        invalid drivers raise exceptions.

        Returns
        -------
        None
        """
        # Test valid string driver
        cache = Cache(default="FILE")
        self.assertEqual(cache.default, Drivers.FILE.value)

        # Test invalid driver
        with self.assertRaises(OrionisIntegrityException):
            Cache(default="INVALID_DRIVER")

    async def testDriverCaseInsensitivity(self):
        """
        Test case insensitivity of driver names provided as strings.

        Ensures that different case variations of driver names are properly
        normalized to the correct enum value.

        Returns
        -------
        None
        """
        # Test lowercase
        cache = Cache(default="file")
        self.assertEqual(cache.default, Drivers.FILE.value)

        # Test mixed case
        cache = Cache(default="FiLe")
        self.assertEqual(cache.default, Drivers.FILE.value)

        # Test uppercase
        cache = Cache(default="FILE")
        self.assertEqual(cache.default, Drivers.FILE.value)

    async def testTypeValidation(self):
        """
        Test type validation for all attributes.

        Ensures that invalid types for each attribute raise
        OrionisIntegrityException.

        Returns
        -------
        None
        """
        # Test invalid default type
        with self.assertRaises(OrionisIntegrityException):
            Cache(default=123)

        # Test invalid stores type
        with self.assertRaises(OrionisIntegrityException):
            Cache(stores="invalid_stores")

    async def testToDictMethod(self):
        """
        Test the toDict method for dictionary representation.

        Ensures that the toDict method returns a dictionary containing all
        expected keys and values.

        Returns
        -------
        None
        """
        cache = Cache()
        cache_dict = cache.toDict()

        self.assertIsInstance(cache_dict, dict)
        self.assertEqual(cache_dict['default'], Drivers.MEMORY.value)
        self.assertIsInstance(cache_dict['stores'], dict)

    async def testStoresInstanceValidation(self):
        """
        Test that the stores attribute must be an instance of Stores.

        Ensures that only Stores instances are accepted for the stores
        attribute and invalid types raise exceptions.

        Returns
        -------
        None
        """
        # Test with proper Stores instance
        stores = Stores()  # Assuming Stores has a default constructor
        cache = Cache(stores=stores)
        self.assertIsInstance(cache.stores, Stores)

        # Test with invalid stores type
        with self.assertRaises(OrionisIntegrityException):
            Cache(stores={"file": "some_path"})

    async def testDriverEnumConversion(self):
        """
        Test conversion of Drivers enum values to string representations.

        Ensures that enum members are converted to their value representations
        when used as the default driver.

        Returns
        -------
        None
        """
        # Test with enum member
        cache = Cache(default=Drivers.MEMORY)
        self.assertEqual(cache.default, Drivers.MEMORY.value)