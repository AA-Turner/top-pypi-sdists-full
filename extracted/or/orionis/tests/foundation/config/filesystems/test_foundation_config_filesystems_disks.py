from orionis.foundation.config.filesystems.entitites.aws import S3
from orionis.foundation.config.filesystems.entitites.disks import Disks
from orionis.foundation.config.filesystems.entitites.local import Local
from orionis.foundation.config.filesystems.entitites.public import Public
from orionis.foundation.exceptions.integrity import OrionisIntegrityException
from orionis.test.cases.asynchronous import AsyncTestCase

class TestFoundationConfigFilesystemsDisks(AsyncTestCase):
    """
    Test cases for the Disks filesystem configuration class.

    This class contains unit tests to validate the behavior and integrity of the
    `Disks` configuration class, ensuring correct type validation, default values,
    custom configuration handling, dictionary conversion, hashability, and
    keyword-only initialization.

    Methods
    -------
    testDefaultValues()
        Test that Disks instance is created with correct default values.
    testLocalTypeValidation()
        Test local attribute type validation.
    testPublicTypeValidation()
        Test public attribute type validation.
    testAwsTypeValidation()
        Test aws attribute type validation.
    testCustomDiskConfigurations()
        Test that custom disk configurations are properly stored and validated.
    testToDictMethod()
        Test that toDict returns proper dictionary representation.
    testHashability()
        Test that Disks maintains hashability due to unsafe_hash=True.
    testKwOnlyInitialization()
        Test that Disks enforces keyword-only initialization.
    """

    async def testDefaultValues(self):
        """
        Test that Disks instance is created with correct default values.

        Ensures that all default disk configurations are properly initialized.

        Returns
        -------
        None
        """
        disks = Disks()
        self.assertIsInstance(disks.local, Local)
        self.assertIsInstance(disks.public, Public)
        self.assertIsInstance(disks.aws, S3)

    async def testLocalTypeValidation(self):
        """
        Test local attribute type validation.

        Ensures that only `Local` instances are accepted for the `local` attribute.

        Raises
        ------
        OrionisIntegrityException
            If the `local` attribute is not a `Local` instance.
        """
        with self.assertRaises(OrionisIntegrityException):
            Disks(local="not_a_local_instance")
        with self.assertRaises(OrionisIntegrityException):
            Disks(local=123)
        with self.assertRaises(OrionisIntegrityException):
            Disks(local=None)

    async def testPublicTypeValidation(self):
        """
        Test public attribute type validation.

        Ensures that only `Public` instances are accepted for the `public` attribute.

        Raises
        ------
        OrionisIntegrityException
            If the `public` attribute is not a `Public` instance.
        """
        with self.assertRaises(OrionisIntegrityException):
            Disks(public="not_a_public_instance")
        with self.assertRaises(OrionisIntegrityException):
            Disks(public=123)
        with self.assertRaises(OrionisIntegrityException):
            Disks(public=None)

    async def testAwsTypeValidation(self):
        """
        Test aws attribute type validation.

        Ensures that only `S3` instances are accepted for the `aws` attribute.

        Raises
        ------
        OrionisIntegrityException
            If the `aws` attribute is not an `S3` instance.
        """
        with self.assertRaises(OrionisIntegrityException):
            Disks(aws="not_an_s3_instance")
        with self.assertRaises(OrionisIntegrityException):
            Disks(aws=123)
        with self.assertRaises(OrionisIntegrityException):
            Disks(aws=None)

    async def testCustomDiskConfigurations(self):
        """
        Test that custom disk configurations are properly stored and validated.

        Ensures that custom disk configurations are correctly handled and their
        attributes are properly set.

        Returns
        -------
        None
        """
        custom_local = Local(path="custom/local/path")
        custom_public = Public(path="custom/public/path", url="assets")
        custom_aws = S3(bucket="custom-bucket", region="eu-west-1")

        disks = Disks(
            local=custom_local,
            public=custom_public,
            aws=custom_aws
        )

        self.assertEqual(disks.local.path, "custom/local/path")
        self.assertEqual(disks.public.path, "custom/public/path")
        self.assertEqual(disks.public.url, "assets")
        self.assertEqual(disks.aws.bucket, "custom-bucket")
        self.assertEqual(disks.aws.region, "eu-west-1")

    async def testToDictMethod(self):
        """
        Test that toDict returns proper dictionary representation.

        Ensures that all disk configurations are correctly included in the
        dictionary representation.

        Returns
        -------
        None
        """
        disks = Disks()
        disks_dict = disks.toDict()

        self.assertIsInstance(disks_dict, dict)
        self.assertIsInstance(disks_dict['local'], dict)
        self.assertIsInstance(disks_dict['public'], dict)
        self.assertIsInstance(disks_dict['aws'], dict)

    async def testHashability(self):
        """
        Test that Disks maintains hashability due to unsafe_hash=True.

        Ensures that `Disks` instances can be used in sets and as dictionary keys.

        Returns
        -------
        None
        """
        disks1 = Disks()
        disks2 = Disks()
        disks_set = {disks1, disks2}

        self.assertEqual(len(disks_set), 1)

        custom_disks = Disks(local=Local(path="custom/path"))
        disks_set.add(custom_disks)
        self.assertEqual(len(disks_set), 2)

    async def testKwOnlyInitialization(self):
        """
        Test that Disks enforces keyword-only initialization.

        Ensures that positional arguments are not allowed for initialization.

        Raises
        ------
        TypeError
            If positional arguments are used for initialization.
        """
        with self.assertRaises(TypeError):
            Disks(Local(), Public(), S3())