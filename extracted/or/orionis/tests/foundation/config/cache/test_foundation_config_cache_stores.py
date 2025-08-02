from orionis.foundation.config.cache.entities.stores import Stores
from orionis.foundation.config.cache.entities.file import File
from orionis.foundation.exceptions.integrity import OrionisIntegrityException
from orionis.test.cases.asynchronous import AsyncTestCase

class TestFoundationConfigCacheStores(AsyncTestCase):
    """
    Test cases for the Stores cache configuration entity.

    This class contains asynchronous unit tests for the `Stores` entity,
    validating its initialization, type enforcement, dictionary conversion,
    hashability, and keyword-only argument enforcement.

    Attributes
    ----------
    None
    """

    async def testDefaultFileStore(self):
        """
        Test initialization with default File instance.

        Ensures that `Stores` initializes with a default `File` instance and
        that the `file` attribute is properly set with the default configuration.

        Returns
        -------
        None
        """
        stores = Stores()
        self.assertIsInstance(stores.file, File)
        self.assertEqual(stores.file.path, 'storage/framework/cache/data')

    async def testCustomFileStore(self):
        """
        Test initialization with a custom File configuration.

        Ensures that a custom `File` instance or dict can be provided during
        initialization and is correctly assigned to the `file` attribute.

        Returns
        -------
        None
        """
        custom_file = File(path='custom/cache/path')
        stores = Stores(file=custom_file)
        self.assertIsInstance(stores.file, File)
        self.assertEqual(stores.file.path, 'custom/cache/path')

        stores_dict = Stores(file={'path': 'dict/cache/path'})
        self.assertIsInstance(stores_dict.file, File)
        self.assertEqual(stores_dict.file.path, 'dict/cache/path')

    async def testFileTypeValidation(self):
        """
        Test type validation for the file attribute.

        Ensures that providing a non-`File` instance or dict to the `file` attribute
        raises an `OrionisIntegrityException`.

        Returns
        -------
        None

        Raises
        ------
        OrionisIntegrityException
            If the `file` attribute is not a `File` instance or dict.
        """
        with self.assertRaises(OrionisIntegrityException):
            Stores(file="not_a_file_instance")

        with self.assertRaises(OrionisIntegrityException):
            Stores(file=123)

        with self.assertRaises(OrionisIntegrityException):
            Stores(file=None)

    async def testToDictMethodWithDefaults(self):
        """
        Test dictionary representation with default values.

        Ensures that `toDict` returns a dictionary with the correct default
        file path.

        Returns
        -------
        None
        """
        stores = Stores()
        stores_dict = stores.toDict()

        self.assertIsInstance(stores_dict, dict)
        self.assertIsInstance(stores_dict['file'], dict)
        self.assertEqual(stores_dict['file']['path'], 'storage/framework/cache/data')

    async def testToDictMethodWithCustomFile(self):
        """
        Test dictionary representation with custom file configuration.

        Ensures that `toDict` reflects custom file paths in its dictionary
        representation.

        Returns
        -------
        None
        """
        custom_file = File(path='alternate/cache/location')
        stores = Stores(file=custom_file)
        stores_dict = stores.toDict()

        self.assertEqual(stores_dict['file']['path'], 'alternate/cache/location')

        stores_dict_input = Stores(file={'path': 'dict/location'})
        stores_dict2 = stores_dict_input.toDict()
        self.assertEqual(stores_dict2['file']['path'], 'dict/location')

    async def testHashability(self):
        """
        Test hashability of Stores instances.

        Ensures that `Stores` instances are hashable and can be used in sets
        and as dictionary keys.

        Returns
        -------
        None
        """
        store1 = Stores()
        store2 = Stores()
        store_set = {store1, store2}

        self.assertEqual(len(store_set), 1)

        custom_store = Stores(file=File(path='custom/path'))
        store_set.add(custom_store)
        self.assertEqual(len(store_set), 2)

    async def testKwOnlyInitialization(self):
        """
        Test keyword-only initialization enforcement.

        Ensures that `Stores` enforces keyword-only arguments and does not
        allow positional arguments during initialization.

        Returns
        -------
        None

        Raises
        ------
        TypeError
            If positional arguments are provided during initialization.
        """
        with self.assertRaises(TypeError):
            Stores(File())