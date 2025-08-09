from orionis.foundation.exceptions.integrity import OrionisIntegrityException
from orionis.foundation.config.filesystems.entitites.public import Public
from orionis.test.cases.asynchronous import AsyncTestCase

class TestFoundationConfigFilesystemsPublic(AsyncTestCase):
    """
    Asynchronous unit tests for the `Public` storage configuration class.

    This class validates the behavior of the `Public` storage configuration, including
    default and custom value assignment, input validation, dictionary conversion,
    whitespace handling, hashability, and enforcement of keyword-only initialization.
    """

    async def testDefaultValues(self):
        """
        Test creation of a Public instance with default values.

        Ensures that the default `path` and `url` attributes are set as defined
        in the class.

        Returns
        -------
        None
        """
        public = Public()
        self.assertEqual(public.path, "storage/app/public")
        self.assertEqual(public.url, "static")

    async def testCustomValues(self):
        """
        Test assignment of custom values to path and url.

        Checks that custom `path` and `url` values are accepted and stored
        correctly during initialization.

        Returns
        -------
        None
        """
        custom_path = "custom/public/path"
        custom_url = "assets"
        public = Public(path=custom_path, url=custom_url)
        self.assertEqual(public.path, custom_path)
        self.assertEqual(public.url, custom_url)

    async def testEmptyPathValidation(self):
        """
        Test validation for empty path values.

        Verifies that providing an empty string for `path` raises
        OrionisIntegrityException.

        Returns
        -------
        None
        """
        with self.assertRaises(OrionisIntegrityException):
            Public(path="")

    async def testEmptyUrlValidation(self):
        """
        Test validation for empty url values.

        Verifies that providing an empty string for `url` raises
        OrionisIntegrityException.

        Returns
        -------
        None
        """
        with self.assertRaises(OrionisIntegrityException):
            Public(url="")

    async def testTypeValidation(self):
        """
        Test type validation for path and url attributes.

        Ensures that non-string values for `path` and `url` raise
        OrionisIntegrityException.

        Returns
        -------
        None
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
        Test the toDict method for correct dictionary output.

        Ensures that the dictionary representation contains the correct
        default values for `path` and `url`.

        Returns
        -------
        None
        """
        public = Public()
        config_dict = public.toDict()

        self.assertIsInstance(config_dict, dict)
        self.assertEqual(config_dict['path'], "storage/app/public")
        self.assertEqual(config_dict['url'], "static")

    async def testCustomValuesToDict(self):
        """
        Test dictionary output with custom values.

        Ensures that the dictionary representation includes custom
        `path` and `url` values when specified.

        Returns
        -------
        None
        """
        custom_path = "public/assets"
        custom_url = "cdn"
        public = Public(path=custom_path, url=custom_url)
        config_dict = public.toDict()

        self.assertEqual(config_dict['path'], custom_path)
        self.assertEqual(config_dict['url'], custom_url)

    async def testWhitespaceHandling(self):
        """
        Test handling of whitespace in attribute values.

        Verifies that values containing whitespace are accepted and
        not automatically trimmed.

        Returns
        -------
        None
        """
        spaced_path = "  public/storage  "
        spaced_url = "  static/files  "
        public = Public(path=spaced_path, url=spaced_url)
        self.assertEqual(public.path, spaced_path)
        self.assertEqual(public.url, spaced_url)

    async def testHashability(self):
        """
        Test hashability of Public instances.

        Ensures that Public instances are hashable and can be used in sets
        and as dictionary keys due to `unsafe_hash=True`.

        Returns
        -------
        None
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
        Test enforcement of keyword-only initialization.

        Verifies that positional arguments are not allowed when initializing
        a Public instance.

        Returns
        -------
        None
        """
        with self.assertRaises(TypeError):
            Public("storage/path", "static")