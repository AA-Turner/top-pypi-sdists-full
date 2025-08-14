from abc import ABC, abstractmethod
from orionis.services.introspection.dependencies.entities.resolve_argument import ResolveArguments

class IReflectDependencies(ABC):
    """
    Abstract interface for reflecting on class and method dependencies.

    This interface defines methods for retrieving dependency information from
    the constructor and methods of a class, distinguishing between resolved and
    unresolved dependencies.
    """

    @abstractmethod
    def getConstructorDependencies(self) -> ResolveArguments:
        """
        Inspects the constructor (__init__) method of the target class to identify and categorize
        its parameter dependencies into resolved and unresolved categories.

        This method analyzes the constructor's signature to determine which parameters can be
        automatically resolved (those with type annotations or default values) and which require
        explicit provision during instantiation.

        Returns
        -------
        ResolveArguments
            An object containing two dictionaries:
            - resolved: Dict[str, Argument] mapping parameter names to Argument objects for
              parameters that have type annotations or default values and can be automatically resolved.
            - unresolved: Dict[str, Argument] mapping parameter names to Argument objects for
              parameters that lack both type annotations and default values, requiring manual resolution.

        Raises
        ------
        ReflectionValueError
            If the target object's constructor signature cannot be inspected or if the target
            is not callable.

        Notes
        -----
        Parameters named 'self', 'cls', 'args', 'kwargs', and variadic parameters (*args, **kwargs)
        are automatically excluded from dependency analysis as they are not relevant for
        dependency injection purposes.
        """
        pass

    @abstractmethod
    def getMethodDependencies(self, method_name: str) -> ResolveArguments:
        """
        Inspects a specific method of the target class to identify and categorize
        its parameter dependencies into resolved and unresolved categories.

        This method analyzes the specified method's signature to determine which parameters
        can be automatically resolved (those with type annotations or default values) and
        which require explicit provision during method invocation.

        Parameters
        ----------
        method_name : str
            The name of the method within the target class to inspect for dependencies.
            The method must exist as an attribute of the target object.

        Returns
        -------
        ResolveArguments
            An object containing two dictionaries:
            - resolved: Dict[str, Argument] mapping parameter names to Argument objects for
              parameters that have type annotations or default values and can be automatically resolved.
            - unresolved: Dict[str, Argument] mapping parameter names to Argument objects for
              parameters that lack both type annotations and default values, requiring manual resolution.

        Raises
        ------
        ReflectionValueError
            If the specified method does not exist on the target object, if the method's
            signature cannot be inspected, or if the target is not callable.
        AttributeError
            If the method_name does not correspond to an existing attribute on the target object.

        Notes
        -----
        Parameters named 'self', 'cls', 'args', 'kwargs', and variadic parameters (*args, **kwargs)
        are automatically excluded from dependency analysis as they are not relevant for
        dependency injection purposes.
        """
        pass

    def getCallableDependencies(self) -> ResolveArguments:
        """
        Inspects a callable target (function, lambda, or other callable object) to identify
        and categorize its parameter dependencies into resolved and unresolved categories.

        This method analyzes the callable's signature to determine which parameters can be
        automatically resolved (those with type annotations or default values) and which
        require explicit provision during function invocation.

        Returns
        -------
        ResolveArguments
            An object containing two dictionaries:
            - resolved: Dict[str, Argument] mapping parameter names to Argument objects for
              parameters that have type annotations or default values and can be automatically resolved.
            - unresolved: Dict[str, Argument] mapping parameter names to Argument objects for
              parameters that lack both type annotations and default values, requiring manual resolution.

        Raises
        ------
        ReflectionValueError
            If the target object is not callable or if the callable's signature cannot be inspected.

        Notes
        -----
        Parameters named 'self', 'cls', 'args', 'kwargs', and variadic parameters (*args, **kwargs)
        are automatically excluded from dependency analysis as they are not relevant for
        dependency injection purposes.
        """
        pass