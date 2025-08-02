from orionis.foundation.config.session.entities.session import Session
from orionis.foundation.config.session.enums.same_site_policy import SameSitePolicy
from orionis.foundation.exceptions import OrionisIntegrityException
from orionis.test.cases.asynchronous import AsyncTestCase

class TestFoundationConfigSession(AsyncTestCase):

    async def testDefaultInitialization(self):
        """
        Test that Session instance is initialized with correct default values.

        Notes
        -----
        Verifies default values for all attributes including secret_key generation.
        """
        session = Session()
        self.assertIsInstance(session.secret_key, str)
        self.assertEqual(session.session_cookie, "orionis_session")
        self.assertEqual(session.max_age, 1800)
        self.assertEqual(session.same_site, SameSitePolicy.LAX.value)
        self.assertEqual(session.path, "/")
        self.assertFalse(session.https_only)
        self.assertIsNone(session.domain)

    async def testSecretKeyValidation(self):
        """
        Test validation for secret_key attribute.

        Notes
        -----
        Verifies that invalid secret keys raise OrionisIntegrityException.
        """
        with self.assertRaises(OrionisIntegrityException):
            Session(secret_key="")  # Empty string
        with self.assertRaises(OrionisIntegrityException):
            Session(secret_key=123)  # Non-string value

    async def testSessionCookieValidation(self):
        """
        Test validation for session_cookie attribute.

        Notes
        -----
        Verifies invalid cookie names raise OrionisIntegrityException.
        """
        with self.assertRaises(OrionisIntegrityException):
            Session(session_cookie="")  # Empty string
        with self.assertRaises(OrionisIntegrityException):
            Session(session_cookie="my session")  # Contains space
        with self.assertRaises(OrionisIntegrityException):
            Session(session_cookie="session;")  # Contains semicolon

    async def testMaxAgeValidation(self):
        """
        Test validation for max_age attribute.

        Notes
        -----
        Verifies invalid max_age values raise OrionisIntegrityException.
        """
        with self.assertRaises(OrionisIntegrityException):
            Session(max_age="3600")  # String instead of int
        with self.assertRaises(OrionisIntegrityException):
            Session(max_age=-1)  # Negative value
        # Test None is acceptable
        session = Session(max_age=None)
        self.assertIsNone(session.max_age)

    async def testSameSiteValidation(self):
        """
        Test validation and normalization for same_site attribute.

        Notes
        -----
        Verifies both string and enum inputs are properly handled.
        """
        # Test string inputs (case-insensitive)
        session1 = Session(same_site="strict")
        self.assertEqual(session1.same_site, SameSitePolicy.STRICT.value)
        session2 = Session(same_site="NONE")
        self.assertEqual(session2.same_site, SameSitePolicy.NONE.value)

        # Test enum inputs
        session3 = Session(same_site=SameSitePolicy.LAX)
        self.assertEqual(session3.same_site, SameSitePolicy.LAX.value)

        # Test invalid inputs
        with self.assertRaises(OrionisIntegrityException):
            Session(same_site="invalid")
        with self.assertRaises(OrionisIntegrityException):
            Session(same_site=123)

    async def testPathValidation(self):
        """
        Test validation for path attribute.

        Notes
        -----
        Verifies invalid paths raise OrionisIntegrityException.
        """
        with self.assertRaises(OrionisIntegrityException):
            Session(path="")  # Empty string
        with self.assertRaises(OrionisIntegrityException):
            Session(path="api")  # Doesn't start with /
        with self.assertRaises(OrionisIntegrityException):
            Session(path=123)  # Non-string value

    async def testHttpsOnlyValidation(self):
        """
        Test validation for https_only attribute.

        Notes
        -----
        Verifies non-boolean values raise OrionisIntegrityException.
        """
        with self.assertRaises(OrionisIntegrityException):
            Session(https_only="true")  # String instead of bool
        with self.assertRaises(OrionisIntegrityException):
            Session(https_only=1)  # Integer instead of bool

    async def testDomainValidation(self):
        """
        Test validation for domain attribute.

        Notes
        -----
        Verifies invalid domains raise OrionisIntegrityException.
        """
        with self.assertRaises(OrionisIntegrityException):
            Session(domain=".example.com")  # Starts with dot
        with self.assertRaises(OrionisIntegrityException):
            Session(domain="example.com.")  # Ends with dot
        with self.assertRaises(OrionisIntegrityException):
            Session(domain="example..com")  # Contains consecutive dots

        # Test None is acceptable
        session = Session(domain=None)
        self.assertIsNone(session.domain)

    async def testToDictMethod(self):
        """
        Test the toDict method returns proper dictionary representation.

        Notes
        -----
        Verifies all fields are included with correct values.
        """
        session = Session()
        result = session.toDict()
        self.assertIsInstance(result, dict)
        self.assertIn("secret_key", result)
        self.assertEqual(result["session_cookie"], "orionis_session")
        self.assertEqual(result["max_age"], 1800)
        self.assertEqual(result["same_site"], SameSitePolicy.LAX.value)
        self.assertEqual(result["path"], "/")
        self.assertFalse(result["https_only"])
        self.assertIsNone(result["domain"])

    async def testKwOnlyInitialization(self):
        """
        Test that Session requires keyword arguments for initialization.

        Notes
        -----
        Verifies the class enforces kw_only=True in its dataclass decorator.
        """
        with self.assertRaises(TypeError):
            Session("key", "session")