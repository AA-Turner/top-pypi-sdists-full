import abc
import asyncio
import inspect
import threading
import typing
from pathlib import Path
from typing import Any, Callable, Optional
from orionis.container.context.manager import ScopeManager
from orionis.container.context.scope import ScopedContext
from orionis.container.contracts.container import IContainer
from orionis.container.entities.binding import Binding
from orionis.container.enums.lifetimes import Lifetime
from orionis.container.exceptions import OrionisContainerException
from orionis.container.validators import (
    ImplementsAbstractMethods,
    IsAbstractClass,
    IsConcreteClass,
    IsInstance,
    IsCallable,
    IsSubclass,
    IsNotSubclass,
    IsValidAlias,
    LifetimeValidator
)
from orionis.services.introspection.abstract.reflection import ReflectionAbstract
from orionis.services.introspection.callables.reflection import ReflectionCallable
from orionis.services.introspection.concretes.reflection import ReflectionConcrete
from orionis.services.introspection.dependencies.entities.argument import Argument
from orionis.services.introspection.dependencies.entities.resolve_argument import ResolveArguments
from orionis.services.introspection.dependencies.reflection import ReflectDependencies

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

            # Return the newly created instance
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
        - The `__aliases` dictionary is used to store service aliases.
        - Initialization occurs only once per instance, regardless of how many times __init__ is called.
        - The container registers itself under the IContainer interface to allow for dependency injection.
        """

        # Check if the instance has already been initialized
        if not hasattr(self, '_Container__initialized'):

            # Current Project Namespaces
            # Get current project namespace from the working directory
            current_project_namespace = Path().cwd().name

            # Add the current project namespace to valid namespaces
            self.__valid_namespaces = set(('app', 'orionis', 'requests', 'rich', 'apscheduler', 'dotenv', current_project_namespace))

            # Initialize the container's internal state
            self.__bindings = {}
            self.__aliases = {}
            self.__resolution_cache = {}
            self.__singleton_cache = {}

            # Mark this instance as initialized
            self.__initialized = True

    def __handleSyncAsyncResult(
        self,
        result: Any
    ) -> Any:
        """
        Universal helper to handle both synchronous and asynchronous results.

        This method automatically detects if a result is a coroutine and handles
        it appropriately based on the current execution context.

        Parameters
        ----------
        result : Any
            The result to handle, which may be a coroutine or regular value.

        Returns
        -------
        Any
            The resolved result. If the result was a coroutine, it will be awaited
            if possible, or scheduled appropriately.
        """

        # If the result is not a coroutine, return it directly
        if not asyncio.iscoroutine(result):
            return result

        try:

            # Check if we're currently in an event loop
            loop = asyncio.get_running_loop()

            # If we're in an async context, we need to let the caller handle the coroutine
            # Since we can't await here, we'll create a task and get the result synchronously
            # This is a compromise for mixed sync/async environments
            if loop.is_running():

                # For running loops, we create a new thread to run the coroutine
                import concurrent.futures

                # Define a function to run the coroutine in a new event loop
                def run_coroutine():

                    # Create a new event loop for this thread
                    new_loop = asyncio.new_event_loop()
                    asyncio.set_event_loop(new_loop)

                    # Run the coroutine until completion
                    try:
                        return new_loop.run_until_complete(result)

                    # Finally, ensure the loop is closed to free resources
                    finally:
                        new_loop.close()

                # Use ThreadPoolExecutor to run the coroutine in a separate thread
                with concurrent.futures.ThreadPoolExecutor() as executor:
                    future = executor.submit(run_coroutine)
                    return future.result()

            else:
                # If loop exists but not running, we can run the coroutine
                return loop.run_until_complete(result)

        except RuntimeError:

            # No event loop running, we can run the coroutine directly
            return asyncio.run(result)

    def __invokeCallableUniversal(
        self,
        fn: Callable[..., Any],
        *args,
        **kwargs
    ) -> Any:
        """
        Universal callable invoker that handles both sync and async callables.

        Parameters
        ----------
        fn : Callable[..., Any]
            The callable to invoke.
        *args : tuple
            Positional arguments to pass to the callable.
        **kwargs : dict
            Keyword arguments to pass to the callable.

        Returns
        -------
        Any
            The result of the callable invocation.

        Raises
        ------
        OrionisContainerException
            If the callable invocation fails.
        """

        try:

            # Count the total number of provided arguments
            total_provided_args = len(args) + len(kwargs)

            # Inspect the callable to determine its signature and parameters
            dependencies = ReflectDependencies(fn).getCallableDependencies()
            total_dependencies = len(dependencies.resolved) + len(dependencies.unresolved)

            # If the callable does not require any dependencies, invoke directly
            if total_dependencies == 0:
                result = fn(*args, **kwargs)
                return self.__handleSyncAsyncResult(result)

            # If enough arguments are provided, invoke directly
            if total_provided_args >= total_dependencies:
                result = fn(*args, **kwargs)
                return self.__handleSyncAsyncResult(result)

            # If not enough arguments are provided, attempt to resolve missing dependencies
            if total_provided_args < total_dependencies:

                # New lists to hold the final arguments to pass to the callable
                n_args = []
                n_kwargs = {}

                # Iterate through the function's required arguments in order
                args_index = 0

                # Iterate over all dependencies in the order they were defined
                for name, dep in dependencies.ordered.items():

                    # Check if the argument was provided positionally and hasn't been used yet
                    if args_index < len(args) and name not in kwargs:

                        # Add the positional argument to the new list
                        n_args.append(args[args_index])

                        # Move to the next positional argument
                        args_index += 1

                    # Check if the argument was provided as a keyword argument
                    elif name in kwargs:

                        # Add the keyword argument to the new dictionary
                        n_kwargs[name] = kwargs[name]

                        # Remove the argument from the original kwargs to avoid duplication
                        del kwargs[name]

                    # If not provided, attempt to resolve it from the container
                    else:

                        n_kwargs[name] = self.__resolveSingleDependency(
                            getattr(fn, '__name__', str(fn)),
                            name,
                            dep
                        )

                # Add any remaining positional arguments that weren't mapped to specific parameters
                n_args.extend(args[args_index:])

                # Add any remaining keyword arguments that weren't processed
                n_kwargs.update(kwargs)

                # Invoke the function with the resolved arguments
                result = fn(*n_args, **n_kwargs)
                return self.__handleSyncAsyncResult(result)

        except TypeError as e:

            # If invocation fails, use ReflectionCallable for better error messaging
            rf_callable = ReflectionCallable(fn)
            function_name = rf_callable.getName()
            signature = rf_callable.getSignature()

            # Raise a more informative exception with the function name and signature
            raise OrionisContainerException(
                f"Failed to invoke function [{function_name}] with the provided arguments: {e}. "
                f"Note that this may include a reference to the same 'self' object.\n"
                f"Expected function signature: {function_name}{signature}"
            ) from e

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
        self.__aliases[alias] = self.__bindings[abstract]

        # Return True to indicate successful registration
        return True

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
        self.__aliases[alias] = self.__bindings[abstract]

        # Return True to indicate successful registration
        return True

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
        self.__aliases[alias] = self.__bindings[abstract]

        # Return True to indicate successful registration
        return True

    def scopedInstance(
        self,
        abstract: Callable[..., Any],
        instance: Any,
        *,
        alias: str = None,
        enforce_decoupling: bool = False
    ) -> Optional[bool]:
        """
        Registers an instance of a class or interface in the container with scoped lifetime.

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
            Whether to enforce decoupling between abstract and concrete types.

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
        OrionisContainerException
            If no active scope is found.

        Notes
        -----
        This method registers the instance with scoped lifetime, meaning it will be
        available only within the current active scope. If no scope is active,
        an exception will be raised.
        """

        # Ensure that the abstract is an abstract class
        IsAbstractClass(abstract, f"Instance {Lifetime.SCOPED}")

        # Ensure that the instance is a valid instance
        IsInstance(instance)

        # Ensure that instance is NOT a subclass of abstract
        if enforce_decoupling:
            IsNotSubclass(abstract, instance.__class__)
        else:
            # Validate that instance is a subclass of abstract
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

        # If the service is already registered in container bindings, drop it
        self.drop(abstract, alias)

        # Register the binding in the container for future scope resolutions
        self.__bindings[abstract] = Binding(
            contract=abstract,
            instance=instance,
            lifetime=Lifetime.SCOPED,
            enforce_decoupling=enforce_decoupling,
            alias=alias
        )

        # Register the alias
        self.__aliases[alias] = self.__bindings[abstract]

        # Store the instance directly in the current scope
        scope = ScopedContext.getCurrentScope()
        if scope:
            scope[abstract] = instance
            if alias != abstract:
                scope[alias] = instance

        # Return True to indicate successful registration
        return True

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

        # Validate the enforce_decoupling parameter
        if isinstance(enforce_decoupling, bool):

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

        else:

            # Drop the existing alias if it exists
            self.drop(alias=alias)

            # If enforce_decoupling is not a boolean, set it to False
            enforce_decoupling = False

        # Register the instance with the abstract type
        self.__bindings[abstract] = Binding(
            contract = abstract,
            instance = instance,
            lifetime = Lifetime.SINGLETON,
            enforce_decoupling = enforce_decoupling,
            alias = alias
        )

        # Register the alias
        self.__aliases[alias] = self.__bindings[abstract]

        # Return True to indicate successful registration
        return True

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
        params: ResolveArguments = ReflectionCallable(fn).getDependencies()

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
        self.__aliases[alias] = self.__bindings[alias]

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
            True if the service is registered and has a valid binding, False otherwise.

        Notes
        -----
        This method not only checks for the existence of a binding but also validates
        its integrity. If a binding exists but is corrupted, this method will return
        False to prevent using invalid bindings.
        """

        try:
            # Use getBinding which includes validation
            binding = self.getBinding(abstract_or_alias)
            return binding is not None
        except OrionisContainerException:
            # If binding validation fails, consider it as not bound
            return False

    def getBinding(
        self,
        abstract_or_alias: Any
    ) -> Optional[Binding]:
        """
        Retrieves the binding for the requested abstract type or alias.

        This method performs a lookup in the container's internal binding dictionaries
        to find the binding associated with the provided abstract type or alias.
        It first searches in the primary bindings dictionary, then in the aliases
        dictionary if no direct binding is found.

        Parameters
        ----------
        abstract_or_alias : Any
            The abstract class, interface, or alias (str) to retrieve the binding for.
            This can be either a class type or a string alias that was registered
            with the container.

        Returns
        -------
        Binding or None
            The binding object associated with the requested abstract type or alias.
            Returns None if no binding is found for the provided abstract_or_alias.
            The binding contains information about the service registration including
            the concrete implementation, lifetime, and other configuration details.

        Raises
        ------
        OrionisContainerException
            If a binding is found but is corrupted or incomplete.

        Notes
        -----
        The method searches in the following order:
        1. Direct lookup in the bindings dictionary using the abstract type
        2. Lookup in the aliases dictionary using the provided alias

        This method validates binding integrity before returning it to ensure
        that only valid, complete bindings are returned to the caller.
        """

        # First, attempt to find the binding directly using the abstract type
        # This handles cases where the service was registered with its abstract class
        binding = self.__bindings.get(abstract_or_alias)
        if binding:
            self.__validateBinding(binding, abstract_or_alias)
            return binding

        # If no direct binding found, search in the aliases dictionary
        # This handles cases where the service is being requested by its alias
        binding = self.__aliases.get(abstract_or_alias)
        if binding:
            self.__validateBinding(binding, abstract_or_alias)
            return binding

        # Return None if no binding is found for the requested abstract type or alias
        return None

    def __validateBinding(
        self,
        binding: Binding,
        requested_key: Any
    ) -> None:
        """
        Validates the integrity and completeness of a binding.

        This method ensures that the binding contains all necessary information
        for successful resolution and that the binding data is consistent and
        not corrupted.

        Parameters
        ----------
        binding : Binding
            The binding to validate.
        requested_key : Any
            The key (abstract type or alias) that was used to retrieve this binding.
            Used for error reporting context.

        Raises
        ------
        OrionisContainerException
            If the binding is invalid, incomplete, or corrupted.
        """

        # Ensure the binding is actually a Binding instance
        if not isinstance(binding, Binding):
            raise OrionisContainerException(
                f"Corrupted binding found for '{requested_key}': expected Binding instance, "
                f"got {type(binding).__name__}"
            )

        # Ensure the binding has a valid lifetime
        if not hasattr(binding, 'lifetime') or binding.lifetime is None:
            raise OrionisContainerException(
                f"Invalid binding for '{requested_key}': missing or null lifetime"
            )

        # Validate that the lifetime is a valid Lifetime enum value
        if not isinstance(binding.lifetime, Lifetime):
            raise OrionisContainerException(
                f"Invalid binding for '{requested_key}': lifetime must be a Lifetime enum value, "
                f"got {type(binding.lifetime).__name__}"
            )

        # Ensure the binding has at least one resolution method
        has_concrete = hasattr(binding, 'concrete') and binding.concrete is not None
        has_instance = hasattr(binding, 'instance') and binding.instance is not None
        has_function = hasattr(binding, 'function') and binding.function is not None

        if not (has_concrete or has_instance or has_function):
            raise OrionisContainerException(
                f"Incomplete binding for '{requested_key}': binding must have at least one of "
                "concrete class, instance, or function defined"
            )

        # Validate that only one primary resolution method is defined
        resolution_methods = [has_concrete, has_instance, has_function]
        if sum(resolution_methods) > 1:
            methods = []
            if has_concrete:
                methods.append("concrete")
            if has_instance:
                methods.append("instance")
            if has_function:
                methods.append("function")

            raise OrionisContainerException(
                f"Conflicting binding for '{requested_key}': binding has multiple resolution methods "
                f"defined: {', '.join(methods)}. Only one should be specified."
            )

        # Additional validations based on binding type
        self.__validateBindingByType(binding, requested_key)

    def __validateBindingByType(
        self,
        binding: Binding,
        requested_key: Any
    ) -> None:
        """
        Performs type-specific validation for different binding types.

        Parameters
        ----------
        binding : Binding
            The binding to validate.
        requested_key : Any
            The key used to retrieve this binding (for error context).

        Raises
        ------
        OrionisContainerException
            If type-specific validation fails.
        """

        # Validate concrete class bindings
        if hasattr(binding, 'concrete') and binding.concrete is not None:
            if not callable(binding.concrete):
                raise OrionisContainerException(
                    f"Invalid concrete binding for '{requested_key}': concrete must be callable"
                )

            if not isinstance(binding.concrete, type):
                raise OrionisContainerException(
                    f"Invalid concrete binding for '{requested_key}': concrete must be a class type"
                )

        # Validate instance bindings
        elif hasattr(binding, 'instance') and binding.instance is not None:
            # Instance bindings should always be singletons
            if binding.lifetime != Lifetime.SINGLETON:
                raise OrionisContainerException(
                    f"Invalid instance binding for '{requested_key}': instances must have "
                    f"SINGLETON lifetime, got {binding.lifetime.name}"
                )

        # Validate function bindings
        elif hasattr(binding, 'function') and binding.function is not None:
            if not callable(binding.function):
                raise OrionisContainerException(
                    f"Invalid function binding for '{requested_key}': function must be callable"
                )

        # Validate contract and alias consistency
        if hasattr(binding, 'contract') and binding.contract is not None:
            if not isinstance(binding.contract, type):
                raise OrionisContainerException(
                    f"Invalid contract in binding for '{requested_key}': contract must be a class type"
                )

        if hasattr(binding, 'alias') and binding.alias is not None:
            if not isinstance(binding.alias, str):
                raise OrionisContainerException(
                    f"Invalid alias in binding for '{requested_key}': alias must be a string"
                )

            if len(binding.alias.strip()) == 0:
                raise OrionisContainerException(
                    f"Invalid alias in binding for '{requested_key}': alias cannot be empty"
                )

    def drop(
        self,
        abstract: Callable[..., Any] = None,
        alias: str = None
    ) -> bool:
        """
        Removes a service registration from the container by abstract type or alias.

        This method unregisters services from the dependency injection container by removing
        their bindings and associated aliases. When a service is removed, all references to it
        are cleaned up from the container's internal dictionaries, including singleton cache
        and resolution cache.

        Parameters
        ----------
        abstract : Callable[..., Any], optional
            The abstract class or interface whose registration should be removed.
            When provided, removes the binding for this type and its default alias
            (generated from module and class name).
        alias : str, optional
            The custom alias whose registration should be removed.
            When provided, removes both the alias entry and any associated binding
            registered under this alias name.

        Returns
        -------
        bool
            True if at least one registration was successfully removed, False if
            no matching registrations were found to remove.

        Warnings
        --------
        Use this method with caution. Removing essential services can break dependency
        resolution chains and cause runtime failures throughout the application.
        Only remove services when you are certain they are no longer needed.

        Notes
        -----
        - At least one parameter (abstract or alias) should be provided for meaningful operation
        - If both parameters are provided, both removal operations will be attempted
        - The method handles cases where the specified abstract type or alias doesn't exist
        - Default aliases are automatically generated using the format: 'module.ClassName'
        - All cache entries (singleton and resolution) are cleaned up
        """

        deleted = False

        # If abstract is provided
        if abstract:

            # Remove the abstract service from the bindings if it exists
            if abstract in self.__bindings:
                del self.__bindings[abstract]
                deleted = True

            # Remove the default alias (module + class name) from aliases if it exists
            abs_alias = ReflectionAbstract(abstract).getModuleWithClassName()
            if abs_alias in self.__aliases:
                del self.__aliases[abs_alias]
                deleted = True

            # Clean up singleton cache for this abstract
            if abstract in self.__singleton_cache:
                del self.__singleton_cache[abstract]
                deleted = True

            # Clean up resolution cache for this abstract
            if hasattr(abstract, '__module__') and hasattr(abstract, '__name__'):
                type_key = f"{abstract.__module__}.{abstract.__name__}"
                if type_key in self.__resolution_cache:
                    del self.__resolution_cache[type_key]
                    deleted = True

        # If a custom alias is provided
        if alias:

            # Remove it from the aliases dictionary if it exists
            if alias in self.__aliases:
                del self.__aliases[alias]
                deleted = True

            # Remove the binding associated with the alias
            if alias in self.__bindings:
                del self.__bindings[alias]
                deleted = True

            # Clean up singleton cache for this alias
            if alias in self.__singleton_cache:
                del self.__singleton_cache[alias]
                deleted = True

        # Return if any deletion occurred
        return deleted

    def createContext(
        self
    ) -> ScopeManager:
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

        # Try to resolve from registered bindings first
        if self.bound(type_):
            # Resolve the binding according to its lifetime and configuration
            return self.resolve(
                self.getBinding(type_),
                *args,
                **kwargs
            )

        # If not registered, try auto-resolution for classes
        if isinstance(type_, type):
            # Attempt to construct the class and resolve its dependencies recursively
            return self.resolveWithoutContainer(
                type_,
                *args,
                **kwargs
            )

        # If all attempts fail, raise an exception indicating resolution failure
        raise OrionisContainerException(
            f"The requested service '{type_}' is not registered in the container "
            f"and cannot be auto-resolved."
        )

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

        # Ensure the binding is an instance of Binding
        if not isinstance(binding, Binding):
            raise OrionisContainerException(
                f"Expected a Binding instance, got {type(binding).__name__}"
            )

        # Handle based on binding type and lifetime
        if binding.lifetime == Lifetime.TRANSIENT:
            return self.__resolveTransient(binding, *args, **kwargs)
        elif binding.lifetime == Lifetime.SINGLETON:
            return self.__resolveSingleton(binding, *args, **kwargs)
        elif binding.lifetime == Lifetime.SCOPED:
            return self.__resolveScoped(binding, *args, **kwargs)

    def __resolveTransient(
        self,
        binding: Binding,
        *args,
        **kwargs
    ) -> Any:
        """
        Resolves a service with transient lifetime.

        Parameters
        ----------
        binding : Binding
            The binding to resolve.
        *args : tuple
            Positional arguments to pass to the constructor.
        **kwargs : dict
            Keyword arguments to pass to the constructor.

        Returns
        -------
        Any
            A new instance of the requested service.
        """

        # Check if the binding has a concrete class or function defined
        if binding.concrete:
            if args or kwargs:
                return self.__instantiateConcreteWithArgs(binding.concrete, *args, **kwargs)
            else:
                return self.__instantiateConcreteReflective(binding.concrete)

        # If the binding has a function defined
        elif binding.function:
            if args or kwargs:
                return self.__instantiateCallableWithArgs(binding.function, *args, **kwargs)
            else:
                return self.__instantiateCallableReflective(binding.function)

        # If neither concrete class nor function is defined
        else:
            raise OrionisContainerException(
                "Cannot resolve transient binding: neither a concrete class nor a function is defined."
            )

    def __resolveSingleton(
        self,
        binding: Binding,
        *args,
        **kwargs
    ) -> Any:
        """
        Resolves a service with singleton lifetime.

        Parameters
        ----------
        binding : Binding
            The binding to resolve.
        *args : tuple
            Positional arguments to pass to the constructor (only used if instance doesn't exist yet).
        **kwargs : dict
            Keyword arguments to pass to the constructor (only used if instance doesn't exist yet).

        Returns
        -------
        Any
            The singleton instance of the requested service.
        """

        # Get the cache key for this binding (prioritize contract over alias)
        cache_key = self.__getSingletonCacheKey(binding)

        # Return existing instance if available
        if cache_key in self.__singleton_cache:
            return self.__singleton_cache[cache_key]

        # Handle pre-registered instances first
        if binding.instance is not None:
            # Store the pre-registered instance in cache and return it
            self.__singleton_cache[cache_key] = binding.instance
            return self.__singleton_cache[cache_key]

        # Create instance if needed
        instance = None
        if binding.concrete:
            if args or kwargs:
                instance = self.__instantiateConcreteWithArgs(
                    binding.concrete,
                    *args,
                    **kwargs
                )
            else:
                instance = self.__instantiateConcreteReflective(
                    binding.concrete
                )

        # If the binding has a function defined
        elif binding.function:
            if args or kwargs:
                instance = self.__instantiateCallableWithArgs(
                    binding.function,
                    *args,
                    **kwargs
                )
            else:
                instance = self.__instantiateCallableReflective(
                    binding.function
                )

        # If neither concrete class, function, nor instance is defined
        else:
            raise OrionisContainerException(
                "Failed to resolve singleton binding: no concrete class, instance, or function is defined for this binding. "
                "Ensure that the binding was registered correctly with a concrete implementation, instance, or callable."
            )

        # Store the instance in the singleton cache using the consistent key
        self.__singleton_cache[cache_key] = instance

        # Store cross-references to ensure we can find the instance by both contract and alias
        self.__storeSingletonCrossReferences(binding, instance)

        # Return the newly created singleton instance
        return instance

    def __getSingletonCacheKey(self, binding: Binding) -> Any:
        """
        Determines the primary cache key for a singleton binding.

        This method establishes a consistent caching strategy by prioritizing
        the contract over the alias for cache key generation. This ensures
        that each singleton has a single, predictable cache key.

        Parameters
        ----------
        binding : Binding
            The binding for which to determine the cache key.

        Returns
        -------
        Any
            The primary cache key to use for this binding.
        """

        # Prioritize contract if available (for class-based bindings)
        if binding.contract is not None:
            return binding.contract

        # Fall back to alias for function-based or alias-only bindings
        if binding.alias is not None:
            return binding.alias

        # This should never happen with valid bindings, but provide fallback
        raise OrionisContainerException(
            "Cannot determine cache key: binding has neither contract nor alias"
        )

    def __storeSingletonCrossReferences(self, binding: Binding, instance: Any) -> None:
        """
        Stores cross-references for singleton instances to ensure discoverability.

        This method ensures that singleton instances can be found by both their
        contract and alias, while maintaining a single source of truth for the
        actual instance storage.

        Parameters
        ----------
        binding : Binding
            The binding containing contract and alias information.
        instance : Any
            The singleton instance to store cross-references for.
        """

        primary_key = self.__getSingletonCacheKey(binding)

        # Store cross-reference for contract if it's not the primary key
        if binding.contract is not None and binding.contract != primary_key:
            self.__singleton_cache[binding.contract] = instance

        # Store cross-reference for alias if it's not the primary key
        if binding.alias is not None and binding.alias != primary_key:
            self.__singleton_cache[binding.alias] = instance

    def __resolveScoped(
        self,
        binding: Binding,
        *args,
        **kwargs
    ) -> Any:
        """
        Resolves a service with scoped lifetime.

        Parameters
        ----------
        binding : Binding
            The binding to resolve.
        *args : tuple
            Positional arguments to pass to the constructor.
        **kwargs : dict
            Keyword arguments to pass to the constructor.

        Returns
        -------
        Any
            The scoped instance of the requested service.

        Raises
        ------
        OrionisContainerException
            If no scope is active or service can't be resolved.
        """

        # Check if the current scope is active
        scope = ScopedContext.getCurrentScope()

        # If no active scope is found, raise an exception
        if scope is None:
            raise OrionisContainerException(
                f"No active scope found while resolving scoped service '{binding.alias}'. "
                f"Use 'with container.createContext():' to create a scope context."
            )

        # If the binding is already in the current scope, return it
        if binding.contract in scope:
            return scope[binding.contract]
        if binding.alias in scope:
            return scope[binding.alias]

        # Create a new instance
        if binding.concrete:
            if args or kwargs:
                instance = self.__instantiateConcreteWithArgs(
                    binding.concrete,
                    *args,
                    **kwargs
                )
            else:
                instance = self.__instantiateConcreteReflective(
                    binding.concrete
                )
        elif binding.function:
            if args or kwargs:
                instance = self.__instantiateCallableWithArgs(
                    binding.function,
                    *args,
                    **kwargs
                )
            else:
                instance = self.__instantiateCallableReflective(
                    binding.function
                )
        else:
            raise OrionisContainerException(
                f"Cannot resolve scoped binding for '{binding.contract} or {binding.alias}': "
                "No concrete class, instance, or function is defined for this binding. "
                "Ensure that the binding was registered correctly with a concrete implementation, instance, or callable."
            )

        # Store the instance in the current scope and return it
        scope[binding.contract] = instance

        # Return the newly created instance
        return scope[binding.contract]

    def __instantiateConcreteWithArgs(
        self,
        concrete: Callable[..., Any],
        *args,
        **kwargs
    ) -> Any:
        """
        Instantiates a concrete class with the provided arguments.

        Parameters
        ----------
        concrete : Callable[..., Any]
            Class to instantiate.
        *args : tuple
            Positional arguments to pass to the constructor.
        **kwargs : dict
            Keyword arguments to pass to the constructor.

        Returns
        -------
        object
            A new instance of the specified concrete class.
        """

        # try to instantiate the concrete class with the provided arguments
        try:

            # If the concrete is a class, instantiate it directly
            return concrete(*args, **kwargs)

        except TypeError as e:

            # If instantiation fails, use ReflectionConcrete to get class name and constructor signature
            rf_concrete = ReflectionConcrete(concrete)
            class_name = rf_concrete.getClassName()
            signature = rf_concrete.getConstructorSignature()

            # Raise an exception with detailed information about the failure
            raise OrionisContainerException(
                f"Failed to instantiate [{class_name}] with the provided arguments: {e}\n"
                f"Expected constructor signature: [{signature}]"
            ) from e

    def __instantiateCallableWithArgs(
        self,
        fn: Callable[..., Any],
        *args,
        **kwargs
    ) -> Any:
        """
        Invokes a callable with the provided arguments.
        Supports both synchronous and asynchronous callables automatically.

        Parameters
        ----------
        fn : Callable[..., Any]
            The callable to invoke.
        *args : tuple
            Positional arguments to pass to the callable.
        **kwargs : dict
            Keyword arguments to pass to the callable.

        Returns
        -------
        Any
            The result of the callable. If the callable is async,
            the coroutine will be handled automatically.
        """
        return self.__invokeCallableUniversal(fn, *args, **kwargs)

    def __instantiateConcreteReflective(
        self,
        concrete: Callable[..., Any]
    ) -> Any:
        """
        Instantiates a concrete class reflectively, resolving its dependencies from the container.

        Parameters
        ----------
        concrete : Callable[..., Any]
            The concrete class to instantiate.

        Returns
        -------
        Any
            A new instance of the concrete class.
        """

        return self.__instantiateWithReflection(concrete, is_class=True)

    def __instantiateCallableReflective(
        self,
        fn: Callable[..., Any]
    ) -> Any:
        """
        Invokes a callable reflectively, resolving its dependencies from the container.

        Parameters
        ----------
        fn : Callable[..., Any]
            The callable to invoke.

        Returns
        -------
        Any
            The result of the callable.
        """

        # Try simple call first for functions without parameters
        try:
            # Use ReflectionCallable to get dependencies
            dependencies = ReflectionCallable(fn).getDependencies()

            # If there are no required parameters, call directly
            if not dependencies or (not dependencies.resolved and not dependencies.unresolved):
                result = fn()
                return self.__handleSyncAsyncResult(result)

            # If there are unresolved dependencies, raise an exception
            if dependencies.unresolved:
                unresolved_args = [name for name in dependencies.unresolved.keys()]
                raise OrionisContainerException(
                    f"Cannot invoke callable '{getattr(fn, '__name__', str(fn))}' because the following required arguments are missing: [{', '.join(unresolved_args)}]."
                )

            # Otherwise, resolve dependencies and call with them
            resolved_params = self.__resolveDependencies(
                getattr(fn, '__name__', str(fn)),
                dependencies
            )

            # Invoke the callable with resolved parameters
            result = fn(**resolved_params)

            # Handle the result, which may be a coroutine
            return self.__handleSyncAsyncResult(result)

        except Exception as inspect_error:

            # If inspection fails, try direct call as last resort
            try:
                result = fn()
                return self.__handleSyncAsyncResult(result)

            # If direct call fails, raise inspection error
            except TypeError:
                raise OrionisContainerException(
                    f"Failed to invoke callable: {inspect_error}"
                ) from inspect_error

    def __reflectTarget(
        self,
        target: Callable[..., Any],
        *,
        is_class: bool = True
    ) -> tuple:
        """
        Analyzes the target (class or callable) and extracts its dependency signature.

        This method uses reflection to inspect either a class or a callable (function/method)
        and retrieves its constructor or callable dependencies. It determines the appropriate
        reflection strategy based on the `is_class` flag.

        Parameters
        ----------
        target : Callable[..., Any]
            The class or callable to be analyzed for dependencies.
        is_class : bool, optional
            If True, treats the target as a class and inspects its constructor.
            If False, treats the target as a callable and inspects its signature.
            Default is True.

        Returns
        -------
        tuple
            A tuple containing:
                - name (str): The name of the class or callable.
                - dependencies (ResolveArguments): The resolved dependencies for the target.

        Notes
        -----
        This method is intended for internal use to facilitate dependency resolution
        by extracting the required arguments for instantiation or invocation.
        """

        # Select the appropriate reflection class based on whether the target is a class or callable
        reflection = ReflectionConcrete(target) if is_class else ReflectionCallable(target)

        # Get the dependencies for the constructor (if class) or signature (if callable)
        dependencies = reflection.getConstructorDependencies() if is_class else reflection.getDependencies()

        # Get the name of the class or callable for identification
        name = reflection.getClassName() if is_class else reflection.getName()

        # Return both the name and the dependencies as a tuple
        return name, dependencies

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

        return self.__resolveDependencies(name, dependencies)

    def __resolveDependencies(
        self,
        name: Optional[str],
        dependencies: Optional[ResolveArguments]
    ) -> dict:
        """
        Resolves and returns a dictionary of dependencies for a given class or callable.

        This method analyzes the provided dependencies (as extracted by reflection)
        and attempts to resolve each required argument. It checks for unresolved
        dependencies, handles default values, and recursively resolves dependencies
        using the container or auto-resolution logic.

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

        try:
            # If there are no dependencies, return empty dict
            if not dependencies:
                return {}

            # Check for unresolved dependencies
            if dependencies.unresolved:
                unresolved_args = [name for name in dependencies.unresolved.keys()]
                raise OrionisContainerException(
                    f"Cannot resolve '{name}' because the following required arguments are missing: [{', '.join(unresolved_args)}]."
                )

            # Resolve dependencies
            params = {}
            for param_name, dep in dependencies.resolved.items():
                params[param_name] = self.__resolveSingleDependency(name, param_name, dep)

            return params

        except Exception as e:

            # If the exception is already an OrionisContainerException, re-raise it
            if isinstance(e, OrionisContainerException):
                raise e from None

            # Otherwise, raise a new OrionisContainerException with additional context
            raise OrionisContainerException(
                f"Error resolving dependencies for '{name}': {str(e)}"
            ) from e

    def __resolveSingleDependency(
        self,
        name: str,
        param_name: str,
        dependency: Argument
    ) -> Any:
        """
        Resolves a single dependency parameter.

        This method centralizes the logic for resolving individual dependencies,
        following a priority order: default values, container bindings, auto-resolution,
        direct instantiation, and callable invocation.

        Parameters
        ----------
        name : str
            The name of the class or callable being resolved (for error context).
        param_name : str
            The name of the parameter being resolved.
        dependency : Argument
            The dependency argument object containing type and metadata.

        Returns
        -------
        Any
            The resolved dependency instance or value.

        Raises
        ------
        OrionisContainerException
            If the dependency cannot be resolved through any available method.
        """

        # Check if the dependency is already in the current scope (for SCOPED lifetime)
        scoped = ScopedContext.getCurrentScope()
        if scoped and (dependency.type in scoped or dependency.full_class_path in scoped):
            return scoped[dependency.type] if dependency.type in scoped else scoped[dependency.full_class_path]

        # If the dependency has a default value, use it
        if dependency.default is not None:
            return dependency.default

        # If the dependency is a built-in type with a default value, return it
        if dependency.module_name == 'builtins' and dependency.resolved:
            return dependency.default

        # If the dependency is a built-in type, raise an exception
        elif dependency.module_name == 'builtins' and not dependency.resolved:
            raise OrionisContainerException(
                f"Cannot resolve '{name}' because parameter '{param_name}' depends on built-in type '{dependency.type.__name__}'."
            )

        # Try to resolve from container using type (Abstract or Interface)
        # This will automatically handle SCOPED lifetime through resolve() -> __resolveScoped()
        if self.bound(dependency.type):
            return self.resolve(self.getBinding(dependency.type))

        # Try to resolve from container using full class path
        # This will also handle SCOPED lifetime appropriately
        if self.bound(dependency.full_class_path):
            return self.resolve(self.getBinding(dependency.full_class_path))

        # Try auto-resolution first
        if self.__canAutoResolve(dependency.type):
            return self.__autoResolve(dependency.type)

        # Try to instantiate directly if it's a concrete class
        if ReflectionConcrete.isConcreteClass(dependency.type):
            return self.__instantiateWithReflection(dependency.type, is_class=True)

        # Try to call directly if it's a callable
        if callable(dependency.type) and not isinstance(dependency.type, type):
            return self.__instantiateWithReflection(dependency.type, is_class=False)

        # If the dependency cannot be resolved, raise an exception
        raise OrionisContainerException(
            f"Cannot resolve dependency '{param_name}' of type '{dependency.type.__name__}' for '{name}'."
        )

    def __instantiateWithReflection(
        self,
        target: Callable[..., Any],
        is_class: bool = True
    ) -> Any:
        """
        Helper method to instantiate a target with reflection-based dependency resolution.
        Supports both synchronous and asynchronous callables automatically.

        Parameters
        ----------
        target : Callable[..., Any]
            The class or callable to instantiate.
        is_class : bool
            Whether the target is a class (True) or callable (False).

        Returns
        -------
        Any
            The instantiated object or callable result. If the callable is async,
            the coroutine will be handled automatically.
        """

        # Reflect the target to get its dependencies
        resolved_params = self.__resolveDependencies(
            *self.__reflectTarget(target, is_class=is_class)
        )

        # If the target is a class, instantiate it with resolved parameters
        result = target(**resolved_params)

        # Handle the result, which may be a coroutine
        return self.__handleSyncAsyncResult(result)

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
        try:
            # If args or kwargs are provided, use them directly
            if args or kwargs:
                if isinstance(type_, type):
                    return type_(*args, **kwargs)
                elif callable(type_):
                    return type_(*args, **kwargs)

            # Try auto-resolution first for unregistered types
            if self.__canAutoResolve(type_):
                return self.__autoResolve(type_)

            # Use the unified reflection-based instantiation
            if ReflectionConcrete.isConcreteClass(type_):
                return self.__instantiateWithReflection(type_, is_class=True)

            if callable(type_) and not isinstance(type_, type):
                return self.__instantiateWithReflection(type_, is_class=False)

            # If the type is neither a concrete class nor a callable, raise an exception
            raise OrionisContainerException(
                f"Cannot force resolve: {getattr(type_, '__name__', str(type_))} is neither a concrete class nor a callable."
            )

        except Exception as e:
            if isinstance(e, OrionisContainerException):
                raise e from None

            raise OrionisContainerException(
                f"Error resolving '{getattr(type_, '__name__', str(type_))}': {str(e)}"
            ) from e

    def __canAutoResolve(
        self,
        type_: Callable[..., Any]
    ) -> bool:
        """
        Check if a type can be automatically resolved by the container.

        This method determines whether a given type meets all the criteria for
        automatic dependency resolution. For a type to be auto-resolvable, it must
        be a concrete class that belongs to a valid application namespace, is
        not a built-in Python type, and is actually instantiable.

        The validation process includes checking that the type is:
        - A proper class (not a function, module, or other callable)
        - Not a built-in Python type (str, int, list, etc.)
        - A concrete class (not abstract or interface)
        - Not a generic type or type variable
        - Part of a valid namespace defined in the container configuration
        - Actually instantiable (has a callable constructor)

        Parameters
        ----------
        type_ : Callable[..., Any]
            The type to check for auto-resolution eligibility. This should be
            a class or callable that represents the type to be validated for
            automatic dependency injection.

        Returns
        -------
        bool
            True if the type can be automatically resolved by the container,
            False otherwise. Returns True only when all validation criteria
            are met: the type is a concrete, instantiable class from a valid
            namespace and is not a built-in type.
        """

        # Check if the provided parameter is actually a class type
        # Functions, modules, and other callables are not eligible for auto-resolution
        if not isinstance(type_, type):
            return False

        # Exclude built-in Python types (str, int, list, dict, etc.)
        # These types cannot be auto-resolved as they require explicit values
        if hasattr(type_, '__module__') and type_.__module__ == 'builtins':
            return False

        # Check if the type belongs to a valid namespace for auto-resolution
        # Only classes from configured application namespaces are allowed
        if not self.__isValidNamespace(type_):
            return False

        # Check if the type is actually instantiable
        if not self.__isInstantiable(type_):
            return False

        # All checks passed - type can be auto-resolved
        return True

    def __isValidNamespace(self, type_: type) -> bool:
        """
        Checks if a type belongs to a valid namespace for auto-resolution.

        Parameters
        ----------
        type_ : type
            The type to check for valid namespace.

        Returns
        -------
        bool
            True if the type belongs to a valid namespace, False otherwise.
        """

        # Verify that the module name starts with any of the valid namespace prefixes
        if hasattr(type_, '__module__'):
            module_name = type_.__module__
            return any(module_name.startswith(namespace) for namespace in self.__valid_namespaces)

        # If the type has no module information, it cannot be auto-resolved
        return False

    def __isInstantiable(self, type_: type) -> bool:
        """
        Checks if a type is actually instantiable (not abstract, not generic, etc.).

        This method performs comprehensive checks to determine if a class can be
        safely instantiated through auto-resolution. It validates that the class
        is concrete, not abstract, not a generic type, and has a callable constructor.

        Parameters
        ----------
        type_ : type
            The type to check for instantiability.

        Returns
        -------
        bool
            True if the type can be instantiated, False otherwise.
        """

        try:

            # 1. Check if it's a concrete class using ReflectionConcrete
            if not ReflectionConcrete.isConcreteClass(type_):
                return False

            # 2. Check if it's an abstract class or has abstract methods
            if self.__isAbstractClass(type_):
                return False

            # 3. Check if it's a generic type (like List[T], Dict[K,V])
            if self.__isGenericType(type_):
                return False

            # 4. Check if it's a protocol or typing construct
            if self.__isProtocolOrTyping(type_):
                return False

            # 5. Check if the constructor is callable
            if not hasattr(type_, '__init__'):
                return False

            # 6. Basic instantiation test with empty args (if no required params)
            if self.__hasRequiredConstructorParams(type_):
                # If it has required params, we can still auto-resolve if they can be resolved
                return True
            else:
                # If no required params, try a quick instantiation test
                return self.__canQuickInstantiate(type_)

        except Exception:
            # If any check fails with an exception, consider it non-instantiable
            return False

    def __isAbstractClass(self, type_: type) -> bool:
        """
        Checks if a type is an abstract class.

        Parameters
        ----------
        type_ : type
            The type to check.

        Returns
        -------
        bool
            True if the type is abstract, False otherwise.
        """

        # Check if it's explicitly marked as abstract
        if hasattr(type_, '__abstractmethods__') and type_.__abstractmethods__:
            return True

        # Check if it inherits from ABC (safely)
        try:
            if issubclass(type_, abc.ABC):
                return True
        except TypeError:
            # type_ is not a class, so it can't be abstract
            pass

        # Check if it has abstract methods
        try:
            # Try to get abstract methods using reflection
            for attr_name in dir(type_):
                attr = getattr(type_, attr_name)
                if hasattr(attr, '__isabstractmethod__') and attr.__isabstractmethod__:
                    return True
        except Exception:
            pass

        return False

    def __isGenericType(self, type_: type) -> bool:
        """
        Checks if a type is a generic type (e.g., List[T], Dict[K,V]).

        Parameters
        ----------
        type_ : type
            The type to check.

        Returns
        -------
        bool
            True if the type is generic, False otherwise.
        """

        # Check for generic alias (Python 3.7+)
        if hasattr(typing, 'get_origin') and typing.get_origin(type_) is not None:
            return True

        # Check for older style generic types
        if hasattr(type_, '__origin__'):
            return True

        # Check if it's a typing construct
        if hasattr(typing, '_GenericAlias') and isinstance(type_, typing._GenericAlias):
            return True

        # Check for type variables
        if hasattr(typing, 'TypeVar') and isinstance(type_, typing.TypeVar):
            return True

        return False

    def __isProtocolOrTyping(self, type_: type) -> bool:
        """
        Checks if a type is a Protocol or other typing construct that shouldn't be instantiated.

        Parameters
        ----------
        type_ : type
            The type to check.

        Returns
        -------
        bool
            True if the type is a protocol or typing construct, False otherwise.
        """

        # Check if it's a Protocol (Python 3.8+)
        try:
            if hasattr(typing, 'Protocol') and issubclass(type_, typing.Protocol):
                return True

        # type_ is not a class, so it can't be a Protocol
        except TypeError:
            pass

        # Check if it's in the typing module
        if hasattr(type_, '__module__') and type_.__module__ == 'typing':
            return True

        # Check for common typing constructs that shouldn't be instantiated
        typing_constructs = ['Union', 'Optional', 'Any', 'Callable', 'Type']
        if hasattr(type_, '__name__') and type_.__name__ in typing_constructs:
            return True

        return False

    def __hasRequiredConstructorParams(self, type_: type) -> bool:
        """
        Checks if a type has required constructor parameters.

        Parameters
        ----------
        type_ : type
            The type to check.

        Returns
        -------
        bool
            True if the type has required constructor parameters, False otherwise.
        """

        try:

            # Use reflection to get constructor dependencies
            reflection = ReflectionConcrete(type_)
            dependencies = reflection.getConstructorDependencies()

            # Check if there are any unresolved dependencies or required parameters
            if dependencies and dependencies.unresolved:
                return True

            # Check if there are resolved dependencies that don't have defaults and can't be resolved
            if dependencies and dependencies.resolved:
                for param_name, dep in dependencies.resolved.items():
                    # Only consider it required if it has no default AND can't be resolved by container
                    if dep.default is None and not self.bound(dep.type) and not self.bound(dep.full_class_path):
                        return True

            # If no unresolved dependencies and all resolved have defaults, return False
            return False

        except Exception:

            # If reflection fails, assume it has required params to be safe
            return True

    def __canQuickInstantiate(self, type_: type) -> bool:
        """
        Performs a quick instantiation test to verify the type can be created.

        This method attempts to create an instance of the type without arguments
        to verify that it can be instantiated successfully.

        Parameters
        ----------
        type_ : type
            The type to test.

        Returns
        -------
        bool
            True if the type can be instantiated, False otherwise.
        """

        try:
            # For safety, first check if the constructor signature suggests it's safe to instantiate
            try:

                # Use inspect to get the constructor signature
                sig = inspect.signature(type_.__init__)

                # If __init__ has required parameters beyond 'self', skip quick instantiation
                required_params = [
                    p for name, p in sig.parameters.items()
                    if name != 'self' and p.default == inspect.Parameter.empty
                ]

                # If there are required parameters, we cannot quick instantiate
                if required_params:
                    return False

            except (ValueError, TypeError):

                # If we can't inspect the signature, assume it's not safe
                return False

            # Attempt to create an instance only if it seems safe
            instance = type_()

            # If successful, clean up and return True
            del instance
            return True

        except Exception:

            # If instantiation fails for any reason, it's not auto-resolvable
            return False

    def __autoResolve(
        self,
        type_: Callable[..., Any],
        *args,
        **kwargs
    ) -> Any:
        """
        Automatically resolves and instantiates a type with its dependencies.

        Parameters
        ----------
        type_ : Callable[..., Any]
            The class or callable to auto-resolve.
        *args : tuple
            Positional arguments to pass directly to the constructor or callable.
        **kwargs : dict
            Keyword arguments to pass directly to the constructor or callable.

        Returns
        -------
        Any
            An instance of the requested type, with all dependencies resolved recursively.

        Raises
        ------
        OrionisContainerException
            If the type cannot be auto-resolved or if circular dependencies are detected.
        """

        # Build a unique key for the type to track resolution and detect circular dependencies
        type_key = f"{type_.__module__}.{type_.__name__}"
        if type_key in self.__resolution_cache:
            raise OrionisContainerException(
                f"Circular dependency detected while auto-resolving '{type_.__name__}'"
            )

        try:
            # Mark this type as being resolved to prevent circular dependencies
            self.__resolution_cache[type_key] = True

            # Validate that the type can still be auto-resolved at resolution time
            if not self.__canAutoResolve(type_):
                raise OrionisContainerException(
                    f"Type '{type_.__name__}' cannot be auto-resolved. "
                    f"It may be abstract, generic, or not from a valid namespace."
                )

            # If explicit arguments are provided, instantiate/call directly
            if args or kwargs:
                return type_(*args, **kwargs)

            # Use unified reflection-based instantiation
            if ReflectionConcrete.isConcreteClass(type_):
                return self.__instantiateWithReflection(type_, is_class=True)
            elif callable(type_) and not isinstance(type_, type):
                return self.__instantiateWithReflection(type_, is_class=False)
            else:
                raise OrionisContainerException(
                    f"Type '{type_.__name__}' is not a concrete class or callable"
                )

        except Exception as e:
            # Remove the type from the resolution cache on error
            self.__resolution_cache.pop(type_key, None)

            if isinstance(e, OrionisContainerException):
                raise
            else:
                raise OrionisContainerException(
                    f"Failed to auto-resolve '{type_.__name__}': {str(e)}"
                ) from e

        finally:
            # Always clean up the resolution cache after resolution attempt
            self.__resolution_cache.pop(type_key, None)

    def call(
        self,
        instance: Any,
        method_name: str,
        *args,
        **kwargs
    ) -> Any:
        """
        Call a method on an instance with automatic dependency injection.
        Supports both synchronous and asynchronous methods automatically.

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
            The result of the method call. If the method is async,
            the coroutine will be handled automatically.
        """

        # Validate inputs
        self.__validateCallInputs(instance, method_name)

        # Get the method
        method = getattr(instance, method_name)

        # Execute the method with appropriate handling
        return self.__executeMethod(method, *args, **kwargs)

    async def callAsync(
        self,
        instance: Any,
        method_name: str,
        *args,
        **kwargs
    ) -> Any:
        """
        Async version of call for when you're in an async context and need to await the result.

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
            The result of the method call, properly awaited if async.
        """

        # Validate inputs
        self.__validateCallInputs(instance, method_name)

        # Get the method
        method = getattr(instance, method_name)

        # Execute the method with async handling
        result = self.__executeMethod(method, *args, **kwargs)

        # If the result is a coroutine, await it
        if asyncio.iscoroutine(result):
            return await result

        # Otherwise, return the result directly
        return result

    def __validateCallInputs(self, instance: Any, method_name: str) -> None:
        """
        Validates the inputs for the call methods.

        Parameters
        ----------
        instance : Any
            The instance to validate.
        method_name : str
            The method name to validate.

        Raises
        ------
        OrionisContainerException
            If validation fails.
        """

        # Ensure the instance is a valid object (allow __main__ for development)
        if instance is None:
            raise OrionisContainerException("Instance cannot be None")

        # Ensure the instance is a valid object with a class
        if not hasattr(instance, '__class__'):
            raise OrionisContainerException("Instance must be a valid object with a class")

        # Validate method_name parameter
        if not isinstance(method_name, str):
            raise OrionisContainerException(
                f"Method name must be a string, got {type(method_name).__name__}"
            )

        if not method_name.strip():
            raise OrionisContainerException(
                "Method name cannot be empty or whitespace"
            )

        # Ensure the method exists and is callable
        method = getattr(instance, method_name, None)
        if not callable(method):
            raise OrionisContainerException(
                f"Method '{method_name}' not found or not callable on instance '{type(instance).__name__}'."
            )

    def invoke(
        self,
        fn: Callable,
        *args,
        **kwargs
    ) -> Any:
        """
        Invokes a callable with automatic dependency injection and sync/async handling.

        Parameters
        ----------
        fn : Callable
            The callable to invoke.
        *args : tuple
            Positional arguments to pass to the callable.
        **kwargs : dict
            Keyword arguments to pass to the callable.

        Returns
        -------
        Any
            The result of the callable invocation.
        """

        # Validate that fn is indeed callable
        if not callable(fn):
            raise OrionisContainerException(
                f"Provided fn '{getattr(fn, '__name__', str(fn))}' is not callable."
            )

        # Execute the callable with appropriate handling
        return self.__executeMethod(fn, *args, **kwargs)

    async def invokeAsync(
        self,
        fn: Callable,
        *args,
        **kwargs
    ) -> Any:
        """
        Async version of invoke for when you're in an async context and need to await the result.

        Parameters
        ----------
        fn : Callable
            The callable to invoke.
        *args : tuple
            Positional arguments to pass to the callable.
        **kwargs : dict
            Keyword arguments to pass to the callable.

        Returns
        -------
        Any
            The result of the callable invocation, properly awaited if async.
        """

        # Validate that fn is indeed callable
        if not callable(fn):
            raise OrionisContainerException(
                f"Provided fn '{getattr(fn, '__name__', str(fn))}' is not callable."
            )

        # Execute the callable with appropriate handling
        result = self.__executeMethod(fn, *args, **kwargs)

        # If the result is a coroutine, await it
        if asyncio.iscoroutine(result):
            return await result

        # Otherwise, return the result directly
        return result

    def __executeMethod(
        self,
        method: Callable,
        *args,
        **kwargs
    ) -> Any:
        """
        Executes a method with automatic dependency injection and sync/async handling.

        Parameters
        ----------
        method : Callable
            The method to execute.
        *args : tuple
            Positional arguments to pass to the method.
        **kwargs : dict
            Keyword arguments to pass to the method.

        Returns
        -------
        Any
            The result of the method execution.
        """

        # If args or kwargs are provided, use them directly
        if args or kwargs:
            return self.__invokeCallableUniversal(method, *args, **kwargs)

        # For methods without provided arguments, try simple call first
        try:

            # Get method signature to check if it needs parameters
            sig = inspect.signature(method)

            # Filter out 'self' parameter for bound methods
            params = [p for name, p in sig.parameters.items()
                     if name != 'self' and p.default == inspect.Parameter.empty]

            # If no required parameters, call directly
            if not params:
                result = method()
                return self.__handleSyncAsyncResult(result)

            # If has required parameters, try dependency injection
            result = self.__instantiateWithReflection(method, is_class=False)
            return result

        except Exception as reflection_error:

            # If reflection fails, try simple call as fallback
            try:
                result = method()
                return self.__handleSyncAsyncResult(result)

            # If both reflection and simple call fail, raise an exception
            except TypeError:
                raise OrionisContainerException(
                    f"Failed to call method '{method.__name__}': {reflection_error}"
                ) from reflection_error
