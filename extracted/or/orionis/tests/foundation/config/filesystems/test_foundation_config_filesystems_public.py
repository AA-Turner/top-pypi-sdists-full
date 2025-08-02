from orionis.foundation.exceptions.integrity import OrionisIntegrityException
from orionis.foundation.config.filesystems.entitites.public import Public
from orionis.test.cases.asynchronous import AsyncTestCase

class TestFoundationConfigFilesystemsPublic(AsyncTestCase):
    """
    Test cases for the Public storage configuration class.

    This class contains asynchronous unit tests for the `Public` storage configuration,
    validating default values, custom values, input validation, dictionary conversion,
    whitespace handling, hashability, and keyword-only initialization.

    Methods
    -------
    testDefaultValues()
        Test that Public instance is created with correct default values.
    testCustomValues()
        Test that custom path and url can be set during initialization.
    testEmptyPathValidation()
        Test that empty paths are rejected.
    testEmptyUrlValidation()
        Test that empty URLs are rejected.
    testTypeValidation()
        Test that non-string values are rejected for both attributes.
    testToDictMethod()
        Test that toDict returns proper dictionary representation.
    testCustomValuesToDict()
        Test that custom values are properly included in dictionary representation.
    testWhitespaceHandling()
        Test that values with whitespace are accepted but not automatically trimmed.
    testHashability()
        Test that Public maintains hashability due to unsafe_hash=True.
    testKwOnlyInitialization()
        Test that Public enforces keyword-only initialization.
    """

    async def testDefaultValues(self):
        """
        Test that Public instance is created with correct default values.

        Verifies both default path and url match expected values from class definition.
        """
        public = Public()
        self.assertEqual(public.path, "storage/app/public")
        self.assertEqual(public.url, "static")

    async def testCustomValues(self):
        """
        Test that custom path and url can be set during initialization.

        Verifies both attributes accept and store valid custom values.
        """
        custom_path = "custom/public/path"
        custom_url = "assets"
        public = Public(path=custom_path, url=custom_url)
        self.assertEqual(public.path, custom_path)
        self.assertEqual(public.url, custom_url)

    async def testEmptyPathValidation(self):
        """
        Test that empty paths are rejected.

        Verifies that an empty path raises OrionisIntegrityException.
        """
        with self.assertRaises(OrionisIntegrityException):
            Public(path="")

    async def testEmptyUrlValidation(self):
        """
        Test that empty URLs are rejected.

        Verifies that an empty url raises OrionisIntegrityException.
        """
        with self.assertRaises(OrionisIntegrityException):
            Public(url="")

    async def testTypeValidation(self):
        """
        Test that non-string values are rejected for both attributes.

        Verifies that non-string values raise OrionisIntegrityException.
        """
        # Test path validation
        with self.assertRaises(OrionisIntegrityException):
            Public(path=123)
        with self.assertRaises(OrionisIntegrityException):
            Public(path=None)

        # Test url validation
        with self.assertRaises(OrionisIntegrityException):
            Public(url=123)
        with self.assertRaises(OrionisIntegrityException):
            Public(url=None)

    async def testToDictMethod(self):
        """
        Test that toDict returns proper dictionary representation.

        Verifies the returned dictionary contains both default values.
        """
        public = Public()
        config_dict = public.toDict()

        self.assertIsInstance(config_dict, dict)
        self.assertEqual(config_dict['path'], "storage/app/public")
        self.assertEqual(config_dict['url'], "static")

    async def testCustomValuesToDict(self):
        """
        Test that custom values are properly included in dictionary representation.

        Verifies toDict() includes custom values when specified.
        """
        custom_path = "public/assets"
        custom_url = "cdn"
        public = Public(path=custom_path, url=custom_url)
        config_dict = public.toDict()

        self.assertEqual(config_dict['path'], custom_path)
        self.assertEqual(config_dict['url'], custom_url)

    async def testWhitespaceHandling(self):
        """
        Test that values with whitespace are accepted but not automatically trimmed.

        Verifies the validation allows values containing whitespace characters.
        """
        spaced_path = "  public/storage  "
        spaced_url = "  static/files  "
        public = Public(path=spaced_path, url=spaced_url)
        self.assertEqual(public.path, spaced_path)
        self.assertEqual(public.url, spaced_url)

    async def testHashability(self):
        """
        Test that Public maintains hashability due to unsafe_hash=True.

        Verifies that Public instances can be used in sets and as dictionary keys.
        """
        public1 = Public()
        public2 = Public()
        public_set = {public1, public2}

        self.assertEqual(len(public_set), 1)

        custom_public = Public(path="custom/public", url="custom-url")
        public_set.add(custom_public)
        self.assertEqual(len(public_set), 2)

    async def testKwOnlyInitialization(self):
        """
        Test that Public enforces keyword-only initialization.

        Verifies that positional arguments are not allowed for initialization.
        """
        with self.assertRaises(TypeError):
            Public("storage/path", "static")