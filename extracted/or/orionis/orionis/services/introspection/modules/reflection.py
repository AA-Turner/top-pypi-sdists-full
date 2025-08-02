import importlib
import inspect
import keyword
from orionis.services.introspection.exceptions import (
    ReflectionTypeError,
    ReflectionValueError
)
from orionis.services.introspection.modules.contracts.reflection import IReflectionModule

class ReflectionModule(IReflectionModule):

    def __init__(self, module: str):
        """
        Parameters
        ----------
        module : str
            The name of the module to import and reflect upon.
        Raises
        ------
        ReflectionTypeError
            If `module` is not a non-empty string or if the module cannot be imported.
        Notes
        -----
        This constructor attempts to import the specified module using `importlib.import_module`.
        If the import fails or the module name is invalid, a `ReflectionTypeError` is raised.
        """
        if not isinstance(module, str) or not module.strip():
            raise ReflectionTypeError(f"Module name must be a non-empty string, got {repr(module)}")
        try:
            self.__module = importlib.import_module(module)
        except Exception as e:
            raise ReflectionTypeError(f"Failed to import module '{module}': {e}") from e

    def getModule(self):
        """
        Returns the module object.

        Returns
        -------
        module
            The imported module object.
        """
        return self.__module

    def hasClass(self, class_name: str) -> bool:
        """
        Check if the module contains a class with the specified name.

        Parameters
        ----------
        class_name : str
            The name of the class to check for.

        Returns
        -------
        bool
            True if the class exists in the module, False otherwise.
        """
        return class_name in self.getClasses()

    def getClass(self, class_name: str):
        """
        Get a class by its name from the module.

        Parameters
        ----------
        class_name : str
            The name of the class to retrieve.

        Returns
        -------
        type
            The class object if found, None otherwise.
        """
        classes = self.getClasses()
        if class_name in classes:
            return classes[class_name]

        return None

    def setClass(self, class_name: str, cls: type) -> bool:
        """
        Set a class in the module.

        Parameters
        ----------
        class_name : str
            The name of the class to set.
        cls : type
            The class object to set.

        Raises
        ------
        ValueError
            If `cls` is not a class or if `class_name` is not a valid identifier.
        """
        if not isinstance(cls, type):
            raise ReflectionValueError(f"Expected a class type, got {type(cls)}")
        if not class_name.isidentifier():
            raise ReflectionValueError(f"Invalid class name '{class_name}'. Must be a valid identifier.")
        if keyword.iskeyword(class_name):
            raise ReflectionValueError(f"Class name '{class_name}' is a reserved keyword.")

        setattr(self.__module, class_name, cls)
        return True

    def removeClass(self, class_name: str) -> bool:
        """
        Remove a class from the module.

        Parameters
        ----------
        class_name : str
            The name of the class to remove.

        Raises
        ------
        ValueError
            If `class_name` is not a valid identifier or if the class does not exist.
        """
        if class_name not in self.getClasses():
            raise ValueError(f"Class '{class_name}' does not exist in module '{self.__module.__name__}'")

        delattr(self.__module, class_name)
        return True

    def initClass(self, class_name: str, *args, **kwargs):
        """
        Initialize a class from the module with the given arguments.

        Parameters
        ----------
        class_name : str
            The name of the class to initialize.
        *args
            Positional arguments to pass to the class constructor.
        **kwargs
            Keyword arguments to pass to the class constructor.

        Returns
        -------
        object
            An instance of the class initialized with the provided arguments.

        Raises
        ------
        ReflectionValueError
            If the class does not exist or if the class name is not a valid identifier.
        """

        cls = self.getClass(class_name)
        if cls is None:
            raise ReflectionValueError(f"Class '{class_name}' does not exist in module '{self.__module.__name__}'")

        return cls(*args, **kwargs)

    def getClasses(self) -> dict:
        """
        Returns a dictionary of classes defined in the module.

        Returns
        -------
        dict
            A dictionary where keys are class names and values are class objects.
        """
        classes = {}

        # Check if it's a module
        for k, v in self.__module.__dict__.items():
            if isinstance(v, type) and issubclass(v, object):
                classes[k] = v

        # Return the dictionary of classes
        return classes

    def getPublicClasses(self) -> dict:
        """
        Returns a dictionary of public classes defined in the module.

        Returns
        -------
        dict
            A dictionary where keys are class names and values are class objects.
        """
        public_classes = {}
        for k, v in self.getClasses().items():
            if not str(k).startswith('_'):
                public_classes[k] = v
        return public_classes

    def getProtectedClasses(self) -> dict:
        """
        Returns a dictionary of protected classes defined in the module.

        Returns
        -------
        dict
            A dictionary where keys are class names and values are class objects.
        """
        protected_classes = {}
        for k, v in self.getClasses().items():
            if str(k).startswith('_') and not str(k).startswith('__'):
                protected_classes[k] = v

        return protected_classes

    def getPrivateClasses(self) -> dict:
        """
        Returns a dictionary of private classes defined in the module.

        Returns
        -------
        dict
            A dictionary where keys are class names and values are class objects.
        """
        private_classes = {}
        for k, v in self.getClasses().items():
            if str(k).startswith('__') and not str(k).endswith('__'):
                private_classes[k] = v

        return private_classes

    def getConstant(self, constant_name: str):
        """
        Get a constant by its name from the module.

        Parameters
        ----------
        constant_name : str
            The name of the constant to retrieve.

        Returns
        -------
        Any
            The value of the constant if found, None otherwise.
        """
        constants = self.getConstants()
        if constant_name in constants:
            return constants[constant_name]

        return None

    def getConstants(self) -> dict:
        """
        Returns a dictionary of constants defined in the module.

        Returns
        -------
        dict
            A dictionary where keys are constant names and values are their values.
        """
        constants = {}
        for k, v in self.__module.__dict__.items():
            if not callable(v) and k.isupper() and not keyword.iskeyword(k):
                constants[k] = v

        return constants

    def getPublicConstants(self) -> dict:
        """
        Returns a dictionary of public constants defined in the module.

        Returns
        -------
        dict
            A dictionary where keys are constant names and values are their values.
        """
        public_constants = {}
        for k, v in self.getConstants().items():
            if not str(k).startswith('_'):
                public_constants[k] = v

        return public_constants

    def getProtectedConstants(self) -> dict:
        """
        Returns a dictionary of protected constants defined in the module.

        Returns
        -------
        dict
            A dictionary where keys are constant names and values are their values.
        """
        protected_constants = {}
        for k, v in self.getConstants().items():
            if str(k).startswith('_') and not str(k).startswith('__'):
                protected_constants[k] = v

        return protected_constants

    def getPrivateConstants(self) -> dict:
        """
        Returns a dictionary of private constants defined in the module.

        Returns
        -------
        dict
            A dictionary where keys are constant names and values are their values.
        """
        private_constants = {}
        for k, v in self.getConstants().items():
            if str(k).startswith('__') and not str(k).endswith('__'):
                private_constants[k] = v

        return private_constants

    def getFunctions(self) -> dict:
        """
        Returns a dictionary of functions defined in the module.

        Returns
        -------
        dict
            A dictionary where keys are function names and values are function objects.
        """
        functions = {}
        for k, v in self.__module.__dict__.items():
            if callable(v):
                if hasattr(v, '__code__'):
                    functions[k] = v

        return functions

    def getPublicFunctions(self) -> dict:
        """
        Returns a dictionary of public functions defined in the module.

        Returns
        -------
        dict
            A dictionary where keys are function names and values are function objects.
        """
        public_functions = {}
        for k, v in self.getFunctions().items():
            if not str(k).startswith('_'):
                public_functions[k] = v

        return public_functions

    def getPublicSyncFunctions(self) -> dict:
        """
        Returns a dictionary of public synchronous functions defined in the module.

        Returns
        -------
        dict
            A dictionary where keys are function names and values are function objects.
        """
        sync_functions = {}
        for k, v in self.getPublicFunctions().items():
            if not v.__code__.co_flags & 0x80:
                sync_functions[k] = v
        return sync_functions

    def getPublicAsyncFunctions(self) -> dict:
        """
        Returns a dictionary of public asynchronous functions defined in the module.

        Returns
        -------
        dict
            A dictionary where keys are function names and values are function objects.
        """
        async_functions = {}
        for k, v in self.getPublicFunctions().items():
            if v.__code__.co_flags & 0x80:
                async_functions[k] = v
        return async_functions

    def getProtectedFunctions(self) -> dict:
        """
        Returns a dictionary of protected functions defined in the module.

        Returns
        -------
        dict
            A dictionary where keys are function names and values are function objects.
        """
        protected_functions = {}
        for k, v in self.getFunctions().items():
            if str(k).startswith('_') and not str(k).startswith('__'):
                protected_functions[k] = v

        return protected_functions

    def getProtectedSyncFunctions(self) -> dict:
        """
        Returns a dictionary of protected synchronous functions defined in the module.

        Returns
        -------
        dict
            A dictionary where keys are function names and values are function objects.
        """
        sync_functions = {}
        for k, v in self.getProtectedFunctions().items():
            if not v.__code__.co_flags & 0x80:
                sync_functions[k] = v
        return sync_functions

    def getProtectedAsyncFunctions(self) -> dict:
        """
        Returns a dictionary of protected asynchronous functions defined in the module.

        Returns
        -------
        dict
            A dictionary where keys are function names and values are function objects.
        """
        async_functions = {}
        for k, v in self.getProtectedFunctions().items():
            if v.__code__.co_flags & 0x80:
                async_functions[k] = v
        return async_functions

    def getPrivateFunctions(self) -> dict:
        """
        Returns a dictionary of private functions defined in the module.

        Returns
        -------
        dict
            A dictionary where keys are function names and values are function objects.
        """
        private_functions = {}
        for k, v in self.getFunctions().items():
            if str(k).startswith('__') and not str(k).endswith('__'):
                private_functions[k] = v

        return private_functions

    def getPrivateSyncFunctions(self) -> dict:
        """
        Returns a dictionary of private synchronous functions defined in the module.

        Returns
        -------
        dict
            A dictionary where keys are function names and values are function objects.
        """
        sync_functions = {}
        for k, v in self.getPrivateFunctions().items():
            if not v.__code__.co_flags & 0x80:
                sync_functions[k] = v
        return sync_functions

    def getPrivateAsyncFunctions(self) -> dict:
        """
        Returns a dictionary of private asynchronous functions defined in the module.

        Returns
        -------
        dict
            A dictionary where keys are function names and values are function objects.
        """
        async_functions = {}
        for k, v in self.getPrivateFunctions().items():
            if v.__code__.co_flags & 0x80:
                async_functions[k] = v
        return async_functions

    def getImports(self) -> dict:
        """
        Returns a dictionary of imported modules in the module.

        Returns
        -------
        dict
            A dictionary where keys are import names and values are module objects.
        """
        imports = {}
        for k, v in self.__module.__dict__.items():
            if isinstance(v, type(importlib)):
                imports[k] = v

        return imports

    def getFile(self) -> str:
        """
        Returns the file name of the module.

        Returns
        -------
        str
            The file name of the module.
        """
        return inspect.getfile(self.__module)

    def getSourceCode(self) -> str:
        """
        Returns the source code of the module.

        Returns
        -------
        str
            The source code of the module.
        """
        try:
            with open(self.getFile(), 'r', encoding='utf-8') as file:
                return file.read()
        except Exception as e:
            raise ReflectionValueError(f"Failed to read source code for module '{self.__module.__name__}': {e}") from e
