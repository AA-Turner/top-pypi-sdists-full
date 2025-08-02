from orionis.foundation.config.queue.entities.queue import Queue
from orionis.foundation.config.queue.entities.brokers import Brokers
from orionis.foundation.exceptions.integrity import OrionisIntegrityException
from orionis.test.cases.asynchronous import AsyncTestCase

class TestFoundationConfigQueue(AsyncTestCase):

    async def testDefaultInitialization(self):
        """
        Test default initialization of Queue.

        Ensures that a Queue instance is initialized with the correct default values.

        Returns
        -------
        None

        Raises
        ------
        AssertionError
            If the default value or brokers instance is incorrect.
        """
        queue = Queue()
        self.assertEqual(queue.default, "sync")
        self.assertIsInstance(queue.brokers, Brokers)

    async def testDefaultValidation(self):
        """
        Test validation of the `default` attribute.

        Checks that invalid values for the `default` attribute raise an OrionisIntegrityException.

        Returns
        -------
        None

        Raises
        ------
        OrionisIntegrityException
            If an invalid default value is provided.
        """
        invalid_options = ["invalid", "", 123, None]
        for option in invalid_options:
            with self.assertRaises(OrionisIntegrityException):
                Queue(default=option)

    async def testValidCustomInitialization(self):
        """
        Test custom initialization with valid parameters.

        Verifies that a Queue instance can be initialized with a valid default value and a Brokers instance.

        Returns
        -------
        None

        Raises
        ------
        AssertionError
            If the custom initialization does not set the attributes correctly.
        """
        custom_brokers = Brokers(sync=False)
        queue = Queue(default="sync", brokers=custom_brokers)
        self.assertEqual(queue.default, "sync")
        self.assertIs(queue.brokers, custom_brokers)
        self.assertFalse(queue.brokers.sync)

    async def testToDictMethod(self):
        """
        Test the `toDict` method.

        Ensures that the `toDict` method returns a dictionary representation of the Queue instance with all fields and correct values.

        Returns
        -------
        None

        Raises
        ------
        AssertionError
            If the dictionary representation is incorrect.
        """
        queue = Queue()
        result = queue.toDict()
        self.assertIsInstance(result, dict)
        self.assertEqual(result["default"], "sync")
        self.assertIsInstance(result["brokers"], dict)
        self.assertTrue(result["brokers"]["sync"])