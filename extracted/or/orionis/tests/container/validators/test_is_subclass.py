from abc import ABC
from orionis.container.validators.is_subclass import IsSubclass
from orionis.container.exceptions.exception import OrionisContainerException
from orionis.test.cases.asynchronous import AsyncTestCase

class TestIsSubclass(AsyncTestCase):

    async def testValidSubclass(self) -> None:
        """
        Validate that `IsSubclass` does not raise an exception when the concrete class is a valid subclass of the abstract class.

        Parameters
        ----------
        None

        Returns
        -------
        None
            This method does not return anything. It passes if no exception is raised.

        Notes
        -----
        The test covers direct and indirect subclass relationships.
        """
        # Define an abstract base class
        class AbstractClass(ABC):
            pass

        # Define a concrete class inheriting from AbstractClass
        class ConcreteClass(AbstractClass):
            pass

        # Define a subclass of ConcreteClass
        class SubConcreteClass(ConcreteClass):
            pass

        # These calls should not raise exceptions since subclass relationships are valid
        IsSubclass(AbstractClass, ConcreteClass)
        IsSubclass(AbstractClass, SubConcreteClass)
        IsSubclass(ConcreteClass, SubConcreteClass)

    async def testInvalidSubclass(self) -> None:
        """
        Validate that `IsSubclass` raises `OrionisContainerException` when the concrete class is not a subclass of the abstract class.

        Parameters
        ----------
        None

        Returns
        -------
        None
            This method does not return anything. It passes if the expected exception is raised.

        Notes
        -----
        The test covers cases where classes are unrelated or the inheritance direction is incorrect.
        """
        # Define two unrelated abstract base classes
        class AbstractClass1(ABC):
            pass

        class AbstractClass2(ABC):
            pass

        # Define concrete classes inheriting from each abstract class
        class ConcreteClass1(AbstractClass1):
            pass

        class ConcreteClass2(AbstractClass2):
            pass

        # These calls should raise exceptions due to invalid subclass relationships
        with self.assertRaises(OrionisContainerException) as context:
            IsSubclass(AbstractClass1, AbstractClass2)
        self.assertIn("concrete class must inherit", str(context.exception))

        with self.assertRaises(OrionisContainerException) as context:
            IsSubclass(AbstractClass1, ConcreteClass2)
        self.assertIn("concrete class must inherit", str(context.exception))

        with self.assertRaises(OrionisContainerException) as context:
            IsSubclass(ConcreteClass1, AbstractClass1)
        self.assertIn("concrete class must inherit", str(context.exception))

    async def testSameClass(self) -> None:
        """
        Validate that `IsSubclass` does not raise an exception when the abstract and concrete classes are the same.

        Parameters
        ----------
        None

        Returns
        -------
        None
            This method does not return anything. It passes if no exception is raised.

        Notes
        -----
        In Python, a class is considered a subclass of itself.
        """
        # Define a test class
        class TestClass:
            pass

        # Should not raise since a class is a subclass of itself
        IsSubclass(TestClass, TestClass)

    async def testBuiltinTypes(self) -> None:
        """
        Validate `IsSubclass` behavior with built-in types, ensuring correct subclass relationships and exception raising.

        Parameters
        ----------
        None

        Returns
        -------
        None
            This method does not return anything. It passes if exceptions are raised or not as expected.

        Notes
        -----
        The test covers both valid and invalid subclass relationships among built-in types.
        """
        # Valid subclass relationships for built-in types
        IsSubclass(Exception, ValueError)
        IsSubclass(BaseException, Exception)

        # Invalid subclass relationships should raise exceptions
        with self.assertRaises(OrionisContainerException):
            IsSubclass(ValueError, Exception)

        with self.assertRaises(OrionisContainerException):
            IsSubclass(int, str)

        with self.assertRaises(OrionisContainerException):
            IsSubclass(list, dict)

    async def testNonClassArguments(self) -> None:
        """
        Validate that `IsSubclass` raises `TypeError` when non-class arguments are provided.

        Parameters
        ----------
        None

        Returns
        -------
        None
            This method does not return anything. It passes if `TypeError` is raised for non-class arguments.

        Notes
        -----
        The test covers various non-class types such as None, int, str, list, dict, and function.
        """
        # Define a valid test class
        class TestClass:
            pass

        # List of non-class arguments to test
        non_class_args = [
            None,
            123,
            "string",
            [],
            {},
            lambda x: x
        ]

        # Each non-class argument should raise TypeError when used as either abstract or concrete class
        for arg in non_class_args:
            with self.assertRaises(TypeError):
                IsSubclass(TestClass, arg)

            with self.assertRaises(TypeError):
                IsSubclass(arg, TestClass)
