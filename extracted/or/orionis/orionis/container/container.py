import threading
from typing import Any, Callable
from orionis.container.context.manager import ScopeManager
from orionis.container.contracts.container import IContainer
from orionis.container.entities.binding import Binding
from orionis.container.enums.lifetimes import Lifetime
from orionis.container.exceptions import OrionisContainerException
from orionis.container.resolver.resolver import Resolver
from orionis.container.validators import (
    ImplementsAbstractMethods,
    IsAbstractClass,
    IsCallable,
    IsConcreteClass,
    IsInstance,
    IsNotSubclass,
    IsSubclass,
    IsValidAlias,
    LifetimeValidator
)
from orionis.services.introspection.abstract.reflection import ReflectionAbstract
from orionis.services.introspection.callables.reflection import ReflectionCallable

class Container(IContainer):

    # Dictionary to hold singleton instances for each class
    # This allows proper inheritance of the singleton pattern
    _instances = {}

    # Lock for thread-safe singleton instantiation and access
    # This lock ensures that only one thread can create or access instances at a time
    _lock = threading.RLock()  # RLock allows reentrant locking

    def __new__(cls) -> 'Container':
        """
        Creates and returns a singleton instance for each specific class.

        This method implements a truly thread-safe singleton pattern with proper
        inheritance support, ensuring that each class in the hierarchy has its own
        singleton instance. Uses double-checked locking with proper memory barriers.

        Returns
        -------
        Container
            The singleton instance of the specific class.

        Notes
        -----
        This implementation is completely thread-safe and guarantees that:
        - Only one instance per class exists across all threads
        - Memory visibility is properly handled
        - No race conditions can occur
        - Inheritance is properly supported
        """

        # First check without lock for performance (fast path)
        if cls in cls._instances:
            return cls._instances[cls]

        # Acquire the lock for the slow path (instance creation)
        with cls._lock:

            # Double-check if the instance was created by another thread
            # while we were waiting for the lock
            if cls in cls._instances:
                return cls._instances[cls]

            # Create a new instance for this specific class
            instance = super(Container, cls).__new__(cls)

            # Store the instance in the class-specific dictionary
            # This write is protected by the lock, ensuring memory visibility
            cls._instances[cls] = instance

            return instance

    def __init__(self) -> None:
        """
        Initializes a new instance of the container.

        This constructor sets up the internal dictionaries for bindings and aliases,
        ensuring that these are only initialized once per instance. The initialization
        is guarded by checking if the instance already has the required attributes.

        Notes
        -----
        - The `__bindings` dictionary is used to store service bindings.
        - The `__aliasses` dictionary is used to store service aliases.
        - Initialization occurs only once per instance, regardless of how many times __init__ is called.
        - The container registers itself under the IContainer interface to allow for dependency injection.
        """

        # Check if the instance has already been initialized
        if not hasattr(self, '_Container__initialized'):

            # Initialize the container's internal state
            self.__bindings = {}
            self.__aliasses = {}

            # Mark this instance as initialized
            self.__initialized = True

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

        Returns
        -------
        bool
            True if the service was registered successfully.

        Raises
        ------
        OrionisContainerTypeError
            If the abstract or concrete class checks fail.
        OrionisContainerException
            If the concrete class inherits from the abstract class.

        Notes
        -----
        Registers the given concrete implementation to the abstract type with a transient lifetime,
        meaning a new instance will be created each time the service is requested. Optionally, an alias
        can be provided for registration.
        """

        # Ensure that abstract is an abstract class
        IsAbstractClass(abstract, Lifetime.TRANSIENT)

        # Ensure that concrete is a concrete class
        IsConcreteClass(concrete, Lifetime.TRANSIENT)

        # Ensure that concrete is NOT a subclass of abstract
        if enforce_decoupling:
            IsNotSubclass(abstract, concrete)

        # Validate that concrete is a subclass of abstract
        else:
            IsSubclass(abstract, concrete)

        # Ensure implementation
        ImplementsAbstractMethods(
            abstract=abstract,
            concrete=concrete
        )

        # Ensure that the alias is a valid string if provided
        if alias:
            IsValidAlias(alias)

        # Extract the module and class name for the alias
        else:
            rf_asbtract = ReflectionAbstract(abstract)
            alias = rf_asbtract.getModuleWithClassName()

        # If the service is already registered, drop it
        self.drop(abstract, alias)

        # Register the service with transient lifetime
        self.__bindings[abstract] = Binding(
            contract = abstract,
            concrete = concrete,
            lifetime = Lifetime.TRANSIENT,
            enforce_decoupling = enforce_decoupling,
            alias = alias
        )

        # Register the alias
        self.__aliasses[alias] = self.__bindings[abstract]

        # Return True to indicate successful registration
        return True

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

        Returns
        -------
        bool
            True if the service was registered successfully.

        Raises
        ------
        OrionisContainerTypeError
            If the abstract or concrete class checks fail.
        OrionisContainerException
            If the concrete class inherits from the abstract class.

        Notes
        -----
        Registers the given concrete implementation to the abstract type with a singleton lifetime,
        meaning a single instance will be created and shared. Optionally, an alias can be provided for registration.
        """

        # Ensure that abstract is an abstract class
        IsAbstractClass(abstract, Lifetime.SINGLETON)

        # Ensure that concrete is a concrete class
        IsConcreteClass(concrete, Lifetime.SINGLETON)

        # Ensure that concrete is NOT a subclass of abstract
        if enforce_decoupling:
            IsNotSubclass(abstract, concrete)

        # Validate that concrete is a subclass of abstract
        else:
            IsSubclass(abstract, concrete)

        # Ensure implementation
        ImplementsAbstractMethods(
            abstract=abstract,
            concrete=concrete
        )

        # Ensure that the alias is a valid string if provided
        if alias:
            IsValidAlias(alias)
        else:
            rf_asbtract = ReflectionAbstract(abstract)
            alias = rf_asbtract.getModuleWithClassName()

        # If the service is already registered, drop it
        self.drop(abstract, alias)

        # Register the service with singleton lifetime
        self.__bindings[abstract] = Binding(
            contract = abstract,
            concrete = concrete,
            lifetime = Lifetime.SINGLETON,
            enforce_decoupling = enforce_decoupling,
            alias = alias
        )

        # Register the alias
        self.__aliasses[alias] = self.__bindings[abstract]

        # Return True to indicate successful registration
        return True

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

        Returns
        -------
        bool
            True if the service was registered successfully.

        Raises
        ------
        OrionisContainerTypeError
            If the abstract or concrete class checks fail.
        OrionisContainerException
            If the concrete class inherits from the abstract class.

        Notes
        -----
        Registers the given concrete implementation to the abstract type with a scoped lifetime,
        meaning a new instance will be created per scope. Optionally, an alias can be provided for registration.
        """

        # Ensure that abstract is an abstract class
        IsAbstractClass(abstract, Lifetime.SCOPED)

        # Ensure that concrete is a concrete class
        IsConcreteClass(concrete, Lifetime.SCOPED)

        # Ensure that concrete is NOT a subclass of abstract
        if enforce_decoupling:
            IsNotSubclass(abstract, concrete)

        # Validate that concrete is a subclass of abstract
        else:
            IsSubclass(abstract, concrete)

        # Ensure implementation
        ImplementsAbstractMethods(
            abstract=abstract,
            concrete=concrete
        )

        # Ensure that the alias is a valid string if provided
        if alias:
            IsValidAlias(alias)
        else:
            rf_asbtract = ReflectionAbstract(abstract)
            alias = rf_asbtract.getModuleWithClassName()

        # If the service is already registered, drop it
        self.drop(abstract, alias)

        # Register the service with scoped lifetime
        self.__bindings[abstract] = Binding(
            contract = abstract,
            concrete = concrete,
            lifetime = Lifetime.SCOPED,
            enforce_decoupling = enforce_decoupling,
            alias = alias
        )

        # Register the alias
        self.__aliasses[alias] = self.__bindings[abstract]

        # Return True to indicate successful registration
        return True

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
        Returns
        -------
        bool
            True if the instance was successfully registered.
        Raises
        ------
        TypeError
            If `abstract` is not an abstract class or if `alias` is not a valid string.
        ValueError
            If `instance` is not a valid instance of `abstract`.
        Notes
        -----
        This method ensures that the abstract is a valid abstract class, the instance
        is valid, and the alias (if provided) is a valid string. The instance is then
        registered in the container under both the abstract and the alias.
        """

        # Ensure that the abstract is an abstract class
        IsAbstractClass(abstract, f"Instance {Lifetime.SINGLETON}")

        # Ensure that the instance is a valid instance
        IsInstance(instance)

        # Ensure that instance is NOT a subclass of abstract
        if enforce_decoupling:
            IsNotSubclass(abstract, instance.__class__)

        # Validate that instance is a subclass of abstract
        else:
            IsSubclass(abstract, instance.__class__)

        # Ensure implementation
        ImplementsAbstractMethods(
            abstract=abstract,
            instance=instance
        )

        # Ensure that the alias is a valid string if provided
        if alias:
            IsValidAlias(alias)
        else:
            rf_asbtract = ReflectionAbstract(abstract)
            alias = rf_asbtract.getModuleWithClassName()

        # If the service is already registered, drop it
        self.drop(abstract, alias)

        # Register the instance with the abstract type
        self.__bindings[abstract] = Binding(
            contract = abstract,
            instance = instance,
            lifetime = Lifetime.SINGLETON,
            enforce_decoupling = enforce_decoupling,
            alias = alias
        )

        # Register the alias
        self.__aliasses[alias] = self.__bindings[abstract]

        # Return True to indicate successful registration
        return True

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

        Raises
        ------
        OrionisContainerTypeError
            If the alias is invalid or the function is not callable.
        OrionisContainerException
            If the lifetime is not allowed for the function signature.
        """

        # Normalize and validate the lifetime parameter
        lifetime = LifetimeValidator(lifetime)

        # Ensure that the alias is a valid string
        IsValidAlias(alias)

        # Validate that the function is callable
        IsCallable(fn)

        # Inspect the function signature
        params = ReflectionCallable(fn).getDependencies()

        # If the function requires arguments, only allow TRANSIENT
        if (len(params.resolved) + len(params.unresolved)) > 0 and lifetime != Lifetime.TRANSIENT:
            raise OrionisContainerException(
                "Functions that require arguments can only be registered with a TRANSIENT lifetime."
            )

        # If the service is already registered, drop it
        self.drop(None, alias)

        # Register the function with the specified alias and lifetime
        self.__bindings[alias] = Binding(
            function=fn,
            lifetime=lifetime,
            alias=alias
        )

        # Register the function as a binding
        self.__aliasses[alias] = self.__bindings[alias]

        return True

    def bound(
        self,
        abstract_or_alias: Any,
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

        Notes
        -----
        This method allows you to verify whether a service has been registered in the container,
        either by its abstract type or by its alias. It supports both class-based and string-based lookups.
        """
        return (
            abstract_or_alias in self.__bindings
            or abstract_or_alias in self.__aliasses
        )

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
        return self.__bindings.get(abstract_or_alias) or self.__aliasses.get(abstract_or_alias)

    def drop(
        self,
        abstract: Callable[..., Any] = None,
        alias: str = None
    ) -> None:
        """
        Drops a service from the container by removing its bindings and aliases.
        This method allows removing registered services from the dependency injection container,
        either by their abstract type or by their alias. When a service is dropped,
        all its bindings and aliases are removed from the container.

        Warning
        -------
        Using this method irresponsibly can severely damage the system's logic.
        Only use it when you are certain about the consequences, as removing
        critical services may lead to system failures and unexpected behavior.
        abstract : Callable[..., Any], optional
            The abstract type or interface to be removed from the container.
            If provided, both the binding and the default alias for this type will be removed.
            The alias of the service to be removed. If provided, both the alias entry
            and any associated binding will be removed.

        Notes
        -----
        At least one parameter (abstract or alias) must be provided for the method to take effect.
        If both are provided, both will be processed independently.
        """

        # If abstract is provided
        if abstract:

            # Remove the abstract service from the bindings if it exists
            if abstract in self.__bindings:
                del self.__bindings[abstract]

            # Remove the default alias (module + class name) from aliases if it exists
            abs_alias = ReflectionAbstract(abstract).getModuleWithClassName()
            if abs_alias in self.__aliasses:
                del self.__aliasses[abs_alias]

        # If a custom alias is provided
        if alias:

            # Remove it from the aliases dictionary if it exists
            if alias in self.__aliasses:
                del self.__aliasses[alias]

            # Remove the binding associated with the alias
            if alias in self.__bindings:
                del self.__bindings[alias]

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

        Raises
        ------
        OrionisContainerException
            If the requested service is not registered in the container.
        """
        if not self.bound(abstract_or_alias):
            raise OrionisContainerException(
                f"The requested service '{abstract_or_alias}' is not registered in the container."
            )

        # Get the binding for the requested abstract type or alias
        binding = self.getBinding(abstract_or_alias)

        # Resolve the binding using the Resolver class
        return Resolver(self).resolve(
            binding,
            *args,
            **kwargs
        )

    def createContext(self) -> ScopeManager:
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
        return ScopeManager()