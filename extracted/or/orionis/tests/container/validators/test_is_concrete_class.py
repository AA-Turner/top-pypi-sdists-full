from abc import ABC, abstractmethod
from orionis.container.validators.is_concrete_class import IsConcreteClass
from orionis.container.exceptions.type import OrionisContainerTypeError
from orionis.test.cases.asynchronous import AsyncTestCase

class TestIsConcreteClass(AsyncTestCase):

    async def testValidConcreteClasses(self) -> None:
        """
        Test that validation passes for valid concrete classes.

        This test verifies that the `IsConcreteClass` validator does not raise an exception
        when provided with classes that are concrete (i.e., not abstract and fully implemented).

        Parameters
        ----------
        self : TestIsConcreteClass
            The test case instance.

        Returns
        -------
        None
            This method does not return anything. It asserts that no exception is raised for valid concrete classes.
        """
        class SimpleClass:
            pass  # A basic concrete class with no methods

        class ClassWithInit:
            def __init__(self, value):
                self.value = value  # Concrete class with an initializer

        # These should not raise exceptions since both are concrete classes
        IsConcreteClass(SimpleClass, "singleton")
        IsConcreteClass(ClassWithInit, "transient")

    async def testAbstractClasses(self) -> None:
        """
        Test that validation fails for abstract classes.

        This test ensures that the `IsConcreteClass` validator raises an `OrionisContainerTypeError`
        when provided with an abstract class.

        Parameters
        ----------
        self : TestIsConcreteClass
            The test case instance.

        Returns
        -------
        None
            This method does not return anything. It asserts that an exception is raised for abstract classes.
        """
        class AbstractBase(ABC):
            @abstractmethod
            def abstract_method(self):
                pass  # Abstract method, making this class abstract

        # Should raise an exception because AbstractBase is abstract
        with self.assertRaises(OrionisContainerTypeError) as context:
            IsConcreteClass(AbstractBase, "scoped")
        self.assertIn("Unexpected error registering scoped service", str(context.exception))

    async def testNonClassTypes(self) -> None:
        """
        Test that validation fails for non-class types.

        This test checks that the `IsConcreteClass` validator raises an `OrionisContainerTypeError`
        when provided with values that are not classes (e.g., integers, strings, functions).

        Parameters
        ----------
        self : TestIsConcreteClass
            The test case instance.

        Returns
        -------
        None
            This method does not return anything. It asserts that an exception is raised for non-class types.
        """
        # Should raise an exception for integer input
        with self.assertRaises(OrionisContainerTypeError) as context:
            IsConcreteClass(42, "singleton")
        self.assertIn("Unexpected error registering singleton service", str(context.exception))

        # Should raise an exception for string input
        with self.assertRaises(OrionisContainerTypeError) as context:
            IsConcreteClass("string", "scoped")
        self.assertIn("Unexpected error registering scoped service", str(context.exception))

        # Should raise an exception for function input
        with self.assertRaises(OrionisContainerTypeError) as context:
            IsConcreteClass(lambda x: x, "transient")
        self.assertIn("Unexpected error registering transient service", str(context.exception))

    async def testInheritedConcreteClasses(self) -> None:
        """
        Test that validation passes for concrete classes that inherit from abstract classes.

        This test verifies that the `IsConcreteClass` validator does not raise an exception
        for classes that inherit from abstract base classes but implement all abstract methods,
        making them concrete.

        Parameters
        ----------
        self : TestIsConcreteClass
            The test case instance.

        Returns
        -------
        None
            This method does not return anything. It asserts that no exception is raised for concrete subclasses.
        """
        class AbstractBase(ABC):
            @abstractmethod
            def abstract_method(self):
                pass  # Abstract method

        class ConcreteImplementation(AbstractBase):
            def abstract_method(self):
                return "Implemented"  # Implements all abstract methods

        # Should not raise an exception since all abstract methods are implemented
        IsConcreteClass(ConcreteImplementation, "singleton")

    async def testPartialImplementations(self) -> None:
        """
        Test that validation fails for classes that don't implement all abstract methods.

        This test ensures that the `IsConcreteClass` validator raises an `OrionisContainerTypeError`
        when a class inherits from an abstract base class but does not implement all required abstract methods.

        Parameters
        ----------
        self : TestIsConcreteClass
            The test case instance.

        Returns
        -------
        None
            This method does not return anything. It asserts that an exception is raised for partial implementations.
        """
        class AbstractBase(ABC):
            @abstractmethod
            def method1(self):
                pass

            @abstractmethod
            def method2(self):
                pass

        class PartialImplementation(AbstractBase):
            def method1(self):
                return "Implemented"  # Only one abstract method is implemented

            # method2 is not implemented, so this class remains abstract

        # Should raise an exception since not all abstract methods are implemented
        with self.assertRaises(OrionisContainerTypeError) as context:
            IsConcreteClass(PartialImplementation, "scoped")
        self.assertIn("Unexpected error registering scoped service", str(context.exception))
