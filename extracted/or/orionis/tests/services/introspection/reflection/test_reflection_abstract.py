from orionis.services.introspection.abstract.reflection import ReflectionAbstract
from orionis.services.introspection.dependencies.entities.class_dependencies import ClassDependency
from tests.services.introspection.reflection.mock.fake_reflect_instance import AbstractFakeClass
from orionis.test.cases.asynchronous import AsyncTestCase

class TestServiceReflectionAbstract(AsyncTestCase):

    async def testGetClass(self):
        """
        Verifies that getClass returns the correct class.
        """
        reflect = ReflectionAbstract(AbstractFakeClass)
        cls = reflect.getClass()
        self.assertEqual(cls, AbstractFakeClass)

    async def testGetClassName(self):
        """
        Verifies that getClassName returns the class name.
        """
        reflect = ReflectionAbstract(AbstractFakeClass)
        class_name = reflect.getClassName()
        self.assertEqual(class_name, 'AbstractFakeClass')

    async def testGetModuleName(self):
        """
        Verifies that getModuleName returns the module name.
        """
        reflect = ReflectionAbstract(AbstractFakeClass)
        module_name = reflect.getModuleName()
        self.assertEqual(module_name, 'tests.services.introspection.reflection.mock.fake_reflect_instance')

    async def testGetModuleWithClassName(self):
        """
        Verifies that getModuleWithClassName returns the module and class name.
        """
        reflect = ReflectionAbstract(AbstractFakeClass)
        module_with_class_name = reflect.getModuleWithClassName()
        self.assertEqual(module_with_class_name, 'tests.services.introspection.reflection.mock.fake_reflect_instance.AbstractFakeClass')

    async def testGetDocstring(self):
        """
        Verifies that getDocstring returns the class docstring.
        """
        reflect = ReflectionAbstract(AbstractFakeClass)
        docstring = reflect.getDocstring()
        self.assertEqual(docstring, AbstractFakeClass.__doc__)

    async def testGetBaseClasses(self):
        """
        Verifies that getBaseClasses returns the base classes.
        """
        reflect = ReflectionAbstract(AbstractFakeClass)
        base_classes = reflect.getBaseClasses()
        self.assertIn(AbstractFakeClass.__base__, base_classes)

    async def testGetSourceCode(self):
        """
        Verifies that getSourceCode returns the class source code.
        """
        reflect = ReflectionAbstract(AbstractFakeClass)
        source_code = reflect.getSourceCode()
        self.assertTrue(source_code.startswith('class AbstractFakeClass'))

    async def testGetFile(self):
        """
        Verifies that getFile returns the class file path.
        """
        reflect = ReflectionAbstract(AbstractFakeClass)
        file_path = reflect.getFile()
        self.assertTrue(file_path.endswith('fake_reflect_instance.py'))

    async def testGetAnnotations(self):
        """
        Verifies that getAnnotations returns the class annotations.
        """
        reflect = ReflectionAbstract(AbstractFakeClass)
        annotations = reflect.getAnnotations()
        self.assertIn('public_attr', annotations)

    async def testHasAttribute(self):
        """
        Verifies that hasAttribute identifies existing attributes.
        """
        reflect = ReflectionAbstract(AbstractFakeClass)
        self.assertTrue(reflect.hasAttribute('public_attr'))
        self.assertFalse(reflect.hasAttribute('non_existent_attr'))

    async def testGetAttribute(self):
        """
        Verifies that getAttribute gets the correct value of an attribute.
        """
        reflect = ReflectionAbstract(AbstractFakeClass)
        self.assertEqual(reflect.getAttribute('public_attr'), 42)
        self.assertIsNone(reflect.getAttribute('non_existent_attr'))

    async def testSetAttribute(self):
        """
        Verifies that setAttribute modifies attributes correctly.
        """
        reflect = ReflectionAbstract(AbstractFakeClass)
        self.assertTrue(reflect.setAttribute('name', 'Orionis Framework'))
        self.assertEqual(reflect.getAttribute('name'), 'Orionis Framework')
        self.assertTrue(reflect.setAttribute('_version', '1.x'))
        self.assertEqual(reflect.getAttribute('_version'), '1.x')
        self.assertTrue(reflect.setAttribute('__python', '3.13+'))
        self.assertEqual(reflect.getAttribute('__python'), '3.13+')

    async def testRemoveAttribute(self):
        """
        Verifies that removeAttribute removes attributes correctly.
        """
        reflect = ReflectionAbstract(AbstractFakeClass)
        reflect.setAttribute('new_attr', 100)
        self.assertTrue(reflect.removeAttribute('new_attr'))
        self.assertFalse(reflect.hasAttribute('new_attr'))

    async def testGetAttributes(self):
        """
        Verifies that getAttributes returns all attributes.
        """
        reflect = ReflectionAbstract(AbstractFakeClass)
        attributes = reflect.getAttributes()
        self.assertIn('public_attr', attributes)
        self.assertIn('_protected_attr', attributes)
        self.assertIn('__private_attr', attributes)

    async def testGetPublicAttributes(self):
        """
        Verifies that getPublicAttributes returns only public attributes.
        """
        reflect = ReflectionAbstract(AbstractFakeClass)
        public_attributes = reflect.getPublicAttributes()
        self.assertIn('public_attr', public_attributes)
        self.assertNotIn('_protected_attr', public_attributes)
        self.assertNotIn('__private_attr', public_attributes)

    async def testGetProtectedAttributes(self):
        """
        Verifies that getProtectedAttributes returns only protected attributes.
        """
        reflect = ReflectionAbstract(AbstractFakeClass)
        protected_attributes = reflect.getProtectedAttributes()
        self.assertIn('_protected_attr', protected_attributes)
        self.assertNotIn('public_attr', protected_attributes)
        self.assertNotIn('__private_attr', protected_attributes)

    async def testGetPrivateAttributes(self):
        """
        Verifies that getPrivateAttributes returns only private attributes.
        """
        reflect = ReflectionAbstract(AbstractFakeClass)
        private_attributes = reflect.getPrivateAttributes()
        self.assertIn('__private_attr', private_attributes)
        self.assertNotIn('public_attr', private_attributes)
        self.assertNotIn('_protected_attr', private_attributes)

    async def testGetDunderAttributes(self):
        """
        Verifies that getDunderAttributes returns dunder attributes.
        """
        reflect = ReflectionAbstract(AbstractFakeClass)
        dunder_attributes = reflect.getDunderAttributes()
        self.assertIn('__dd__', dunder_attributes)

    async def testGetMagicAttributes(self):
        """
        Verifies that getMagicAttributes returns magic attributes.
        """
        reflect = ReflectionAbstract(AbstractFakeClass)
        magic_attributes = reflect.getMagicAttributes()
        self.assertIn('__dd__', magic_attributes)

    async def testHasMethod(self):
        """
        Verifies that hasMethod identifies existing methods.
        """
        reflect = ReflectionAbstract(AbstractFakeClass)
        self.assertTrue(reflect.hasMethod('instanceSyncMethod'))
        self.assertFalse(reflect.hasMethod('non_existent_method'))

    async def testCallMethod(self):
        """
        Verifies that callMethod executes methods correctly.
        """
        # No aplica para ReflectionAbstract, se omite

    async def testCallAsyncMethod(self):
        """
        Verifies that callMethod executes async methods correctly.
        """
        # No aplica para ReflectionAbstract, se omite

    async def testSetMethod(self):
        """
        Verifies that setMethod assigns methods correctly.
        """
        # No aplica para ReflectionAbstract, se omite

    async def testRemoveMethod(self):
        """
        Verifies that removeMethod removes methods correctly.
        """
        # No aplica para ReflectionAbstract, se omite

    async def testGetMethodSignature(self):
        """
        Verifies that getMethodSignature returns the method signature.
        """
        reflect = ReflectionAbstract(AbstractFakeClass)
        signature = reflect.getMethodSignature('instanceSyncMethod')
        self.assertEqual(str(signature), '(self, x: int, y: int) -> int')

    async def testGetMethods(self):
        """
        Verifies that getMethods returns the class methods.
        """
        reflect = ReflectionAbstract(AbstractFakeClass)
        methods = reflect.getMethods()
        self.assertIn('instanceSyncMethod', methods)
        self.assertIn('instanceAsyncMethod', methods)

    async def testGetPublicMethods(self):
        """
        Verifies that getPublicMethods returns only public methods.
        """
        reflect = ReflectionAbstract(AbstractFakeClass)
        public_methods = reflect.getPublicMethods()
        self.assertIn('instanceSyncMethod', public_methods)
        self.assertNotIn('_protected_method', public_methods)
        self.assertNotIn('__private_method', public_methods)

    async def testGetPublicSyncMethods(self):
        """
        Verifies that getPublicSyncMethods returns only public sync methods.
        """
        reflect = ReflectionAbstract(AbstractFakeClass)
        public_sync_methods = reflect.getPublicSyncMethods()
        self.assertIn('instanceSyncMethod', public_sync_methods)
        self.assertNotIn('_protected_method', public_sync_methods)
        self.assertNotIn('__private_method', public_sync_methods)

    async def testGetPublicAsyncMethods(self):
        """
        Verifies that getPublicAsyncMethods returns only public async methods.
        """
        reflect = ReflectionAbstract(AbstractFakeClass)
        public_async_methods = reflect.getPublicAsyncMethods()
        self.assertIn('instanceAsyncMethod', public_async_methods)
        self.assertNotIn('_protected_async_method', public_async_methods)
        self.assertNotIn('__private_async_method', public_async_methods)

    async def testGetProtectedMethods(self):
        """
        Verifies that getProtectedMethods returns only protected methods.
        """
        reflect = ReflectionAbstract(AbstractFakeClass)
        protected_methods = reflect.getProtectedMethods()
        self.assertIn('_protectedAsyncMethod', protected_methods)
        self.assertNotIn('instanceSyncMethod', protected_methods)
        self.assertNotIn('__privateSyncMethod', protected_methods)

    async def testGetProtectedSyncMethods(self):
        """
        Verifies that getProtectedSyncMethods returns only protected sync methods.
        """
        reflect = ReflectionAbstract(AbstractFakeClass)
        protected_sync_methods = reflect.getProtectedSyncMethods()
        self.assertIn('_protectedsyncMethod', protected_sync_methods)
        self.assertNotIn('instanceAsyncMethod', protected_sync_methods)
        self.assertNotIn('__privateSyncMethod', protected_sync_methods)

    async def testGetProtectedAsyncMethods(self):
        """
        Verifies that getProtectedAsyncMethods returns only protected async methods.
        """
        reflect = ReflectionAbstract(AbstractFakeClass)
        protected_async_methods = reflect.getProtectedAsyncMethods()
        self.assertIn('_protectedAsyncMethod', protected_async_methods)
        self.assertNotIn('instanceSyncMethod', protected_async_methods)
        self.assertNotIn('__privateSyncMethod', protected_async_methods)

    async def testGetPrivateMethods(self):
        """
        Verifies that getPrivateMethods returns only private methods.
        """
        reflect = ReflectionAbstract(AbstractFakeClass)
        private_methods = reflect.getPrivateMethods()
        self.assertIn('__privateSyncMethod', private_methods)
        self.assertNotIn('instanceSyncMethod', private_methods)
        self.assertNotIn('_protectedAsyncMethod', private_methods)

    async def testGetPrivateSyncMethods(self):
        """
        Verifies that getPrivateSyncMethods returns only private sync methods.
        """
        reflect = ReflectionAbstract(AbstractFakeClass)
        private_sync_methods = reflect.getPrivateSyncMethods()
        self.assertIn('__privateSyncMethod', private_sync_methods)
        self.assertNotIn('instanceAsyncMethod', private_sync_methods)
        self.assertNotIn('_protectedAsyncMethod', private_sync_methods)

    async def testGetPrivateAsyncMethods(self):
        """
        Verifies that getPrivateAsyncMethods returns only private async methods.
        """
        reflect = ReflectionAbstract(AbstractFakeClass)
        private_async_methods = reflect.getPrivateAsyncMethods()
        self.assertIn('__privateAsyncMethod', private_async_methods)
        self.assertNotIn('instanceSyncMethod', private_async_methods)
        self.assertNotIn('_protectedAsyncMethod', private_async_methods)

    async def testGetPublicClassMethods(self):
        """
        Verifies that getPublicClassMethods returns only public class methods.
        """
        reflect = ReflectionAbstract(AbstractFakeClass)
        public_class_methods = reflect.getPublicClassMethods()
        self.assertIn('classSyncMethod', public_class_methods)
        self.assertNotIn('_protected_class_method', public_class_methods)
        self.assertNotIn('__private_class_method', public_class_methods)

    async def testGetPublicClassSyncMethods(self):
        """
        Verifies that getPublicClassSyncMethods returns only public class sync methods.
        """
        reflect = ReflectionAbstract(AbstractFakeClass)
        public_class_sync_methods = reflect.getPublicClassSyncMethods()
        self.assertIn('classSyncMethod', public_class_sync_methods)
        self.assertNotIn('_protected_class_method', public_class_sync_methods)
        self.assertNotIn('__private_class_method', public_class_sync_methods)

    async def testGetPublicClassAsyncMethods(self):
        """
        Verifies that getPublicClassAsyncMethods returns only public class async methods.
        """
        reflect = ReflectionAbstract(AbstractFakeClass)
        public_class_async_methods = reflect.getPublicClassAsyncMethods()
        self.assertIn('classAsyncMethod', public_class_async_methods)
        self.assertNotIn('_protected_class_async_method', public_class_async_methods)
        self.assertNotIn('__private_class_async_method', public_class_async_methods)

    async def testGetProtectedClassMethods(self):
        """
        Verifies that getProtectedClassMethods returns only protected class methods.
        """
        reflect = ReflectionAbstract(AbstractFakeClass)
        protected_class_methods = reflect.getProtectedClassMethods()
        self.assertIn('_classMethodProtected', protected_class_methods)
        self.assertNotIn('classSyncMethod', protected_class_methods)
        self.assertNotIn('__classMethodPrivate', protected_class_methods)

    async def testGetProtectedClassSyncMethods(self):
        """
        Verifies that getProtectedClassSyncMethods returns only protected class sync methods.
        """
        reflect = ReflectionAbstract(AbstractFakeClass)
        protected_class_sync_methods = reflect.getProtectedClassSyncMethods()
        self.assertIn('_classMethodProtected', protected_class_sync_methods)
        self.assertNotIn('classSyncMethod', protected_class_sync_methods)
        self.assertNotIn('__classSyncMethodPrivate', protected_class_sync_methods)

    async def testGetProtectedClassAsyncMethods(self):
        """
        Verifies that getProtectedClassAsyncMethods returns only protected class async methods.
        """
        reflect = ReflectionAbstract(AbstractFakeClass)
        protected_class_async_methods = reflect.getProtectedClassAsyncMethods()
        self.assertIn('_classAsyncMethodProtected', protected_class_async_methods)
        self.assertNotIn('classAsyncMethod', protected_class_async_methods)
        self.assertNotIn('__classAsyncMethodPrivate', protected_class_async_methods)

    async def testGetPrivateClassMethods(self):
        """
        Verifies that getPrivateClassMethods returns only private class methods.
        """
        reflect = ReflectionAbstract(AbstractFakeClass)
        private_class_methods = reflect.getPrivateClassMethods()
        self.assertIn('__classMethodPrivate', private_class_methods)
        self.assertNotIn('classSyncMethod', private_class_methods)
        self.assertNotIn('_classMethodProtected', private_class_methods)

    async def testGetPrivateClassSyncMethods(self):
        """
        Verifies that getPrivateClassSyncMethods returns only private class sync methods.
        """
        reflect = ReflectionAbstract(AbstractFakeClass)
        private_class_methods = reflect.getPrivateClassSyncMethods()
        self.assertIn('__classMethodPrivate', private_class_methods)
        self.assertNotIn('classSyncMethod', private_class_methods)
        self.assertNotIn('_classMethodProtected', private_class_methods)

    async def testGetPrivateClassAsyncMethods(self):
        """
        Verifies that getPrivateClassAsyncMethods returns only private class async methods.
        """
        reflect = ReflectionAbstract(AbstractFakeClass)
        private_class_async_methods = reflect.getPrivateClassAsyncMethods()
        self.assertIn('__classAsyncMethodPrivate', private_class_async_methods)
        self.assertNotIn('classAsyncMethod', private_class_async_methods)
        self.assertNotIn('_classAsyncMethodProtected', private_class_async_methods)

    async def testGetPublicStaticMethods(self):
        """
        Verifies that getPublicStaticMethods returns only public static methods.
        """
        reflect = ReflectionAbstract(AbstractFakeClass)
        public_static_methods = reflect.getPublicStaticMethods()
        self.assertIn('staticMethod', public_static_methods)
        self.assertIn('staticAsyncMethod', public_static_methods)
        self.assertNotIn('static_async_method', public_static_methods)

    async def testGetPublicStaticSyncMethods(self):
        """
        Verifies that getPublicStaticSyncMethods returns only public static sync methods.
        """
        reflect = ReflectionAbstract(AbstractFakeClass)
        public_static_sync_methods = reflect.getPublicStaticSyncMethods()
        self.assertIn('staticMethod', public_static_sync_methods)
        self.assertNotIn('staticAsyncMethod', public_static_sync_methods)
        self.assertNotIn('static_async_method', public_static_sync_methods)

    async def testGetPublicStaticAsyncMethods(self):
        """
        Verifies that getPublicStaticAsyncMethods returns only public static async methods.
        """
        reflect = ReflectionAbstract(AbstractFakeClass)
        public_static_async_methods = reflect.getPublicStaticAsyncMethods()
        self.assertIn('staticAsyncMethod', public_static_async_methods)
        self.assertNotIn('staticMethod', public_static_async_methods)
        self.assertNotIn('static_async_method', public_static_async_methods)

    async def testGetProtectedStaticMethods(self):
        """
        Verifies that getProtectedStaticMethods returns only protected static methods.
        """
        reflect = ReflectionAbstract(AbstractFakeClass)
        protected_static_methods = reflect.getProtectedStaticMethods()
        self.assertIn('_staticMethodProtected', protected_static_methods)
        self.assertNotIn('staticMethod', protected_static_methods)
        self.assertNotIn('__staticMethodPrivate', protected_static_methods)

    async def testGetProtectedStaticSyncMethods(self):
        """
        Verifies that getProtectedStaticSyncMethods returns only protected static sync methods.
        """
        reflect = ReflectionAbstract(AbstractFakeClass)
        protected_static_sync_methods = reflect.getProtectedStaticSyncMethods()
        self.assertIn('_staticMethodProtected', protected_static_sync_methods)
        self.assertNotIn('staticAsyncMethod', protected_static_sync_methods)
        self.assertNotIn('__staticMethodPrivate', protected_static_sync_methods)

    async def testGetProtectedStaticAsyncMethods(self):
        """
        Verifies that getProtectedStaticAsyncMethods returns only protected static async methods.
        """
        reflect = ReflectionAbstract(AbstractFakeClass)
        protected_static_async_methods = reflect.getProtectedStaticAsyncMethods()
        self.assertIn('_staticAsyncMethodProtected', protected_static_async_methods)
        self.assertNotIn('staticMethod', protected_static_async_methods)
        self.assertNotIn('__staticMethodPrivate', protected_static_async_methods)

    async def testGetPrivateStaticMethods(self):
        """
        Verifies that getPrivateStaticMethods returns only private static methods.
        """
        reflect = ReflectionAbstract(AbstractFakeClass)
        private_static_methods = reflect.getPrivateStaticMethods()
        self.assertIn('__staticMethodPrivate', private_static_methods)
        self.assertNotIn('staticMethod', private_static_methods)
        self.assertNotIn('_staticMethodProtected', private_static_methods)

    async def testGetPrivateStaticSyncMethods(self):
        """
        Verifies that getPrivateStaticSyncMethods returns only private static sync methods.
        """
        reflect = ReflectionAbstract(AbstractFakeClass)
        private_static_sync_methods = reflect.getPrivateStaticSyncMethods()
        self.assertIn('__staticMethodPrivate', private_static_sync_methods)
        self.assertNotIn('staticMethod', private_static_sync_methods)
        self.assertNotIn('_staticMethodProtected', private_static_sync_methods)

    async def testGetPrivateStaticAsyncMethods(self):
        """
        Verifies that getPrivateStaticAsyncMethods returns only private static async methods.
        """
        reflect = ReflectionAbstract(AbstractFakeClass)
        private_static_async_methods = reflect.getPrivateStaticAsyncMethods()
        self.assertIn('__staticAsyncMethodPrivate', private_static_async_methods)
        self.assertNotIn('staticAsyncMethod', private_static_async_methods)
        self.assertNotIn('_staticAsyncMethodProtected', private_static_async_methods)

    async def testGetDunderMethods(self):
        """
        Verifies that getDunderMethods returns dunder methods.
        """
        reflect = ReflectionAbstract(AbstractFakeClass)
        dunder_methods = reflect.getDunderMethods()
        self.assertIn('__init__', dunder_methods)

    async def testGetMagicMethods(self):
        """
        Verifies that getMagicMethods returns magic methods.
        """
        reflect = ReflectionAbstract(AbstractFakeClass)
        magic_methods = reflect.getMagicMethods()
        self.assertIn('__init__', magic_methods)

    async def testGetProperties(self):
        """
        Verifies that getProperties returns the class properties.
        """
        reflect = ReflectionAbstract(AbstractFakeClass)
        properties = reflect.getProperties()
        self.assertIn('computed_public_property', properties)
        self.assertIn('_computed_property_protected', properties)
        self.assertIn('__computed_property_private', properties)

    async def testGetPublicProperties(self):
        """
        Verifies that getPublicProperties returns only public properties.
        """
        reflect = ReflectionAbstract(AbstractFakeClass)
        public_properties = reflect.getPublicProperties()
        self.assertIn('computed_public_property', public_properties)
        self.assertNotIn('_computed_property_protected', public_properties)
        self.assertNotIn('__computed_property_private', public_properties)

    async def testGetProtectedProperties(self):
        """
        Verifies that getProtectedProperties returns only protected properties.
        """
        reflect = ReflectionAbstract(AbstractFakeClass)
        protected_properties = reflect.getProtectedProperties()
        self.assertIn('_computed_property_protected', protected_properties)
        self.assertNotIn('computed_public_property', protected_properties)
        self.assertNotIn('__computed_property_private', protected_properties)

    async def testGetPrivateProperties(self):
        """
        Verifies that getPrivateProperties returns only private properties.
        """
        reflect = ReflectionAbstract(AbstractFakeClass)
        private_properties = reflect.getPrivateProperties()
        self.assertIn('__computed_property_private', private_properties)
        self.assertNotIn('computed_public_property', private_properties)
        self.assertNotIn('_computed_property_protected', private_properties)

    async def testGetPropertySignature(self):
        """
        Verifies that getPropertySignature returns the property signature.
        """
        reflect = ReflectionAbstract(AbstractFakeClass)
        signature = reflect.getPropertySignature('computed_public_property')
        self.assertEqual(str(signature), '(self) -> str')

    async def testGetPropertyDocstring(self):
        """
        Verifies that getPropertyDocstring returns the property docstring.
        """
        reflect = ReflectionAbstract(AbstractFakeClass)
        docstring = reflect.getPropertyDocstring('computed_public_property')
        self.assertIn('Computes and returns the valu', docstring)

    async def testGetConstructorDependencies(self):
        """
        Verifies that getConstructorDependencies returns the constructor dependencies.
        """
        reflect = ReflectionAbstract(AbstractFakeClass)
        dependencies = reflect.getConstructorDependencies()
        self.assertIsInstance(dependencies, ClassDependency)

    async def testGetMethodDependencies(self):
        """
        Verifies that getMethodDependencies returns the method dependencies.
        """
        reflect = ReflectionAbstract(AbstractFakeClass)
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
