import inspect
import keyword
from abc import ABC
from typing import List, Type
from orionis.services.introspection.abstract.contracts.reflection import IReflectionAbstract
from orionis.services.introspection.dependencies.entities.class_dependencies import ClassDependency
from orionis.services.introspection.dependencies.entities.method_dependencies import MethodDependency
from orionis.services.introspection.dependencies.reflection import ReflectDependencies
from orionis.services.introspection.exceptions import (
    ReflectionAttributeError,
    ReflectionTypeError,
    ReflectionValueError
)

class ReflectionAbstract(IReflectionAbstract):

    @staticmethod
    def isAbstractClass(abstract: Type) -> bool:
        """
        Checks if the provided object is an abstract base class (interface).

        Parameters
        ----------
        abstract : Type
            The class to check.

        Returns
        -------
        bool
            True if 'abstract' is an abstract base class, False otherwise.
        """
        return isinstance(abstract, type) and bool(getattr(abstract, '__abstractmethods__', False)) and ABC in abstract.__bases__

    @staticmethod
    def ensureIsAbstractClass(abstract: Type) -> bool:
        """
        Ensures that the provided object is an abstract base class (interface) and directly inherits from ABC.

        Parameters
        ----------
        abstract : Type
            The class to check.

        Raises
        ------
        ReflectionTypeError
            If 'abstract' is not a class type, not an abstract base class, or does not directly inherit from ABC.
        """
        if not isinstance(abstract, type):
            raise ReflectionTypeError(f"Expected a class type for 'abstract', got {type(abstract).__name__!r}")
        if not bool(getattr(abstract, '__abstractmethods__', False)):
            raise ReflectionTypeError(f"Provided class '{abstract.__name__}' is not an interface (abstract base class)")
        if ABC not in abstract.__bases__:
            raise ReflectionTypeError(f"Provided class '{abstract.__name__}' must directly inherit from abc.ABC")
        return True

    def __init__(self, abstract: Type) -> None:
        """
        Initializes the ReflectionAbstract instance with the given abstract class.
        Args:
            abstract (Type): The abstract base class (interface) to be reflected.
        Raises:
            TypeError: If the provided abstract is not an abstract base class.
        """

        # Ensure the provided abstract is an abstract base class (interface)
        ReflectionAbstract.ensureIsAbstractClass(abstract)

        # Set the abstract class as a private attribute
        self.__abstract = abstract

    def getClass(self) -> Type:
        """
        Returns the class type that this reflection concrete is based on.

        Returns
        -------
        Type
            The class type provided during initialization.
        """
        return self.__abstract

    def getClassName(self) -> str:
        """
        Returns the name of the class type.

        Returns
        -------
        str
            The name of the class type.
        """
        return self.__abstract.__name__

    def getModuleName(self) -> str:
        """
        Returns the name of the module where the class is defined.

        Returns
        -------
        str
            The name of the module.
        """
        return self.__abstract.__module__

    def getModuleWithClassName(self) -> str:
        """
        Returns the module name concatenated with the class name.

        Returns
        -------
        str
            The module name followed by the class name.
        """
        return f"{self.getModuleName()}.{self.getClassName()}"

    def getDocstring(self) -> str:
        """
        Returns the docstring of the class.

        Returns
        -------
        str or None
            The docstring of the class, or None if not defined.
        """
        return self.__abstract.__doc__ if self.__abstract.__doc__ else None

    def getBaseClasses(self) -> list:
        """
        Returns a list of base classes of the reflected class.

        Returns
        -------
        list
            A list of base classes.
        """
        return self.__abstract.__bases__

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
        try:
            return inspect.getsource(self.__abstract)
        except OSError as e:
            raise ReflectionValueError(f"Could not retrieve source code for '{self.__abstract.__name__}': {e}")

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
        try:
            return inspect.getfile(self.__abstract)
        except TypeError as e:
            raise ReflectionValueError(f"Could not retrieve file for '{self.__abstract.__name__}': {e}")

    def getAnnotations(self) -> dict:
        """
        Returns the type annotations of the class.

        Returns
        -------
        dict
            A dictionary of type annotations.
        """
        annotations = {}
        for k, v in getattr(self.__abstract, '__annotations__', {}).items():
            annotations[str(k).replace(f"_{self.getClassName()}", "")] = v
        return annotations

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
        return attribute in self.getAttributes()

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
        attrs = self.getAttributes()
        return attrs.get(attribute, None)

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

        # Ensure the name is a valid attr name with regular expression
        if not isinstance(name, str) or not name.isidentifier() or keyword.iskeyword(name):
            raise ReflectionValueError(f"Invalid attribute name '{name}'. Must be a valid Python identifier and not a keyword.")

        # Ensure the value is not callable
        if callable(value):
            raise ReflectionValueError(f"Cannot set attribute '{name}' to a callable. Use setMethod instead.")

        # Handle private attribute name mangling
        if name.startswith("__") and not name.endswith("__"):
            class_name = self.getClassName()
            name = f"_{class_name}{name}"

        # Set the attribute on the class itself
        setattr(self.__abstract, name, value)

        return True

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
        if not self.hasAttribute(name):
            raise ReflectionValueError(f"Attribute '{name}' does not exist in class '{self.getClassName()}'.")

        # Handle private attribute name mangling
        if name.startswith("__") and not name.endswith("__"):
            class_name = self.getClassName()
            name = f"_{class_name}{name}"

        delattr(self.__abstract, name)

        return True

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
        return {
            **self.getPublicAttributes(),
            **self.getProtectedAttributes(),
            **self.getPrivateAttributes(),
            **self.getDunderAttributes()
        }

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
        class_name = self.getClassName()
        attributes = self.__abstract.__dict__
        public = {}

        # Exclude dunder, protected, and private attributes
        for attr, value in attributes.items():
            if callable(value) or isinstance(value, staticmethod) or isinstance(value, classmethod) or isinstance(value, property):
                continue
            if attr.startswith("__") and attr.endswith("__"):
                continue
            if attr.startswith(f"_{class_name}"):
                continue
            if attr.startswith("_"):
                continue
            public[attr] = value

        return public

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
        class_name = self.getClassName()
        attributes = self.__abstract.__dict__
        protected = {}

        # Exclude dunder, public, and private attributes
        for attr, value in attributes.items():
            if callable(value) or isinstance(value, staticmethod) or isinstance(value, classmethod) or isinstance(value, property):
                continue
            if attr.startswith("__") and attr.endswith("__"):
                continue
            if attr.startswith(f"_{class_name}"):
                continue
            if not attr.startswith("_"):
                continue
            if attr.startswith("_abc_"):
                continue
            protected[attr] = value

        return protected

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
        class_name = self.getClassName()
        attributes = self.__abstract.__dict__
        private = {}

        # Exclude dunder, public, and protected attributes
        for attr, value in attributes.items():
            if callable(value) or isinstance(value, staticmethod) or isinstance(value, classmethod) or isinstance(value, property):
                continue
            if attr.startswith(f"_{class_name}"):
                private[str(attr).replace(f"_{class_name}", "")] = value

        return private

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
        attributes = self.__abstract.__dict__
        dunder = {}
        exclude = [
            "__class__", "__delattr__", "__dir__", "__doc__", "__eq__", "__format__", "__ge__", "__getattribute__",
            "__gt__", "__hash__", "__init__", "__init_subclass__", "__le__", "__lt__", "__module__", "__ne__",
            "__new__", "__reduce__", "__reduce_ex__", "__repr__", "__setattr__", "__sizeof__", "__str__",
            "__subclasshook__", "__firstlineno__", "__annotations__", "__static_attributes__", "__dict__",
            "__weakref__", "__slots__", "__mro__", "__subclasses__", "__bases__", "__base__", "__flags__",
            "__abstractmethods__", "__code__", "__defaults__", "__kwdefaults__", "__closure__"
        ]

        # Exclude public, protected, and private attributes
        for attr, value in attributes.items():
            if callable(value) or isinstance(value, staticmethod) or isinstance(value, classmethod) or isinstance(value, property) or not attr.startswith("__"):
                continue
            if attr in exclude:
                continue
            if attr.startswith("__") and attr.endswith("__"):
                dunder[attr] = value

        return dunder

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
        return self.getDunderAttributes()

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
        return name in self.getMethods()

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
        if not self.hasMethod(name):
            raise ReflectionValueError(f"Method '{name}' does not exist in class '{self.getClassName()}'.")

        # Handle private method name mangling
        if name.startswith("__") and not name.endswith("__"):
            class_name = self.getClassName()
            name = f"_{class_name}{name}"

        # Delete the method from the class itself
        delattr(self.__abstract, name)

        # Return True to indicate successful removal
        return True

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
        if not self.hasMethod(name):
            raise ReflectionValueError(f"Method '{name}' does not exist in class '{self.getClassName()}'.")

        # Extract the method from the class if instance is not initialized
        method = getattr(self.__abstract, name, None)

        if not callable(method):
            raise ReflectionValueError(f"'{name}' is not callable in class '{self.getClassName()}'.")

        # Get the signature of the method
        return inspect.signature(method)

    def getMethods(self) -> List[str]:
        """
        Get all method names of the instance.

        Returns
        -------
        List[str]
            List of method names
        """
        return [
            *self.getPublicMethods(),
            *self.getProtectedMethods(),
            *self.getPrivateMethods(),
            *self.getPublicClassMethods(),
            *self.getProtectedClassMethods(),
            *self.getPrivateClassMethods(),
            *self.getPublicStaticMethods(),
            *self.getProtectedStaticMethods(),
            *self.getPrivateStaticMethods(),
        ]

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
        class_name = self.getClassName()
        attributes = self.__abstract.__dict__
        public_methods = []

        # Exclude dunder, protected, private attributes and properties
        for attr, value in attributes.items():
            if callable(value) and not isinstance(value, (staticmethod, classmethod)) and not isinstance(value, property):
                if attr.startswith("__") and attr.endswith("__"):
                    continue
                if attr.startswith(f"_{class_name}"):
                    continue
                if attr.startswith("_"):
                    continue
                public_methods.append(attr)

        return public_methods

    def getPublicSyncMethods(self) -> list:
        """
        Get all public synchronous method names of the class.

        Returns
        -------
        list
            List of public synchronous method names
        """
        methods = self.getPublicMethods()
        sync_methods = []
        for method in methods:
            if not inspect.iscoroutinefunction(getattr(self.__abstract, method)):
                sync_methods.append(method)
        return sync_methods

    def getPublicAsyncMethods(self) -> list:
        """
        Get all public asynchronous method names of the class.

        Returns
        -------
        list
            List of public asynchronous method names
        """
        methods = self.getPublicMethods()
        async_methods = []
        for method in methods:
            if inspect.iscoroutinefunction(getattr(self.__abstract, method)):
                async_methods.append(method)
        return async_methods

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
        class_name = self.getClassName()
        attributes = self.__abstract.__dict__
        protected_methods = []

        # Exclude dunder, public, private attributes and properties
        for attr, value in attributes.items():
            if callable(value) and not isinstance(value, (staticmethod, classmethod)) and not isinstance(value, property):
                if attr.startswith("_") and not attr.startswith("__") and not attr.startswith(f"_{self.getClassName()}"):
                    protected_methods.append(attr)

        return protected_methods

    def getProtectedSyncMethods(self) -> list:
        """
        Get all protected synchronous method names of the class.

        Returns
        -------
        list
            List of protected synchronous method names
        """
        methods = self.getProtectedMethods()
        sync_methods = []
        for method in methods:
            if not inspect.iscoroutinefunction(getattr(self.__abstract, method)):
                sync_methods.append(method)
        return sync_methods

    def getProtectedAsyncMethods(self) -> list:
        """
        Get all protected asynchronous method names of the class.

        Returns
        -------
        list
            List of protected asynchronous method names
        """
        methods = self.getProtectedMethods()
        async_methods = []
        for method in methods:
            if inspect.iscoroutinefunction(getattr(self.__abstract, method)):
                async_methods.append(method)
        return async_methods

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
        class_name = self.getClassName()
        attributes = self.__abstract.__dict__
        private_methods = []

        # Exclude dunder, public, protected attributes and properties
        for attr, value in attributes.items():
            if callable(value) and not isinstance(value, (staticmethod, classmethod)) and not isinstance(value, property):
                if attr.startswith(f"_{class_name}"):
                    private_methods.append(str(attr).replace(f"_{class_name}", ""))

        return private_methods

    def getPrivateSyncMethods(self) -> list:
        """
        Get all private synchronous method names of the class.

        Returns
        -------
        list
            List of private synchronous method names
        """
        methods = self.getPrivateMethods()
        sync_methods = []
        for method in methods:
            if not inspect.iscoroutinefunction(getattr(self.__abstract, f"_{self.getClassName()}{method}")):
                sync_methods.append(method)
        return sync_methods

    def getPrivateAsyncMethods(self) -> list:
        """
        Get all private asynchronous method names of the class.

        Returns
        -------
        list
            List of private asynchronous method names
        """
        methods = self.getPrivateMethods()
        async_methods = []
        for method in methods:
            if inspect.iscoroutinefunction(getattr(self.__abstract, f"_{self.getClassName()}{method}")):
                async_methods.append(method)
        return async_methods

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
        class_name = self.getClassName()
        attributes = self.__abstract.__dict__
        public_class_methods = []

        # Exclude dunder, protected, private attributes and properties
        for attr, value in attributes.items():
            if isinstance(value, classmethod):
                if attr.startswith("__") and attr.endswith("__"):
                    continue
                if attr.startswith(f"_{class_name}"):
                    continue
                if attr.startswith("_"):
                    continue
                public_class_methods.append(attr)

        return public_class_methods

    def getPublicClassSyncMethods(self) -> list:
        """
        Get all public synchronous class method names of the class.

        Returns
        -------
        list
            List of public synchronous class method names
        """
        methods = self.getPublicClassMethods()
        sync_methods = []
        for method in methods:
            if not inspect.iscoroutinefunction(getattr(self.__abstract, method)):
                sync_methods.append(method)
        return sync_methods

    def getPublicClassAsyncMethods(self) -> list:
        """
        Get all public asynchronous class method names of the class.

        Returns
        -------
        list
            List of public asynchronous class method names
        """
        methods = self.getPublicClassMethods()
        async_methods = []
        for method in methods:
            if inspect.iscoroutinefunction(getattr(self.__abstract, method)):
                async_methods.append(method)
        return async_methods

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
        class_name = self.getClassName()
        attributes = self.__abstract.__dict__
        protected_class_methods = []

        # Exclude dunder, public, private attributes and properties
        for attr, value in attributes.items():
            if isinstance(value, classmethod):
                if attr.startswith("_") and not attr.startswith("__") and not attr.startswith(f"_{class_name}"):
                    protected_class_methods.append(attr)

        return protected_class_methods

    def getProtectedClassSyncMethods(self) -> list:
        """
        Get all protected synchronous class method names of the class.

        Returns
        -------
        list
            List of protected synchronous class method names
        """
        methods = self.getProtectedClassMethods()
        sync_methods = []
        for method in methods:
            if not inspect.iscoroutinefunction(getattr(self.__abstract, method)):
                sync_methods.append(method)
        return sync_methods

    def getProtectedClassAsyncMethods(self) -> list:
        """
        Get all protected asynchronous class method names of the class.

        Returns
        -------
        list
            List of protected asynchronous class method names
        """
        methods = self.getProtectedClassMethods()
        async_methods = []
        for method in methods:
            if inspect.iscoroutinefunction(getattr(self.__abstract, method)):
                async_methods.append(method)
        return async_methods

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
        class_name = self.getClassName()
        attributes = self.__abstract.__dict__
        private_class_methods = []

        # Exclude dunder, public, protected attributes and properties
        for attr, value in attributes.items():
            if isinstance(value, classmethod):
                if attr.startswith(f"_{class_name}"):
                    private_class_methods.append(str(attr).replace(f"_{class_name}", ""))

        return private_class_methods

    def getPrivateClassSyncMethods(self) -> list:
        """
        Get all private synchronous class method names of the class.

        Returns
        -------
        list
            List of private synchronous class method names
        """
        methods = self.getPrivateClassMethods()
        sync_methods = []
        for method in methods:
            if not inspect.iscoroutinefunction(getattr(self.__abstract, f"_{self.getClassName()}{method}")):
                sync_methods.append(method)
        return sync_methods

    def getPrivateClassAsyncMethods(self) -> list:
        """
        Get all private asynchronous class method names of the class.

        Returns
        -------
        list
            List of private asynchronous class method names
        """
        methods = self.getPrivateClassMethods()
        async_methods = []
        for method in methods:
            if inspect.iscoroutinefunction(getattr(self.__abstract, f"_{self.getClassName()}{method}")):
                async_methods.append(method)
        return async_methods

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
        class_name = self.getClassName()
        attributes = self.__abstract.__dict__
        public_static_methods = []

        # Exclude dunder, protected, private attributes and properties
        for attr, value in attributes.items():
            if isinstance(value, staticmethod):
                if attr.startswith("__") and attr.endswith("__"):
                    continue
                if attr.startswith(f"_{class_name}"):
                    continue
                if attr.startswith("_"):
                    continue
                public_static_methods.append(attr)

        return public_static_methods

    def getPublicStaticSyncMethods(self) -> list:
        """
        Get all public synchronous static method names of the class.

        Returns
        -------
        list
            List of public synchronous static method names
        """
        methods = self.getPublicStaticMethods()
        sync_methods = []
        for method in methods:
            if not inspect.iscoroutinefunction(getattr(self.__abstract, method)):
                sync_methods.append(method)
        return sync_methods

    def getPublicStaticAsyncMethods(self) -> list:
        """
        Get all public asynchronous static method names of the class.

        Returns
        -------
        list
            List of public asynchronous static method names
        """
        methods = self.getPublicStaticMethods()
        async_methods = []
        for method in methods:
            if inspect.iscoroutinefunction(getattr(self.__abstract, method)):
                async_methods.append(method)
        return async_methods

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
        class_name = self.getClassName()
        attributes = self.__abstract.__dict__
        protected_static_methods = []

        # Exclude dunder, public, private attributes and properties
        for attr, value in attributes.items():
            if isinstance(value, staticmethod):
                if attr.startswith("_") and not attr.startswith("__") and not attr.startswith(f"_{class_name}"):
                    protected_static_methods.append(attr)

        return protected_static_methods

    def getProtectedStaticSyncMethods(self) -> list:
        """
        Get all protected synchronous static method names of the class.

        Returns
        -------
        list
            List of protected synchronous static method names
        """
        methods = self.getProtectedStaticMethods()
        sync_methods = []
        for method in methods:
            if not inspect.iscoroutinefunction(getattr(self.__abstract, method)):
                sync_methods.append(method)
        return sync_methods

    def getProtectedStaticAsyncMethods(self) -> list:
        """
        Get all protected asynchronous static method names of the class.

        Returns
        -------
        list
            List of protected asynchronous static method names
        """
        methods = self.getProtectedStaticMethods()
        async_methods = []
        for method in methods:
            if inspect.iscoroutinefunction(getattr(self.__abstract, method)):
                async_methods.append(method)
        return async_methods

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
        class_name = self.getClassName()
        attributes = self.__abstract.__dict__
        private_static_methods = []

        # Exclude dunder, public, protected attributes and properties
        for attr, value in attributes.items():
            if isinstance(value, staticmethod):
                if attr.startswith(f"_{class_name}"):
                    private_static_methods.append(str(attr).replace(f"_{class_name}", ""))

        return private_static_methods

    def getPrivateStaticSyncMethods(self) -> list:
        """
        Get all private synchronous static method names of the class.

        Returns
        -------
        list
            List of private synchronous static method names
        """
        methods = self.getPrivateStaticMethods()
        sync_methods = []
        for method in methods:
            if not inspect.iscoroutinefunction(getattr(self.__abstract, f"_{self.getClassName()}{method}")):
                sync_methods.append(method)
        return sync_methods

    def getPrivateStaticAsyncMethods(self) -> list:
        """
        Get all private asynchronous static method names of the class.

        Returns
        -------
        list
            List of private asynchronous static method names
        """
        methods = self.getPrivateStaticMethods()
        async_methods = []
        for method in methods:
            if inspect.iscoroutinefunction(getattr(self.__abstract, f"_{self.getClassName()}{method}")):
                async_methods.append(method)
        return async_methods

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
        attributes = self.__abstract.__dict__
        dunder_methods = []
        exclude = []

        # Exclude public, protected, private attributes and properties
        for attr, value in attributes.items():
            if callable(value) and not isinstance(value, (staticmethod, classmethod)) and not isinstance(value, property):
                if attr.startswith("__") and attr.endswith("__") and attr not in exclude:
                    dunder_methods.append(attr)

        return dunder_methods

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
        return self.getDunderMethods()

    def getProperties(self) -> List:
        """
        Get all properties of the instance.

        Returns
        -------
        List[str]
            List of property names
        """

        properties = []
        for name, prop in self.__abstract.__dict__.items():
            if isinstance(prop, property):
                name_prop = name.replace(f"_{self.getClassName()}", "")
                properties.append(name_prop)
        return properties

    def getPublicProperties(self) -> List:
        """
        Get all public properties of the instance.

        Returns
        -------
        List:
            List of public property names and their values
        """
        properties = []
        cls_name = self.getClassName()
        for name, prop in self.__abstract.__dict__.items():
            if isinstance(prop, property):
                if not name.startswith(f"_") and not name.startswith(f"_{cls_name}"):
                    properties.append(name.replace(f"_{cls_name}", ""))
        return properties

    def getProtectedProperties(self) -> List:
        """
        Get all protected properties of the instance.

        Returns
        -------
        List
            List of protected property names and their values
        """
        properties = []
        for name, prop in self.__abstract.__dict__.items():
            if isinstance(prop, property):
                if name.startswith(f"_") and not name.startswith("__") and not name.startswith(f"_{self.getClassName()}"):
                    properties.append(name)
        return properties

    def getPrivateProperties(self) -> List:
        """
        Get all private properties of the instance.

        Returns
        -------
        List
            List of private property names and their values
        """
        properties = []
        for name, prop in self.__abstract.__dict__.items():
            if isinstance(prop, property):
                if name.startswith(f"_{self.getClassName()}") and not name.startswith("__"):
                    properties.append(name.replace(f"_{self.getClassName()}", ""))
        return properties

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
        # Handle private property name mangling
        if name.startswith("__") and not name.endswith("__"):
            class_name = self.getClassName()
            name = f"_{class_name}{name}"

        if not hasattr(self.__abstract, name):
            raise ReflectionValueError(f"Property '{name}' does not exist in class '{self.getClassName()}'.")

        prop = getattr(self.__abstract, name)
        if not isinstance(prop, property):
            raise ReflectionValueError(f"'{name}' is not a property in class '{self.getClassName()}'.")

        return inspect.signature(prop.fget)

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
        # Handle private property name mangling
        if name.startswith("__") and not name.endswith("__"):
            class_name = self.getClassName()
            name = f"_{class_name}{name}"

        if not hasattr(self.__abstract, name):
            raise ReflectionValueError(f"Property '{name}' does not exist in class '{self.getClassName()}'.")

        prop = getattr(self.__abstract, name)
        if not isinstance(prop, property):
            raise ReflectionValueError(f"'{name}' is not a property in class '{self.getClassName()}'.")

        return prop.fget.__doc__ if prop.fget else None

    def getConstructorDependencies(self) -> ClassDependency:
        """
        Get the resolved and unresolved dependencies from the constructor of the instance's class.

        Returns
        -------
        ClassDependency
            A structured representation of the constructor dependencies, containing:
            - resolved: Dictionary of resolved dependencies with their names and values.
            - unresolved: List of unresolved dependencies (parameter names without default values or annotations).
        """
        return ReflectDependencies(self.__abstract).getConstructorDependencies()

    def getMethodDependencies(self, method_name: str) -> MethodDependency:
        """
        Get the resolved and unresolved dependencies from a method of the instance's class.

        Parameters
        ----------
        method_name : str
            The name of the method to inspect

        Returns
        -------
        MethodDependency
            A structured representation of the method dependencies, containing:
            - resolved: Dictionary of resolved dependencies with their names and values.
            - unresolved: List of unresolved dependencies (parameter names without default values or annotations).
        """

        # Ensure the method name is a valid identifier
        if not self.hasMethod(method_name):
            raise ReflectionAttributeError(f"Method '{method_name}' does not exist on '{self.getClassName()}'.")

        # Handle private method name mangling
        if method_name.startswith("__") and not method_name.endswith("__"):
            class_name = self.getClassName()
            method_name = f"_{class_name}{method_name}"

        # Use ReflectDependencies to get method dependencies
        return ReflectDependencies(self.__abstract).getMethodDependencies(method_name)