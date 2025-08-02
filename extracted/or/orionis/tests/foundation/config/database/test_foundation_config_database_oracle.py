from orionis.foundation.config.database.entities.oracle import Oracle
from orionis.foundation.config.database.enums.oracle_encoding import OracleEncoding
from orionis.foundation.config.database.enums.oracle_nencoding import OracleNencoding
from orionis.foundation.exceptions.integrity import OrionisIntegrityException
from orionis.test.cases.asynchronous import AsyncTestCase

class TestFoundationConfigDatabaseOracle(AsyncTestCase):
    """
    Test cases for the Oracle database configuration class.

    Notes
    -----
    This class contains asynchronous unit tests for the `Oracle` configuration entity,
    validating its attributes, value constraints, and dictionary serialization.
    """

    async def testDefaultValues(self):
        """
        Test Oracle instance creation with default values.

        Ensures that all default attribute values match the expected defaults
        as defined in the class.

        Raises
        ------
        AssertionError
            If any default value does not match the expected value.
        """
        oracle = Oracle()
        self.assertEqual(oracle.driver, 'oracle')
        self.assertEqual(oracle.username, 'sys')
        self.assertEqual(oracle.password, '')
        self.assertEqual(oracle.host, 'localhost')
        self.assertEqual(oracle.port, 1521)
        self.assertEqual(oracle.service_name, 'ORCL')
        self.assertIsNone(oracle.sid)
        self.assertIsNone(oracle.dsn)
        self.assertIsNone(oracle.tns_name)
        self.assertEqual(oracle.encoding, OracleEncoding.AL32UTF8.value)
        self.assertEqual(oracle.nencoding, OracleNencoding.AL32UTF8.value)

    async def testDriverValidation(self):
        """
        Test validation of the `driver` attribute.

        Ensures that only the value 'oracle' is accepted for the driver.

        Raises
        ------
        OrionisIntegrityException
            If the driver value is invalid.
        """
        with self.assertRaises(OrionisIntegrityException):
            Oracle(driver='')
        with self.assertRaises(OrionisIntegrityException):
            Oracle(driver='postgres')
        with self.assertRaises(OrionisIntegrityException):
            Oracle(driver=123)

    async def testUsernameValidation(self):
        """
        Test validation of the `username` attribute.

        Ensures that empty or non-string usernames raise exceptions.

        Raises
        ------
        OrionisIntegrityException
            If the username is invalid.
        """
        with self.assertRaises(OrionisIntegrityException):
            Oracle(username='')
        with self.assertRaises(OrionisIntegrityException):
            Oracle(username=123)

    async def testPasswordValidation(self):
        """
        Test validation of the `password` attribute.

        Ensures that non-string passwords raise exceptions.

        Raises
        ------
        OrionisIntegrityException
            If the password is invalid.
        """
        with self.assertRaises(OrionisIntegrityException):
            Oracle(password=123)

    async def testHostValidation(self):
        """
        Test validation of the `host` attribute when not using DSN/TNS.

        Ensures that empty or non-string hosts raise exceptions.

        Raises
        ------
        OrionisIntegrityException
            If the host is invalid.
        """
        with self.assertRaises(OrionisIntegrityException):
            Oracle(host='', dsn=None, tns_name=None)
        with self.assertRaises(OrionisIntegrityException):
            Oracle(host=123, dsn=None, tns_name=None)

    async def testPortValidation(self):
        """
        Test validation of the `port` attribute when not using DSN/TNS.

        Ensures that invalid port numbers raise exceptions.

        Raises
        ------
        OrionisIntegrityException
            If the port is invalid.
        """
        with self.assertRaises(OrionisIntegrityException):
            Oracle(port=0, dsn=None, tns_name=None)
        with self.assertRaises(OrionisIntegrityException):
            Oracle(port=65536, dsn=None, tns_name=None)
        with self.assertRaises(OrionisIntegrityException):
            Oracle(port='1521', dsn=None, tns_name=None)

    async def testServiceNameAndSidValidation(self):
        """
        Test validation of `service_name` and `sid` attributes when not using DSN/TNS.

        Ensures that at least one of `service_name` or `sid` is required.

        Raises
        ------
        OrionisIntegrityException
            If both `service_name` and `sid` are missing.
        """
        # Test with neither service_name nor sid
        with self.assertRaises(OrionisIntegrityException):
            Oracle(service_name=None, sid=None, dsn=None, tns_name=None)

        # Test valid with service_name only
        try:
            Oracle(service_name='ORCL', sid=None, dsn=None, tns_name=None)
        except OrionisIntegrityException:
            self.fail("Valid service_name should not raise exception")

        # Test valid with sid only
        try:
            Oracle(service_name=None, sid='XE', dsn=None, tns_name=None)
        except OrionisIntegrityException:
            self.fail("Valid sid should not raise exception")

    async def testDsnValidation(self):
        """
        Test validation of the `dsn` attribute.

        Ensures that `dsn` must be a non-empty string or None.

        Raises
        ------
        OrionisIntegrityException
            If the dsn is invalid.
        """
        with self.assertRaises(OrionisIntegrityException):
            Oracle(dsn='')
        try:
            Oracle(dsn='valid_dsn_string')
        except OrionisIntegrityException:
            self.fail("Valid dsn should not raise exception")

    async def testTnsNameValidation(self):
        """
        Test validation of the `tns_name` attribute.

        Ensures that `tns_name` must be a non-empty string or None.

        Raises
        ------
        OrionisIntegrityException
            If the tns_name is invalid.
        """
        with self.assertRaises(OrionisIntegrityException):
            Oracle(tns_name='')
        try:
            Oracle(tns_name='valid_tns_name')
        except OrionisIntegrityException:
            self.fail("Valid tns_name should not raise exception")

    async def testEncodingValidation(self):
        """
        Test validation of the `encoding` attribute.

        Ensures correct enum conversion and invalid value handling.

        Raises
        ------
        OrionisIntegrityException
            If the encoding value is invalid.
        """
        # Test enum assignment
        oracle = Oracle(encoding=OracleEncoding.WE8ISO8859P1)
        self.assertEqual(oracle.encoding, OracleEncoding.WE8ISO8859P1.value)

        # Test invalid value
        with self.assertRaises(OrionisIntegrityException):
            Oracle(encoding='INVALID')

    async def testNencodingValidation(self):
        """
        Test validation of the `nencoding` attribute.

        Ensures correct enum conversion and invalid value handling.

        Raises
        ------
        OrionisIntegrityException
            If the nencoding value is invalid.
        """
        # Test string conversion
        oracle = Oracle(nencoding='EE8MSWIN1250')
        self.assertEqual(oracle.nencoding, OracleNencoding.EE8MSWIN1250.value)

        # Test enum assignment
        oracle = Oracle(nencoding=OracleNencoding.ZHS16GBK)
        self.assertEqual(oracle.nencoding, OracleNencoding.ZHS16GBK.value)

        # Test invalid value
        with self.assertRaises(OrionisIntegrityException):
            Oracle(nencoding='INVALID')

    async def testToDictMethod(self):
        """
        Test the `toDict` method for dictionary representation.

        Ensures that all attributes are correctly included in the dictionary.

        Raises
        ------
        AssertionError
            If any attribute is missing or incorrect in the dictionary.
        """
        oracle = Oracle()
        oracle_dict = oracle.toDict()

        self.assertEqual(oracle_dict['driver'], 'oracle')
        self.assertEqual(oracle_dict['username'], 'sys')
        self.assertEqual(oracle_dict['password'], '')
        self.assertEqual(oracle_dict['host'], 'localhost')
        self.assertEqual(oracle_dict['port'], 1521)
        self.assertEqual(oracle_dict['service_name'], 'ORCL')
        self.assertIsNone(oracle_dict['sid'])
        self.assertIsNone(oracle_dict['dsn'])
        self.assertIsNone(oracle_dict['tns_name'])
        self.assertEqual(oracle_dict['encoding'], OracleEncoding.AL32UTF8.value)
        self.assertEqual(oracle_dict['nencoding'], OracleNencoding.AL32UTF8.value)

    async def testConnectionMethods(self):
        """
        Test handling of different Oracle connection methods.

        Ensures that DSN, TNS, or host/port/service/sid combinations are valid.

        Raises
        ------
        OrionisIntegrityException
            If a valid connection method raises an exception.
        """
        # Test DSN connection
        try:
            Oracle(dsn='valid_dsn', host=None, port=None, service_name=None, sid=None)
        except OrionisIntegrityException:
            self.fail("Valid DSN connection should not raise exception")

        # Test TNS connection
        try:
            Oracle(tns_name='valid_tns', host=None, port=None, service_name=None, sid=None)
        except OrionisIntegrityException:
            self.fail("Valid TNS connection should not raise exception")

        # Test host/port/service connection
        try:
            Oracle(dsn=None, tns_name=None, host='localhost', port=1521, service_name='ORCL')
        except OrionisIntegrityException:
            self.fail("Valid host/port/service connection should not raise exception")

        # Test host/port/sid connection
        try:
            Oracle(dsn=None, tns_name=None, host='localhost', port=1521, sid='XE')
        except OrionisIntegrityException:
            self.fail("Valid host/port/sid connection should not raise exception")