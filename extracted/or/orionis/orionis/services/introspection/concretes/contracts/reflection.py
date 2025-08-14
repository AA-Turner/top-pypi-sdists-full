from abc import ABC, abstractmethod
import inspect
from typing import Any, Callable, List, Type
from orionis.services.introspection.dependencies.entities.resolve_argument import ResolveArguments
from orionis.services.introspection.instances.reflection import ReflectionInstance

class IReflectionConcrete(ABC):

    @abstractmethod
    def getInstance(self, *args, **kwargs):
        """
        Returns an instance of the reflected class.

        Parameters
        ----------
        *args : tuple
            Positional arguments to pass to the class constructor.
        **kwargs : dict
            Keyword arguments to pass to the class constructor.

        Returns
        -------
        object
            An instance of the class type provided during initialization.

        Raises
        ------
        ReflectionValueError
            If instantiation fails or if the class defines an asynchronous __str__ method.
        """
        pass

    @abstractmethod
    def getClass(self) -> Type:
        """
        Returns the class type that this reflection concrete is based on.

        Returns
        -------
        Type
            The class type provided during initialization.
        """
        pass

    @abstractmethod
    def getClassName(self) -> str:
        """
        Returns the name of the class type.

        Returns
        -------
        str
            The name of the class type.
        """
        pass

    @abstractmethod
    def getModuleName(self) -> str:
        """
        Returns the name of the module where the class is defined.

        Returns
        -------
        str
            The name of the module.
        """
        pass

    @abstractmethod
    def getModuleWithClassName(self) -> str:
        """
        Returns the module name concatenated with the class name.

        Returns
        -------
        str
            The module name followed by the class name.
        """
        pass

    @abstractmethod
    def getDocstring(self) -> str:
        """
        Returns the docstring of the class.

        Returns
        -------
        str or None
            The docstring of the class, or None if not defined.
        """
        pass

    @abstractmethod
    def getBaseClasses(self) -> list:
        """
        Returns a list of base classes of the reflected class.

        Returns
        -------
        list
            A list of base classes.
        """
        pass

    @abstractmethod
    def getSourceCode(self) -> str:
        """
        Returns the source code of the class.

        Returns
        -------
        str
            The source code of the class.

        Raises
        ------
        ReflectionValueError
            If the source code cannot be retrieved.
        """
        pass

    @abstractmethod
    def getFile(self) -> str:
        """
        Returns the file path where the class is defined.

        Returns
        -------
        str
            The file path of the class definition.

        Raises
        ------
        ReflectionValueError
            If the file path cannot be retrieved.
        """
        pass

    @abstractmethod
    def getAnnotations(self) -> dict:
        """
        Returns the type annotations of the class.

        Returns
        -------
        dict
            A dictionary of type annotations.
        """
        pass

    @abstractmethod
    def hasAttribute(self, attribute: str) -> bool:
        """
        Checks if the class has a specific attribute.

        Parameters
        ----------
        attribute : str
            The name of the attribute to check.

        Returns
        -------
        bool
            True if the class has the specified attribute, False otherwise.
        """
        pass

    @abstractmethod
    def getAttribute(self, attribute: str):
        """
        Returns the value of a specific class attribute.

        Parameters
        ----------
        attribute : str
            The name of the attribute to retrieve.

        Returns
        -------
        Any
            The value of the specified class attribute.

        Raises
        ------
        ReflectionValueError
            If the attribute does not exist or is not accessible.
        """
        pass

    @abstractmethod
    def setAttribute(self, name: str, value) -> bool:
        """
        Set an attribute value.

        Parameters
        ----------
        name : str
            The attribute name
        value : Any
            The value to set

        Raises
        ------
        ReflectionValueError
            If the attribute is read-only or invalid
        """
        pass

    @abstractmethod
    def removeAttribute(self, name: str) -> bool:
        """
        Remove an attribute from the class.

        Parameters
        ----------
        name : str
            The name of the attribute to remove.

        Raises
        ------
        ReflectionValueError
            If the attribute does not exist or cannot be removed.
        """
        pass

    @abstractmethod
    def getAttributes(self) -> dict:
        """
        Returns a dictionary of all class attributes (not instance attributes).

        Parameters
        ----------
        None

        Returns
        -------
        dict
            A dictionary where keys are the names of class attributes and values are their corresponding values.
            Only attributes that are not callable, not static/class methods, not properties, and do not start with
            underscores (including dunder, protected, or private) are included.
        """
        pass

    @abstractmethod
    def getPublicAttributes(self) -> dict:
        """
        Returns a dictionary of public class attributes (not instance attributes).

        Parameters
        ----------
        None

        Returns
        -------
        dict
            A dictionary where keys are the names of public class attributes and values are their corresponding values.
            Only attributes that are not callable, not static/class methods, not properties, and do not start with
            underscores (including dunder, protected, or private) are included.
        """
        pass

    @abstractmethod
    def getProtectedAttributes(self) -> dict:
        """
        Returns a dictionary of protected class attributes (not instance attributes).

        Parameters
        ----------
        None

        Returns
        -------
        dict
            A dictionary where keys are the names of protected class attributes and values are their corresponding values.
            Only attributes that are not callable, not static/class methods, not properties, and start with a single underscore
            (indicating protected visibility) are included.
        """
        pass

    @abstractmethod
    def getPrivateAttributes(self) -> dict:
        """
        Returns a dictionary of private class attributes (not instance attributes).

        Parameters
        ----------
        None

        Returns
        -------
        dict
            A dictionary where keys are the names of private class attributes and values are their corresponding values.
            Only attributes that are not callable, not static/class methods, not properties, and start with double underscores
            (indicating private visibility) are included.
        """
        pass

    @abstractmethod
    def getDunderAttributes(self) -> dict:
        """
        Returns a dictionary of dunder (double underscore) class attributes (not instance attributes).

        Parameters
        ----------
        None

        Returns
        -------
        dict
            A dictionary where keys are the names of dunder class attributes and values are their corresponding values.
            Only attributes that are not callable, not static/class methods, not properties, and start with double underscores
            (indicating dunder visibility) are included.
        """
        pass

    @abstractmethod
    def getMagicAttributes(self) -> dict:
        """
        Returns a dictionary of magic (dunder) class attributes (not instance attributes).

        Parameters
        ----------
        None

        Returns
        -------
        dict
            A dictionary where keys are the names of magic class attributes and values are their corresponding values.
            Only attributes that are not callable, not static/class methods, not properties, and start with double underscores
            (indicating magic visibility) are included.
        """
        pass

    @abstractmethod
    def hasMethod(self, name: str) -> bool:
        """
        Check if the instance has a specific method.

        Parameters
        ----------
        name : str
            The method name to check

        Returns
        -------
        bool
            True if the method exists, False otherwise
        """
        pass

    @abstractmethod
    def callMethod(self, name: str, *args, **kwargs):
        """
        Call a method of the instance with the provided arguments.

        Parameters
        ----------
        name : str
            The method name to call
        *args : tuple
            Positional arguments to pass to the method
        **kwargs : dict
            Keyword arguments to pass to the method

        Returns
        -------
        Any
            The return value of the method call

        Raises
        ------
        ReflectionValueError
            If the method does not exist or is not callable.
        """
        pass

    @abstractmethod
    def setMethod(self, name: str, method: Callable) -> bool:
        """
        Set a method on the class.

        Parameters
        ----------
        name : str
            The method name to set
        method : callable
            The method to set

        Raises
        ------
        ReflectionValueError
            If the method is not callable or if the name is invalid.
        """
        pass

    @abstractmethod
    def removeMethod(self, name: str) -> bool:
        """
        Remove a method from the class.

        Parameters
        ----------
        name : str
            The method name to remove

        Raises
        ------
        ReflectionValueError
            If the method does not exist or cannot be removed.
        """
        pass

    @abstractmethod
    def getMethodSignature(self, name: str) -> inspect.Signature:
        """
        Get the signature of a method.

        Parameters
        ----------
        name : str
            The method name to get the signature for

        Returns
        -------
        str
            The signature of the method

        Raises
        ------
        ReflectionValueError
            If the method does not exist or is not callable.
        """
        pass

    @abstractmethod
    def getMethods(self) -> List[str]:
        """
        Get all method names of the instance.

        Returns
        -------
        List[str]
            List of method names
        """
        pass

    @abstractmethod
    def getPublicMethods(self) -> list:
        """
        Returns a list of public class methods (not instance methods).

        Parameters
        ----------
        None

        Returns
        -------
        dict
            A list where each element is the name of a public class method.
        """
        pass

    @abstractmethod
    def getPublicSyncMethods(self) -> list:
        """
        Get all public synchronous method names of the class.

        Returns
        -------
        list
            List of public synchronous method names
        """
        pass

    @abstractmethod
    def getPublicAsyncMethods(self) -> list:
        """
        Get all public asynchronous method names of the class.

        Returns
        -------
        list
            List of public asynchronous method names
        """
        pass

    @abstractmethod
    def getProtectedMethods(self) -> list:
        """
        Returns a list of protected class methods (not instance methods).

        Parameters
        ----------
        None

        Returns
        -------
        dict
            A list where each element is the name of a protected class method.
        """
        pass

    @abstractmethod
    def getProtectedSyncMethods(self) -> list:
        """
        Get all protected synchronous method names of the class.

        Returns
        -------
        list
            List of protected synchronous method names
        """
        pass

    @abstractmethod
    def getProtectedAsyncMethods(self) -> list:
        """
        Get all protected asynchronous method names of the class.

        Returns
        -------
        list
            List of protected asynchronous method names
        """
        pass

    @abstractmethod
    def getPrivateMethods(self) -> list:
        """
        Returns a list of private class methods (not instance methods).

        Parameters
        ----------
        None

        Returns
        -------
        list
            A list where each element is the name of a private class method.
        """
        pass

    @abstractmethod
    def getPrivateSyncMethods(self) -> list:
        """
        Get all private synchronous method names of the class.

        Returns
        -------
        list
            List of private synchronous method names
        """
        pass

    @abstractmethod
    def getPrivateAsyncMethods(self) -> list:
        """
        Get all private asynchronous method names of the class.

        Returns
        -------
        list
            List of private asynchronous method names
        """
        pass

    @abstractmethod
    def getPublicClassMethods(self) -> list:
        """
        Returns a list of public class methods (not instance methods).

        Parameters
        ----------
        None

        Returns
        -------
        list
            A list where each element is the name of a public class method.
        """
        pass

    @abstractmethod
    def getPublicClassSyncMethods(self) -> list:
        """
        Get all public synchronous class method names of the class.

        Returns
        -------
        list
            List of public synchronous class method names
        """
        pass

    @abstractmethod
    def getPublicClassAsyncMethods(self) -> list:
        """
        Get all public asynchronous class method names of the class.

        Returns
        -------
        list
            List of public asynchronous class method names
        """
        pass

    @abstractmethod
    def getProtectedClassMethods(self) -> list:
        """
        Returns a list of protected class methods (not instance methods).

        Parameters
        ----------
        None

        Returns
        -------
        list
            A list where each element is the name of a protected class method.
        """
        pass

    @abstractmethod
    def getProtectedClassSyncMethods(self) -> list:
        """
        Get all protected synchronous class method names of the class.

        Returns
        -------
        list
            List of protected synchronous class method names
        """
        pass

    @abstractmethod
    def getProtectedClassAsyncMethods(self) -> list:
        """
        Get all protected asynchronous class method names of the class.

        Returns
        -------
        list
            List of protected asynchronous class method names
        """
        pass

    @abstractmethod
    def getPrivateClassMethods(self) -> list:
        """
        Returns a list of private class methods (not instance methods).

        Parameters
        ----------
        None

        Returns
        -------
        list
            A list where each element is the name of a private class method.
        """
        pass

    @abstractmethod
    def getPrivateClassSyncMethods(self) -> list:
        """
        Get all private synchronous class method names of the class.

        Returns
        -------
        list
            List of private synchronous class method names
        """
        pass

    @abstractmethod
    def getPrivateClassAsyncMethods(self) -> list:
        """
        Get all private asynchronous class method names of the class.

        Returns
        -------
        list
            List of private asynchronous class method names
        """
        pass

    @abstractmethod
    def getPublicStaticMethods(self) -> list:
        """
        Returns a list of public static methods of the class.

        Parameters
        ----------
        None

        Returns
        -------
        list
            A list where each element is the name of a public static method.
        """
        pass

    @abstractmethod
    def getPublicStaticSyncMethods(self) -> list:
        """
        Get all public synchronous static method names of the class.

        Returns
        -------
        list
            List of public synchronous static method names
        """
        pass

    @abstractmethod
    def getPublicStaticAsyncMethods(self) -> list:
        """
        Get all public asynchronous static method names of the class.

        Returns
        -------
        list
            List of public asynchronous static method names
        """
        pass

    @abstractmethod
    def getProtectedStaticMethods(self) -> list:
        """
        Returns a list of protected static methods of the class.

        Parameters
        ----------
        None

        Returns
        -------
        list
            A list where each element is the name of a protected static method.
        """
        pass

    @abstractmethod
    def getProtectedStaticSyncMethods(self) -> list:
        """
        Get all protected synchronous static method names of the class.

        Returns
        -------
        list
            List of protected synchronous static method names
        """
        pass

    @abstractmethod
    def getProtectedStaticAsyncMethods(self) -> list:
        """
        Get all protected asynchronous static method names of the class.

        Returns
        -------
        list
            List of protected asynchronous static method names
        """
        pass

    @abstractmethod
    def getPrivateStaticMethods(self) -> list:
        """
        Returns a list of private static methods of the class.

        Parameters
        ----------
        None

        Returns
        -------
        list
            A list where each element is the name of a private static method.
        """
        pass

    @abstractmethod
    def getPrivateStaticSyncMethods(self) -> list:
        """
        Get all private synchronous static method names of the class.

        Returns
        -------
        list
            List of private synchronous static method names
        """
        pass

    @abstractmethod
    def getPrivateStaticAsyncMethods(self) -> list:
        """
        Get all private asynchronous static method names of the class.

        Returns
        -------
        list
            List of private asynchronous static method names
        """
        pass

    @abstractmethod
    def getDunderMethods(self) -> list:
        """
        Returns a list of dunder (double underscore) methods of the class.

        Parameters
        ----------
        None

        Returns
        -------
        list
            A list where each element is the name of a dunder method.
        """
        pass

    @abstractmethod
    def getMagicMethods(self) -> list:
        """
        Returns a list of magic (dunder) methods of the class.

        Parameters
        ----------
        None

        Returns
        -------
        list
            A list where each element is the name of a magic method.
        """
        pass

    @abstractmethod
    def getProperties(self) -> List:
        """
        Get all properties of the instance.

        Returns
        -------
        List[str]
            List of property names
        """
        pass

    @abstractmethod
    def getPublicProperties(self) -> List:
        """
        Get all public properties of the instance.

        Returns
        -------
        List:
            List of public property names and their values
        """
        pass

    @abstractmethod
    def getProtectedProperties(self) -> List:
        """
        Get all protected properties of the instance.

        Returns
        -------
        List
            List of protected property names and their values
        """
        pass

    @abstractmethod
    def getPrivateProperties(self) -> List:
        """
        Get all private properties of the instance.

        Returns
        -------
        List
            List of private property names and their values
        """
        pass

    @abstractmethod
    def getProperty(self, name: str) -> Any:
        """
        Get a specific property of the instance.

        Parameters
        ----------
        name : str
            The name of the property to retrieve

        Returns
        -------
        Any
            The value of the property

        Raises
        ------
        ReflectionValueError
            If the property does not exist or is not accessible.
        """
        pass

    @abstractmethod
    def getPropertySignature(self, name: str) -> inspect.Signature:
        """
        Get the signature of a property.

        Parameters
        ----------
        name : str
            The property name to get the signature for

        Returns
        -------
        inspect.Signature
            The signature of the property

        Raises
        ------
        ReflectionValueError
            If the property does not exist or is not accessible.
        """
        pass

    @abstractmethod
    def getPropertyDocstring(self, name: str) -> str:
        """
        Get the docstring of a property.

        Parameters
        ----------
        name : str
            The property name to get the docstring for

        Returns
        -------
        str
            The docstring of the property

        Raises
        ------
        ReflectionValueError
            If the property does not exist or is not accessible.
        """
        pass

    @abstractmethod
    def getConstructorDependencies(self) -> ResolveArguments:
        """
        Get the resolved and unresolved dependencies from the constructor of the instance's class.

        Returns
        -------
        ResolveArguments
            A structured representation of the constructor dependencies, containing:
            - resolved: Dictionary of resolved dependencies with their names and values.
            - unresolved: List of unresolved dependencies (parameter names without default values or annotations).
        """
        pass

    @abstractmethod
    def getMethodDependencies(self, method_name: str) -> ResolveArguments:
        """
        Get the resolved and unresolved dependencies from a method of the instance's class.

        Parameters
        ----------
        method_name : str
            The name of the method to inspect

        Returns
        -------
        ResolveArguments
            A structured representation of the method dependencies, containing:
            - resolved: Dictionary of resolved dependencies with their names and values.
            - unresolved: List of unresolved dependencies (parameter names without default values or annotations).
        """
        pass

    @abstractmethod
    def reflectionInstance(self) -> ReflectionInstance:
        """
        Get the reflection instance of the concrete class.

        Returns
        -------
        ReflectionInstance
            An instance of ReflectionInstance for the concrete class
        """
        pass