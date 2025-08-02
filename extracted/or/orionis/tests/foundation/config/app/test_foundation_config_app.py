from orionis.foundation.config.app.entities.app import App
from orionis.foundation.config.app.enums.ciphers import Cipher
from orionis.foundation.config.app.enums.environments import Environments
from orionis.foundation.exceptions.integrity import OrionisIntegrityException
from orionis.test.cases.asynchronous import AsyncTestCase
from orionis.services.system.workers import Workers

class TestFoundationConfigApp(AsyncTestCase):

    async def testDefaultValues(self):
        """
        Tests that the App class initializes with the correct default values for all attributes.

        This method creates an instance of the App class without passing any arguments and
        verifies that each attribute is set to its expected default value. It also checks that
        the generated key is a non-empty string.

        Returns
        -------
        None
            This method does not return any value. It performs assertions to validate default values.
        """
        app = App()  # Create App instance with default parameters

        # Assert default name
        self.assertEqual(app.name, 'Orionis Application')

        # Assert default environment
        self.assertEqual(app.env, Environments.DEVELOPMENT.value)

        # Assert default debug mode is enabled
        self.assertTrue(app.debug)

        # Assert default URL
        self.assertEqual(app.url, 'http://127.0.0.1')

        # Assert default port
        self.assertEqual(app.port, 8000)

        # Assert default timezone
        self.assertEqual(app.timezone, 'UTC')

        # Assert default locale
        self.assertEqual(app.locale, 'en')

        # Assert default fallback locale
        self.assertEqual(app.fallback_locale, 'en')

        # Assert default cipher
        self.assertEqual(app.cipher, Cipher.AES_256_CBC.value)

        # Assert key is a non-empty string
        self.assertIsInstance(app.key, str)
        self.assertTrue(app.key)  # key is never None or empty
        self.assertEqual(app.maintenance, '/maintenance')

    async def testEnvironmentValidation(self):
        """
        Validates that the App class correctly handles environment values.

        This method tests the initialization of the App class with different environment values,
        ensuring that valid environments are accepted and set correctly, while invalid values
        raise an OrionisIntegrityException.

        Parameters
        ----------
        None

        Returns
        -------
        None
            This method does not return any value. It performs assertions to validate environment handling.
        """
        # Test with a valid environment string
        app = App(env="PRODUCTION")
        self.assertEqual(app.env, Environments.PRODUCTION.value)

        # Test with a valid Environments enum
        app = App(env=Environments.TESTING)
        self.assertEqual(app.env, Environments.TESTING.value)

        # Test with an invalid environment value, expecting an exception
        with self.assertRaises(OrionisIntegrityException):
            App(env="INVALID_ENV")

    async def testCipherValidation(self):
        """
        Validates that the App class correctly handles cipher values.

        This method tests the initialization of the App class with different cipher values,
        ensuring that valid ciphers are accepted and set correctly, while invalid values
        raise an OrionisIntegrityException.

        Parameters
        ----------
        None

        Returns
        -------
        None
            This method does not return any value. It performs assertions to validate cipher handling.
        """
        # Test with a valid cipher string
        app = App(cipher="AES_128_CBC")
        self.assertEqual(app.cipher, Cipher.AES_128_CBC.value)

        # Test with a valid Cipher enum
        app = App(cipher=Cipher.AES_192_CBC)
        self.assertEqual(app.cipher, Cipher.AES_192_CBC.value)

        # Test with an invalid cipher value, expecting an exception
        with self.assertRaises(OrionisIntegrityException):
            App(cipher="INVALID_CIPHER")

    async def testTypeValidation(self):
        """
        Validates that the App class enforces correct types for its attributes.

        This method attempts to initialize the App class with incorrect types for various attributes.
        It asserts that an OrionisIntegrityException is raised for each case, ensuring that type validation
        is properly enforced for all relevant parameters.

        Parameters
        ----------
        None

        Returns
        -------
        None
            This method does not return any value. It performs assertions to verify type validation.
        """
        # Name must be a string, not an integer
        with self.assertRaises(OrionisIntegrityException):
            App(name=123)

        # Debug must be a boolean, not a string
        with self.assertRaises(OrionisIntegrityException):
            App(debug="true")

        # URL must be a string, not an integer
        with self.assertRaises(OrionisIntegrityException):
            App(url=123)

        # Port must be an integer, not a string
        with self.assertRaises(OrionisIntegrityException):
            App(port="8000")

        # Workers must be an integer, not a string
        with self.assertRaises(OrionisIntegrityException):
            App(workers="4")

        # Reload must be a boolean, not a string
        with self.assertRaises(OrionisIntegrityException):
            App(reload="true")

    async def testWorkersRangeValidation(self):
        """
        Tests the validation of the workers parameter range for the App class.

        This method verifies that the App class raises an OrionisIntegrityException
        when initialized with an invalid number of workers. Specifically, it checks
        for two cases:
            - When the number of workers is set to 0 (below the minimum allowed).
            - When the number of workers exceeds the maximum allowed, as calculated
              by Workers().calculate().

        Comments are provided within the code to clarify the purpose of each assertion.

        Returns
        -------
        None
            This test method does not return any value. It asserts that exceptions
            are raised for invalid worker counts.
        """
        max_workers = Workers().calculate()
        with self.assertRaises(OrionisIntegrityException):
            App(workers=0)
        with self.assertRaises(OrionisIntegrityException):
            App(workers=max_workers + 1)

    async def testToDictMethod(self):
        """
        Tests the `toDict` method of the App class to ensure it returns a dictionary
        representation of the application's configuration with correct values.

        This method creates an instance of the App class using default parameters,
        invokes the `toDict` method, and verifies that the returned dictionary contains
        all expected keys and values matching the default configuration. It also checks
        that the key attribute is a non-empty string.

        Returns
        -------
        None
            This method does not return any value. It performs assertions to validate
            the correctness of the dictionary returned by `toDict`.
        """
        app = App()  # Create App instance with default parameters

        app_dict = app.toDict()  # Get dictionary representation of the app configuration

        # Assert that the returned value is a dictionary
        self.assertIsInstance(app_dict, dict)

        # Assert each key in the dictionary matches the expected default value
        self.assertEqual(app_dict['name'], 'Orionis Application')
        self.assertEqual(app_dict['env'], Environments.DEVELOPMENT.value)
        self.assertTrue(app_dict['debug'])
        self.assertEqual(app_dict['url'], 'http://127.0.0.1')
        self.assertEqual(app_dict['port'], 8000)
        self.assertEqual(app_dict['timezone'], 'UTC')
        self.assertEqual(app_dict['locale'], 'en')
        self.assertEqual(app_dict['fallback_locale'], 'en')
        self.assertEqual(app_dict['cipher'], Cipher.AES_256_CBC.value)

        # Assert that the key is a non-empty string
        self.assertIsInstance(app_dict['key'], str)
        self.assertTrue(app_dict['key'])

        self.assertEqual(app_dict['maintenance'], '/maintenance')

    async def testNonEmptyStringValidation(self):
        """
        Validates that the App class enforces non-empty string constraints for specific attributes.

        This method attempts to initialize the App class with empty strings for attributes that require
        non-empty values, such as `name`, `url`, `timezone`, `locale`, `fallback_locale`, and `maintenance`.
        It asserts that an OrionisIntegrityException is raised for each case, ensuring that the class
        properly enforces non-empty string validation. Additionally, it checks that the `maintenance`
        attribute must start with a forward slash (`/`).

        Returns
        -------
        None
            This method does not return any value. It performs assertions to verify non-empty string validation.
        """
        # Name must not be an empty string
        with self.assertRaises(OrionisIntegrityException):
            App(name="")

        # URL must not be an empty string
        with self.assertRaises(OrionisIntegrityException):
            App(url="")

        # Timezone must not be an empty string
        with self.assertRaises(OrionisIntegrityException):
            App(timezone="")

        # Locale must not be an empty string
        with self.assertRaises(OrionisIntegrityException):
            App(locale="")

        # Fallback locale must not be an empty string
        with self.assertRaises(OrionisIntegrityException):
            App(fallback_locale="")

        # Maintenance must not be an empty string
        with self.assertRaises(OrionisIntegrityException):
            App(maintenance="")

        # Maintenance must start with a forward slash ('/')
        with self.assertRaises(OrionisIntegrityException):
            App(maintenance="maintenance")
