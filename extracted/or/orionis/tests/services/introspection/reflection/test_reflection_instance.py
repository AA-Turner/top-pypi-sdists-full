from orionis.services.introspection.dependencies.entities.class_dependencies import ClassDependency
from tests.services.introspection.reflection.mock.fake_reflect_instance import FakeClass
from orionis.services.introspection.instances.reflection import ReflectionInstance
from orionis.test.cases.asynchronous import AsyncTestCase

class TestServiceReflectionInstance(AsyncTestCase):

    async def testGetInstance(self):
        """
        Tests that the ReflectionInstance.getInstance() method returns an instance of the expected class.
        This test creates a ReflectionInstance with a FakeClass object, retrieves the instance using getInstance(),
        and asserts that the returned object is an instance of FakeClass.
        """
        reflect = ReflectionInstance(FakeClass())
        instance = reflect.getInstance()
        self.assertIsInstance(instance, FakeClass)

    async def testGetClass(self):
        """
        Tests that the `getClass` method of `ReflectionInstance` returns the correct class type
        for the given instance.
        This test creates a `ReflectionInstance` with an instance of `FakeClass`, calls `getClass`,
        and asserts that the returned class is `FakeClass`.
        """
        reflect = ReflectionInstance(FakeClass())
        cls = reflect.getClass()
        self.assertEqual(cls, FakeClass)

    async def testGetClassName(self):
        """
        Tests that the ReflectionInstance correctly retrieves the class name of the given object.
        This test creates an instance of FakeClass, wraps it with ReflectionInstance,
        and asserts that getClassName() returns the expected class name 'FakeClass'.
        """
        reflect = ReflectionInstance(FakeClass())
        class_name = reflect.getClassName()
        self.assertEqual(class_name, 'FakeClass')

    async def testGetModuleName(self):
        """
        Tests that the `getModuleName` method of `ReflectionInstance` returns the correct module name
        for the provided `FakeClass` instance.

        Asserts:
            The returned module name matches the expected string
            'tests.services.introspection.reflection.mock.fake_reflect_instance'.
        """
        reflect = ReflectionInstance(FakeClass())
        module_name = reflect.getModuleName()
        self.assertEqual(module_name, 'tests.services.introspection.reflection.mock.fake_reflect_instance')

    async def testGetModuleWithClassName(self):
        """
        Tests that the getModuleWithClassName method of ReflectionInstance returns the fully qualified
        module and class name of the provided instance.

        Asserts:
            The returned string matches the expected module and class path for FakeClass.
        """
        reflect = ReflectionInstance(FakeClass())
        module_with_class_name = reflect.getModuleWithClassName()
        self.assertEqual(module_with_class_name, 'tests.services.introspection.reflection.mock.fake_reflect_instance.FakeClass')

    async def testGetDocstring(self):
        """
        Test that the getDocstring method of ReflectionInstance returns the correct docstring
        for the provided class instance.
        """
        reflect = ReflectionInstance(FakeClass())
        docstring = reflect.getDocstring()
        self.assertEqual(docstring, FakeClass.__doc__)

    async def testGetBaseClasses(self):
        """
        Tests that the getBaseClasses method of ReflectionInstance correctly retrieves
        the base classes of the provided instance.

        This test creates a ReflectionInstance for a FakeClass object, calls getBaseClasses,
        and asserts that FakeClass's immediate base class is included in the returned list.
        """
        reflect = ReflectionInstance(FakeClass())
        base_classes = reflect.getBaseClasses()
        self.assertIn(FakeClass.__base__, base_classes)

    async def testGetSourceCode(self):
        """
        Tests that the `getSourceCode` method of `ReflectionInstance` correctly retrieves
        the source code of the provided class instance. Asserts that the returned source
        code starts with the expected class definition.
        """
        reflect = ReflectionInstance(FakeClass())
        source_code = reflect.getSourceCode()
        self.assertTrue(source_code.startswith('class FakeClass'))

    async def testGetFile(self):
        """
        Tests that the `getFile` method of `ReflectionInstance` returns the correct file path
        for the given instance. Asserts that the returned file path ends with 'fake_reflect_instance.py'.
        """
        reflect = ReflectionInstance(FakeClass())
        file_path = reflect.getFile()
        self.assertTrue(file_path.endswith('fake_reflect_instance.py'))

    async def testGetAnnotations(self):
        """
        Test that the ReflectionInstance.getAnnotations() method returns the correct annotations
        for the given FakeClass instance, specifically verifying that 'public_attr' is present
        in the returned annotations.
        """
        reflect = ReflectionInstance(FakeClass())
        annotations = reflect.getAnnotations()
        self.assertIn('public_attr', annotations)

    async def testHasAttribute(self):
        """
        Tests the hasAttribute method of the ReflectionInstance class.

        Verifies that hasAttribute returns True for an existing attribute ('public_attr')
        and False for a non-existent attribute ('non_existent_attr') on a FakeClass instance.
        """
        reflect = ReflectionInstance(FakeClass())
        self.assertTrue(reflect.hasAttribute('public_attr'))
        self.assertFalse(reflect.hasAttribute('non_existent_attr'))

    async def testGetAttribute(self):
        """
        Tests the `getAttribute` method of the `ReflectionInstance` class.

        Verifies that:
        - Retrieving an existing attribute ('public_attr') returns its correct value (42).
        - Retrieving a non-existent attribute ('non_existent_attr') returns None.
        """
        reflect = ReflectionInstance(FakeClass())
        self.assertEqual(reflect.getAttribute('public_attr'), 42)
        self.assertIsNone(reflect.getAttribute('non_existent_attr'))

    async def testSetAttribute(self):
        """
        Test the setAttribute method of the ReflectionInstance class.

        This test verifies that setAttribute correctly sets the value of attributes
        on the wrapped object, including public, protected, and private attributes.
        It also checks that the updated values can be retrieved using getAttribute.

        Assertions:
            - setAttribute returns True when setting a public attribute.
            - The value of the public attribute is updated correctly.
            - setAttribute returns True when setting a protected attribute.
            - The value of the protected attribute is updated correctly.
            - setAttribute returns True when setting a private attribute.
            - The value of the private attribute is updated correctly.
        """
        reflect = ReflectionInstance(FakeClass())
        self.assertTrue(reflect.setAttribute('name', 'Orionis Framework'))
        self.assertEqual(reflect.getAttribute('name'), 'Orionis Framework')
        self.assertTrue(reflect.setAttribute('_version', '1.x'))
        self.assertEqual(reflect.getAttribute('_version'), '1.x')
        self.assertTrue(reflect.setAttribute('__python', '3.13+'))
        self.assertEqual(reflect.getAttribute('__python'), '3.13+')

    async def testRemoveAttribute(self):
        """
        Test that the removeAttribute method successfully removes an attribute from the reflected instance.
        Verifies that the attribute is removed and no longer present after removal.
        """
        reflect = ReflectionInstance(FakeClass())
        reflect.setAttribute('new_attr', 100)
        self.assertTrue(reflect.removeAttribute('new_attr'))
        self.assertFalse(reflect.hasAttribute('new_attr'))

    async def testGetAttributes(self):
        """
        Tests that the ReflectionInstance.getAttributes() method correctly retrieves
        all attribute names from an instance of FakeClass, including public, protected,
        and private attributes.
        """
        reflect = ReflectionInstance(FakeClass())
        attributes = reflect.getAttributes()
        self.assertIn('public_attr', attributes)
        self.assertIn('_protected_attr', attributes)
        self.assertIn('__private_attr', attributes)

    async def testGetPublicAttributes(self):
        """
        Test that ReflectionInstance.getPublicAttributes() returns only public attributes of a class instance.

        This test verifies that:
        - Public attributes (e.g., 'public_attr') are included in the returned list.
        - Protected attributes (e.g., '_protected_attr') are not included.
        - Private attributes (e.g., '__private_attr') are not included.
        """
        reflect = ReflectionInstance(FakeClass())
        public_attributes = reflect.getPublicAttributes()
        self.assertIn('public_attr', public_attributes)
        self.assertNotIn('_protected_attr', public_attributes)
        self.assertNotIn('__private_attr', public_attributes)

    async def testGetProtectedAttributes(self):
        """
        Test that ReflectionInstance.getProtectedAttributes() correctly identifies protected attributes.

        This test verifies that:
        - Protected attributes (those prefixed with a single underscore) are included in the result.
        - Public attributes are not included.
        - Private attributes (those prefixed with double underscores) are not included.
        """
        reflect = ReflectionInstance(FakeClass())
        protected_attributes = reflect.getProtectedAttributes()
        self.assertIn('_protected_attr', protected_attributes)
        self.assertNotIn('public_attr', protected_attributes)
        self.assertNotIn('__private_attr', protected_attributes)

    async def testGetPrivateAttributes(self):
        """
        Test that the `getPrivateAttributes` method of `ReflectionInstance` correctly identifies and returns only the private attributes of a class instance.

        This test verifies that:
        - The private attribute (`__private_attr`) is included in the returned list.
        - The public attribute (`public_attr`) is not included.
        - The protected attribute (`_protected_attr`) is not included.
        """
        reflect = ReflectionInstance(FakeClass())
        private_attributes = reflect.getPrivateAttributes()
        self.assertIn('__private_attr', private_attributes)
        self.assertNotIn('public_attr', private_attributes)
        self.assertNotIn('_protected_attr', private_attributes)

    async def testGetDunderAttributes(self):
        """
        Tests that the getDunderAttributes method of ReflectionInstance correctly retrieves
        all double underscore (dunder) attributes from an instance of FakeClass.

        Asserts that the attribute '__dd__' is present in the returned list of dunder attributes.
        """
        reflect = ReflectionInstance(FakeClass())
        dunder_attributes = reflect.getDunderAttributes()
        self.assertIn('__dd__', dunder_attributes)

    async def testGetMagicAttributes(self):
        """
        Tests that the `getMagicAttributes` method of `ReflectionInstance` returns a list of magic attributes
        for the given instance, and verifies that the attribute '__dd__' is present in the result.
        """
        reflect = ReflectionInstance(FakeClass())
        magic_attributes = reflect.getMagicAttributes()
        self.assertIn('__dd__', magic_attributes)

    async def testHasMethod(self):
        """
        Tests the hasMethod function of the ReflectionInstance class.

        Verifies that hasMethod correctly identifies the presence or absence of a method
        on the provided FakeClass instance. Asserts that 'instanceSyncMethod' exists and
        'non_existent_method' does not.
        """
        reflect = ReflectionInstance(FakeClass())
        self.assertTrue(reflect.hasMethod('instanceSyncMethod'))
        self.assertFalse(reflect.hasMethod('non_existent_method'))

    async def testCallMethod(self):
        """
        Tests the callMethod function of the ReflectionInstance class.

        This test verifies that calling the 'instanceSyncMethod' on a FakeClass instance
        via ReflectionInstance.callMethod with arguments 2 and 3 returns the expected result (5).
        """
        reflect = ReflectionInstance(FakeClass())
        result = reflect.callMethod('instanceSyncMethod', 2, 3)
        self.assertEqual(result, 5)

    async def testCallAsyncMethod(self):
        """
        Tests that the ReflectionInstance can correctly call an asynchronous method on an instance
        and return the expected result.

        This test creates a ReflectionInstance for a FakeClass object, invokes the 'instanceAsyncMethod'
        asynchronously with arguments 2 and 3, and asserts that the result is 5.
        """
        reflect = ReflectionInstance(FakeClass())
        result = await reflect.callMethod('instanceAsyncMethod', 2, 3)
        self.assertEqual(result, 5)

    async def testSetMethod(self):
        """
        Tests the ability of ReflectionInstance to set and call both synchronous and asynchronous methods dynamically.
        This test:
        - Defines a synchronous and an asynchronous mock method.
        - Sets these methods on a ReflectionInstance of FakeClass using setMethod.
        - Calls the synchronous method using callMethod and checks the result.
        - Calls the asynchronous method using await callMethod and checks the result.
        - Asserts that both methods return the expected sum of their arguments.
        """

        def mockSyncMethod(cls:FakeClass, num1, num2):
            return num1 + num2

        async def mockAsyncMethod(cls:FakeClass, num1, num2):
            import asyncio
            await asyncio.sleep(0.1)
            return num1 + num2

        reflect = ReflectionInstance(FakeClass())
        reflect.setMethod('mockSyncMethodInstance', mockSyncMethod)
        reflect.setMethod('mockAsyncMethodInstance', mockAsyncMethod)
        sync_result = reflect.callMethod('mockSyncMethodInstance', 2, 3)
        async_result = await reflect.callMethod('mockAsyncMethodInstance', 2, 3)
        self.assertEqual(sync_result, 5)
        self.assertEqual(async_result, 5)

    async def testRemoveMethod(self):
        """
        Tests the removal of a dynamically added method from a ReflectionInstance.
        This test adds a protected-like method to a ReflectionInstance of FakeClass,
        verifies its existence, removes it, and then checks that it no longer exists.
        """
        def _testProtectedMethod(cls:FakeClass, x, y):
            return x + y

        def __testPrivateMethod(cls:FakeClass, x, y):
            return x + y

        reflect = ReflectionInstance(FakeClass())
        reflect.setMethod('_testProtectedMethod', _testProtectedMethod)
        self.assertTrue(reflect.hasMethod('_testProtectedMethod'))
        reflect.removeMethod('_testProtectedMethod')
        self.assertFalse(reflect.hasMethod('_testProtectedMethod'))

    async def testGetMethodSignature(self):
        """
        Tests that the ReflectionInstance.getMethodSignature method correctly retrieves
        the signature of the 'instanceSyncMethod' from the FakeClass instance.
        Asserts that the returned signature string matches the expected format:
        '(self, x: int, y: int) -> int'.
        """
        reflect = ReflectionInstance(FakeClass())
        signature = reflect.getMethodSignature('instanceSyncMethod')
        self.assertEqual(str(signature), '(self, x: int, y: int) -> int')

    async def testGetMethods(self):
        """
        Tests that the ReflectionInstance.getMethods() method correctly retrieves the names of all instance methods,
        including both synchronous and asynchronous methods, from the FakeClass instance.
        Asserts that 'instanceSyncMethod' and 'instanceAsyncMethod' are present in the returned methods list.
        """
        reflect = ReflectionInstance(FakeClass())
        methods = reflect.getMethods()
        self.assertIn('instanceSyncMethod', methods)
        self.assertIn('instanceAsyncMethod', methods)

    async def testGetPublicMethods(self):
        """
        Tests that the `getPublicMethods` method of `ReflectionInstance` returns only the public methods of a class instance.
        Verifies that:
            - Public methods (e.g., 'instanceSyncMethod') are included in the result.
            - Protected methods (prefixed with a single underscore) are not included.
            - Private methods (prefixed with double underscores) are not included.
        """
        reflect = ReflectionInstance(FakeClass())
        public_methods = reflect.getPublicMethods()
        self.assertIn('instanceSyncMethod', public_methods)
        self.assertNotIn('_protected_method', public_methods)
        self.assertNotIn('__private_method', public_methods)

    async def testGetPublicSyncMethods(self):
        """
        Test that ReflectionInstance.getPublicSyncMethods() returns only the names of public synchronous methods.

        This test verifies that:
        - Public synchronous methods (e.g., 'instanceSyncMethod') are included in the result.
        - Protected methods (prefixed with a single underscore) are excluded.
        - Private methods (prefixed with double underscores) are excluded.
        """
        reflect = ReflectionInstance(FakeClass())
        public_sync_methods = reflect.getPublicSyncMethods()
        self.assertIn('instanceSyncMethod', public_sync_methods)
        self.assertNotIn('_protected_method', public_sync_methods)
        self.assertNotIn('__private_method', public_sync_methods)

    async def testGetPublicAsyncMethods(self):
        """
        Test that ReflectionInstance.getPublicAsyncMethods() correctly identifies public asynchronous methods.

        This test verifies that:
        - Public async methods (e.g., 'instanceAsyncMethod') are included in the returned list.
        - Protected (prefixed with a single underscore) and private (double underscore) async methods are not included.
        """
        reflect = ReflectionInstance(FakeClass())
        public_async_methods = reflect.getPublicAsyncMethods()
        self.assertIn('instanceAsyncMethod', public_async_methods)
        self.assertNotIn('_protected_async_method', public_async_methods)
        self.assertNotIn('__private_async_method', public_async_methods)

    async def testGetProtectedMethods(self):
        """
        Test that ReflectionInstance.getProtectedMethods() correctly identifies protected methods.

        This test verifies that:
        - Protected methods (those prefixed with a single underscore) are included in the result.
        - Public methods are not included.
        - Private methods (those prefixed with double underscores) are not included.
        """
        reflect = ReflectionInstance(FakeClass())
        protected_methods = reflect.getProtectedMethods()
        self.assertIn('_protectedAsyncMethod', protected_methods)
        self.assertNotIn('instanceSyncMethod', protected_methods)
        self.assertNotIn('__privateSyncMethod', protected_methods)

    async def testGetProtectedSyncMethods(self):
        """
        Test that ReflectionInstance.getProtectedSyncMethods() correctly identifies protected synchronous methods.

        This test verifies that:
        - Protected synchronous methods (e.g., methods prefixed with a single underscore) are included in the result.
        - Asynchronous methods and private methods (e.g., methods prefixed with double underscores) are not included in the result.
        """
        reflect = ReflectionInstance(FakeClass())
        protected_sync_methods = reflect.getProtectedSyncMethods()
        self.assertIn('_protectedsyncMethod', protected_sync_methods)
        self.assertNotIn('instanceAsyncMethod', protected_sync_methods)
        self.assertNotIn('__privateSyncMethod', protected_sync_methods)

    async def testGetProtectedAsyncMethods(self):
        """
        Test that ReflectionInstance.getProtectedAsyncMethods() correctly identifies protected asynchronous methods.

        This test verifies that:
        - The protected asynchronous method '_protectedAsyncMethod' is included in the returned list.
        - The public synchronous method 'instanceSyncMethod' is not included.
        - The private synchronous method '__privateSyncMethod' is not included.
        """
        reflect = ReflectionInstance(FakeClass())
        protected_async_methods = reflect.getProtectedAsyncMethods()
        self.assertIn('_protectedAsyncMethod', protected_async_methods)
        self.assertNotIn('instanceSyncMethod', protected_async_methods)
        self.assertNotIn('__privateSyncMethod', protected_async_methods)

    async def testGetPrivateMethods(self):
        """
        Test that `getPrivateMethods` correctly identifies private methods of a class instance.

        This test verifies that:
        - The method `__privateSyncMethod` is included in the list of private methods.
        - The method `instanceSyncMethod` (a public method) is not included.
        - The method `_protectedAsyncMethod` (a protected method) is not included.
        """
        reflect = ReflectionInstance(FakeClass())
        private_methods = reflect.getPrivateMethods()
        self.assertIn('__privateSyncMethod', private_methods)
        self.assertNotIn('instanceSyncMethod', private_methods)
        self.assertNotIn('_protectedAsyncMethod', private_methods)

    async def testGetPrivateSyncMethods(self):
        """
        Test that ReflectionInstance.getPrivateSyncMethods correctly identifies private synchronous methods.

        This test verifies that:
        - The method '__privateSyncMethod' is included in the list of private synchronous methods.
        - The methods 'instanceAsyncMethod' and '_protectedAsyncMethod' are not included in the list.
        """
        reflect = ReflectionInstance(FakeClass())
        private_sync_methods = reflect.getPrivateSyncMethods()
        self.assertIn('__privateSyncMethod', private_sync_methods)
        self.assertNotIn('instanceAsyncMethod', private_sync_methods)
        self.assertNotIn('_protectedAsyncMethod', private_sync_methods)

    async def testGetPrivateAsyncMethods(self):
        """
        Test that ReflectionInstance.getPrivateAsyncMethods correctly identifies private asynchronous methods.

        This test verifies that:
        - The method '__privateAsyncMethod' is included in the list of private async methods.
        - The method 'instanceSyncMethod' is not included in the list.
        - The method '_protectedAsyncMethod' is not included in the list.
        """
        reflect = ReflectionInstance(FakeClass())
        private_async_methods = reflect.getPrivateAsyncMethods()
        self.assertIn('__privateAsyncMethod', private_async_methods)
        self.assertNotIn('instanceSyncMethod', private_async_methods)
        self.assertNotIn('_protectedAsyncMethod', private_async_methods)

    async def testGetPublicClassMethods(self):
        """
        Test that `getPublicClassMethods` returns only the public class methods of the given instance.

        This test verifies that:
        - Public class methods (e.g., 'classSyncMethod') are included in the result.
        - Protected (e.g., '_protected_class_method') and private (e.g., '__private_class_method') class methods are excluded from the result.
        """
        reflect = ReflectionInstance(FakeClass())
        public_class_methods = reflect.getPublicClassMethods()
        self.assertIn('classSyncMethod', public_class_methods)
        self.assertNotIn('_protected_class_method', public_class_methods)
        self.assertNotIn('__private_class_method', public_class_methods)

    async def testGetPublicClassSyncMethods(self):
        """
        Test that `getPublicClassSyncMethods` returns only public synchronous class methods.

        This test verifies that:
        - Public synchronous class methods (e.g., 'classSyncMethod') are included in the result.
        - Protected (methods starting with a single underscore) and private (methods starting with double underscores) class methods are excluded from the result.
        """
        reflect = ReflectionInstance(FakeClass())
        public_class_sync_methods = reflect.getPublicClassSyncMethods()
        self.assertIn('classSyncMethod', public_class_sync_methods)
        self.assertNotIn('_protected_class_method', public_class_sync_methods)
        self.assertNotIn('__private_class_method', public_class_sync_methods)

    async def testGetPublicClassAsyncMethods(self):
        """
        Test that ReflectionInstance.getPublicClassAsyncMethods() correctly identifies public asynchronous class methods.

        This test verifies that:
        - Public async class methods (e.g., 'classAsyncMethod') are included in the returned list.
        - Protected (prefixed with a single underscore) and private (prefixed with double underscores) async class methods are not included.
        """
        reflect = ReflectionInstance(FakeClass())
        public_class_async_methods = reflect.getPublicClassAsyncMethods()
        self.assertIn('classAsyncMethod', public_class_async_methods)
        self.assertNotIn('_protected_class_async_method', public_class_async_methods)
        self.assertNotIn('__private_class_async_method', public_class_async_methods)

    async def testGetProtectedClassMethods(self):
        """
        Test that ReflectionInstance.getProtectedClassMethods() correctly identifies protected class methods.

        This test verifies that:
        - Protected class methods (those prefixed with a single underscore) are included in the result.
        - Public class methods are not included.
        - Private class methods (those prefixed with double underscores) are not included.
        """
        reflect = ReflectionInstance(FakeClass())
        protected_class_methods = reflect.getProtectedClassMethods()
        self.assertIn('_classMethodProtected', protected_class_methods)
        self.assertNotIn('classSyncMethod', protected_class_methods)
        self.assertNotIn('__classMethodPrivate', protected_class_methods)

    async def testGetProtectedClassSyncMethods(self):
        """
        Test that ReflectionInstance.getProtectedClassSyncMethods correctly identifies
        protected (single underscore-prefixed) synchronous class methods.

        Asserts that:
            - '_classMethodProtected' is included in the returned list.
            - 'classSyncMethod' (public) is not included.
            - '__classSyncMethodPrivate' (private, double underscore) is not included.
        """
        reflect = ReflectionInstance(FakeClass())
        protected_class_sync_methods = reflect.getProtectedClassSyncMethods()
        self.assertIn('_classMethodProtected', protected_class_sync_methods)
        self.assertNotIn('classSyncMethod', protected_class_sync_methods)
        self.assertNotIn('__classSyncMethodPrivate', protected_class_sync_methods)

    async def testGetProtectedClassAsyncMethods(self):
        """
        Test that ReflectionInstance correctly retrieves protected asynchronous class methods.

        This test verifies that:
        - Protected async class methods (those prefixed with a single underscore) are included in the result.
        - Public async class methods are not included.
        - Private async class methods (those prefixed with double underscores) are not included.
        """
        reflect = ReflectionInstance(FakeClass())
        protected_class_async_methods = reflect.getProtectedClassAsyncMethods()
        self.assertIn('_classAsyncMethodProtected', protected_class_async_methods)
        self.assertNotIn('classAsyncMethod', protected_class_async_methods)
        self.assertNotIn('__classAsyncMethodPrivate', protected_class_async_methods)

    async def testGetPrivateClassMethods(self):
        """
        Test that `getPrivateClassMethods` correctly identifies private class methods.

        This test verifies that:
        - The private class method '__classMethodPrivate' is included in the returned list.
        - The public class method 'classSyncMethod' is not included.
        - The protected class method '_classMethodProtected' is not included.
        """
        reflect = ReflectionInstance(FakeClass())
        private_class_methods = reflect.getPrivateClassMethods()
        self.assertIn('__classMethodPrivate', private_class_methods)
        self.assertNotIn('classSyncMethod', private_class_methods)
        self.assertNotIn('_classMethodProtected', private_class_methods)

    async def testGetPrivateClassSyncMethods(self):
        """
        Test that ReflectionInstance.getPrivateClassSyncMethods() correctly identifies private class-level synchronous methods.

        This test verifies that:
        - The private class method '__classMethodPrivate' is included in the returned list.
        - The public class method 'classSyncMethod' is not included.
        - The protected class method '_classMethodProtected' is not included.
        """
        reflect = ReflectionInstance(FakeClass())
        private_class_methods = reflect.getPrivateClassSyncMethods()
        self.assertIn('__classMethodPrivate', private_class_methods)
        self.assertNotIn('classSyncMethod', private_class_methods)
        self.assertNotIn('_classMethodProtected', private_class_methods)

    async def testGetPrivateClassAsyncMethods(self):
        """
        Test that ReflectionInstance correctly retrieves private class asynchronous methods.

        This test verifies that:
        - The private async method '__classAsyncMethodPrivate' is included in the list of private class async methods.
        - The public async method 'classAsyncMethod' is not included.
        - The protected async method '_classAsyncMethodProtected' is not included.
        """
        reflect = ReflectionInstance(FakeClass())
        private_class_async_methods = reflect.getPrivateClassAsyncMethods()
        self.assertIn('__classAsyncMethodPrivate', private_class_async_methods)
        self.assertNotIn('classAsyncMethod', private_class_async_methods)
        self.assertNotIn('_classAsyncMethodProtected', private_class_async_methods)

    async def testGetPublicStaticMethods(self):
        """
        Tests that the `getPublicStaticMethods` method of `ReflectionInstance` correctly retrieves
        the names of public static methods from the `FakeClass` instance.

        Asserts that:
            - 'staticMethod' is included in the list of public static methods.
            - 'staticAsyncMethod' is included in the list of public static methods.
            - 'static_async_method' is not included in the list of public static methods.
        """
        reflect = ReflectionInstance(FakeClass())
        public_static_methods = reflect.getPublicStaticMethods()
        self.assertIn('staticMethod', public_static_methods)
        self.assertIn('staticAsyncMethod', public_static_methods)
        self.assertNotIn('static_async_method', public_static_methods)

    async def testGetPublicStaticSyncMethods(self):
        """
        Test that ReflectionInstance.getPublicStaticSyncMethods() correctly identifies public static synchronous methods.

        This test verifies that:
        - 'staticMethod' (a public static synchronous method) is included in the returned list.
        - 'staticAsyncMethod' and 'static_async_method' (presumed to be static asynchronous methods) are not included in the returned list.
        """
        reflect = ReflectionInstance(FakeClass())
        public_static_sync_methods = reflect.getPublicStaticSyncMethods()
        self.assertIn('staticMethod', public_static_sync_methods)
        self.assertNotIn('staticAsyncMethod', public_static_sync_methods)
        self.assertNotIn('static_async_method', public_static_sync_methods)

    async def testGetPublicStaticAsyncMethods(self):
        """
        Test that ReflectionInstance.getPublicStaticAsyncMethods() correctly identifies public static asynchronous methods.

        This test verifies that:
        - 'staticAsyncMethod' is included in the list of public static async methods.
        - 'staticMethod' and 'static_async_method' are not included in the list.
        """
        reflect = ReflectionInstance(FakeClass())
        public_static_async_methods = reflect.getPublicStaticAsyncMethods()
        self.assertIn('staticAsyncMethod', public_static_async_methods)
        self.assertNotIn('staticMethod', public_static_async_methods)
        self.assertNotIn('static_async_method', public_static_async_methods)

    async def testGetProtectedStaticMethods(self):
        """
        Test that ReflectionInstance.getProtectedStaticMethods() correctly identifies protected static methods.

        This test verifies that:
        - The protected static method '_staticMethodProtected' is included in the returned list.
        - The public static method 'staticMethod' is not included.
        - The private static method '__staticMethodPrivate' is not included.
        """
        reflect = ReflectionInstance(FakeClass())
        protected_static_methods = reflect.getProtectedStaticMethods()
        self.assertIn('_staticMethodProtected', protected_static_methods)
        self.assertNotIn('staticMethod', protected_static_methods)
        self.assertNotIn('__staticMethodPrivate', protected_static_methods)

    async def testGetProtectedStaticSyncMethods(self):
        """
        Test that ReflectionInstance.getProtectedStaticSyncMethods() correctly identifies
        protected static synchronous methods of the FakeClass.

        Asserts that:
            - '_staticMethodProtected' is included in the returned list.
            - 'staticAsyncMethod' and '__staticMethodPrivate' are not included.
        """
        reflect = ReflectionInstance(FakeClass())
        protected_static_sync_methods = reflect.getProtectedStaticSyncMethods()
        self.assertIn('_staticMethodProtected', protected_static_sync_methods)
        self.assertNotIn('staticAsyncMethod', protected_static_sync_methods)
        self.assertNotIn('__staticMethodPrivate', protected_static_sync_methods)

    async def testGetProtectedStaticAsyncMethods(self):
        """
        Test that ReflectionInstance correctly identifies protected static asynchronous methods.

        This test verifies that:
        - The protected static async method '_staticAsyncMethodProtected' is included in the list returned by getProtectedStaticAsyncMethods().
        - The public static method 'staticMethod' is not included in the list.
        - The private static method '__staticMethodPrivate' is not included in the list.
        """
        reflect = ReflectionInstance(FakeClass())
        protected_static_async_methods = reflect.getProtectedStaticAsyncMethods()
        self.assertIn('_staticAsyncMethodProtected', protected_static_async_methods)
        self.assertNotIn('staticMethod', protected_static_async_methods)
        self.assertNotIn('__staticMethodPrivate', protected_static_async_methods)

    async def testGetPrivateStaticMethods(self):
        """
        Test that `getPrivateStaticMethods` correctly identifies and returns the names of private static methods
        from the reflected class instance. Ensures that private static methods (those with double underscores)
        are included, while protected (single underscore) and public static methods are excluded from the result.
        """
        reflect = ReflectionInstance(FakeClass())
        private_static_methods = reflect.getPrivateStaticMethods()
        self.assertIn('__staticMethodPrivate', private_static_methods)
        self.assertNotIn('staticMethod', private_static_methods)
        self.assertNotIn('_staticMethodProtected', private_static_methods)

    async def testGetPrivateStaticSyncMethods(self):
        """
        Test that ReflectionInstance.getPrivateStaticSyncMethods() correctly identifies private static synchronous methods.

        This test verifies that:
        - The method '__staticMethodPrivate' (a private static sync method) is included in the returned list.
        - The methods 'staticMethod' (public) and '_staticMethodProtected' (protected) are not included in the returned list.
        """
        reflect = ReflectionInstance(FakeClass())
        private_static_sync_methods = reflect.getPrivateStaticSyncMethods()
        self.assertIn('__staticMethodPrivate', private_static_sync_methods)
        self.assertNotIn('staticMethod', private_static_sync_methods)
        self.assertNotIn('_staticMethodProtected', private_static_sync_methods)

    async def testGetPrivateStaticAsyncMethods(self):
        """
        Test that ReflectionInstance correctly identifies private static asynchronous methods.

        This test verifies that:
        - The list of private static async methods includes '__staticAsyncMethodPrivate'.
        - The list does not include 'staticAsyncMethod' (public) or '_staticAsyncMethodProtected' (protected).
        """
        reflect = ReflectionInstance(FakeClass())
        private_static_async_methods = reflect.getPrivateStaticAsyncMethods()
        self.assertIn('__staticAsyncMethodPrivate', private_static_async_methods)
        self.assertNotIn('staticAsyncMethod', private_static_async_methods)
        self.assertNotIn('_staticAsyncMethodProtected', private_static_async_methods)

    async def testGetDunderMethods(self):
        """
        Test that the getDunderMethods method of ReflectionInstance returns a list containing
        dunder (double underscore) methods of the given instance, such as '__init__' and '__class__'.
        """
        reflect = ReflectionInstance(FakeClass())
        dunder_methods = reflect.getDunderMethods()
        self.assertIn('__init__', dunder_methods)
        self.assertIn('__class__', dunder_methods)

    async def testGetMagicMethods(self):
        """
        Tests that the ReflectionInstance.getMagicMethods() method correctly retrieves
        the list of magic methods from the given FakeClass instance.

        Asserts that commonly expected magic methods such as '__init__' and '__class__'
        are present in the returned list.
        """
        reflect = ReflectionInstance(FakeClass())
        magic_methods = reflect.getMagicMethods()
        self.assertIn('__init__', magic_methods)
        self.assertIn('__class__', magic_methods)

    async def testGetProperties(self):
        """
        Test that ReflectionInstance.getProperties() returns all expected properties,
        including public, protected, and private computed properties of the target class.
        """
        reflect = ReflectionInstance(FakeClass())
        properties = reflect.getProperties()
        self.assertIn('computed_public_property', properties)
        self.assertIn('_computed_property_protected', properties)
        self.assertIn('__computed_property_private', properties)

    async def testGetPublicProperties(self):
        """
        Tests that the `getPublicProperties` method of `ReflectionInstance` correctly identifies
        and returns only the public properties of a given class instance.

        Verifies that:
            - Public properties (e.g., 'computed_public_property') are included in the result.
            - Protected (e.g., '_computed_property_protected') and private (e.g., '__computed_property_private') 
              properties are not included in the result.
        """
        reflect = ReflectionInstance(FakeClass())
        public_properties = reflect.getPublicProperties()
        self.assertIn('computed_public_property', public_properties)
        self.assertNotIn('_computed_property_protected', public_properties)
        self.assertNotIn('__computed_property_private', public_properties)

    async def testGetProtectedProperties(self):
        """
        Test that ReflectionInstance.getProtectedProperties() correctly identifies protected properties.

        This test verifies that:
        - Protected properties (those prefixed with a single underscore) are included in the result.
        - Public properties are not included.
        - Private properties (those prefixed with double underscores) are not included.
        """
        reflect = ReflectionInstance(FakeClass())
        protected_properties = reflect.getProtectedProperties()
        self.assertIn('_computed_property_protected', protected_properties)
        self.assertNotIn('computed_public_property', protected_properties)
        self.assertNotIn('__computed_property_private', protected_properties)

    async def testGetPrivateProperties(self):
        """
        Test that ReflectionInstance.getPrivateProperties() correctly identifies private properties.

        This test verifies that:
        - Private properties (those with double underscores) are included in the result.
        - Public and protected properties are not included in the result.
        """
        reflect = ReflectionInstance(FakeClass())
        private_properties = reflect.getPrivateProperties()
        self.assertIn('__computed_property_private', private_properties)
        self.assertNotIn('computed_public_property', private_properties)
        self.assertNotIn('_computed_property_protected', private_properties)

    async def testGetProperty(self):
        """
        Tests that the ReflectionInstance.getProperty method correctly retrieves the value of a computed public property
        from an instance of FakeClass.

        Asserts that the value returned by getProperty for 'computed_public_property' matches the actual property value
        from a new FakeClass instance.
        """
        reflect = ReflectionInstance(FakeClass())
        value = reflect.getProperty('computed_public_property')
        self.assertEqual(value, FakeClass().computed_public_property)

    async def testGetPropertySignature(self):
        """
        Tests that the `getPropertySignature` method of `ReflectionInstance` correctly retrieves
        the signature of the specified property ('computed_public_property') from a `FakeClass` instance.
        Asserts that the returned signature string matches the expected format '(self) -> str'.
        """
        reflect = ReflectionInstance(FakeClass())
        signature = reflect.getPropertySignature('computed_public_property')
        self.assertEqual(str(signature), '(self) -> str')

    async def testGetPropertyDocstring(self):
        """
        Tests that the getPropertyDocstring method of ReflectionInstance correctly retrieves
        the docstring for the specified property ('computed_public_property') of the FakeClass instance.
        Asserts that the returned docstring contains the expected description.
        """
        reflect = ReflectionInstance(FakeClass())
        docstring = reflect.getPropertyDocstring('computed_public_property')
        self.assertIn('Returns the string "public" as', docstring)

    async def testGetConstructorDependencies(self):
        """
        Tests that the `getConstructorDependencies` method of `ReflectionInstance` returns an instance of `ClassDependency`.

        This test creates a `ReflectionInstance` for a `FakeClass` object, retrieves its constructor dependencies,
        and asserts that the returned value is an instance of `ClassDependency`.
        """
        reflect = ReflectionInstance(FakeClass())
        dependencies = reflect.getConstructorDependencies()
        self.assertIsInstance(dependencies, ClassDependency)

    async def testGetMethodDependencies(self):
        """
        Test that the `getMethodDependencies` method of `ReflectionInstance` correctly resolves
        the dependencies of the 'instanceSyncMethod' in `FakeClass`.

        This test verifies that:
          - The method dependencies 'x' and 'y' are present in the resolved dependencies.
          - Both 'x' and 'y' are identified as integers (`int`), with the correct class name, module name,
            type, and full class path.
          - There are no unresolved dependencies.
        """
        reflect = ReflectionInstance(FakeClass())
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