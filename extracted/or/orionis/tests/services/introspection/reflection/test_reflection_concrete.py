from orionis.services.introspection.concretes.reflection import ReflectionConcrete
from orionis.services.introspection.dependencies.entities.class_dependencies import ClassDependency
from tests.services.introspection.reflection.mock.fake_reflect_instance import FakeClass
from orionis.test.cases.asynchronous import AsyncTestCase

class TestServiceReflectionConcrete(AsyncTestCase):

    async def testGetInstance(self):
        """
        Tests that the ReflectionConcrete class correctly creates an instance of FakeClass
        using the getInstance method.

        Asserts:
            The returned instance is of type FakeClass.
        """
        reflect = ReflectionConcrete(FakeClass)
        instance = reflect.getInstance()
        self.assertIsInstance(instance, FakeClass)

    async def testGetClass(self):
        """
        Tests that the ReflectionConcrete.getClass() method returns the correct class object.

        This test creates a ReflectionConcrete instance with FakeClass, calls getClass(),
        and asserts that the returned class is FakeClass.
        """
        reflect = ReflectionConcrete(FakeClass)
        cls = reflect.getClass()
        self.assertEqual(cls, FakeClass)

    async def testGetClassName(self):
        """
        Tests that the ReflectionConcrete class correctly retrieves the name of the provided class.

        This test creates a ReflectionConcrete instance using the FakeClass,
        calls the getClassName() method, and asserts that the returned class name
        matches the expected string 'FakeClass'.
        """
        reflect = ReflectionConcrete(FakeClass)
        class_name = reflect.getClassName()
        self.assertEqual(class_name, 'FakeClass')

    async def testGetModuleName(self):
        """
        Tests that the getModuleName method of the ReflectionConcrete class returns the correct module name
        for the provided FakeClass. Asserts that the returned module name matches the expected string
        'tests.services.introspection.reflection.mock.fake_reflect_instance'.
        """
        reflect = ReflectionConcrete(FakeClass)
        module_name = reflect.getModuleName()
        self.assertEqual(module_name, 'tests.services.introspection.reflection.mock.fake_reflect_instance')

    async def testGetModuleWithClassName(self):
        """
        Tests that the `getModuleWithClassName` method of the `ReflectionConcrete` class
        returns the fully qualified module and class name for the given `FakeClass`.

        Asserts:
            The returned string matches the expected module path and class name:
            'tests.services.introspection.reflection.mock.fake_reflect_instance.FakeClass'
        """
        reflect = ReflectionConcrete(FakeClass)
        module_with_class_name = reflect.getModuleWithClassName()
        self.assertEqual(module_with_class_name, 'tests.services.introspection.reflection.mock.fake_reflect_instance.FakeClass')

    async def testGetDocstring(self):
        """
        Tests that the getDocstring method of ReflectionConcrete returns the correct docstring
        for the given class (FakeClass) by comparing it to the class's __doc__ attribute.
        """
        reflect = ReflectionConcrete(FakeClass)
        docstring = reflect.getDocstring()
        self.assertEqual(docstring, FakeClass.__doc__)

    async def testGetBaseClasses(self):
        """
        Tests that the getBaseClasses method of the ReflectionConcrete class returns the base classes of the given class.

        This test creates a ReflectionConcrete instance for the FakeClass, retrieves its base classes using getBaseClasses(),
        and asserts that the direct base class of FakeClass is included in the returned list.
        """
        reflect = ReflectionConcrete(FakeClass)
        base_classes = reflect.getBaseClasses()
        self.assertIn(FakeClass.__base__, base_classes)

    async def testGetSourceCode(self):
        """
        Tests that the `getSourceCode` method of the `ReflectionConcrete` class
        correctly retrieves the source code of the `FakeClass` class.

        The test asserts that the returned source code starts with the expected
        class definition line.
        """
        reflect = ReflectionConcrete(FakeClass)
        source_code = reflect.getSourceCode()
        self.assertTrue(source_code.startswith('class FakeClass'))

    async def testGetFile(self):
        """
        Tests that the `getFile` method of the `ReflectionConcrete` class returns the correct file path
        for the given `FakeClass`. Asserts that the returned file path ends with 'fake_reflect_instance.py'.
        """
        reflect = ReflectionConcrete(FakeClass)
        file_path = reflect.getFile()
        self.assertTrue(file_path.endswith('fake_reflect_instance.py'))

    async def testGetAnnotations(self):
        """
        Tests that the `getAnnotations` method of the `ReflectionConcrete` class
        correctly retrieves the annotations of the `FakeClass`, ensuring that
        'public_attr' is present in the returned annotations.
        """
        reflect = ReflectionConcrete(FakeClass)
        annotations = reflect.getAnnotations()
        self.assertIn('public_attr', annotations)

    async def testHasAttribute(self):
        """
        Test whether the ReflectionConcrete class correctly identifies the presence or absence of attributes on the target class.

        This test verifies that:
        - `hasAttribute('public_attr')` returns True for an existing attribute.
        - `hasAttribute('non_existent_attr')` returns False for a non-existent attribute.
        """
        reflect = ReflectionConcrete(FakeClass)
        self.assertTrue(reflect.hasAttribute('public_attr'))
        self.assertFalse(reflect.hasAttribute('non_existent_attr'))

    async def testGetAttribute(self):
        """
        Tests the `getAttribute` method of the `ReflectionConcrete` class.

        This test verifies that:
        - Retrieving an existing attribute ('public_attr') from `FakeClass` returns the correct value (42).
        - Retrieving a non-existent attribute ('non_existent_attr') returns `None`.
        """
        reflect = ReflectionConcrete(FakeClass)
        self.assertEqual(reflect.getAttribute('public_attr'), 42)
        self.assertIsNone(reflect.getAttribute('non_existent_attr'))

    async def testSetAttribute(self):
        """
        Test the setAttribute and getAttribute methods of the ReflectionConcrete class.

        This test verifies that attributes (including public, protected, and private) can be set and retrieved correctly
        using the setAttribute and getAttribute methods. It checks for:
        - Setting and getting a public attribute ('name').
        - Setting and getting a protected attribute ('_version').
        - Setting and getting a private attribute ('__python').
        """
        reflect = ReflectionConcrete(FakeClass)
        self.assertTrue(reflect.setAttribute('name', 'Orionis Framework'))
        self.assertEqual(reflect.getAttribute('name'), 'Orionis Framework')
        self.assertTrue(reflect.setAttribute('_version', '1.x'))
        self.assertEqual(reflect.getAttribute('_version'), '1.x')
        self.assertTrue(reflect.setAttribute('__python', '3.13+'))
        self.assertEqual(reflect.getAttribute('__python'), '3.13+')

    async def testRemoveAttribute(self):
        """
        Tests the removal of an attribute from a reflected class instance.

        This test verifies that:
        - An attribute ('new_attr') can be set on the reflected class instance.
        - The attribute can be successfully removed using `removeAttribute`.
        - After removal, the attribute no longer exists on the instance, as confirmed by `hasAttribute`.
        """
        reflect = ReflectionConcrete(FakeClass)
        reflect.setAttribute('new_attr', 100)
        self.assertTrue(reflect.removeAttribute('new_attr'))
        self.assertFalse(reflect.hasAttribute('new_attr'))

    async def testGetAttributes(self):
        """
        Tests that the ReflectionConcrete.getAttributes() method correctly retrieves all attribute names
        from the FakeClass, including public, protected, and private attributes.

        Asserts:
            - 'public_attr' is present in the returned attributes.
            - '_protected_attr' is present in the returned attributes.
            - '__private_attr' is present in the returned attributes.
        """
        reflect = ReflectionConcrete(FakeClass)
        attributes = reflect.getAttributes()
        self.assertIn('public_attr', attributes)
        self.assertIn('_protected_attr', attributes)
        self.assertIn('__private_attr', attributes)

    async def testGetPublicAttributes(self):
        """
        Test that the getPublicAttributes method of ReflectionConcrete correctly retrieves only the public attributes of FakeClass.

        This test verifies that:
        - 'public_attr' is included in the list of public attributes.
        - '_protected_attr' and '__private_attr' are not included in the list of public attributes.
        """
        reflect = ReflectionConcrete(FakeClass)
        public_attributes = reflect.getPublicAttributes()
        self.assertIn('public_attr', public_attributes)
        self.assertNotIn('_protected_attr', public_attributes)
        self.assertNotIn('__private_attr', public_attributes)

    async def testGetProtectedAttributes(self):
        """
        Test that the getProtectedAttributes method of ReflectionConcrete correctly identifies protected attributes.

        This test verifies that:
        - The protected attribute '_protected_attr' is included in the returned list.
        - The public attribute 'public_attr' is not included.
        - The private attribute '__private_attr' is not included.
        """
        reflect = ReflectionConcrete(FakeClass)
        protected_attributes = reflect.getProtectedAttributes()
        self.assertIn('_protected_attr', protected_attributes)
        self.assertNotIn('public_attr', protected_attributes)
        self.assertNotIn('__private_attr', protected_attributes)

    async def testGetPrivateAttributes(self):
        """
        Test that the getPrivateAttributes method of ReflectionConcrete correctly identifies private attributes
        of the FakeClass. Ensures that '__private_attr' is included in the result, while 'public_attr' and
        '_protected_attr' are not.
        """
        reflect = ReflectionConcrete(FakeClass)
        private_attributes = reflect.getPrivateAttributes()
        self.assertIn('__private_attr', private_attributes)
        self.assertNotIn('public_attr', private_attributes)
        self.assertNotIn('_protected_attr', private_attributes)

    async def testGetDunderAttributes(self):
        """
        Tests that the getDunderAttributes method of the ReflectionConcrete class
        correctly retrieves dunder (double underscore) attributes from the FakeClass.
        Asserts that the '__dd__' attribute is present in the returned list of dunder attributes.
        """
        reflect = ReflectionConcrete(FakeClass)
        dunder_attributes = reflect.getDunderAttributes()
        self.assertIn('__dd__', dunder_attributes)

    async def testGetMagicAttributes(self):
        """
        Tests that the `getMagicAttributes` method of the `ReflectionConcrete` class
        correctly retrieves magic (dunder) attributes from the `FakeClass`.

        Asserts that the magic attribute '__dd__' is present in the returned list of attributes.
        """
        reflect = ReflectionConcrete(FakeClass)
        magic_attributes = reflect.getMagicAttributes()
        self.assertIn('__dd__', magic_attributes)

    async def testHasMethod(self):
        """
        Tests the 'hasMethod' function of the ReflectionConcrete class.

        This test verifies that 'hasMethod' correctly identifies whether a given method name exists
        on the FakeClass. It asserts that 'instanceSyncMethod' is present and that a non-existent
        method returns False.
        """
        reflect = ReflectionConcrete(FakeClass)
        self.assertTrue(reflect.hasMethod('instanceSyncMethod'))
        self.assertFalse(reflect.hasMethod('non_existent_method'))

    async def testCallMethod(self):
        """
        Tests the 'callMethod' function of the ReflectionConcrete class by invoking the 'instanceSyncMethod'
        on a FakeClass instance with arguments 2 and 3, and asserts that the result is 5.
        """
        reflect = ReflectionConcrete(FakeClass)
        reflect.getInstance()  # Ensure instance is created
        result = reflect.callMethod('instanceSyncMethod', 2, 3)
        self.assertEqual(result, 5)

    async def testCallAsyncMethod(self):
        """
        Tests that the ReflectionConcrete class can correctly call an asynchronous instance method.
        Ensures that:
        - An instance of FakeClass is created via ReflectionConcrete.
        - The asynchronous method 'instanceAsyncMethod' is called with arguments 2 and 3.
        - The result of the method call is awaited and checked to be equal to 5.
        """
        reflect = ReflectionConcrete(FakeClass)
        reflect.getInstance()  # Ensure instance is created
        result = await reflect.callMethod('instanceAsyncMethod', 2, 3)
        self.assertEqual(result, 5)

    async def testSetMethod(self):
        """
        Tests the ability of the ReflectionConcrete class to dynamically set and call both synchronous and asynchronous methods on an instance of FakeClass.
        This test:
        - Defines a synchronous and an asynchronous mock method.
        - Sets these methods on a ReflectionConcrete instance.
        - Calls the methods using callMethod, verifying correct results for both sync and async cases.
        Asserts:
        - The synchronous method returns the correct sum.
        - The asynchronous method returns the correct sum after awaiting.
        """
        def mockSyncMethod(cls:FakeClass, num1, num2):
            return num1 + num2

        async def mockAsyncMethod(cls:FakeClass, num1, num2):
            import asyncio
            await asyncio.sleep(0.1)
            return num1 + num2

        reflect = ReflectionConcrete(FakeClass)
        reflect.getInstance()
        reflect.setMethod('mockSyncMethodConcrete', mockSyncMethod)
        reflect.setMethod('mockAsyncMethodConcrete', mockAsyncMethod)
        sync_result = reflect.callMethod('mockSyncMethodConcrete', 2, 3)
        async_result = await reflect.callMethod('mockAsyncMethodConcrete', 2, 3)
        self.assertEqual(sync_result, 5)
        self.assertEqual(async_result, 5)

    async def testRemoveMethod(self):
        """
        Test the removal of a dynamically added private method from a reflected class instance.
        This test:
        - Defines a protected and a private method.
        - Adds the private method to the reflected instance using `setMethod`.
        - Asserts that the method exists after addition.
        - Removes the method using `removeMethod`.
        - Asserts that the method no longer exists after removal.
        """
        def _testProtectedMethod(cls:FakeClass, x, y):
            return x + y

        def __testPrivateMethod(cls:FakeClass, x, y):
            return x + y

        reflect = ReflectionConcrete(FakeClass)
        reflect.getInstance()
        reflect.setMethod('__testPrivateMethod', __testPrivateMethod)
        self.assertTrue(reflect.hasMethod('__testPrivateMethod'))
        reflect.removeMethod('__testPrivateMethod')
        self.assertFalse(reflect.hasMethod('__testPrivateMethod'))

    async def testGetMethodSignature(self):
        """
        Tests that the ReflectionConcrete.getMethodSignature method correctly retrieves
        the signature of the 'instanceSyncMethod' from the FakeClass.

        Asserts that the returned signature string matches the expected format:
        '(self, x: int, y: int) -> int'.
        """
        reflect = ReflectionConcrete(FakeClass)
        signature = reflect.getMethodSignature('instanceSyncMethod')
        self.assertEqual(str(signature), '(self, x: int, y: int) -> int')

    async def testGetMethods(self):
        """
        Test that the getMethods function of the ReflectionConcrete class correctly retrieves
        the method names of the FakeClass, including both synchronous and asynchronous instance methods.
        """
        reflect = ReflectionConcrete(FakeClass)
        methods = reflect.getMethods()
        self.assertIn('instanceSyncMethod', methods)
        self.assertIn('instanceAsyncMethod', methods)

    async def testGetPublicMethods(self):
        """
        Test that the getPublicMethods method of ReflectionConcrete returns only the public methods of the given class.

        This test verifies that:
        - Public methods (e.g., 'instanceSyncMethod') are included in the returned list.
        - Protected methods (prefixed with a single underscore) are not included.
        - Private methods (prefixed with double underscores) are not included.
        """
        reflect = ReflectionConcrete(FakeClass)
        public_methods = reflect.getPublicMethods()
        self.assertIn('instanceSyncMethod', public_methods)
        self.assertNotIn('_protected_method', public_methods)
        self.assertNotIn('__private_method', public_methods)

    async def testGetPublicSyncMethods(self):
        """
        Test that ReflectionConcrete.getPublicSyncMethods() returns only public synchronous methods of the given class.

        This test verifies that:
        - Public synchronous methods (e.g., 'instanceSyncMethod') are included in the returned list.
        - Protected methods (prefixed with a single underscore) are not included.
        - Private methods (prefixed with double underscores) are not included.
        """
        reflect = ReflectionConcrete(FakeClass)
        public_sync_methods = reflect.getPublicSyncMethods()
        self.assertIn('instanceSyncMethod', public_sync_methods)
        self.assertNotIn('_protected_method', public_sync_methods)
        self.assertNotIn('__private_method', public_sync_methods)

    async def testGetPublicAsyncMethods(self):
        """
        Test that ReflectionConcrete.getPublicAsyncMethods() correctly identifies public asynchronous methods
        of the FakeClass, ensuring that protected and private async methods are excluded from the result.
        """
        reflect = ReflectionConcrete(FakeClass)
        public_async_methods = reflect.getPublicAsyncMethods()
        self.assertIn('instanceAsyncMethod', public_async_methods)
        self.assertNotIn('_protected_async_method', public_async_methods)
        self.assertNotIn('__private_async_method', public_async_methods)

    async def testGetProtectedMethods(self):
        """
        Test that the getProtectedMethods method of ReflectionConcrete correctly identifies protected methods
        in the FakeClass. Ensures that '_protectedAsyncMethod' is included, while public and private methods
        are excluded from the result.
        """
        reflect = ReflectionConcrete(FakeClass)
        protected_methods = reflect.getProtectedMethods()
        self.assertIn('_protectedAsyncMethod', protected_methods)
        self.assertNotIn('instanceSyncMethod', protected_methods)
        self.assertNotIn('__privateSyncMethod', protected_methods)

    async def testGetProtectedSyncMethods(self):
        """
        Test that the getProtectedSyncMethods method of ReflectionConcrete correctly identifies
        protected synchronous methods in the FakeClass.

        This test verifies that:
        - The protected synchronous method '_protectedsyncMethod' is included in the result.
        - The asynchronous method 'instanceAsyncMethod' is not included.
        - The private synchronous method '__privateSyncMethod' is not included.
        """
        reflect = ReflectionConcrete(FakeClass)
        protected_sync_methods = reflect.getProtectedSyncMethods()
        self.assertIn('_protectedsyncMethod', protected_sync_methods)
        self.assertNotIn('instanceAsyncMethod', protected_sync_methods)
        self.assertNotIn('__privateSyncMethod', protected_sync_methods)

    async def testGetProtectedAsyncMethods(self):
        """
        Tests that the getProtectedAsyncMethods method of ReflectionConcrete returns only protected async methods of FakeClass.

        This test creates a ReflectionConcrete object initialized with FakeClass,
        calls getProtectedAsyncMethods, and asserts that the returned list contains only protected async methods.
        """
        reflect = ReflectionConcrete(FakeClass)
        protected_async_methods = reflect.getProtectedAsyncMethods()
        self.assertIn('_protectedAsyncMethod', protected_async_methods)
        self.assertNotIn('instanceSyncMethod', protected_async_methods)
        self.assertNotIn('__privateSyncMethod', protected_async_methods)

    async def testGetPrivateMethods(self):
        """
        Tests that the getPrivateMethods method of ReflectionConcrete returns only private methods of FakeClass.

        This test creates a ReflectionConcrete object initialized with FakeClass,
        calls getPrivateMethods, and asserts that the returned list contains only private methods.
        """
        reflect = ReflectionConcrete(FakeClass)
        private_methods = reflect.getPrivateMethods()
        self.assertIn('__privateSyncMethod', private_methods)
        self.assertNotIn('instanceSyncMethod', private_methods)
        self.assertNotIn('_protectedAsyncMethod', private_methods)

    async def testGetPrivateSyncMethods(self):
        """
        Tests that the getPrivateSyncMethods method of ReflectionConcrete returns only private sync methods of FakeClass.

        This test creates a ReflectionConcrete object initialized with FakeClass,
        calls getPrivateSyncMethods, and asserts that the returned list contains only private sync methods.
        """
        reflect = ReflectionConcrete(FakeClass)
        private_sync_methods = reflect.getPrivateSyncMethods()
        self.assertIn('__privateSyncMethod', private_sync_methods)
        self.assertNotIn('instanceAsyncMethod', private_sync_methods)
        self.assertNotIn('_protectedAsyncMethod', private_sync_methods)

    async def testGetPrivateAsyncMethods(self):
        """
        Tests that the getPrivateAsyncMethods method of ReflectionConcrete returns only private async methods of FakeClass.

        This test creates a ReflectionConcrete object initialized with FakeClass,
        calls getPrivateAsyncMethods, and asserts that the returned list contains only private async methods.
        """
        reflect = ReflectionConcrete(FakeClass)
        private_async_methods = reflect.getPrivateAsyncMethods()
        self.assertIn('__privateAsyncMethod', private_async_methods)
        self.assertNotIn('instanceSyncMethod', private_async_methods)
        self.assertNotIn('_protectedAsyncMethod', private_async_methods)

    async def testGetPublicClassMethods(self):
        """
        Tests that the getPublicClassMethods method of ReflectionConcrete returns only public class methods of FakeClass.

        This test creates a ReflectionConcrete object initialized with FakeClass,
        calls getPublicClassMethods, and asserts that the returned list contains only public class methods.
        """
        reflect = ReflectionConcrete(FakeClass)
        public_class_methods = reflect.getPublicClassMethods()
        self.assertIn('classSyncMethod', public_class_methods)
        self.assertNotIn('_protected_class_method', public_class_methods)
        self.assertNotIn('__private_class_method', public_class_methods)

    async def testGetPublicClassSyncMethods(self):
        """
        Tests that the getPublicClassSyncMethods method of ReflectionConcrete returns only public class sync methods of FakeClass.

        This test creates a ReflectionConcrete object initialized with FakeClass,
        calls getPublicClassSyncMethods, and asserts that the returned list contains only public class sync methods.
        """
        reflect = ReflectionConcrete(FakeClass)
        public_class_sync_methods = reflect.getPublicClassSyncMethods()
        self.assertIn('classSyncMethod', public_class_sync_methods)
        self.assertNotIn('_protected_class_method', public_class_sync_methods)
        self.assertNotIn('__private_class_method', public_class_sync_methods)

    async def testGetPublicClassAsyncMethods(self):
        """
        Tests that the getPublicClassAsyncMethods method of ReflectionConcrete returns only public class async methods of FakeClass.

        This test creates a ReflectionConcrete object initialized with FakeClass,
        calls getPublicClassAsyncMethods, and asserts that the returned list contains only public class async methods.
        """
        reflect = ReflectionConcrete(FakeClass)
        public_class_async_methods = reflect.getPublicClassAsyncMethods()
        self.assertIn('classAsyncMethod', public_class_async_methods)
        self.assertNotIn('_protected_class_async_method', public_class_async_methods)
        self.assertNotIn('__private_class_async_method', public_class_async_methods)

    async def testGetProtectedClassMethods(self):
        """
        Tests that the getProtectedClassMethods method of ReflectionConcrete returns only protected class methods of FakeClass.

        This test creates a ReflectionConcrete object initialized with FakeClass,
        calls getProtectedClassMethods, and asserts that the returned list contains only protected class methods.
        """
        reflect = ReflectionConcrete(FakeClass)
        protected_class_methods = reflect.getProtectedClassMethods()
        self.assertIn('_classMethodProtected', protected_class_methods)
        self.assertNotIn('classSyncMethod', protected_class_methods)
        self.assertNotIn('__classMethodPrivate', protected_class_methods)

    async def testGetProtectedClassSyncMethods(self):
        """
        Tests that the getProtectedClassSyncMethods method of ReflectionConcrete returns only protected class sync methods of FakeClass.

        This test creates a ReflectionConcrete object initialized with FakeClass,
        calls getProtectedClassSyncMethods, and asserts that the returned list contains only protected class sync methods.
        """
        reflect = ReflectionConcrete(FakeClass)
        protected_class_sync_methods = reflect.getProtectedClassSyncMethods()
        self.assertIn('_classMethodProtected', protected_class_sync_methods)
        self.assertNotIn('classSyncMethod', protected_class_sync_methods)
        self.assertNotIn('__classSyncMethodPrivate', protected_class_sync_methods)

    async def testGetProtectedClassAsyncMethods(self):
        """
        Tests that the getProtectedClassAsyncMethods method of ReflectionConcrete returns only protected class async methods of FakeClass.

        This test creates a ReflectionConcrete object initialized with FakeClass,
        calls getProtectedClassAsyncMethods, and asserts that the returned list contains only protected class async methods.
        """
        reflect = ReflectionConcrete(FakeClass)
        protected_class_async_methods = reflect.getProtectedClassAsyncMethods()
        self.assertIn('_classAsyncMethodProtected', protected_class_async_methods)
        self.assertNotIn('classAsyncMethod', protected_class_async_methods)
        self.assertNotIn('__classAsyncMethodPrivate', protected_class_async_methods)

    async def testGetPrivateClassMethods(self):
        """
        Tests that the getPrivateClassMethods method of ReflectionConcrete returns only private class methods of FakeClass.

        This test creates a ReflectionConcrete object initialized with FakeClass,
        calls getPrivateClassMethods, and asserts that the returned list contains only private class methods.
        """
        reflect = ReflectionConcrete(FakeClass)
        private_class_methods = reflect.getPrivateClassMethods()
        self.assertIn('__classMethodPrivate', private_class_methods)
        self.assertNotIn('classSyncMethod', private_class_methods)
        self.assertNotIn('_classMethodProtected', private_class_methods)

    async def testGetPrivateClassSyncMethods(self):
        """
        Tests that the getPrivateClassSyncMethods method of ReflectionConcrete returns only private class sync methods of FakeClass.

        This test creates a ReflectionConcrete object initialized with FakeClass,
        calls getPrivateClassSyncMethods, and asserts that the returned list contains only private class sync methods.
        """
        reflect = ReflectionConcrete(FakeClass)
        private_class_methods = reflect.getPrivateClassSyncMethods()
        self.assertIn('__classMethodPrivate', private_class_methods)
        self.assertNotIn('classSyncMethod', private_class_methods)
        self.assertNotIn('_classMethodProtected', private_class_methods)

    async def testGetPrivateClassAsyncMethods(self):
        """
        Tests that the getPrivateClassAsyncMethods method of ReflectionConcrete returns only private class async methods of FakeClass.

        This test creates a ReflectionConcrete object initialized with FakeClass,
        calls getPrivateClassAsyncMethods, and asserts that the returned list contains only private class async methods.
        """
        reflect = ReflectionConcrete(FakeClass)
        private_class_async_methods = reflect.getPrivateClassAsyncMethods()
        self.assertIn('__classAsyncMethodPrivate', private_class_async_methods)
        self.assertNotIn('classAsyncMethod', private_class_async_methods)
        self.assertNotIn('_classAsyncMethodProtected', private_class_async_methods)

    async def testGetPublicStaticMethods(self):
        """
        Tests that the getPublicStaticMethods method of ReflectionConcrete returns only public static methods of FakeClass.

        This test creates a ReflectionConcrete object initialized with FakeClass,
        calls getPublicStaticMethods, and asserts that the returned list contains only public static methods.
        """
        reflect = ReflectionConcrete(FakeClass)
        public_static_methods = reflect.getPublicStaticMethods()
        self.assertIn('staticMethod', public_static_methods)
        self.assertIn('staticAsyncMethod', public_static_methods)
        self.assertNotIn('static_async_method', public_static_methods)

    async def testGetPublicStaticSyncMethods(self):
        """
        Tests that the getPublicStaticSyncMethods method of ReflectionConcrete returns only public static sync methods of FakeClass.

        This test creates a ReflectionConcrete object initialized with FakeClass,
        calls getPublicStaticSyncMethods, and asserts that the returned list contains only public static sync methods.
        """
        reflect = ReflectionConcrete(FakeClass)
        public_static_sync_methods = reflect.getPublicStaticSyncMethods()
        self.assertIn('staticMethod', public_static_sync_methods)
        self.assertNotIn('staticAsyncMethod', public_static_sync_methods)
        self.assertNotIn('static_async_method', public_static_sync_methods)

    async def testGetPublicStaticAsyncMethods(self):
        """
        Tests that the getPublicStaticAsyncMethods method of ReflectionConcrete returns only public static async methods of FakeClass.

        This test creates a ReflectionConcrete object initialized with FakeClass,
        calls getPublicStaticAsyncMethods, and asserts that the returned list contains only public static async methods.
        """
        reflect = ReflectionConcrete(FakeClass)
        public_static_async_methods = reflect.getPublicStaticAsyncMethods()
        self.assertIn('staticAsyncMethod', public_static_async_methods)
        self.assertNotIn('staticMethod', public_static_async_methods)
        self.assertNotIn('static_async_method', public_static_async_methods)

    async def testGetProtectedStaticMethods(self):
        """
        Tests that the getProtectedStaticMethods method of ReflectionConcrete returns only protected static methods of FakeClass.

        This test creates a ReflectionConcrete object initialized with FakeClass,
        calls getProtectedStaticMethods, and asserts that the returned list contains only protected static methods.
        """
        reflect = ReflectionConcrete(FakeClass)
        protected_static_methods = reflect.getProtectedStaticMethods()
        self.assertIn('_staticMethodProtected', protected_static_methods)
        self.assertNotIn('staticMethod', protected_static_methods)
        self.assertNotIn('__staticMethodPrivate', protected_static_methods)

    async def testGetProtectedStaticSyncMethods(self):
        """
        Tests that the getProtectedStaticSyncMethods method of ReflectionConcrete returns only protected static sync methods of FakeClass.

        This test creates a ReflectionConcrete object initialized with FakeClass,
        calls getProtectedStaticSyncMethods, and asserts that the returned list contains only protected static sync methods.
        """
        reflect = ReflectionConcrete(FakeClass)
        protected_static_sync_methods = reflect.getProtectedStaticSyncMethods()
        self.assertIn('_staticMethodProtected', protected_static_sync_methods)
        self.assertNotIn('staticAsyncMethod', protected_static_sync_methods)
        self.assertNotIn('__staticMethodPrivate', protected_static_sync_methods)

    async def testGetProtectedStaticAsyncMethods(self):
        """
        Tests that the getProtectedStaticAsyncMethods method of ReflectionConcrete returns only protected static async methods of FakeClass.

        This test creates a ReflectionConcrete object initialized with FakeClass,
        calls getProtectedStaticAsyncMethods, and asserts that the returned list contains only protected static async methods.
        """
        reflect = ReflectionConcrete(FakeClass)
        protected_static_async_methods = reflect.getProtectedStaticAsyncMethods()
        self.assertIn('_staticAsyncMethodProtected', protected_static_async_methods)
        self.assertNotIn('staticMethod', protected_static_async_methods)
        self.assertNotIn('__staticMethodPrivate', protected_static_async_methods)

    async def testGetPrivateStaticMethods(self):
        """
        Tests that the getPrivateStaticMethods method of ReflectionConcrete returns only private static methods of FakeClass.

        This test creates a ReflectionConcrete object initialized with FakeClass,
        calls getPrivateStaticMethods, and asserts that the returned list contains only private static methods.
        """
        reflect = ReflectionConcrete(FakeClass)
        private_static_methods = reflect.getPrivateStaticMethods()
        self.assertIn('__staticMethodPrivate', private_static_methods)
        self.assertNotIn('staticMethod', private_static_methods)
        self.assertNotIn('_staticMethodProtected', private_static_methods)

    async def testGetPrivateStaticSyncMethods(self):
        """
        Tests that the getPrivateStaticSyncMethods method of ReflectionConcrete returns only private static sync methods of FakeClass.

        This test creates a ReflectionConcrete object initialized with FakeClass,
        calls getPrivateStaticSyncMethods, and asserts that the returned list contains only private static sync methods.
        """
        reflect = ReflectionConcrete(FakeClass)
        private_static_sync_methods = reflect.getPrivateStaticSyncMethods()
        self.assertIn('__staticMethodPrivate', private_static_sync_methods)
        self.assertNotIn('staticMethod', private_static_sync_methods)
        self.assertNotIn('_staticMethodProtected', private_static_sync_methods)

    async def testGetPrivateStaticAsyncMethods(self):
        """
        Tests that the getPrivateStaticAsyncMethods method of ReflectionConcrete returns only private static async methods of FakeClass.

        This test creates a ReflectionConcrete object initialized with FakeClass,
        calls getPrivateStaticAsyncMethods, and asserts that the returned list contains only private static async methods.
        """
        reflect = ReflectionConcrete(FakeClass)
        private_static_async_methods = reflect.getPrivateStaticAsyncMethods()
        self.assertIn('__staticAsyncMethodPrivate', private_static_async_methods)
        self.assertNotIn('staticAsyncMethod', private_static_async_methods)
        self.assertNotIn('_staticAsyncMethodProtected', private_static_async_methods)

    async def testGetDunderMethods(self):
        """
        Test that the getDunderMethods method correctly retrieves dunder (double underscore) methods
        from ReflectionConcrete for the FakeClass.
        Assertions ensure that '__init__' is present in the results.
        """
        reflect = ReflectionConcrete(FakeClass)
        dunder_methods = reflect.getDunderMethods()
        self.assertIn('__init__', dunder_methods)

    async def testGetMagicMethods(self):
        """
        Test the retrieval of magic methods from ReflectionConcrete.
        This test verifies that the `getMagicMethods` method correctly identifies and returns
        magic methods (such as `__init__`) for ReflectionConcrete with FakeClass.
        """
        reflect = ReflectionConcrete(FakeClass)
        magic_methods = reflect.getMagicMethods()
        self.assertIn('__init__', magic_methods)

    async def testGetProperties(self):
        """
        Tests that the getProperties method of ReflectionConcrete returns properties of FakeClass.
        This test creates a ReflectionConcrete object initialized with FakeClass,
        calls getProperties, and asserts that the returned list contains properties.
        """
        reflect = ReflectionConcrete(FakeClass)
        properties = reflect.getProperties()
        self.assertIn('computed_public_property', properties)
        self.assertIn('_computed_property_protected', properties)
        self.assertIn('__computed_property_private', properties)

    async def testGetPublicProperties(self):
        """
        Tests that the getPublicProperties method of ReflectionConcrete returns only public properties of FakeClass.

        This test creates a ReflectionConcrete object initialized with FakeClass,
        calls getPublicProperties, and asserts that the returned list contains only public properties.
        """
        reflect = ReflectionConcrete(FakeClass)
        public_properties = reflect.getPublicProperties()
        self.assertIn('computed_public_property', public_properties)
        self.assertNotIn('_computed_property_protected', public_properties)
        self.assertNotIn('__computed_property_private', public_properties)

    async def testGetProtectedProperties(self):
        """
        Tests that the getProtectedProperties method of ReflectionConcrete returns only protected properties of FakeClass.

        This test creates a ReflectionConcrete object initialized with FakeClass,
        calls getProtectedProperties, and asserts that the returned list contains only protected properties.
        """
        reflect = ReflectionConcrete(FakeClass)
        protected_properties = reflect.getProtectedProperties()
        self.assertIn('_computed_property_protected', protected_properties)
        self.assertNotIn('computed_public_property', protected_properties)
        self.assertNotIn('__computed_property_private', protected_properties)

    async def testGetPrivateProperties(self):
        """
        Tests that the getPrivateProperties method of ReflectionConcrete returns only private properties of FakeClass.

        This test creates a ReflectionConcrete object initialized with FakeClass,
        calls getPrivateProperties, and asserts that the returned list contains only private properties.
        """
        reflect = ReflectionConcrete(FakeClass)
        private_properties = reflect.getPrivateProperties()
        self.assertIn('__computed_property_private', private_properties)
        self.assertNotIn('computed_public_property', private_properties)
        self.assertNotIn('_computed_property_protected', private_properties)

    async def testGetProperty(self):
        """
        Tests that the getProperty method of ReflectionConcrete returns the correct value for a given property name.

        This test creates a ReflectionConcrete object initialized with FakeClass,
        calls getProperty for 'computed_public_property', and asserts that the returned value matches the expected value.
        """
        reflect = ReflectionConcrete(FakeClass)
        value = reflect.getProperty('computed_public_property')
        self.assertEqual(value, FakeClass().computed_public_property)

    async def testGetPropertySignature(self):
        """
        Tests that the getPropertySignature method of ReflectionConcrete returns the correct signature for a given property name.
        """
        reflect = ReflectionConcrete(FakeClass)
        signature = reflect.getPropertySignature('computed_public_property')
        self.assertEqual(str(signature), '(self) -> str')

    async def testGetPropertyDocstring(self):
        """
        Tests that the getPropertyDocstring method of ReflectionConcrete returns the correct docstring for a given property name.
        This test creates a ReflectionConcrete object initialized with FakeClass,
        calls getPropertyDocstring for 'computed_public_property', and asserts that the returned docstring matches the expected value.
        """
        reflect = ReflectionConcrete(FakeClass)
        docstring = reflect.getPropertyDocstring('computed_public_property')
        self.assertIn('Returns the string "public" as', docstring)

    async def testGetConstructorDependencies(self):
        """
        Tests that the getConstructorDependencies method of ReflectionConcrete returns the correct constructor dependencies for FakeClass.
        This test creates a ReflectionConcrete object initialized with FakeClass,
        calls getConstructorDependencies, and asserts that the returned dependencies are returned as a ClassDependency object.
        """
        reflect = ReflectionConcrete(FakeClass)
        dependencies = reflect.getConstructorDependencies()
        self.assertIsInstance(dependencies, ClassDependency)

    async def testGetMethodDependencies(self):
        """
        Tests that the getMethodDependencies method of ReflectionConcrete returns the correct method dependencies for 'instanceSyncMethod'.
        This test creates a ReflectionConcrete object,
        calls getMethodDependencies for 'instanceSyncMethod', and asserts that the returned dependencies are as expected.
        """
        reflect = ReflectionConcrete(FakeClass)
        method_deps = reflect.getMethodDependencies('instanceSyncMethod')
        self.assertIn('x', method_deps.resolved)
        self.assertIn('y', method_deps.resolved)
        self.assertEqual(method_deps.resolved['x'].class_name, 'int')
        self.assertEqual(method_deps.resolved['y'].class_name, 'int')
        self.assertEqual(method_deps.resolved['x'].module_name, 'builtins')
        self.assertEqual(method_deps.resolved['y'].module_name, 'builtins')
        self.assertEqual(method_deps.resolved['x'].type, int)
        self.assertEqual(method_deps.resolved['y'].type, int)
        self.assertEqual(method_deps.resolved['x'].full_class_path, 'builtins.int')
        self.assertEqual(method_deps.resolved['y'].full_class_path, 'builtins.int')
        self.assertEqual(method_deps.unresolved, [])
