from abc import ABC, abstractmethod
from orionis.container.validators.is_instance import IsInstance
from orionis.container.exceptions.type import OrionisContainerTypeError
from orionis.test.cases.asynchronous import AsyncTestCase

class TestIsInstance(AsyncTestCase):

    async def testValidInstances(self) -> None:
        """
        Validate that IsInstance accepts valid object instances.

        This test checks that IsInstance does not raise an exception when provided with
        instances of user-defined classes, including those with and without an __init__ method.

        Returns
        -------
        None
            This method does not return any value.
        """
        # Custom class instance
        class SimpleClass:
            pass

        # Class with __init__ method
        class ClassWithInit:
            def __init__(self, value):
                self.value = value

        # Should not raise an exception for valid instances
        IsInstance(SimpleClass())
        IsInstance(ClassWithInit(42))

    async def testInvalidClasses(self) -> None:
        """
        Ensure IsInstance raises an error when provided with class objects instead of instances.

        This test verifies that passing class types (rather than instances) to IsInstance
        results in an OrionisContainerTypeError.

        Returns
        -------
        None
            This method does not return any value.
        """
        # Passing built-in type should raise an error
        with self.assertRaises(OrionisContainerTypeError) as context:
            IsInstance(str)
        self.assertIn("Error registering instance", str(context.exception))

        # Passing user-defined class should raise an error
        class TestClass:
            pass

        with self.assertRaises(OrionisContainerTypeError) as context:
            IsInstance(TestClass)
        self.assertIn("Error registering instance", str(context.exception))

    async def testAbstractClasses(self) -> None:
        """
        Test IsInstance behavior with abstract classes and their concrete implementations.

        This test ensures that abstract classes are not accepted as valid instances,
        but instances of concrete subclasses are accepted.

        Returns
        -------
        None
            This method does not return any value.
        """
        # Define an abstract base class
        class AbstractBase(ABC):
            @abstractmethod
            def abstract_method(self):
                pass

        # Concrete implementation of the abstract base
        class ConcreteImplementation(AbstractBase):
            def abstract_method(self):
                return "Implemented"

        # Abstract class should raise an error
        with self.assertRaises(OrionisContainerTypeError) as context:
            IsInstance(AbstractBase)
        self.assertIn("Error registering instance", str(context.exception))

        # Instance of concrete implementation should not raise an error
        IsInstance(ConcreteImplementation())

    async def testTypeObjects(self) -> None:
        """
        Verify that IsInstance raises errors for type objects.

        This test checks that passing type objects such as `type`, `int`, or `list`
        to IsInstance results in an OrionisContainerTypeError.

        Returns
        -------
        None
            This method does not return any value.
        """
        # Should raise error for built-in type objects
        with self.assertRaises(OrionisContainerTypeError):
            IsInstance(type)

        with self.assertRaises(OrionisContainerTypeError):
            IsInstance(int)

        with self.assertRaises(OrionisContainerTypeError):
            IsInstance(list)

    async def testNoneValue(self) -> None:
        """
        Test IsInstance validation with None value.

        This test verifies that passing None to IsInstance raises an OrionisContainerTypeError,
        even though None is a valid instance in Python.

        Returns
        -------
        None
            This method does not return any value.
        """
        # Should raise error for None value
        with self.assertRaises(OrionisContainerTypeError):
            IsInstance(None)

    async def testCallables(self) -> None:
        """
        Test IsInstance validation with callable objects.

        This test checks that passing function objects and lambda functions to IsInstance
        raises an OrionisContainerTypeError, while passing their types also raises an error.

        Returns
        -------
        None
            This method does not return any value.
        """
        # Define a function for testing
        def test_function():
            pass

        # Should raise error for function and lambda instances
        with self.assertRaises(OrionisContainerTypeError):
            IsInstance(test_function)
            IsInstance(lambda x: x * 2)

        # Should raise error for type of function
        with self.assertRaises(OrionisContainerTypeError):
            IsInstance(type(test_function))
