from orionis.services.introspection.callables.reflection import ReflectionCallable
from orionis.services.introspection.dependencies.entities.callable_dependencies import CallableDependency
from orionis.test.cases.asynchronous import AsyncTestCase
from orionis.services.introspection.exceptions import ReflectionTypeError

class TestReflectionCallable(AsyncTestCase):

    async def testInitValidFunction(self):
        """
        Tests that a ReflectionCallable object can be correctly initialized with a valid function.
        Verifies that the callable stored in the ReflectionCallable instance matches the original function.
        """
        def sample_function(a, b=2):
            """Sample docstring."""
            return a + b
        rc = ReflectionCallable(sample_function)
        self.assertEqual(rc.getCallable(), sample_function)

    async def testInitInvalid(self):
        """
        Test that initializing ReflectionCallable with an invalid argument (e.g., an integer)
        raises a ReflectionTypeError.
        """
        with self.assertRaises(ReflectionTypeError):
            ReflectionCallable(123)

    async def testGetName(self):
        """
        Tests that the ReflectionCallable.getName() method correctly returns the name of the provided function.

        This test defines a sample function, wraps it with ReflectionCallable, and asserts that getName()
        returns the function's name as a string.
        """
        def sample_function(a, b=2):
            """Sample docstring."""
            return a + b
        rc = ReflectionCallable(sample_function)
        self.assertEqual(rc.getName(), "sample_function")

    async def testGetModuleName(self):
        """
        Tests that the getModuleName method of ReflectionCallable returns the correct module name
        for a given function. It verifies that the module name returned matches the __module__ attribute
        of the sample function.
        """
        def sample_function(a, b=2):
            """Sample docstring."""
            return a + b
        rc = ReflectionCallable(sample_function)
        self.assertEqual(rc.getModuleName(), sample_function.__module__)

    async def testGetModuleWithCallableName(self):
        """
        Tests that the `getModuleWithCallableName` method of the `ReflectionCallable` class
        correctly returns the fully qualified name of a given callable, including its module
        and function name.

        The test defines a sample function, wraps it with `ReflectionCallable`, and asserts
        that the returned string matches the expected format: "<module>.<function_name>".
        """
        def sample_function(a, b=2):
            """Sample docstring."""
            return a + b
        rc = ReflectionCallable(sample_function)
        expected = f"{sample_function.__module__}.sample_function"
        self.assertEqual(rc.getModuleWithCallableName(), expected)

    async def testGetDocstring(self):
        """
        Tests that the getDocstring method of ReflectionCallable correctly retrieves the docstring from a given function.
        """
        def sample_function(a, b=2):
            """Sample docstring."""
            return a + b
        rc = ReflectionCallable(sample_function)
        self.assertIn("Sample docstring", rc.getDocstring())

    async def testGetSourceCode(self):
        """
        Tests that the getSourceCode method of ReflectionCallable correctly retrieves
        the source code of a given function. Verifies that the returned code contains
        the function definition for 'sample_function'.
        """
        def sample_function(a, b=2):
            """Sample docstring."""
            return a + b
        rc = ReflectionCallable(sample_function)
        code = rc.getSourceCode()
        self.assertIn("def sample_function", code)

    async def testGetSourceCodeError(self):
        """
        Test that ReflectionCallable.getSourceCode() raises a ReflectionTypeError
        when called on a built-in function (e.g., len) that does not have accessible source code.
        """
        with self.assertRaises(ReflectionTypeError):
            rc = ReflectionCallable(len)
            rc.getSourceCode()

    async def testGetFile(self):
        """
        Tests that the getFile() method of the ReflectionCallable class returns the correct file path
        for a given callable. Verifies that the returned file path ends with '.py', indicating it is a
        Python source file.
        """
        def sample_function(a, b=2):
            """Sample docstring."""
            return a + b
        rc = ReflectionCallable(sample_function)
        file_path = rc.getFile()
        self.assertTrue(file_path.endswith(".py"))

    async def testCallSync(self):
        """
        Tests the synchronous call functionality of the ReflectionCallable class.

        This test defines a sample function with one required and one optional argument,
        wraps it with ReflectionCallable, and asserts that calling it with specific arguments
        returns the expected result.
        """
        def sample_function(a, b=2):
            """Sample docstring."""
            return a + b
        rc = ReflectionCallable(sample_function)
        self.assertEqual(rc.call(1, 2), 3)

    async def testCallAsync(self):
        """
        Tests the ReflectionCallable's ability to call an asynchronous function synchronously.

        This test defines an asynchronous function `sample_async_function` that takes two arguments and returns their sum.
        It then wraps this function with `ReflectionCallable` and asserts that calling it with arguments (1, 2) returns 3.
        """
        async def sample_async_function(a, b=2):
            """Async docstring."""
            return a + b
        rc = ReflectionCallable(sample_async_function)
        self.assertEqual(await rc.call(1, 2), 3)

    async def testGetDependencies(self):
        """
        Tests the getDependencies method of the ReflectionCallable class.

        This test defines a sample function with one required and one default argument,
        creates a ReflectionCallable instance for it, and retrieves its dependencies.
        It then asserts that the returned dependencies object has both 'resolved' and
        'unresolved' attributes.
        """
        def sample_function(a, b=2):
            """Sample docstring."""
            return a + b
        rc = ReflectionCallable(sample_function)
        deps = rc.getDependencies()
        self.assertIsInstance(deps, CallableDependency)
        self.assertTrue(hasattr(deps, "resolved"))
        self.assertTrue(hasattr(deps, "unresolved"))
