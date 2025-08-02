from orionis.foundation.config.database.entities.sqlite import SQLite
from orionis.foundation.config.database.enums.sqlite_foreign_key import SQLiteForeignKey
from orionis.foundation.config.database.enums.sqlite_journal import SQLiteJournalMode
from orionis.foundation.config.database.enums.sqlite_synchronous import SQLiteSynchronous
from orionis.foundation.exceptions.integrity import OrionisIntegrityException
from orionis.test.cases.asynchronous import AsyncTestCase

class TestFoundationConfigDatabaseSqlite(AsyncTestCase):
    """
    Test cases for the SQLite database configuration class.

    This class contains unit tests to validate the behavior and integrity of the
    SQLite configuration entity, ensuring correct default values, validation logic,
    and dictionary representation.
    """

    async def testDefaultValues(self):
        """
        Test that SQLite instance is created with correct default values.

        Ensures all default values match expected defaults from the class definition.

        Returns
        -------
        None
        """
        sqlite = SQLite()
        self.assertEqual(sqlite.driver, 'sqlite')
        self.assertTrue(sqlite.url.startswith('sqlite:///'))
        self.assertEqual(sqlite.database, 'database.sqlite')
        self.assertEqual(sqlite.prefix, '')
        self.assertEqual(sqlite.foreign_key_constraints, SQLiteForeignKey.OFF.value)
        self.assertEqual(sqlite.busy_timeout, 5000)
        self.assertEqual(sqlite.journal_mode, SQLiteJournalMode.DELETE.value)
        self.assertEqual(sqlite.synchronous, SQLiteSynchronous.NORMAL.value)

    async def testDriverValidation(self):
        """
        Test driver attribute validation.

        Verifies that empty or non-string drivers raise exceptions.

        Returns
        -------
        None
        """
        with self.assertRaises(OrionisIntegrityException):
            SQLite(driver='')
        with self.assertRaises(OrionisIntegrityException):
            SQLite(driver=123)

    async def testUrlValidation(self):
        """
        Test URL attribute validation.

        Verifies that empty or non-string URLs raise exceptions.

        Returns
        -------
        None
        """
        with self.assertRaises(OrionisIntegrityException):
            SQLite(url='')
        with self.assertRaises(OrionisIntegrityException):
            SQLite(url=123)

    async def testDatabaseValidation(self):
        """
        Test database attribute validation.

        Verifies that empty or non-string database paths raise exceptions.

        Returns
        -------
        None
        """
        with self.assertRaises(OrionisIntegrityException):
            SQLite(database='')
        with self.assertRaises(OrionisIntegrityException):
            SQLite(database=123)

    async def testForeignKeyConstraintsValidation(self):
        """
        Test foreign_key_constraints attribute validation.

        Verifies enum conversion and invalid value handling.

        Returns
        -------
        None
        """
        # Test string conversion
        sqlite = SQLite(foreign_key_constraints='ON')
        self.assertEqual(sqlite.foreign_key_constraints, SQLiteForeignKey.ON.value)

        # Test enum assignment
        sqlite = SQLite(foreign_key_constraints=SQLiteForeignKey.OFF)
        self.assertEqual(sqlite.foreign_key_constraints, SQLiteForeignKey.OFF.value)

        # Test invalid value
        with self.assertRaises(OrionisIntegrityException):
            SQLite(foreign_key_constraints='INVALID')

    async def testBusyTimeoutValidation(self):
        """
        Test busy_timeout attribute validation.

        Verifies non-negative integer requirement.

        Returns
        -------
        None
        """
        with self.assertRaises(OrionisIntegrityException):
            SQLite(busy_timeout=-1)
        with self.assertRaises(OrionisIntegrityException):
            SQLite(busy_timeout='invalid')

    async def testJournalModeValidation(self):
        """
        Test journal_mode attribute validation.

        Verifies enum conversion and invalid value handling.

        Returns
        -------
        None
        """
        # Test string conversion
        sqlite = SQLite(journal_mode='WAL')
        self.assertEqual(sqlite.journal_mode, SQLiteJournalMode.WAL.value)

        # Test enum assignment
        sqlite = SQLite(journal_mode=SQLiteJournalMode.TRUNCATE)
        self.assertEqual(sqlite.journal_mode, SQLiteJournalMode.TRUNCATE.value)

        # Test invalid value
        with self.assertRaises(OrionisIntegrityException):
            SQLite(journal_mode='INVALID')

    async def testSynchronousValidation(self):
        """
        Test synchronous attribute validation.

        Verifies enum conversion and invalid value handling.

        Returns
        -------
        None
        """
        # Test string conversion
        sqlite = SQLite(synchronous='FULL')
        self.assertEqual(sqlite.synchronous, SQLiteSynchronous.FULL.value)

        # Test enum assignment
        sqlite = SQLite(synchronous=SQLiteSynchronous.OFF)
        self.assertEqual(sqlite.synchronous, SQLiteSynchronous.OFF.value)

        # Test invalid value
        with self.assertRaises(OrionisIntegrityException):
            SQLite(synchronous='INVALID')

    async def testToDictMethod(self):
        """
        Test that toDict returns proper dictionary representation.

        Verifies all attributes are correctly included in the dictionary.

        Returns
        -------
        None
        """
        sqlite = SQLite()
        sqlite_dict = sqlite.toDict()
        self.assertEqual(sqlite_dict['driver'], 'sqlite')
        self.assertTrue(sqlite_dict['url'].startswith('sqlite:///'))
        self.assertEqual(sqlite_dict['database'], 'database.sqlite')
        self.assertEqual(sqlite_dict['prefix'], '')
        self.assertEqual(sqlite_dict['foreign_key_constraints'], SQLiteForeignKey.OFF.value)
        self.assertEqual(sqlite_dict['busy_timeout'], 5000)
        self.assertEqual(sqlite_dict['journal_mode'], SQLiteJournalMode.DELETE.value)
        self.assertEqual(sqlite_dict['synchronous'], SQLiteSynchronous.NORMAL.value)

    async def testCustomValues(self):
        """
        Test that custom values are properly stored and validated.

        Verifies custom configuration values are correctly handled.

        Returns
        -------
        None
        """
        custom_sqlite = SQLite(
            database='custom.db',
            prefix='app_',
            foreign_key_constraints='ON',
            busy_timeout=10000,
            journal_mode='MEMORY',
            synchronous='OFF'
        )
        self.assertEqual(custom_sqlite.database, 'custom.db')
        self.assertEqual(custom_sqlite.prefix, 'app_')
        self.assertEqual(custom_sqlite.foreign_key_constraints, SQLiteForeignKey.ON.value)
        self.assertEqual(custom_sqlite.busy_timeout, 10000)
        self.assertEqual(custom_sqlite.journal_mode, SQLiteJournalMode.MEMORY.value)
        self.assertEqual(custom_sqlite.synchronous, SQLiteSynchronous.OFF.value)