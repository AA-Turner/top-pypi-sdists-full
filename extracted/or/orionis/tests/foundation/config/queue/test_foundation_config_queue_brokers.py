from orionis.foundation.config.queue.entities.brokers import Brokers
from orionis.foundation.config.queue.entities.database import Database
from orionis.foundation.exceptions.integrity import OrionisIntegrityException
from orionis.test.cases.asynchronous import AsyncTestCase

class TestFoundationConfigQueueBrokers(AsyncTestCase):
    async def testDefaultInitialization(self):
        """
        Test that Brokers instance is initialized with correct default values.

        Notes
        -----
        Verifies that `sync` is `True` by default and `database` is a `Database` instance.
        """
        brokers = Brokers()
        self.assertTrue(brokers.sync)
        self.assertIsInstance(brokers.database, Database)

    async def testSyncValidation(self):
        """
        Test validation for the `sync` attribute.

        Notes
        -----
        Verifies that non-boolean values for `sync` raise `OrionisIntegrityException`.
        """
        with self.assertRaises(OrionisIntegrityException):
            Brokers(sync="true")
        with self.assertRaises(OrionisIntegrityException):
            Brokers(sync=1)

    async def testCustomInitialization(self):
        """
        Test custom initialization with valid parameters.

        Notes
        -----
        Verifies that valid boolean and `Database` instances are accepted for initialization.
        """
        custom_db = Database(table="custom_queue")
        brokers = Brokers(sync=False, database=custom_db)
        self.assertFalse(brokers.sync)
        self.assertIs(brokers.database, custom_db)
        self.assertEqual(brokers.database.table, "custom_queue")

    async def testToDictMethod(self):
        """
        Test the `toDict` method returns proper dictionary representation.

        Notes
        -----
        Verifies all fields are included with correct values in the returned dictionary.
        """
        brokers = Brokers()
        result = brokers.toDict()
        self.assertIsInstance(result, dict)
        self.assertIn("sync", result)
        self.assertIn("database", result)
        self.assertTrue(result["sync"])
        self.assertIsInstance(result["database"], dict)

    async def testKwOnlyInitialization(self):
        """
        Test that Brokers requires keyword arguments for initialization.

        Notes
        -----
        Verifies the class enforces `kw_only=True` in its dataclass decorator.
        """
        with self.assertRaises(TypeError):
            Brokers(True, Database())