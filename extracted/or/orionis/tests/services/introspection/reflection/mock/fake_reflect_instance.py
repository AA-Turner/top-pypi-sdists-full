from abc import ABC, abstractmethod
import asyncio

PUBLIC_CONSTANT = "public constant"
_PROTECTED_CONSTANT = "protected constant"
__PRIVATE_CONSTANT = "private constant"

def publicSyncFunction(x: int, y: int) -> int:
    """
    Adds two integers synchronously.

    Parameters
    ----------
    x : int
        The first integer.
    y : int
        The second integer.

    Returns
    -------
    int
        The sum of `x` and `y`.
    """
    return x + y

async def publicAsyncFunction(x: int, y: int) -> int:
    """
    Adds two integers asynchronously.

    Parameters
    ----------
    x : int
        The first integer.
    y : int
        The second integer.

    Returns
    -------
    int
        The sum of `x` and `y`.
    """
    await asyncio.sleep(0.1)
    return x + y

def _protectedSyncFunction(x: int, y: int) -> int:
    """
    Adds two integers synchronously (protected function).

    Parameters
    ----------
    x : int
        The first integer.
    y : int
        The second integer.

    Returns
    -------
    int
        The sum of `x` and `y`.
    """
    return x + y

async def _protectedAsyncFunction(x: int, y: int) -> int:
    """
    Adds two integers asynchronously (protected function).

    Parameters
    ----------
    x : int
        The first integer.
    y : int
        The second integer.

    Returns
    -------
    int
        The sum of `x` and `y`.
    """
    await asyncio.sleep(0.1)
    return x + y

def __privateSyncFunction(x: int, y: int) -> int:
    """
    Adds two integers synchronously (private function).

    Parameters
    ----------
    x : int
        The first integer.
    y : int
        The second integer.

    Returns
    -------
    int
        The sum of `x` and `y`.
    """
    return x + y

async def __privateAsyncFunction(x: int, y: int) -> int:
    """
    Adds two integers asynchronously (private function).

    Parameters
    ----------
    x : int
        The first integer.
    y : int
        The second integer.

    Returns
    -------
    int
        The sum of `x` and `y`.
    """
    await asyncio.sleep(0.1)
    return x + y

class PublicFakeClass:
    """
    Public class used as a test double for inspection and mocking purposes.

    This class acts as a simple parent class for test doubles in inspection-related tests.

    Attributes
    ----------
    None

    Methods
    -------
    None
    """
    pass

class _ProtectedFakeClass:
    """
    Protected class used as a test double for inspection and mocking purposes.

    This class acts as a simple parent class for test doubles in inspection-related tests.

    Attributes
    ----------
    None

    Methods
    -------
    None
    """
    pass

class __PrivateFakeClass:
    """
    Private class used as a test double for inspection and mocking purposes.

    This class acts as a simple parent class for test doubles in inspection-related tests.

    Attributes
    ----------
    None

    Methods
    -------
    None
    """
    pass

class BaseFakeClass:
    """
    Base class for creating fake or mock classes for testing and inspection.

    This class serves as a foundational parent for test doubles used in inspection-related tests.

    Attributes
    ----------
    None

    Methods
    -------
    None
    """
    pass

