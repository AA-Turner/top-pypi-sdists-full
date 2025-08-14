import inspect
from orionis.services.asynchrony.coroutines import Coroutine
from orionis.services.introspection.callables.contracts.reflection import IReflectionCallable
from orionis.services.introspection.dependencies.entities.resolve_argument import ResolveArguments
from orionis.services.introspection.dependencies.reflection import ReflectDependencies
from orionis.services.introspection.exceptions import (
    ReflectionAttributeError,
    ReflectionTypeError
)

class ReflectionCallable(IReflectionCallable):
    """
    Concrete implementation of callable reflection operations.

    This class provides comprehensive introspection capabilities for callable objects,
    including functions, methods, and lambdas. It enables runtime analysis of callable
    properties, dependency injection, and execution management for both synchronous
    and asynchronous callables.

    Parameters
    ----------
    fn : callable
        The function, method, or lambda to be wrapped for reflection operations.

    Raises
    ------
    ReflectionTypeError
        If `fn` is not a function, method, or lambda with the required attributes.
    """

    def __init__(self, fn: callable) -> None:
        """
        Initialize the reflection wrapper with a callable object.

        Validates that the provided object is a valid callable (function, method,
        or lambda) and stores it for reflection operations.

        Parameters
        ----------
        fn : callable
            The function, method, or lambda to be wrapped.

        Raises
        ------
        ReflectionTypeError
            If `fn` is not a function, method, or lambda.

        Notes
        -----
        This constructor performs type validation to ensure that only valid
        callable objects are wrapped. Built-in functions and objects without
        the `__code__` attribute are rejected.
        """

        # Validate that the input is a proper callable with introspectable attributes
        if not (inspect.isfunction(fn) or inspect.ismethod(fn) or (callable(fn) and hasattr(fn, "__code__"))):
            raise ReflectionTypeError(f"Expected a function, method, or lambda, got {type(fn).__name__}")

        # Store the callable for reflection operations
        self.__function = fn

    def getCallable(self) -> callable:
        """
        Retrieve the callable function associated with this instance.

        Returns
        -------
        callable
            The function object encapsulated by this instance.
        """
        return self.__function

    def getName(self) -> str:
        """
        Get the name of the callable function.

        Returns
        -------
        str
            The name of the function as defined in its declaration.
        """
        return self.__function.__name__

    def getModuleName(self) -> str:
        """
        Get the name of the module where the callable is defined.

        Returns
        -------
        str
            The name of the module in which the function was originally declared.
        """
        return self.__function.__module__

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
        return f"{self.getModuleName()}.{self.getName()}"

    def getDocstring(self) -> str:
        """
        Retrieve the docstring of the callable function.

        Returns
        -------
        str
            The docstring associated with the function. Returns an empty 
            string if no docstring is present.
        """
        return self.__function.__doc__ or ""

    def getSourceCode(self) -> str:
        """
        Retrieve the source code of the wrapped callable.

        Uses Python's inspect module to extract the complete source code
        of the callable function from its definition file.

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
        try:
            return inspect.getsource(self.__function)
        except OSError as e:
            # Re-raise as a more specific reflection error for better error handling
            raise ReflectionAttributeError(f"Could not retrieve source code: {e}")

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
        return inspect.getfile(self.__function)

    def call(self, *args, **kwargs):
        """
        Execute the wrapped function with the provided arguments.

        Automatically detects whether the callable is synchronous or asynchronous
        and handles execution appropriately. For coroutine functions, uses the
        Coroutine wrapper to manage async execution.

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

        # Check if the function is a coroutine and handle async execution
        if inspect.iscoroutinefunction(self.__function):
            return Coroutine(self.__function(*args, **kwargs)).run()

        # For regular functions, call directly
        return self.__function(*args, **kwargs)

    def getSignature(self) -> inspect.Signature:
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
        return inspect.signature(self.__function)

    def getDependencies(self) -> ResolveArguments:
        """
        Analyze the callable and retrieve its dependency information.

        Examines the callable's parameters to determine which dependencies
        can be resolved (have default values or type annotations) and which
        remain unresolved for dependency injection purposes.

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
        return ReflectDependencies(self.__function).getCallableDependencies()