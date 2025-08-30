import abc
import inspect
import keyword
from typing import Any, Callable, List, Type
from orionis.services.asynchrony.coroutines import Coroutine
from orionis.services.introspection.concretes.contracts.reflection import IReflectionConcrete
from orionis.services.introspection.dependencies.entities.resolve_argument import ResolveArguments
from orionis.services.introspection.dependencies.reflection import ReflectDependencies
from orionis.services.introspection.exceptions import (
    ReflectionAttributeError,
    ReflectionTypeError,
    ReflectionValueError
)
from orionis.services.introspection.instances.reflection import ReflectionInstance

class ReflectionConcrete(IReflectionConcrete):
    """
    A concrete implementation for reflecting on class types and their members.

    This class provides comprehensive introspection capabilities for analyzing class
    structures, attributes, methods, properties, and dependencies. It supports
    dynamic manipulation of class members while maintaining type safety and
    validation.
    """

    @staticmethod
    def isConcreteClass(concrete: Type) -> bool:
        """
        Check if the provided type is a valid concrete class for reflection.

        Parameters
        ----------
        concrete : Type
            The class type to validate for reflection compatibility.

        Returns
        -------
        bool
            True if the class is valid for reflection, False otherwise.
        """
        try:
            return ReflectionConcrete.ensureIsConcreteClass(concrete)
        except (ReflectionTypeError, ReflectionValueError):
            return False

    @staticmethod
    def ensureIsConcreteClass(concrete: Type) -> bool:
        """
        Validate that the provided type is a concrete class suitable for reflection.

        This method performs comprehensive validation to ensure the type can be
        safely used for reflection operations. It checks for proper class type,
        excludes built-in types, and prevents abstract classes.

        Parameters
        ----------
        concrete : Type
            The class type to validate.

        Returns
        -------
        bool
            True if validation passes.

        Raises
        ------
        ReflectionTypeError
            If the argument is not a class type or is an instance.
        ReflectionValueError
            If the class is built-in, primitive, abstract, or an interface.
        """

        # Check if the concrete is a class type
        if not isinstance(concrete, type):
            raise ReflectionTypeError(f"Expected a class, got {type(concrete)}")

        # Define a set of built-in and primitive types
        builtin_types = {
            int, float, str, bool, bytes, type(None), complex,
            list, tuple, dict, set, frozenset
        }

        # Check if the concrete class is a built-in or primitive type
        if concrete in builtin_types:
            raise ReflectionValueError(f"Class '{concrete.__name__}' is a built-in or primitive type and cannot be used.")

        # Prevent instantiating if it's already an instance
        if not isinstance(concrete, type):
            raise ReflectionTypeError(f"Expected a class type, got instance of '{type(concrete).__name__}'.")

        # Check for ABC inheritance to catch interfaces
        if abc.ABC in concrete.__bases__:
            raise ReflectionValueError(f"Class '{concrete.__name__}' is an interface and cannot be used.")

        # Check if the class has any abstract methods
        if inspect.isabstract(concrete):
            raise ReflectionValueError(f"Class '{concrete.__name__}' is an abstract class and cannot be used.")

        return True

    def __init__(self, concrete: Type) -> None:
        """
        Initialize the reflection concrete with a validated class type.

        Performs validation on the provided class type and initializes the
        reflection instance with the concrete class for subsequent operations.

        Parameters
        ----------
        concrete : Type
            The class type to reflect upon.

        Raises
        ------
        ReflectionTypeError
            If the argument is not a class type or is an instance.
        ReflectionValueError
            If the class is built-in, primitive, abstract, or an interface.

        Notes
        -----
        Built-in and primitive types (e.g., int, str, list) are not allowed.
        Abstract classes and interfaces (classes with abstract methods) are not allowed.
        """

        # Ensure the provided concrete type is a valid ReflectionConcrete class
        ReflectionConcrete.ensureIsConcreteClass(concrete)

        # Set the concrete class in the instance
        self._concrete = concrete
        self.__instance = None

    def getInstance(self, *args, **kwargs):
        """
        Create and return an instance of the reflected class.

        Instantiates the reflected class using the provided arguments and
        performs validation to ensure the instance is compatible with
        reflection operations.

        Parameters
        ----------
        *args : tuple
            Positional arguments to pass to the class constructor.
        **kwargs : dict
            Keyword arguments to pass to the class constructor.

        Returns
        -------
        object
            An instance of the reflected class.

        Raises
        ------
        ReflectionValueError
            If instantiation fails or the class has an asynchronous __str__ method.
        """

        try:

            # Try to instantiate the class
            instance = self._concrete(*args, **kwargs)

            # Check if __str__ is a coroutine function
            str_method = getattr(instance, '__str__', None)
            if str_method and inspect.iscoroutinefunction(str_method):
                raise ReflectionValueError(
                    f"Class '{self._concrete.__name__}' defines an asynchronous __str__ method, which is not supported."
                )

            # If successful, set the instance internal variable
            self.__instance = instance

            # Return the instance
            return instance

        except Exception as e:

            # Catch any exception during instantiation and raise a ReflectionValueError
            raise ReflectionValueError(f"Failed to instantiate '{self._concrete.__name__}': {e}")

    def getClass(self) -> Type:
        """
        Get the class type being reflected upon.

        Returns
        -------
        Type
            The class type provided during initialization.
        """
        return self._concrete

    def getClassName(self) -> str:
        """
        Get the name of the reflected class.

        Returns
        -------
        str
            The simple name of the class without module qualification.
        """
        return self._concrete.__name__

    def getModuleName(self) -> str:
        """
        Get the module name where the reflected class is defined.

        Returns
        -------
        str
            The fully qualified module name containing the class.
        """
        return self._concrete.__module__

    def getModuleWithClassName(self) -> str:
        """
        Get the fully qualified class name including module path.

        Returns
        -------
        str
            The module name concatenated with the class name, separated by a dot.
        """
        return f"{self.getModuleName()}.{self.getClassName()}"

    def getDocstring(self) -> str:
        """
        Get the docstring of the reflected class.

        Returns
        -------
        str or None
            The class docstring if defined, None otherwise.
        """
        return self._concrete.__doc__ if self._concrete.__doc__ else None

    def getBaseClasses(self) -> list:
        """
        Get all base classes of the reflected class.

        Returns
        -------
        list
            A list containing all base classes in the method resolution order.
        """
        return self._concrete.__bases__

    def getSourceCode(self) -> str:
        """
        Get the source code of the reflected class.

        Returns
        -------
        str
            The complete source code of the class definition.

        Raises
        ------
        ReflectionValueError
            If the source code cannot be retrieved (e.g., built-in classes).
        """
        try:
            return inspect.getsource(self._concrete)
        except OSError as e:
            raise ReflectionValueError(f"Could not retrieve source code for '{self._concrete.__name__}': {e}")

    def getFile(self) -> str:
        """
        Get the file path where the reflected class is defined.

        Returns
        -------
        str
            The absolute file path containing the class definition.

        Raises
        ------
        ReflectionValueError
            If the file path cannot be determined (e.g., dynamically created classes).
        """
        try:
            return inspect.getfile(self._concrete)
        except TypeError as e:
            raise ReflectionValueError(f"Could not retrieve file for '{self._concrete.__name__}': {e}")

    def getAnnotations(self) -> dict:
        """
        Get type annotations defined on the reflected class.

        Processes and returns the type annotations with proper name mangling
        resolution for private attributes.

        Returns
        -------
        dict
            A dictionary mapping attribute names to their type annotations.
        """
        annotations = {}
        for k, v in getattr(self._concrete, '__annotations__', {}).items():
            # Remove private attribute name mangling for cleaner output
            annotations[str(k).replace(f"_{self.getClassName()}", "")] = v
        return annotations

    def hasAttribute(self, attribute: str) -> bool:
        """
        Check if the reflected class has a specific attribute.

        Parameters
        ----------
        attribute : str
            The name of the attribute to check for.

        Returns
        -------
        bool
            True if the attribute exists, False otherwise.
        """
        return attribute in self.getAttributes()

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
            The value of the specified attribute, or None if not found.

        Raises
        ------
        ReflectionValueError
            If the attribute does not exist or is not accessible.
        """
        attrs = self.getAttributes()
        return attrs.get(attribute, None)

    def setAttribute(self, name: str, value) -> bool:
        """
        Set a class attribute to the specified value.

        Validates the attribute name and value before setting. Handles private
        attribute name mangling automatically.

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
            If the attribute name is invalid or the value is callable.
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
        setattr(self._concrete, name, value)

        return True

    def removeAttribute(self, name: str) -> bool:
        """
        Remove an attribute from the reflected class.

        Handles private attribute name mangling automatically before removal.

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

        # Check if the attribute exists
        if not self.hasAttribute(name):
            raise ReflectionValueError(f"Attribute '{name}' does not exist in class '{self.getClassName()}'.")

        # Handle private attribute name mangling
        if name.startswith("__") and not name.endswith("__"):
            class_name = self.getClassName()
            name = f"_{class_name}{name}"

        # Delete the attribute from the class itself
        delattr(self._concrete, name)

        # Return True to indicate successful removal
        return True

    def getAttributes(self) -> dict:
        """
        Get all class attributes regardless of visibility.

        Combines public, protected, private, and dunder attributes into a
        single dictionary for comprehensive attribute access.

        Returns
        -------
        dict
            A dictionary mapping attribute names to their values, including
            all visibility levels (public, protected, private, dunder).
        """

        # Combine all attribute types into a single dictionary
        return {
            **self.getPublicAttributes(),
            **self.getProtectedAttributes(),
            **self.getPrivateAttributes(),
            **self.getDunderAttributes()
        }

    def getPublicAttributes(self) -> dict:
        """
        Get all public class attributes.

        Retrieves class attributes that do not start with underscores,
        excluding callables, static methods, class methods, and properties.

        Returns
        -------
        dict
            A dictionary mapping public attribute names to their values.
            Excludes dunder, protected, and private attributes.
        """
        class_name = self.getClassName()
        attributes = self._concrete.__dict__
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
        Get all protected class attributes.

        Retrieves class attributes that start with a single underscore,
        indicating protected visibility in Python convention.

        Returns
        -------
        dict
            A dictionary mapping protected attribute names to their values.
            Includes only attributes starting with single underscore.
        """
        class_name = self.getClassName()
        attributes = self._concrete.__dict__
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
            protected[attr] = value

        return protected

    def getPrivateAttributes(self) -> dict:
        """
        Get all private class attributes.

        Retrieves class attributes that use Python's name mangling convention
        for private attributes (double underscore prefix).

        Returns
        -------
        dict
            A dictionary mapping private attribute names (with mangling removed)
            to their values.
        """
        class_name = self.getClassName()
        attributes = self._concrete.__dict__
        private = {}

        # Exclude dunder, public, and protected attributes
        for attr, value in attributes.items():
            if callable(value) or isinstance(value, staticmethod) or isinstance(value, classmethod) or isinstance(value, property):
                continue
            if attr.startswith(f"_{class_name}"):
                # Remove name mangling for cleaner output
                private[str(attr).replace(f"_{class_name}", "")] = value

        return private

    def getDunderAttributes(self) -> dict:
        """
        Get all dunder (magic) class attributes.

        Retrieves class attributes that follow the double underscore naming
        convention, excluding common built-in dunder attributes.

        Returns
        -------
        dict
            A dictionary mapping dunder attribute names to their values.
            Excludes standard Python dunder attributes like __class__, __dict__, etc.
        """
        attributes = self._concrete.__dict__
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
        Get all magic (dunder) class attributes.

        This is an alias for getDunderAttributes() providing alternative naming
        for accessing double underscore attributes.

        Returns
        -------
        dict
            A dictionary mapping magic attribute names to their values.
        """
        return self.getDunderAttributes()

    def hasMethod(self, name: str) -> bool:
        """
        Check if the reflected class has a specific method.

        Parameters
        ----------
        name : str
            The name of the method to check for.

        Returns
        -------
        bool
            True if the method exists in the class, False otherwise.
        """
        return name in self.getMethods()

    def callMethod(self, name: str, *args, **kwargs):
        """
        Call a method on the class instance with provided arguments.

        Requires that an instance has been created using getInstance().
        Automatically handles asynchronous methods using the Coroutine wrapper.

        Parameters
        ----------
        name : str
            The name of the method to call.
        *args : tuple
            Positional arguments to pass to the method.
        **kwargs : dict
            Keyword arguments to pass to the method.

        Returns
        -------
        Any
            The return value of the method call.

        Raises
        ------
        ReflectionValueError
            If the method does not exist, instance is not initialized, or method call fails.
        """
        if not self.hasMethod(name):
            raise ReflectionValueError(f"Method '{name}' does not exist in class '{self.getClassName()}'.")

        # If no instance is provided, use the class itself
        if self.__instance is None:
            raise ReflectionValueError(f"Instance of class '{self.getClassName()}' is not initialized. Use getInstance() to create an instance before calling methods.")

        # Extract the method from the instance
        method = getattr(self.__instance, name, None)

        # Check if method is coroutine function
        if inspect.iscoroutinefunction(method):
            return Coroutine(method(*args, **kwargs)).run()

        # Call the method with provided arguments
        return method(*args, **kwargs)

    def setMethod(self, name: str, method: Callable) -> bool:
        """
        Add a new method to the reflected class.

        Validates the method name and callable before adding it to the class.
        Handles private method name mangling automatically.

        Parameters
        ----------
        name : str
            The name for the new method.
        method : Callable
            The callable object to set as a method.

        Returns
        -------
        bool
            True if the method was successfully added.

        Raises
        ------
        ReflectionValueError
            If the method name already exists, is invalid, or the object is not callable.
        """
        # Check if the method already exists
        if name in self.getMethods():
            raise ReflectionValueError(f"Method '{name}' already exists in class '{self.getClassName()}'. Use a different name or remove the existing method first.")

        # Ensure the name is a valid method name with regular expression
        if not isinstance(name, str) or not name.isidentifier() or keyword.iskeyword(name):
            raise ReflectionValueError(f"Invalid method name '{name}'. Must be a valid Python identifier and not a keyword.")

        # Ensure the method is callable
        if not callable(method):
            raise ReflectionValueError(f"Cannot set method '{name}' to a non-callable value.")

        # Handle private method name mangling
        if name.startswith("__") and not name.endswith("__"):
            class_name = self.getClassName()
            name = f"_{class_name}{name}"

        # Set the method on the class itself
        setattr(self._concrete, name, method)

        return True

    def removeMethod(self, name: str) -> bool:
        """
        Remove a method from the reflected class.

        Handles private method name mangling automatically before removal.

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
        if not self.hasMethod(name):
            raise ReflectionValueError(f"Method '{name}' does not exist in class '{self.getClassName()}'.")

        # Handle private method name mangling
        if name.startswith("__") and not name.endswith("__"):
            class_name = self.getClassName()
            name = f"_{class_name}{name}"

        # Delete the method from the class itself
        delattr(self._concrete, name)

        # Return True to indicate successful removal
        return True

    def getMethodSignature(self, name: str) -> inspect.Signature:
        """
        Get the signature of a specific method.

        Parameters
        ----------
        name : str
            The name of the method to inspect.

        Returns
        -------
        inspect.Signature
            The signature object containing parameter and return information.

        Raises
        ------
        ReflectionValueError
            If the method does not exist or is not callable.
        """
        if not self.hasMethod(name):
            raise ReflectionValueError(f"Method '{name}' does not exist in class '{self.getClassName()}'.")

        # Extract the method from the class if instance is not initialized
        method = getattr(self._concrete, name, None)

        if not callable(method):
            raise ReflectionValueError(f"'{name}' is not callable in class '{self.getClassName()}'.")

        # Get the signature of the method
        return inspect.signature(method)

    def getMethods(self) -> List[str]:
        """
        Get all method names from the reflected class.

        Combines all types of methods including instance methods, class methods,
        and static methods with different visibility levels.

        Returns
        -------
        List[str]
            A comprehensive list of all method names in the class.
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
        Get all public instance method names from the reflected class.

        Retrieves methods that are callable, not static or class methods,
        not properties, and do not start with underscores.

        Returns
        -------
        list
            A list of public instance method names.
        """
        class_name = self.getClassName()
        attributes = self._concrete.__dict__
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
        Get all public synchronous method names from the reflected class.

        Filters public methods to include only those that are not coroutine functions.

        Returns
        -------
        list
            A list of public synchronous method names.
        """
        methods = self.getPublicMethods()
        sync_methods = []
        for method in methods:
            if not inspect.iscoroutinefunction(getattr(self._concrete, method)):
                sync_methods.append(method)
        return sync_methods

    def getPublicAsyncMethods(self) -> list:
        """
        Get all public asynchronous method names from the reflected class.

        Filters public methods to include only those that are coroutine functions.

        Returns
        -------
        list
            A list of public asynchronous method names.
        """
        methods = self.getPublicMethods()
        async_methods = []
        for method in methods:
            if inspect.iscoroutinefunction(getattr(self._concrete, method)):
                async_methods.append(method)
        return async_methods

    def getProtectedMethods(self) -> list:
        """
        Get all protected instance method names from the reflected class.

        Retrieves methods that start with a single underscore, indicating
        protected visibility according to Python naming conventions.

        Returns
        -------
        list
            A list of protected instance method names.
        """
        class_name = self.getClassName()
        attributes = self._concrete.__dict__
        protected_methods = []

        # Exclude dunder, public, private attributes and properties
        for attr, value in attributes.items():
            if callable(value) and not isinstance(value, (staticmethod, classmethod)) and not isinstance(value, property):
                if attr.startswith("_") and not attr.startswith("__") and not attr.startswith(f"_{self.getClassName()}"):
                    protected_methods.append(attr)

        return protected_methods

    def getProtectedSyncMethods(self) -> list:
        """
        Get all protected synchronous method names from the reflected class.

        Filters protected methods to include only those that are not coroutine functions.

        Returns
        -------
        list
            A list of protected synchronous method names.
        """
        methods = self.getProtectedMethods()
        sync_methods = []
        for method in methods:
            if not inspect.iscoroutinefunction(getattr(self._concrete, method)):
                sync_methods.append(method)
        return sync_methods

    def getProtectedAsyncMethods(self) -> list:
        """
        Get all protected asynchronous method names from the reflected class.

        Filters protected methods to include only those that are coroutine functions.

        Returns
        -------
        list
            A list of protected asynchronous method names.
        """
        methods = self.getProtectedMethods()
        async_methods = []
        for method in methods:
            if inspect.iscoroutinefunction(getattr(self._concrete, method)):
                async_methods.append(method)
        return async_methods

    def getPrivateMethods(self) -> list:
        """
        Get all private instance method names from the reflected class.

        Retrieves methods that use Python's name mangling convention
        for private methods (class name prefix), with name mangling resolved.

        Returns
        -------
        list
            A list of private instance method names with mangling removed.
        """
        class_name = self.getClassName()
        attributes = self._concrete.__dict__
        private_methods = []

        # Exclude dunder, public, protected attributes and properties
        for attr, value in attributes.items():
            if callable(value) and not isinstance(value, (staticmethod, classmethod)) and not isinstance(value, property):
                if attr.startswith(f"_{class_name}"):
                    # Remove name mangling for cleaner output
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
            if not inspect.iscoroutinefunction(getattr(self._concrete, f"_{self.getClassName()}{method}")):
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
            if inspect.iscoroutinefunction(getattr(self._concrete, f"_{self.getClassName()}{method}")):
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
        attributes = self._concrete.__dict__
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
            if not inspect.iscoroutinefunction(getattr(self._concrete, method)):
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
            if inspect.iscoroutinefunction(getattr(self._concrete, method)):
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
        attributes = self._concrete.__dict__
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
            if not inspect.iscoroutinefunction(getattr(self._concrete, method)):
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
            if inspect.iscoroutinefunction(getattr(self._concrete, method)):
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
        attributes = self._concrete.__dict__
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
            if not inspect.iscoroutinefunction(getattr(self._concrete, f"_{self.getClassName()}{method}")):
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
            if inspect.iscoroutinefunction(getattr(self._concrete, f"_{self.getClassName()}{method}")):
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
        attributes = self._concrete.__dict__
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
            if not inspect.iscoroutinefunction(getattr(self._concrete, method)):
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
            if inspect.iscoroutinefunction(getattr(self._concrete, method)):
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
        attributes = self._concrete.__dict__
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
            if not inspect.iscoroutinefunction(getattr(self._concrete, method)):
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
            if inspect.iscoroutinefunction(getattr(self._concrete, method)):
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
        attributes = self._concrete.__dict__
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
            if not inspect.iscoroutinefunction(getattr(self._concrete, f"_{self.getClassName()}{method}")):
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
            if inspect.iscoroutinefunction(getattr(self._concrete, f"_{self.getClassName()}{method}")):
                async_methods.append(method)
        return async_methods

    def getDunderMethods(self) -> list:
        """
        Get all dunder (magic) method names from the reflected class.

        Retrieves methods that follow the double underscore naming convention,
        excluding built-in Python methods and non-callable attributes.

        Returns
        -------
        list
            A list of dunder method names available in the class.
        """
        attributes = self._concrete.__dict__
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
        Get all magic (dunder) method names from the reflected class.

        This is an alias for getDunderMethods() providing alternative naming
        for accessing double underscore methods.

        Returns
        -------
        list
            A list of magic method names available in the class.
        """
        return self.getDunderMethods()

    def getProperties(self) -> List:
        """
        Get all property names from the reflected class.

        Scans the class dictionary for property objects and returns their names
        with private attribute name mangling resolved.

        Returns
        -------
        List[str]
            A list of all property names in the class.
        """
        properties = []
        for name, prop in self._concrete.__dict__.items():
            if isinstance(prop, property):
                # Remove private attribute name mangling for cleaner output
                name_prop = name.replace(f"_{self.getClassName()}", "")
                properties.append(name_prop)
        return properties

    def getPublicProperties(self) -> List:
        """
        Get all public property names from the reflected class.

        Retrieves properties that do not start with underscores, indicating
        public visibility according to Python naming conventions.

        Returns
        -------
        List[str]
            A list of public property names with name mangling resolved.
        """
        properties = []
        cls_name = self.getClassName()
        for name, prop in self._concrete.__dict__.items():
            if isinstance(prop, property):
                if not name.startswith("_") and not name.startswith(f"_{cls_name}"):
                    properties.append(name.replace(f"_{cls_name}", ""))
        return properties

    def getProtectedProperties(self) -> List:
        """
        Get all protected property names from the reflected class.

        Retrieves properties that start with a single underscore but are not
        private (double underscore) attributes.

        Returns
        -------
        List[str]
            A list of protected property names.
        """
        properties = []
        for name, prop in self._concrete.__dict__.items():
            if isinstance(prop, property):
                if name.startswith("_") and not name.startswith("__") and not name.startswith(f"_{self.getClassName()}"):
                    properties.append(name)
        return properties

    def getPrivateProperties(self) -> List:
        """
        Get all private property names from the reflected class.

        Retrieves properties that use Python's name mangling convention
        for private attributes (class name prefix).

        Returns
        -------
        List[str]
            A list of private property names with name mangling resolved.
        """
        properties = []
        for name, prop in self._concrete.__dict__.items():
            if isinstance(prop, property):
                if name.startswith(f"_{self.getClassName()}") and not name.startswith("__"):
                    properties.append(name.replace(f"_{self.getClassName()}", ""))
        return properties

    def getProperty(self, name: str) -> Any:
        """
        Get the value of a specific property from the reflected class.

        Handles private property name mangling and validates that the
        requested attribute is actually a property object.

        Parameters
        ----------
        name : str
            The name of the property to retrieve.

        Returns
        -------
        Any
            The current value of the property.

        Raises
        ------
        ReflectionValueError
            If the property does not exist or is not accessible.
        """
        # Handle private property name mangling
        if name.startswith("__") and not name.endswith("__"):
            class_name = self.getClassName()
            name = f"_{class_name}{name}"

        if not hasattr(self._concrete, name):
            raise ReflectionValueError(f"Property '{name}' does not exist in class '{self.getClassName()}'.")

        prop = getattr(self._concrete, name)
        if not isinstance(prop, property):
            raise ReflectionValueError(f"'{name}' is not a property in class '{self.getClassName()}'.")

        return prop.fget(self._concrete)

    def getPropertySignature(self, name: str) -> inspect.Signature:
        """
        Get the signature of a specific property's getter method.

        Parameters
        ----------
        name : str
            The name of the property to inspect.

        Returns
        -------
        inspect.Signature
            The signature of the property's getter function.

        Raises
        ------
        ReflectionValueError
            If the property does not exist or is not accessible.
        """
        # Handle private property name mangling
        if name.startswith("__") and not name.endswith("__"):
            class_name = self.getClassName()
            name = f"_{class_name}{name}"

        if not hasattr(self._concrete, name):
            raise ReflectionValueError(f"Property '{name}' does not exist in class '{self.getClassName()}'.")

        prop = getattr(self._concrete, name)
        if not isinstance(prop, property):
            raise ReflectionValueError(f"'{name}' is not a property in class '{self.getClassName()}'.")

        return inspect.signature(prop.fget)

    def getPropertyDocstring(self, name: str) -> str:
        """
        Get the docstring of a specific property's getter method.

        Parameters
        ----------
        name : str
            The name of the property to inspect.

        Returns
        -------
        str or None
            The docstring of the property's getter function, or None if not defined.

        Raises
        ------
        ReflectionValueError
            If the property does not exist or is not accessible.
        """
        # Handle private property name mangling
        if name.startswith("__") and not name.endswith("__"):
            class_name = self.getClassName()
            name = f"_{class_name}{name}"

        if not hasattr(self._concrete, name):
            raise ReflectionValueError(f"Property '{name}' does not exist in class '{self.getClassName()}'.")

        prop = getattr(self._concrete, name)
        if not isinstance(prop, property):
            raise ReflectionValueError(f"'{name}' is not a property in class '{self.getClassName()}'.")

        return prop.fget.__doc__ if prop.fget else None

    def getConstructorSignature(self) -> inspect.Signature:
        """
        Get the signature of the class constructor.

        Returns
        -------
        inspect.Signature
            The signature of the __init__ method containing parameter information.
        """
        return inspect.signature(self._concrete.__init__)

    def getConstructorDependencies(self) -> ResolveArguments:
        """
        Get dependency analysis for the class constructor.

        Analyzes the constructor parameters to identify resolved and unresolved
        dependencies based on type annotations and default values.

        Returns
        -------
        ResolveArguments
            A structured representation containing resolved dependencies
            (with default values/annotations) and unresolved dependencies
            (parameters without defaults or type information).
        """
        return ReflectDependencies(self._concrete).getConstructorDependencies()

    def getMethodDependencies(self, method_name: str) -> ResolveArguments:
        """
        Get dependency analysis for a specific method.

        Analyzes the method parameters to identify resolved and unresolved
        dependencies, handling private method name mangling automatically.

        Parameters
        ----------
        method_name : str
            The name of the method to analyze.

        Returns
        -------
        ResolveArguments
            A structured representation containing resolved dependencies
            (with default values/annotations) and unresolved dependencies
            (parameters without defaults or type information).

        Raises
        ------
        ReflectionAttributeError
            If the method does not exist in the class.
        """
        # Ensure the method name is a valid identifier
        if not self.hasMethod(method_name):
            raise ReflectionAttributeError(f"Method '{method_name}' does not exist on '{self.getClassName()}'.")

        # Handle private method name mangling
        if method_name.startswith("__") and not method_name.endswith("__"):
            class_name = self.getClassName()
            method_name = f"_{class_name}{method_name}"

        # Use ReflectDependencies to get method dependencies
        return ReflectDependencies(self._concrete).getMethodDependencies(method_name)

    def reflectionInstance(self) -> ReflectionInstance:
        """
        Get a reflection wrapper for the current class instance.

        Provides access to instance-level reflection capabilities for the
        instantiated object.

        Returns
        -------
        ReflectionInstance
            A reflection wrapper for instance-level introspection operations.

        Raises
        ------
        ReflectionValueError
            If no instance has been created using getInstance().
        """
        if not self.__instance:
            raise ReflectionValueError(f"Instance of class '{self.getClassName()}' is not initialized. Use getInstance() to create an instance before calling methods.")

        return ReflectionInstance(self.__instance)