class FakeClass(BaseFakeClass):
    """
    FakeClass is a test double designed to simulate various attribute and method visibilities for inspection and testing.

    This class provides public, protected, and private class-level and instance-level attributes, as well as properties and methods with different visibilities. It includes synchronous and asynchronous instance, class, and static methods to facilitate comprehensive testing of attribute and method access patterns, including Python's name mangling for private members.

    Attributes
    ----------
    public_attr : int
        Public class and instance attribute set to 42.
    dynamic_attr
        Public attribute initialized to None, can be set dynamically.
    _protected_attr : str
        Protected class and instance attribute set to "protected".
    __private_attr : str
        Private class and instance attribute set to "private".
    __dd__ : str
        Dunder (double underscore) attribute set to "dunder_value".

    Properties
    ----------
    computed_public_property : str
        Returns "public property".
    _computed_property_protected : str
        Returns "protected property".
    __computed_property_private : str
        Returns "private property".

    Methods
    -------
    instanceSyncMethod(x: int, y: int) -> int
        Synchronously adds two integers and returns the result.
    instanceAsyncMethod(x: int, y: int) -> int
        Asynchronously adds two integers and returns the result.
    _protectedsyncMethod(x: int, y: int) -> int
        Protected synchronous addition method.
    _protectedAsyncMethod(x: int, y: int) -> int
        Protected asynchronous addition method.
    __privateSyncMethod(x: int, y: int) -> int
        Private synchronous addition method.
    __privateAsyncMethod(x: int, y: int) -> int
        Private asynchronous addition method.

    Class Methods
    -------------
    classSyncMethod(x: int, y: int) -> int
        Synchronously adds two integers and returns the result (class method).
    classAsyncMethod(x: int, y: int) -> int
        Asynchronously adds two integers and returns the result (class method).
    _classMethodProtected(x: int, y: int) -> int
        Protected synchronous class addition method.
    _classAsyncMethodProtected(x: int, y: int) -> int
        Protected asynchronous class addition method.
    __classMethodPrivate(x: int, y: int) -> int
        Private synchronous class addition method.
    __classAsyncMethodPrivate(x: int, y: int) -> int
        Private asynchronous class addition method.

    Static Methods
    --------------
    staticMethod(text: str) -> str
        Synchronously converts the input text to uppercase.
    staticAsyncMethod(text: str) -> str
        Asynchronously converts the input text to uppercase.
    _staticMethodProtected(text: str) -> str
        Protected synchronous static method to convert text to uppercase.
    _staticAsyncMethodProtected(text: str) -> str
        Protected asynchronous static method to convert text to uppercase.
    __staticMethodPrivate(text: str) -> str
        Private synchronous static method to convert text to uppercase.
    __staticAsyncMethodPrivate(text: str) -> str
        Private asynchronous static method to convert text to uppercase.

    Notes
    -----
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
        Returns a string indicating this is a public computed property.

        Returns
        -------
        str
            The string "public property".
        """
        return f"public property"

    @property
    def _computed_property_protected(self) -> str:
        """
        Returns a string indicating this is a protected computed property.

        Returns
        -------
        str
            The string "protected property".
        """
        # Protected computed property for testing attribute visibility
        return f"protected property"

    @property
    def __computed_property_private(self) -> str:
        """
        Returns a string indicating this is a private computed property.

        Returns
        -------
        str
            The string "private property".
        """
        # Private computed property for internal use or testing
        return f"private property"

    def __init__(self) -> None:
        """
        Initialize a FakeClass instance with attributes of varying visibility.

        Parameters
        ----------
        None

        Attributes
        ----------
        public_attr : int
            Public attribute set to 42.
        dynamic_attr
            Public attribute initialized to None, can be set dynamically.
        _protected_attr : str
            Protected attribute set to "protected".
        __private_attr : str
            Private attribute set to "private".
        __dd__ : str
            Dunder (double underscore) attribute set to "dunder_value".
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
        Synchronously add two integers and return the result.

        Parameters
        ----------
        x : int
            The first integer to add.
        y : int
            The second integer to add.

        Returns
        -------
        int
            The sum of `x` and `y`.
        """
        return x + y

    async def instanceAsyncMethod(self, x: int, y: int) -> int:
        """
        Asynchronously add two integers and return the result.

        Parameters
        ----------
        x : int
            First integer to add.
        y : int
            Second integer to add.

        Returns
        -------
        int
            The sum of `x` and `y`.
        """
        await asyncio.sleep(0.1)
        return x + y

    def _protectedsyncMethod(self, x: int, y: int) -> int:
        """
        Synchronously add two integers and return the result (protected method).

        Parameters
        ----------
        x : int
            First integer to add.
        y : int
            Second integer to add.

        Returns
        -------
        int
            The sum of `x` and `y`.
        """
        return x + y

    async def _protectedAsyncMethod(self, x: int, y: int) -> int:
        """
        Asynchronously add two integers and return the result (protected method).

        Parameters
        ----------
        x : int
            First integer to add.
        y : int
            Second integer to add.

        Returns
        -------
        int
            The sum of `x` and `y`.
        """
        await asyncio.sleep(0.1)
        return x + y

    def __privateSyncMethod(self, x: int, y: int) -> int:
        """
        Synchronously add two integers and return the result (private method).

        Parameters
        ----------
        x : int
            First integer to add.
        y : int
            Second integer to add.

        Returns
        -------
        int
            The sum of `x` and `y`.
        """
        return x + y

    async def __privateAsyncMethod(self, x: int, y: int) -> int:
        """
        Asynchronously add two integers and return the result (private method).

        Parameters
        ----------
        x : int
            First integer to add.
        y : int
            Second integer to add.

        Returns
        -------
        int
            The sum of `x` and `y`.
        """
        await asyncio.sleep(0.1)
        return x + y

    @classmethod
    def classSyncMethod(cls, x: int, y: int) -> int:
        """
        Synchronously adds two integers and returns the result.

        Parameters
        ----------
        x : int
            The first integer to add.
        y : int
            The second integer to add.

        Returns
        -------
        int
            The sum of `x` and `y`.
        """
        return x + y

    @classmethod
    async def classAsyncMethod(cls, x: int, y: int) -> int:
        """
        Asynchronously adds two integers and returns the result.

        Parameters
        ----------
        x : int
            The first integer to add.
        y : int
            The second integer to add.

        Returns
        -------
        int
            The sum of `x` and `y`.
        """
        await asyncio.sleep(0.1)
        return x + y

    @classmethod
    def _classMethodProtected(cls, x: int, y: int) -> int:
        """
        Synchronously adds two integers and returns the result (protected class method).

        Parameters
        ----------
        x : int
            The first integer to add.
        y : int
            The second integer to add.

        Returns
        -------
        int
            The sum of `x` and `y`.
        """
        return x + y

    @classmethod
    async def _classAsyncMethodProtected(cls, x: int, y: int) -> int:
        """
        Asynchronously add two integers and return the result (protected class method).

        Parameters
        ----------
        x : int
            The first integer to add.
        y : int
            The second integer to add.

        Returns
        -------
        int
            The sum of `x` and `y`.
        """
        await asyncio.sleep(0.1)
        return x + y

    @classmethod
    def __classMethodPrivate(cls, x: int, y: int) -> int:
        """
        Synchronously add two integers and return the result (private class method).

        Parameters
        ----------
        x : int
            The first integer to add.
        y : int
            The second integer to add.

        Returns
        -------
        int
            The sum of `x` and `y`.
        """
        return x + y

    @classmethod
    async def __classAsyncMethodPrivate(cls, x: int, y: int) -> int:
        """
        Asynchronously add two integers and return the result (private class method).

        Parameters
        ----------
        x : int
            First integer to add.
        y : int
            Second integer to add.

        Returns
        -------
        int
            The sum of `x` and `y`.
        """
        await asyncio.sleep(0.1)
        return x + y

    @staticmethod
    def staticMethod(text: str) -> str:
        """
        Convert the input string to uppercase synchronously.

        Parameters
        ----------
        text : str
            Input string to convert.

        Returns
        -------
        str
            Uppercase version of the input string.
        """
        return text.upper()

    @staticmethod
    async def staticAsyncMethod(text: str) -> str:
        """
        Convert the input string to uppercase asynchronously.

        Parameters
        ----------
        text : str
            Input string to convert.

        Returns
        -------
        str
            Uppercase version of the input string.
        """
        await asyncio.sleep(0.1)
        return text.upper()

    @staticmethod
    def _staticMethodProtected(text: str) -> str:
        """
        Converts the input string to uppercase (protected static method).

        Parameters
        ----------
        text : str
            The input string to convert.

        Returns
        -------
        str
            The uppercase version of the input string.
        """
        return text.upper()

    @staticmethod
    async def _staticAsyncMethodProtected(text: str) -> str:
        """
        Asynchronously converts the input string to uppercase (protected static method).

        Parameters
        ----------
        text : str
            The input string to convert.

        Returns
        -------
        str
            The uppercase version of the input string.
        """
        await asyncio.sleep(0.1)
        return text.upper()

    @staticmethod
    def __staticMethodPrivate(text: str) -> str:
        """
        Converts the input string to uppercase (private static method).

        Parameters
        ----------
        text : str
            The input string to convert.

        Returns
        -------
        str
            The uppercase version of the input string.
        """
        return text.upper()

    @staticmethod
    async def __staticAsyncMethodPrivate(text: str) -> str:
        """
        Asynchronously converts the input string to uppercase (private static method).

        Parameters
        ----------
        text : str
            The input string to be converted to uppercase.

        Returns
        -------
        str
            The uppercase version of the input string.

        Notes
        -----
        This is a private static asynchronous method intended for internal use.
        """
        await asyncio.sleep(0.1)
        return text.upper()

