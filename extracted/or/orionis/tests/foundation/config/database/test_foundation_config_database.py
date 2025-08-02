from orionis.foundation.config.database.entities.database import Database
from orionis.foundation.config.database.entities.connections import Connections
from orionis.foundation.exceptions.integrity import OrionisIntegrityException
from orionis.test.cases.asynchronous import AsyncTestCase

class TestFoundationConfigDatabase(AsyncTestCase):
    """
    Test cases for the Database configuration class.

    This class contains unit tests for the `Database` configuration class,
    ensuring correct default values, validation, dictionary representation,
    custom values, hashability, and keyword-only initialization.

    Attributes
    ----------
    None
    """

    async def testDefaultValues(self):
        """
        Test creation of Database instance with default values.

        Ensures that the default connection is set to 'sqlite' and the
        connections attribute is properly initialized as a Connections instance.
        """
        db = Database()
        self.assertEqual(db.default, 'sqlite')
        self.assertIsInstance(db.connections, Connections)

    async def testDefaultConnectionValidation(self):
        """
        Validate the default connection attribute.

        Checks that only valid connection types are accepted as default.
        Also verifies that invalid, empty, or non-string defaults raise
        OrionisIntegrityException.
        """
        # Test valid connection types
        valid_connections = ['sqlite', 'mysql', 'pgsql', 'oracle']
        for conn in valid_connections:
            try:
                Database(default=conn)
            except OrionisIntegrityException:
                self.fail(f"Valid connection type '{conn}' should not raise exception")

        # Test invalid connection type
        with self.assertRaises(OrionisIntegrityException):
            Database(default='invalid_connection')

        # Test empty default
        with self.assertRaises(OrionisIntegrityException):
            Database(default='')

        # Test non-string default
        with self.assertRaises(OrionisIntegrityException):
            Database(default=123)

    async def testConnectionsValidation(self):
        """
        Validate the connections attribute.

        Ensures that only instances of Connections are accepted for the
        connections attribute. Invalid types or None should raise
        OrionisIntegrityException.
        """
        # Test invalid connections type
        with self.assertRaises(OrionisIntegrityException):
            Database(connections="not_a_connections_instance")

        # Test None connections
        with self.assertRaises(OrionisIntegrityException):
            Database(connections=None)

        # Test valid connections
        try:
            Database(connections=Connections())
        except OrionisIntegrityException:
            self.fail("Valid Connections instance should not raise exception")

    async def testToDictMethod(self):
        """
        Test the toDict method of Database.

        Ensures that the toDict method returns a dictionary representation
        of the Database instance, including all attributes.
        """
        db = Database()
        db_dict = db.toDict()
        self.assertIsInstance(db_dict, dict)
        self.assertEqual(db_dict['default'], 'sqlite')
        self.assertIsInstance(db_dict['connections'], dict)

    async def testCustomValues(self):
        """
        Test storage and validation of custom values.

        Ensures that custom configurations for default and connections
        are correctly handled and validated.
        """
        custom_connections = Connections()
        custom_db = Database(
            default='mysql',
            connections=custom_connections
        )
        self.assertEqual(custom_db.default, 'mysql')
        self.assertIs(custom_db.connections, custom_connections)

    async def testHashability(self):
        """
        Test hashability of Database instances.

        Ensures that Database instances are hashable (due to unsafe_hash=True)
        and can be used in sets and as dictionary keys.
        """
        db1 = Database()
        db2 = Database()
        db_set = {db1, db2}
        self.assertEqual(len(db_set), 1)

        custom_db = Database(default='pgsql')
        db_set.add(custom_db)
        self.assertEqual(len(db_set), 2)

    async def testKwOnlyInitialization(self):
        """
        Test keyword-only initialization enforcement.

        Ensures that Database enforces keyword-only initialization and
        raises TypeError when positional arguments are used.
        """
        with self.assertRaises(TypeError):
            Database('sqlite', Connections())