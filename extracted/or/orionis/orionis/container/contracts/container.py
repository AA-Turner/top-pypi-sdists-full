from abc import ABC, abstractmethod
from typing import Any, Callable
from orionis.container.enums.lifetimes import Lifetime
from orionis.container.entities.binding import Binding

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
    ) -> bool:
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
    ) -> bool:
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
    ) -> bool:
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
    ) -> bool:
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
    ) -> bool:
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
    def make(
        self,
        abstract_or_alias: Any,
        *args: tuple,
        **kwargs: dict
    ) -> Any:
        """
        Resolves and returns an instance of the requested service.

        Parameters
        ----------
        abstract_or_alias : Any
            The abstract class, interface, or alias (str) to resolve.
        *args : tuple
            Positional arguments to pass to the constructor of the resolved service.
        **kwargs : dict
            Keyword arguments to pass to the constructor of the resolved service.

        Returns
        -------
        Any
            An instance of the requested service.
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
    ) -> Binding:
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