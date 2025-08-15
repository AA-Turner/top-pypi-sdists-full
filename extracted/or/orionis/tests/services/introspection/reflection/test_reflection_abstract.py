from orionis.services.introspection.abstract.reflection import ReflectionAbstract
from orionis.services.introspection.dependencies.entities.argument import Argument
from orionis.services.introspection.dependencies.entities.resolve_argument import ResolveArguments
from tests.services.introspection.reflection.mock.fake_reflect_instance import AbstractFakeClass
from orionis.test.cases.asynchronous import AsyncTestCase

class TestServiceReflectionAbstract(AsyncTestCase):

    async def testGetClass(self):
        """
        Test the getClass method of ReflectionAbstract.

        Verifies that the getClass method correctly returns the class object
        that was passed during ReflectionAbstract instantiation.

        Assertions
        ----------
        The returned class object should be identical to the original class.
        """
        reflect = ReflectionAbstract(AbstractFakeClass)
        cls = reflect.getClass()
        self.assertEqual(cls, AbstractFakeClass)

    async def testGetClassName(self):
        """
        Test the getClassName method of ReflectionAbstract.

        Verifies that the getClassName method correctly returns the name
        of the class as a string.

        Assertions
        ----------
        The returned string should match the actual class name.
        """
        reflect = ReflectionAbstract(AbstractFakeClass)
        class_name = reflect.getClassName()
        self.assertEqual(class_name, 'AbstractFakeClass')

    async def testGetModuleName(self):
        """
        Test the getModuleName method of ReflectionAbstract.

        Verifies that the getModuleName method correctly returns the fully
        qualified module name where the class is defined.

        Assertions
        ----------
        The returned string should match the complete module path.
        """
        reflect = ReflectionAbstract(AbstractFakeClass)
        module_name = reflect.getModuleName()
        self.assertEqual(module_name, 'tests.services.introspection.reflection.mock.fake_reflect_instance')

    async def testGetModuleWithClassName(self):
        """
        Test the getModuleWithClassName method of ReflectionAbstract.

        Verifies that the getModuleWithClassName method correctly returns
        the fully qualified name combining module path and class name.

        Assertions
        ----------
        The returned string should contain the complete module path followed
        by the class name, separated by a dot.
        """
        reflect = ReflectionAbstract(AbstractFakeClass)
        module_with_class_name = reflect.getModuleWithClassName()
        self.assertEqual(module_with_class_name, 'tests.services.introspection.reflection.mock.fake_reflect_instance.AbstractFakeClass')

    async def testGetDocstring(self):
        """
        Test the getDocstring method of ReflectionAbstract.

        Verifies that the getDocstring method correctly returns the class
        docstring as it appears in the class definition.

        Assertions
        ----------
        The returned docstring should be identical to the class's __doc__ attribute.
        """
        reflect = ReflectionAbstract(AbstractFakeClass)
        docstring = reflect.getDocstring()
        self.assertEqual(docstring, AbstractFakeClass.__doc__)

    async def testGetBaseClasses(self):
        """
        Test the getBaseClasses method of ReflectionAbstract.

        Verifies that the getBaseClasses method correctly returns a collection
        of base classes that the reflected class inherits from.

        Assertions
        ----------
        The returned collection should contain the class's base class.
        """
        reflect = ReflectionAbstract(AbstractFakeClass)
        base_classes = reflect.getBaseClasses()
        self.assertIn(AbstractFakeClass.__base__, base_classes)

    async def testGetSourceCode(self):
        """
        Test the getSourceCode method of ReflectionAbstract.

        Verifies that the getSourceCode method correctly returns the source
        code of the class as a string.

        Assertions
        ----------
        The returned source code should start with the class definition.
        """
        reflect = ReflectionAbstract(AbstractFakeClass)
        source_code = reflect.getSourceCode()
        self.assertTrue(source_code.startswith('class AbstractFakeClass'))

    async def testGetFile(self):
        """
        Test the getFile method of ReflectionAbstract.

        Verifies that the getFile method correctly returns the file path
        where the class is defined.

        Assertions
        ----------
        The returned file path should end with the expected filename.
        """
        reflect = ReflectionAbstract(AbstractFakeClass)
        file_path = reflect.getFile()
        self.assertTrue(file_path.endswith('fake_reflect_instance.py'))

    async def testGetAnnotations(self):
        """
        Test the getAnnotations method of ReflectionAbstract.

        Verifies that the getAnnotations method correctly returns the type
        annotations defined in the class.

        Assertions
        ----------
        The returned annotations should contain the expected annotated attribute.
        """
        reflect = ReflectionAbstract(AbstractFakeClass)
        annotations = reflect.getAnnotations()
        self.assertIn('public_attr', annotations)

    async def testHasAttribute(self):
        """
        Test the hasAttribute method of ReflectionAbstract.

        Verifies that the hasAttribute method correctly identifies whether
        a specific attribute exists in the class.

        Assertions
        ----------
        Should return True for existing attributes and False for non-existent ones.
        """
        reflect = ReflectionAbstract(AbstractFakeClass)
        self.assertTrue(reflect.hasAttribute('public_attr'))
        self.assertFalse(reflect.hasAttribute('non_existent_attr'))

    async def testGetAttribute(self):
        """
        Test the getAttribute method of ReflectionAbstract.

        Verifies that the getAttribute method correctly retrieves the value
        of existing attributes and returns None for non-existent ones.

        Assertions
        ----------
        Should return the correct value for existing attributes and None
        for non-existent attributes.
        """
        reflect = ReflectionAbstract(AbstractFakeClass)
        self.assertEqual(reflect.getAttribute('public_attr'), 42)
        self.assertIsNone(reflect.getAttribute('non_existent_attr'))

    async def testSetAttribute(self):
        """
        Test the setAttribute method of ReflectionAbstract.

        Verifies that the setAttribute method correctly assigns values to
        attributes, including public, protected, and private attributes.

        Assertions
        ----------
        Should successfully set attributes with different visibility levels
        and confirm the values are correctly assigned.
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
        Test the removeAttribute method of ReflectionAbstract.

        Verifies that the removeAttribute method correctly removes attributes
        from the class and returns the appropriate boolean result.

        Assertions
        ----------
        Should successfully remove existing attributes and return True,
        then confirm the attribute no longer exists.
        """
        reflect = ReflectionAbstract(AbstractFakeClass)
        reflect.setAttribute('new_attr', 100)
        self.assertTrue(reflect.removeAttribute('new_attr'))
        self.assertFalse(reflect.hasAttribute('new_attr'))

    async def testGetAttributes(self):
        """
        Test the getAttributes method of ReflectionAbstract.

        Verifies that the getAttributes method correctly returns all attributes
        from the class, regardless of their visibility level.

        Assertions
        ----------
        The returned collection should contain public, protected, and private attributes.
        """
        reflect = ReflectionAbstract(AbstractFakeClass)
        attributes = reflect.getAttributes()
        self.assertIn('public_attr', attributes)
        self.assertIn('_protected_attr', attributes)
        self.assertIn('__private_attr', attributes)

    async def testGetPublicAttributes(self):
        """
        Test the getPublicAttributes method of ReflectionAbstract.

        Verifies that the getPublicAttributes method correctly returns only
        attributes with public visibility (no leading underscore).

        Assertions
        ----------
        Should include public attributes and exclude protected and private attributes.
        """
        reflect = ReflectionAbstract(AbstractFakeClass)
        public_attributes = reflect.getPublicAttributes()
        self.assertIn('public_attr', public_attributes)
        self.assertNotIn('_protected_attr', public_attributes)
        self.assertNotIn('__private_attr', public_attributes)

    async def testGetProtectedAttributes(self):
        """
        Test the getProtectedAttributes method of ReflectionAbstract.

        Verifies that the getProtectedAttributes method correctly returns only
        attributes with protected visibility (single leading underscore).

        Assertions
        ----------
        Should include protected attributes and exclude public and private attributes.
        """
        reflect = ReflectionAbstract(AbstractFakeClass)
        protected_attributes = reflect.getProtectedAttributes()
        self.assertIn('_protected_attr', protected_attributes)
        self.assertNotIn('public_attr', protected_attributes)
        self.assertNotIn('__private_attr', protected_attributes)

    async def testGetPrivateAttributes(self):
        """
        Test the getPrivateAttributes method of ReflectionAbstract.

        Verifies that the getPrivateAttributes method correctly returns only
        attributes with private visibility (double leading underscore).

        Assertions
        ----------
        Should include private attributes and exclude public and protected attributes.
        """
        reflect = ReflectionAbstract(AbstractFakeClass)
        private_attributes = reflect.getPrivateAttributes()
        self.assertIn('__private_attr', private_attributes)
        self.assertNotIn('public_attr', private_attributes)
        self.assertNotIn('_protected_attr', private_attributes)

    async def testGetDunderAttributes(self):
        """
        Test the getDunderAttributes method of ReflectionAbstract.

        Verifies that the getDunderAttributes method correctly returns attributes
        that follow the dunder (double underscore) naming convention.

        Assertions
        ----------
        Should include attributes with double underscores at both ends.
        """
        reflect = ReflectionAbstract(AbstractFakeClass)
        dunder_attributes = reflect.getDunderAttributes()
        self.assertIn('__dd__', dunder_attributes)

    async def testGetMagicAttributes(self):
        """
        Test the getMagicAttributes method of ReflectionAbstract.

        Verifies that the getMagicAttributes method correctly returns attributes
        that are considered magic methods or special attributes in Python.

        Assertions
        ----------
        Should include magic attributes like dunder attributes.
        """
        reflect = ReflectionAbstract(AbstractFakeClass)
        magic_attributes = reflect.getMagicAttributes()
        self.assertIn('__dd__', magic_attributes)

    async def testHasMethod(self):
        """
        Test the hasMethod method of ReflectionAbstract.

        Verifies that the hasMethod method correctly identifies whether
        a specific method exists in the class.

        Assertions
        ----------
        Should return True for existing methods and False for non-existent ones.
        """
        reflect = ReflectionAbstract(AbstractFakeClass)
        self.assertTrue(reflect.hasMethod('instanceSyncMethod'))
        self.assertFalse(reflect.hasMethod('non_existent_method'))

    async def testGetMethodSignature(self):
        """
        Test the getMethodSignature method of ReflectionAbstract.

        Verifies that the getMethodSignature method correctly returns the
        method signature including parameters and return type annotations.

        Assertions
        ----------
        The returned signature should match the expected method signature format.
        """
        reflect = ReflectionAbstract(AbstractFakeClass)
        signature = reflect.getMethodSignature('instanceSyncMethod')
        self.assertEqual(str(signature), '(self, x: int, y: int) -> int')

    async def testGetMethods(self):
        """
        Test the getMethods method of ReflectionAbstract.

        Verifies that the getMethods method correctly returns all methods
        defined in the class, regardless of their visibility level.

        Assertions
        ----------
        The returned collection should contain the expected class methods.
        """
        reflect = ReflectionAbstract(AbstractFakeClass)
        methods = reflect.getMethods()
        self.assertIn('instanceSyncMethod', methods)
        self.assertIn('instanceAsyncMethod', methods)

    async def testGetPublicMethods(self):
        """
        Test the getPublicMethods method of ReflectionAbstract.

        Verifies that the getPublicMethods method correctly returns only
        methods with public visibility (no leading underscore).

        Assertions
        ----------
        Should include public methods and exclude protected and private methods.
        """
        reflect = ReflectionAbstract(AbstractFakeClass)
        public_methods = reflect.getPublicMethods()
        self.assertIn('instanceSyncMethod', public_methods)
        self.assertNotIn('_protected_method', public_methods)
        self.assertNotIn('__private_method', public_methods)

    async def testGetPublicSyncMethods(self):
        """
        Test the getPublicSyncMethods method of ReflectionAbstract.

        Verifies that the getPublicSyncMethods method correctly returns only
        synchronous methods with public visibility.

        Assertions
        ----------
        Should include public sync methods and exclude async, protected, and private methods.
        """
        reflect = ReflectionAbstract(AbstractFakeClass)
        public_sync_methods = reflect.getPublicSyncMethods()
        self.assertIn('instanceSyncMethod', public_sync_methods)
        self.assertNotIn('_protected_method', public_sync_methods)
        self.assertNotIn('__private_method', public_sync_methods)

    async def testGetPublicAsyncMethods(self):
        """
        Test the getPublicAsyncMethods method of ReflectionAbstract.

        Verifies that the getPublicAsyncMethods method correctly returns only
        asynchronous methods with public visibility.

        Assertions
        ----------
        Should include public async methods and exclude sync, protected, and private methods.
        """
        reflect = ReflectionAbstract(AbstractFakeClass)
        public_async_methods = reflect.getPublicAsyncMethods()
        self.assertIn('instanceAsyncMethod', public_async_methods)
        self.assertNotIn('_protected_async_method', public_async_methods)
        self.assertNotIn('__private_async_method', public_async_methods)

    async def testGetProtectedMethods(self):
        """
        Test the getProtectedMethods method of ReflectionAbstract.

        Verifies that the getProtectedMethods method correctly returns only
        methods with protected visibility (single leading underscore).

        Assertions
        ----------
        Should include protected methods and exclude public and private methods.
        """
        reflect = ReflectionAbstract(AbstractFakeClass)
        protected_methods = reflect.getProtectedMethods()
        self.assertIn('_protectedAsyncMethod', protected_methods)
        self.assertNotIn('instanceSyncMethod', protected_methods)
        self.assertNotIn('__privateSyncMethod', protected_methods)

    async def testGetProtectedSyncMethods(self):
        """
        Test the getProtectedSyncMethods method of ReflectionAbstract.

        Verifies that the getProtectedSyncMethods method correctly returns only
        synchronous methods with protected visibility.

        Assertions
        ----------
        Should include protected sync methods and exclude async, public, and private methods.
        """
        reflect = ReflectionAbstract(AbstractFakeClass)
        protected_sync_methods = reflect.getProtectedSyncMethods()
        self.assertIn('_protectedsyncMethod', protected_sync_methods)
        self.assertNotIn('instanceAsyncMethod', protected_sync_methods)
        self.assertNotIn('__privateSyncMethod', protected_sync_methods)

    async def testGetProtectedAsyncMethods(self):
        """
        Test the getProtectedAsyncMethods method of ReflectionAbstract.

        Verifies that the getProtectedAsyncMethods method correctly returns only
        asynchronous methods with protected visibility.

        Assertions
        ----------
        Should include protected async methods and exclude sync, public, and private methods.
        """
        reflect = ReflectionAbstract(AbstractFakeClass)
        protected_async_methods = reflect.getProtectedAsyncMethods()
        self.assertIn('_protectedAsyncMethod', protected_async_methods)
        self.assertNotIn('instanceSyncMethod', protected_async_methods)
        self.assertNotIn('__privateSyncMethod', protected_async_methods)

    async def testGetPrivateMethods(self):
        """
        Test the getPrivateMethods method of ReflectionAbstract.

        Verifies that the getPrivateMethods method correctly returns only
        methods with private visibility (double leading underscore).

        Assertions
        ----------
        Should include private methods and exclude public and protected methods.
        """
        reflect = ReflectionAbstract(AbstractFakeClass)
        private_methods = reflect.getPrivateMethods()
        self.assertIn('__privateSyncMethod', private_methods)
        self.assertNotIn('instanceSyncMethod', private_methods)
        self.assertNotIn('_protectedAsyncMethod', private_methods)

    async def testGetPrivateSyncMethods(self):
        """
        Test the getPrivateSyncMethods method of ReflectionAbstract.

        Verifies that the getPrivateSyncMethods method correctly returns only
        synchronous methods with private visibility.

        Assertions
        ----------
        Should include private sync methods and exclude async, public, and protected methods.
        """
        reflect = ReflectionAbstract(AbstractFakeClass)
        private_sync_methods = reflect.getPrivateSyncMethods()
        self.assertIn('__privateSyncMethod', private_sync_methods)
        self.assertNotIn('instanceAsyncMethod', private_sync_methods)
        self.assertNotIn('_protectedAsyncMethod', private_sync_methods)

    async def testGetPrivateAsyncMethods(self):
        """
        Test the getPrivateAsyncMethods method of ReflectionAbstract.

        Verifies that the getPrivateAsyncMethods method correctly returns only
        asynchronous methods with private visibility.

        Assertions
        ----------
        Should include private async methods and exclude sync, public, and protected methods.
        """
        reflect = ReflectionAbstract(AbstractFakeClass)
        private_async_methods = reflect.getPrivateAsyncMethods()
        self.assertIn('__privateAsyncMethod', private_async_methods)
        self.assertNotIn('instanceSyncMethod', private_async_methods)
        self.assertNotIn('_protectedAsyncMethod', private_async_methods)

    async def testGetPublicClassMethods(self):
        """
        Test the getPublicClassMethods method of ReflectionAbstract.

        Verifies that the getPublicClassMethods method correctly returns only
        class methods with public visibility (no leading underscore).

        Assertions
        ----------
        Should include public class methods and exclude protected and private class methods.
        """
        reflect = ReflectionAbstract(AbstractFakeClass)
        public_class_methods = reflect.getPublicClassMethods()
        self.assertIn('classSyncMethod', public_class_methods)
        self.assertNotIn('_protected_class_method', public_class_methods)
        self.assertNotIn('__private_class_method', public_class_methods)

    async def testGetPublicClassSyncMethods(self):
        """
        Test the getPublicClassSyncMethods method of ReflectionAbstract.

        Verifies that the getPublicClassSyncMethods method correctly returns only
        synchronous class methods with public visibility.

        Assertions
        ----------
        Should include public class sync methods and exclude async, protected, and private methods.
        """
        reflect = ReflectionAbstract(AbstractFakeClass)
        public_class_sync_methods = reflect.getPublicClassSyncMethods()
        self.assertIn('classSyncMethod', public_class_sync_methods)
        self.assertNotIn('_protected_class_method', public_class_sync_methods)
        self.assertNotIn('__private_class_method', public_class_sync_methods)

    async def testGetPublicClassAsyncMethods(self):
        """
        Test getPublicClassAsyncMethods for public class async methods.

        Returns
        -------
        None

        Notes
        -----
        Ensures that only public class asynchronous methods are returned by
        getPublicClassAsyncMethods. Public methods have no leading underscores.
        """
        reflect = ReflectionAbstract(AbstractFakeClass)
        public_class_async_methods = reflect.getPublicClassAsyncMethods()
        self.assertIn('classAsyncMethod', public_class_async_methods)
        self.assertNotIn('_protected_class_async_method', public_class_async_methods)
        self.assertNotIn('__private_class_async_method', public_class_async_methods)

    async def testGetProtectedClassMethods(self):
        """
        Test getProtectedClassMethods for protected class methods.

        Returns
        -------
        None

        Notes
        -----
        Ensures that only protected class methods (single leading underscore)
        are returned by getProtectedClassMethods.
        """
        reflect = ReflectionAbstract(AbstractFakeClass)
        protected_class_methods = reflect.getProtectedClassMethods()
        self.assertIn('_classMethodProtected', protected_class_methods)
        self.assertNotIn('classSyncMethod', protected_class_methods)
        self.assertNotIn('__classMethodPrivate', protected_class_methods)

    async def testGetProtectedClassSyncMethods(self):
        """
        Test getProtectedClassSyncMethods for protected class sync methods.

        Returns
        -------
        None

        Notes
        -----
        Ensures that only protected synchronous class methods (single leading underscore)
        are returned by getProtectedClassSyncMethods.
        """
        reflect = ReflectionAbstract(AbstractFakeClass)
        protected_class_sync_methods = reflect.getProtectedClassSyncMethods()
        self.assertIn('_classMethodProtected', protected_class_sync_methods)
        self.assertNotIn('classSyncMethod', protected_class_sync_methods)
        self.assertNotIn('__classSyncMethodPrivate', protected_class_sync_methods)

    async def testGetProtectedClassAsyncMethods(self):
        """
        Test that getProtectedClassAsyncMethods returns only protected class asynchronous methods.

        Returns
        -------
        None

        Notes
        -----
        Ensures that only protected class async methods (single leading underscore)
        are included in the result, while public and private class async methods are excluded.
        """
        reflect = ReflectionAbstract(AbstractFakeClass)
        protected_class_async_methods = reflect.getProtectedClassAsyncMethods()
        self.assertIn('_classAsyncMethodProtected', protected_class_async_methods)
        self.assertNotIn('classAsyncMethod', protected_class_async_methods)
        self.assertNotIn('__classAsyncMethodPrivate', protected_class_async_methods)

    async def testGetPrivateClassMethods(self):
        """
        Test that getPrivateClassMethods returns only private class methods.

        Returns
        -------
        None

        Notes
        -----
        Ensures that only private class methods (double leading underscore)
        are included in the result, while public and protected class methods are excluded.
        """
        reflect = ReflectionAbstract(AbstractFakeClass)
        private_class_methods = reflect.getPrivateClassMethods()
        self.assertIn('__classMethodPrivate', private_class_methods)
        self.assertNotIn('classSyncMethod', private_class_methods)
        self.assertNotIn('_classMethodProtected', private_class_methods)

    async def testGetPrivateClassSyncMethods(self):
        """
        Test that getPrivateClassSyncMethods returns only private synchronous class methods.

        Returns
        -------
        None

        Notes
        -----
        Ensures that only private synchronous class methods (double leading underscore)
        are included in the result, while public and protected class sync methods are excluded.
        """
        reflect = ReflectionAbstract(AbstractFakeClass)
        private_class_methods = reflect.getPrivateClassSyncMethods()
        self.assertIn('__classMethodPrivate', private_class_methods)
        self.assertNotIn('classSyncMethod', private_class_methods)
        self.assertNotIn('_classMethodProtected', private_class_methods)

    async def testGetPrivateClassAsyncMethods(self):
        """
        Test that getPrivateClassAsyncMethods returns only private class asynchronous methods.

        Returns
        -------
        None

        Notes
        -----
        Ensures that only private class async methods (double leading underscore)
        are included in the result, while public and protected class async methods are excluded.
        """
        reflect = ReflectionAbstract(AbstractFakeClass)
        private_class_async_methods = reflect.getPrivateClassAsyncMethods()
        self.assertIn('__classAsyncMethodPrivate', private_class_async_methods)
        self.assertNotIn('classAsyncMethod', private_class_async_methods)
        self.assertNotIn('_classAsyncMethodProtected', private_class_async_methods)

    async def testGetPublicStaticMethods(self):
        """
        Test that getPublicStaticMethods returns only public static methods.

        Returns
        -------
        None

        Notes
        -----
        Ensures that only public static methods (no leading underscore) are included in the result.
        Both synchronous and asynchronous public static methods are considered.
        """
        reflect = ReflectionAbstract(AbstractFakeClass)
        public_static_methods = reflect.getPublicStaticMethods()
        self.assertIn('staticMethod', public_static_methods)
        self.assertIn('staticAsyncMethod', public_static_methods)
        self.assertNotIn('static_async_method', public_static_methods)

    async def testGetPublicStaticSyncMethods(self):
        """
        Test that getPublicStaticSyncMethods returns only public static synchronous methods.

        Returns
        -------
        None

        Notes
        -----
        Ensures that only public static synchronous methods (no leading underscore)
        are included in the result, while async and non-public static methods are excluded.
        """
        reflect = ReflectionAbstract(AbstractFakeClass)
        public_static_sync_methods = reflect.getPublicStaticSyncMethods()
        self.assertIn('staticMethod', public_static_sync_methods)
        self.assertNotIn('staticAsyncMethod', public_static_sync_methods)
        self.assertNotIn('static_async_method', public_static_sync_methods)

    async def testGetPublicStaticAsyncMethods(self):
        """
        Test that getPublicStaticAsyncMethods returns only public static asynchronous methods.

        Returns
        -------
        None

        Notes
        -----
        Ensures that only public static asynchronous methods (no leading underscore)
        are included in the result, while synchronous and non-public static methods are excluded.
        """
        reflect = ReflectionAbstract(AbstractFakeClass)
        public_static_async_methods = reflect.getPublicStaticAsyncMethods()
        self.assertIn('staticAsyncMethod', public_static_async_methods)
        self.assertNotIn('staticMethod', public_static_async_methods)
        self.assertNotIn('static_async_method', public_static_async_methods)

    async def testGetProtectedStaticMethods(self):
        """
        Test that getProtectedStaticMethods returns only protected static methods.

        Returns
        -------
        None

        Notes
        -----
        Ensures that only protected static methods (single leading underscore)
        are included in the result, while public and private static methods are excluded.
        """
        reflect = ReflectionAbstract(AbstractFakeClass)
        protected_static_methods = reflect.getProtectedStaticMethods()
        self.assertIn('_staticMethodProtected', protected_static_methods)
        self.assertNotIn('staticMethod', protected_static_methods)
        self.assertNotIn('__staticMethodPrivate', protected_static_methods)

    async def testGetProtectedStaticSyncMethods(self):
        """
        Test that getProtectedStaticSyncMethods returns only protected static synchronous methods.

        Returns
        -------
        None

        Notes
        -----
        Ensures that only protected static synchronous methods (single leading underscore)
        are included in the result, while async, public, and private static methods are excluded.
        """
        reflect = ReflectionAbstract(AbstractFakeClass)
        protected_static_sync_methods = reflect.getProtectedStaticSyncMethods()
        self.assertIn('_staticMethodProtected', protected_static_sync_methods)
        self.assertNotIn('staticAsyncMethod', protected_static_sync_methods)
        self.assertNotIn('__staticMethodPrivate', protected_static_sync_methods)

    async def testGetProtectedStaticAsyncMethods(self):
        """
        Test that getProtectedStaticAsyncMethods returns only protected static asynchronous methods.

        Returns
        -------
        None

        Notes
        -----
        Ensures that only protected static asynchronous methods (single leading underscore)
        are included in the result, while public and private static methods are excluded.
        """
        reflect = ReflectionAbstract(AbstractFakeClass)
        protected_static_async_methods = reflect.getProtectedStaticAsyncMethods()
        self.assertIn('_staticAsyncMethodProtected', protected_static_async_methods)
        self.assertNotIn('staticMethod', protected_static_async_methods)
        self.assertNotIn('__staticMethodPrivate', protected_static_async_methods)

    async def testGetPrivateStaticMethods(self):
        """
        Test that getPrivateStaticMethods returns only private static methods.

        Returns
        -------
        None

        Notes
        -----
        Ensures that only private static methods (double leading underscore)
        are included in the result, while public and protected static methods are excluded.
        """
        reflect = ReflectionAbstract(AbstractFakeClass)
        private_static_methods = reflect.getPrivateStaticMethods()
        self.assertIn('__staticMethodPrivate', private_static_methods)
        self.assertNotIn('staticMethod', private_static_methods)
        self.assertNotIn('_staticMethodProtected', private_static_methods)

    async def testGetPrivateStaticSyncMethods(self):
        """
        Test that getPrivateStaticSyncMethods returns only private static synchronous methods.

        Returns
        -------
        None

        Notes
        -----
        Ensures that only private static synchronous methods (double leading underscore)
        are included in the result, while public and protected static sync methods are excluded.
        """
        reflect = ReflectionAbstract(AbstractFakeClass)
        private_static_sync_methods = reflect.getPrivateStaticSyncMethods()
        self.assertIn('__staticMethodPrivate', private_static_sync_methods)
        self.assertNotIn('staticMethod', private_static_sync_methods)
        self.assertNotIn('_staticMethodProtected', private_static_sync_methods)

    async def testGetPrivateStaticAsyncMethods(self):
        """
        Test that getPrivateStaticAsyncMethods returns only private static asynchronous methods.

        Parameters
        ----------
        self : TestServiceReflectionAbstract
            The test case instance.

        Returns
        -------
        None

        Notes
        -----
        Ensures that only private static asynchronous methods (double leading underscore)
        are included in the result, while public and protected static async methods are excluded.
        """
        reflect = ReflectionAbstract(AbstractFakeClass)
        private_static_async_methods = reflect.getPrivateStaticAsyncMethods()
        # Should include only double underscore (private) static async methods
        self.assertIn('__staticAsyncMethodPrivate', private_static_async_methods)
        self.assertNotIn('staticAsyncMethod', private_static_async_methods)
        self.assertNotIn('_staticAsyncMethodProtected', private_static_async_methods)

    async def testGetDunderMethods(self):
        """
        Test the getDunderMethods method of ReflectionAbstract.

        Verifies that the getDunderMethods method correctly returns methods
        that follow the dunder (double underscore) naming convention.

        Assertions
        ----------
        Should include methods with double underscores at both ends like __init__.
        """
        reflect = ReflectionAbstract(AbstractFakeClass)
        dunder_methods = reflect.getDunderMethods()
        self.assertIn('__init__', dunder_methods)

    async def testGetMagicMethods(self):
        """
        Test the getMagicMethods method of ReflectionAbstract.

        Verifies that the getMagicMethods method correctly returns methods
        that are considered magic methods or special methods in Python.

        Assertions
        ----------
        Should include magic methods like dunder methods.
        """
        reflect = ReflectionAbstract(AbstractFakeClass)
        magic_methods = reflect.getMagicMethods()
        self.assertIn('__init__', magic_methods)

    async def testGetProperties(self):
        """
        Test the getProperties method of ReflectionAbstract.

        Verifies that the getProperties method correctly returns all properties
        defined in the class using the @property decorator.

        Assertions
        ----------
        The returned collection should contain the expected class properties.
        """
        reflect = ReflectionAbstract(AbstractFakeClass)
        properties = reflect.getProperties()
        self.assertIn('computed_public_property', properties)
        self.assertIn('_computed_property_protected', properties)
        self.assertIn('__computed_property_private', properties)

    async def testGetPublicProperties(self):
        """
        Test the getPublicProperties method of ReflectionAbstract.

        Verifies that the getPublicProperties method correctly returns only
        properties with public visibility (no leading underscore).

        Assertions
        ----------
        Should include public properties and exclude protected and private properties.
        """
        reflect = ReflectionAbstract(AbstractFakeClass)
        public_properties = reflect.getPublicProperties()
        self.assertIn('computed_public_property', public_properties)
        self.assertNotIn('_computed_property_protected', public_properties)
        self.assertNotIn('__computed_property_private', public_properties)

    async def testGetProtectedProperties(self):
        """
        Test the getProtectedProperties method of ReflectionAbstract.

        Verifies that the getProtectedProperties method correctly returns only
        properties with protected visibility (single leading underscore).

        Assertions
        ----------
        Should include protected properties and exclude public and private properties.
        """
        reflect = ReflectionAbstract(AbstractFakeClass)
        protected_properties = reflect.getProtectedProperties()
        self.assertIn('_computed_property_protected', protected_properties)
        self.assertNotIn('computed_public_property', protected_properties)
        self.assertNotIn('__computed_property_private', protected_properties)

    async def testGetPrivateProperties(self):
        """
        Test the getPrivateProperties method of ReflectionAbstract.

        Verifies that the getPrivateProperties method correctly returns only
        properties with private visibility (double leading underscore).

        Assertions
        ----------
        Should include private properties and exclude public and protected properties.
        """
        reflect = ReflectionAbstract(AbstractFakeClass)
        private_properties = reflect.getPrivateProperties()
        self.assertIn('__computed_property_private', private_properties)
        self.assertNotIn('computed_public_property', private_properties)
        self.assertNotIn('_computed_property_protected', private_properties)

    async def testGetPropertySignature(self):
        """
        Test the getPropertySignature method of ReflectionAbstract.

        Verifies that the getPropertySignature method correctly returns the
        signature of a property's getter method.

        Assertions
        ----------
        The returned signature should match the expected property signature format.
        """
        reflect = ReflectionAbstract(AbstractFakeClass)
        signature = reflect.getPropertySignature('computed_public_property')
        self.assertEqual(str(signature), '(self) -> str')

    async def testGetPropertyDocstring(self):
        """
        Test the getPropertyDocstring method of ReflectionAbstract.

        Verifies that the getPropertyDocstring method correctly returns the
        docstring of a property.

        Assertions
        ----------
        The returned docstring should contain the expected property documentation.
        """
        reflect = ReflectionAbstract(AbstractFakeClass)
        docstring = reflect.getPropertyDocstring('computed_public_property')
        self.assertIn('Abstract property for a computed', docstring)

    async def testGetConstructorDependencies(self):
        """
        Test the getConstructorDependencies method of ReflectionAbstract.

        Verifies that the getConstructorDependencies method correctly returns
        the dependencies required by the class constructor.

        Assertions
        ----------
        Should return a ResolveArguments instance with constructor dependencies.
        """
        reflect = ReflectionAbstract(AbstractFakeClass)
        dependencies = reflect.getConstructorDependencies()
        self.assertIsInstance(dependencies, ResolveArguments)

    async def testGetMethodDependencies(self):
        """
        Test the getMethodDependencies method of ReflectionAbstract.

        Verifies that the getMethodDependencies method correctly returns the
        dependencies and parameter information for a specific method.

        Assertions
        ----------
        Should return method dependencies with correct parameter types and metadata.
        """
        reflect = ReflectionAbstract(AbstractFakeClass)
        method_deps: ResolveArguments = reflect.getMethodDependencies('instanceSyncMethod')
        self.assertIn('x', method_deps.unresolved)
        self.assertIn('y', method_deps.unresolved)