class AbstractFakeClass(ABC):
    """
    Abstract base class that simulates attributes and methods with various visibility levels for testing and inspection.

    This class defines abstract properties and methods, including public, protected, and private members, to be implemented by concrete subclasses. It is designed to facilitate comprehensive testing of attribute and method access patterns, including Python's name mangling for private members.

    Attributes
    ----------
    public_attr : int
        Public class and instance attribute set to 42.
    dynamic_attr
        Public attribute initialized to None, can be set dynamically.
    _protected_attr : str
        Protected class and instance attribute set to "protected".
    __private_attr : str
        Private class and instance attribute set to "private".
    __dd__ : str
        Dunder (double underscore) attribute set to "dunder_value".

    Notes
    -----
    All properties and methods are abstract and must be implemented by subclasses.
    """

    # Class-level attributes
    public_attr: int = 42
    dynamic_attr = None
    _protected_attr: str = "protected"
    __private_attr: str = "private"
    __dd__: str = "dunder_value"

    @property
    @abstractmethod
    def computed_public_property(self) -> str:
        """
        Abstract property for a computed public property.

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
        Abstract property for a computed protected property.

        Returns
        -------
        str
            The computed value of the protected property.
        """
        pass

    @property
    @abstractmethod
    def __computed_property_private(self) -> str:
        """
        Abstract property for a computed private property.

        Returns
        -------
        str
            The computed value of the private property.
        """
        pass

    def __init__(self) -> None:
        """
        Initialize an AbstractFakeClass instance with attributes of varying visibility.

        Attributes
        ----------
        public_attr : int
            Public attribute set to 42.
        dynamic_attr
            Public attribute initialized to None, can be set dynamically.
        _protected_attr : str
            Protected attribute set to "protected".
        __private_attr : str
            Private attribute set to "private".
        __dd__ : str
            Dunder (double underscore) attribute set to "dunder_value".
        """
        self.public_attr = 42
        self.dynamic_attr = None
        self._protected_attr = "protected"
        self.__private_attr = "private"
        self.__dd__ = "dunder_value"

    # Instance methods
    @abstractmethod
    def instanceSyncMethod(self, x: int, y: int) -> int:
        """
        Abstract synchronous instance method to add two integers.

        Parameters
        ----------
        x : int
            First integer.
        y : int
            Second integer.

        Returns
        -------
        int
            The sum of `x` and `y`.
        """
        pass

    @abstractmethod
    async def instanceAsyncMethod(self, x: int, y: int) -> int:
        """
        Abstract asynchronous instance method to add two integers.

        Parameters
        ----------
        x : int
            First integer.
        y : int
            Second integer.

        Returns
        -------
        int
            The sum of `x` and `y`.
        """
        pass

    @abstractmethod
    def _protectedsyncMethod(self, x: int, y: int) -> int:
        """
        Abstract protected synchronous instance method to add two integers.

        Parameters
        ----------
        x : int
            First integer.
        y : int
            Second integer.

        Returns
        -------
        int
            The sum of `x` and `y`.
        """
        pass

    @abstractmethod
    async def _protectedAsyncMethod(self, x: int, y: int) -> int:
        """
        Abstract protected asynchronous instance method to add two integers.

        Parameters
        ----------
        x : int
            First integer.
        y : int
            Second integer.

        Returns
        -------
        int
            The sum of `x` and `y`.
        """
        pass

    @abstractmethod
    def __privateSyncMethod(self, x: int, y: int) -> int:
        """
        Abstract private synchronous instance method to add two integers.

        Parameters
        ----------
        x : int
            First integer.
        y : int
            Second integer.

        Returns
        -------
        int
            The sum of `x` and `y`.
        """
        pass

    @abstractmethod
    async def __privateAsyncMethod(self, x: int, y: int) -> int:
        """
        Abstract private asynchronous instance method to add two integers.

        Parameters
        ----------
        x : int
            First integer.
        y : int
            Second integer.

        Returns
        -------
        int
            The sum of `x` and `y`.
        """
        pass

    # Class methods
    @classmethod
    @abstractmethod
    def classSyncMethod(cls, x: int, y: int) -> int:
        """
        Abstract synchronous class method to add two integers.

        Parameters
        ----------
        x : int
            First integer.
        y : int
            Second integer.

        Returns
        -------
        int
            The sum of `x` and `y`.
        """
        pass

    @classmethod
    @abstractmethod
    async def classAsyncMethod(cls, x: int, y: int) -> int:
        """
        Abstract asynchronous class method to add two integers.

        Parameters
        ----------
        x : int
            First integer.
        y : int
            Second integer.

        Returns
        -------
        int
            The sum of `x` and `y`.
        """
        pass

    @classmethod
    @abstractmethod
    def _classMethodProtected(cls, x: int, y: int) -> int:
        """
        Abstract protected synchronous class method to add two integers.

        Parameters
        ----------
        x : int
            First integer.
        y : int
            Second integer.

        Returns
        -------
        int
            The sum of `x` and `y`.
        """
        pass

    @classmethod
    @abstractmethod
    async def _classAsyncMethodProtected(cls, x: int, y: int) -> int:
        """
        Abstract protected asynchronous class method to add two integers.

        Parameters
        ----------
        x : int
            First integer.
        y : int
            Second integer.

        Returns
        -------
        int
            The sum of `x` and `y`.
        """
        pass

    @classmethod
    @abstractmethod
    def __classMethodPrivate(cls, x: int, y: int) -> int:
        """
        Abstract private synchronous class method to add two integers.

        Parameters
        ----------
        x : int
            First integer.
        y : int
            Second integer.

        Returns
        -------
        int
            The sum of `x` and `y`.
        """
        pass

    @classmethod
    @abstractmethod
    async def __classAsyncMethodPrivate(cls, x: int, y: int) -> int:
        """
        Abstract private asynchronous class method to add two integers.

        Parameters
        ----------
        x : int
            First integer.
        y : int
            Second integer.

        Returns
        -------
        int
            The sum of `x` and `y`.
        """
        pass

    # Static methods
    @staticmethod
    @abstractmethod
    def staticMethod(text: str) -> str:
        """
        Abstract synchronous static method to convert a string to uppercase.

        Parameters
        ----------
        text : str
            Input string.

        Returns
        -------
        str
            Uppercase version of the input string.
        """
        pass

    @staticmethod
    @abstractmethod
    async def staticAsyncMethod(text: str) -> str:
        """
        Abstract asynchronous static method to convert a string to uppercase.

        Parameters
        ----------
        text : str
            Input string.

        Returns
        -------
        str
            Uppercase version of the input string.
        """
        pass

    @staticmethod
    @abstractmethod
    def _staticMethodProtected(text: str) -> str:
        """
        Abstract protected synchronous static method to convert a string to uppercase.

        Parameters
        ----------
        text : str
            Input string.

        Returns
        -------
        str
            Uppercase version of the input string.
        """
        pass

    @staticmethod
    @abstractmethod
    async def _staticAsyncMethodProtected(text: str) -> str:
        """
        Abstract protected asynchronous static method to convert a string to uppercase.

        Parameters
        ----------
        text : str
            Input string.

        Returns
        -------
        str
            Uppercase version of the input string.
        """
        pass

    @staticmethod
    @abstractmethod
    def __staticMethodPrivate(text: str) -> str:
        """
        Abstract private synchronous static method to convert a string to uppercase.

        Parameters
        ----------
        text : str
            Input string.

        Returns
        -------
        str
            Uppercase version of the input string.
        """
        pass

    @staticmethod
    @abstractmethod
    async def __staticAsyncMethodPrivate(text: str) -> str:
        """
        Abstract private asynchronous static method to convert a string to uppercase.

        Parameters
        ----------
        text : str
            Input string.

        Returns
        -------
        str
            Uppercase version of the input string.
        """
        pass