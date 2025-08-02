from orionis.foundation.config.cors.entities.cors import Cors
from orionis.foundation.exceptions.integrity import OrionisIntegrityException
from orionis.test.cases.asynchronous import AsyncTestCase

class TestFoundationConfigCors(AsyncTestCase):
    """
    Unit tests for Cors configuration defaults and validation.

    Notes
    -----
    These tests verify the default values, custom value assignment, and type validation
    for the `Cors` configuration entity.
    """

    async def testDefaultValues(self):
        """
        Test the default values of the Cors configuration.

        Verifies that a newly instantiated Cors object has the expected default settings.

        Expected Defaults
        -----------------
        allow_origins : list of str
            ["*"]
        allow_origin_regex : None or str
            None
        allow_methods : list of str
            ["*"]
        allow_headers : list of str
            ["*"]
        expose_headers : list of str
            []
        allow_credentials : bool
            False
        max_age : int
            600
        """
        cors = Cors()
        self.assertEqual(cors.allow_origins, ["*"])
        self.assertIsNone(cors.allow_origin_regex)
        self.assertEqual(cors.allow_methods, ["*"])
        self.assertEqual(cors.allow_headers, ["*"])
        self.assertEqual(cors.expose_headers, [])
        self.assertFalse(cors.allow_credentials)
        self.assertEqual(cors.max_age, 600)

    async def testCustomValues(self):
        """
        Test custom value assignment for all Cors configuration parameters.

        Ensures that the Cors object accurately reflects the provided custom configuration values.

        Parameters
        ----------
        allow_origins : list of str
            Custom list of allowed origins.
        allow_origin_regex : str
            Custom regex pattern for allowed origins.
        allow_methods : list of str
            Custom list of allowed HTTP methods.
        allow_headers : list of str
            Custom list of allowed headers.
        expose_headers : list of str
            Custom list of exposed headers.
        allow_credentials : bool
            Whether credentials are allowed.
        max_age : int
            Custom max age value.
        """
        cors = Cors(
            allow_origins=["https://example.com"],
            allow_origin_regex="^https://.*\\.example\\.com$",
            allow_methods=["GET", "POST"],
            allow_headers=["Authorization", "Content-Type"],
            expose_headers=["X-Custom-Header"],
            allow_credentials=True,
            max_age=3600
        )
        self.assertEqual(cors.allow_origins, ["https://example.com"])
        self.assertEqual(cors.allow_origin_regex, "^https://.*\\.example\\.com$")
        self.assertEqual(cors.allow_methods, ["GET", "POST"])
        self.assertEqual(cors.allow_headers, ["Authorization", "Content-Type"])
        self.assertEqual(cors.expose_headers, ["X-Custom-Header"])
        self.assertTrue(cors.allow_credentials)
        self.assertEqual(cors.max_age, 3600)

    async def testInvalidAllowOriginsType(self):
        """
        Test type validation for 'allow_origins' parameter.

        Ensures that passing a string instead of a list to the `allow_origins` parameter
        raises an OrionisIntegrityException.

        Raises
        ------
        OrionisIntegrityException
            If `allow_origins` is not a list.
        """
        with self.assertRaises(OrionisIntegrityException):
            Cors(allow_origins="*")

    async def testInvalidAllowOriginRegexType(self):
        """
        Test type validation for 'allow_origin_regex' parameter.

        Ensures that passing a non-string, non-None value (e.g., integer) to the
        `allow_origin_regex` parameter raises an OrionisIntegrityException.

        Raises
        ------
        OrionisIntegrityException
            If `allow_origin_regex` is not a string or None.
        """
        with self.assertRaises(OrionisIntegrityException):
            Cors(allow_origin_regex=123)

    async def testInvalidAllowMethodsType(self):
        """
        Test type validation for 'allow_methods' parameter.

        Ensures that passing a string instead of a list to the `allow_methods` parameter
        raises an OrionisIntegrityException.

        Raises
        ------
        OrionisIntegrityException
            If `allow_methods` is not a list.
        """
        with self.assertRaises(OrionisIntegrityException):
            Cors(allow_methods="GET")

    async def testInvalidAllowHeadersType(self):
        """
        Test type validation for 'allow_headers' parameter.

        Ensures that passing a string instead of a list to the `allow_headers` parameter
        raises an OrionisIntegrityException.

        Raises
        ------
        OrionisIntegrityException
            If `allow_headers` is not a list.
        """
        with self.assertRaises(OrionisIntegrityException):
            Cors(allow_headers="Authorization")

    async def testInvalidExposeHeadersType(self):
        """
        Test type validation for 'expose_headers' parameter.

        Ensures that passing a string instead of a list to the `expose_headers` parameter
        raises an OrionisIntegrityException.

        Raises
        ------
        OrionisIntegrityException
            If `expose_headers` is not a list.
        """
        with self.assertRaises(OrionisIntegrityException):
            Cors(expose_headers="X-Custom-Header")

    async def testInvalidAllowCredentialsType(self):
        """
        Test type validation for 'allow_credentials' parameter.

        Ensures that passing a non-boolean value to the `allow_credentials` parameter
        raises an OrionisIntegrityException.

        Raises
        ------
        OrionisIntegrityException
            If `allow_credentials` is not a boolean.
        """
        with self.assertRaises(OrionisIntegrityException):
            Cors(allow_credentials="yes")

    async def testInvalidMaxAgeType(self):
        """
        Test type validation for 'max_age' parameter.

        Ensures that passing a non-integer value (e.g., string) to the `max_age` parameter
        raises an OrionisIntegrityException.

        Raises
        ------
        OrionisIntegrityException
            If `max_age` is not an integer or None.
        """
        with self.assertRaises(OrionisIntegrityException):
            Cors(max_age="3600")