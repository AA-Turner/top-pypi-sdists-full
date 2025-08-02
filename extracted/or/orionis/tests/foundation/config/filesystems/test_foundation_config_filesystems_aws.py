from orionis.foundation.exceptions.integrity import OrionisIntegrityException
from orionis.foundation.config.filesystems.entitites.aws import S3
from orionis.test.cases.asynchronous import AsyncTestCase

class TestFoundationConfigFilesystemsAws(AsyncTestCase):
    """
    Test cases for the S3 storage configuration class.

    This class contains unit tests for the S3 configuration entity, ensuring
    correct default values, field validation, custom value handling, dictionary
    conversion, hashability, and keyword-only initialization.
    """

    async def testDefaultValues(self):
        """
        Test that S3 instance is created with correct default values.

        Verifies all default values match expected defaults from class definition.
        """
        s3 = S3()
        self.assertEqual(s3.key, "")
        self.assertEqual(s3.secret, "")
        self.assertEqual(s3.region, "us-east-1")
        self.assertEqual(s3.bucket, "")
        self.assertIsNone(s3.url)
        self.assertIsNone(s3.endpoint)
        self.assertFalse(s3.use_path_style_endpoint)
        self.assertFalse(s3.throw)

    async def testRequiredFieldValidation(self):
        """
        Test validation of required fields.

        Ensures that the 'region' field must be a non-empty string.

        Raises
        ------
        OrionisIntegrityException
            If 'region' is empty or not a string.
        """
        # Test empty region
        with self.assertRaises(OrionisIntegrityException):
            S3(region="")

        # Test non-string region
        with self.assertRaises(OrionisIntegrityException):
            S3(region=123)

    async def testOptionalFieldValidation(self):
        """
        Test validation of optional fields.

        Ensures that optional fields accept None or proper types.

        Raises
        ------
        OrionisIntegrityException
            If optional fields are not of the correct type.
        """
        # Valid optional configurations
        try:
            S3(url=None, endpoint=None)
            S3(url="https://example.com", endpoint="https://s3.example.com")
        except OrionisIntegrityException:
            self.fail("Valid optional configurations should not raise exceptions")

        # Invalid optional configurations
        with self.assertRaises(OrionisIntegrityException):
            S3(url=123)
        with self.assertRaises(OrionisIntegrityException):
            S3(endpoint=[])

    async def testBooleanFieldValidation(self):
        """
        Test validation of boolean fields.

        Ensures that boolean fields only accept boolean values.

        Raises
        ------
        OrionisIntegrityException
            If boolean fields are not of type bool.
        """
        # Test use_path_style_endpoint
        with self.assertRaises(OrionisIntegrityException):
            S3(use_path_style_endpoint="true")

        # Test throw
        with self.assertRaises(OrionisIntegrityException):
            S3(throw=1)

    async def testCustomValues(self):
        """
        Test that custom values are properly stored and validated.

        Ensures custom configuration values are correctly handled.

        """
        custom_s3 = S3(
            key="AKIAEXAMPLE",
            secret="secret123",
            region="eu-west-1",
            bucket="my-bucket",
            url="https://my-bucket.s3.amazonaws.com",
            endpoint="https://s3.eu-west-1.amazonaws.com",
            use_path_style_endpoint=True,
            throw=True
        )

        self.assertEqual(custom_s3.key, "AKIAEXAMPLE")
        self.assertEqual(custom_s3.secret, "secret123")
        self.assertEqual(custom_s3.region, "eu-west-1")
        self.assertEqual(custom_s3.bucket, "my-bucket")
        self.assertEqual(custom_s3.url, "https://my-bucket.s3.amazonaws.com")
        self.assertEqual(custom_s3.endpoint, "https://s3.eu-west-1.amazonaws.com")
        self.assertTrue(custom_s3.use_path_style_endpoint)
        self.assertTrue(custom_s3.throw)

    async def testToDictMethod(self):
        """
        Test that toDict returns proper dictionary representation.

        Ensures all attributes are correctly included in the dictionary.

        Returns
        -------
        dict
            Dictionary representation of the S3 instance.
        """
        s3 = S3()
        s3_dict = s3.toDict()

        self.assertIsInstance(s3_dict, dict)
        self.assertEqual(s3_dict['key'], "")
        self.assertEqual(s3_dict['secret'], "")
        self.assertEqual(s3_dict['region'], "us-east-1")
        self.assertEqual(s3_dict['bucket'], "")
        self.assertIsNone(s3_dict['url'])
        self.assertIsNone(s3_dict['endpoint'])
        self.assertFalse(s3_dict['use_path_style_endpoint'])
        self.assertFalse(s3_dict['throw'])

    async def testHashability(self):
        """
        Test that S3 maintains hashability due to unsafe_hash=True.

        Ensures that S3 instances can be used in sets and as dictionary keys.
        """
        s3_1 = S3()
        s3_2 = S3()
        s3_set = {s3_1, s3_2}

        self.assertEqual(len(s3_set), 1)

        custom_s3 = S3(bucket="custom-bucket")
        s3_set.add(custom_s3)
        self.assertEqual(len(s3_set), 2)

    async def testKwOnlyInitialization(self):
        """
        Test that S3 enforces keyword-only initialization.

        Ensures that positional arguments are not allowed for initialization.

        Raises
        ------
        TypeError
            If positional arguments are used for initialization.
        """
        with self.assertRaises(TypeError):
            S3("key", "secret", "region")  # Should fail as it requires keyword arguments