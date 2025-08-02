from abc import ABC, abstractmethod

class IReflectionModule(ABC):

    @abstractmethod
    def getModule(self):
        """
        Returns the module object.

        Returns
        -------
        module
            The imported module object.
        """
        pass

    @abstractmethod
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
        pass

    @abstractmethod
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
        pass

    @abstractmethod
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
        pass

    @abstractmethod
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
        pass

    @abstractmethod
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
        pass

    @abstractmethod
    def getClasses(self) -> dict:
        """
        Returns a dictionary of classes defined in the module.

        Returns
        -------
        dict
            A dictionary where keys are class names and values are class objects.
        """
        pass

    @abstractmethod
    def getPublicClasses(self) -> dict:
        """
        Returns a dictionary of public classes defined in the module.

        Returns
        -------
        dict
            A dictionary where keys are class names and values are class objects.
        """
        pass

    @abstractmethod
    def getProtectedClasses(self) -> dict:
        """
        Returns a dictionary of protected classes defined in the module.

        Returns
        -------
        dict
            A dictionary where keys are class names and values are class objects.
        """
        pass

    @abstractmethod
    def getPrivateClasses(self) -> dict:
        """
        Returns a dictionary of private classes defined in the module.

        Returns
        -------
        dict
            A dictionary where keys are class names and values are class objects.
        """
        pass

    @abstractmethod
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
        pass

    @abstractmethod
    def getConstants(self) -> dict:
        """
        Returns a dictionary of constants defined in the module.

        Returns
        -------
        dict
            A dictionary where keys are constant names and values are their values.
        """
        pass

    @abstractmethod
    def getPublicConstants(self) -> dict:
        """
        Returns a dictionary of public constants defined in the module.

        Returns
        -------
        dict
            A dictionary where keys are constant names and values are their values.
        """
        pass

    @abstractmethod
    def getProtectedConstants(self) -> dict:
        """
        Returns a dictionary of protected constants defined in the module.

        Returns
        -------
        dict
            A dictionary where keys are constant names and values are their values.
        """
        pass

    @abstractmethod
    def getPrivateConstants(self) -> dict:
        """
        Returns a dictionary of private constants defined in the module.

        Returns
        -------
        dict
            A dictionary where keys are constant names and values are their values.
        """
        pass

    @abstractmethod
    def getFunctions(self) -> dict:
        """
        Returns a dictionary of functions defined in the module.

        Returns
        -------
        dict
            A dictionary where keys are function names and values are function objects.
        """
        pass

    @abstractmethod
    def getPublicFunctions(self) -> dict:
        """
        Returns a dictionary of public functions defined in the module.

        Returns
        -------
        dict
            A dictionary where keys are function names and values are function objects.
        """
        pass

    @abstractmethod
    def getPublicSyncFunctions(self) -> dict:
        """
        Returns a dictionary of public synchronous functions defined in the module.

        Returns
        -------
        dict
            A dictionary where keys are function names and values are function objects.
        """
        pass

    @abstractmethod
    def getPublicAsyncFunctions(self) -> dict:
        """
        Returns a dictionary of public asynchronous functions defined in the module.

        Returns
        -------
        dict
            A dictionary where keys are function names and values are function objects.
        """
        pass

    @abstractmethod
    def getProtectedFunctions(self) -> dict:
        """
        Returns a dictionary of protected functions defined in the module.

        Returns
        -------
        dict
            A dictionary where keys are function names and values are function objects.
        """
        pass

    @abstractmethod
    def getProtectedSyncFunctions(self) -> dict:
        """
        Returns a dictionary of protected synchronous functions defined in the module.

        Returns
        -------
        dict
            A dictionary where keys are function names and values are function objects.
        """
        pass

    @abstractmethod
    def getProtectedAsyncFunctions(self) -> dict:
        """
        Returns a dictionary of protected asynchronous functions defined in the module.

        Returns
        -------
        dict
            A dictionary where keys are function names and values are function objects.
        """
        pass

    @abstractmethod
    def getPrivateFunctions(self) -> dict:
        """
        Returns a dictionary of private functions defined in the module.

        Returns
        -------
        dict
            A dictionary where keys are function names and values are function objects.
        """
        pass

    @abstractmethod
    def getPrivateSyncFunctions(self) -> dict:
        """
        Returns a dictionary of private synchronous functions defined in the module.

        Returns
        -------
        dict
            A dictionary where keys are function names and values are function objects.
        """
        pass

    @abstractmethod
    def getPrivateAsyncFunctions(self) -> dict:
        """
        Returns a dictionary of private asynchronous functions defined in the module.

        Returns
        -------
        dict
            A dictionary where keys are function names and values are function objects.
        """
        pass

    @abstractmethod
    def getImports(self) -> dict:
        """
        Returns a dictionary of imported modules in the module.

        Returns
        -------
        dict
            A dictionary where keys are import names and values are module objects.
        """
        pass

    @abstractmethod
    def getFile(self) -> str:
        """
        Returns the file name of the module.

        Returns
        -------
        str
            The file name of the module.
        """
        pass

    @abstractmethod
    def getSourceCode(self) -> str:
        """
        Returns the source code of the module.

        Returns
        -------
        str
            The source code of the module.
        """
        pass
