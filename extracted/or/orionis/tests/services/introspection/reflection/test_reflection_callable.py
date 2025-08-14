from orionis.services.introspection.callables.reflection import ReflectionCallable
from orionis.services.introspection.dependencies.entities.resolve_argument import ResolveArguments
from orionis.test.cases.asynchronous import AsyncTestCase
from orionis.services.introspection.exceptions import ReflectionTypeError

class TestReflectionCallable(AsyncTestCase):

    async def testInitValidFunction(self):
        """
        Test initialization of ReflectionCallable with a valid function.

        Validates that a ReflectionCallable instance can be created with a standard function
        and that the stored callable matches the original function.

        Returns
        -------
        None
        """
        def sample_function(a, b=2):
            """Sample docstring."""
            return a + b
        rc = ReflectionCallable(sample_function)
        self.assertEqual(rc.getCallable(), sample_function)

    async def testInitInvalid(self):
        """
        Test initialization of ReflectionCallable with an invalid argument.

        Ensures that passing a non-callable object (e.g., an integer) to ReflectionCallable
        raises a ReflectionTypeError.

        Returns
        -------
        None
        """
        with self.assertRaises(ReflectionTypeError):
            ReflectionCallable(123)

    async def testGetName(self):
        """
        Test retrieval of the function name from ReflectionCallable.

        Checks that the getName() method returns the correct name of the wrapped function.

        Returns
        -------
        None
        """
        def sample_function(a, b=2):
            """Sample docstring."""
            return a + b
        rc = ReflectionCallable(sample_function)
        self.assertEqual(rc.getName(), "sample_function")

    async def testGetModuleName(self):
        """
        Test retrieval of the module name from ReflectionCallable.

        Verifies that getModuleName() returns the module name where the function is defined.

        Returns
        -------
        None
        """
        def sample_function(a, b=2):
            """Sample docstring."""
            return a + b
        rc = ReflectionCallable(sample_function)
        self.assertEqual(rc.getModuleName(), sample_function.__module__)

    async def testGetModuleWithCallableName(self):
        """
        Test retrieval of the fully qualified name from ReflectionCallable.

        Ensures that getModuleWithCallableName() returns the module and function name
        in the format "<module>.<function_name>".

        Returns
        -------
        None
        """
        def sample_function(a, b=2):
            """Sample docstring."""
            return a + b
        rc = ReflectionCallable(sample_function)
        expected = f"{sample_function.__module__}.sample_function"
        self.assertEqual(rc.getModuleWithCallableName(), expected)

    async def testGetDocstring(self):
        """
        Test retrieval of the docstring from ReflectionCallable.

        Confirms that getDocstring() returns the docstring of the wrapped function.

        Returns
        -------
        None
        """
        def sample_function(a, b=2):
            """Sample docstring."""
            return a + b
        rc = ReflectionCallable(sample_function)
        self.assertIn("Sample docstring", rc.getDocstring())

    async def testGetSourceCode(self):
        """
        Test retrieval of source code from ReflectionCallable.

        Checks that getSourceCode() returns the source code of the wrapped function,
        and that the code contains the function definition.

        Returns
        -------
        None
        """
        def sample_function(a, b=2):
            """Sample docstring."""
            return a + b
        rc = ReflectionCallable(sample_function)
        code = rc.getSourceCode()
        self.assertIn("def sample_function", code)

    async def testGetSourceCodeError(self):
        """
        Test error handling when retrieving source code from a built-in function.

        Ensures that getSourceCode() raises a ReflectionTypeError when called on a
        built-in function (e.g., len) that lacks accessible source code.

        Returns
        -------
        None
        """
        with self.assertRaises(ReflectionTypeError):
            rc = ReflectionCallable(len)
            rc.getSourceCode()

    async def testGetFile(self):
        """
        Test retrieval of the file path from ReflectionCallable.

        Verifies that getFile() returns the file path of the wrapped function and that
        the path ends with '.py', indicating a Python source file.

        Returns
        -------
        None
        """
        def sample_function(a, b=2):
            """Sample docstring."""
            return a + b
        rc = ReflectionCallable(sample_function)
        file_path = rc.getFile()
        self.assertTrue(file_path.endswith(".py"))

    async def testCallSync(self):
        """
        Test synchronous invocation of the wrapped function using ReflectionCallable.

        Validates that calling the wrapped function with arguments returns the expected result.

        Returns
        -------
        None
        """
        def sample_function(a, b=2):
            """Sample docstring."""
            return a + b
        rc = ReflectionCallable(sample_function)
        self.assertEqual(rc.call(1, 2), 3)

    async def testCallAsync(self):
        """
        Test asynchronous invocation of an async function using ReflectionCallable.

        Ensures that an asynchronous function can be called and awaited, returning the correct result.

        Returns
        -------
        None
        """
        async def sample_async_function(a, b=2):
            """Async docstring."""
            return a + b
        rc = ReflectionCallable(sample_async_function)
        self.assertEqual(await rc.call(1, 2), 3)

    async def testGetDependencies(self):
        """
        Test retrieval of callable dependencies from ReflectionCallable.

        Checks that getDependencies() returns a ResolveArguments object with
        'resolved' and 'unresolved' attributes for the wrapped function.

        Returns
        -------
        None
        """
        def sample_function(a, b=2):
            """Sample docstring."""
            return a + b
        rc = ReflectionCallable(sample_function)
        deps = rc.getDependencies()
        self.assertIsInstance(deps, ResolveArguments)
        self.assertTrue(hasattr(deps, "resolved"))
        self.assertTrue(hasattr(deps, "unresolved"))
