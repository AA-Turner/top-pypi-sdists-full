from orionis.test.cases.asynchronous import AsyncTestCase
from orionis.services.introspection.modules.reflection import ReflectionModule
from orionis.services.introspection.exceptions import ReflectionTypeError, ReflectionValueError

class TestServiceReflectionModule(AsyncTestCase):
    """
    Test suite for the ReflectionModule class functionality.

    This test class validates the introspection capabilities of the ReflectionModule
    which provides reflection functionality for Python modules including class,
    function, and constant discovery and manipulation.
    """

    module_name = 'tests.services.introspection.reflection.mock.fake_reflect_instance'

    async def testGetModule(self):
        """
        Test retrieval of the underlying module object.

        Validates that the getModule method returns the correct module object
        and that the module's __name__ attribute matches the expected name.

        Raises
        ------
        AssertionError
            If the module name does not match the expected value.
        """
        reflection = ReflectionModule(self.module_name)
        module = reflection.getModule()
        self.assertEqual(module.__name__, self.module_name)

    async def testHasClass(self):
        """
        Test class existence detection within the module.

        Verifies that the hasClass method correctly identifies the presence
        or absence of classes within the reflected module.

        Raises
        ------
        AssertionError
            If the class existence check returns incorrect boolean values.
        """
        reflection = ReflectionModule(self.module_name)
        self.assertTrue(reflection.hasClass('PublicFakeClass'))  # Existing class should return True
        self.assertFalse(reflection.hasClass('NonExistentClass'))  # Non-existent class should return False

    async def testGetClass(self):
        """
        Test class object retrieval by name.

        Validates that the getClass method returns the correct class object
        for existing classes and None for non-existent classes.

        Raises
        ------
        AssertionError
            If the retrieved class object is incorrect or None when it should exist.
        """
        reflection = ReflectionModule(self.module_name)
        cls = reflection.getClass('PublicFakeClass')
        self.assertIsNotNone(cls)  # Class should exist and be returned
        self.assertEqual(cls.__name__, 'PublicFakeClass')  # Class name should match
        self.assertIsNone(reflection.getClass('NonExistentClass'))  # Non-existent class should return None

    async def testSetAndRemoveClass(self):
        """
        Test dynamic class registration and removal operations.

        Validates the complete lifecycle of dynamically adding and removing
        classes from the module through the ReflectionModule interface.

        Raises
        ------
        AssertionError
            If class registration, retrieval, or removal operations fail.
        """
        reflection = ReflectionModule(self.module_name)

        # Define a mock class for testing
        class MockClass:
            pass

        # Test class registration
        reflection.setClass('MockClass', MockClass)
        self.assertTrue(reflection.hasClass('MockClass'))  # Class should be registered
        self.assertEqual(reflection.getClass('MockClass'), MockClass)  # Retrieved class should match

        # Test class removal
        reflection.removeClass('MockClass')
        self.assertFalse(reflection.hasClass('MockClass'))  # Class should be removed

    async def testSetClassInvalid(self):
        """
        Test error handling for invalid class registration attempts.

        Validates that the setClass method properly raises ReflectionValueError
        when provided with invalid class names or non-class objects.

        Raises
        ------
        AssertionError
            If expected ReflectionValueError exceptions are not raised.
        """
        reflection = ReflectionModule(self.module_name)

        # Test invalid class name starting with digit
        with self.assertRaises(ReflectionValueError):
            reflection.setClass('123Invalid', object)

        # Test reserved keyword as class name
        with self.assertRaises(ReflectionValueError):
            reflection.setClass('class', object)

        # Test non-class object registration
        with self.assertRaises(ReflectionValueError):
            reflection.setClass('ValidName', 123)

    async def testRemoveClassInvalid(self):
        """
        Test error handling for invalid class removal attempts.

        Validates that the removeClass method properly raises ValueError
        when attempting to remove a non-existent class from the module.

        Raises
        ------
        AssertionError
            If the expected ValueError exception is not raised.
        """
        reflection = ReflectionModule(self.module_name)
        with self.assertRaises(ValueError):
            reflection.removeClass('NonExistentClass')

    async def testInitClass(self):
        """
        Test class instantiation through reflection.

        Validates that the initClass method can successfully create instances
        of existing classes and properly handles non-existent class errors.

        Raises
        ------
        AssertionError
            If class instantiation fails or error handling is incorrect.
        """
        reflection = ReflectionModule(self.module_name)

        # Test successful class instantiation
        instance = reflection.initClass('PublicFakeClass')
        self.assertEqual(instance.__class__.__name__, 'PublicFakeClass')

        # Test error handling for non-existent class
        with self.assertRaises(ReflectionValueError):
            reflection.initClass('NonExistentClass')

    async def testGetClasses(self):
        """
        Test retrieval of all classes defined in the module.

        Validates that the getClasses method returns a complete dictionary
        of all class definitions including public, protected, and private classes.

        Raises
        ------
        AssertionError
            If expected classes are not found in the returned dictionary.
        """
        reflection = ReflectionModule(self.module_name)
        classes = reflection.getClasses()
        self.assertIn('PublicFakeClass', classes)      # Public class should be included
        self.assertIn('_ProtectedFakeClass', classes)  # Protected class should be included
        self.assertIn('__PrivateFakeClass', classes)   # Private class should be included

    async def testGetPublicClasses(self):
        """
        Test retrieval of public classes only.

        Validates that the getPublicClasses method returns only classes
        with public visibility (not prefixed with underscores).

        Raises
        ------
        AssertionError
            If protected or private classes are included or public classes are excluded.
        """
        reflection = ReflectionModule(self.module_name)
        public_classes = reflection.getPublicClasses()
        self.assertIn('PublicFakeClass', public_classes)        # Public class should be included
        self.assertNotIn('_ProtectedFakeClass', public_classes) # Protected class should be excluded
        self.assertNotIn('__PrivateFakeClass', public_classes)  # Private class should be excluded

    async def testGetProtectedClasses(self):
        """
        Test retrieval of protected classes only.

        Validates that the getProtectedClasses method returns only classes
        with protected visibility (prefixed with single underscore).

        Raises
        ------
        AssertionError
            If public or private classes are included or protected classes are excluded.
        """
        reflection = ReflectionModule(self.module_name)
        protected_classes = reflection.getProtectedClasses()
        self.assertIn('_ProtectedFakeClass', protected_classes)  # Protected class should be included
        self.assertNotIn('PublicFakeClass', protected_classes)   # Public class should be excluded

    async def testGetPrivateClasses(self):
        """
        Test retrieval of private classes only.

        Validates that the getPrivateClasses method returns only classes
        with private visibility (prefixed with double underscores, not ending with them).

        Raises
        ------
        AssertionError
            If public or protected classes are included or private classes are excluded.
        """
        reflection = ReflectionModule(self.module_name)
        private_classes = reflection.getPrivateClasses()
        self.assertIn('__PrivateFakeClass', private_classes)  # Private class should be included
        self.assertNotIn('PublicFakeClass', private_classes)  # Public class should be excluded

    async def testGetConstants(self):
        """
        Test retrieval of all constants defined in the module.

        Validates that the getConstants method returns a complete dictionary
        of all constant definitions including public, protected, and private constants.

        Raises
        ------
        AssertionError
            If expected constants are not found in the returned dictionary.
        """
        reflection = ReflectionModule(self.module_name)
        consts = reflection.getConstants()
        self.assertIn('PUBLIC_CONSTANT', consts)      # Public constant should be included
        self.assertIn('_PROTECTED_CONSTANT', consts)  # Protected constant should be included
        self.assertIn('__PRIVATE_CONSTANT', consts)   # Private constant should be included

    async def testGetPublicConstants(self):
        """
        Test retrieval of public constants only.

        Validates that the getPublicConstants method returns only constants
        with public visibility (not prefixed with underscores).

        Raises
        ------
        AssertionError
            If protected or private constants are included or public constants are excluded.
        """
        reflection = ReflectionModule(self.module_name)
        public_consts = reflection.getPublicConstants()
        self.assertIn('PUBLIC_CONSTANT', public_consts)        # Public constant should be included
        self.assertNotIn('_PROTECTED_CONSTANT', public_consts) # Protected constant should be excluded
        self.assertNotIn('__PRIVATE_CONSTANT', public_consts)  # Private constant should be excluded

    async def testGetProtectedConstants(self):
        """
        Test retrieval of protected constants only.

        Validates that the getProtectedConstants method returns only constants
        with protected visibility (prefixed with single underscore).

        Raises
        ------
        AssertionError
            If public or private constants are included or protected constants are excluded.
        """
        reflection = ReflectionModule(self.module_name)
        protected_consts = reflection.getProtectedConstants()
        self.assertIn('_PROTECTED_CONSTANT', protected_consts)  # Protected constant should be included
        self.assertNotIn('PUBLIC_CONSTANT', protected_consts)   # Public constant should be excluded

    async def testGetPrivateConstants(self):
        """
        Test retrieval of private constants only.

        Validates that the getPrivateConstants method returns only constants
        with private visibility (prefixed with double underscores, not ending with them).

        Raises
        ------
        AssertionError
            If public or protected constants are included or private constants are excluded.
        """
        reflection = ReflectionModule(self.module_name)
        private_consts = reflection.getPrivateConstants()
        self.assertIn('__PRIVATE_CONSTANT', private_consts)  # Private constant should be included
        self.assertNotIn('PUBLIC_CONSTANT', private_consts)  # Public constant should be excluded

    async def testGetConstant(self):
        """
        Test individual constant value retrieval by name.

        Validates that the getConstant method returns the correct value
        for existing constants and None for non-existent constants.

        Raises
        ------
        AssertionError
            If the retrieved constant value is incorrect or None when it should exist.
        """
        reflection = ReflectionModule(self.module_name)
        value = reflection.getConstant('PUBLIC_CONSTANT')
        self.assertEqual(value, 'public constant')  # Constant value should match expected
        self.assertIsNone(reflection.getConstant('NON_EXISTENT_CONST'))  # Non-existent constant should return None

    async def testGetFunctions(self):
        """
        Test retrieval of all functions defined in the module.

        Validates that the getFunctions method returns a complete dictionary
        of all function definitions including public, protected, and private functions
        of both synchronous and asynchronous types.

        Raises
        ------
        AssertionError
            If expected functions are not found in the returned dictionary.
        """
        reflection = ReflectionModule(self.module_name)
        funcs = reflection.getFunctions()
        # Test public functions
        self.assertIn('publicSyncFunction', funcs)      # Public sync function should be included
        self.assertIn('publicAsyncFunction', funcs)     # Public async function should be included
        # Test protected functions
        self.assertIn('_protectedSyncFunction', funcs)  # Protected sync function should be included
        self.assertIn('_protectedAsyncFunction', funcs) # Protected async function should be included
        # Test private functions
        self.assertIn('__privateSyncFunction', funcs)   # Private sync function should be included
        self.assertIn('__privateAsyncFunction', funcs)  # Private async function should be included

    async def testGetPublicFunctions(self):
        """
        Test retrieval of public functions only.

        Validates that the getPublicFunctions method returns only functions
        with public visibility (not prefixed with underscores) including
        both synchronous and asynchronous functions.

        Raises
        ------
        AssertionError
            If protected or private functions are included or public functions are excluded.
        """
        reflection = ReflectionModule(self.module_name)
        public_funcs = reflection.getPublicFunctions()
        self.assertIn('publicSyncFunction', public_funcs)        # Public sync function should be included
        self.assertIn('publicAsyncFunction', public_funcs)       # Public async function should be included
        self.assertNotIn('_protectedSyncFunction', public_funcs) # Protected function should be excluded
        self.assertNotIn('__privateSyncFunction', public_funcs)  # Private function should be excluded

    async def testGetPublicSyncFunctions(self):
        """
        Test retrieval of public synchronous functions only.

        Validates that the getPublicSyncFunctions method returns only functions
        with public visibility that are synchronous (non-async).

        Raises
        ------
        AssertionError
            If asynchronous functions are included or synchronous public functions are excluded.
        """
        reflection = ReflectionModule(self.module_name)
        sync_funcs = reflection.getPublicSyncFunctions()
        self.assertIn('publicSyncFunction', sync_funcs)     # Public sync function should be included
        self.assertNotIn('publicAsyncFunction', sync_funcs) # Public async function should be excluded

    async def testGetPublicAsyncFunctions(self):
        """
        Test retrieval of public asynchronous functions only.

        Validates that the getPublicAsyncFunctions method returns only functions
        with public visibility that are asynchronous (async def).

        Raises
        ------
        AssertionError
            If synchronous functions are included or asynchronous public functions are excluded.
        """
        reflection = ReflectionModule(self.module_name)
        async_funcs = reflection.getPublicAsyncFunctions()
        self.assertIn('publicAsyncFunction', async_funcs)    # Public async function should be included
        self.assertNotIn('publicSyncFunction', async_funcs)  # Public sync function should be excluded

    async def testGetProtectedFunctions(self):
        """
        Test retrieval of protected functions only.

        Validates that the getProtectedFunctions method returns only functions
        with protected visibility (prefixed with single underscore) including
        both synchronous and asynchronous functions.

        Raises
        ------
        AssertionError
            If public functions are included or protected functions are excluded.
        """
        reflection = ReflectionModule(self.module_name)
        protected_funcs = reflection.getProtectedFunctions()
        self.assertIn('_protectedSyncFunction', protected_funcs)  # Protected sync function should be included
        self.assertIn('_protectedAsyncFunction', protected_funcs) # Protected async function should be included
        self.assertNotIn('publicSyncFunction', protected_funcs)   # Public function should be excluded

    async def testGetProtectedSyncFunctions(self):
        """
        Test retrieval of protected synchronous functions only.

        Validates that the getProtectedSyncFunctions method returns only functions
        with protected visibility that are synchronous (non-async).

        Raises
        ------
        AssertionError
            If asynchronous functions are included or synchronous protected functions are excluded.
        """
        reflection = ReflectionModule(self.module_name)
        sync_funcs = reflection.getProtectedSyncFunctions()
        self.assertIn('_protectedSyncFunction', sync_funcs)     # Protected sync function should be included
        self.assertNotIn('_protectedAsyncFunction', sync_funcs) # Protected async function should be excluded

    async def testGetProtectedAsyncFunctions(self):
        """
        Test retrieval of protected asynchronous functions only.

        Validates that the getProtectedAsyncFunctions method returns only functions
        with protected visibility that are asynchronous (async def).

        Raises
        ------
        AssertionError
            If synchronous functions are included or asynchronous protected functions are excluded.
        """
        reflection = ReflectionModule(self.module_name)
        async_funcs = reflection.getProtectedAsyncFunctions()
        self.assertIn('_protectedAsyncFunction', async_funcs)    # Protected async function should be included
        self.assertNotIn('_protectedSyncFunction', async_funcs)  # Protected sync function should be excluded

    async def testGetPrivateFunctions(self):
        """
        Test retrieval of private functions only.

        Validates that the getPrivateFunctions method returns only functions
        with private visibility (prefixed with double underscores, not ending with them)
        including both synchronous and asynchronous functions.

        Raises
        ------
        AssertionError
            If public functions are included or private functions are excluded.
        """
        reflection = ReflectionModule(self.module_name)
        private_funcs = reflection.getPrivateFunctions()
        self.assertIn('__privateSyncFunction', private_funcs)  # Private sync function should be included
        self.assertIn('__privateAsyncFunction', private_funcs) # Private async function should be included
        self.assertNotIn('publicSyncFunction', private_funcs)  # Public function should be excluded

    async def testGetPrivateSyncFunctions(self):
        """
        Test retrieval of private synchronous functions only.

        Validates that the getPrivateSyncFunctions method returns only functions
        with private visibility that are synchronous (non-async).

        Raises
        ------
        AssertionError
            If asynchronous functions are included or synchronous private functions are excluded.
        """
        reflection = ReflectionModule(self.module_name)
        sync_funcs = reflection.getPrivateSyncFunctions()
        self.assertIn('__privateSyncFunction', sync_funcs)     # Private sync function should be included
        self.assertNotIn('__privateAsyncFunction', sync_funcs) # Private async function should be excluded

    async def testGetPrivateAsyncFunctions(self):
        """
        Test retrieval of private asynchronous functions only.

        Validates that the getPrivateAsyncFunctions method returns only functions
        with private visibility that are asynchronous (async def).

        Raises
        ------
        AssertionError
            If synchronous functions are included or asynchronous private functions are excluded.
        """
        reflection = ReflectionModule(self.module_name)
        async_funcs = reflection.getPrivateAsyncFunctions()
        self.assertIn('__privateAsyncFunction', async_funcs)    # Private async function should be included
        self.assertNotIn('__privateSyncFunction', async_funcs)  # Private sync function should be excluded

    async def testGetImports(self):
        """
        Test retrieval of imported modules within the reflected module.

        Validates that the getImports method correctly identifies and returns
        all imported module objects from the module's namespace.

        Raises
        ------
        AssertionError
            If expected imported modules are not found in the returned dictionary.
        """
        reflection = ReflectionModule(self.module_name)
        imports = reflection.getImports()
        self.assertIn('asyncio', imports)  # asyncio module should be imported

    async def testGetFile(self):
        """
        Test retrieval of the module's file path.

        Validates that the getFile method returns the correct absolute path
        to the module's source file.

        Raises
        ------
        AssertionError
            If the returned file path does not end with the expected filename.
        """
        reflection = ReflectionModule(self.module_name)
        file_path = reflection.getFile()
        self.assertTrue(file_path.endswith('fake_reflect_instance.py'))  # Path should end with expected filename

    async def testGetSourceCode(self):
        """
        Test retrieval of the module's complete source code.

        Validates that the getSourceCode method returns the entire source code
        content of the module file and contains expected code elements.

        Raises
        ------
        AssertionError
            If expected code elements are not found in the returned source code.
        """
        reflection = ReflectionModule(self.module_name)
        code = reflection.getSourceCode()
        self.assertIn('PUBLIC_CONSTANT', code)        # Constant should be present in source
        self.assertIn('def publicSyncFunction', code) # Function definition should be present in source

    async def test_invalid_module_name(self):
        """
        Test error handling for invalid module initialization.

        Validates that ReflectionModule properly raises ReflectionTypeError
        when initialized with invalid module names such as empty strings
        or non-existent module paths.

        Raises
        ------
        AssertionError
            If expected ReflectionTypeError exceptions are not raised.
        """
        # Test empty string module name
        with self.assertRaises(ReflectionTypeError):
            ReflectionModule('')

        # Test non-existent module path
        with self.assertRaises(ReflectionTypeError):
            ReflectionModule('nonexistent.module.name')