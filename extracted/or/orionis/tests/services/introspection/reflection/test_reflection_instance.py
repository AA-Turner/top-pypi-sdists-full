from orionis.services.introspection.dependencies.entities.class_dependencies import ClassDependency
from tests.services.introspection.reflection.mock.fake_reflect_instance import FakeClass
from orionis.services.introspection.instances.reflection import ReflectionInstance
from orionis.test.cases.asynchronous import AsyncTestCase

class TestServiceReflectionInstance(AsyncTestCase):

    async def testGetInstance(self):
        """
        Test ReflectionInstance.getInstance() method functionality.

        Verifies that the getInstance() method returns the wrapped instance object 
        correctly. Creates a ReflectionInstance wrapper around a FakeClass object
        and validates that the retrieved instance maintains its original type.

        Assertions
        ----------
        - Retrieved instance is of type FakeClass
        """
        reflect = ReflectionInstance(FakeClass())
        instance = reflect.getInstance()
        self.assertIsInstance(instance, FakeClass)

    async def testGetClass(self):
        """
        Test ReflectionInstance.getClass() method functionality.

        Verifies that the getClass method correctly returns the class type
        of the wrapped instance object. Creates a ReflectionInstance with 
        a FakeClass instance and validates the returned class type.

        Assertions
        ----------
        - Returned class equals FakeClass type
        """
        reflect = ReflectionInstance(FakeClass())
        cls = reflect.getClass()
        self.assertEqual(cls, FakeClass)

    async def testGetClassName(self):
        """
        Test ReflectionInstance.getClassName() method functionality.

        Verifies that the getClassName method correctly retrieves the string
        name of the wrapped instance's class. Creates a ReflectionInstance
        with a FakeClass object and validates the returned class name.

        Assertions
        ----------
        - Returned class name equals 'FakeClass'
        """
        reflect = ReflectionInstance(FakeClass())
        class_name = reflect.getClassName()
        self.assertEqual(class_name, 'FakeClass')

    async def testGetModuleName(self):
        """
        Test ReflectionInstance.getModuleName() method functionality.

        Verifies that the getModuleName method correctly returns the fully
        qualified module name of the wrapped instance's class. Creates a
        ReflectionInstance with a FakeClass object and validates the module path.

        Assertions
        ----------
        - Returned module name equals 'tests.services.introspection.reflection.mock.fake_reflect_instance'
        """
        reflect = ReflectionInstance(FakeClass())
        module_name = reflect.getModuleName()
        self.assertEqual(module_name, 'tests.services.introspection.reflection.mock.fake_reflect_instance')

    async def testGetModuleWithClassName(self):
        """
        Test ReflectionInstance.getModuleWithClassName() method functionality.

        Verifies that the getModuleWithClassName method returns the fully qualified
        module path combined with the class name. Creates a ReflectionInstance
        with a FakeClass object and validates the complete module.class path.

        Assertions
        ----------
        - Returned string equals 'tests.services.introspection.reflection.mock.fake_reflect_instance.FakeClass'
        """
        reflect = ReflectionInstance(FakeClass())
        module_with_class_name = reflect.getModuleWithClassName()
        self.assertEqual(module_with_class_name, 'tests.services.introspection.reflection.mock.fake_reflect_instance.FakeClass')

    async def testGetDocstring(self):
        """
        Test ReflectionInstance.getDocstring() method functionality.

        Verifies that the getDocstring method correctly retrieves the docstring
        of the wrapped instance's class. Creates a ReflectionInstance with a
        FakeClass object and compares the returned docstring with the class's __doc__.

        Assertions
        ----------
        - Returned docstring equals FakeClass.__doc__
        """
        reflect = ReflectionInstance(FakeClass())
        docstring = reflect.getDocstring()
        self.assertEqual(docstring, FakeClass.__doc__)

    async def testGetBaseClasses(self):
        """
        Test ReflectionInstance.getBaseClasses() method functionality.

        Verifies that the getBaseClasses method correctly retrieves the base
        classes of the wrapped instance's class. Creates a ReflectionInstance
        with a FakeClass object and validates that the base class is included.

        Assertions
        ----------
        - FakeClass.__base__ is present in the returned base classes list
        """
        reflect = ReflectionInstance(FakeClass())
        base_classes = reflect.getBaseClasses()
        self.assertIn(FakeClass.__base__, base_classes)

    async def testGetSourceCode(self):
        """
        Test ReflectionInstance.getSourceCode() method functionality.

        Verifies that the getSourceCode method correctly retrieves the source
        code of the wrapped instance's class. Creates a ReflectionInstance
        with a FakeClass object and validates the source code content.

        Assertions
        ----------
        - Returned source code starts with 'class FakeClass'
        """
        reflect = ReflectionInstance(FakeClass())
        source_code = reflect.getSourceCode()
        self.assertTrue(source_code.startswith('class FakeClass'))

    async def testGetFile(self):
        """
        Test ReflectionInstance.getFile() method functionality.

        Verifies that the getFile method correctly returns the file path
        of the wrapped instance's class definition. Creates a ReflectionInstance
        with a FakeClass object and validates the returned file path.

        Assertions
        ----------
        - Returned file path ends with 'fake_reflect_instance.py'
        """
        reflect = ReflectionInstance(FakeClass())
        file_path = reflect.getFile()
        self.assertTrue(file_path.endswith('fake_reflect_instance.py'))

    async def testGetAnnotations(self):
        """
        Test ReflectionInstance.getAnnotations() method functionality.

        Verifies that the getAnnotations method correctly returns the type
        annotations of the wrapped instance's class. Creates a ReflectionInstance
        with a FakeClass object and validates the presence of expected annotations.

        Assertions
        ----------
        - 'public_attr' annotation is present in the returned annotations
        """
        reflect = ReflectionInstance(FakeClass())
        annotations = reflect.getAnnotations()
        self.assertIn('public_attr', annotations)

    async def testHasAttribute(self):
        """
        Test ReflectionInstance.hasAttribute() method functionality.

        Verifies that the hasAttribute method correctly identifies the presence
        or absence of attributes on the wrapped instance. Tests both existing
        and non-existing attributes to validate proper boolean responses.

        Assertions
        ----------
        - Returns True for existing attribute 'public_attr'
        - Returns False for non-existent attribute 'non_existent_attr'
        """
        reflect = ReflectionInstance(FakeClass())
        self.assertTrue(reflect.hasAttribute('public_attr'))
        self.assertFalse(reflect.hasAttribute('non_existent_attr'))

    async def testGetAttribute(self):
        """
        Test ReflectionInstance.getAttribute() method functionality.

        Verifies that the getAttribute method correctly retrieves attribute
        values from the wrapped instance. Tests both existing attributes
        and non-existent attributes to validate proper value retrieval.

        Assertions
        ----------
        - Returns correct value (42) for existing attribute 'public_attr'
        - Returns None for non-existent attribute 'non_existent_attr'
        """
        reflect = ReflectionInstance(FakeClass())
        self.assertEqual(reflect.getAttribute('public_attr'), 42)
        self.assertIsNone(reflect.getAttribute('non_existent_attr'))

    async def testSetAttribute(self):
        """
        Test ReflectionInstance.setAttribute() method functionality.

        Verifies that the setAttribute method correctly sets attribute values
        on the wrapped instance, including public, protected, and private attributes.
        Also validates that the updated values can be retrieved using getAttribute.

        Assertions
        ----------
        - setAttribute returns True when setting public attribute 'name'
        - Public attribute value is updated correctly to 'Orionis Framework'
        - setAttribute returns True when setting protected attribute '_version'
        - Protected attribute value is updated correctly to '1.x'
        - setAttribute returns True when setting private attribute '__python'
        - Private attribute value is updated correctly to '3.13+'
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
        Test ReflectionInstance.removeAttribute() method functionality.

        Verifies that the removeAttribute method successfully removes an attribute
        from the wrapped instance. Tests the removal process by first setting
        an attribute, then removing it, and validating its absence.

        Assertions
        ----------
        - removeAttribute returns True when removing an existing attribute
        - Attribute is no longer present after removal (hasAttribute returns False)
        """
        reflect = ReflectionInstance(FakeClass())
        reflect.setAttribute('new_attr', 100)
        self.assertTrue(reflect.removeAttribute('new_attr'))
        self.assertFalse(reflect.hasAttribute('new_attr'))

    async def testGetAttributes(self):
        """
        Test ReflectionInstance.getAttributes() method functionality.

        Verifies that the getAttributes method correctly retrieves all attribute
        names from the wrapped instance, including public, protected, and private
        attributes. Tests comprehensive attribute visibility.

        Assertions
        ----------
        - 'public_attr' is present in the returned attributes list
        - '_protected_attr' is present in the returned attributes list
        - '__private_attr' is present in the returned attributes list
        """
        reflect = ReflectionInstance(FakeClass())
        attributes = reflect.getAttributes()
        self.assertIn('public_attr', attributes)
        self.assertIn('_protected_attr', attributes)
        self.assertIn('__private_attr', attributes)

    async def testGetPublicAttributes(self):
        """
        Test ReflectionInstance.getPublicAttributes() method functionality.

        Verifies that the getPublicAttributes method returns only public attributes
        of the wrapped instance, excluding protected and private attributes. Tests
        proper visibility filtering based on Python naming conventions.

        Assertions
        ----------
        - 'public_attr' is included in the returned list
        - '_protected_attr' is not included in the returned list
        - '__private_attr' is not included in the returned list
        """
        reflect = ReflectionInstance(FakeClass())
        public_attributes = reflect.getPublicAttributes()
        self.assertIn('public_attr', public_attributes)
        self.assertNotIn('_protected_attr', public_attributes)
        self.assertNotIn('__private_attr', public_attributes)

    async def testGetProtectedAttributes(self):
        """
        Test ReflectionInstance.getProtectedAttributes() method functionality.

        Verifies that the getProtectedAttributes method correctly identifies and
        returns only protected attributes (prefixed with single underscore) of
        the wrapped instance, excluding public and private attributes.

        Assertions
        ----------
        - '_protected_attr' is included in the returned list
        - 'public_attr' is not included in the returned list
        - '__private_attr' is not included in the returned list
        """
        reflect = ReflectionInstance(FakeClass())
        protected_attributes = reflect.getProtectedAttributes()
        self.assertIn('_protected_attr', protected_attributes)
        self.assertNotIn('public_attr', protected_attributes)
        self.assertNotIn('__private_attr', protected_attributes)

    async def testGetPrivateAttributes(self):
        """
        Test ReflectionInstance.getPrivateAttributes() method functionality.

        Verifies that the getPrivateAttributes method correctly identifies and
        returns only private attributes (prefixed with double underscores) of
        the wrapped instance, excluding public and protected attributes.

        Assertions
        ----------
        - '__private_attr' is included in the returned list
        - 'public_attr' is not included in the returned list
        - '_protected_attr' is not included in the returned list
        """
        reflect = ReflectionInstance(FakeClass())
        private_attributes = reflect.getPrivateAttributes()
        self.assertIn('__private_attr', private_attributes)
        self.assertNotIn('public_attr', private_attributes)
        self.assertNotIn('_protected_attr', private_attributes)

    async def testGetDunderAttributes(self):
        """
        Test ReflectionInstance.getDunderAttributes() method functionality.

        Verifies that the getDunderAttributes method correctly retrieves all
        double underscore (dunder) attributes from the wrapped instance. Tests
        the identification of special attributes with the dunder naming pattern.

        Assertions
        ----------
        - '__dd__' is present in the returned list of dunder attributes
        """
        reflect = ReflectionInstance(FakeClass())
        dunder_attributes = reflect.getDunderAttributes()
        self.assertIn('__dd__', dunder_attributes)

    async def testGetMagicAttributes(self):
        """
        Test ReflectionInstance.getMagicAttributes() method functionality.

        Verifies that the getMagicAttributes method returns a list of magic attributes
        (special methods and attributes with double underscores) for the wrapped instance.
        Tests the identification of Python magic/special attributes.

        Assertions
        ----------
        - '__dd__' is present in the returned list of magic attributes
        """
        reflect = ReflectionInstance(FakeClass())
        magic_attributes = reflect.getMagicAttributes()
        self.assertIn('__dd__', magic_attributes)

    async def testHasMethod(self):
        """
        Test ReflectionInstance.hasMethod() method functionality.

        Verifies that the hasMethod method correctly identifies the presence
        or absence of methods on the wrapped instance. Tests both existing
        and non-existing methods to validate proper boolean responses.

        Assertions
        ----------
        - Returns True for existing method 'instanceSyncMethod'
        - Returns False for non-existent method 'non_existent_method'
        """
        reflect = ReflectionInstance(FakeClass())
        self.assertTrue(reflect.hasMethod('instanceSyncMethod'))
        self.assertFalse(reflect.hasMethod('non_existent_method'))

    async def testCallMethod(self):
        """
        Test ReflectionInstance.callMethod() synchronous method functionality.

        Verifies that the callMethod method correctly invokes synchronous methods
        on the wrapped instance with arguments and returns the expected result.
        Tests method execution through reflection with parameter passing.

        Assertions
        ----------
        - Calling 'instanceSyncMethod' with arguments 2 and 3 returns 5
        """
        reflect = ReflectionInstance(FakeClass())
        result = reflect.callMethod('instanceSyncMethod', 2, 3)
        self.assertEqual(result, 5)

    async def testCallAsyncMethod(self):
        """
        Test ReflectionInstance.callMethod() asynchronous method functionality.

        Verifies that the callMethod method correctly invokes asynchronous methods
        on the wrapped instance with arguments and returns the expected result.
        Tests async method execution through reflection with parameter passing.

        Assertions
        ----------
        - Calling 'instanceAsyncMethod' with arguments 2 and 3 returns 5
        """
        reflect = ReflectionInstance(FakeClass())
        result = await reflect.callMethod('instanceAsyncMethod', 2, 3)
        self.assertEqual(result, 5)

    async def testSetMethod(self):
        """
        Test ReflectionInstance.setMethod() method functionality.

        Verifies that the setMethod method can dynamically add both synchronous
        and asynchronous methods to the wrapped instance. Tests the ability to
        set custom methods and then call them through the reflection interface.

        Assertions
        ----------
        - Synchronous mock method returns expected result (5) when called with arguments 2 and 3
        - Asynchronous mock method returns expected result (5) when called with arguments 2 and 3
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
        Test ReflectionInstance.removeMethod() method functionality.

        Verifies that the removeMethod method can successfully remove dynamically
        added methods from the wrapped instance. Tests the process of adding a
        method, confirming its existence, removing it, and validating its absence.

        Assertions
        ----------
        - Method exists after being added (hasMethod returns True)
        - Method no longer exists after removal (hasMethod returns False)
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
        Test ReflectionInstance.getMethodSignature() method functionality.

        Verifies that the getMethodSignature method correctly retrieves the
        signature of a specified method from the wrapped instance. Tests
        signature inspection and string representation of method parameters.

        Assertions
        ----------
        - Signature of 'instanceSyncMethod' equals '(self, x: int, y: int) -> int'
        """
        reflect = ReflectionInstance(FakeClass())
        signature = reflect.getMethodSignature('instanceSyncMethod')
        self.assertEqual(str(signature), '(self, x: int, y: int) -> int')

    async def testGetMethods(self):
        """
        Test ReflectionInstance.getMethods() method functionality.

        Verifies that the getMethods method correctly retrieves the names of all
        instance methods from the wrapped instance, including both synchronous
        and asynchronous methods. Tests comprehensive method discovery.

        Assertions
        ----------
        - 'instanceSyncMethod' is present in the returned methods list
        - 'instanceAsyncMethod' is present in the returned methods list
        """
        reflect = ReflectionInstance(FakeClass())
        methods = reflect.getMethods()
        self.assertIn('instanceSyncMethod', methods)
        self.assertIn('instanceAsyncMethod', methods)

    async def testGetPublicMethods(self):
        """
        Test ReflectionInstance.getPublicMethods() method functionality.

        Verifies that the getPublicMethods method returns only public methods
        of the wrapped instance, excluding protected and private methods. Tests
        method visibility filtering based on Python naming conventions.

        Assertions
        ----------
        - 'instanceSyncMethod' is included in the returned list
        - '_protected_method' is not included in the returned list
        - '__private_method' is not included in the returned list
        """
        reflect = ReflectionInstance(FakeClass())
        public_methods = reflect.getPublicMethods()
        self.assertIn('instanceSyncMethod', public_methods)
        self.assertNotIn('_protected_method', public_methods)
        self.assertNotIn('__private_method', public_methods)

    async def testGetPublicSyncMethods(self):
        """
        Test ReflectionInstance.getPublicSyncMethods() method functionality.

        Verifies that the getPublicSyncMethods method returns only the names of
        public synchronous methods from the wrapped instance, excluding protected
        and private methods. Tests synchronous method filtering with visibility.

        Assertions
        ----------
        - 'instanceSyncMethod' is included in the returned list
        - '_protected_method' is not included in the returned list
        - '__private_method' is not included in the returned list
        """
        reflect = ReflectionInstance(FakeClass())
        public_sync_methods = reflect.getPublicSyncMethods()
        self.assertIn('instanceSyncMethod', public_sync_methods)
        self.assertNotIn('_protected_method', public_sync_methods)
        self.assertNotIn('__private_method', public_sync_methods)

    async def testGetPublicAsyncMethods(self):
        """
        Test ReflectionInstance.getPublicAsyncMethods() method functionality.

        Verifies that the getPublicAsyncMethods method correctly identifies and
        returns only public asynchronous methods from the wrapped instance,
        excluding protected and private async methods.

        Assertions
        ----------
        - 'instanceAsyncMethod' is included in the returned list
        - '_protected_async_method' is not included in the returned list
        - '__private_async_method' is not included in the returned list
        """
        reflect = ReflectionInstance(FakeClass())
        public_async_methods = reflect.getPublicAsyncMethods()
        self.assertIn('instanceAsyncMethod', public_async_methods)
        self.assertNotIn('_protected_async_method', public_async_methods)
        self.assertNotIn('__private_async_method', public_async_methods)

    async def testGetProtectedMethods(self):
        """
        Test ReflectionInstance.getProtectedMethods() method functionality.

        Verifies that the getProtectedMethods method correctly identifies and
        returns only protected methods (prefixed with single underscore) from
        the wrapped instance, excluding public and private methods.

        Assertions
        ----------
        - '_protectedAsyncMethod' is included in the returned list
        - 'instanceSyncMethod' is not included in the returned list
        - '__privateSyncMethod' is not included in the returned list
        """
        reflect = ReflectionInstance(FakeClass())
        protected_methods = reflect.getProtectedMethods()
        self.assertIn('_protectedAsyncMethod', protected_methods)
        self.assertNotIn('instanceSyncMethod', protected_methods)
        self.assertNotIn('__privateSyncMethod', protected_methods)

    async def testGetProtectedSyncMethods(self):
        """
        Test ReflectionInstance.getProtectedSyncMethods() method functionality.

        Verifies that the getProtectedSyncMethods method correctly identifies and
        returns only protected synchronous methods (prefixed with single underscore)
        from the wrapped instance, excluding async and private methods.

        Assertions
        ----------
        - '_protectedsyncMethod' is included in the returned list
        - 'instanceAsyncMethod' is not included in the returned list
        - '__privateSyncMethod' is not included in the returned list
        """
        reflect = ReflectionInstance(FakeClass())
        protected_sync_methods = reflect.getProtectedSyncMethods()
        self.assertIn('_protectedsyncMethod', protected_sync_methods)
        self.assertNotIn('instanceAsyncMethod', protected_sync_methods)
        self.assertNotIn('__privateSyncMethod', protected_sync_methods)

    async def testGetProtectedAsyncMethods(self):
        """
        Test ReflectionInstance.getProtectedAsyncMethods() method functionality.

        Verifies that the getProtectedAsyncMethods method correctly identifies and
        returns only protected asynchronous methods (prefixed with single underscore)
        from the wrapped instance, excluding public and private methods.

        Assertions
        ----------
        - '_protectedAsyncMethod' is included in the returned list
        - 'instanceSyncMethod' is not included in the returned list
        - '__privateSyncMethod' is not included in the returned list
        """
        reflect = ReflectionInstance(FakeClass())
        protected_async_methods = reflect.getProtectedAsyncMethods()
        self.assertIn('_protectedAsyncMethod', protected_async_methods)
        self.assertNotIn('instanceSyncMethod', protected_async_methods)
        self.assertNotIn('__privateSyncMethod', protected_async_methods)

    async def testGetPrivateMethods(self):
        """
        Test ReflectionInstance.getPrivateMethods() method functionality.

        Verifies that the getPrivateMethods method correctly identifies and
        returns only private methods (prefixed with double underscores) from
        the wrapped instance, excluding public and protected methods.

        Assertions
        ----------
        - '__privateSyncMethod' is included in the returned list
        - 'instanceSyncMethod' is not included in the returned list
        - '_protectedAsyncMethod' is not included in the returned list
        """
        reflect = ReflectionInstance(FakeClass())
        private_methods = reflect.getPrivateMethods()
        self.assertIn('__privateSyncMethod', private_methods)
        self.assertNotIn('instanceSyncMethod', private_methods)
        self.assertNotIn('_protectedAsyncMethod', private_methods)

    async def testGetPrivateSyncMethods(self):
        """
        Test ReflectionInstance.getPrivateSyncMethods() method functionality.

        Verifies that the getPrivateSyncMethods method correctly identifies and
        returns only private synchronous methods (prefixed with double underscores)
        from the wrapped instance, excluding async and protected methods.

        Assertions
        ----------
        - '__privateSyncMethod' is included in the returned list
        - 'instanceAsyncMethod' is not included in the returned list
        - '_protectedAsyncMethod' is not included in the returned list
        """
        reflect = ReflectionInstance(FakeClass())
        private_sync_methods = reflect.getPrivateSyncMethods()
        self.assertIn('__privateSyncMethod', private_sync_methods)
        self.assertNotIn('instanceAsyncMethod', private_sync_methods)
        self.assertNotIn('_protectedAsyncMethod', private_sync_methods)

    async def testGetPrivateAsyncMethods(self):
        """
        Test ReflectionInstance.getPrivateAsyncMethods() method functionality.

        Verifies that the getPrivateAsyncMethods method correctly identifies and
        returns only private asynchronous methods (prefixed with double underscores)
        from the wrapped instance, excluding public and protected methods.

        Assertions
        ----------
        - '__privateAsyncMethod' is included in the returned list
        - 'instanceSyncMethod' is not included in the returned list
        - '_protectedAsyncMethod' is not included in the returned list
        """
        reflect = ReflectionInstance(FakeClass())
        private_async_methods = reflect.getPrivateAsyncMethods()
        self.assertIn('__privateAsyncMethod', private_async_methods)
        self.assertNotIn('instanceSyncMethod', private_async_methods)
        self.assertNotIn('_protectedAsyncMethod', private_async_methods)

    async def testGetPublicClassMethods(self):
        """
        Test ReflectionInstance.getPublicClassMethods() method functionality.

        Verifies that the getPublicClassMethods method correctly identifies and
        returns only public class methods from the wrapped instance, excluding
        protected and private class methods.

        Assertions
        ----------
        - 'classSyncMethod' is included in the returned list
        - '_protected_class_method' is not included in the returned list
        - '__private_class_method' is not included in the returned list
        """
        reflect = ReflectionInstance(FakeClass())
        public_class_methods = reflect.getPublicClassMethods()
        self.assertIn('classSyncMethod', public_class_methods)
        self.assertNotIn('_protected_class_method', public_class_methods)
        self.assertNotIn('__private_class_method', public_class_methods)

    async def testGetPublicClassSyncMethods(self):
        """
        Test ReflectionInstance.getPublicClassSyncMethods() method functionality.

        Verifies that the getPublicClassSyncMethods method correctly identifies and
        returns only public synchronous class methods from the wrapped instance,
        excluding protected and private class methods.

        Assertions
        ----------
        - 'classSyncMethod' is included in the returned list
        - '_protected_class_method' is not included in the returned list
        - '__private_class_method' is not included in the returned list
        """
        reflect = ReflectionInstance(FakeClass())
        public_class_sync_methods = reflect.getPublicClassSyncMethods()
        self.assertIn('classSyncMethod', public_class_sync_methods)
        self.assertNotIn('_protected_class_method', public_class_sync_methods)
        self.assertNotIn('__private_class_method', public_class_sync_methods)

    async def testGetPublicClassAsyncMethods(self):
        """
        Test ReflectionInstance.getPublicClassAsyncMethods() method functionality.

        Verifies that the getPublicClassAsyncMethods method correctly identifies and
        returns only public asynchronous class methods from the wrapped instance,
        excluding protected and private async class methods.

        Assertions
        ----------
        - 'classAsyncMethod' is included in the returned list
        - '_protected_class_async_method' is not included in the returned list
        - '__private_class_async_method' is not included in the returned list
        """
        reflect = ReflectionInstance(FakeClass())
        public_class_async_methods = reflect.getPublicClassAsyncMethods()
        self.assertIn('classAsyncMethod', public_class_async_methods)
        self.assertNotIn('_protected_class_async_method', public_class_async_methods)
        self.assertNotIn('__private_class_async_method', public_class_async_methods)

    async def testGetProtectedClassMethods(self):
        """
        Test ReflectionInstance.getProtectedClassMethods() method functionality.

        Verifies that the getProtectedClassMethods method correctly identifies and
        returns only protected class methods (prefixed with single underscore) from
        the wrapped instance, excluding public and private class methods.

        Assertions
        ----------
        - '_classMethodProtected' is included in the returned list
        - 'classSyncMethod' is not included in the returned list
        - '__classMethodPrivate' is not included in the returned list
        """
        reflect = ReflectionInstance(FakeClass())
        protected_class_methods = reflect.getProtectedClassMethods()
        self.assertIn('_classMethodProtected', protected_class_methods)
        self.assertNotIn('classSyncMethod', protected_class_methods)
        self.assertNotIn('__classMethodPrivate', protected_class_methods)

    async def testGetProtectedClassSyncMethods(self):
        """
        Test ReflectionInstance.getProtectedClassSyncMethods() method functionality.

        Verifies that the getProtectedClassSyncMethods method correctly identifies and
        returns only protected synchronous class methods (prefixed with single underscore)
        from the wrapped instance, excluding public and private class methods.

        Assertions
        ----------
        - '_classMethodProtected' is included in the returned list
        - 'classSyncMethod' is not included in the returned list
        - '__classSyncMethodPrivate' is not included in the returned list
        """
        reflect = ReflectionInstance(FakeClass())
        protected_class_sync_methods = reflect.getProtectedClassSyncMethods()
        self.assertIn('_classMethodProtected', protected_class_sync_methods)
        self.assertNotIn('classSyncMethod', protected_class_sync_methods)
        self.assertNotIn('__classSyncMethodPrivate', protected_class_sync_methods)

    async def testGetProtectedClassAsyncMethods(self):
        """
        Test ReflectionInstance.getProtectedClassAsyncMethods() method functionality.

        Verifies that the getProtectedClassAsyncMethods method correctly identifies and
        returns only protected asynchronous class methods (prefixed with single underscore)
        from the wrapped instance, excluding public and private async class methods.

        Assertions
        ----------
        - '_classAsyncMethodProtected' is included in the returned list
        - 'classAsyncMethod' is not included in the returned list
        - '__classAsyncMethodPrivate' is not included in the returned list
        """
        reflect = ReflectionInstance(FakeClass())
        protected_class_async_methods = reflect.getProtectedClassAsyncMethods()
        self.assertIn('_classAsyncMethodProtected', protected_class_async_methods)
        self.assertNotIn('classAsyncMethod', protected_class_async_methods)
        self.assertNotIn('__classAsyncMethodPrivate', protected_class_async_methods)

    async def testGetPrivateClassMethods(self):
        """
        Test ReflectionInstance.getPrivateClassMethods() method functionality.

        Verifies that the getPrivateClassMethods method correctly identifies and
        returns only private class methods (prefixed with double underscores) from
        the wrapped instance, excluding public and protected class methods.

        Assertions
        ----------
        - '__classMethodPrivate' is included in the returned list
        - 'classSyncMethod' is not included in the returned list
        - '_classMethodProtected' is not included in the returned list
        """
        reflect = ReflectionInstance(FakeClass())
        private_class_methods = reflect.getPrivateClassMethods()
        self.assertIn('__classMethodPrivate', private_class_methods)
        self.assertNotIn('classSyncMethod', private_class_methods)
        self.assertNotIn('_classMethodProtected', private_class_methods)

    async def testGetPrivateClassSyncMethods(self):
        """
        Test ReflectionInstance.getPrivateClassSyncMethods() method functionality.

        Verifies that the getPrivateClassSyncMethods method correctly identifies and
        returns only private synchronous class methods (prefixed with double underscores)
        from the wrapped instance, excluding public and protected class methods.

        Assertions
        ----------
        - '__classMethodPrivate' is included in the returned list
        - 'classSyncMethod' is not included in the returned list
        - '_classMethodProtected' is not included in the returned list
        """
        reflect = ReflectionInstance(FakeClass())
        private_class_methods = reflect.getPrivateClassSyncMethods()
        self.assertIn('__classMethodPrivate', private_class_methods)
        self.assertNotIn('classSyncMethod', private_class_methods)
        self.assertNotIn('_classMethodProtected', private_class_methods)

    async def testGetPrivateClassAsyncMethods(self):
        """
        Test ReflectionInstance.getPrivateClassAsyncMethods() method functionality.

        Verifies that the getPrivateClassAsyncMethods method correctly identifies and
        returns only private asynchronous class methods (prefixed with double underscores)
        from the wrapped instance, excluding public and protected async class methods.

        Assertions
        ----------
        - '__classAsyncMethodPrivate' is included in the returned list
        - 'classAsyncMethod' is not included in the returned list
        - '_classAsyncMethodProtected' is not included in the returned list
        """
        reflect = ReflectionInstance(FakeClass())
        private_class_async_methods = reflect.getPrivateClassAsyncMethods()
        self.assertIn('__classAsyncMethodPrivate', private_class_async_methods)
        self.assertNotIn('classAsyncMethod', private_class_async_methods)
        self.assertNotIn('_classAsyncMethodProtected', private_class_async_methods)

    async def testGetPublicStaticMethods(self):
        """
        Test ReflectionInstance.getPublicStaticMethods() method functionality.

        Verifies that the getPublicStaticMethods method correctly identifies and
        returns the names of public static methods from the wrapped instance,
        excluding protected and private static methods.

        Assertions
        ----------
        - 'staticMethod' is included in the returned list
        - 'staticAsyncMethod' is included in the returned list
        - 'static_async_method' is not included in the returned list
        """
        reflect = ReflectionInstance(FakeClass())
        public_static_methods = reflect.getPublicStaticMethods()
        self.assertIn('staticMethod', public_static_methods)
        self.assertIn('staticAsyncMethod', public_static_methods)
        self.assertNotIn('static_async_method', public_static_methods)

    async def testGetPublicStaticSyncMethods(self):
        """
        Test ReflectionInstance.getPublicStaticSyncMethods() method functionality.

        Verifies that the getPublicStaticSyncMethods method correctly identifies and
        returns only public static synchronous methods from the wrapped instance,
        excluding async and non-public static methods.

        Assertions
        ----------
        - 'staticMethod' is included in the returned list
        - 'staticAsyncMethod' is not included in the returned list
        - 'static_async_method' is not included in the returned list
        """
        reflect = ReflectionInstance(FakeClass())
        public_static_sync_methods = reflect.getPublicStaticSyncMethods()
        self.assertIn('staticMethod', public_static_sync_methods)
        self.assertNotIn('staticAsyncMethod', public_static_sync_methods)
        self.assertNotIn('static_async_method', public_static_sync_methods)

    async def testGetPublicStaticAsyncMethods(self):
        """
        Test ReflectionInstance.getPublicStaticAsyncMethods() method functionality.

        Verifies that the getPublicStaticAsyncMethods method correctly identifies and
        returns only public static asynchronous methods from the wrapped instance,
        excluding sync and non-public static methods.

        Assertions
        ----------
        - 'staticAsyncMethod' is included in the returned list
        - 'staticMethod' is not included in the returned list
        - 'static_async_method' is not included in the returned list
        """
        reflect = ReflectionInstance(FakeClass())
        public_static_async_methods = reflect.getPublicStaticAsyncMethods()
        self.assertIn('staticAsyncMethod', public_static_async_methods)
        self.assertNotIn('staticMethod', public_static_async_methods)
        self.assertNotIn('static_async_method', public_static_async_methods)

    async def testGetProtectedStaticMethods(self):
        """
        Test ReflectionInstance.getProtectedStaticMethods() method functionality.

        Verifies that the getProtectedStaticMethods method correctly identifies and
        returns only protected static methods (prefixed with single underscore) from
        the wrapped instance, excluding public and private static methods.

        Assertions
        ----------
        - '_staticMethodProtected' is included in the returned list
        - 'staticMethod' is not included in the returned list
        - '__staticMethodPrivate' is not included in the returned list
        """
        reflect = ReflectionInstance(FakeClass())
        protected_static_methods = reflect.getProtectedStaticMethods()
        self.assertIn('_staticMethodProtected', protected_static_methods)
        self.assertNotIn('staticMethod', protected_static_methods)
        self.assertNotIn('__staticMethodPrivate', protected_static_methods)

    async def testGetProtectedStaticSyncMethods(self):
        """
        Test ReflectionInstance.getProtectedStaticSyncMethods() method functionality.

        Verifies that the getProtectedStaticSyncMethods method correctly identifies and
        returns only protected static synchronous methods (prefixed with single underscore)
        from the wrapped instance, excluding async and non-protected static methods.

        Assertions
        ----------
        - '_staticMethodProtected' is included in the returned list
        - 'staticAsyncMethod' is not included in the returned list
        - '__staticMethodPrivate' is not included in the returned list
        """
        reflect = ReflectionInstance(FakeClass())
        protected_static_sync_methods = reflect.getProtectedStaticSyncMethods()
        self.assertIn('_staticMethodProtected', protected_static_sync_methods)
        self.assertNotIn('staticAsyncMethod', protected_static_sync_methods)
        self.assertNotIn('__staticMethodPrivate', protected_static_sync_methods)

    async def testGetProtectedStaticAsyncMethods(self):
        """
        Test ReflectionInstance.getProtectedStaticAsyncMethods() method functionality.

        Verifies that the getProtectedStaticAsyncMethods method correctly identifies and
        returns only protected static asynchronous methods (prefixed with single underscore)
        from the wrapped instance, excluding public and private static methods.

        Assertions
        ----------
        - '_staticAsyncMethodProtected' is included in the returned list
        - 'staticMethod' is not included in the returned list
        - '__staticMethodPrivate' is not included in the returned list
        """
        reflect = ReflectionInstance(FakeClass())
        protected_static_async_methods = reflect.getProtectedStaticAsyncMethods()
        self.assertIn('_staticAsyncMethodProtected', protected_static_async_methods)
        self.assertNotIn('staticMethod', protected_static_async_methods)
        self.assertNotIn('__staticMethodPrivate', protected_static_async_methods)

    async def testGetPrivateStaticMethods(self):
        """
        Test ReflectionInstance.getPrivateStaticMethods() method functionality.

        Verifies that the getPrivateStaticMethods method correctly identifies and
        returns only private static methods (prefixed with double underscores) from
        the wrapped instance, excluding protected and public static methods.

        Assertions
        ----------
        - '__staticMethodPrivate' is included in the returned list
        - 'staticMethod' is not included in the returned list
        - '_staticMethodProtected' is not included in the returned list
        """
        reflect = ReflectionInstance(FakeClass())
        private_static_methods = reflect.getPrivateStaticMethods()
        self.assertIn('__staticMethodPrivate', private_static_methods)
        self.assertNotIn('staticMethod', private_static_methods)
        self.assertNotIn('_staticMethodProtected', private_static_methods)

    async def testGetPrivateStaticSyncMethods(self):
        """
        Test ReflectionInstance.getPrivateStaticSyncMethods() method functionality.

        Verifies that the getPrivateStaticSyncMethods method correctly identifies and
        returns only private static synchronous methods (prefixed with double underscores)
        from the wrapped instance, excluding public and protected static methods.

        Assertions
        ----------
        - '__staticMethodPrivate' is included in the returned list
        - 'staticMethod' is not included in the returned list
        - '_staticMethodProtected' is not included in the returned list
        """
        reflect = ReflectionInstance(FakeClass())
        private_static_sync_methods = reflect.getPrivateStaticSyncMethods()
        self.assertIn('__staticMethodPrivate', private_static_sync_methods)
        self.assertNotIn('staticMethod', private_static_sync_methods)
        self.assertNotIn('_staticMethodProtected', private_static_sync_methods)

    async def testGetPrivateStaticAsyncMethods(self):
        """
        Test ReflectionInstance.getPrivateStaticAsyncMethods() method functionality.

        Verifies that the getPrivateStaticAsyncMethods method correctly identifies and
        returns only private static asynchronous methods (prefixed with double underscores)
        from the wrapped instance, excluding public and protected static async methods.

        Assertions
        ----------
        - '__staticAsyncMethodPrivate' is included in the returned list
        - 'staticAsyncMethod' is not included in the returned list
        - '_staticAsyncMethodProtected' is not included in the returned list
        """
        reflect = ReflectionInstance(FakeClass())
        private_static_async_methods = reflect.getPrivateStaticAsyncMethods()
        self.assertIn('__staticAsyncMethodPrivate', private_static_async_methods)
        self.assertNotIn('staticAsyncMethod', private_static_async_methods)
        self.assertNotIn('_staticAsyncMethodProtected', private_static_async_methods)

    async def testGetDunderMethods(self):
        """
        Test ReflectionInstance.getDunderMethods() method functionality.

        Verifies that the getDunderMethods method correctly identifies and returns
        dunder (double underscore) methods from the wrapped instance. Tests the
        detection of special Python methods with double underscore prefix and suffix.

        Assertions
        ----------
        - '__init__' is present in the returned list
        - '__class__' is present in the returned list
        """
        reflect = ReflectionInstance(FakeClass())
        dunder_methods = reflect.getDunderMethods()
        self.assertIn('__init__', dunder_methods)
        self.assertIn('__class__', dunder_methods)

    async def testGetMagicMethods(self):
        """
        Test ReflectionInstance.getMagicMethods() method functionality.

        Verifies that the getMagicMethods method correctly identifies and returns
        magic methods (special Python methods with double underscores) from the
        wrapped instance. Tests the detection of commonly expected magic methods.

        Assertions
        ----------
        - '__init__' is present in the returned list
        - '__class__' is present in the returned list
        """
        reflect = ReflectionInstance(FakeClass())
        magic_methods = reflect.getMagicMethods()
        self.assertIn('__init__', magic_methods)
        self.assertIn('__class__', magic_methods)

    async def testGetProperties(self):
        """
        Test ReflectionInstance.getProperties() method functionality.

        Verifies that the getProperties method correctly identifies and returns all
        properties (computed properties) from the wrapped instance, including public,
        protected, and private properties.

        Assertions
        ----------
        - 'computed_public_property' is present in the returned list
        - '_computed_property_protected' is present in the returned list
        - '__computed_property_private' is present in the returned list
        """
        reflect = ReflectionInstance(FakeClass())
        properties = reflect.getProperties()
        self.assertIn('computed_public_property', properties)
        self.assertIn('_computed_property_protected', properties)
        self.assertIn('__computed_property_private', properties)

    async def testGetPublicProperties(self):
        """
        Test ReflectionInstance.getPublicProperties() method functionality.

        Verifies that the getPublicProperties method correctly identifies and returns
        only public properties from the wrapped instance, excluding protected and
        private properties based on Python naming conventions.

        Assertions
        ----------
        - 'computed_public_property' is included in the returned list
        - '_computed_property_protected' is not included in the returned list
        - '__computed_property_private' is not included in the returned list
        """
        reflect = ReflectionInstance(FakeClass())
        public_properties = reflect.getPublicProperties()
        self.assertIn('computed_public_property', public_properties)
        self.assertNotIn('_computed_property_protected', public_properties)
        self.assertNotIn('__computed_property_private', public_properties)

    async def testGetProtectedProperties(self):
        """
        Test ReflectionInstance.getProtectedProperties() method functionality.

        Verifies that the getProtectedProperties method correctly identifies and returns
        only protected properties (prefixed with single underscore) from the wrapped
        instance, excluding public and private properties.

        Assertions
        ----------
        - '_computed_property_protected' is included in the returned list
        - 'computed_public_property' is not included in the returned list
        - '__computed_property_private' is not included in the returned list
        """
        reflect = ReflectionInstance(FakeClass())
        protected_properties = reflect.getProtectedProperties()
        self.assertIn('_computed_property_protected', protected_properties)
        self.assertNotIn('computed_public_property', protected_properties)
        self.assertNotIn('__computed_property_private', protected_properties)

    async def testGetPrivateProperties(self):
        """
        Test ReflectionInstance.getPrivateProperties() method functionality.

        Verifies that the getPrivateProperties method correctly identifies and returns
        only private properties (prefixed with double underscores) from the wrapped
        instance, excluding public and protected properties.

        Assertions
        ----------
        - '__computed_property_private' is included in the returned list
        - 'computed_public_property' is not included in the returned list
        - '_computed_property_protected' is not included in the returned list
        """
        reflect = ReflectionInstance(FakeClass())
        private_properties = reflect.getPrivateProperties()
        self.assertIn('__computed_property_private', private_properties)
        self.assertNotIn('computed_public_property', private_properties)
        self.assertNotIn('_computed_property_protected', private_properties)

    async def testGetProperty(self):
        """
        Test ReflectionInstance.getProperty() method functionality.

        Verifies that the getProperty method correctly retrieves the value of a
        computed property from the wrapped instance. Tests property value access
        through reflection and compares with direct property access.

        Assertions
        ----------
        - Property value retrieved through reflection equals direct property access value
        """
        reflect = ReflectionInstance(FakeClass())
        value = reflect.getProperty('computed_public_property')
        self.assertEqual(value, FakeClass().computed_public_property)

    async def testGetPropertySignature(self):
        """
        Test ReflectionInstance.getPropertySignature() method functionality.

        Verifies that the getPropertySignature method correctly retrieves the
        signature of a specified property from the wrapped instance. Tests
        property signature inspection and string representation.

        Assertions
        ----------
        - Signature of 'computed_public_property' equals '(self) -> str'
        """
        reflect = ReflectionInstance(FakeClass())
        signature = reflect.getPropertySignature('computed_public_property')
        self.assertEqual(str(signature), '(self) -> str')

    async def testGetPropertyDocstring(self):
        """
        Test ReflectionInstance.getPropertyDocstring() method functionality.

        Verifies that the getPropertyDocstring method correctly retrieves the
        docstring for a specified property from the wrapped instance. Tests
        property documentation extraction.

        Assertions
        ----------
        - Docstring for 'computed_public_property' contains 'Returns a string indicating this is a public'
        """
        reflect = ReflectionInstance(FakeClass())
        docstring = reflect.getPropertyDocstring('computed_public_property')
        self.assertIn('Returns a string indicating this is a public', docstring)

    async def testGetConstructorDependencies(self):
        """
        Test ReflectionInstance.getConstructorDependencies() method functionality.

        Verifies that the getConstructorDependencies method returns an instance
        of ClassDependency containing the constructor dependencies of the wrapped
        instance's class. Tests dependency analysis for class constructors.

        Assertions
        ----------
        - Returned value is an instance of ClassDependency
        """
        reflect = ReflectionInstance(FakeClass())
        dependencies = reflect.getConstructorDependencies()
        self.assertIsInstance(dependencies, ClassDependency)

    async def testGetMethodDependencies(self):
        """
        Test ReflectionInstance.getMethodDependencies() method functionality.

        Verifies that the getMethodDependencies method correctly resolves the
        dependencies of a specified method from the wrapped instance. Tests
        method parameter type analysis and dependency resolution.

        Assertions
        ----------
        - 'x' parameter is present in resolved dependencies
        - 'y' parameter is present in resolved dependencies
        - Both parameters are identified as int type with correct metadata
        - No unresolved dependencies exist
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