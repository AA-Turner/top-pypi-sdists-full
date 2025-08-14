from abc import ABC, abstractmethod
from typing import Any, Callable, Optional
from orionis.container.enums.lifetimes import Lifetime
from orionis.container.entities.binding import Binding
from orionis.services.introspection.dependencies.entities.resolve_argument import ResolveArguments

class IContainer(ABC):
    """
    IContainer is an interface that defines the structure for a dependency injection container.
    It provides methods for registering and resolving services with different lifetimes.
    """

    @abstractmethod
    def singleton(
        self,
        abstract: Callable[..., Any],
        concrete: Callable[..., Any],
        *,
        alias: str = None,
        enforce_decoupling: bool = False
    ) -> Optional[bool]:
        """
        Registers a service with a singleton lifetime.

        Parameters
        ----------
        abstract : Callable[..., Any]
            The abstract base type or interface to be bound.
        concrete : Callable[..., Any]
            The concrete implementation to associate with the abstract type.
        alias : str, optional
            An alternative name to register the service under. If not provided, the abstract's class name is used.
        enforce_decoupling : bool, optional
            Whether to enforce that concrete is not a subclass of abstract.

        Returns
        -------
        bool
            True if the service was registered successfully.
        """
        pass

    @abstractmethod
    def transient(
        self,
        abstract: Callable[..., Any],
        concrete: Callable[..., Any],
        *,
        alias: str = None,
        enforce_decoupling: bool = False
    ) -> Optional[bool]:
        """
        Registers a service with a transient lifetime.

        Parameters
        ----------
        abstract : Callable[..., Any]
            The abstract base type or interface to be bound.
        concrete : Callable[..., Any]
            The concrete implementation to associate with the abstract type.
        alias : str, optional
            An alternative name to register the service under. If not provided, the abstract's class name is used.
        enforce_decoupling : bool, optional
            Whether to enforce that concrete is not a subclass of abstract.

        Returns
        -------
        bool
            True if the service was registered successfully.
        """
        pass

    @abstractmethod
    def scoped(
        self,
        abstract: Callable[..., Any],
        concrete: Callable[..., Any],
        *,
        alias: str = None,
        enforce_decoupling: bool = False
    ) -> Optional[bool]:
        """
        Registers a service with a scoped lifetime.

        Parameters
        ----------
        abstract : Callable[..., Any]
            The abstract base type or interface to be bound.
        concrete : Callable[..., Any]
            The concrete implementation to associate with the abstract type.
        alias : str, optional
            An alternative name to register the service under. If not provided, the abstract's class name is used.
        enforce_decoupling : bool, optional
            Whether to enforce that concrete is not a subclass of abstract.

        Returns
        -------
        bool
            True if the service was registered successfully.
        """
        pass

    @abstractmethod
    def instance(
        self,
        abstract: Callable[..., Any],
        instance: Any,
        *,
        alias: str = None,
        enforce_decoupling: bool = False
    ) -> Optional[bool]:
        """
        Registers an instance of a class or interface in the container.

        Parameters
        ----------
        abstract : Callable[..., Any]
            The abstract class or interface to associate with the instance.
        instance : Any
            The concrete instance to register.
        alias : str, optional
            An optional alias to register the instance under. If not provided,
            the abstract's `__name__` attribute will be used as the alias if available.
        enforce_decoupling : bool, optional
            Whether to enforce that instance's class is not a subclass of abstract.

        Returns
        -------
        bool
            True if the instance was successfully registered.
        """
        pass

    @abstractmethod
    def callable(
        self,
        alias: str,
        fn: Callable[..., Any],
        *,
        lifetime: Lifetime = Lifetime.TRANSIENT
    ) -> Optional[bool]:
        """
        Registers a function or factory under a given alias.

        Parameters
        ----------
        alias : str
            The alias to register the function under.
        fn : Callable[..., Any]
            The function or factory to register.
        lifetime : Lifetime, optional
            The lifetime of the function registration (default is TRANSIENT).

        Returns
        -------
        bool
            True if the function was registered successfully.
        """
        pass

    @abstractmethod
    def bound(
        self,
        abstract_or_alias: Any
    ) -> bool:
        """
        Checks if a service (by abstract type or alias) is registered in the container.

        Parameters
        ----------
        abstract_or_alias : Any
            The abstract class, interface, or alias (str) to check for registration.

        Returns
        -------
        bool
            True if the service is registered (either as an abstract type or alias), False otherwise.
        """
        pass

    @abstractmethod
    def getBinding(
        self,
        abstract_or_alias: Any
    ) -> Optional[Binding]:
        """
        Retrieves the binding for the requested abstract type or alias.

        Parameters
        ----------
        abstract_or_alias : Any
            The abstract class, interface, or alias (str) to retrieve.

        Returns
        -------
        Binding
            The binding associated with the requested abstract type or alias.
        """
        pass

    @abstractmethod
    def drop(
        self,
        abstract: Callable[..., Any] = None,
        alias: str = None
    ) -> None:
        """
        Drops a service from the container by removing its bindings and aliases.

        Warning
        -------
        Using this method irresponsibly can severely damage the system's logic.
        Only use it when you are certain about the consequences, as removing
        critical services may lead to system failures and unexpected behavior.

        Parameters
        ----------
        abstract : Callable[..., Any], optional
            The abstract type or interface to be removed from the container.
        alias : str, optional
            The alias of the service to be removed.
        """
        pass

    @abstractmethod
    def createContext(self):
        """
        Creates a new context for managing scoped services.

        This method returns a context manager that can be used with a 'with' statement
        to control the lifecycle of scoped services.

        Returns
        -------
        ScopeManager
            A context manager for scoped services.

        Usage
        -------
        with container.createContext():
            # Scoped services created here will be disposed when exiting this block
            service = container.make(IScopedService)
            ...
        # Scoped services are automatically disposed here
        """
        pass

    @abstractmethod
    def resolveDependencyArguments(
        self,
        name: Optional[str],
        dependencies: Optional[ResolveArguments]
    ) -> dict:
        """
        Public method to resolve dependencies for a given class or callable.

        This method serves as the public interface for resolving dependencies.
        It wraps the internal dependency resolution logic and provides error
        handling to ensure that any exceptions are communicated clearly.

        Parameters
        ----------
        name : str or None
            The name of the class or callable whose dependencies are being resolved.
            Used for error reporting and context.
        dependencies : ResolveArguments or None
            The dependencies object containing resolved and unresolved arguments,
            as extracted by reflection from the target's signature.

        Returns
        -------
        dict
            A dictionary mapping parameter names to their resolved values. Each key
            is the name of a constructor or callable parameter, and each value is
            the resolved dependency instance or value.

        Raises
        ------
        OrionisContainerException
            If any required dependency cannot be resolved, if there are unresolved
            arguments, or if a dependency refers to a built-in type.
        """
        pass

    @abstractmethod
    def make(
        self,
        type_: Any,
        *args: tuple,
        **kwargs: dict
    ) -> Any:
        """
        Resolve and instantiate a service or type.

        This method attempts to resolve and instantiate the requested service or type.
        It first checks if the type is registered in the container and, if so, resolves
        it according to its binding and lifetime. If the type is not registered but is
        a class, it attempts to auto-resolve it by constructing it and resolving its
        dependencies recursively. If neither approach is possible, an exception is raised.

        Parameters
        ----------
        type_ : Any
            The abstract type, class, or alias to resolve. This can be a class, interface,
            or a string alias registered in the container.
        *args : tuple
            Positional arguments to pass to the constructor or factory function.
        **kwargs : dict
            Keyword arguments to pass to the constructor or factory function.

        Returns
        -------
        Any
            The resolved and instantiated service or object. If the type is registered,
            the instance is created according to its binding's lifetime (singleton,
            transient, or scoped). If the type is not registered but is a class,
            a new instance is created with its dependencies resolved automatically.

        Raises
        ------
        OrionisContainerException
            If the requested service or type is not registered in the container and
            cannot be auto-resolved.

        Notes
        -----
        - If the type is registered, the container's binding and lifetime rules are used.
        - If the type is not registered but is a class, auto-resolution is attempted.
        - If the type cannot be resolved by either method, an exception is raised.
        """
        pass

    @abstractmethod
    def resolve(
        self,
        binding: Binding,
        *args,
        **kwargs
    ):
        """
        Resolves an instance from a binding according to its lifetime.

        Parameters
        ----------
        binding : Binding
            The binding to resolve.
        *args : tuple
            Additional positional arguments to pass to the constructor.
        **kwargs : dict
            Additional keyword arguments to pass to the constructor.

        Returns
        -------
        Any
            The resolved instance.

        Raises
        ------
        OrionisContainerException
            If the binding is not an instance of Binding or if the lifetime is not supported.
        """
        pass

    @abstractmethod
    def resolveWithoutContainer(
        self,
        type_: Callable[..., Any],
        *args,
        **kwargs
    ) -> Any:
        """
        Forces resolution of a type whether it's registered in the container or not.

        Parameters
        ----------
        type_ : Callable[..., Any]
            The type or callable to resolve.
        *args : tuple
            Positional arguments to pass to the constructor/callable.
        **kwargs : dict
            Keyword arguments to pass to the constructor/callable.

        Returns
        -------
        Any
            The resolved instance.

        Raises
        ------
        OrionisContainerException
            If the type cannot be resolved.
        """
        pass

    @abstractmethod
    def call(
        self,
        instance: Any,
        method_name: str,
        *args,
        **kwargs
    ) -> Any:
        """
        Call a method on an instance with automatic dependency injection.

        Parameters
        ----------
        instance : Any
            The instance on which to call the method.
        method_name : str
            The name of the method to call.
        *args : tuple
            Positional arguments to pass to the method.
        **kwargs : dict
            Keyword arguments to pass to the method.

        Returns
        -------
        Any
            The result of the method call.
        """
        pass