from orionis.test.cases.asynchronous import AsyncTestCase
from orionis.services.introspection.modules.reflection import ReflectionModule
from orionis.services.introspection.exceptions import ReflectionTypeError, ReflectionValueError

class TestServiceReflectionModule(AsyncTestCase):

    module_name = 'tests.services.introspection.reflection.mock.fake_reflect_instance'

    async def testGetModule(self):
        """
        Test that the `getModule` method of the `ReflectionModule` class returns a module object
        whose `__name__` attribute matches the expected module name.
        """
        reflection = ReflectionModule(self.module_name)
        module = reflection.getModule()
        self.assertEqual(module.__name__, self.module_name)

    async def testHasClass(self):
        """
        Tests the hasClass method of the ReflectionModule.

        This test verifies that hasClass correctly identifies the presence or absence of a class within the module:
        - Asserts that hasClass returns True for an existing class ('PublicFakeClass').
        - Asserts that hasClass returns False for a non-existent class ('NonExistentClass').
        """
        reflection = ReflectionModule(self.module_name)
        self.assertTrue(reflection.hasClass('PublicFakeClass'))
        self.assertFalse(reflection.hasClass('NonExistentClass'))

    async def testGetClass(self):
        """
        Test the `getClass` method of the ReflectionModule.

        This test verifies that:
        - The method returns the correct class object when given a valid class name ('PublicFakeClass').
        - The returned class object has the expected name.
        - The method returns None when given a non-existent class name ('NonExistentClass').
        """
        reflection = ReflectionModule(self.module_name)
        cls = reflection.getClass('PublicFakeClass')
        self.assertIsNotNone(cls)
        self.assertEqual(cls.__name__, 'PublicFakeClass')
        self.assertIsNone(reflection.getClass('NonExistentClass'))

    async def testSetAndRemoveClass(self):
        """
        Test the functionality of setting, retrieving, and removing a class in the ReflectionModule.

        This test verifies that:
        - A class can be registered with the ReflectionModule using setClass.
        - The presence of the class can be checked with hasClass.
        - The registered class can be retrieved with getClass.
        - The class can be removed with removeClass.
        - After removal, hasClass returns False for the class name.
        """
        reflection = ReflectionModule(self.module_name)
        class MockClass:
            pass
        reflection.setClass('MockClass', MockClass)
        self.assertTrue(reflection.hasClass('MockClass'))
        self.assertEqual(reflection.getClass('MockClass'), MockClass)
        reflection.removeClass('MockClass')
        self.assertFalse(reflection.hasClass('MockClass'))

    async def testSetClassInvalid(self):
        """
        Test that the `setClass` method of `ReflectionModule` raises a `ReflectionValueError`
        when provided with invalid class names or class types.

        Scenarios tested:
            - Class name starts with a digit.
            - Class name is a reserved keyword.
            - Class type is not a valid type (e.g., passing an integer instead of a class).
        """
        reflection = ReflectionModule(self.module_name)
        with self.assertRaises(ReflectionValueError):
            reflection.setClass('123Invalid', object)
        with self.assertRaises(ReflectionValueError):
            reflection.setClass('class', object)
        with self.assertRaises(ReflectionValueError):
            reflection.setClass('ValidName', 123)

    async def testRemoveClassInvalid(self):
        """
        Test that attempting to remove a non-existent class from the ReflectionModule raises a ValueError.

        This test verifies that the `removeClass` method correctly handles the case where the specified class
        does not exist in the module by raising a `ValueError` exception.
        """
        reflection = ReflectionModule(self.module_name)
        with self.assertRaises(ValueError):
            reflection.removeClass('NonExistentClass')

    async def testInitClass(self):
        """
        Tests the initialization of a class using the ReflectionModule.

        This test verifies that:
        - An instance of 'PublicFakeClass' can be successfully created using the initClass method.
        - The created instance has the correct class name.
        - Attempting to initialize a non-existent class ('NonExistentClass') raises a ReflectionValueError.
        """
        reflection = ReflectionModule(self.module_name)
        instance = reflection.initClass('PublicFakeClass')
        self.assertEqual(instance.__class__.__name__, 'PublicFakeClass')
        with self.assertRaises(ReflectionValueError):
            reflection.initClass('NonExistentClass')

    async def testGetClasses(self):
        """
        Test that the `getClasses` method of the `ReflectionModule` returns a list of class names
        defined in the module, including public, protected, and private classes.
        """
        reflection = ReflectionModule(self.module_name)
        classes = reflection.getClasses()
        self.assertIn('PublicFakeClass', classes)
        self.assertIn('_ProtectedFakeClass', classes)
        self.assertIn('__PrivateFakeClass', classes)

    async def testGetPublicClasses(self):
        """
        Test that the `getPublicClasses` method of the `ReflectionModule` returns only public class names.
        Verifies that:
        - Public class names (e.g., 'PublicFakeClass') are included in the result.
        - Protected (e.g., '_ProtectedFakeClass') and private (e.g., '__PrivateFakeClass') class names are excluded.
        """
        reflection = ReflectionModule(self.module_name)
        public_classes = reflection.getPublicClasses()
        self.assertIn('PublicFakeClass', public_classes)
        self.assertNotIn('_ProtectedFakeClass', public_classes)
        self.assertNotIn('__PrivateFakeClass', public_classes)

    async def testGetProtectedClasses(self):
        """
        Test that the ReflectionModule correctly identifies protected classes.

        This test verifies that the `getProtectedClasses` method returns a list containing
        the names of protected classes (those prefixed with an underscore) and excludes
        public class names. Specifically, it checks that '_ProtectedFakeClass' is present
        in the returned list, while 'PublicFakeClass' is not.
        """
        reflection = ReflectionModule(self.module_name)
        protected_classes = reflection.getProtectedClasses()
        self.assertIn('_ProtectedFakeClass', protected_classes)
        self.assertNotIn('PublicFakeClass', protected_classes)

    async def testGetPrivateClasses(self):
        """
        Test that the `getPrivateClasses` method of the `ReflectionModule` correctly identifies private classes within the specified module.

        This test verifies that:
        - The private class '__PrivateFakeClass' is present in the list of private classes returned.
        - The public class 'PublicFakeClass' is not included in the list of private classes.
        """
        reflection = ReflectionModule(self.module_name)
        private_classes = reflection.getPrivateClasses()
        self.assertIn('__PrivateFakeClass', private_classes)
        self.assertNotIn('PublicFakeClass', private_classes)

    async def testGetConstants(self):
        """
        Test that the `getConstants` method of the `ReflectionModule` retrieves all types of constants
        (public, protected, and private) defined in the module.

        Asserts:
            - 'PUBLIC_CONSTANT' is present in the returned constants.
            - '_PROTECTED_CONSTANT' is present in the returned constants.
            - '__PRIVATE_CONSTANT' is present in the returned constants.
        """
        reflection = ReflectionModule(self.module_name)
        consts = reflection.getConstants()
        self.assertIn('PUBLIC_CONSTANT', consts)
        self.assertIn('_PROTECTED_CONSTANT', consts)
        self.assertIn('__PRIVATE_CONSTANT', consts)

    async def testGetPublicConstants(self):
        """
        Test that `getPublicConstants` returns only public constants from the module.

        This test verifies that:
        - 'PUBLIC_CONSTANT' is present in the returned list of public constants.
        - '_PROTECTED_CONSTANT' and '__PRIVATE_CONSTANT' are not included in the list, ensuring that protected and private constants are excluded.
        """
        reflection = ReflectionModule(self.module_name)
        public_consts = reflection.getPublicConstants()
        self.assertIn('PUBLIC_CONSTANT', public_consts)
        self.assertNotIn('_PROTECTED_CONSTANT', public_consts)
        self.assertNotIn('__PRIVATE_CONSTANT', public_consts)

    async def testGetProtectedConstants(self):
        """
        Tests that the `getProtectedConstants` method of the `ReflectionModule` class
        correctly retrieves protected constants (those prefixed with an underscore) from the module.

        Asserts that '_PROTECTED_CONSTANT' is present in the returned list of protected constants,
        and that 'PUBLIC_CONSTANT' is not included.
        """
        reflection = ReflectionModule(self.module_name)
        protected_consts = reflection.getProtectedConstants()
        self.assertIn('_PROTECTED_CONSTANT', protected_consts)
        self.assertNotIn('PUBLIC_CONSTANT', protected_consts)

    async def testGetPrivateConstants(self):
        """
        Test that the getPrivateConstants method of the ReflectionModule correctly retrieves private constants.

        This test verifies that:
        - The private constant '__PRIVATE_CONSTANT' is present in the list of private constants.
        - The public constant 'PUBLIC_CONSTANT' is not included in the list of private constants.
        """
        reflection = ReflectionModule(self.module_name)
        private_consts = reflection.getPrivateConstants()
        self.assertIn('__PRIVATE_CONSTANT', private_consts)
        self.assertNotIn('PUBLIC_CONSTANT', private_consts)

    async def testGetConstant(self):
        """
        Test the `getConstant` method of the ReflectionModule.

        This test verifies that:
        - Retrieving an existing constant ('PUBLIC_CONSTANT') returns its expected value ('public constant').
        - Retrieving a non-existent constant ('NON_EXISTENT_CONST') returns None.
        """
        reflection = ReflectionModule(self.module_name)
        value = reflection.getConstant('PUBLIC_CONSTANT')
        self.assertEqual(value, 'public constant')
        self.assertIsNone(reflection.getConstant('NON_EXISTENT_CONST'))

    async def testGetFunctions(self):
        """
        Test that the ReflectionModule correctly retrieves all function names, including public, protected, and private methods, from the specified module.
        """
        reflection = ReflectionModule(self.module_name)
        funcs = reflection.getFunctions()
        self.assertIn('publicSyncFunction', funcs)
        self.assertIn('publicAsyncFunction', funcs)
        self.assertIn('_protectedSyncFunction', funcs)
        self.assertIn('_protectedAsyncFunction', funcs)
        self.assertIn('__privateSyncFunction', funcs)
        self.assertIn('__privateAsyncFunction', funcs)

    async def testGetPublicFunctions(self):
        """
        Test that ReflectionModule.getPublicFunctions() returns only public functions.

        This test verifies that:
        - Public synchronous and asynchronous functions are included in the returned list.
        - Protected (prefixed with a single underscore) and private (prefixed with double underscores) functions are not included.
        """
        reflection = ReflectionModule(self.module_name)
        public_funcs = reflection.getPublicFunctions()
        self.assertIn('publicSyncFunction', public_funcs)
        self.assertIn('publicAsyncFunction', public_funcs)
        self.assertNotIn('_protectedSyncFunction', public_funcs)
        self.assertNotIn('__privateSyncFunction', public_funcs)

    async def testGetPublicSyncFunctions(self):
        """
        Test that `getPublicSyncFunctions` returns only public synchronous functions.

        This test verifies that:
        - The list of public synchronous functions includes 'publicSyncFunction'.
        - The list does not include 'publicAsyncFunction', ensuring only synchronous functions are returned.
        """
        reflection = ReflectionModule(self.module_name)
        sync_funcs = reflection.getPublicSyncFunctions()
        self.assertIn('publicSyncFunction', sync_funcs)
        self.assertNotIn('publicAsyncFunction', sync_funcs)

    async def testGetPublicAsyncFunctions(self):
        """
        Test that ReflectionModule.getPublicAsyncFunctions() returns a list containing the names of public asynchronous functions,
        including 'publicAsyncFunction', and excludes synchronous functions such as 'publicSyncFunction'.
        """
        reflection = ReflectionModule(self.module_name)
        async_funcs = reflection.getPublicAsyncFunctions()
        self.assertIn('publicAsyncFunction', async_funcs)
        self.assertNotIn('publicSyncFunction', async_funcs)

    async def testGetProtectedFunctions(self):
        """
        Test that the ReflectionModule correctly identifies protected functions.

        This test verifies that:
        - Protected functions (those prefixed with a single underscore) are included in the list returned by getProtectedFunctions().
        - Public functions (those without a leading underscore) are not included in the list of protected functions.
        """
        reflection = ReflectionModule(self.module_name)
        protected_funcs = reflection.getProtectedFunctions()
        self.assertIn('_protectedSyncFunction', protected_funcs)
        self.assertIn('_protectedAsyncFunction', protected_funcs)
        self.assertNotIn('publicSyncFunction', protected_funcs)

    async def testGetProtectedSyncFunctions(self):
        """
        Test that the `getProtectedSyncFunctions` method of the `ReflectionModule` class
        returns a list containing protected synchronous function names, specifically
        including '_protectedSyncFunction' and excluding '_protectedAsyncFunction'.
        """
        reflection = ReflectionModule(self.module_name)
        sync_funcs = reflection.getProtectedSyncFunctions()
        self.assertIn('_protectedSyncFunction', sync_funcs)
        self.assertNotIn('_protectedAsyncFunction', sync_funcs)

    async def testGetProtectedAsyncFunctions(self):
        """
        Test that the ReflectionModule correctly identifies protected asynchronous functions.

        This test verifies that:
        - The list of protected async functions returned by `getProtectedAsyncFunctions()` includes '_protectedAsyncFunction'.
        - The list does not include '_protectedSyncFunction', ensuring only async functions are returned.
        """
        reflection = ReflectionModule(self.module_name)
        async_funcs = reflection.getProtectedAsyncFunctions()
        self.assertIn('_protectedAsyncFunction', async_funcs)
        self.assertNotIn('_protectedSyncFunction', async_funcs)

    async def testGetPrivateFunctions(self):
        """
        Test that ReflectionModule.getPrivateFunctions correctly identifies private functions.

        This test verifies that:
        - Private functions (e.g., '__privateSyncFunction', '__privateAsyncFunction') are included in the returned list.
        - Public functions (e.g., 'publicSyncFunction') are not included in the returned list.
        """
        reflection = ReflectionModule(self.module_name)
        private_funcs = reflection.getPrivateFunctions()
        self.assertIn('__privateSyncFunction', private_funcs)
        self.assertIn('__privateAsyncFunction', private_funcs)
        self.assertNotIn('publicSyncFunction', private_funcs)

    async def testGetPrivateSyncFunctions(self):
        """
        Test that the getPrivateSyncFunctions method of ReflectionModule returns a list containing
        the names of private synchronous functions, specifically including '__privateSyncFunction'
        and excluding '__privateAsyncFunction'.
        """
        reflection = ReflectionModule(self.module_name)
        sync_funcs = reflection.getPrivateSyncFunctions()
        self.assertIn('__privateSyncFunction', sync_funcs)
        self.assertNotIn('__privateAsyncFunction', sync_funcs)

    async def testGetPrivateAsyncFunctions(self):
        """
        Tests that the ReflectionModule correctly identifies private asynchronous functions.

        This test verifies that:
        - The list of private async functions returned by `getPrivateAsyncFunctions()` includes '__privateAsyncFunction'.
        - The list does not include '__privateSyncFunction', ensuring only async functions are returned.
        """
        reflection = ReflectionModule(self.module_name)
        async_funcs = reflection.getPrivateAsyncFunctions()
        self.assertIn('__privateAsyncFunction', async_funcs)
        self.assertNotIn('__privateSyncFunction', async_funcs)

    async def testGetImports(self):
        """
        Test that the `getImports` method of the `ReflectionModule` correctly retrieves the list of imported modules.
        Asserts that 'asyncio' is present in the returned imports.
        """
        reflection = ReflectionModule(self.module_name)
        imports = reflection.getImports()
        self.assertIn('asyncio', imports)

    async def testGetFile(self):
        """
        Tests that the `getFile` method of the `ReflectionModule` returns the correct file path.

        This test creates an instance of `ReflectionModule` with the specified module name,
        retrieves the file path using `getFile`, and asserts that the returned path ends with
        'fake_reflect_instance.py', indicating the correct file is being referenced.
        """
        reflection = ReflectionModule(self.module_name)
        file_path = reflection.getFile()
        self.assertTrue(file_path.endswith('fake_reflect_instance.py'))

    async def testGetSourceCode(self):
        """
        Tests that the `getSourceCode` method of the ReflectionModule retrieves the source code
        containing specific elements such as 'PUBLIC_CONSTANT' and the function definition
        'def publicSyncFunction'. Asserts that these elements are present in the returned code.
        """
        reflection = ReflectionModule(self.module_name)
        code = reflection.getSourceCode()
        self.assertIn('PUBLIC_CONSTANT', code)
        self.assertIn('def publicSyncFunction', code)

    async def test_invalid_module_name(self):
        """
        Test that ReflectionModule raises a ReflectionTypeError when initialized with an invalid module name,
        such as an empty string or a non-existent module path.
        """
        with self.assertRaises(ReflectionTypeError):
            ReflectionModule('')
        with self.assertRaises(ReflectionTypeError):
            ReflectionModule('nonexistent.module.name')