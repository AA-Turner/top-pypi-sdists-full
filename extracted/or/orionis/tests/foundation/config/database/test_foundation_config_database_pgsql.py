from orionis.foundation.config.database.entities.pgsql import PGSQL
from orionis.foundation.config.database.enums.pgsql_charsets import PGSQLCharset
from orionis.foundation.config.database.enums.pgsql_mode import PGSQLSSLMode
from orionis.foundation.exceptions.integrity import OrionisIntegrityException
from orionis.test.cases.asynchronous import AsyncTestCase

class TestFoundationConfigDatabasePgsql(AsyncTestCase):
    """
    Test cases for the PGSQL database configuration class.

    This class contains asynchronous unit tests for validating the behavior,
    default values, and integrity checks of the PGSQL configuration entity.
    """

    async def testDefaultValues(self):
        """
        Test default values of PGSQL instance.

        Ensures that a PGSQL instance is created with the correct default values
        as defined in the class.

        Returns
        -------
        None
        """
        pgsql = PGSQL()
        self.assertEqual(pgsql.driver, 'pgsql')
        self.assertEqual(pgsql.host, '127.0.0.1')
        self.assertEqual(pgsql.port, 5432)
        self.assertEqual(pgsql.database, 'orionis')
        self.assertEqual(pgsql.username, 'postgres')
        self.assertEqual(pgsql.password, '')
        self.assertEqual(pgsql.charset, PGSQLCharset.UTF8.value)
        self.assertEqual(pgsql.prefix, '')
        self.assertTrue(pgsql.prefix_indexes)
        self.assertEqual(pgsql.search_path, 'public')
        self.assertEqual(pgsql.sslmode, PGSQLSSLMode.PREFER.value)

    async def testDriverValidation(self):
        """
        Test validation of the driver attribute.

        Checks that empty or non-string driver values raise an exception.

        Returns
        -------
        None
        """
        with self.assertRaises(OrionisIntegrityException):
            PGSQL(driver='')
        with self.assertRaises(OrionisIntegrityException):
            PGSQL(driver=123)

    async def testHostValidation(self):
        """
        Test validation of the host attribute.

        Checks that empty or non-string host values raise an exception.

        Returns
        -------
        None
        """
        with self.assertRaises(OrionisIntegrityException):
            PGSQL(host='')
        with self.assertRaises(OrionisIntegrityException):
            PGSQL(host=123)

    async def testPortValidation(self):
        """
        Test validation of the port attribute.

        Checks that non-numeric string ports or non-string ports raise an exception.

        Returns
        -------
        None
        """
        with self.assertRaises(OrionisIntegrityException):
            PGSQL(port='abc')
        with self.assertRaises(OrionisIntegrityException):
            PGSQL(port='string')

    async def testDatabaseValidation(self):
        """
        Test validation of the database attribute.

        Checks that empty or non-string database names raise an exception.

        Returns
        -------
        None
        """
        with self.assertRaises(OrionisIntegrityException):
            PGSQL(database='')
        with self.assertRaises(OrionisIntegrityException):
            PGSQL(database=123)

    async def testUsernameValidation(self):
        """
        Test validation of the username attribute.

        Checks that empty or non-string usernames raise an exception.

        Returns
        -------
        None
        """
        with self.assertRaises(OrionisIntegrityException):
            PGSQL(username='')
        with self.assertRaises(OrionisIntegrityException):
            PGSQL(username=123)

    async def testPasswordValidation(self):
        """
        Test validation of the password attribute.

        Checks that non-string passwords raise an exception.

        Returns
        -------
        None
        """
        with self.assertRaises(OrionisIntegrityException):
            PGSQL(password=123)

    async def testCharsetValidation(self):
        """
        Test validation of the charset attribute.

        Ensures correct enum conversion and handling of invalid values.

        Returns
        -------
        None
        """
        # Test string conversion
        pgsql = PGSQL(charset='UTF8')
        self.assertEqual(pgsql.charset, PGSQLCharset.UTF8.value)

        # Test enum assignment
        pgsql = PGSQL(charset=PGSQLCharset.LATIN1)
        self.assertEqual(pgsql.charset, PGSQLCharset.LATIN1.value)

        # Test invalid value
        with self.assertRaises(OrionisIntegrityException):
            PGSQL(charset='INVALID')

    async def testPrefixIndexesValidation(self):
        """
        Test validation of the prefix_indexes attribute.

        Checks that non-boolean values raise an exception.

        Returns
        -------
        None
        """
        with self.assertRaises(OrionisIntegrityException):
            PGSQL(prefix_indexes='true')
        with self.assertRaises(OrionisIntegrityException):
            PGSQL(prefix_indexes=1)

    async def testSearchPathValidation(self):
        """
        Test validation of the search_path attribute.

        Checks that empty or non-string search paths raise an exception.

        Returns
        -------
        None
        """
        with self.assertRaises(OrionisIntegrityException):
            PGSQL(search_path='')
        with self.assertRaises(OrionisIntegrityException):
            PGSQL(search_path=123)

    async def testSSLModeValidation(self):
        """
        Test validation of the sslmode attribute.

        Ensures correct enum conversion and handling of invalid values.

        Returns
        -------
        None
        """
        # Test string conversion
        pgsql = PGSQL(sslmode='REQUIRE')
        self.assertEqual(pgsql.sslmode, PGSQLSSLMode.REQUIRE.value)

        # Test enum assignment
        pgsql = PGSQL(sslmode=PGSQLSSLMode.DISABLE)
        self.assertEqual(pgsql.sslmode, PGSQLSSLMode.DISABLE.value)

        # Test invalid value
        with self.assertRaises(OrionisIntegrityException):
            PGSQL(sslmode='INVALID')

    async def testToDictMethod(self):
        """
        Test the toDict method of PGSQL.

        Ensures that the dictionary representation contains all attributes
        with correct values.

        Returns
        -------
        None
        """
        pgsql = PGSQL()
        pgsql_dict = pgsql.toDict()
        self.assertEqual(pgsql_dict['driver'], 'pgsql')
        self.assertEqual(pgsql_dict['host'], '127.0.0.1')
        self.assertEqual(pgsql_dict['port'], 5432)
        self.assertEqual(pgsql_dict['database'], 'orionis')
        self.assertEqual(pgsql_dict['username'], 'postgres')
        self.assertEqual(pgsql_dict['password'], '')
        self.assertEqual(pgsql_dict['charset'], PGSQLCharset.UTF8.value)
        self.assertEqual(pgsql_dict['prefix'], '')
        self.assertTrue(pgsql_dict['prefix_indexes'])
        self.assertEqual(pgsql_dict['search_path'], 'public')
        self.assertEqual(pgsql_dict['sslmode'], PGSQLSSLMode.PREFER.value)

    async def testCustomValues(self):
        """
        Test custom configuration values for PGSQL.

        Ensures that custom values are properly stored and validated.

        Returns
        -------
        None
        """
        custom_pgsql = PGSQL(
            host='db.example.com',
            port='6432',
            database='custom_db',
            username='admin',
            password='secure123',
            charset='LATIN1',
            prefix='app_',
            prefix_indexes=False,
            search_path='app_schema',
            sslmode='VERIFY_FULL'
        )
        self.assertEqual(custom_pgsql.host, 'db.example.com')
        self.assertEqual(custom_pgsql.port, '6432')
        self.assertEqual(custom_pgsql.database, 'custom_db')
        self.assertEqual(custom_pgsql.username, 'admin')
        self.assertEqual(custom_pgsql.password, 'secure123')
        self.assertEqual(custom_pgsql.charset, PGSQLCharset.LATIN1.value)
        self.assertEqual(custom_pgsql.prefix, 'app_')
        self.assertFalse(custom_pgsql.prefix_indexes)
        self.assertEqual(custom_pgsql.search_path, 'app_schema')
        self.assertEqual(custom_pgsql.sslmode, PGSQLSSLMode.VERIFY_FULL.value)