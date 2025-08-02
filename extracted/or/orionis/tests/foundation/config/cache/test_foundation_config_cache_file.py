from orionis.foundation.config.cache.entities.file import File
from orionis.foundation.exceptions.integrity import OrionisIntegrityException
from orionis.test.cases.asynchronous import AsyncTestCase

class TestFoundationConfigCacheFile(AsyncTestCase):
    """
    Unit tests for the File cache configuration dataclass.

    These tests validate the initialization, attribute validation, and dictionary representation
    of the File cache configuration entity.
    """

    async def testDefaultPath(self):
        """
        Test default path initialization.

        Ensures that a File instance is created with the correct default path.

        Returns
        -------
        None
        """
        file_config = File()
        self.assertEqual(file_config.path, 'storage/framework/cache/data')

    async def testCustomPath(self):
        """
        Test custom path initialization.

        Ensures that a custom path can be set during initialization and is stored correctly.

        Returns
        -------
        None
        """
        custom_path = 'custom/cache/path'
        file_config = File(path=custom_path)
        self.assertEqual(file_config.path, custom_path)

    async def testEmptyPathValidation(self):
        """
        Test validation for empty path.

        Ensures that providing an empty path raises an OrionisIntegrityException.

        Returns
        -------
        None

        Raises
        ------
        OrionisIntegrityException
            If the path is empty.
        """
        with self.assertRaises(OrionisIntegrityException):
            File(path="")

    async def testPathTypeValidation(self):
        """
        Test validation for path type.

        Ensures that non-string path values raise an OrionisIntegrityException.

        Returns
        -------
        None

        Raises
        ------
        OrionisIntegrityException
            If the path is not a string.
        """
        with self.assertRaises(OrionisIntegrityException):
            File(path=123)

        with self.assertRaises(OrionisIntegrityException):
            File(path=None)

        with self.assertRaises(OrionisIntegrityException):
            File(path=[])

    async def testToDictMethod(self):
        """
        Test dictionary representation.

        Ensures that the toDict method returns a dictionary with the expected path value.

        Returns
        -------
        None
        """
        file_config = File()
        config_dict = file_config.toDict()

        self.assertIsInstance(config_dict, dict)
        self.assertEqual(config_dict['path'], 'storage/framework/cache/data')

    async def testCustomPathToDict(self):
        """
        Test custom path in dictionary representation.

        Ensures that custom paths are properly included in the dictionary returned by toDict.

        Returns
        -------
        None
        """
        custom_path = 'another/cache/location'
        file_config = File(path=custom_path)
        config_dict = file_config.toDict()

        self.assertEqual(config_dict['path'], custom_path)

    async def testWhitespacePathHandling(self):
        """
        Test handling of paths with whitespace.

        Ensures that paths containing whitespace are accepted and not automatically trimmed.

        Returns
        -------
        None
        """
        spaced_path = '  storage/cache/with/space  '
        file_config = File(path=spaced_path)
        self.assertEqual(file_config.path, spaced_path)