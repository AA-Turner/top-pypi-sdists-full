from abc import ABC, abstractmethod
import asyncio

from tests.container.mocks.mock_simple_classes import ICar

def ejemplo(x:int = 3, y:int = 2):
    return x + y

class AbstractFakeClass(ABC):

    """
    AbstractFakeClass es una clase abstracta basada en FakeClass, diseñada para simular atributos y métodos de diferentes niveles de visibilidad.
    Define métodos y propiedades abstractas para ser implementadas por subclases concretas.
    """

    # Atributos de clase
    public_attr: int = 42
    dynamic_attr = None
    _protected_attr: str = "protected"
    __private_attr: str = "private"
    __dd__: str = "dunder_value"

    @property
    @abstractmethod
    def computed_public_property(self) -> str:
        """
        Computes and returns the value of a public property.

        Returns:
            str: The computed value of the public property.
        """
        pass

    @property
    @abstractmethod
    def _computed_property_protected(self) -> str:
        """
        A protected method intended to compute and return a string property.

        Returns:
            str: The computed property as a string.
        """
        pass

    def __init__(self) -> None:
        self.public_attr = 42
        self.dynamic_attr = None
        self._protected_attr = "protected"
        self.__private_attr = "private"
        self.__dd__ = "dunder_value"

    # Métodos de instancia
    @abstractmethod
    def instanceSyncMethod(self, x: int, y: int) -> int:
        pass

    @abstractmethod
    async def instanceAsyncMethod(self, x: int, y: int) -> int:
        pass

    @abstractmethod
    def _protectedsyncMethod(self, x: int, y: int) -> int:
        pass

    @abstractmethod
    async def _protectedAsyncMethod(self, x: int, y: int) -> int:
        pass

    # Métodos de clase
    @classmethod
    @abstractmethod
    def classSyncMethod(cls, x: int, y: int) -> int:
        pass

    @classmethod
    @abstractmethod
    async def classAsyncMethod(cls, x: int, y: int) -> int:
        pass

    @classmethod
    @abstractmethod
    def _classMethodProtected(cls, x: int, y: int) -> int:
        pass

    @classmethod
    @abstractmethod
    async def _classAsyncMethodProtected(cls, x: int, y: int) -> int:
        pass

    # Métodos estáticos
    @staticmethod
    @abstractmethod
    def staticMethod(text: str) -> str:
        pass

    @staticmethod
    @abstractmethod
    async def staticAsyncMethod(text: str) -> str:
        pass

    @staticmethod
    @abstractmethod
    def _staticMethodProtected(text: str) -> str:
        pass

    @staticmethod
    @abstractmethod
    async def _staticAsyncMethodProtected(text: str) -> str:
        pass

