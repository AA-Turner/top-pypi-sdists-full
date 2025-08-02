from orionis.foundation.config.mail.entities.smtp import Smtp
from orionis.foundation.exceptions.integrity import OrionisIntegrityException
from orionis.test.cases.asynchronous import AsyncTestCase

class TestFoundationConfigMailSmtp(AsyncTestCase):
    """
    Unit tests for the Smtp configuration entity.

    This test suite validates the default initialization, type validation,
    attribute-specific validation, custom initialization, dictionary conversion,
    and keyword-only enforcement for the Smtp class.
    """

    async def testDefaultInitialization(self):
        """
        Test default initialization of Smtp.

        Ensures that an Smtp instance is initialized with the correct default values.

        Returns
        -------
        None
        """
        smtp = Smtp()
        self.assertEqual(smtp.url, "smtp.mailtrap.io")
        self.assertEqual(smtp.host, "smtp.mailtrap.io")
        self.assertEqual(smtp.port, 587)
        self.assertEqual(smtp.encryption, "TLS")
        self.assertEqual(smtp.username, "")
        self.assertEqual(smtp.password, "")
        self.assertIsNone(smtp.timeout)

    async def testTypeValidation(self):
        """
        Test type validation for Smtp attributes.

        Ensures that providing invalid types for Smtp attributes raises
        OrionisIntegrityException.

        Returns
        -------
        None
        """
        with self.assertRaises(OrionisIntegrityException):
            Smtp(url=123)
        with self.assertRaises(OrionisIntegrityException):
            Smtp(host=456)
        with self.assertRaises(OrionisIntegrityException):
            Smtp(port="invalid")
        with self.assertRaises(OrionisIntegrityException):
            Smtp(encryption=123)
        with self.assertRaises(OrionisIntegrityException):
            Smtp(username=123)
        with self.assertRaises(OrionisIntegrityException):
            Smtp(password=123)
        with self.assertRaises(OrionisIntegrityException):
            Smtp(timeout="invalid")

    async def testPortValidation(self):
        """
        Test validation for the port attribute.

        Ensures that negative port numbers raise OrionisIntegrityException.

        Returns
        -------
        None
        """
        with self.assertRaises(OrionisIntegrityException):
            Smtp(port=-1)

    async def testTimeoutValidation(self):
        """
        Test validation for the timeout attribute.

        Ensures that negative timeout values raise OrionisIntegrityException.

        Returns
        -------
        None
        """
        with self.assertRaises(OrionisIntegrityException):
            Smtp(timeout=-1)

    async def testValidCustomInitialization(self):
        """
        Test custom initialization with valid parameters.

        Ensures that valid custom values are accepted and stored correctly.

        Returns
        -------
        None
        """
        custom_config = Smtp(
            url="smtp.example.com",
            host="mail.example.com",
            port=465,
            encryption="SSL",
            username="user",
            password="pass",
            timeout=30
        )
        self.assertEqual(custom_config.url, "smtp.example.com")
        self.assertEqual(custom_config.host, "mail.example.com")
        self.assertEqual(custom_config.port, 465)
        self.assertEqual(custom_config.encryption, "SSL")
        self.assertEqual(custom_config.username, "user")
        self.assertEqual(custom_config.password, "pass")
        self.assertEqual(custom_config.timeout, 30)

    async def testToDictMethod(self):
        """
        Test the toDict method of Smtp.

        Ensures that the toDict method returns a dictionary containing all fields
        with correct values.

        Returns
        -------
        None
        """
        smtp = Smtp()
        result = smtp.toDict()
        self.assertIsInstance(result, dict)
        self.assertEqual(result["url"], "smtp.mailtrap.io")
        self.assertEqual(result["host"], "smtp.mailtrap.io")
        self.assertEqual(result["port"], 587)
        self.assertEqual(result["encryption"], "TLS")
        self.assertEqual(result["username"], "")
        self.assertEqual(result["password"], "")
        self.assertIsNone(result["timeout"])

    async def testKwOnlyInitialization(self):
        """
        Test keyword-only initialization enforcement.

        Ensures that Smtp requires keyword arguments for initialization and
        enforces kw_only=True in its dataclass decorator.

        Returns
        -------
        None
        """
        with self.assertRaises(TypeError):
            Smtp("smtp.mailtrap.io", "smtp.mailtrap.io", 587, "TLS", "", "", None)