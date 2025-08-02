from orionis.foundation.config.filesystems.entitites.local import Local
from orionis.foundation.exceptions.integrity import OrionisIntegrityException
from orionis.test.cases.asynchronous import AsyncTestCase

class TestFoundationConfigFilesystemsLocal(AsyncTestCase):
    """
    Test cases for the Local storage configuration class.

    This class contains asynchronous unit tests for the `Local` storage configuration,
    validating path handling, dictionary conversion, hashability, and initialization constraints.
    """

    async def testDefaultPath(self):
        """
        Test Local instance creation with default path.

        Ensures that the default path of a Local instance matches the expected value.

        Returns
        -------
        None
        """
        local = Local()
        self.assertEqual(local.path, "storage/app/private")

    async def testCustomPath(self):
        """
        Test setting a custom path during initialization.

        Ensures that the path attribute accepts and stores valid custom paths.

        Returns
        -------
        None
        """
        custom_path = "custom/storage/path"
        local = Local(path=custom_path)
        self.assertEqual(local.path, custom_path)

    async def testEmptyPathValidation(self):
        """
        Test rejection of empty paths.

        Ensures that initializing Local with an empty path raises OrionisIntegrityException.

        Returns
        -------
        None
        """
        with self.assertRaises(OrionisIntegrityException):
            Local(path="")

    async def testPathTypeValidation(self):
        """
        Test rejection of non-string paths.

        Ensures that non-string path values raise OrionisIntegrityException.

        Returns
        -------
        None
        """
        with self.assertRaises(OrionisIntegrityException):
            Local(path=123)
        with self.assertRaises(OrionisIntegrityException):
            Local(path=None)
        with self.assertRaises(OrionisIntegrityException):
            Local(path=[])

    async def testToDictMethod(self):
        """
        Test dictionary representation of Local.

        Ensures that toDict returns a dictionary containing the expected path value.

        Returns
        -------
        None
        """
        local = Local()
        config_dict = local.toDict()
        self.assertIsInstance(config_dict, dict)
        self.assertEqual(config_dict['path'], "storage/app/private")

    async def testCustomPathToDict(self):
        """
        Test dictionary representation with custom path.

        Ensures that toDict includes custom path values when specified.

        Returns
        -------
        None
        """
        custom_path = "another/storage/location"
        local = Local(path=custom_path)
        config_dict = local.toDict()
        self.assertEqual(config_dict['path'], custom_path)

    async def testWhitespacePathHandling(self):
        """
        Test handling of paths with whitespace.

        Ensures that paths containing whitespace are accepted and not automatically trimmed.

        Returns
        -------
        None
        """
        spaced_path = "  storage/with/space  "
        local = Local(path=spaced_path)
        self.assertEqual(local.path, spaced_path)

    async def testHashability(self):
        """
        Test hashability of Local instances.

        Ensures that Local instances can be used in sets and as dictionary keys.

        Returns
        -------
        None
        """
        local1 = Local()
        local2 = Local()
        local_set = {local1, local2}
        self.assertEqual(len(local_set), 1)
        custom_local = Local(path="custom/path")
        local_set.add(custom_local)
        self.assertEqual(len(local_set), 2)

    async def testKwOnlyInitialization(self):
        """
        Test enforcement of keyword-only initialization.

        Ensures that positional arguments are not allowed for Local initialization.

        Returns
        -------
        None
        """
        with self.assertRaises(TypeError):
            Local("storage/path")