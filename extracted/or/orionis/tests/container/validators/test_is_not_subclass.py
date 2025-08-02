from abc import ABC
from orionis.container.validators.is_not_subclass import IsNotSubclass
from orionis.container.exceptions.exception import OrionisContainerException
from orionis.test.cases.asynchronous import AsyncTestCase

class TestIsNotSubclass(AsyncTestCase):

    async def testValidNonSubclass(self) -> None:
        """
        Validate that `IsNotSubclass` does not raise an exception when the second argument
        is not a subclass of the first argument.

        This test covers various scenarios including unrelated abstract classes, concrete classes,
        and built-in types to ensure that only true subclass relationships trigger validation errors.

        Parameters
        ----------
        self : TestIsNotSubclass
            The test case instance.

        Returns
        -------
        None
            This method does not return any value.

        Raises
        ------
        AssertionError
            If `IsNotSubclass` raises an exception for valid non-subclass relationships.
        """
        # Define abstract base classes
        class AbstractClass1(ABC):
            pass

        class AbstractClass2(ABC):
            pass

        # Define concrete classes inheriting from abstract base classes
        class ConcreteClass1(AbstractClass1):
            pass

        class ConcreteClass2(AbstractClass2):
            pass

        # These calls should NOT raise exceptions since there is no subclass relationship
        IsNotSubclass(AbstractClass1, AbstractClass2)  # Unrelated abstract classes
        IsNotSubclass(AbstractClass1, ConcreteClass2)  # Unrelated concrete class
        IsNotSubclass(ConcreteClass1, AbstractClass1)  # Concrete is not subclass of unrelated abstract
        IsNotSubclass(int, str)                        # Built-in types, no subclass relationship
        IsNotSubclass(list, dict)                      # Built-in types, no subclass relationship