class FakeClass(AbstractFakeClass):
    """
    FakeClass is a test double class designed to simulate a variety of attribute and method visibilities for inspection and testing purposes.
    This class provides:
    - Public, protected, and private class-level and instance-level attributes.
    - Public, protected, and private properties.
    - Synchronous and asynchronous instance methods with varying visibilities.
    - Synchronous and asynchronous class methods with varying visibilities.
    - Synchronous and asynchronous static methods with varying visibilities.
        public_attr (int): A public class and instance attribute set to 42.
        dynamic_attr: A public attribute initialized to None, can be set dynamically.
        _protected_attr (str): A protected class and instance attribute set to "protected".
        __private_attr (str): A private class and instance attribute set to "private".
    Properties:
        computed_public_property (str): Returns "public property".
        _computed_property_protected (str): Returns "protected property".
        __computed_property_private (str): Returns "private property".
    Methods:
        instanceSyncMethod(x: int, y: int) -> int:
        instanceAsyncMethod(x: int, y: int) -> int:
        _protectedsyncMethod(x: int, y: int) -> int:
            Protected synchronous addition method.
        _protectedAsyncMethod(x: int, y: int) -> int:
            Protected asynchronous addition method.
        __privateSyncMethod(x: int, y: int) -> int:
            Private synchronous addition method.
        __privateAsyncMethod(x: int, y: int) -> int:
            Private asynchronous addition method.
    Class Methods:
        classSyncMethod(x: int, y: int) -> int:
        classAsyncMethod(x: int, y: int) -> int:
        _classMethodProtected(x: int, y: int) -> int:
            Protected synchronous class addition method.
        _classAsyncMethodProtected(x: int, y: int) -> int:
            Protected asynchronous class addition method.
        __classMethodPrivate(x: int, y: int) -> int:
            Private synchronous class addition method.
        __classAsyncMethodPrivate(x: int, y: int) -> int:
            Private asynchronous class addition method.
    Static Methods:
        staticMethod(text: str) -> str:
            Synchronously converts the input text to uppercase.
        staticAsyncMethod(text: str) -> str:
            Asynchronously converts the input text to uppercase.
        _staticMethodProtected(text: str) -> str:
            Protected synchronous static method to uppercase text.
        _staticAsyncMethodProtected(text: str) -> str:
            Protected asynchronous static method to uppercase text.
        __staticMethodPrivate(text: str) -> str:
            Private synchronous static method to uppercase text.
        __staticAsyncMethodPrivate(text: str) -> str:
            Private asynchronous static method to uppercase text.
    Note:
        This class is intended for testing and inspection of attribute and method visibility, including Python's name mangling for private members.
    """

    # Class-level attribute (Public)
    public_attr: int = 42
    dynamic_attr = None

    # Class-level attribute (Protected)
    _protected_attr: str = "protected"

    # Class-level attribute (Private)
    __private_attr: str = "private"
    __dd__: str = "dunder_value"

    @property
    def computed_public_property(self) -> str:
        """
        Returns the string "public" as a computed property.

        Returns:
            str: The string "public".
        """
        return f"public property"

    @property
    def _computed_property_protected(self) -> str:
        """
        Returns a string indicating that this is a protected computed property.

        Returns:
            str: The string "protected".
        """
        """A computed property."""
        return f"protected property"

    @property
    def __computed_property_private(self) -> str:
        """
        Returns the string "private".

        This is a private computed property method, typically used for internal logic or testing purposes.

        Returns:
            str: The string "private".
        """
        return f"private property"

    def __init__(self, carro:ICar, *, edad:int=10, callback:ejemplo) -> None:
        """
        Initializes the instance with various attributes for testing attribute visibility.

        Attributes:
            public_attr (int): A public attribute set to 42.
            _protected_attr (str): A protected attribute set to "protected".
            __private_attr (str): A private attribute set to "private".
            dynamic_attr: An attribute initialized to None, can be set dynamically.
            __dd__ (str): A dunder (double underscore) attribute set to "dunder_value".
        """

        # Initialize attributes (Publics)
        self.public_attr = 42
        self.dynamic_attr = None

        # Initialize attributes (Protected)
        self._protected_attr = "protected"

        # Initialize attributes (Private)
        self.__private_attr = "private"
        self.__dd__ = "dunder_value"

    def instanceSyncMethod(self, x: int, y: int) -> int:
        """
        Synchronously adds two integers and returns the result.

        Args:
            x (int): The first integer to add.
            y (int): The second integer to add.

        Returns:
            int: The sum of x and y.
        """
        return x + y

    async def instanceAsyncMethod(self, x: int, y: int) -> int:
        """
        Asynchronously adds two integers and returns the result.

        Args:
            x (int): The first integer to add.
            y (int): The second integer to add.

        Returns:
            int: The sum of x and y.
        """
        await asyncio.sleep(0.1)
        return x + y

    def _protectedsyncMethod(self, x: int, y: int) -> int:
        """
        Synchronously adds two integers and returns the result (protected method).

        Args:
            x (int): The first integer to add.
            y (int): The second integer to add.

        Returns:
            int: The sum of x and y.
        """
        return x + y

    async def _protectedAsyncMethod(self, x: int, y: int) -> int:
        """
        Asynchronously adds two integers and returns the result (protected method).

        Args:
            x (int): The first integer to add.
            y (int): The second integer to add.

        Returns:
            int: The sum of x and y.
        """
        await asyncio.sleep(0.1)
        return x + y

    def __privateSyncMethod(self, x: int, y: int) -> int:
        """
        Synchronously adds two integers and returns the result (private method).

        Args:
            x (int): The first integer to add.
            y (int): The second integer to add.

        Returns:
            int: The sum of x and y.
        """
        return x + y

    async def __privateAsyncMethod(self, x: int, y: int) -> int:
        """
        Asynchronously adds two integers and returns the result (private method).

        Args:
            x (int): The first integer to add.
            y (int): The second integer to add.

        Returns:
            int: The sum of x and y.
        """
        await asyncio.sleep(0.1)
        return x + y

    @classmethod
    def classSyncMethod(cls, x: int, y: int) -> int:
        """
        Synchronously adds two integers and returns the result (class method).

        Args:
            x (int): The first integer to add.
            y (int): The second integer to add.

        Returns:
            int: The sum of x and y.
        """
        return x + y

    @classmethod
    async def classAsyncMethod(cls, x: int, y: int) -> int:
        """
        Asynchronously adds two integers and returns the result (class method).

        Args:
            x (int): The first integer to add.
            y (int): The second integer to add.

        Returns:
            int: The sum of x and y.
        """
        await asyncio.sleep(0.1)
        return x + y

    @classmethod
    def _classMethodProtected(cls, x: int, y: int) -> int:
        """
        Synchronously adds two integers and returns the result (protected class method).

        Args:
            x (int): The first integer to add.
            y (int): The second integer to add.

        Returns:
            int: The sum of x and y.
        """
        return x + y

    @classmethod
    async def _classAsyncMethodProtected(cls, x: int, y: int) -> int:
        """
        Asynchronously adds two integers and returns the result (protected class method).

        Args:
            x (int): The first integer to add.
            y (int): The second integer to add.

        Returns:
            int: The sum of x and y.
        """
        await asyncio.sleep(0.1)
        return x + y

    @classmethod
    def __classMethodPrivate(cls, x: int, y: int) -> int:
        """
        Synchronously adds two integers and returns the result (private class method).

        Args:
            x (int): The first integer to add.
            y (int): The second integer to add.

        Returns:
            int: The sum of x and y.
        """
        return x + y

    @classmethod
    async def __classAsyncMethodPrivate(cls, x: int, y: int) -> int:
        """
        Asynchronously adds two integers and returns the result (private class method).

        Args:
            x (int): The first integer to add.
            y (int): The second integer to add.

        Returns:
            int: The sum of x and y.
        """
        await asyncio.sleep(0.1)
        return x + y

    @staticmethod
    def staticMethod(text: str) -> str:
        """
        Synchronously converts the input text to uppercase (static method).

        Args:
            text (str): The input string.

        Returns:
            str: The uppercase version of the input string.
        """
        return text.upper()

    @staticmethod
    async def staticAsyncMethod(text: str) -> str:
        """
        Asynchronously converts the input text to uppercase (static method).

        Args:
            text (str): The input string.

        Returns:
            str: The uppercase version of the input string.
        """
        await asyncio.sleep(0.1)
        return text.upper()

    @staticmethod
    def _staticMethodProtected(text: str) -> str:
        """
        Synchronously converts the input text to uppercase (protected static method).

        Args:
            text (str): The input string.

        Returns:
            str: The uppercase version of the input string.
        """
        return text.upper()

    @staticmethod
    async def _staticAsyncMethodProtected(text: str) -> str:
        """
        Asynchronously converts the input text to uppercase (protected static method).

        Args:
            text (str): The input string.

        Returns:
            str: The uppercase version of the input string.
        """
        await asyncio.sleep(0.1)
        return text.upper()

    @staticmethod
    def __staticMethodPrivate(text: str) -> str:
        """
        Synchronously converts the input text to uppercase (private static method).

        Args:
            text (str): The input string.

        Returns:
            str: The uppercase version of the input string.
        """
        return text.upper()

    @staticmethod
    async def __staticAsyncMethodPrivate(text: str) -> str:
        """
        Asynchronously converts the input text to uppercase (private static method).

        Args:
            text (str): The input string.

        Returns:
            str: The uppercase version of the input string.
        """
        await asyncio.sleep(0.1)
        return text.upper()

