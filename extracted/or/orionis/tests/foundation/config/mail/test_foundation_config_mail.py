from orionis.foundation.config.mail.entities.mail import Mail
from orionis.foundation.config.mail.entities.mailers import Mailers
from orionis.foundation.exceptions.integrity import OrionisIntegrityException
from orionis.test.cases.asynchronous import AsyncTestCase

class TestFoundationConfigMail(AsyncTestCase):
    """
    Test suite for the Mail class, covering initialization, validation, and utility methods.
    """

    async def testDefaultInitialization(self):
        """
        Test default initialization of Mail.

        Tests that a Mail instance is initialized with the correct default values.

        Returns
        -------
        None

        Raises
        ------
        AssertionError
            If the default mailer is not 'smtp' or mailers is not an instance of Mailers.
        """
        mail = Mail()
        self.assertEqual(mail.default, "smtp")
        self.assertIsInstance(mail.mailers, Mailers)

    async def testDefaultValidation(self):
        """
        Test validation of the default mailer.

        Ensures that providing an invalid default mailer raises an exception.

        Returns
        -------
        None

        Raises
        ------
        OrionisIntegrityException
            If the default mailer is invalid or not a string.
        """
        with self.assertRaises(OrionisIntegrityException):
            Mail(default="invalid_mailer")
        with self.assertRaises(OrionisIntegrityException):
            Mail(default=123)

    async def testMailersTypeValidation(self):
        """
        Test type validation for the mailers attribute.

        Ensures that assigning a non-Mailers object to mailers raises an exception.

        Returns
        -------
        None

        Raises
        ------
        OrionisIntegrityException
            If mailers is not an instance of Mailers.
        """
        with self.assertRaises(OrionisIntegrityException):
            Mail(mailers="invalid_mailers_object")

    async def testToDictMethod(self):
        """
        Test the toDict method.

        Checks that the toDict method returns a dictionary representation of the Mail instance.

        Returns
        -------
        None

        Raises
        ------
        AssertionError
            If the returned value is not a dict or missing expected fields.
        """
        mail = Mail()
        result = mail.toDict()
        self.assertIsInstance(result, dict)
        self.assertIn("default", result)
        self.assertIn("mailers", result)
        self.assertEqual(result["default"], "smtp")

    async def testHashability(self):
        """
        Test hashability of Mail instances.

        Ensures that Mail instances are hashable and can be used in sets or as dictionary keys.

        Returns
        -------
        None

        Raises
        ------
        AssertionError
            If Mail instances are not hashable or set behavior is incorrect.
        """
        mail1 = Mail()
        mail2 = Mail(default="smtp")
        test_set = {mail1, mail2}
        self.assertEqual(len(test_set), 1)

    async def testKwOnlyInitialization(self):
        """
        Test keyword-only initialization enforcement.

        Ensures that Mail requires keyword arguments for initialization.

        Returns
        -------
        None

        Raises
        ------
        TypeError
            If positional arguments are used for initialization.
        """
        with self.assertRaises(TypeError):
            Mail("smtp", Mailers())

    async def testValidCustomInitialization(self):
        """
        Test valid custom initialization.

        Checks that a Mail instance can be created with valid, non-default values.

        Returns
        -------
        None

        Raises
        ------
        AssertionError
            If the instance is not initialized with the provided values.
        """
        mail = Mail(default="smtp", mailers=Mailers())
        self.assertEqual(mail.default, "smtp")
        self.assertIsInstance(mail.mailers, Mailers)