from orionis.services.introspection.concretes.reflection import ReflectionConcrete
from orionis.services.introspection.dependencies.entities.resolve_argument import ResolveArguments
from tests.services.introspection.reflection.mock.fake_reflect_instance import FakeClass
from orionis.test.cases.asynchronous import AsyncTestCase

class TestServiceReflectionConcrete(AsyncTestCase):

    async def testGetInstance(self):
        """
        Test that ReflectionConcrete creates an instance of FakeClass using getInstance.

        Returns
        -------
        None
            This method asserts that the returned instance is of type FakeClass.
        """
        reflect = ReflectionConcrete(FakeClass)
        instance = reflect.getInstance()
        self.assertIsInstance(instance, FakeClass)

    async def testGetClass(self):
        """
        Test that ReflectionConcrete.getClass returns the correct class object.

        Returns
        -------
        None
            Asserts that the returned class is FakeClass.
        """
        reflect = ReflectionConcrete(FakeClass)
        cls = reflect.getClass()
        self.assertEqual(cls, FakeClass)

    async def testGetClassName(self):
        """
        Test that ReflectionConcrete retrieves the correct class name.

        Returns
        -------
        None
            Asserts that the returned class name matches 'FakeClass'.
        """
        reflect = ReflectionConcrete(FakeClass)
        class_name = reflect.getClassName()
        self.assertEqual(class_name, 'FakeClass')

    async def testGetModuleName(self):
        """
        Test that ReflectionConcrete.getModuleName returns the correct module name for FakeClass.

        Returns
        -------
        None
            Asserts that the returned module name matches the expected string.
        """
        reflect = ReflectionConcrete(FakeClass)
        module_name = reflect.getModuleName()
        self.assertEqual(module_name, 'tests.services.introspection.reflection.mock.fake_reflect_instance')

    async def testGetModuleWithClassName(self):
        """
        Test that ReflectionConcrete.getModuleWithClassName returns the fully qualified module and class name.

        Returns
        -------
        None
            Asserts that the returned string matches the expected module path and class name.
        """
        reflect = ReflectionConcrete(FakeClass)
        module_with_class_name = reflect.getModuleWithClassName()
        self.assertEqual(module_with_class_name, 'tests.services.introspection.reflection.mock.fake_reflect_instance.FakeClass')

    async def testGetDocstring(self):
        """
        Test that ReflectionConcrete.getDocstring returns the correct docstring for FakeClass.

        Returns
        -------
        None
            Asserts that the returned docstring matches FakeClass.__doc__.
        """
        reflect = ReflectionConcrete(FakeClass)
        docstring = reflect.getDocstring()
        self.assertEqual(docstring, FakeClass.__doc__)

    async def testGetBaseClasses(self):
        """
        Test that ReflectionConcrete.getBaseClasses returns the base classes of FakeClass.

        Returns
        -------
        None
            Asserts that the direct base class of FakeClass is included in the returned list.
        """
        reflect = ReflectionConcrete(FakeClass)
        base_classes = reflect.getBaseClasses()
        self.assertIn(FakeClass.__base__, base_classes)

    async def testGetSourceCode(self):
        """
        Test that ReflectionConcrete.getSourceCode retrieves the source code of FakeClass.

        Returns
        -------
        None
            Asserts that the returned source code starts with the expected class definition line.
        """
        reflect = ReflectionConcrete(FakeClass)
        source_code = reflect.getSourceCode()
        self.assertTrue(source_code.startswith('class FakeClass'))

    async def testGetFile(self):
        """
        Test that ReflectionConcrete.getFile returns the correct file path for FakeClass.

        Returns
        -------
        None
            Asserts that the returned file path ends with 'fake_reflect_instance.py'.
        """
        reflect = ReflectionConcrete(FakeClass)
        file_path = reflect.getFile()
        self.assertTrue(file_path.endswith('fake_reflect_instance.py'))

    async def testGetAnnotations(self):
        """
        Test that ReflectionConcrete.getAnnotations retrieves the annotations of FakeClass.

        Returns
        -------
        None
            Asserts that 'public_attr' is present in the returned annotations.
        """
        reflect = ReflectionConcrete(FakeClass)
        annotations = reflect.getAnnotations()
        self.assertIn('public_attr', annotations)

    async def testHasAttribute(self):
        """
        Test whether ReflectionConcrete correctly identifies the presence or absence of attributes.

        Returns
        -------
        None
            Asserts that hasAttribute returns True for an existing attribute and False for a non-existent attribute.
        """
        reflect = ReflectionConcrete(FakeClass)
        self.assertTrue(reflect.hasAttribute('public_attr'))
        self.assertFalse(reflect.hasAttribute('non_existent_attr'))

    async def testGetAttribute(self):
        """
        Test ReflectionConcrete.getAttribute for retrieving attribute values.

        Returns
        -------
        None
            Asserts correct value for an existing attribute and None for a non-existent attribute.
        """
        reflect = ReflectionConcrete(FakeClass)
        self.assertEqual(reflect.getAttribute('public_attr'), 42)
        self.assertIsNone(reflect.getAttribute('non_existent_attr'))

    async def testSetAttribute(self):
        """
        Test ReflectionConcrete.setAttribute and getAttribute for setting and retrieving attributes.

        Returns
        -------
        None
            Asserts that public, protected, and private attributes can be set and retrieved correctly.
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
        Test the removal of an attribute from a reflected class instance.

        Returns
        -------
        None
            Asserts that an attribute can be set, removed, and is no longer present after removal.
        """
        reflect = ReflectionConcrete(FakeClass)
        reflect.setAttribute('new_attr', 100)
        self.assertTrue(reflect.removeAttribute('new_attr'))
        self.assertFalse(reflect.hasAttribute('new_attr'))

    async def testGetAttributes(self):
        """
        Test that ReflectionConcrete.getAttributes retrieves all attribute names from FakeClass.

        Returns
        -------
        None
            Asserts that public, protected, and private attributes are present in the returned list.
        """
        reflect = ReflectionConcrete(FakeClass)
        attributes = reflect.getAttributes()
        self.assertIn('public_attr', attributes)
        self.assertIn('_protected_attr', attributes)
        self.assertIn('__private_attr', attributes)

    async def testGetPublicAttributes(self):
        """
        Test that ReflectionConcrete.getPublicAttributes retrieves only public attributes.

        Returns
        -------
        None
            Asserts that only public attributes are included in the result.
        """
        reflect = ReflectionConcrete(FakeClass)
        public_attributes = reflect.getPublicAttributes()
        self.assertIn('public_attr', public_attributes)
        self.assertNotIn('_protected_attr', public_attributes)
        self.assertNotIn('__private_attr', public_attributes)

    async def testGetProtectedAttributes(self):
        """
        Test that ReflectionConcrete.getProtectedAttributes identifies protected attributes.

        Returns
        -------
        None
            Asserts that only protected attributes are included in the result.
        """
        reflect = ReflectionConcrete(FakeClass)
        protected_attributes = reflect.getProtectedAttributes()
        self.assertIn('_protected_attr', protected_attributes)
        self.assertNotIn('public_attr', protected_attributes)
        self.assertNotIn('__private_attr', protected_attributes)

    async def testGetPrivateAttributes(self):
        """
        Test that ReflectionConcrete.getPrivateAttributes identifies private attributes.

        Returns
        -------
        None
            Asserts that only private attributes are included in the result.
        """
        reflect = ReflectionConcrete(FakeClass)
        private_attributes = reflect.getPrivateAttributes()
        self.assertIn('__private_attr', private_attributes)
        self.assertNotIn('public_attr', private_attributes)
        self.assertNotIn('_protected_attr', private_attributes)

    async def testGetDunderAttributes(self):
        """
        Test that ReflectionConcrete.getDunderAttributes retrieves dunder attributes.

        Returns
        -------
        None
            Asserts that '__dd__' is present in the returned list of dunder attributes.
        """
        reflect = ReflectionConcrete(FakeClass)
        dunder_attributes = reflect.getDunderAttributes()
        self.assertIn('__dd__', dunder_attributes)

    async def testGetMagicAttributes(self):
        """
        Test that ReflectionConcrete.getMagicAttributes retrieves magic (dunder) attributes.

        Returns
        -------
        None
            Asserts that '__dd__' is present in the returned list of magic attributes.
        """
        reflect = ReflectionConcrete(FakeClass)
        magic_attributes = reflect.getMagicAttributes()
        self.assertIn('__dd__', magic_attributes)

    async def testHasMethod(self):
        """
        Test that ReflectionConcrete.hasMethod identifies the presence of methods.

        Returns
        -------
        None
            Asserts that an existing method is found and a non-existent method is not found.
        """
        reflect = ReflectionConcrete(FakeClass)
        self.assertTrue(reflect.hasMethod('instanceSyncMethod'))
        self.assertFalse(reflect.hasMethod('non_existent_method'))

    async def testCallMethod(self):
        """
        Test that ReflectionConcrete.callMethod invokes a synchronous method with arguments.

        Returns
        -------
        None
            Asserts that the result of calling 'instanceSyncMethod' with arguments 2 and 3 is 5.
        """
        reflect = ReflectionConcrete(FakeClass)
        reflect.getInstance()  # Ensure instance is created
        result = reflect.callMethod('instanceSyncMethod', 2, 3)
        self.assertEqual(result, 5)

    async def testCallAsyncMethod(self):
        """
        Test that ReflectionConcrete can call an asynchronous instance method.

        Returns
        -------
        None
            Asserts that the result of calling 'instanceAsyncMethod' with arguments 2 and 3 is 5.
        """
        reflect = ReflectionConcrete(FakeClass)
        reflect.getInstance()  # Ensure instance is created
        result = await reflect.callMethod('instanceAsyncMethod', 2, 3)
        self.assertEqual(result, 5)

    async def testSetMethod(self):
        """
        Test that ReflectionConcrete can dynamically set and call synchronous and asynchronous methods.

        Returns
        -------
        None
            Asserts correct results for both sync and async dynamically set methods.
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

        Returns
        -------
        None
            Asserts that the method exists after addition and is removed successfully.
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
        Test that ReflectionConcrete.getMethodSignature retrieves the signature of a method.

        Returns
        -------
        None
            Asserts that the returned signature string matches the expected format.
        """
        reflect = ReflectionConcrete(FakeClass)
        signature = reflect.getMethodSignature('instanceSyncMethod')
        self.assertEqual(str(signature), '(self, x: int, y: int) -> int')

    async def testGetMethods(self):
        """
        Test that ReflectionConcrete.getMethods retrieves method names of FakeClass.

        Returns
        -------
        None
            Asserts that both synchronous and asynchronous instance methods are present.
        """
        reflect = ReflectionConcrete(FakeClass)
        methods = reflect.getMethods()
        self.assertIn('instanceSyncMethod', methods)
        self.assertIn('instanceAsyncMethod', methods)

    async def testGetPublicMethods(self):
        """
        Test that ReflectionConcrete.getPublicMethods returns only public methods.

        Returns
        -------
        None
            Asserts that public methods are included and protected/private methods are excluded.
        """
        reflect = ReflectionConcrete(FakeClass)
        public_methods = reflect.getPublicMethods()
        self.assertIn('instanceSyncMethod', public_methods)
        self.assertNotIn('_protected_method', public_methods)
        self.assertNotIn('__private_method', public_methods)

    async def testGetPublicSyncMethods(self):
        """
        Test that ReflectionConcrete.getPublicSyncMethods returns only public synchronous methods.

        Returns
        -------
        None
            Asserts that only public synchronous methods are included in the result.
        """
        reflect = ReflectionConcrete(FakeClass)
        public_sync_methods = reflect.getPublicSyncMethods()
        self.assertIn('instanceSyncMethod', public_sync_methods)
        self.assertNotIn('_protected_method', public_sync_methods)
        self.assertNotIn('__private_method', public_sync_methods)

    async def testGetPublicAsyncMethods(self):
        """
        Test that ReflectionConcrete.getPublicAsyncMethods identifies public asynchronous methods.

        Returns
        -------
        None
            Asserts that only public async methods are included in the result.
        """
        reflect = ReflectionConcrete(FakeClass)
        public_async_methods = reflect.getPublicAsyncMethods()
        self.assertIn('instanceAsyncMethod', public_async_methods)
        self.assertNotIn('_protected_async_method', public_async_methods)
        self.assertNotIn('__private_async_method', public_async_methods)

    async def testGetProtectedMethods(self):
        """
        Test that ReflectionConcrete.getProtectedMethods identifies protected methods.

        Returns
        -------
        None
            Asserts that only protected methods are included in the result.
        """
        reflect = ReflectionConcrete(FakeClass)
        protected_methods = reflect.getProtectedMethods()
        self.assertIn('_protectedAsyncMethod', protected_methods)
        self.assertNotIn('instanceSyncMethod', protected_methods)
        self.assertNotIn('__privateSyncMethod', protected_methods)

    async def testGetProtectedSyncMethods(self):
        """
        Test that ReflectionConcrete.getProtectedSyncMethods identifies protected synchronous methods.

        Returns
        -------
        None
            Asserts that only protected synchronous methods are included in the result.
        """
        reflect = ReflectionConcrete(FakeClass)
        protected_sync_methods = reflect.getProtectedSyncMethods()
        self.assertIn('_protectedsyncMethod', protected_sync_methods)
        self.assertNotIn('instanceAsyncMethod', protected_sync_methods)
        self.assertNotIn('__privateSyncMethod', protected_sync_methods)

    async def testGetProtectedAsyncMethods(self):
        """
        Test that ReflectionConcrete.getProtectedAsyncMethods returns only protected async methods.

        Returns
        -------
        None
            Asserts that only protected async methods are included in the result.
        """
        reflect = ReflectionConcrete(FakeClass)
        protected_async_methods = reflect.getProtectedAsyncMethods()
        self.assertIn('_protectedAsyncMethod', protected_async_methods)
        self.assertNotIn('instanceSyncMethod', protected_async_methods)
        self.assertNotIn('__privateSyncMethod', protected_async_methods)

    async def testGetPrivateMethods(self):
        """
        Test that ReflectionConcrete.getPrivateMethods returns only private methods.

        Returns
        -------
        None
            Asserts that only private methods are included in the result.
        """
        reflect = ReflectionConcrete(FakeClass)
        private_methods = reflect.getPrivateMethods()
        self.assertIn('__privateSyncMethod', private_methods)
        self.assertNotIn('instanceSyncMethod', private_methods)
        self.assertNotIn('_protectedAsyncMethod', private_methods)

    async def testGetPrivateSyncMethods(self):
        """
        Test that ReflectionConcrete.getPrivateSyncMethods returns only private sync methods.

        Returns
        -------
        None
            Asserts that only private sync methods are included in the result.
        """
        reflect = ReflectionConcrete(FakeClass)
        private_sync_methods = reflect.getPrivateSyncMethods()
        self.assertIn('__privateSyncMethod', private_sync_methods)
        self.assertNotIn('instanceAsyncMethod', private_sync_methods)
        self.assertNotIn('_protectedAsyncMethod', private_sync_methods)

    async def testGetPrivateAsyncMethods(self):
        """
        Test that ReflectionConcrete.getPrivateAsyncMethods returns only private async methods.

        Returns
        -------
        None
            Asserts that only private async methods are included in the result.
        """
        reflect = ReflectionConcrete(FakeClass)
        private_async_methods = reflect.getPrivateAsyncMethods()
        self.assertIn('__privateAsyncMethod', private_async_methods)
        self.assertNotIn('instanceSyncMethod', private_async_methods)
        self.assertNotIn('_protectedAsyncMethod', private_async_methods)

    async def testGetPublicClassMethods(self):
        """
        Test that ReflectionConcrete.getPublicClassMethods returns only public class methods.

        Returns
        -------
        None
            Asserts that only public class methods are included in the result.
        """
        reflect = ReflectionConcrete(FakeClass)
        public_class_methods = reflect.getPublicClassMethods()
        self.assertIn('classSyncMethod', public_class_methods)
        self.assertNotIn('_protected_class_method', public_class_methods)
        self.assertNotIn('__private_class_method', public_class_methods)

    async def testGetPublicClassSyncMethods(self):
        """
        Test that ReflectionConcrete.getPublicClassSyncMethods returns only public class sync methods.

        Returns
        -------
        None
            Asserts that only public class sync methods are included in the result.
        """
        reflect = ReflectionConcrete(FakeClass)
        public_class_sync_methods = reflect.getPublicClassSyncMethods()
        self.assertIn('classSyncMethod', public_class_sync_methods)
        self.assertNotIn('_protected_class_method', public_class_sync_methods)
        self.assertNotIn('__private_class_method', public_class_sync_methods)

    async def testGetPublicClassAsyncMethods(self):
        """
        Test that ReflectionConcrete.getPublicClassAsyncMethods returns only public class async methods.

        Returns
        -------
        None
            Asserts that only public class async methods are included in the result.
        """
        reflect = ReflectionConcrete(FakeClass)
        public_class_async_methods = reflect.getPublicClassAsyncMethods()
        self.assertIn('classAsyncMethod', public_class_async_methods)
        self.assertNotIn('_protected_class_async_method', public_class_async_methods)
        self.assertNotIn('__private_class_async_method', public_class_async_methods)

    async def testGetProtectedClassMethods(self):
        """
        Test that ReflectionConcrete.getProtectedClassMethods returns only protected class methods.

        Returns
        -------
        None
            Asserts that only protected class methods are included in the result.
        """
        reflect = ReflectionConcrete(FakeClass)
        protected_class_methods = reflect.getProtectedClassMethods()
        self.assertIn('_classMethodProtected', protected_class_methods)
        self.assertNotIn('classSyncMethod', protected_class_methods)
        self.assertNotIn('__classMethodPrivate', protected_class_methods)

    async def testGetProtectedClassSyncMethods(self):
        """
        Test that ReflectionConcrete.getProtectedClassSyncMethods returns only protected class sync methods.

        Returns
        -------
        None
            Asserts that only protected class sync methods are included in the result.
        """
        reflect = ReflectionConcrete(FakeClass)
        protected_class_sync_methods = reflect.getProtectedClassSyncMethods()
        self.assertIn('_classMethodProtected', protected_class_sync_methods)
        self.assertNotIn('classSyncMethod', protected_class_sync_methods)
        self.assertNotIn('__classSyncMethodPrivate', protected_class_sync_methods)

    async def testGetProtectedClassAsyncMethods(self):
        """
        Test that ReflectionConcrete.getProtectedClassAsyncMethods returns only protected class async methods.

        Returns
        -------
        None
            Asserts that only protected class async methods are included in the result.
        """
        reflect = ReflectionConcrete(FakeClass)
        protected_class_async_methods = reflect.getProtectedClassAsyncMethods()
        self.assertIn('_classAsyncMethodProtected', protected_class_async_methods)
        self.assertNotIn('classAsyncMethod', protected_class_async_methods)
        self.assertNotIn('__classAsyncMethodPrivate', protected_class_async_methods)

    async def testGetPrivateClassMethods(self):
        """
        Test that ReflectionConcrete.getPrivateClassMethods returns only private class methods.

        Returns
        -------
        None
            Asserts that only private class methods are included in the result.
        """
        reflect = ReflectionConcrete(FakeClass)
        private_class_methods = reflect.getPrivateClassMethods()
        self.assertIn('__classMethodPrivate', private_class_methods)
        self.assertNotIn('classSyncMethod', private_class_methods)
        self.assertNotIn('_classMethodProtected', private_class_methods)

    async def testGetPrivateClassSyncMethods(self):
        """
        Test that ReflectionConcrete.getPrivateClassSyncMethods returns only private class sync methods.

        Returns
        -------
        None
            Asserts that only private class sync methods are included in the result.
        """
        reflect = ReflectionConcrete(FakeClass)
        private_class_methods = reflect.getPrivateClassSyncMethods()
        self.assertIn('__classMethodPrivate', private_class_methods)
        self.assertNotIn('classSyncMethod', private_class_methods)
        self.assertNotIn('_classMethodProtected', private_class_methods)

    async def testGetPrivateClassAsyncMethods(self):
        """
        Test that ReflectionConcrete.getPrivateClassAsyncMethods returns only private class async methods.

        Returns
        -------
        None
            Asserts that only private class async methods are included in the result.
        """
        reflect = ReflectionConcrete(FakeClass)
        private_class_async_methods = reflect.getPrivateClassAsyncMethods()
        self.assertIn('__classAsyncMethodPrivate', private_class_async_methods)
        self.assertNotIn('classAsyncMethod', private_class_async_methods)
        self.assertNotIn('_classAsyncMethodProtected', private_class_async_methods)

    async def testGetPublicStaticMethods(self):
        """
        Test that ReflectionConcrete.getPublicStaticMethods returns only public static methods.

        Returns
        -------
        None
            Asserts that only public static methods are included in the result.
        """
        reflect = ReflectionConcrete(FakeClass)
        public_static_methods = reflect.getPublicStaticMethods()
        self.assertIn('staticMethod', public_static_methods)
        self.assertIn('staticAsyncMethod', public_static_methods)
        self.assertNotIn('static_async_method', public_static_methods)

    async def testGetPublicStaticSyncMethods(self):
        """
        Test that ReflectionConcrete.getPublicStaticSyncMethods returns only public static sync methods.

        Returns
        -------
        None
            Asserts that only public static sync methods are included in the result.
        """
        reflect = ReflectionConcrete(FakeClass)
        public_static_sync_methods = reflect.getPublicStaticSyncMethods()
        self.assertIn('staticMethod', public_static_sync_methods)
        self.assertNotIn('staticAsyncMethod', public_static_sync_methods)
        self.assertNotIn('static_async_method', public_static_sync_methods)

    async def testGetPublicStaticAsyncMethods(self):
        """
        Test that ReflectionConcrete.getPublicStaticAsyncMethods returns only public static async methods.

        Returns
        -------
        None
            Asserts that only public static async methods are included in the result.
        """
        reflect = ReflectionConcrete(FakeClass)
        public_static_async_methods = reflect.getPublicStaticAsyncMethods()
        self.assertIn('staticAsyncMethod', public_static_async_methods)
        self.assertNotIn('staticMethod', public_static_async_methods)
        self.assertNotIn('static_async_method', public_static_async_methods)

    async def testGetProtectedStaticMethods(self):
        """
        Test that ReflectionConcrete.getProtectedStaticMethods returns only protected static methods.

        Returns
        -------
        None
            Asserts that only protected static methods are included in the result.
        """
        reflect = ReflectionConcrete(FakeClass)
        protected_static_methods = reflect.getProtectedStaticMethods()
        self.assertIn('_staticMethodProtected', protected_static_methods)
        self.assertNotIn('staticMethod', protected_static_methods)
        self.assertNotIn('__staticMethodPrivate', protected_static_methods)

    async def testGetProtectedStaticSyncMethods(self):
        """
        Test that ReflectionConcrete.getProtectedStaticSyncMethods returns only protected static sync methods.

        Returns
        -------
        None
            Asserts that only protected static sync methods are included in the result.
        """
        reflect = ReflectionConcrete(FakeClass)
        protected_static_sync_methods = reflect.getProtectedStaticSyncMethods()
        self.assertIn('_staticMethodProtected', protected_static_sync_methods)
        self.assertNotIn('staticAsyncMethod', protected_static_sync_methods)
        self.assertNotIn('__staticMethodPrivate', protected_static_sync_methods)

    async def testGetProtectedStaticAsyncMethods(self):
        """
        Test that ReflectionConcrete.getProtectedStaticAsyncMethods returns only protected static async methods.

        Returns
        -------
        None
            Asserts that only protected static async methods are included in the result.
        """
        reflect = ReflectionConcrete(FakeClass)
        protected_static_async_methods = reflect.getProtectedStaticAsyncMethods()
        self.assertIn('_staticAsyncMethodProtected', protected_static_async_methods)
        self.assertNotIn('staticMethod', protected_static_async_methods)
        self.assertNotIn('__staticMethodPrivate', protected_static_async_methods)

    async def testGetPrivateStaticMethods(self):
        """
        Test that ReflectionConcrete.getPrivateStaticMethods returns only private static methods.

        Returns
        -------
        None
            Asserts that only private static methods are included in the result.
        """
        reflect = ReflectionConcrete(FakeClass)
        private_static_methods = reflect.getPrivateStaticMethods()
        self.assertIn('__staticMethodPrivate', private_static_methods)
        self.assertNotIn('staticMethod', private_static_methods)
        self.assertNotIn('_staticMethodProtected', private_static_methods)

    async def testGetPrivateStaticSyncMethods(self):
        """
        Test that ReflectionConcrete.getPrivateStaticSyncMethods returns only private static sync methods.

        Returns
        -------
        None
            Asserts that only private static sync methods are included in the result.
        """
        reflect = ReflectionConcrete(FakeClass)
        private_static_sync_methods = reflect.getPrivateStaticSyncMethods()
        self.assertIn('__staticMethodPrivate', private_static_sync_methods)
        self.assertNotIn('staticMethod', private_static_sync_methods)
        self.assertNotIn('_staticMethodProtected', private_static_sync_methods)

    async def testGetPrivateStaticAsyncMethods(self):
        """
        Test that ReflectionConcrete.getPrivateStaticAsyncMethods returns only private static async methods.

        Returns
        -------
        None
            Asserts that only private static async methods are included in the result.
        """
        reflect = ReflectionConcrete(FakeClass)
        private_static_async_methods = reflect.getPrivateStaticAsyncMethods()
        self.assertIn('__staticAsyncMethodPrivate', private_static_async_methods)
        self.assertNotIn('staticAsyncMethod', private_static_async_methods)
        self.assertNotIn('_staticAsyncMethodProtected', private_static_async_methods)

    async def testGetDunderMethods(self):
        """
        Test that ReflectionConcrete.getDunderMethods retrieves dunder (double underscore) methods.

        Returns
        -------
        None
            Asserts that '__init__' is present in the results.
        """
        reflect = ReflectionConcrete(FakeClass)
        dunder_methods = reflect.getDunderMethods()
        self.assertIn('__init__', dunder_methods)

    async def testGetMagicMethods(self):
        """
        Test that ReflectionConcrete.getMagicMethods retrieves magic methods.

        Returns
        -------
        None
            Asserts that '__init__' is present in the results.
        """
        reflect = ReflectionConcrete(FakeClass)
        magic_methods = reflect.getMagicMethods()
        self.assertIn('__init__', magic_methods)

    async def testGetProperties(self):
        """
        Test that ReflectionConcrete.getProperties returns properties of FakeClass.

        Returns
        -------
        None
            Asserts that public, protected, and private properties are present in the result.
        """
        reflect = ReflectionConcrete(FakeClass)
        properties = reflect.getProperties()
        self.assertIn('computed_public_property', properties)
        self.assertIn('_computed_property_protected', properties)
        self.assertIn('__computed_property_private', properties)

    async def testGetPublicProperties(self):
        """
        Test that ReflectionConcrete.getPublicProperties returns only public properties.

        Returns
        -------
        None
            Asserts that only public properties are included in the result.
        """
        reflect = ReflectionConcrete(FakeClass)
        public_properties = reflect.getPublicProperties()
        self.assertIn('computed_public_property', public_properties)
        self.assertNotIn('_computed_property_protected', public_properties)
        self.assertNotIn('__computed_property_private', public_properties)

    async def testGetProtectedProperties(self):
        """
        Test that ReflectionConcrete.getProtectedProperties returns only protected properties.

        Returns
        -------
        None
            Asserts that only protected properties are included in the result.
        """
        reflect = ReflectionConcrete(FakeClass)
        protected_properties = reflect.getProtectedProperties()
        self.assertIn('_computed_property_protected', protected_properties)
        self.assertNotIn('computed_public_property', protected_properties)
        self.assertNotIn('__computed_property_private', protected_properties)

    async def testGetPrivateProperties(self):
        """
        Test that ReflectionConcrete.getPrivateProperties returns only private properties.

        Returns
        -------
        None
            Asserts that only private properties are included in the result.
        """
        reflect = ReflectionConcrete(FakeClass)
        private_properties = reflect.getPrivateProperties()
        self.assertIn('__computed_property_private', private_properties)
        self.assertNotIn('computed_public_property', private_properties)
        self.assertNotIn('_computed_property_protected', private_properties)

    async def testGetProperty(self):
        """
        Test that ReflectionConcrete.getProperty returns the correct value for a property.

        Returns
        -------
        None
            Asserts that the returned value matches the expected value for the property.
        """
        reflect = ReflectionConcrete(FakeClass)
        value = reflect.getProperty('computed_public_property')
        self.assertEqual(value, FakeClass().computed_public_property)

    async def testGetPropertySignature(self):
        """
        Test that ReflectionConcrete.getPropertySignature returns the correct signature for a property.

        Returns
        -------
        None
            Asserts that the returned signature matches the expected format.
        """
        reflect = ReflectionConcrete(FakeClass)
        signature = reflect.getPropertySignature('computed_public_property')
        self.assertEqual(str(signature), '(self) -> str')

    async def testGetPropertyDocstring(self):
        """
        Test that ReflectionConcrete.getPropertyDocstring returns the correct docstring for a property.

        Returns
        -------
        None
            Asserts that the returned docstring matches the expected value.
        """
        reflect = ReflectionConcrete(FakeClass)
        docstring = reflect.getPropertyDocstring('computed_public_property')
        self.assertIn('Returns a string indicating this is a public', docstring)

    async def testGetConstructorDependencies(self):
        """
        Test that ReflectionConcrete.getConstructorDependencies returns the correct constructor dependencies.

        Returns
        -------
        None
            Asserts that the returned dependencies are a ResolveArguments object.
        """
        reflect = ReflectionConcrete(FakeClass)
        dependencies = reflect.getConstructorDependencies()
        self.assertIsInstance(dependencies, ResolveArguments)

    async def testGetMethodDependencies(self):
        """
        Test that ReflectionConcrete.getMethodDependencies returns correct method dependencies.

        Returns
        -------
        None
            Asserts that the returned dependencies for 'instanceSyncMethod' are as expected.
        """
        reflect = ReflectionConcrete(FakeClass)
        method_deps: ResolveArguments = reflect.getMethodDependencies('instanceSyncMethod')
        self.assertIn('x', method_deps.unresolved)
        self.assertIn('y', method_deps.unresolved)
