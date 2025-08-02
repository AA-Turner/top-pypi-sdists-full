from abc import ABC, abstractmethod
from orionis.test.cases.asynchronous import AsyncTestCase
from orionis.container.validators.implements import ImplementsAbstractMethods
from orionis.container.exceptions.exception import OrionisContainerException

class TestImplementsAbstractMethods(AsyncTestCase):

    async def asyncSetUp(self) -> None:
        """
        Set up test fixtures for ImplementsAbstractMethods validator tests.

        This method defines several abstract and concrete classes to be used in the test cases:
        - An abstract base class with two abstract methods.
        - A concrete class that correctly implements all abstract methods.
        - A concrete class that does not implement all abstract methods.
        - A non-abstract base class for negative test cases.

        The defined classes are assigned to instance attributes for use in subsequent tests.

        Returns
        -------
        None
            This method does not return any value.
        """
        # Define an abstract base class with two abstract methods
        class AbstractBase(ABC):
            @abstractmethod
            def abstract_method(self) -> None:
                pass

            @abstractmethod
            def another_abstract_method(self) -> str:
                pass

        # Concrete class that implements all abstract methods
        class ConcreteCorrect(AbstractBase):
            def abstract_method(self) -> None:
                pass

            def another_abstract_method(self) -> str:
                return "implemented"

        # Concrete class that does not implement all abstract methods
        class ConcreteIncomplete(AbstractBase):
            def abstract_method(self) -> None:
                pass

        # Non-abstract base class for negative test cases
        class NonAbstractBase:
            def regular_method(self) -> None:
                pass

        # Assign classes to instance attributes for use in tests
        self.AbstractBase = AbstractBase
        self.ConcreteCorrect = ConcreteCorrect
        self.ConcreteIncomplete = ConcreteIncomplete
        self.NonAbstractBase = NonAbstractBase

    async def testValidImplementation(self) -> None:
        """
        Test that validation passes when all abstract methods are implemented.

        Returns
        -------
        None
            This method does not return any value.
        """
        # Test with class
        ImplementsAbstractMethods(
            abstract=self.AbstractBase,
            concrete=self.ConcreteCorrect
        )

        # Test with instance
        instance = self.ConcreteCorrect()
        ImplementsAbstractMethods(
            abstract=self.AbstractBase,
            instance=instance
        )

    async def testIncompleteImplementation(self) -> None:
        """
        Test that validation fails when not all abstract methods are implemented.

        Returns
        -------
        None
            This method does not return any value.
        """
        # Test with class missing an abstract method
        with self.assertRaises(OrionisContainerException) as context:
            ImplementsAbstractMethods(
                abstract=self.AbstractBase,
                concrete=self.ConcreteIncomplete
            )

        self.assertIn("does not implement the following abstract methods", str(context.exception))
        self.assertIn("another_abstract_method", str(context.exception))

        # Test with instance missing an abstract method
        with self.assertRaises(TypeError):
            ImplementsAbstractMethods(
                abstract=self.AbstractBase,
                instance=self.ConcreteIncomplete()
            )

    async def testMissingAbstractClass(self) -> None:
        """
        Test that validation fails when no abstract class is provided.

        Returns
        -------
        None
            This method does not return any value.
        """
        # Should raise exception if abstract class is not provided
        with self.assertRaises(OrionisContainerException) as context:
            ImplementsAbstractMethods(
                concrete=self.ConcreteCorrect
            )

        self.assertIn("Abstract class must be provided", str(context.exception))

    async def testMissingConcreteImplementation(self) -> None:
        """
        Test that validation fails when neither concrete class nor instance is provided.

        Returns
        -------
        None
            This method does not return any value.
        """
        # Should raise exception if neither concrete nor instance is provided
        with self.assertRaises(OrionisContainerException) as context:
            ImplementsAbstractMethods(
                abstract=self.AbstractBase
            )

        self.assertIn("Either concrete class or instance must be provided", str(context.exception))

    async def testNonAbstractClass(self) -> None:
        """
        Test that validation fails when the provided abstract class has no abstract methods.

        Returns
        -------
        None
            This method does not return any value.
        """
        # Should raise exception if abstract class does not define any abstract methods
        with self.assertRaises(OrionisContainerException) as context:
            ImplementsAbstractMethods(
                abstract=self.NonAbstractBase,
                concrete=self.ConcreteCorrect
            )

        self.assertIn("does not define any abstract methods", str(context.exception))

    async def testRenamedAbstractMethods(self) -> None:
        """
        Test handling of renamed abstract methods with class name prefixes.

        This test verifies that the validator correctly handles cases where abstract methods
        are renamed with class name prefixes in the concrete implementation.

        Returns
        -------
        None
            This method does not return any value.
        """
        # Define an abstract class with a prefixed abstract method
        class AbstractWithPrefix(ABC):
            @abstractmethod
            def _AbstractWithPrefix_method(self) -> None:
                pass

        # Concrete class with a similarly prefixed method
        class ConcreteWithPrefix:
            def _ConcreteWithPrefix_method(self) -> None:
                pass

        # Should pass validation because the method is renamed according to class name
        ImplementsAbstractMethods(
            abstract=AbstractWithPrefix,
            concrete=ConcreteWithPrefix
        )