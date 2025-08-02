from orionis.support.wrapper import DotDict
from orionis.test.cases.asynchronous import AsyncTestCase

class TestSupportWrapperDocDict(AsyncTestCase):

    async def testDotNotationAccess(self):
        """
        Tests dot notation access for dictionary values.

        This method verifies that values in a DotDict instance can be accessed using dot notation.
        It checks that existing keys return their corresponding values, nested dictionaries are
        accessible via chained dot notation, and accessing a non-existent key returns None.

        Returns
        -------
        None
            This is a test method and does not return a value.
        """

        # Create a DotDict instance with initial values
        dd = DotDict({'key1': 'value1', 'nested': {'inner': 42}})

        # Access existing key using dot notation
        self.assertEqual(dd.key1, 'value1')

        # Access nested dictionary value using chained dot notation
        self.assertEqual(dd.nested.inner, 42)

        # Access non-existent key, should return None
        self.assertIsNone(dd.non_existent)

    async def testDotNotationAssignment(self):
        """
        Tests assignment of dictionary values using dot notation.

        This method verifies that new keys can be added and existing keys can be updated
        using dot notation. It also checks that nested dictionaries assigned via dot notation
        are automatically converted to DotDict instances.

        Returns
        -------
        None
            This is a test method and does not return a value.
        """

        # Create a DotDict instance and assign values using dot notation
        dd = DotDict()

        # Assign new key using dot notation
        dd.key1 = 'value1'

        # Assign nested dictionary, should convert to DotDict
        dd.nested = {'inner': 42}

        # Verify the assignments
        self.assertEqual(dd['key1'], 'value1')
        self.assertIsInstance(dd.nested, DotDict)
        self.assertEqual(dd.nested.inner, 42)

    async def testDotNotationDeletion(self):
        """
        Tests deletion of dictionary keys using dot notation.

        This method verifies that existing keys can be deleted using dot notation.
        It also checks that attempting to delete a non-existent key raises an AttributeError.

        Returns
        -------
        None
            This is a test method and does not return a value.
        """

        # Create a DotDict instance and delete an existing key
        dd = DotDict({'key1': 'value1', 'key2': 'value2'})

        # Delete existing key using dot notation
        del dd.key1
        self.assertNotIn('key1', dd)

        # Attempt to delete non-existent key, should raise AttributeError
        with self.assertRaises(AttributeError):
            del dd.non_existent

    async def testGetMethod(self):
        """
        Tests the `get` method with automatic DotDict conversion.

        This method verifies that the `get` method returns the correct value for a given key,
        returns the provided default for missing keys, and converts nested dictionaries to
        DotDict instances when accessed.

        Returns
        -------
        None
            This is a test method and does not return a value.
        """

        # Create a DotDict instance and test the `get` method
        dd = DotDict({'key1': 'value1', 'nested': {'inner': 42}})

        self.assertEqual(dd.get('key1'), 'value1')
        self.assertEqual(dd.get('non_existent', 'default'), 'default')

        # Nested dictionary should be returned as DotDict
        self.assertIsInstance(dd.get('nested'), DotDict)
        self.assertEqual(dd.get('nested').inner, 42)

    async def testExportMethod(self):
        """
        Tests the `export` method for recursive conversion to regular dict.

        This method verifies that calling `export` on a DotDict instance recursively converts
        all nested DotDict objects back to regular Python dictionaries.

        Returns
        -------
        None
            This is a test method and does not return a value.
        """

        # Create a DotDict instance and export it
        dd = DotDict({
            'key1': 'value1',
            'nested': DotDict({
                'inner': 42,
                'deep': DotDict({'a': 1})
            })
        })

        exported = dd.export()

        # Top-level and nested DotDicts should be converted to dicts
        self.assertIsInstance(exported, dict)
        self.assertIsInstance(exported['nested'], dict)
        self.assertIsInstance(exported['nested']['deep'], dict)
        self.assertEqual(exported['nested']['inner'], 42)

    async def testCopyMethod(self):
        """
        Tests the `copy` method for deep copy with DotDict conversion.

        This method verifies that copying a DotDict instance produces an independent copy,
        with all nested dictionaries converted to DotDict instances. It checks that changes
        to the copy do not affect the original.

        Returns
        -------
        None
            This is a test method and does not return a value.
        """

        # Create a DotDict instance and copy it
        original = DotDict({
            'key1': 'value1',
            'nested': {'inner': 42}
        })

        # Copy the original DotDict
        copied = original.copy()

        # Modify the copy and verify original is unchanged
        copied.key1 = 'modified'
        copied.nested.inner = 100

        # Check that original remains unchanged
        self.assertEqual(original.key1, 'value1')
        self.assertEqual(original.nested.inner, 42)
        self.assertEqual(copied.key1, 'modified')
        self.assertEqual(copied.nested.inner, 100)
        self.assertIsInstance(copied.nested, DotDict)

    async def testNestedDictConversion(self):
        """
        Tests automatic conversion of nested dictionaries to DotDict.

        This method verifies that nested dictionaries are converted to DotDict instances
        both during initialization and dynamic assignment.

        Returns
        -------
        None
            This is a test method and does not return a value.
        """
        dd = DotDict({
            'level1': {
                'level2': {
                    'value': 42
                }
            }
        })

        # Nested dicts should be DotDict instances
        self.assertIsInstance(dd.level1, DotDict)
        self.assertIsInstance(dd.level1.level2, DotDict)
        self.assertEqual(dd.level1.level2.value, 42)

        # Test dynamic assignment of nested dict
        dd.new_nested = {'a': {'b': 1}}
        self.assertIsInstance(dd.new_nested, DotDict)
        self.assertIsInstance(dd.new_nested.a, DotDict)

    async def testReprMethod(self):
        """
        Tests the string representation of DotDict.

        This method verifies that the `__repr__` method of DotDict returns a string
        representation that includes the DotDict prefix.

        Returns
        -------
        None
            This is a test method and does not return a value.
        """

        # Create a DotDict instance and test its string representation
        dd = DotDict({'key': 'value'})
        self.assertEqual(repr(dd), "{'key': 'value'}")
