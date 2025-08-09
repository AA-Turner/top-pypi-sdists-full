from abc import ABC, abstractmethod
import asyncio
from tests.container.mocks.mock_simple_classes import ICar

def ejemplo(x:int = 3, y:int = 2):
    """
    Add two integers together.

    Parameters
    ----------
    x : int, default 3
        First integer operand.
    y : int, default 2
        Second integer operand.

    Returns
    -------
    int
        Sum of x and y.
    """
    return x + y

class AbstractFakeClass(ABC):
    """
    Abstract base class for testing attribute and method visibility patterns.

    This class defines abstract methods and properties with different visibility
    levels (public, protected, private) for testing purposes. It includes
    synchronous and asynchronous methods as instance, class, and static methods.

    Attributes
    ----------
    public_attr : int
        Public class attribute with default value 42.
    dynamic_attr : Any
        Dynamic attribute that can be set at runtime, initially None.
    _protected_attr : str
        Protected class attribute with default value "protected".
    __private_attr : str
        Private class attribute with default value "private".
    __dd__ : str
        Dunder attribute with default value "dunder_value".

    Notes
    -----
    All methods are abstract and must be implemented by concrete subclasses.
    This class serves as a template for testing different method and property
    visibility patterns in Python.
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
        Abstract property that computes and returns a public property value.

        Returns
        -------
        str
            The computed value of the public property.
        """
        pass

    @property
    @abstractmethod
    def _computed_property_protected(self) -> str:
        """
        Abstract protected property that computes and returns a string value.

        Returns
        -------
        str
            The computed property as a string.
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
        """
        Abstract synchronous instance method for integer operations.

        Parameters
        ----------
        x : int
            First integer operand.
        y : int
            Second integer operand.

        Returns
        -------
        int
            Result of the operation.
        """
        pass

    @abstractmethod
    async def instanceAsyncMethod(self, x: int, y: int) -> int:
        """
        Abstract asynchronous instance method for integer operations.

        Parameters
        ----------
        x : int
            First integer operand.
        y : int
            Second integer operand.

        Returns
        -------
        int
            Result of the operation.
        """
        pass

    @abstractmethod
    def _protectedsyncMethod(self, x: int, y: int) -> int:
        """
        Abstract protected synchronous instance method for integer operations.

        Parameters
        ----------
        x : int
            First integer operand.
        y : int
            Second integer operand.

        Returns
        -------
        int
            Result of the operation.
        """
        pass

    @abstractmethod
    async def _protectedAsyncMethod(self, x: int, y: int) -> int:
        """
        Abstract protected asynchronous instance method for integer operations.

        Parameters
        ----------
        x : int
            First integer operand.
        y : int
            Second integer operand.

        Returns
        -------
        int
            Result of the operation.
        """
        pass

    # Métodos de clase
    @classmethod
    @abstractmethod
    def classSyncMethod(cls, x: int, y: int) -> int:
        """
        Abstract synchronous class method for integer operations.

        Parameters
        ----------
        x : int
            First integer operand.
        y : int
            Second integer operand.

        Returns
        -------
        int
            Result of the operation.
        """
        pass

    @classmethod
    @abstractmethod
    async def classAsyncMethod(cls, x: int, y: int) -> int:
        """
        Abstract asynchronous class method for integer operations.

        Parameters
        ----------
        x : int
            First integer operand.
        y : int
            Second integer operand.

        Returns
        -------
        int
            Result of the operation.
        """
        pass

    @classmethod
    @abstractmethod
    def _classMethodProtected(cls, x: int, y: int) -> int:
        """
        Abstract protected synchronous class method for integer operations.

        Parameters
        ----------
        x : int
            First integer operand.
        y : int
            Second integer operand.

        Returns
        -------
        int
            Result of the operation.
        """
        pass

    @classmethod
    @abstractmethod
    async def _classAsyncMethodProtected(cls, x: int, y: int) -> int:
        """
        Abstract protected asynchronous class method for integer operations.

        Parameters
        ----------
        x : int
            First integer operand.
        y : int
            Second integer operand.

        Returns
        -------
        int
            Result of the operation.
        """
        pass

    # Métodos estáticos
    @staticmethod
    @abstractmethod
    def staticMethod(text: str) -> str:
        """
        Abstract static method for text processing.

        Parameters
        ----------
        text : str
            Input text string to process.

        Returns
        -------
        str
            Processed text string.
        """
        pass

    @staticmethod
    @abstractmethod
    async def staticAsyncMethod(text: str) -> str:
        """
        Abstract asynchronous static method for text processing.

        Parameters
        ----------
        text : str
            Input text string to process.

        Returns
        -------
        str
            Processed text string.
        """
        pass

    @staticmethod
    @abstractmethod
    def _staticMethodProtected(text: str) -> str:
        """
        Abstract protected static method for text processing.

        Parameters
        ----------
        text : str
            Input text string to process.

        Returns
        -------
        str
            Processed text string.
        """
        pass

    @staticmethod
    @abstractmethod
    async def _staticAsyncMethodProtected(text: str) -> str:
        """
        Abstract protected asynchronous static method for text processing.

        Parameters
        ----------
        text : str
            Input text string to process.

        Returns
        -------
        str
            Processed text string.
        """
        pass

class FakeClass(AbstractFakeClass):
    """
    Concrete implementation of AbstractFakeClass for testing attribute and method visibility.

    This test double class provides concrete implementations of all abstract methods
    and properties defined in AbstractFakeClass. It demonstrates various visibility
    levels (public, protected, private) for attributes, properties, and methods
    including synchronous and asynchronous variants for instance, class, and static methods.

    Attributes
    ----------
    public_attr : int
        Public attribute accessible from anywhere, default value 42.
    dynamic_attr : Any
        Dynamic attribute that can be set at runtime, initially None.
    _protected_attr : str
        Protected attribute following Python naming convention, default "protected".
    __private_attr : str
        Private attribute using name mangling, default "private".
    __dd__ : str
        Dunder attribute demonstrating double underscore usage, default "dunder_value".

    Notes
    -----
    This class is intended for testing and inspection of Python's attribute and
    method visibility patterns, including name mangling behavior for private members.
    All methods perform simple operations (addition for numeric methods, uppercase
    conversion for string methods) with optional async delays for testing purposes.
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
        Compute and return a public property value.

        Returns
        -------
        str
            The string "public property".
        """
        return f"public property"

    @property
    def _computed_property_protected(self) -> str:
        """
        Compute and return a protected property value.

        Returns
        -------
        str
            The string "protected property".
        """
        # A computed property.
        return f"protected property"

    @property
    def __computed_property_private(self) -> str:
        """
        Compute and return a private property value.

        Returns
        -------
        str
            The string "private property".

        Notes
        -----
        This is a private computed property method using name mangling,
        typically used for internal logic or testing purposes.
        """
        return f"private property"

    def __init__(self, carro:ICar, *, edad:int=10, callback:ejemplo) -> None:
        """
        Initialize the FakeClass instance with various attributes for testing visibility.

        Parameters
        ----------
        carro : ICar
            Car instance dependency.
        edad : int, default 10
            Age parameter (keyword-only).
        callback : callable
            Callback function, typically the ejemplo function.

        Notes
        -----
        Initializes attributes with different visibility levels:
        - Public attributes: public_attr, dynamic_attr
        - Protected attributes: _protected_attr
        - Private attributes: __private_attr, __dd__
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
        Synchronously add two integers.

        Parameters
        ----------
        x : int
            The first integer to add.
        y : int
            The second integer to add.

        Returns
        -------
        int
            The sum of x and y.
        """
        return x + y

    async def instanceAsyncMethod(self, x: int, y: int) -> int:
        """
        Asynchronously add two integers with a brief delay.

        Parameters
        ----------
        x : int
            The first integer to add.
        y : int
            The second integer to add.

        Returns
        -------
        int
            The sum of x and y.
        """
        await asyncio.sleep(0.1)  # Brief async delay for testing
        return x + y

    def _protectedsyncMethod(self, x: int, y: int) -> int:
        """
        Protected synchronous method to add two integers.

        Parameters
        ----------
        x : int
            The first integer to add.
        y : int
            The second integer to add.

        Returns
        -------
        int
            The sum of x and y.
        """
        return x + y

    async def _protectedAsyncMethod(self, x: int, y: int) -> int:
        """
        Protected asynchronous method to add two integers with a brief delay.

        Parameters
        ----------
        x : int
            The first integer to add.
        y : int
            The second integer to add.

        Returns
        -------
        int
            The sum of x and y.
        """
        await asyncio.sleep(0.1)  # Brief async delay for testing
        return x + y

    def __privateSyncMethod(self, x: int, y: int) -> int:
        """
        Private synchronous method to add two integers.

        Parameters
        ----------
        x : int
            The first integer to add.
        y : int
            The second integer to add.

        Returns
        -------
        int
            The sum of x and y.

        Notes
        -----
        This method uses name mangling due to the double underscore prefix.
        """
        return x + y

    async def __privateAsyncMethod(self, x: int, y: int) -> int:
        """
        Private asynchronous method to add two integers with a brief delay.

        Parameters
        ----------
        x : int
            The first integer to add.
        y : int
            The second integer to add.

        Returns
        -------
        int
            The sum of x and y.

        Notes
        -----
        This method uses name mangling due to the double underscore prefix.
        """
        await asyncio.sleep(0.1)  # Brief async delay for testing
        return x + y

    @classmethod
    def classSyncMethod(cls, x: int, y: int) -> int:
        """
        Synchronous class method to add two integers.

        Parameters
        ----------
        x : int
            The first integer to add.
        y : int
            The second integer to add.

        Returns
        -------
        int
            The sum of x and y.
        """
        return x + y

    @classmethod
    async def classAsyncMethod(cls, x: int, y: int) -> int:
        """
        Asynchronous class method to add two integers with a brief delay.

        Parameters
        ----------
        x : int
            The first integer to add.
        y : int
            The second integer to add.

        Returns
        -------
        int
            The sum of x and y.
        """
        await asyncio.sleep(0.1)  # Brief async delay for testing
        return x + y

    @classmethod
    def _classMethodProtected(cls, x: int, y: int) -> int:
        """
        Protected synchronous class method to add two integers.

        Parameters
        ----------
        x : int
            The first integer to add.
        y : int
            The second integer to add.

        Returns
        -------
        int
            The sum of x and y.
        """
        return x + y

    @classmethod
    async def _classAsyncMethodProtected(cls, x: int, y: int) -> int:
        """
        Protected asynchronous class method to add two integers with a brief delay.

        Parameters
        ----------
        x : int
            The first integer to add.
        y : int
            The second integer to add.

        Returns
        -------
        int
            The sum of x and y.
        """
        await asyncio.sleep(0.1)  # Brief async delay for testing
        return x + y

    @classmethod
    def __classMethodPrivate(cls, x: int, y: int) -> int:
        """
        Private synchronous class method to add two integers.

        Parameters
        ----------
        x : int
            The first integer to add.
        y : int
            The second integer to add.

        Returns
        -------
        int
            The sum of x and y.

        Notes
        -----
        This method uses name mangling due to the double underscore prefix.
        """
        return x + y

    @classmethod
    async def __classAsyncMethodPrivate(cls, x: int, y: int) -> int:
        """
        Private asynchronous class method to add two integers with a brief delay.

        Parameters
        ----------
        x : int
            The first integer to add.
        y : int
            The second integer to add.

        Returns
        -------
        int
            The sum of x and y.

        Notes
        -----
        This method uses name mangling due to the double underscore prefix.
        """
        await asyncio.sleep(0.1)  # Brief async delay for testing
        return x + y

    @staticmethod
    def staticMethod(text: str) -> str:
        """
        Static method to convert text to uppercase.

        Parameters
        ----------
        text : str
            Input text string to convert.

        Returns
        -------
        str
            The uppercase version of the input string.
        """
        return text.upper()

    @staticmethod
    async def staticAsyncMethod(text: str) -> str:
        """
        Asynchronous static method to convert text to uppercase with a brief delay.

        Parameters
        ----------
        text : str
            Input text string to convert.

        Returns
        -------
        str
            The uppercase version of the input string.
        """
        await asyncio.sleep(0.1)  # Brief async delay for testing
        return text.upper()

    @staticmethod
    def _staticMethodProtected(text: str) -> str:
        """
        Protected static method to convert text to uppercase.

        Parameters
        ----------
        text : str
            Input text string to convert.

        Returns
        -------
        str
            The uppercase version of the input string.
        """
        return text.upper()

    @staticmethod
    async def _staticAsyncMethodProtected(text: str) -> str:
        """
        Protected asynchronous static method to convert text to uppercase with a brief delay.

        Parameters
        ----------
        text : str
            Input text string to convert.

        Returns
        -------
        str
            The uppercase version of the input string.
        """
        await asyncio.sleep(0.1)  # Brief async delay for testing
        return text.upper()

    @staticmethod
    def __staticMethodPrivate(text: str) -> str:
        """
        Private static method to convert text to uppercase.

        Parameters
        ----------
        text : str
            Input text string to convert.

        Returns
        -------
        str
            The uppercase version of the input string.

        Notes
        -----
        This method uses name mangling due to the double underscore prefix.
        """
        return text.upper()

    @staticmethod
    async def __staticAsyncMethodPrivate(text: str) -> str:
        """
        Private asynchronous static method to convert text to uppercase with a brief delay.

        Parameters
        ----------
        text : str
            Input text string to convert.

        Returns
        -------
        str
            The uppercase version of the input string.

        Notes
        -----
        This method uses name mangling due to the double underscore prefix.
        """
        await asyncio.sleep(0.1)  # Brief async delay for testing
        return text.upper()

