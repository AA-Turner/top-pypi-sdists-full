from orionis.container.validators.is_callable import IsCallable
from orionis.container.exceptions.type import OrionisContainerTypeError
from orionis.test.cases.asynchronous import AsyncTestCase

class TestIsCallable(AsyncTestCase):

    async def testValidCallables(self) -> None:
        """
        Validate that IsCallable accepts valid callable objects without raising exceptions.

        This test covers various types of callables, including functions, classes with
        a __call__ method, lambda functions, and built-in functions.

        Returns
        -------
        None
            This method does not return any value. It asserts that no exception is raised
            for valid callables.
        """
        def simple_function():
            pass  # Simple user-defined function

        class ClassWithCall:
            def __call__(self):
                pass  # Class instance with __call__ method

        lambda_func = lambda x: x  # Lambda function

        # These should not raise exceptions as they are all callable
        IsCallable(simple_function)
        IsCallable(ClassWithCall())
        IsCallable(lambda_func)
        IsCallable(len)
        IsCallable(print)

    async def testNonCallables(self) -> None:
        """
        Ensure that IsCallable raises OrionisContainerTypeError for non-callable objects.

        This test iterates over a list of non-callable objects and asserts that the
        expected exception is raised with the correct error message.

        Returns
        -------
        None
            This method does not return any value. It asserts that exceptions are raised
            for non-callable objects.
        """
        non_callables = [
            42,                # Integer
            "string",          # String
            [1, 2, 3],         # List
            {"key": "value"},  # Dictionary
            None,              # NoneType
            True,              # Boolean
            (1, 2, 3)          # Tuple
        ]

        for value in non_callables:
            # Assert that IsCallable raises the expected exception for non-callables
            with self.assertRaises(OrionisContainerTypeError) as context:
                IsCallable(value)
            expected_message = f"Expected a callable type, but got {type(value).__name__} instead."
            self.assertEqual(str(context.exception), expected_message)

    async def testClassesAsCallables(self) -> None:
        """
        Verify that classes themselves are considered callable by IsCallable.

        Classes are callable because they can be instantiated. This test ensures
        that passing a class to IsCallable does not raise an exception.

        Returns
        -------
        None
            This method does not return any value. It asserts that no exception is raised
            for classes.
        """
        class SimpleClass:
            pass  # Simple class definition

        # Should not raise an exception since classes are callable
        IsCallable(SimpleClass)

    async def testBuiltinFunctions(self) -> None:
        """
        Confirm that built-in functions are recognized as callable by IsCallable.

        This test checks several built-in functions to ensure they are accepted
        without raising exceptions.

        Returns
        -------
        None
            This method does not return any value. It asserts that no exception is raised
            for built-in functions.
        """
        # These built-in functions should not raise exceptions
        IsCallable(sum)
        IsCallable(map)
        IsCallable(filter)
        IsCallable(sorted)
