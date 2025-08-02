from orionis.foundation.config.filesystems.entitites.disks import Disks
from orionis.foundation.config.filesystems.entitites.filesystems import Filesystems
from orionis.foundation.exceptions.integrity import OrionisIntegrityException
from orionis.test.cases.asynchronous import AsyncTestCase

class TestFoundationConfigFilesystems(AsyncTestCase):
    """
    Test cases for the Filesystems configuration class.

    This class contains unit tests for the `Filesystems` configuration class,
    including validation of default values, disk types, dictionary conversion,
    custom values, hashability, and keyword-only initialization.
    """

    async def testDefaultValues(self):
        """
        Test Filesystems instance creation with default values.

        Ensures that the default disk is set to 'local' and the disks attribute
        is properly initialized as a Disks instance.
        """
        fs = Filesystems()
        self.assertEqual(fs.default, "local")
        self.assertIsInstance(fs.disks, Disks)

    async def testDefaultDiskValidation(self):
        """
        Validate the default disk attribute.

        Checks that only valid disk types are accepted as default and that
        invalid types raise an OrionisIntegrityException.

        Raises
        ------
        OrionisIntegrityException
            If an invalid disk type is provided as default.
        """
        # Test valid disk types
        valid_disks = ["local", "public", "aws"]
        for disk in valid_disks:
            try:
                Filesystems(default=disk)
            except OrionisIntegrityException:
                self.fail(f"Valid disk type '{disk}' should not raise exception")

        # Test invalid disk type
        with self.assertRaises(OrionisIntegrityException):
            Filesystems(default="invalid_disk")

        # Test empty default
        with self.assertRaises(OrionisIntegrityException):
            Filesystems(default="")

        # Test non-string default
        with self.assertRaises(OrionisIntegrityException):
            Filesystems(default=123)

    async def testDisksValidation(self):
        """
        Validate the disks attribute.

        Ensures that only instances of Disks are accepted for the disks attribute.
        Invalid types should raise an OrionisIntegrityException.

        Raises
        ------
        OrionisIntegrityException
            If disks is not a Disks instance or is None.
        """
        # Test invalid disks type
        with self.assertRaises(OrionisIntegrityException):
            Filesystems(disks="not_a_disks_instance")

        # Test None disks
        with self.assertRaises(OrionisIntegrityException):
            Filesystems(disks=None)

        # Test valid disks
        try:
            Filesystems(disks=Disks())
        except OrionisIntegrityException:
            self.fail("Valid Disks instance should not raise exception")

    async def testToDictMethod(self):
        """
        Test the toDict method of Filesystems.

        Ensures that the method returns a dictionary representation of the
        Filesystems instance with all attributes correctly included.

        Returns
        -------
        dict
            Dictionary representation of the Filesystems instance.
        """
        fs = Filesystems()
        fs_dict = fs.toDict()

        self.assertIsInstance(fs_dict, dict)
        self.assertEqual(fs_dict['default'], "local")
        self.assertIsInstance(fs_dict['disks'], dict)

    async def testCustomValues(self):
        """
        Test custom values for Filesystems.

        Ensures that custom configurations are properly stored and validated.

        Parameters
        ----------
        custom_disks : Disks
            Custom Disks instance to be used in Filesystems.

        Returns
        -------
        None
        """
        custom_disks = Disks()
        custom_fs = Filesystems(
            default="aws",
            disks=custom_disks
        )
        self.assertEqual(custom_fs.default, "aws")
        self.assertIs(custom_fs.disks, custom_disks)

    async def testHashability(self):
        """
        Test hashability of Filesystems instances.

        Ensures that Filesystems instances are hashable and can be used in sets
        and as dictionary keys due to `unsafe_hash=True`.

        Returns
        -------
        None
        """
        fs1 = Filesystems()
        fs2 = Filesystems()
        fs_set = {fs1, fs2}

        self.assertEqual(len(fs_set), 1)

        custom_fs = Filesystems(default="public")
        fs_set.add(custom_fs)
        self.assertEqual(len(fs_set), 2)

    async def testKwOnlyInitialization(self):
        """
        Test keyword-only initialization enforcement.

        Ensures that Filesystems enforces keyword-only arguments and does not
        allow positional arguments during initialization.

        Raises
        ------
        TypeError
            If positional arguments are used for initialization.
        """
        with self.assertRaises(TypeError):
            Filesystems("local", Disks())