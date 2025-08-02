from abc import ABC, abstractmethod

class IReflectionCallable(ABC):

    @abstractmethod
    def getCallable(self) -> callable:
        """
        Retrieve the callable function associated with this instance.
        Returns
        -------
        callable
            The function object encapsulated by this instance.
        """
        pass

    @abstractmethod
    def getName(self) -> str:
        """
        Returns
        -------
        str
            The name of the function.
        """
        pass

    @abstractmethod
    def getModuleName(self) -> str:
        """
        Get the name of the module where the underlying function is defined.
        Returns
        -------
        str
            The name of the module in which the function was originally declared.
        """
        pass

    @abstractmethod
    def getModuleWithCallableName(self) -> str:
        """
        Get the fully qualified name of the callable, including its module.
        Returns
        -------
        str
            A string consisting of the module name and the callable name, separated by a dot.
        """
        pass

    @abstractmethod
    def getDocstring(self) -> str:
        """
        Retrieve the docstring of the callable function.
        Returns
        -------
        str
            The docstring associated with the function. Returns an empty string if no docstring is present.
        """
        pass

    @abstractmethod
    def getSourceCode(self) -> str:
        """
        Retrieve the source code of the wrapped callable.
        Returns
        -------
        str
            The source code of the callable function as a string. If the source code
            cannot be retrieved, a ReflectionAttributeError is raised.
        Raises
        ------
        ReflectionAttributeError
            If the source code cannot be obtained due to an OSError.
        """
        pass

    @abstractmethod
    def getFile(self) -> str:
        """
        Retrieve the filename where the underlying callable function is defined.
        Returns
        -------
        str
            The absolute path to the source file containing the callable.
        Raises
        ------
        TypeError
            If the underlying object is a built-in function or method, or if its source file cannot be determined.
        """
        pass

    @abstractmethod
    def call(self, *args, **kwargs):
        """
        Call the wrapped function with the provided arguments.
        If the wrapped function is asynchronous, it will be executed using `asyncio.run`.
        Parameters
        ----------
        *args : tuple
            Positional arguments to pass to the function.
        **kwargs : dict
            Keyword arguments to pass to the function.
        Returns
        -------
        Any
            The result returned by the function call.
        Raises
        ------
        Exception
            Propagates any exception raised by the called function.
        """
        pass

    @abstractmethod
    def getSignature(self):
        """
        Retrieve the signature of the callable function.
        Returns
        -------
        inspect.Signature
            An `inspect.Signature` object representing the callable's signature.
        Notes
        -----
        This method provides detailed information about the parameters of the callable,
        including their names, default values, and annotations.
        """
        pass

    @abstractmethod
    def getDependencies(self):
        """
        Analyzes the callable associated with this instance and retrieves its dependencies.
        CallableDependency
            An object containing information about the callable's dependencies, including:
            - resolved: dict
                A dictionary mapping parameter names to their resolved values (e.g., default values or injected dependencies).
            - unresolved: list of str
                A list of parameter names that could not be resolved (i.e., parameters without default values or missing annotations).
        Notes
        -----
        This method leverages the `ReflectDependencies` utility to inspect the callable and determine which dependencies are satisfied and which remain unresolved.
        """
        pass