from orionis.foundation.config.database.entities.database import Database
from orionis.foundation.config.database.entities.connections import Connections
from orionis.foundation.exceptions.integrity import OrionisIntegrityException
from orionis.test.cases.asynchronous import AsyncTestCase

class TestFoundationConfigDatabase(AsyncTestCase):
    """
    Unit tests for the Database configuration class.

    This class provides asynchronous test cases to verify the behavior,
    validation, and integrity of the `Database` configuration class,
    including default values, attribute validation, dictionary conversion,
    custom values, hashability, and keyword-only initialization enforcement.
    """

    async def testDefaultValues(self):
        """
        Test that a Database instance initializes with correct default values.

        Ensures that the `default` attribute is set to 'sqlite' and the
        `connections` attribute is an instance of Connections.

        Returns
        -------
        None
        """
        db = Database()
        self.assertEqual(db.default, 'sqlite')
        self.assertIsInstance(db.connections, Connections)

    async def testDefaultConnectionValidation(self):
        """
        Validate the `default` connection attribute for allowed values.

        Checks that only valid connection types are accepted for the `default`
        attribute. Verifies that invalid, empty, or non-string values raise
        OrionisIntegrityException.

        Returns
        -------
        None
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
        Validate the `connections` attribute for correct type.

        Ensures that only instances of Connections are accepted for the
        `connections` attribute. Invalid types or None should raise
        OrionisIntegrityException.

        Returns
        -------
        None
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
        Test the `toDict` method for dictionary representation.

        Ensures that the `toDict` method returns a dictionary containing
        all attributes of the Database instance, including `default` and
        `connections`.

        Returns
        -------
        None
        """
        db = Database()
        db_dict = db.toDict()
        self.assertIsInstance(db_dict, dict)
        self.assertEqual(db_dict['default'], 'sqlite')
        self.assertIsInstance(db_dict['connections'], dict)

    async def testCustomValues(self):
        """
        Test handling and validation of custom attribute values.

        Ensures that custom values for `default` and `connections` are
        correctly stored and validated in the Database instance.

        Returns
        -------
        None
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
        Test that Database instances are hashable.

        Verifies that Database instances can be used in sets and as dictionary
        keys, and that identical instances are considered equal.

        Returns
        -------
        None
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
        Test enforcement of keyword-only initialization.

        Ensures that Database raises TypeError when positional arguments are
        used instead of keyword arguments during initialization.

        Returns
        -------
        None
        """
        with self.assertRaises(TypeError):
            Database('sqlite', Connections())