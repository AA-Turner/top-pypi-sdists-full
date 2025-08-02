from orionis.foundation.config.database.entities.mysql import MySQL
from orionis.foundation.config.database.enums.mysql_charsets import MySQLCharset
from orionis.foundation.config.database.enums.mysql_collations import MySQLCollation
from orionis.foundation.config.database.enums.mysql_engine import MySQLEngine
from orionis.foundation.exceptions.integrity import OrionisIntegrityException
from orionis.test.cases.asynchronous import AsyncTestCase

class TestFoundationConfigDatabaseMysql(AsyncTestCase):
    """
    Test cases for the MySQL database configuration class.

    This class contains asynchronous unit tests for validating the behavior,
    default values, and input validation of the `MySQL` configuration entity.

    Attributes
    ----------
    None

    Methods
    -------
    testDefaultValues()
        Test that MySQL instance is created with correct default values.
    testDriverValidation()
        Test driver attribute validation.
    testHostValidation()
        Test host attribute validation.
    testPortValidation()
        Test port attribute validation.
    testDatabaseValidation()
        Test database attribute validation.
    testUsernameValidation()
        Test username attribute validation.
    testPasswordValidation()
        Test password attribute validation.
    testUnixSocketValidation()
        Test unix_socket attribute validation.
    testCharsetValidation()
        Test charset attribute validation.
    testCollationValidation()
        Test collation attribute validation.
    testPrefixValidation()
        Test prefix attribute validation.
    testPrefixIndexesValidation()
        Test prefix_indexes attribute validation.
    testStrictValidation()
        Test strict attribute validation.
    testEngineValidation()
        Test engine attribute validation.
    testToDictMethod()
        Test that toDict returns proper dictionary representation.
    testCustomValues()
        Test that custom values are properly stored and validated.
    """

    async def testDefaultValues(self):
        """
        Test that MySQL instance is created with correct default values.

        Verifies all default values match expected defaults from class definition.
        """
        mysql = MySQL()
        self.assertEqual(mysql.driver, 'mysql')
        self.assertEqual(mysql.host, '127.0.0.1')
        self.assertEqual(mysql.port, 3306)
        self.assertEqual(mysql.database, 'orionis')
        self.assertEqual(mysql.username, 'root')
        self.assertEqual(mysql.password, '')
        self.assertEqual(mysql.unix_socket, '')
        self.assertEqual(mysql.charset, MySQLCharset.UTF8MB4.value)
        self.assertEqual(mysql.collation, MySQLCollation.UTF8MB4_UNICODE_CI.value)
        self.assertEqual(mysql.prefix, '')
        self.assertTrue(mysql.prefix_indexes)
        self.assertTrue(mysql.strict)
        self.assertEqual(mysql.engine, MySQLEngine.INNODB.value)

    async def testDriverValidation(self):
        """
        Test driver attribute validation.

        Ensures that only 'mysql' value is accepted for driver.

        Raises
        ------
        OrionisIntegrityException
            If the driver value is invalid.
        """
        with self.assertRaises(OrionisIntegrityException):
            MySQL(driver='')
        with self.assertRaises(OrionisIntegrityException):
            MySQL(driver='postgres')
        with self.assertRaises(OrionisIntegrityException):
            MySQL(driver=123)

    async def testHostValidation(self):
        """
        Test host attribute validation.

        Ensures that empty or non-string hosts raise exceptions.

        Raises
        ------
        OrionisIntegrityException
            If the host value is invalid.
        """
        with self.assertRaises(OrionisIntegrityException):
            MySQL(host='')
        with self.assertRaises(OrionisIntegrityException):
            MySQL(host=123)

    async def testPortValidation(self):
        """
        Test port attribute validation.

        Ensures invalid port numbers raise exceptions.

        Raises
        ------
        OrionisIntegrityException
            If the port value is invalid.
        """
        with self.assertRaises(OrionisIntegrityException):
            MySQL(port=0)
        with self.assertRaises(OrionisIntegrityException):
            MySQL(port=65536)
        with self.assertRaises(OrionisIntegrityException):
            MySQL(port='3306')

    async def testDatabaseValidation(self):
        """
        Test database attribute validation.

        Ensures that empty or non-string database names raise exceptions.

        Raises
        ------
        OrionisIntegrityException
            If the database value is invalid.
        """
        with self.assertRaises(OrionisIntegrityException):
            MySQL(database='')
        with self.assertRaises(OrionisIntegrityException):
            MySQL(database=123)

    async def testUsernameValidation(self):
        """
        Test username attribute validation.

        Ensures that empty or non-string usernames raise exceptions.

        Raises
        ------
        OrionisIntegrityException
            If the username value is invalid.
        """
        with self.assertRaises(OrionisIntegrityException):
            MySQL(username='')
        with self.assertRaises(OrionisIntegrityException):
            MySQL(username=123)

    async def testPasswordValidation(self):
        """
        Test password attribute validation.

        Ensures that non-string passwords raise exceptions.

        Raises
        ------
        OrionisIntegrityException
            If the password value is invalid.
        """
        with self.assertRaises(OrionisIntegrityException):
            MySQL(password=123)

    async def testUnixSocketValidation(self):
        """
        Test unix_socket attribute validation.

        Ensures that non-string socket paths raise exceptions.

        Raises
        ------
        OrionisIntegrityException
            If the unix_socket value is invalid.
        """
        with self.assertRaises(OrionisIntegrityException):
            MySQL(unix_socket=123)

    async def testCharsetValidation(self):
        """
        Test charset attribute validation.

        Ensures enum conversion and invalid value handling.

        Raises
        ------
        OrionisIntegrityException
            If the charset value is invalid.
        """
        # Test string conversion
        mysql = MySQL(charset='UTF8')
        self.assertEqual(mysql.charset, MySQLCharset.UTF8.value)
        # Test enum assignment
        mysql = MySQL(charset=MySQLCharset.LATIN1)
        self.assertEqual(mysql.charset, MySQLCharset.LATIN1.value)

        # Test invalid value
        with self.assertRaises(OrionisIntegrityException):
            MySQL(charset='INVALID')

    async def testCollationValidation(self):
        """
        Test collation attribute validation.

        Ensures enum conversion and invalid value handling.

        Raises
        ------
        OrionisIntegrityException
            If the collation value is invalid.
        """
        # Test string conversion
        mysql = MySQL(collation='UTF8_GENERAL_CI')
        self.assertEqual(mysql.collation, MySQLCollation.UTF8_GENERAL_CI.value)
        # Test enum assignment
        mysql = MySQL(collation=MySQLCollation.UTF8MB4_BIN)
        self.assertEqual(mysql.collation, MySQLCollation.UTF8MB4_BIN.value)

        # Test invalid value
        with self.assertRaises(OrionisIntegrityException):
            MySQL(collation='INVALID')

    async def testPrefixValidation(self):
        """
        Test prefix attribute validation.

        Ensures that non-string prefixes raise exceptions.

        Raises
        ------
        OrionisIntegrityException
            If the prefix value is invalid.
        """
        with self.assertRaises(OrionisIntegrityException):
            MySQL(prefix=123)

    async def testPrefixIndexesValidation(self):
        """
        Test prefix_indexes attribute validation.

        Ensures that non-boolean values raise exceptions.

        Raises
        ------
        OrionisIntegrityException
            If the prefix_indexes value is invalid.
        """
        with self.assertRaises(OrionisIntegrityException):
            MySQL(prefix_indexes='true')
        with self.assertRaises(OrionisIntegrityException):
            MySQL(prefix_indexes=1)

    async def testStrictValidation(self):
        """
        Test strict attribute validation.

        Ensures that non-boolean values raise exceptions.

        Raises
        ------
        OrionisIntegrityException
            If the strict value is invalid.
        """
        with self.assertRaises(OrionisIntegrityException):
            MySQL(strict='true')
        with self.assertRaises(OrionisIntegrityException):
            MySQL(strict=1)

    async def testEngineValidation(self):
        """
        Test engine attribute validation.

        Ensures enum conversion and invalid value handling.

        Raises
        ------
        OrionisIntegrityException
            If the engine value is invalid.
        """
        # Test string conversion
        mysql = MySQL(engine='MYISAM')
        self.assertEqual(mysql.engine, MySQLEngine.MYISAM.value)

        # Test enum assignment
        mysql = MySQL(engine=MySQLEngine.MEMORY)
        self.assertEqual(mysql.engine, MySQLEngine.MEMORY.value)

        # Test invalid value
        with self.assertRaises(OrionisIntegrityException):
            MySQL(engine='INVALID')

    async def testToDictMethod(self):
        """
        Test that toDict returns proper dictionary representation.

        Ensures all attributes are correctly included in dictionary.
        """
        mysql = MySQL()
        mysql_dict = mysql.toDict()
        self.assertEqual(mysql_dict['driver'], 'mysql')
        self.assertEqual(mysql_dict['host'], '127.0.0.1')
        self.assertEqual(mysql_dict['port'], 3306)
        self.assertEqual(mysql_dict['database'], 'orionis')
        self.assertEqual(mysql_dict['username'], 'root')
        self.assertEqual(mysql_dict['password'], '')
        self.assertEqual(mysql_dict['unix_socket'], '')
        self.assertEqual(mysql_dict['charset'], MySQLCharset.UTF8MB4.value)
        self.assertEqual(mysql_dict['collation'], MySQLCollation.UTF8MB4_UNICODE_CI.value)
        self.assertEqual(mysql_dict['prefix'], '')
        self.assertTrue(mysql_dict['prefix_indexes'])
        self.assertTrue(mysql_dict['strict'])
        self.assertEqual(mysql_dict['engine'], MySQLEngine.INNODB.value)

    async def testCustomValues(self):
        """
        Test that custom values are properly stored and validated.

        Ensures custom configuration values are correctly handled.
        """
        custom_mysql = MySQL(
            host='db.example.com',
            port=3307,
            database='custom_db',
            username='admin',
            password='secure123',
            unix_socket='/var/run/mysqld/mysqld.sock',
            charset='LATIN1',
            collation='LATIN1_GENERAL_CI',
            prefix='app_',
            prefix_indexes=False,
            strict=False,
            engine='MEMORY'
        )
        self.assertEqual(custom_mysql.host, 'db.example.com')
        self.assertEqual(custom_mysql.port, 3307)
        self.assertEqual(custom_mysql.database, 'custom_db')
        self.assertEqual(custom_mysql.username, 'admin')
        self.assertEqual(custom_mysql.password, 'secure123')
        self.assertEqual(custom_mysql.unix_socket, '/var/run/mysqld/mysqld.sock')
        self.assertEqual(custom_mysql.charset, MySQLCharset.LATIN1.value)
        self.assertEqual(custom_mysql.collation, MySQLCollation.LATIN1_GENERAL_CI.value)
        self.assertEqual(custom_mysql.prefix, 'app_')
        self.assertFalse(custom_mysql.prefix_indexes)
        self.assertFalse(custom_mysql.strict)
        self.assertEqual(custom_mysql.engine, MySQLEngine.MEMORY.value)