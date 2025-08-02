import inspect
import keyword
from typing import Any, Callable, Dict, List, Optional, Tuple, Type
from orionis.services.asynchrony.coroutines import Coroutine
from orionis.services.introspection.dependencies.entities.class_dependencies import ClassDependency
from orionis.services.introspection.dependencies.entities.method_dependencies import MethodDependency
from orionis.services.introspection.dependencies.reflection import ReflectDependencies
from orionis.services.introspection.exceptions import (
    ReflectionAttributeError,
    ReflectionTypeError,
    ReflectionValueError
)
from orionis.services.introspection.instances.contracts.reflection import IReflectionInstance

class ReflectionInstance(IReflectionInstance):

    @staticmethod
    def isInstance(instance: Any) -> bool:
        """
        Check if the given object is a valid instance according to ReflectionInstance rules.

        Parameters
        ----------
        instance : Any
            The object to check.

        Returns
        -------
        bool
            True if the object is a valid instance, False otherwise.

        Notes
        -----
        This method catches and handles exceptions internally; it does not raise.
        """
        try:
            return ReflectionInstance.ensureIsInstance(instance)
        except (ReflectionTypeError, ReflectionValueError):
            return False

    @staticmethod
    def ensureIsInstance(instance: Any) -> bool:
        """
        Validate that the provided object is a proper instance of a user-defined class.

        Parameters
        ----------
        instance : Any
            The object to validate.

        Returns
        -------
        bool
            True if the instance passes all checks.

        Raises
        ------
        ReflectionTypeError
            If the input is not a valid object instance.
        ReflectionValueError
            If the instance belongs to a disallowed module ('builtins', 'abc') or originates from '__main__'.

        Notes
        -----
        This method performs the following checks:
            1. Ensures the input is an object instance (not a class/type).
            2. Disallows instances of types defined in the 'builtins' or 'abc' modules.
            3. Disallows instances originating from the '__main__' module, requiring importable module origins.
        """

        # Ensure the provided instance is a valid object instance
        if not (isinstance(instance, object) and not isinstance(instance, type)):
            raise ReflectionTypeError(
                f"Expected an object instance, got {type(instance).__name__!r}: {instance!r}"
            )

        # Check if the instance belongs to a built-in or abstract base class
        module = type(instance).__module__
        if module in {'builtins', 'abc'}:
            raise ReflectionValueError(
                f"Instance of type '{type(instance).__name__}' belongs to disallowed module '{module}'."
            )

        # Check if the instance originates from '__main__'
        if module == '__main__':
            raise ReflectionValueError(
                "Instance originates from '__main__'; please provide an instance from an importable module."
            )

        # If all checks pass, return True
        return True

    def __init__(self, instance: Any) -> None:
        """
        Initialize the ReflectionInstance with a given object instance.

        Parameters
        ----------
        instance : Any
            The object instance to be reflected upon.

        Raises
        ------
        ReflectionTypeError
            If the provided instance is not a valid object instance.
        ReflectionValueError
            If the instance belongs to a built-in, abstract base class, or '__main__' module.
        """

        # Ensure the instance is valid
        ReflectionInstance.ensureIsInstance(instance)

        # Store the instance for reflection
        self._instance = instance

    def getInstance(self) -> Any:
        """
        Get the instance being reflected upon.

        Returns
        -------
        Any
            The object instance
        """
        return self._instance

    def getClass(self) -> Type:
        """
        Get the class of the instance.

        Returns
        -------
        Type
            The class object of the instance
        """
        return self._instance.__class__

    def getClassName(self) -> str:
        """
        Get the name of the instance's class.

        Returns
        -------
        str
            The name of the class
        """
        return self._instance.__class__.__name__

    def getModuleName(self) -> str:
        """
        Get the name of the module where the class is defined.

        Returns
        -------
        str
            The module name
        """
        return self._instance.__class__.__module__

    def getModuleWithClassName(self) -> str:
        """
        Get the name of the module where the class is defined.

        Returns
        -------
        str
            The module name
        """
        return f"{self.getModuleName()}.{self.getClassName()}"

    def getDocstring(self) -> Optional[str]:
        """
        Get the docstring of the instance's class.

        Returns
        -------
        Optional[str]
            The class docstring, or None if not available
        """
        return self._instance.__class__.__doc__

    def getBaseClasses(self) -> Tuple[Type, ...]:
        """
        Get the base classes of the instance's class.

        Returns
        -------
        Tuple[Type, ...]
            Tuple of base classes
        """
        return self._instance.__class__.__bases__

    def getSourceCode(self) -> Optional[str]:
        """
        Get the source code of the instance's class.

        Returns
        -------
        Optional[str]
            The source code if available, None otherwise
        """
        try:
            return inspect.getsource(self._instance.__class__)
        except (TypeError, OSError):
            return None

    def getFile(self) -> Optional[str]:
        """
        Get the file location where the class is defined.

        Returns
        -------
        Optional[str]
            The file path if available, None otherwise
        """
        try:
            return inspect.getfile(self._instance.__class__)
        except (TypeError, OSError):
            return None

    def getAnnotations(self) -> Dict[str, Any]:
        """
        Get type annotations of the class.

        Returns
        -------
        Dict[str, Any]
            Dictionary of attribute names and their type annotations
        """
        annotations = {}
        for k, v in self._instance.__annotations__.items():
            annotations[str(k).replace(f"_{self.getClassName()}", "")] = v
        return annotations

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
        return name in self.getAttributes()

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
        attrs = self.getAttributes()
        return attrs.get(name, None)

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
        # Ensure the name is a valid attr name with regular expression
        if not isinstance(name, str) or not name.isidentifier() or keyword.iskeyword(name):
            raise ReflectionAttributeError(f"Invalid method name '{name}'. Must be a valid Python identifier and not a keyword.")

        # Ensure the value is not callable
        if callable(value):
            raise ReflectionAttributeError(f"Cannot set attribute '{name}' to a callable. Use setMethod instead.")

        # Handle private attribute name mangling
        if name.startswith("__") and not name.endswith("__"):
            class_name = self.getClassName()
            name = f"_{class_name}{name}"

        # Check if the attribute already exists
        setattr(self._instance, name, value)

        # Return True
        return True

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
        if self.getAttribute(name) is None:
            raise ReflectionAttributeError(f"'{self.getClassName()}' object has no attribute '{name}'.")
        if name.startswith("__") and not name.endswith("__"):
            class_name = self.getClassName()
            name = f"_{class_name}{name}"
        delattr(self._instance, name)
        return True

    def getAttributes(self) -> Dict[str, Any]:
        """
        Get all attributes of the instance, including public, private, protected, and dunder attributes.

        Returns
        -------
        Dict[str, Any]
            Dictionary of all attribute names and their values
        """
        return {
            **self.getPublicAttributes(),
            **self.getProtectedAttributes(),
            **self.getPrivateAttributes(),
            **self.getDunderAttributes()
        }

    def getPublicAttributes(self) -> Dict[str, Any]:
        """
        Get all public attributes of the instance.

        Returns
        -------
        Dict[str, Any]
            Dictionary of public attribute names and their values
        """
        class_name = self.getClassName()
        attributes = vars(self._instance)
        public = {}

        # Exclude dunder, protected, and private attributes
        for attr, value in attributes.items():
            if attr.startswith("__") and attr.endswith("__"):
                continue
            if attr.startswith(f"_{class_name}"):
                continue
            if attr.startswith("_"):
                continue
            public[attr] = value

        return public

    def getProtectedAttributes(self) -> Dict[str, Any]:
        """
        Get all Protected attributes of the instance.

        Returns
        -------
        Dict[str, Any]
            Dictionary of Protected attribute names and their values
        """
        class_name = self.getClassName()
        attributes = vars(self._instance)
        protected = {}

        # Select protected attributes that start with a single underscore
        for attr, value in attributes.items():
            if attr.startswith("_") and not attr.startswith("__") and not attr.startswith(f"_{class_name}"):
                protected[attr] = value

        return protected

    def getPrivateAttributes(self) -> Dict[str, Any]:
        """
        Get all private attributes of the instance.

        Returns
        -------
        Dict[str, Any]
            Dictionary of private attribute names and their values
        """
        class_name = self.getClassName()
        attributes = vars(self._instance)
        private = {}

        # Select private attributes that start with the class name
        for attr, value in attributes.items():
            if attr.startswith(f"_{class_name}"):
                private[str(attr).replace(f"_{class_name}", "")] = value

        return private

    def getDunderAttributes(self) -> Dict[str, Any]:
        """
        Get all dunder (double underscore) attributes of the instance.

        Returns
        -------
        Dict[str, Any]
            Dictionary of dunder attribute names and their values
        """
        attributes = vars(self._instance)
        dunder = {}

        # Select dunder attributes that start and end with double underscores
        for attr, value in attributes.items():
            if attr.startswith("__") and attr.endswith("__"):
                dunder[attr] = value

        return dunder

    def getMagicAttributes(self) -> Dict[str, Any]:
        """
        Get all magic attributes of the instance.

        Returns
        -------
        Dict[str, Any]
            Dictionary of magic attribute names and their values
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

        # Hanlde private method name mangling
        if name.startswith("__") and not name.endswith("__"):
            class_name = self.getClassName()
            name = f"_{class_name}{name}"

        # Try to get the method from the instance
        method = getattr(self._instance, name, None)

        # If not found, try to get it from the class
        if method is None:
            cls = self._instance.__class__
            method = getattr(cls, name, None)

        # If still not found, raise an error
        if method is None:
            raise ReflectionAttributeError(f"Method '{name}' does not exist on '{self.getClassName()}'.")

        # Check if the method is callable
        if not callable(method):
            raise ReflectionTypeError(f"'{name}' is not callable on '{self.getClassName()}'.")

        # Check if method is coroutine function
        if inspect.iscoroutinefunction(method):
            return Coroutine(method(*args, **kwargs)).run()

        # Call the method with provided arguments
        return method(*args, **kwargs)

    def setMethod(self, name: str, method: Callable) -> bool:
        """
        Set a callable attribute method.

        Parameters
        ----------
        name : str
            The attribute name
        method : Callable
            The callable to set

        Raises
        ------
        ReflectionAttributeError
            If the attribute is not callable or already exists as a method
        """
        # Ensure the name is a valid method name with regular expression
        if not isinstance(name, str) or not name.isidentifier() or keyword.iskeyword(name):
            raise ReflectionAttributeError(f"Invalid method name '{name}'. Must be a valid Python identifier and not a keyword.")

        # Ensure the method is callable
        if not callable(method):
            raise ReflectionAttributeError(f"Cannot set attribute '{name}' to a non-callable value.")

        # Extarct the signature of the method and classtype
        sign = inspect.signature(method)
        classtype = self.getClass()

        # Check first parameter is 'cls'
        params = list(sign.parameters.values())
        if not params or params[0].name != "cls":
            raise ReflectionAttributeError(f"The first (or only) argument of the method must be named 'cls' and must be of type {classtype}.")

        # Get the expected type from the first parameter's annotation
        annotation = params[0].annotation
        if annotation != classtype:
            raise ReflectionAttributeError(
                f"The first argument has an incorrect annotation. Expected '{classtype}', but got '{annotation}'."
            )

        # Handle private method name mangling
        if name.startswith("__") and not name.endswith("__"):
            class_name = self.getClassName()
            name = f"_{class_name}{name}"

        # Check if the method already exists
        if hasattr(self._instance, name):
            raise ReflectionAttributeError(f"Attribute '{name}' already exists on '{self.getClassName()}'.")

        # Set the method on the instance
        setattr(self._instance.__class__, name, method)

        # Return True
        return True

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
        if not self.hasMethod(name):
            raise ReflectionAttributeError(f"Method '{name}' does not exist on '{self.getClassName()}'.")
        delattr(self._instance.__class__, name)

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

        # Handle private method name mangling
        if name.startswith("__") and not name.endswith("__"):
            name = f"_{self.getClassName()}{name}"

        # Check if the method exists and is callable
        method = getattr(self._instance.__class__, name)
        if callable(method):
            return inspect.signature(method)

        # If the method is not callable, raise an error
        raise ReflectionAttributeError(f"Method '{name}' is not callable on '{self.getClassName()}'.")

    def getMethodDocstring(self, name: str) -> Optional[str]:
        """
        Get the docstring of a method.

        Parameters
        ----------
        name : str
            Name of the method

        Returns
        -------
        Optional[str]
            The method docstring, or None if not available
        """

        # Handle private method name mangling
        if name.startswith("__") and not name.endswith("__"):
            class_name = self.getClassName()
            name = f"_{class_name}{name}"

        # Check if the method exists and is callable
        method = getattr(self._instance.__class__, name, None)
        if callable(method):
            return method.__doc__

        # If the method is not callable, raise an error
        raise ReflectionAttributeError(f"Method '{name}' does not exist on '{self.getClassName()}'.")

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

    def getPublicMethods(self) -> List[str]:
        """
        Get all public method names of the instance.

        Returns
        -------
        List[str]
            List of public method names
        """
        class_name = self.getClassName()
        cls = self._instance.__class__
        public_methods = []

        # Gather all class methods to exclude them
        class_methods = set()
        for name in dir(cls):
            attr = inspect.getattr_static(cls, name)
            if isinstance(attr, (staticmethod, classmethod)):
                class_methods.add(name)

        # Collect public instance methods (not static, not class, not private/protected/magic)
        for name, method in inspect.getmembers(self._instance, predicate=inspect.ismethod):
            if (
                name not in class_methods and
                not (name.startswith("__") and name.endswith("__")) and
                not name.startswith(f"_{class_name}") and
                not (name.startswith("_") and not name.startswith(f"_{class_name}"))
            ):
                public_methods.append(name)

        return public_methods

    def getPublicSyncMethods(self) -> List[str]:
        """
        Get all public synchronous method names of the instance.

        Returns
        -------
        List[str]
            List of public synchronous method names
        """
        methods = self.getPublicMethods()
        return [method for method in methods if not inspect.iscoroutinefunction(getattr(self._instance, method))]

    def getPublicAsyncMethods(self) -> List[str]:
        """
        Get all public asynchronous method names of the instance.

        Returns
        -------
        List[str]
            List of public asynchronous method names
        """
        methods = self.getPublicMethods()
        return [method for method in methods if inspect.iscoroutinefunction(getattr(self._instance, method))]

    def getProtectedMethods(self) -> List[str]:
        """
        Get all protected method names of the instance.

        Returns
        -------
        List[str]
            List of protected method names
        """
        protected_methods = []
        cls = self._instance.__class__

        # Collect protected instance methods (starting with a single underscore)
        for name, method in inspect.getmembers(self._instance, predicate=inspect.ismethod):
            # Skip static and class methods
            attr = inspect.getattr_static(cls, name)
            if isinstance(attr, (staticmethod, classmethod)):
                continue
            if name.startswith("_") and not name.startswith("__") and not name.startswith(f"_{self.getClassName()}"):
                protected_methods.append(name)

        return protected_methods

    def getProtectedSyncMethods(self) -> List[str]:
        """
        Get all protected synchronous method names of the instance.

        Returns
        -------
        List[str]
            List of protected synchronous method names
        """
        methods = self.getProtectedMethods()
        return [method for method in methods if not inspect.iscoroutinefunction(getattr(self._instance, method))]

    def getProtectedAsyncMethods(self) -> List[str]:
        """
        Get all protected asynchronous method names of the instance.

        Returns
        -------
        List[str]
            List of protected asynchronous method names
        """
        methods = self.getProtectedMethods()
        return [method for method in methods if inspect.iscoroutinefunction(getattr(self._instance, method))]

    def getPrivateMethods(self) -> List[str]:
        """
        Get all private method names of the instance.

        Returns
        -------
        List[str]
            List of private method names
        """
        class_name = self.getClassName()
        private_methods = []
        cls = self._instance.__class__

        # Collect private instance methods (starting with class name)
        for name, method in inspect.getmembers(self._instance, predicate=inspect.ismethod):
            attr = inspect.getattr_static(cls, name)
            if isinstance(attr, (staticmethod, classmethod)):
                continue
            if name.startswith(f"_{class_name}") and not name.startswith("__"):
                private_methods.append(name.replace(f"_{class_name}", ""))

        # Return private methods without the class name prefix
        return private_methods

    def getPrivateSyncMethods(self) -> List[str]:
        """
        Get all private synchronous method names of the instance.

        Returns
        -------
        List[str]
            List of private synchronous method names
        """
        class_name = self.getClassName()
        private_methods = []
        cls = self._instance.__class__

        for name, method in inspect.getmembers(self._instance, predicate=inspect.ismethod):
            attr = inspect.getattr_static(cls, name)
            if isinstance(attr, (staticmethod, classmethod)):
                continue
            if name.startswith(f"_{class_name}") and not name.startswith("__"):
                # Remove the class name prefix for the returned name
                short_name = name.replace(f"_{class_name}", "")
                if not inspect.iscoroutinefunction(method):
                    private_methods.append(short_name)
        return private_methods

    def getPrivateAsyncMethods(self) -> List[str]:
        """
        Get all private asynchronous method names of the instance.

        Returns
        -------
        List[str]
            List of private asynchronous method names
        """
        class_name = self.getClassName()
        private_methods = []
        cls = self._instance.__class__

        for name, method in inspect.getmembers(self._instance, predicate=inspect.ismethod):
            attr = inspect.getattr_static(cls, name)
            if isinstance(attr, (staticmethod, classmethod)):
                continue
            if name.startswith(f"_{class_name}") and not name.startswith("__"):
                # Remove the class name prefix for the returned name
                short_name = name.replace(f"_{class_name}", "")
                if inspect.iscoroutinefunction(method):
                    private_methods.append(short_name)
        return private_methods

    def getPublicClassMethods(self) -> List[str]:
        """
        Get all class method names of the instance.

        Returns
        -------
        List[str]
            List of class method names
        """
        cls = self._instance.__class__
        class_methods = []

        # Iterate over all attributes of the class
        for name in dir(cls):

            # Get the attribute using getattr_static to avoid triggering property getters
            attr = inspect.getattr_static(cls, name)

            # Check if the attribute is a class method
            if isinstance(attr, classmethod):

                # Check not private or protected methods
                if not name.startswith(f"_"):
                    class_methods.append(name)

        # Return the list of public class method
        return class_methods

    def getPublicClassSyncMethods(self) -> List[str]:
        """
        Get all public synchronous class method names of the instance.

        Returns
        -------
        List[str]
            List of public synchronous class method names
        """
        class_name = self.getClassName()
        cls = self._instance.__class__
        public_class_sync_methods = []

        # Iterate over all attributes of the class
        for name in dir(cls):

            # Get the attribute using getattr_static to avoid triggering property getters
            attr = inspect.getattr_static(cls, name)

            # Check if the attribute is a class method
            if isinstance(attr, classmethod):

                # Get the underlying function
                func = attr.__func__

                # Check if it's NOT a coroutine function (i.e., synchronous)
                if not inspect.iscoroutinefunction(func) and not name.startswith(f"_"):
                    public_class_sync_methods.append(str(name).replace(f"_{class_name}", ""))

        # Return the list of public synchronous class method names
        return public_class_sync_methods

    def getPublicClassAsyncMethods(self) -> List[str]:
        """
        Get all public asynchronous class method names of the instance.

        Returns
        -------
        List[str]
            List of public asynchronous class method names
        """
        class_name = self.getClassName()
        cls = self._instance.__class__
        public_class_async_methods = []

        # Iterate over all attributes of the class
        for name in dir(cls):

            # Get the attribute using getattr_static to avoid triggering property getters
            attr = inspect.getattr_static(cls, name)

            # Check if the attribute is a class method
            if isinstance(attr, classmethod):

                # Get the underlying function
                func = attr.__func__

                # Check if it's a coroutine function (i.e., asynchronous)
                if inspect.iscoroutinefunction(func) and not name.startswith(f"_"):
                    public_class_async_methods.append(str(name).replace(f"_{class_name}", ""))

        # Return the list of public asynchronous class method names
        return public_class_async_methods

    def getProtectedClassMethods(self) -> List[str]:
        """
        Get all protected class method names of the instance.

        Returns
        -------
        List[str]
            List of protected class method names
        """
        cls = self._instance.__class__
        class_methods = []

        # Iterate over all attributes of the class
        for name in dir(cls):

            # Get the attribute using getattr_static to avoid triggering property getters
            attr = inspect.getattr_static(cls, name)

            # Check if the attribute is a class method
            if isinstance(attr, classmethod):

                # Check is a protected class method
                if name.startswith(f"_") and not name.startswith("__") and not name.startswith(f"_{self.getClassName()}"):
                    class_methods.append(name)

        # Return the list of public class method
        return class_methods

    def getProtectedClassSyncMethods(self) -> List[str]:
        """
        Get all protected synchronous class method names of the instance.

        Returns
        -------
        List[str]
            List of protected synchronous class method names
        """
        class_name = self.getClassName()
        cls = self._instance.__class__
        protected_class_sync_methods = []

        # Iterate over all attributes of the class
        for name in dir(cls):

            # Get the attribute using getattr_static to avoid triggering property getters
            attr = inspect.getattr_static(cls, name)

            # Check if the attribute is a class method
            if isinstance(attr, classmethod):

                # Get the underlying function
                func = attr.__func__

                # Check if it's NOT a coroutine function (i.e., synchronous)
                if not inspect.iscoroutinefunction(func) and name.startswith(f"_") and not name.startswith(f"_{class_name}"):
                    protected_class_sync_methods.append(str(name).replace(f"_{class_name}", ""))

        # Return the list of protected class method names
        return protected_class_sync_methods

    def getProtectedClassAsyncMethods(self) -> List[str]:
        """
        Get all protected asynchronous class method names of the instance.

        Returns
        -------
        List[str]
            List of protected asynchronous class method names
        """
        class_name = self.getClassName()
        cls = self._instance.__class__
        protected_class_async_methods = []

        # Iterate over all attributes of the class
        for name in dir(cls):

            # Get the attribute using getattr_static to avoid triggering property getters
            attr = inspect.getattr_static(cls, name)

            # Check if the attribute is a class method
            if isinstance(attr, classmethod):

                # Get the underlying function
                func = attr.__func__

                # Check if it's a coroutine function (i.e., asynchronous)
                if inspect.iscoroutinefunction(func) and name.startswith(f"_") and not name.startswith(f"_{class_name}"):
                    protected_class_async_methods.append(str(name).replace(f"_{class_name}", ""))

        # Return the list of protected asynchronous class method names
        return protected_class_async_methods

    def getPrivateClassMethods(self) -> List[str]:
        """
        Get all private class method names of the instance.

        Returns
        -------
        List[str]
            List of private class method names
        """
        class_name = self.getClassName()
        cls = self._instance.__class__
        private_class_methods = []

        # Iterate over all attributes of the class
        for name in dir(cls):

            # Get the attribute using getattr_static to avoid triggering property getters
            attr = inspect.getattr_static(cls, name)

            # Check if the attribute is a class method
            if isinstance(attr, classmethod):

                # Get the underlying function
                func = attr.__func__

                # Check if a private class method
                if name.startswith(f"_{class_name}"):
                    private_class_methods.append(str(name).replace(f"_{class_name}", ""))

        # Return the list of protected class method names
        return private_class_methods

    def getPrivateClassSyncMethods(self) -> List[str]:
        """
        Get all private synchronous class method names of the instance.

        Returns
        -------
        List[str]
            List of private synchronous class method names
        """
        class_name = self.getClassName()
        cls = self._instance.__class__
        private_class_sync_methods = []

        # Iterate over all attributes of the class
        for name in dir(cls):

            # Get the attribute using getattr_static to avoid triggering property getters
            attr = inspect.getattr_static(cls, name)

            # Check if the attribute is a class method
            if isinstance(attr, classmethod):

                # Get the underlying function
                func = attr.__func__

                # Check if it's NOT a coroutine function (i.e., synchronous)
                if not inspect.iscoroutinefunction(func) and name.startswith(f"_{class_name}"):
                    private_class_sync_methods.append(str(name).replace(f"_{class_name}", ""))

        # Return the list of private synchronous class method names
        return private_class_sync_methods

    def getPrivateClassAsyncMethods(self) -> List[str]:
        """
        Get all private asynchronous class method names of the instance.

        Returns
        -------
        List[str]
            List of private asynchronous class method names
        """
        class_name = self.getClassName()
        cls = self._instance.__class__
        private_class_async_methods = []

        # Iterate over all attributes of the class
        for name in dir(cls):

            # Get the attribute using getattr_static to avoid triggering property getters
            attr = inspect.getattr_static(cls, name)

            # Check if the attribute is a class method
            if isinstance(attr, classmethod):

                # Get the underlying function
                func = attr.__func__

                # Check if it's a coroutine function (i.e., asynchronous)
                if inspect.iscoroutinefunction(func) and name.startswith(f"_{class_name}"):
                    private_class_async_methods.append(str(name).replace(f"_{class_name}", ""))

        # Return the list of private asynchronous class method names
        return private_class_async_methods

    def getPublicStaticMethods(self) -> List[str]:
        """
        Get public static method names of the instance.

        Returns
        -------
        List[str]
            List of static method names
        """
        cls = self._instance.__class__
        static_methods = []
        for name in dir(cls):
            attr = inspect.getattr_static(cls, name)
            if isinstance(attr, staticmethod) and not name.startswith(f"_"):
                static_methods.append(name)
        return static_methods

    def getPublicStaticSyncMethods(self) -> List[str]:
        """
        Get all public synchronous static method names of the instance.

        Returns
        -------
        List[str]
            List of public synchronous static method names
        """
        class_name = self.getClassName()
        cls = self._instance.__class__
        public_static_sync_methods = []

        # Iterate over all attributes of the class
        for name in dir(cls):

            # Get the attribute using getattr_static to avoid triggering property getters
            attr = inspect.getattr_static(cls, name)

            # Check if the attribute is a static method
            if isinstance(attr, staticmethod):

                # Get the underlying function
                func = attr.__func__

                # Check if it's NOT a coroutine function (i.e., synchronous)
                if not inspect.iscoroutinefunction(func) and not name.startswith(f"_"):
                    public_static_sync_methods.append(str(name).replace(f"_{class_name}", ""))

        # Return the list of public synchronous static method names
        return public_static_sync_methods

    def getPublicStaticAsyncMethods(self) -> List[str]:
        """
        Get all public asynchronous static method names of the instance.

        Returns
        -------
        List[str]
            List of public asynchronous static method names
        """
        class_name = self.getClassName()
        cls = self._instance.__class__
        public_static_async_methods = []

        # Iterate over all attributes of the class
        for name in dir(cls):

            # Get the attribute using getattr_static to avoid triggering property getters
            attr = inspect.getattr_static(cls, name)

            # Check if the attribute is a static method
            if isinstance(attr, staticmethod):

                # Get the underlying function
                func = attr.__func__

                # Check if it's a coroutine function (i.e., asynchronous)
                if inspect.iscoroutinefunction(func) and not name.startswith(f"_"):
                    public_static_async_methods.append(str(name).replace(f"_{class_name}", ""))

        # Return the list of public asynchronous static method names
        return public_static_async_methods

    def getProtectedStaticMethods(self) -> List[str]:
        """
        Get all protected static method names of the instance.

        Returns
        -------
        List[str]
            List of protected static method names
        """
        cls = self._instance.__class__
        protected_static_methods = []

        # Iterate over all attributes of the class
        for name in dir(cls):

            # Get the attribute using getattr_static to avoid triggering property getters
            attr = inspect.getattr_static(cls, name)

            # Check if the attribute is a static method
            if isinstance(attr, staticmethod) and name.startswith(f"_") and not name.startswith("__") and not name.startswith(f"_{self.getClassName()}"):
                protected_static_methods.append(name)

        return protected_static_methods

    def getProtectedStaticSyncMethods(self) -> List[str]:
        """
        Get all protected synchronous static method names of the instance.

        Returns
        -------
        List[str]
            List of protected synchronous static method names
        """
        class_name = self.getClassName()
        cls = self._instance.__class__
        protected_static_sync_methods = []

        # Iterate over all attributes of the class
        for name in dir(cls):

            # Get the attribute using getattr_static to avoid triggering property getters
            attr = inspect.getattr_static(cls, name)

            # Check if the attribute is a static method
            if isinstance(attr, staticmethod):

                # Get the underlying function
                func = attr.__func__

                # Check if it's NOT a coroutine function (i.e., synchronous)
                if not inspect.iscoroutinefunction(func) and name.startswith(f"_") and not name.startswith(f"_{class_name}"):
                    protected_static_sync_methods.append(str(name).replace(f"_{class_name}", ""))

        return protected_static_sync_methods

    def getProtectedStaticAsyncMethods(self) -> List[str]:
        """
        Get all protected asynchronous static method names of the instance.

        Returns
        -------
        List[str]
            List of protected asynchronous static method names
        """
        class_name = self.getClassName()
        cls = self._instance.__class__
        protected_static_async_methods = []

        # Iterate over all attributes of the class
        for name in dir(cls):

            # Get the attribute using getattr_static to avoid triggering property getters
            attr = inspect.getattr_static(cls, name)

            # Check if the attribute is a static method
            if isinstance(attr, staticmethod):

                # Get the underlying function
                func = attr.__func__

                # Check if it's a coroutine function (i.e., asynchronous)
                if inspect.iscoroutinefunction(func) and name.startswith(f"_") and not name.startswith(f"_{class_name}"):
                    protected_static_async_methods.append(str(name).replace(f"_{class_name}", ""))

        return protected_static_async_methods

    def getPrivateStaticMethods(self) -> List[str]:
        """
        Get all private static method names of the instance.

        Returns
        -------
        List[str]
            List of private static method names
        """
        class_name = self.getClassName()
        cls = self._instance.__class__
        private_static_methods = []

        # Iterate over all attributes of the class
        for name in dir(cls):

            # Get the attribute using getattr_static to avoid triggering property getters
            attr = inspect.getattr_static(cls, name)

            # Check if the attribute is a static method
            if isinstance(attr, staticmethod):

                # Check if a private static method
                if name.startswith(f"_{class_name}"):
                    private_static_methods.append(str(name).replace(f"_{class_name}", ""))

        return private_static_methods

    def getPrivateStaticSyncMethods(self) -> List[str]:
        """
        Get all private synchronous static method names of the instance.

        Returns
        -------
        List[str]
            List of private synchronous static method names
        """
        class_name = self.getClassName()
        cls = self._instance.__class__
        private_static_sync_methods = []

        # Iterate over all attributes of the class
        for name in dir(cls):

            # Get the attribute using getattr_static to avoid triggering property getters
            attr = inspect.getattr_static(cls, name)

            # Check if the attribute is a static method
            if isinstance(attr, staticmethod):

                # Get the underlying function
                func = attr.__func__

                # Check if it's NOT a coroutine function (i.e., synchronous)
                if not inspect.iscoroutinefunction(func) and name.startswith(f"_{class_name}"):
                    private_static_sync_methods.append(str(name).replace(f"_{class_name}", ""))

        return private_static_sync_methods

    def getPrivateStaticAsyncMethods(self) -> List[str]:
        """
        Get all private asynchronous static method names of the instance.

        Returns
        -------
        List[str]
            List of private asynchronous static method names
        """
        class_name = self.getClassName()
        cls = self._instance.__class__
        private_static_async_methods = []

        # Iterate over all attributes of the class
        for name in dir(cls):

            # Get the attribute using getattr_static to avoid triggering property getters
            attr = inspect.getattr_static(cls, name)

            # Check if the attribute is a static method
            if isinstance(attr, staticmethod):

                # Get the underlying function
                func = attr.__func__

                # Check if it's a coroutine function (i.e., asynchronous)
                if inspect.iscoroutinefunction(func) and name.startswith(f"_{class_name}"):
                    private_static_async_methods.append(str(name).replace(f"_{class_name}", ""))

        return private_static_async_methods

    def getDunderMethods(self) -> List[str]:
        """
        Get all dunder (double underscore) method names of the instance.

        Returns
        -------
        List[str]
            List of dunder method names
        """
        dunder_methods = []
        exclude = []

        # Collect dunder methods (starting and ending with double underscores)
        for name in dir(self._instance):
            if name in exclude:
                continue
            if name.startswith("__") and name.endswith("__"):
                dunder_methods.append(name)

        return dunder_methods

    def getMagicMethods(self) -> List[str]:
        """
        Get all magic method names of the instance.

        Returns
        -------
        List[str]
            List of magic method names
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
        for name, prop in self._instance.__class__.__dict__.items():
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
        for name, prop in self._instance.__class__.__dict__.items():
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
        for name, prop in self._instance.__class__.__dict__.items():
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
        for name, prop in self._instance.__class__.__dict__.items():
            if isinstance(prop, property):
                if name.startswith(f"_{self.getClassName()}") and not name.startswith("__"):
                    properties.append(name.replace(f"_{self.getClassName()}", ""))
        return properties

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
        # Check if the property name is valid
        if name in self.getProperties():

            # Handle private property name mangling
            if name.startswith("__") and not name.endswith("__"):
                class_name = self.getClassName()
                name = f"_{class_name}{name}"

            # Return the property value from the instance
            return getattr(self._instance, name, None)

        # If the property does not exist, raise an error
        raise ReflectionAttributeError(f"Property '{name}' does not exist on '{self.getClassName()}'.")

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
        # Handle private property name mangling
        original_name = name
        if name.startswith("__") and not name.endswith("__"):
            class_name = self.getClassName()
            name = f"_{class_name}{name}"

        # Check if the property exists
        prop = getattr(self._instance.__class__, name, None)
        if isinstance(prop, property):
            return inspect.signature(prop.fget)

        # If the property does not exist, raise an error
        raise ReflectionAttributeError(f"Property '{original_name}' does not exist on '{self.getClassName()}'.")

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
        # Handle private property name mangling
        original_name = name
        if name.startswith("__") and not name.endswith("__"):
            class_name = self.getClassName()
            name = f"_{class_name}{name}"

        # Check if the property exists
        prop = getattr(self._instance.__class__, name, None)
        if isinstance(prop, property):
            return prop.fget.__doc__ or ""

        # If the property does not exist, raise an error
        raise ReflectionAttributeError(f"Property '{original_name}' does not exist on '{self.getClassName()}'.")

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
        return ReflectDependencies(self._instance.__class__).getConstructorDependencies()

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
        return ReflectDependencies(self._instance).getMethodDependencies(method_name)