from orionis.support.wrapper import DotDict
from orionis.test.cases.asynchronous import AsyncTestCase

class TestSupportWrapperDocDict(AsyncTestCase):

    async def testDotNotationAccess(self):
        """
        Test dot notation access for dictionary values.

        Checks that values in a DotDict instance can be accessed using dot notation,
        including nested dictionaries via chained dot notation. Also verifies that
        accessing a non-existent key returns None.

        Returns
        -------
        None
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
        Test assignment of dictionary values using dot notation.

        Verifies that new keys can be added and existing keys updated using dot notation.
        Also checks that nested dictionaries assigned via dot notation are automatically
        converted to DotDict instances.

        Returns
        -------
        None
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
        Test deletion of dictionary keys using dot notation.

        Ensures that existing keys can be deleted using dot notation and that attempting
        to delete a non-existent key raises an AttributeError.

        Returns
        -------
        None
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
        Test the `get` method with automatic DotDict conversion.

        Verifies that the `get` method returns the correct value for a given key,
        returns the provided default for missing keys, and converts nested dictionaries
        to DotDict instances when accessed.

        Returns
        -------
        None
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
        Test the `export` method for recursive conversion to regular dict.

        Ensures that calling `export` on a DotDict instance recursively converts
        all nested DotDict objects back to regular Python dictionaries.

        Returns
        -------
        None
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
        Test the `copy` method for deep copy with DotDict conversion.

        Verifies that copying a DotDict instance produces an independent copy,
        with all nested dictionaries converted to DotDict instances. Checks that
        changes to the copy do not affect the original.

        Returns
        -------
        None
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
        Test automatic conversion of nested dictionaries to DotDict.

        Verifies that nested dictionaries are converted to DotDict instances
        both during initialization and dynamic assignment.

        Returns
        -------
        None
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
        Test the string representation of DotDict.

        Verifies that the `__repr__` method of DotDict returns a string
        representation that includes the DotDict prefix.

        Returns
        -------
        None
        """
        # Create a DotDict instance and test its string representation
        dd = DotDict({'key': 'value'})
        self.assertEqual(repr(dd), "{'key': 'value'}")
