import inspect
from orionis.services.asynchrony.coroutines import Coroutine
from orionis.services.introspection.callables.contracts.reflection import IReflectionCallable
from orionis.services.introspection.dependencies.entities.callable_dependencies import CallableDependency
from orionis.services.introspection.dependencies.reflection import ReflectDependencies
from orionis.services.introspection.exceptions import (
    ReflectionAttributeError,
    ReflectionTypeError
)

class ReflectionCallable(IReflectionCallable):

    def __init__(self, fn: callable) -> None:
        """
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
        This constructor initializes the ReflectionCallable with the provided callable object.
        It ensures that the input is a valid function, method, or lambda, and raises an error otherwise.
        """
        if not (inspect.isfunction(fn) or inspect.ismethod(fn) or (callable(fn) and hasattr(fn, "__code__"))):
            raise ReflectionTypeError(f"Expected a function, method, or lambda, got {type(fn).__name__}")
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
        Returns
        -------
        str
            The name of the function.
        """
        return self.__function.__name__

    def getModuleName(self) -> str:
        """
        Get the name of the module where the underlying function is defined.
        Returns
        -------
        str
            The name of the module in which the function was originally declared.
        """
        return self.__function.__module__

    def getModuleWithCallableName(self) -> str:
        """
        Get the fully qualified name of the callable, including its module.
        Returns
        -------
        str
            A string consisting of the module name and the callable name, separated by a dot.
        """
        return f"{self.getModuleName()}.{self.getName()}"

    def getDocstring(self) -> str:
        """
        Retrieve the docstring of the callable function.
        Returns
        -------
        str
            The docstring associated with the function. Returns an empty string if no docstring is present.
        """
        return self.__function.__doc__ or ""

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
        try:
            return inspect.getsource(self.__function)
        except OSError as e:
            raise ReflectionAttributeError(f"Could not retrieve source code: {e}")

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
        return inspect.getfile(self.__function)

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
        if inspect.iscoroutinefunction(self.__function):
            return Coroutine(self.__function(*args, **kwargs)).run()
        return self.__function(*args, **kwargs)

    def getSignature(self) -> inspect.Signature:
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
        return inspect.signature(self.__function)

    def getDependencies(self) -> CallableDependency:
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
        return ReflectDependencies().getCallableDependencies(self.__function)