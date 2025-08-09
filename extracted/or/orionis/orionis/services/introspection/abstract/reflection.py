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
    """
    A reflection utility class for introspecting abstract base classes (interfaces).

    This class provides comprehensive introspection capabilities for abstract base classes,
    allowing examination of their structure, methods, attributes, and metadata. It enforces
    that the target class must be an abstract base class that directly inherits from abc.ABC.
    """

    @staticmethod
    def isAbstractClass(abstract: Type) -> bool:
        """
        Determine if the provided object is an abstract base class.

        Parameters
        ----------
        abstract : Type
            The class object to check for abstract base class characteristics.

        Returns
        -------
        bool
            True if the object is a class type with abstract methods that directly
            inherits from abc.ABC, False otherwise.
        """
        # Check if the object is a class, has abstract methods, and directly inherits from ABC
        return isinstance(abstract, type) and bool(getattr(abstract, '__abstractmethods__', False)) and ABC in abstract.__bases__

    @staticmethod
    def ensureIsAbstractClass(abstract: Type) -> bool:
        """
        Validate that the provided object is a valid abstract base class.

        Parameters
        ----------
        abstract : Type
            The class object to validate for abstract base class compliance.

        Returns
        -------
        bool
            True if validation passes successfully.

        Raises
        ------
        ReflectionTypeError
            If the object is not a class type, lacks abstract methods, or does not
            directly inherit from abc.ABC.
        """

        # Check if the provided abstract is a class type, has abstract methods, and directly inherits from ABC
        if not isinstance(abstract, type):
            raise ReflectionTypeError(f"Expected a class type for 'abstract', got {type(abstract).__name__!r}")
        if not bool(getattr(abstract, '__abstractmethods__', False)):
            raise ReflectionTypeError(f"Provided class '{abstract.__name__}' is not an interface (abstract base class)")
        if ABC not in abstract.__bases__:
            raise ReflectionTypeError(f"Provided class '{abstract.__name__}' must directly inherit from abc.ABC")

        # If all checks pass, return True
        return True

    def __init__(self, abstract: Type) -> None:
        """
        Initialize the ReflectionAbstract instance with an abstract base class.

        Parameters
        ----------
        abstract : Type
            The abstract base class to be used for reflection operations.
            Must be a valid abstract base class that directly inherits from abc.ABC.

        Raises
        ------
        ReflectionTypeError
            If the provided class is not a valid abstract base class or does not
            directly inherit from abc.ABC.
        """

        # Ensure the provided abstract is an abstract base class (interface)
        ReflectionAbstract.ensureIsAbstractClass(abstract)

        # Set the abstract class as a private attribute
        self.__abstract = abstract

    def getClass(self) -> Type:
        """
        Get the class type associated with this reflection instance.

        Returns
        -------
        Type
            The abstract base class type that was provided during initialization.
        """

        # Return the abstract class type
        return self.__abstract

    def getClassName(self) -> str:
        """
        Get the name of the reflected abstract class.

        Returns
        -------
        str
            The name of the abstract class provided during initialization.
        """

        # Return the name of the abstract class
        return self.__abstract.__name__

    def getModuleName(self) -> str:
        """
        Get the module name where the reflected abstract class is defined.

        Returns
        -------
        str
            The fully qualified module name containing the abstract class definition.
        """

        # Return the module name of the abstract class
        return self.__abstract.__module__

    def getModuleWithClassName(self) -> str:
        """
        Get the fully qualified name of the abstract class including its module.

        Returns
        -------
        str
            The complete module path and class name separated by a dot
            (e.g., 'module.submodule.ClassName').
        """

        # Return the fully qualified name of the class
        return f"{self.getModuleName()}.{self.getClassName()}"

    def getDocstring(self) -> str:
        """
        Retrieve the docstring of the reflected abstract class.

        Returns
        -------
        str or None
            The docstring of the abstract class if available, None otherwise.
        """

        # Return the docstring of the abstract class
        return self.__abstract.__doc__ if self.__abstract.__doc__ else None

    def getBaseClasses(self) -> list:
        """
        Get the base classes of the reflected abstract class.

        Returns
        -------
        list of Type
            List containing all direct base classes of the reflected abstract class.
        """

        # Return the base classes of the abstract class
        return self.__abstract.__bases__

    def getSourceCode(self) -> str:
        """
        Retrieve the complete source code of the reflected abstract class.

        Returns
        -------
        str
            The complete source code of the abstract class as a string.

        Raises
        ------
        ReflectionValueError
            If the source code cannot be retrieved due to file system errors
            or other unexpected exceptions.
        """

        # Attempt to get the source code of the abstract class
        try:
            return inspect.getsource(self.__abstract)

        # Handle OSError if the source code cannot be retrieved
        except OSError as e:
            raise ReflectionValueError(f"Could not retrieve source code for '{self.__abstract.__name__}': {e}")

        # Handle any other unexpected exceptions
        except Exception as e:
            raise ReflectionValueError(f"An unexpected error occurred while retrieving source code for '{self.__abstract.__name__}': {e}")

    def getFile(self) -> str:
        """
        Get the file path where the reflected abstract class is defined.

        Returns
        -------
        str
            The absolute file path containing the abstract class definition.

        Raises
        ------
        ReflectionValueError
            If the file path cannot be retrieved due to type errors or
            other unexpected exceptions.
        """

        # Attempt to get the file path of the abstract class
        try:
            return inspect.getfile(self.__abstract)

        # Handle TypeError if the file path cannot be retrieved
        except TypeError as e:
            raise ReflectionValueError(f"Could not retrieve file for '{self.__abstract.__name__}': {e}")

        # Handle any other unexpected exceptions
        except Exception as e:
            raise ReflectionValueError(f"An unexpected error occurred while retrieving file for '{self.__abstract.__name__}': {e}")

    def getAnnotations(self) -> dict:
        """
        Get the type annotations defined on the reflected abstract class.

        Returns
        -------
        dict
            Dictionary mapping attribute names to their annotated types.
            Private attribute names are normalized by removing name mangling prefixes.
        """

        # Retrieve the annotations from the abstract class
        annotations = {}

        # Iterate through the annotations and handle private attribute name mangling
        for k, v in getattr(self.__abstract, '__annotations__', {}).items():

            # Handle private attribute name mangling for clarity
            annotations[str(k).replace(f"_{self.getClassName()}", "")] = v

        # Return the annotations dictionary
        return annotations

    def hasAttribute(self, attribute: str) -> bool:
        """
        Check if the reflected abstract class has a specific attribute.

        Parameters
        ----------
        attribute : str
            Name of the attribute to check for existence.

        Returns
        -------
        bool
            True if the attribute exists in the class, False otherwise.
        """

        # Check if the attribute exists in the class attributes
        return attribute in self.getAttributes()

    def getAttribute(self, attribute: str):
        """
        Retrieve the value of a specific class attribute.

        Parameters
        ----------
        attribute : str
            The name of the attribute to retrieve.

        Returns
        -------
        Any
            The value of the specified class attribute if it exists, None otherwise.

        Raises
        ------
        ReflectionValueError
            If the attribute does not exist or is not accessible.
        """

        # Get all class attributes (excluding methods and properties)
        attrs = self.getAttributes()

        # Retrieve the attribute value if it exists
        return attrs.get(attribute, None)

    def setAttribute(self, name: str, value) -> bool:
        """
        Set the value of a class attribute.

        Parameters
        ----------
        name : str
            The name of the attribute to set. Must be a valid Python identifier
            and not a reserved keyword.
        value : Any
            The value to assign to the attribute. Must not be callable.

        Returns
        -------
        bool
            True if the attribute was successfully set.

        Raises
        ------
        ReflectionValueError
            If the attribute name is invalid, is a Python keyword, or if the
            value is callable (use setMethod for callables).
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

        # Return True to indicate successful setting of the attribute
        return True

    def removeAttribute(self, name: str) -> bool:
        """
        Remove an attribute from the reflected abstract class.

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

        # Check if the attribute exists in the class
        if not self.hasAttribute(name):
            raise ReflectionValueError(f"Attribute '{name}' does not exist in class '{self.getClassName()}'.")

        # Handle private attribute name mangling for correct attribute resolution
        if name.startswith("__") and not name.endswith("__"):
            class_name = self.getClassName()
            name = f"_{class_name}{name}"

        # Delete the attribute from the class itself
        delattr(self.__abstract, name)

        # Return True to indicate successful removal
        return True

    def getAttributes(self) -> dict:
        """
        Retrieve all class-level attributes from the reflected abstract class.

        Returns
        -------
        dict
            Dictionary containing all class attributes including public, protected,
            private, and dunder attributes. Keys are attribute names and values are
            their corresponding values. Excludes callable objects, static/class methods,
            and properties.
        """

        # Return a dictionary containing all class attributes
        return {
            **self.getPublicAttributes(),
            **self.getProtectedAttributes(),
            **self.getPrivateAttributes(),
            **self.getDunderAttributes()
        }

    def getPublicAttributes(self) -> dict:
        """
        Retrieve all public class-level attributes.

        Returns
        -------
        dict
            Dictionary where keys are names of public class attributes and values
            are their corresponding values. Includes only attributes that do not
            start with underscores and are not callable, static methods, class
            methods, or properties.
        """

        # Get the class name for name mangling checks
        class_name = self.getClassName()

        # Retrieve all attributes from the class
        attributes = self.__abstract.__dict__

        # Initialize a dictionary to hold public attributes
        public = {}

        # Exclude dunder, protected, and private attributes
        for attr, value in attributes.items():

            # Skip callables, static methods, class methods, and properties
            if callable(value) or isinstance(value, staticmethod) or isinstance(value, classmethod) or isinstance(value, property):
                continue

            # Skip dunder attributes
            if attr.startswith("__") and attr.endswith("__"):
                continue

            # Skip private attributes (name-mangled)
            if attr.startswith(f"_{class_name}"):
                continue

            # Skip protected attributes (single underscore)
            if attr.startswith("_"):
                continue

            # Set public attributes
            public[attr] = value

        # Ensure the class name is not a keyword
        return public

    def getProtectedAttributes(self) -> dict:
        """
        Retrieve all protected class-level attributes.

        Returns
        -------
        dict
            Dictionary where keys are names of protected class attributes and values
            are their corresponding values. Includes only attributes that start with
            a single underscore (protected visibility) and are not callable, static
            methods, class methods, or properties. Excludes dunder, public, and
            private attributes.
        """

        # Get the class name for name mangling checks
        class_name = self.getClassName()

        # Retrieve all attributes from the class
        attributes = self.__abstract.__dict__

        # Initialize a dictionary to hold protected attributes
        protected = {}

        # Exclude dunder, public, and private attributes
        for attr, value in attributes.items():

            # Skip callables, static methods, class methods, and properties
            if callable(value) or isinstance(value, staticmethod) or isinstance(value, classmethod) or isinstance(value, property):
                continue

            # Skip dunder attributes
            if attr.startswith("__") and attr.endswith("__"):
                continue

            # Skip private attributes (name-mangled)
            if attr.startswith(f"_{class_name}"):
                continue

            # Only include attributes that start with a single underscore (protected)
            if not attr.startswith("_"):
                continue

            # Exclude internal abc attributes
            if attr.startswith("_abc_"):
                continue

            # Set protected attributes
            protected[attr] = value

        return protected

    def getPrivateAttributes(self) -> dict:
        """
        Retrieve all private class-level attributes.

        Returns
        -------
        dict
            Dictionary where keys are names of private class attributes with name
            mangling prefixes removed for clarity, and values are their corresponding
            values. Includes only name-mangled attributes (starting with _ClassName)
            that are not callable, static methods, class methods, or properties.
        """

        # Get the class name for name mangling checks
        class_name = self.getClassName()

        # Retrieve all attributes from the class
        attributes = self.__abstract.__dict__

        # Initialize a dictionary to hold private attributes
        private = {}

        # Exclude callables, static methods, class methods, and properties
        for attr, value in attributes.items():

            # If the attribute is callable, a static method, a class method, or a property, skip it
            if callable(value) or isinstance(value, staticmethod) or isinstance(value, classmethod) or isinstance(value, property):
                continue

            # Include only name-mangled private attributes
            if attr.startswith(f"_{class_name}"):
                private[str(attr).replace(f"_{class_name}", "")] = value

        # Return the dictionary of private attributes
        return private

    def getDunderAttributes(self) -> dict:
        """
        Retrieve all dunder (double underscore) class-level attributes.

        Returns
        -------
        dict
            Dictionary where keys are names of dunder (magic) class attributes and
            values are their corresponding values. Includes only attributes that
            start and end with double underscores and are not callable, static
            methods, class methods, or properties. Excludes certain built-in
            dunder attributes.
        """

        # Retrieve all attributes from the class
        attributes = self.__abstract.__dict__

        # Initialize a dictionary to hold dunder attributes
        dunder = {}

        # List of built-in dunder attributes to exclude from the result
        exclude = [
            "__class__", "__delattr__", "__dir__", "__doc__", "__eq__", "__format__", "__ge__", "__getattribute__",
            "__gt__", "__hash__", "__init__", "__init_subclass__", "__le__", "__lt__", "__module__", "__ne__",
            "__new__", "__reduce__", "__reduce_ex__", "__repr__", "__setattr__", "__sizeof__", "__str__",
            "__subclasshook__", "__firstlineno__", "__annotations__", "__static_attributes__", "__dict__",
            "__weakref__", "__slots__", "__mro__", "__subclasses__", "__bases__", "__base__", "__flags__",
            "__abstractmethods__", "__code__", "__defaults__", "__kwdefaults__", "__closure__"
        ]

        # Iterate through all attributes and filter for dunder attributes
        for attr, value in attributes.items():

            # Skip callables, static/class methods, properties, and non-dunder attributes
            if callable(value) or isinstance(value, staticmethod) or isinstance(value, classmethod) or isinstance(value, property) or not attr.startswith("__"):
                continue

            # Skip excluded built-in dunder attributes
            if attr in exclude:
                continue

            # Only include attributes that start and end with double underscores
            if attr.startswith("__") and attr.endswith("__"):
                dunder[attr] = value

        # Return the dictionary of dunder attributes
        return dunder

    def getMagicAttributes(self) -> dict:
        """
        Get a dictionary of magic (dunder) class attributes.

        Returns
        -------
        dict
            Dictionary where keys are names of magic class attributes and values
            are their corresponding values. Includes only attributes that start
            with double underscores and are not callable, static methods, class
            methods, or properties.
        """
        return self.getDunderAttributes()

    def hasMethod(self, name: str) -> bool:
        """
        Check if the abstract class has a specific method.

        Parameters
        ----------
        name : str
            The method name to check for existence.

        Returns
        -------
        bool
            True if the method exists in the class, False otherwise.
        """
        return name in self.getMethods()

    def removeMethod(self, name: str) -> bool:
        """
        Remove a method from the abstract class.

        Parameters
        ----------
        name : str
            The method name to remove.

        Returns
        -------
        bool
            True if the method was successfully removed.

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
        Get the signature of a method in the abstract class.

        Parameters
        ----------
        name : str
            The method name to get the signature for.

        Returns
        -------
        inspect.Signature
            The signature object of the specified method.

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
        Get all method names from the abstract class.

        Returns
        -------
        List[str]
            List containing all method names including public, protected, private,
            static, and class methods.
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
        Get all public class methods.

        Returns
        -------
        list
            List of public class method names. Excludes dunder, protected, private
            methods and non-callable attributes like properties, static methods,
            and class methods.
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
        Get all public synchronous method names from the abstract class.

        Returns
        -------
        list
            List of public synchronous method names. Excludes asynchronous methods.
        """
        methods = self.getPublicMethods()
        sync_methods = []
        for method in methods:
            if not inspect.iscoroutinefunction(getattr(self.__abstract, method)):
                sync_methods.append(method)
        return sync_methods

    def getPublicAsyncMethods(self) -> list:
        """
        Get all public asynchronous method names from the abstract class.

        Returns
        -------
        list
            List of public asynchronous method names. Includes only coroutine functions.
        """
        methods = self.getPublicMethods()
        async_methods = []
        for method in methods:
            if inspect.iscoroutinefunction(getattr(self.__abstract, method)):
                async_methods.append(method)
        return async_methods

    def getProtectedMethods(self) -> list:
        """
        Get all protected class methods.

        Returns
        -------
        list
            List of protected class method names. Includes only methods that start
            with a single underscore and are not static methods, class methods,
            or properties.
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
        Get all private class methods.

        Returns
        -------
        list
            List of private class method names with class name prefixes removed
            for clarity. Includes only name-mangled methods that start with
            _ClassName and are not static methods, class methods, or properties.
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
        Get all public class methods from the abstract class.

        Returns
        -------
        list
            List of public class method names. Includes only methods decorated
            with @classmethod that do not start with underscores.
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
        Get all public static methods from the abstract class.

        Returns
        -------
        list
            List of public static method names. Includes only methods decorated
            with @staticmethod that do not start with underscores.
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
        Get all dunder (double underscore) methods from the abstract class.

        Returns
        -------
        list
            List of dunder method names. Includes only methods that start and
            end with double underscores and are callable, excluding certain
            built-in methods.
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
        Get all magic (dunder) methods from the abstract class.

        Returns
        -------
        list
            List of magic method names. This is an alias for getDunderMethods().
        """
        return self.getDunderMethods()

    def getProperties(self) -> List:
        """
        Get all properties from the abstract class.

        Returns
        -------
        List
            List of property names with name mangling prefixes removed for clarity.
        """

        properties = []
        for name, prop in self.__abstract.__dict__.items():
            if isinstance(prop, property):
                name_prop = name.replace(f"_{self.getClassName()}", "")
                properties.append(name_prop)
        return properties

    def getPublicProperties(self) -> List:
        """
        Get all public properties from the abstract class.

        Returns
        -------
        List
            List of public property names with name mangling prefixes removed
            for clarity. Includes only properties that do not start with
            underscores.
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
        Get all protected properties from the abstract class.

        Returns
        -------
        List
            List of protected property names. Includes only properties that start
            with a single underscore but are not name-mangled private properties.
        """
        properties = []
        for name, prop in self.__abstract.__dict__.items():
            if isinstance(prop, property):
                if name.startswith(f"_") and not name.startswith("__") and not name.startswith(f"_{self.getClassName()}"):
                    properties.append(name)
        return properties

    def getPrivateProperties(self) -> List:
        """
        Get all private properties from the abstract class.

        Returns
        -------
        List
            List of private property names with class name prefixes removed for
            clarity. Includes only name-mangled properties that start with
            _ClassName.
        """
        properties = []
        for name, prop in self.__abstract.__dict__.items():
            if isinstance(prop, property):
                if name.startswith(f"_{self.getClassName()}") and not name.startswith("__"):
                    properties.append(name.replace(f"_{self.getClassName()}", ""))
        return properties

    def getPropertySignature(self, name: str) -> inspect.Signature:
        """
        Get the signature of a property's getter method.

        Parameters
        ----------
        name : str
            The property name to get the signature for.

        Returns
        -------
        inspect.Signature
            The signature of the property's getter method.

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
        Get the docstring of a property's getter method.

        Parameters
        ----------
        name : str
            The property name to get the docstring for.

        Returns
        -------
        str or None
            The docstring of the property's getter method if available, None otherwise.

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
        Get the resolved and unresolved dependencies from the constructor.

        Returns
        -------
        ClassDependency
            A structured representation of the constructor dependencies containing
            resolved dependencies (with names and values) and unresolved dependencies
            (parameter names without default values or annotations).
        """
        return ReflectDependencies(self.__abstract).getConstructorDependencies()

    def getMethodDependencies(self, method_name: str) -> MethodDependency:
        """
        Get the resolved and unresolved dependencies from a specific method.

        Parameters
        ----------
        method_name : str
            The name of the method to inspect for dependencies.

        Returns
        -------
        MethodDependency
            A structured representation of the method dependencies containing
            resolved dependencies (with names and values) and unresolved dependencies
            (parameter names without default values or annotations).

        Raises
        ------
        ReflectionAttributeError
            If the specified method does not exist on the abstract class.
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