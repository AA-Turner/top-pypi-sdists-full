from orionis.foundation.config.logging.entities.logging import Logging
from orionis.foundation.config.logging.entities.channels import Channels
from orionis.foundation.exceptions.integrity import OrionisIntegrityException
from orionis.test.cases.asynchronous import AsyncTestCase

class TestFoundationConfigLogging(AsyncTestCase):
    """
    Unit tests for the Logging class.

    This test suite verifies the correct initialization, dictionary conversion,
    post-initialization validation, and keyword-only argument enforcement of the
    Logging class.
    """

    async def testDefaultValues(self):
        """
        Test default values of Logging.

        Ensures that a new Logging instance is initialized with the correct default values.

        Parameters
        ----------
        self : TestLogging
            The test case instance.

        Returns
        -------
        None

        Raises
        ------
        AssertionError
            If the default values are not as expected.
        """
        logging = Logging()
        self.assertEqual(logging.default, "stack")
        self.assertIsInstance(logging.channels, Channels)

    async def testToDictMethod(self):
        """
        Test the toDict method of Logging.

        Checks that the toDict method returns a dictionary representation with all expected fields.

        Parameters
        ----------
        self : TestLogging
            The test case instance.

        Returns
        -------
        None

        Raises
        ------
        AssertionError
            If the dictionary representation is not as expected.
        """
        logging = Logging()
        result = logging.toDict()
        self.assertIsInstance(result, dict)
        self.assertIn("default", result)
        self.assertIn("channels", result)

    async def testPostInitValidation(self):
        """
        Test post-initialization validation of Logging.

        Verifies that providing an invalid default channel or channels type raises an exception.

        Parameters
        ----------
        self : TestLogging
            The test case instance.

        Returns
        -------
        None

        Raises
        ------
        AssertionError
            If the expected exception is not raised.
        """
        with self.assertRaises(OrionisIntegrityException):
            Logging(default="invalid_channel")

        with self.assertRaises(OrionisIntegrityException):
            Logging(channels="invalid_channels")

    async def testKwOnlyInitialization(self):
        """
        Test keyword-only initialization enforcement.

        Ensures that Logging requires keyword arguments for initialization.

        Parameters
        ----------
        self : TestLogging
            The test case instance.

        Returns
        -------
        None

        Raises
        ------
        AssertionError
            If TypeError is not raised when using positional arguments.
        """
        with self.assertRaises(TypeError):
            Logging("stack", Channels())