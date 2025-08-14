from abc import ABC, abstractmethod
from orionis.services.introspection.dependencies.entities.resolve_argument import ResolveArguments

class IReflectionCallable(ABC):
    """
    Abstract base class defining the interface for callable reflection operations.

    This interface provides methods to introspect and manipulate callable objects,
    including functions, methods, and lambdas. It enables reflection capabilities
    such as source code retrieval, dependency analysis, and runtime execution.
    """

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
        Get the name of the callable function.

        Returns
        -------
        str
            The name of the function as defined in its declaration.
        """
        pass

    @abstractmethod
    def getModuleName(self) -> str:
        """
        Get the name of the module where the callable is defined.

        Returns
        -------
        str
            The name of the module in which the function was originally declared.
        """
        pass

    @abstractmethod
    def getModuleWithCallableName(self) -> str:
        """
        Get the fully qualified name of the callable.

        Combines the module name and callable name to create a complete
        identifier for the function.

        Returns
        -------
        str
            A string consisting of the module name and the callable name,
            separated by a dot (e.g., 'module.function').
        """
        pass

    @abstractmethod
    def getDocstring(self) -> str:
        """
        Retrieve the docstring of the callable function.

        Returns
        -------
        str
            The docstring associated with the function. Returns an empty 
            string if no docstring is present.
        """
        pass

    @abstractmethod
    def getSourceCode(self) -> str:
        """
        Retrieve the source code of the wrapped callable.

        Returns
        -------
        str
            The source code of the callable function as a string.

        Raises
        ------
        ReflectionAttributeError
            If the source code cannot be obtained due to an OSError or
            if the callable is built-in without accessible source.
        """
        pass

    @abstractmethod
    def getFile(self) -> str:
        """
        Retrieve the filename where the callable is defined.

        Returns
        -------
        str
            The absolute path to the source file containing the callable.

        Raises
        ------
        TypeError
            If the underlying object is a built-in function or method,
            or if its source file cannot be determined.
        """
        pass

    @abstractmethod
    def call(self, *args, **kwargs):
        """
        Execute the wrapped function with the provided arguments.

        Handles both synchronous and asynchronous callables, automatically
        running coroutines when necessary.

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
            An `inspect.Signature` object representing the callable's signature,
            including parameter names, default values, and type annotations.

        Notes
        -----
        This method provides detailed information about the parameters of the callable,
        enabling runtime inspection and validation of function arguments.
        """
        pass

    @abstractmethod
    def getDependencies(self) -> ResolveArguments:
        """
        Analyze the callable and retrieve its dependency information.

        Examines the callable's parameters to determine which dependencies
        can be resolved (have default values or type annotations) and which
        remain unresolved.

        Returns
        -------
        ResolveArguments
            An object containing information about the callable's dependencies:
            - resolved : dict
                A dictionary mapping parameter names to their resolved values
                (e.g., default values or injected dependencies).
            - unresolved : list of str
                A list of parameter names that could not be resolved
                (parameters without default values or missing annotations).

        Notes
        -----
        This method leverages the `ReflectDependencies` utility to inspect
        the callable and determine which dependencies are satisfied and
        which remain unresolved for dependency injection purposes.
        """
        pass