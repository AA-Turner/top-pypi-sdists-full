from abc import ABC, abstractmethod
import inspect
from typing import Any, Callable, Dict, List, Optional, Tuple, Type
from orionis.services.introspection.dependencies.entities.resolve_argument import ResolveArguments

class IReflectionInstance(ABC):

    @abstractmethod
    def getClass(self) -> Type:
        """
        Get the class of the instance.

        Returns
        -------
        Type
            The class object of the instance
        """
        pass

    @abstractmethod
    def getInstance(self) -> Any:
        """
        Get the instance being reflected upon.

        Returns
        -------
        Any
            The object instance
        """
        pass

    @abstractmethod
    def getClassName(self) -> str:
        """
        Get the name of the instance's class.

        Returns
        -------
        str
            The name of the class
        """
        pass

    @abstractmethod
    def getModuleName(self) -> str:
        """
        Get the name of the module where the class is defined.

        Returns
        -------
        str
            The module name
        """
        pass

    @abstractmethod
    def getModuleWithClassName(self) -> str:
        """
        Get the name of the module where the class is defined.

        Returns
        -------
        str
            The module name
        """
        pass

    @abstractmethod
    def getDocstring(self) -> Optional[str]:
        """
        Get the docstring of the instance's class.

        Returns
        -------
        Optional[str]
            The class docstring, or None if not available
        """
        pass

    @abstractmethod
    def getBaseClasses(self) -> Tuple[Type, ...]:
        """
        Get the base classes of the instance's class.

        Returns
        -------
        Tuple[Type, ...]
            Tuple of base classes
        """
        pass

    @abstractmethod
    def getSourceCode(self) -> Optional[str]:
        """
        Get the source code of the instance's class.

        Returns
        -------
        Optional[str]
            The source code if available, None otherwise
        """
        pass

    @abstractmethod
    def getFile(self) -> Optional[str]:
        """
        Get the file location where the class is defined.

        Returns
        -------
        Optional[str]
            The file path if available, None otherwise
        """
        pass

    @abstractmethod
    def getAnnotations(self) -> Dict[str, Any]:
        """
        Get type annotations of the class.

        Returns
        -------
        Dict[str, Any]
            Dictionary of attribute names and their type annotations
        """
        pass

    @abstractmethod
    def hasAttribute(self, name: str) -> bool:
        """
        Check if the instance has a specific attribute.

        Parameters
        ----------
        name : str
            The attribute name to check

        Returns
        -------
        bool
            True if the attribute exists
        """
        pass

    @abstractmethod
    def getAttribute(self, name: str) -> Any:
        """
        Get an attribute value by name.

        Parameters
        ----------
        name : str
            The attribute name

        Returns
        -------
        Any
            The attribute value

        Raises
        ------
        AttributeError
            If the attribute doesn't exist
        """
        pass

    @abstractmethod
    def setAttribute(self, name: str, value: Any) -> bool:
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
        ReflectionAttributeError
            If the attribute is read-only
        """
        pass

    @abstractmethod
    def removeAttribute(self, name: str) -> bool:
        """
        Remove an attribute from the instance.

        Parameters
        ----------
        name : str
            The attribute name to remove

        Raises
        ------
        ReflectionAttributeError
            If the attribute doesn't exist or is read-only
        """
        pass

    @abstractmethod
    def getAttributes(self) -> Dict[str, Any]:
        """
        Get all attributes of the instance, including public, private, protected, and dunder attributes.

        Returns
        -------
        Dict[str, Any]
            Dictionary of all attribute names and their values
        """
        pass

    @abstractmethod
    def getPublicAttributes(self) -> Dict[str, Any]:
        """
        Get all public attributes of the instance.

        Returns
        -------
        Dict[str, Any]
            Dictionary of public attribute names and their values
        """
        pass

    @abstractmethod
    def getProtectedAttributes(self) -> Dict[str, Any]:
        """
        Get all Protected attributes of the instance.

        Returns
        -------
        Dict[str, Any]
            Dictionary of Protected attribute names and their values
        """
        pass

    @abstractmethod
    def getPrivateAttributes(self) -> Dict[str, Any]:
        """
        Get all private attributes of the instance.

        Returns
        -------
        Dict[str, Any]
            Dictionary of private attribute names and their values
        """
        pass

    @abstractmethod
    def getDunderAttributes(self) -> Dict[str, Any]:
        """
        Get all dunder (double underscore) attributes of the instance.

        Returns
        -------
        Dict[str, Any]
            Dictionary of dunder attribute names and their values
        """
        pass

    @abstractmethod
    def getMagicAttributes(self) -> Dict[str, Any]:
        """
        Get all magic attributes of the instance.

        Returns
        -------
        Dict[str, Any]
            Dictionary of magic attribute names and their values
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
    def callMethod(self, name: str, *args: Any, **kwargs: Any) -> Any:
        """
        Call a method on the instance.

        Parameters
        ----------
        name : str
            Name of the method to call
        *args : Any
            Positional arguments for the method
        **kwargs : Any
            Keyword arguments for the method

        Returns
        -------
        Any
            The result of the method call

        Raises
        ------
        AttributeError
            If the method does not exist on the instance
        TypeError
            If the method is not callable
        """
        pass

    @abstractmethod
    def setMethod(self, name: str, value: Callable) -> bool:
        """
        Set a callable attribute value.

        Parameters
        ----------
        name : str
            The attribute name
        value : Callable
            The callable to set

        Raises
        ------
        ReflectionAttributeError
            If the attribute is not callable or already exists as a method
        """
        pass

    @abstractmethod
    def removeMethod(self, name: str) -> None:
        """
        Remove a method from the instance.

        Parameters
        ----------
        name : str
            The method name to remove

        Raises
        ------
        ReflectionAttributeError
            If the method does not exist or is not callable
        """
        pass

    @abstractmethod
    def getMethodSignature(self, name: str) -> inspect.Signature:
        """
        Get the signature of a method.

        Parameters
        ----------
        name : str
            Name of the method

        Returns
        -------
        inspect.Signature
            The method signature
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
    def getPublicMethods(self) -> List[str]:
        """
        Get all public method names of the instance.

        Returns
        -------
        List[str]
            List of public method names
        """
        pass

    @abstractmethod
    def getPublicSyncMethods(self) -> List[str]:
        """
        Get all public synchronous method names of the instance.

        Returns
        -------
        List[str]
            List of public synchronous method names
        """
        pass

    @abstractmethod
    def getPublicAsyncMethods(self) -> List[str]:
        """
        Get all public asynchronous method names of the instance.

        Returns
        -------
        List[str]
            List of public asynchronous method names
        """
        pass

    @abstractmethod
    def getProtectedMethods(self) -> List[str]:
        """
        Get all protected method names of the instance.

        Returns
        -------
        List[str]
            List of protected method names
        """
        pass

    @abstractmethod
    def getProtectedSyncMethods(self) -> List[str]:
        """
        Get all protected synchronous method names of the instance.

        Returns
        -------
        List[str]
            List of protected synchronous method names
        """
        pass

    @abstractmethod
    def getProtectedAsyncMethods(self) -> List[str]:
        """
        Get all protected asynchronous method names of the instance.

        Returns
        -------
        List[str]
            List of protected asynchronous method names
        """
        pass

    @abstractmethod
    def getPrivateMethods(self) -> List[str]:
        """
        Get all private method names of the instance.

        Returns
        -------
        List[str]
            List of private method names
        """
        pass

    @abstractmethod
    def getPrivateSyncMethods(self) -> List[str]:
        """
        Get all private synchronous method names of the instance.

        Returns
        -------
        List[str]
            List of private synchronous method names
        """
        pass

    @abstractmethod
    def getPrivateAsyncMethods(self) -> List[str]:
        """
        Get all private asynchronous method names of the instance.

        Returns
        -------
        List[str]
            List of private asynchronous method names
        """
        pass

    @abstractmethod
    def getPublicClassMethods(self) -> List[str]:
        """
        Get all class method names of the instance.

        Returns
        -------
        List[str]
            List of class method names
        """
        pass

    @abstractmethod
    def getPublicClassSyncMethods(self) -> List[str]:
        """
        Get all public synchronous class method names of the instance.

        Returns
        -------
        List[str]
            List of public synchronous class method names
        """
        pass

    @abstractmethod
    def getPublicClassAsyncMethods(self) -> List[str]:
        """
        Get all public asynchronous class method names of the instance.

        Returns
        -------
        List[str]
            List of public asynchronous class method names
        """
        pass

    @abstractmethod
    def getProtectedClassMethods(self) -> List[str]:
        """
        Get all protected class method names of the instance.

        Returns
        -------
        List[str]
            List of protected class method names
        """
        pass

    @abstractmethod
    def getProtectedClassSyncMethods(self) -> List[str]:
        """
        Get all protected synchronous class method names of the instance.

        Returns
        -------
        List[str]
            List of protected synchronous class method names
        """
        pass

    @abstractmethod
    def getProtectedClassAsyncMethods(self) -> List[str]:
        """
        Get all protected asynchronous class method names of the instance.

        Returns
        -------
        List[str]
            List of protected asynchronous class method names
        """
        pass

    @abstractmethod
    def getPrivateClassMethods(self) -> List[str]:
        """
        Get all private class method names of the instance.

        Returns
        -------
        List[str]
            List of private class method names
        """
        pass

    @abstractmethod
    def getPrivateClassSyncMethods(self) -> List[str]:
        """
        Get all private synchronous class method names of the instance.

        Returns
        -------
        List[str]
            List of private synchronous class method names
        """
        pass

    @abstractmethod
    def getPrivateClassAsyncMethods(self) -> List[str]:
        """
        Get all private asynchronous class method names of the instance.

        Returns
        -------
        List[str]
            List of private asynchronous class method names
        """
        pass

    @abstractmethod
    def getPublicStaticMethods(self) -> List[str]:
        """
        Get public static method names of the instance.

        Returns
        -------
        List[str]
            List of static method names
        """
        pass

    @abstractmethod
    def getPublicStaticSyncMethods(self) -> List[str]:
        """
        Get all public synchronous static method names of the instance.

        Returns
        -------
        List[str]
            List of public synchronous static method names
        """
        pass

    @abstractmethod
    def getPublicStaticAsyncMethods(self) -> List[str]:
        """
        Get all public asynchronous static method names of the instance.

        Returns
        -------
        List[str]
            List of public asynchronous static method names
        """
        pass

    @abstractmethod
    def getProtectedStaticMethods(self) -> List[str]:
        """
        Get all protected static method names of the instance.

        Returns
        -------
        List[str]
            List of protected static method names
        """
        pass

    @abstractmethod
    def getProtectedStaticSyncMethods(self) -> List[str]:
        """
        Get all protected synchronous static method names of the instance.

        Returns
        -------
        List[str]
            List of protected synchronous static method names
        """
        pass

    @abstractmethod
    def getProtectedStaticAsyncMethods(self) -> List[str]:
        """
        Get all protected asynchronous static method names of the instance.

        Returns
        -------
        List[str]
            List of protected asynchronous static method names
        """
        pass

    @abstractmethod
    def getPrivateStaticMethods(self) -> List[str]:
        """
        Get all private static method names of the instance.

        Returns
        -------
        List[str]
            List of private static method names
        """
        pass

    @abstractmethod
    def getPrivateStaticSyncMethods(self) -> List[str]:
        """
        Get all private synchronous static method names of the instance.

        Returns
        -------
        List[str]
            List of private synchronous static method names
        """
        pass

    @abstractmethod
    def getPrivateStaticAsyncMethods(self) -> List[str]:
        """
        Get all private asynchronous static method names of the instance.

        Returns
        -------
        List[str]
            List of private asynchronous static method names
        """
        pass

    @abstractmethod
    def getDunderMethods(self) -> List[str]:
        """
        Get all dunder (double underscore) method names of the instance.

        Returns
        -------
        List[str]
            List of dunder method names
        """
        pass

    @abstractmethod
    def getMagicMethods(self) -> List[str]:
        """
        Get all magic method names of the instance.

        Returns
        -------
        List[str]
            List of magic method names
        """
        pass

    @abstractmethod
    def getProperties(self) -> Dict:
        """
        Get all properties of the instance.

        Returns
        -------
        List[str]
            List of property names
        """
        pass

    @abstractmethod
    def getPublicProperties(self) -> Dict:
        """
        Get all public properties of the instance.

        Returns
        -------
        Dict
            Dictionary of public property names and their values
        """
        pass

    @abstractmethod
    def getProtectedProperties(self) -> Dict:
        """
        Get all protected properties of the instance.

        Returns
        -------
        Dict
            Dictionary of protected property names and their values
        """
        pass

    @abstractmethod
    def getPrivateProperties(self) -> Dict:
        """
        Get all private properties of the instance.

        Returns
        -------
        Dict
            Dictionary of private property names and their values
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
        ClassProperty
            The value of the specified property

        Raises
        ------
        ReflectionAttributeError
            If the property does not exist or is not accessible
        """
        pass

    @abstractmethod
    def getPropertySignature(self, name: str) -> inspect.Signature:
        """
        Get the signature of a property.

        Parameters
        ----------
        name : str
            Name of the property

        Returns
        -------
        inspect.Signature
            The property signature
        """
        pass

    @abstractmethod
    def getPropertyDocstring(self, name: str) -> str:
        """
        Get the docstring of a property.

        Parameters
        ----------
        name : str
            Name of the property

        Returns
        -------
        str
            The docstring of the property
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