from abc import ABC, abstractmethod
import inspect
from typing import List, Type
from orionis.services.introspection.dependencies.entities.class_dependencies import ClassDependency
from orionis.services.introspection.dependencies.entities.method_dependencies import MethodDependency

class IReflectionAbstract(ABC):
    """
    Abstract base class for reflection operations on Python classes.

    This interface defines the contract for introspecting and manipulating
    class attributes, methods, properties, and dependencies through reflection.
    Provides comprehensive functionality for examining class structure,
    metadata, and behavior at runtime.
    """

    @abstractmethod
    def getClass(self) -> Type:
        """
        Get the class type that this reflection instance is based on.

        Returns
        -------
        Type
            The class type provided during reflection initialization.
        """
        pass

    @abstractmethod
    def getClassName(self) -> str:
        """
        Get the name of the reflected class.

        Returns
        -------
        str
            The simple name of the class without module qualification.
        """
        pass

    @abstractmethod
    def getModuleName(self) -> str:
        """
        Get the name of the module where the reflected class is defined.

        Returns
        -------
        str
            The fully qualified module name where the class is defined.
        """
        pass

    @abstractmethod
    def getModuleWithClassName(self) -> str:
        """
        Get the fully qualified class name including module path.

        Returns
        -------
        str
            The module name concatenated with the class name in the format 'module.ClassName'.
        """
        pass

    @abstractmethod
    def getDocstring(self) -> str:
        """
        Get the docstring of the reflected class.

        Returns
        -------
        str or None
            The class docstring if present, None if no docstring is defined.
        """
        pass

    @abstractmethod
    def getBaseClasses(self) -> list:
        """
        Get all base classes of the reflected class.

        Returns
        -------
        list
            A list of base class types that the reflected class inherits from.
        """
        pass

    @abstractmethod
    def getSourceCode(self) -> str:
        """
        Get the source code of the reflected class.

        Returns
        -------
        str
            The complete source code of the class as a string.

        Raises
        ------
        ReflectionValueError
            If the source code cannot be retrieved (e.g., built-in classes, 
            dynamically created classes, or unavailable source files).
        """
        pass

    @abstractmethod
    def getFile(self) -> str:
        """
        Get the file path where the reflected class is defined.

        Returns
        -------
        str
            The absolute file path of the class definition.

        Raises
        ------
        ReflectionValueError
            If the file path cannot be retrieved (e.g., built-in classes 
            or dynamically created classes).
        """
        pass

    @abstractmethod
    def getAnnotations(self) -> dict:
        """
        Get the type annotations of the reflected class.

        Returns
        -------
        dict
            A dictionary mapping attribute names to their type annotations.
            Returns empty dict if no annotations are present.
        """
        pass

    @abstractmethod
    def hasAttribute(self, attribute: str) -> bool:
        """
        Check if the reflected class has a specific attribute.

        Parameters
        ----------
        attribute : str
            The name of the attribute to check for existence.

        Returns
        -------
        bool
            True if the class has the specified attribute, False otherwise.
        """
        pass

    @abstractmethod
    def getAttribute(self, attribute: str):
        """
        Get the value of a specific class attribute.

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
        Set the value of a class attribute.

        Parameters
        ----------
        name : str
            The name of the attribute to set.
        value : Any
            The value to assign to the attribute.

        Returns
        -------
        bool
            True if the attribute was successfully set.

        Raises
        ------
        ReflectionValueError
            If the attribute is read-only or the operation is invalid.
        """
        pass

    @abstractmethod
    def removeAttribute(self, name: str) -> bool:
        """
        Remove an attribute from the reflected class.

        Parameters
        ----------
        name : str
            The name of the attribute to remove.

        Returns
        -------
        bool
            True if the attribute was successfully removed.

        Raises
        ------
        ReflectionValueError
            If the attribute does not exist or cannot be removed.
        """
        pass

    @abstractmethod
    def getAttributes(self) -> dict:
        """
        Get all non-callable class attributes.

        Returns
        -------
        dict
            A dictionary mapping attribute names to their values. Includes only 
            class attributes that are not callable, not static/class methods, 
            not properties, and do not start with underscores.
        """
        pass

    @abstractmethod
    def getPublicAttributes(self) -> dict:
        """
        Get all public class attributes.

        Returns
        -------
        dict
            A dictionary mapping public attribute names to their values. 
            Includes only class attributes that are not callable, not 
            static/class methods, not properties, and do not start with underscores.
        """
        pass

    @abstractmethod
    def getProtectedAttributes(self) -> dict:
        """
        Get all protected class attributes.

        Returns
        -------
        dict
            A dictionary mapping protected attribute names to their values.
            Includes only class attributes that are not callable, not 
            static/class methods, not properties, and start with a single 
            underscore (indicating protected visibility).
        """
        pass

    @abstractmethod
    def getPrivateAttributes(self) -> dict:
        """
        Get all private class attributes.

        Returns
        -------
        dict
            A dictionary mapping private attribute names to their values.
            Includes only class attributes that are not callable, not 
            static/class methods, not properties, and start with double 
            underscores (indicating private visibility).
        """
        pass

    @abstractmethod
    def getDunderAttributes(self) -> dict:
        """
        Get all dunder (double underscore) class attributes.

        Returns
        -------
        dict
            A dictionary mapping dunder attribute names to their values.
            Includes only class attributes that are not callable, not 
            static/class methods, not properties, and follow the dunder 
            naming pattern (__attribute__).
        """
        pass

    @abstractmethod
    def getMagicAttributes(self) -> dict:
        """
        Get all magic (dunder) class attributes.

        Returns
        -------
        dict
            A dictionary mapping magic attribute names to their values.
            Includes only class attributes that are not callable, not 
            static/class methods, not properties, and follow the magic 
            method naming pattern (__attribute__).
        """
        pass

    @abstractmethod
    def hasMethod(self, name: str) -> bool:
        """
        Check if the reflected class has a specific method.

        Parameters
        ----------
        name : str
            The name of the method to check for existence.

        Returns
        -------
        bool
            True if the method exists, False otherwise.
        """
        pass

    @abstractmethod
    def removeMethod(self, name: str) -> bool:
        """
        Remove a method from the reflected class.

        Parameters
        ----------
        name : str
            The name of the method to remove.

        Returns
        -------
        bool
            True if the method was successfully removed.

        Raises
        ------
        ReflectionValueError
            If the method does not exist or cannot be removed.
        """
        pass

    @abstractmethod
    def getMethodSignature(self, name: str) -> inspect.Signature:
        """
        Get the signature of a specific method.

        Parameters
        ----------
        name : str
            The name of the method to get the signature for.

        Returns
        -------
        inspect.Signature
            The signature object containing parameter information for the method.

        Raises
        ------
        ReflectionValueError
            If the method does not exist or is not callable.
        """
        pass

    @abstractmethod
    def getMethods(self) -> List[str]:
        """
        Get all method names of the reflected class.

        Returns
        -------
        List[str]
            A list containing the names of all methods in the class.
        """
        pass

    @abstractmethod
    def getPublicMethods(self) -> list:
        """
        Get all public method names of the reflected class.

        Returns
        -------
        list
            A list containing the names of all public methods (not starting with underscore).
        """
        pass

    @abstractmethod
    def getPublicSyncMethods(self) -> list:
        """
        Get all public synchronous method names of the reflected class.

        Returns
        -------
        list
            A list containing the names of all public synchronous (non-async) methods.
        """
        pass

    @abstractmethod
    def getPublicAsyncMethods(self) -> list:
        """
        Get all public asynchronous method names of the reflected class.

        Returns
        -------
        list
            A list containing the names of all public asynchronous methods.
        """
        pass

    @abstractmethod
    def getProtectedMethods(self) -> list:
        """
        Get all protected method names of the reflected class.

        Returns
        -------
        list
            A list containing the names of all protected methods (starting with single underscore).
        """
        pass

    @abstractmethod
    def getProtectedSyncMethods(self) -> list:
        """
        Get all protected synchronous method names of the reflected class.

        Returns
        -------
        list
            A list containing the names of all protected synchronous methods.
        """
        pass

    @abstractmethod
    def getProtectedAsyncMethods(self) -> list:
        """
        Get all protected asynchronous method names of the reflected class.

        Returns
        -------
        list
            A list containing the names of all protected asynchronous methods.
        """
        pass

    @abstractmethod
    def getPrivateMethods(self) -> list:
        """
        Get all private method names of the reflected class.

        Returns
        -------
        list
            A list containing the names of all private methods (starting with double underscore).
        """
        pass

    @abstractmethod
    def getPrivateSyncMethods(self) -> list:
        """
        Get all private synchronous method names of the reflected class.

        Returns
        -------
        list
            A list containing the names of all private synchronous methods.
        """
        pass

    @abstractmethod
    def getPrivateAsyncMethods(self) -> list:
        """
        Get all private asynchronous method names of the reflected class.

        Returns
        -------
        list
            A list containing the names of all private asynchronous methods.
        """
        pass

    @abstractmethod
    def getPublicClassMethods(self) -> list:
        """
        Get all public class method names of the reflected class.

        Returns
        -------
        list
            A list containing the names of all public class methods (decorated with @classmethod).
        """
        pass

    @abstractmethod
    def getPublicClassSyncMethods(self) -> list:
        """
        Get all public synchronous class method names of the reflected class.

        Returns
        -------
        list
            A list containing the names of all public synchronous class methods.
        """
        pass

    @abstractmethod
    def getPublicClassAsyncMethods(self) -> list:
        """
        Get all public asynchronous class method names of the reflected class.

        Returns
        -------
        list
            A list containing the names of all public asynchronous class methods.
        """
        pass

    @abstractmethod
    def getProtectedClassMethods(self) -> list:
        """
        Get all protected class method names of the reflected class.

        Returns
        -------
        list
            A list containing the names of all protected class methods (starting with single underscore).
        """
        pass

    @abstractmethod
    def getProtectedClassSyncMethods(self) -> list:
        """
        Get all protected synchronous class method names of the reflected class.

        Returns
        -------
        list
            A list containing the names of all protected synchronous class methods.
        """
        pass

    @abstractmethod
    def getProtectedClassAsyncMethods(self) -> list:
        """
        Get all protected asynchronous class method names of the reflected class.

        Returns
        -------
        list
            A list containing the names of all protected asynchronous class methods.
        """
        pass

    @abstractmethod
    def getPrivateClassMethods(self) -> list:
        """
        Get all private class method names of the reflected class.

        Returns
        -------
        list
            A list containing the names of all private class methods (starting with double underscore).
        """
        pass

    @abstractmethod
    def getPrivateClassSyncMethods(self) -> list:
        """
        Get all private synchronous class method names of the reflected class.

        Returns
        -------
        list
            A list containing the names of all private synchronous class methods.
        """
        pass

    @abstractmethod
    def getPrivateClassAsyncMethods(self) -> list:
        """
        Get all private asynchronous class method names of the reflected class.

        Returns
        -------
        list
            A list containing the names of all private asynchronous class methods.
        """
        pass

    @abstractmethod
    def getPublicStaticMethods(self) -> list:
        """
        Get all public static method names of the reflected class.

        Returns
        -------
        list
            A list containing the names of all public static methods (decorated with @staticmethod).
        """
        pass

    @abstractmethod
    def getPublicStaticSyncMethods(self) -> list:
        """
        Get all public synchronous static method names of the reflected class.

        Returns
        -------
        list
            A list containing the names of all public synchronous static methods.
        """
        pass

    @abstractmethod
    def getPublicStaticAsyncMethods(self) -> list:
        """
        Get all public asynchronous static method names of the reflected class.

        Returns
        -------
        list
            A list containing the names of all public asynchronous static methods.
        """
        pass

    @abstractmethod
    def getProtectedStaticMethods(self) -> list:
        """
        Get all protected static method names of the reflected class.

        Returns
        -------
        list
            A list containing the names of all protected static methods (starting with single underscore).
        """
        pass

    @abstractmethod
    def getProtectedStaticSyncMethods(self) -> list:
        """
        Get all protected synchronous static method names of the reflected class.

        Returns
        -------
        list
            A list containing the names of all protected synchronous static methods.
        """
        pass

    @abstractmethod
    def getProtectedStaticAsyncMethods(self) -> list:
        """
        Get all protected asynchronous static method names of the reflected class.

        Returns
        -------
        list
            A list containing the names of all protected asynchronous static methods.
        """
        pass

    @abstractmethod
    def getPrivateStaticMethods(self) -> list:
        """
        Get all private static method names of the reflected class.

        Returns
        -------
        list
            A list containing the names of all private static methods (starting with double underscore).
        """
        pass

    @abstractmethod
    def getPrivateStaticSyncMethods(self) -> list:
        """
        Get all private synchronous static method names of the reflected class.

        Returns
        -------
        list
            A list containing the names of all private synchronous static methods.
        """
        pass

    @abstractmethod
    def getPrivateStaticAsyncMethods(self) -> list:
        """
        Get all private asynchronous static method names of the reflected class.

        Returns
        -------
        list
            A list containing the names of all private asynchronous static methods.
        """
        pass

    @abstractmethod
    def getDunderMethods(self) -> list:
        """
        Get all dunder (double underscore) method names of the reflected class.

        Returns
        -------
        list
            A list containing the names of all dunder methods following the __method__ pattern.
        """
        pass

    @abstractmethod
    def getMagicMethods(self) -> list:
        """
        Get all magic (dunder) method names of the reflected class.

        Returns
        -------
        list
            A list containing the names of all magic methods following the __method__ pattern.
        """
        pass

    @abstractmethod
    def getProperties(self) -> List[str]:
        """
        Get all property names of the reflected class.

        Returns
        -------
        List[str]
            A list containing the names of all properties defined in the class.
        """
        pass

    @abstractmethod
    def getPublicProperties(self) -> List[str]:
        """
        Get all public property names of the reflected class.

        Returns
        -------
        List[str]
            A list containing the names of all public properties (not starting with underscore).
        """
        pass

    @abstractmethod
    def getProtectedProperties(self) -> List[str]:
        """
        Get all protected property names of the reflected class.

        Returns
        -------
        List[str]
            A list containing the names of all protected properties (starting with single underscore).
        """
        pass

    @abstractmethod
    def getPrivateProperties(self) -> List[str]:
        """
        Get all private property names of the reflected class.

        Returns
        -------
        List[str]
            A list containing the names of all private properties (starting with double underscore).
        """
        pass

    @abstractmethod
    def getPropertySignature(self, name: str) -> inspect.Signature:
        """
        Get the signature of a specific property.

        Parameters
        ----------
        name : str
            The name of the property to get the signature for.

        Returns
        -------
        inspect.Signature
            The signature object containing parameter information for the property.

        Raises
        ------
        ReflectionValueError
            If the property does not exist or is not accessible.
        """
        pass

    @abstractmethod
    def getPropertyDocstring(self, name: str) -> str:
        """
        Get the docstring of a specific property.

        Parameters
        ----------
        name : str
            The name of the property to get the docstring for.

        Returns
        -------
        str
            The docstring of the specified property if present, None if no docstring is defined.

        Raises
        ------
        ReflectionValueError
            If the property does not exist or is not accessible.
        """
        pass

    @abstractmethod
    def getConstructorDependencies(self) -> ClassDependency:
        """
        Get the resolved and unresolved dependencies from the constructor of the reflected class.

        Returns
        -------
        ClassDependency
            A structured representation of the constructor dependencies containing:
            - resolved: Dictionary of resolved dependencies with their names and values
            - unresolved: List of unresolved dependencies (parameter names without default values or annotations)
        """
        pass

    @abstractmethod
    def getMethodDependencies(self, method_name: str) -> MethodDependency:
        """
        Get the resolved and unresolved dependencies from a specific method of the reflected class.

        Parameters
        ----------
        method_name : str
            The name of the method to inspect for dependencies.

        Returns
        -------
        MethodDependency
            A structured representation of the method dependencies containing:
            - resolved: Dictionary of resolved dependencies with their names and values
            - unresolved: List of unresolved dependencies (parameter names without default values or annotations)

        Raises
        ------
        ReflectionValueError
            If the method does not exist or is not accessible.
        """
        pass