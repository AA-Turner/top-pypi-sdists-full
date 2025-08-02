from abc import ABC, abstractmethod
import unittest.mock
from orionis.container.validators.is_abstract_class import IsAbstractClass
from orionis.container.exceptions.type import OrionisContainerTypeError
from orionis.test.cases.asynchronous import AsyncTestCase

class TestIsAbstractClass(AsyncTestCase):

    async def testValidAbstractClass(self) -> None:
        """
        Validates that the IsAbstractClass validator accepts a valid abstract class.

        This test creates an abstract class using Python's `abc` module and verifies
        that the validator does not raise an exception when provided with a proper abstract class.

        Returns
        -------
        None
            This method does not return anything. It asserts correct behavior via exceptions and mocks.
        """
        # Create an abstract class with an abstract method
        class AbstractBase(ABC):
            @abstractmethod
            def abstract_method(self):
                pass

        # Patch the reflection method to ensure it is called correctly
        with unittest.mock.patch('orionis.services.introspection.abstract.reflection.ReflectionAbstract.ensureIsAbstractClass') as mock_ensure:
            IsAbstractClass(AbstractBase, "singleton")
            # Assert that the reflection method was called with the correct class
            mock_ensure.assert_called_once_with(AbstractBase)

    async def testNonAbstractClass(self) -> None:
        """
        Validates that the IsAbstractClass validator raises an error for non-abstract classes.

        This test provides a concrete class and mocks the reflection method to raise a ValueError,
        ensuring that the validator responds with an OrionisContainerTypeError.

        Returns
        -------
        None
            This method does not return anything. It asserts correct behavior via exceptions and mocks.
        """
        # Define a concrete class with no abstract methods
        class ConcreteClass:
            def some_method(self):
                pass

        # Patch the reflection method to simulate failure for non-abstract classes
        with unittest.mock.patch(
            'orionis.services.introspection.abstract.reflection.ReflectionAbstract.ensureIsAbstractClass',
            side_effect=ValueError("Not an abstract class")
        ) as mock_ensure:
            # Assert that the validator raises the expected error
            with self.assertRaises(OrionisContainerTypeError) as context:
                IsAbstractClass(ConcreteClass, "scoped")

            self.assertIn("Unexpected error registering scoped service", str(context.exception))
            mock_ensure.assert_called_once_with(ConcreteClass)

    async def testWithInheritedAbstractClass(self) -> None:
        """
        Validates that the IsAbstractClass validator accepts classes that inherit from abstract classes and remain abstract.

        This test creates a base abstract class and a derived abstract class, ensuring that the validator
        does not raise an exception when the derived class is still abstract.

        Returns
        -------
        None
            This method does not return anything. It asserts correct behavior via exceptions and mocks.
        """
        # Define a base abstract class
        class BaseAbstract(ABC):
            @abstractmethod
            def method1(self):
                pass

        # Define a derived abstract class that adds another abstract method
        class DerivedAbstract(BaseAbstract):
            @abstractmethod
            def method2(self):
                pass

        # Patch the reflection method to ensure it is called correctly
        with unittest.mock.patch('orionis.services.introspection.abstract.reflection.ReflectionAbstract.ensureIsAbstractClass') as mock_ensure:
            IsAbstractClass(DerivedAbstract, "transient")
            mock_ensure.assert_called_once_with(DerivedAbstract)

    async def testWithConcreteImplementation(self) -> None:
        """
        Validates that the IsAbstractClass validator raises an error for concrete implementations of abstract classes.

        This test creates a concrete class that implements all abstract methods and mocks the reflection method
        to raise a TypeError, ensuring that the validator responds with an OrionisContainerTypeError.

        Returns
        -------
        None
            This method does not return anything. It asserts correct behavior via exceptions and mocks.
        """
        # Define a base abstract class
        class BaseAbstract(ABC):
            @abstractmethod
            def method(self):
                pass

        # Define a concrete class that implements the abstract method
        class ConcreteImplementation(BaseAbstract):
            def method(self):
                return "Implemented"

        # Patch the reflection method to simulate failure for concrete classes
        with unittest.mock.patch(
            'orionis.services.introspection.abstract.reflection.ReflectionAbstract.ensureIsAbstractClass',
            side_effect=TypeError("Not an abstract class")
        ) as mock_ensure:
            # Assert that the validator raises the expected error
            with self.assertRaises(OrionisContainerTypeError) as context:
                IsAbstractClass(ConcreteImplementation, "singleton")

            self.assertIn("Unexpected error registering singleton service", str(context.exception))
            mock_ensure.assert_called_once_with(ConcreteImplementation)

    async def testWithNonClassTypes(self) -> None:
        """
        Validates that the IsAbstractClass validator raises an error for non-class types.

        This test iterates over several primitive and non-class values, mocking the reflection method
        to raise a TypeError, and ensures that the validator responds with an OrionisContainerTypeError.

        Returns
        -------
        None
            This method does not return anything. It asserts correct behavior via exceptions and mocks.
        """
        # Test with various non-class types
        for invalid_value in [1, "string", [], {}, lambda: None]:
            # Patch the reflection method to simulate failure for non-class types
            with unittest.mock.patch(
                'orionis.services.introspection.abstract.reflection.ReflectionAbstract.ensureIsAbstractClass',
                side_effect=TypeError(f"{type(invalid_value)} is not a class")
            ) as mock_ensure:
                # Assert that the validator raises the expected error
                with self.assertRaises(OrionisContainerTypeError):
                    IsAbstractClass(invalid_value, "transient")
