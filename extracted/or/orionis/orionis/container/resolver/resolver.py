from typing import Any, Callable
from orionis.container.context.scope import ScopedContext
from orionis.container.contracts.container import IContainer
from orionis.container.contracts.resolver import IResolver
from orionis.container.entities.binding import Binding
from orionis.container.enums.lifetimes import Lifetime
from orionis.container.exceptions import OrionisContainerException
from orionis.services.introspection.callables.reflection import ReflectionCallable
from orionis.services.introspection.concretes.reflection import ReflectionConcrete
from orionis.services.introspection.dependencies.entities.known_dependencies import KnownDependency
from orionis.services.introspection.dependencies.entities.method_dependencies import MethodDependency

class Resolver(IResolver):

    def __init__(
        self,
        container: IContainer
    ):
        """
        Parameters
        ----------
        container : IContainer
            The container instance used by the resolver to resolve dependencies.

        Notes
        -----
        Initializes the Resolver with a reference to the dependency injection container.
        This allows the resolver to access registered bindings and resolve dependencies
        as required throughout the container's lifecycle.
        """
        self.container = container

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
                "The binding must be an instance of Binding."
            )

        # Handle based on binding type and lifetime
        if binding.lifetime == Lifetime.TRANSIENT:
            return self.__resolveTransient(binding, *args, **kwargs)
        elif binding.lifetime == Lifetime.SINGLETON:
            return self.__resolveSingleton(binding, *args, **kwargs)
        elif binding.lifetime == Lifetime.SCOPED:
            return self.__resolveScoped(binding, *args, **kwargs)

    def resolveType(
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

        # Try to resolve the type with the provided arguments
        # If the type is already bound in the container, resolve it directly
        # or if args or kwargs are provided, instantiate it directly
        # If the type is a concrete class, instantiate it with resolved dependencies
        try:

            # Check if the type is already bound in the container
            if self.container.bound(type_):
                binding = self.container.getBinding(type_)
                return self.resolve(binding, *args, **kwargs)

            # If args or kwargs are provided, use them directly
            if args or kwargs:

                # For classes
                if isinstance(type_, type):
                    return type_(*args, **kwargs)

                # For callables
                elif callable(type_):
                    return type_(*args, **kwargs)

            # Otherwise use reflection to resolve dependencies
            # If the type is a concrete class, instantiate it with resolved dependencies
            elif ReflectionConcrete.isConcreteClass(type_):
                return type_(**self.__resolveDependencies(type_, is_class=True))

            # Try to call directly if it's a callable
            elif callable(type_) and not isinstance(type_, type):
                return type_(**self.__resolveDependencies(type_, is_class=False))

            # If the type is neither a concrete class nor a callable, raise an exception
            raise OrionisContainerException(
                f"Cannot force resolve: {getattr(type_, '__name__', str(type_))} is neither a concrete class nor a callable."
            )

        except Exception as e:

            # Get the type name safely to avoid AttributeError
            type_name = getattr(type_, '__name__', str(type_))
            module_name = getattr(type_, '__module__', "unknown module")

            # Provide more detailed error message
            error_msg = f"Error while force-resolving '{type_name}' from '{module_name}':\n{str(e)}"

            # If it's already an OrionisContainerException, just re-raise it with the context
            if isinstance(e, OrionisContainerException):
                raise e from None

            # Raise a new OrionisContainerException with the original exception as context
            else:
                raise OrionisContainerException(error_msg) from e

    def resolveSignature(
        self,
        signature: MethodDependency
    ) -> dict:
        """
        Resolves dependencies defined in a method signature.

        Parameters
        ----------
        signature : MethodDependency
            The method dependency information to resolve.

        Returns
        -------
        dict
            A dictionary of resolved parameter values.

        Raises
        ------
        OrionisContainerException
            If any dependencies cannot be resolved.
        """
        # If no dependencies to resolve, return empty dict
        if not signature.resolved and not signature.unresolved:
            return {}

        # If there are unresolved dependencies, raise an error
        if signature.unresolved:
            raise OrionisContainerException(
                f"Cannot resolve method dependencies because the following parameters are unresolved: {', '.join(signature.unresolved)}."
            )

        # Create a dict of resolved dependencies
        params = {}
        for param_name, dep in signature.resolved.items():
            if isinstance(dep, KnownDependency):
                # Try to resolve the dependency using the container
                if self.container.bound(dep.type):
                    params[param_name] = self.resolve(
                        self.container.getBinding(dep.type)
                    )
                elif self.container.bound(dep.full_class_path):
                    params[param_name] = self.resolve(
                        self.container.getBinding(dep.full_class_path)
                    )
                # Try to resolve directly if it's a concrete type
                elif ReflectionConcrete.isConcreteClass(dep.type):
                    params[param_name] = self.resolveType(dep.type)
                else:
                    raise OrionisContainerException(
                        f"Cannot resolve dependency '{param_name}' of type '{dep.type.__name__}'."
                    )
            else:
                # Use default value
                params[param_name] = dep

        return params

    def __resolveTransient(self, binding: Binding, *args, **kwargs) -> Any:
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

    def __resolveSingleton(self, binding: Binding, *args, **kwargs) -> Any:
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
        # Return existing instance if available
        if binding.instance:
            return binding.instance

        # Create instance if needed
        if binding.concrete:
            if args or kwargs:
                binding.instance = self.__instantiateConcreteWithArgs(binding.concrete, *args, **kwargs)
            else:
                binding.instance = self.__instantiateConcreteReflective(binding.concrete)
            return binding.instance

        # If the binding has a function defined
        elif binding.function:
            if args or kwargs:
                result = self.__instantiateCallableWithArgs(binding.function, *args, **kwargs)
            else:
                result = self.__instantiateCallableReflective(binding.function)

            # Store the result directly as the singleton instance
            # We don't automatically invoke factory function results anymore
            binding.instance = result
            return binding.instance

        # If neither concrete class nor function is defined
        else:
            raise OrionisContainerException(
                "Cannot resolve singleton binding: neither a concrete class, instance, nor function is defined."
            )

    def __resolveScoped(self, binding: Binding, *args, **kwargs) -> Any:
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
        scope = ScopedContext.getCurrentScope()
        if scope is None:
            raise OrionisContainerException(
                f"No active scope found while resolving scoped service '{binding.alias}'. "
                f"Use 'with container.createContext():' to create a scope context."
            )

        if binding.alias in scope:
            return scope[binding.alias]

        # Create a new instance
        if binding.concrete:
            if args or kwargs:
                instance = self.__instantiateConcreteWithArgs(binding.concrete, *args, **kwargs)
            else:
                instance = self.__instantiateConcreteReflective(binding.concrete)
        elif binding.function:
            if args or kwargs:
                instance = self.__instantiateCallableWithArgs(binding.function, *args, **kwargs)
            else:
                instance = self.__instantiateCallableReflective(binding.function)
        else:
            raise OrionisContainerException(
                "Cannot resolve scoped binding: neither a concrete class nor a function is defined."
            )

        scope[binding.alias] = instance
        return instance

    def __instantiateConcreteWithArgs(self, concrete: Callable[..., Any], *args, **kwargs) -> Any:
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

    def __instantiateCallableWithArgs(self, fn: Callable[..., Any], *args, **kwargs) -> Any:
        """
        Invokes a callable with the provided arguments.

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
            The result of the callable.
        """

        # Try to invoke the callable with the provided arguments
        try:

            # If the callable is a function, invoke it directly
            return fn(*args, **kwargs)

        except TypeError as e:

            # If invocation fails, use ReflectionCallable to get function name and signature
            rf_callable = ReflectionCallable(fn)
            function_name = rf_callable.getName()
            signature = rf_callable.getSignature()

            # Raise an exception with detailed information about the failure
            raise OrionisContainerException(
                f"Failed to invoke function [{function_name}] with the provided arguments: {e}\n"
                f"Expected function signature: [{signature}]"
            ) from e

    def __instantiateConcreteReflective(self, concrete: Callable[..., Any]) -> Any:
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
        # Resolve dependencies for the concrete class
        params = self.__resolveDependencies(concrete, is_class=True)

        # Instantiate the concrete class with resolved dependencies
        return concrete(**params)

    def __instantiateCallableReflective(self, fn: Callable[..., Any]) -> Any:
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

        # Resolve dependencies for the callable
        params = self.__resolveDependencies(fn, is_class=False)

        # Invoke the callable with resolved dependencies
        return fn(**params)

    def __resolveDependencies(
        self,
        target: Callable[..., Any],
        *,
        is_class: bool = False
    ) -> dict:
        """
        Resolves dependencies for a target callable or class.

        Parameters
        ----------
        target : Callable[..., Any]
            The target callable or class whose dependencies to resolve.
        is_class : bool, optional
            Whether the target is a class (True) or a callable (False).

        Returns
        -------
        dict
            A dictionary of resolved dependencies.
        """
        try:

            # Use ReflectionConcrete for classes and ReflectionCallable for callables
            if is_class:
                reflection = ReflectionConcrete(target)
                dependencies = reflection.getConstructorDependencies()
                name = reflection.getClassName()

            # If the target is a callable, use ReflectionCallable
            else:
                reflection = ReflectionCallable(target)
                dependencies = reflection.getDependencies()
                name = reflection.getName()

            # Check for unresolved dependencies
            if dependencies.unresolved:
                unresolved_args = ', '.join(dependencies.unresolved)
                raise OrionisContainerException(
                    f"Cannot resolve '{name}' because the following required arguments are missing: [{unresolved_args}]."
                )

            # Resolve dependencies
            params = {}
            for param_name, dep in dependencies.resolved.items():

                # If the dependency is a KnownDependency, resolve it
                if isinstance(dep, KnownDependency):

                    # If the dependency is a built-in type, raise an exception
                    if dep.module_name == 'builtins':
                        raise OrionisContainerException(
                            f"Cannot resolve '{name}' because parameter '{param_name}' depends on built-in type '{dep.type.__name__}'."
                        )

                    # Try to resolve from container using type (Abstract or Interface)
                    if self.container.bound(dep.type):
                        params[param_name] = self.resolve(
                            self.container.getBinding(dep.type)
                        )

                    # Try to resolve from container using full class path
                    elif self.container.bound(dep.full_class_path):
                        params[param_name] = self.resolve(
                            self.container.getBinding(dep.full_class_path)
                        )

                    # Try to instantiate directly if it's a concrete class
                    elif ReflectionConcrete.isConcreteClass(dep.type):
                        params[param_name] = dep.type(**self.__resolveDependencies(dep.type, is_class=True))

                    # Try to call directly if it's a callable
                    elif callable(dep.type) and not isinstance(dep.type, type):
                        params[param_name] = dep.type(**self.__resolveDependencies(dep.type, is_class=False))

                    # If the dependency cannot be resolved, raise an exception
                    else:
                        raise OrionisContainerException(
                            f"Cannot resolve dependency '{param_name}' of type '{dep.type.__name__}' for '{name}'."
                        )
                else:
                    # Use default value
                    params[param_name] = dep

            # Return the resolved parameters
            return params

        except ImportError as e:

            # Get target name safely
            target_name = getattr(target, '__name__', str(target))
            module_name = getattr(target, '__module__', "unknown module")

            # Improved circular import detection with more helpful guidance
            if "circular import" in str(e).lower() or "cannot import name" in str(e).lower():
                raise OrionisContainerException(
                    f"Circular import detected while resolving dependencies for '{target_name}' in module '{module_name}'.\n"
                    f"This typically happens when two modules import each other. Consider:\n"
                    f"1. Restructuring your code to avoid circular dependencies\n"
                    f"2. Using delayed imports inside methods rather than at module level\n"
                    f"3. Using dependency injection to break the cycle\n"
                    f"Original error: {str(e)}"
                ) from e
            else:
                raise OrionisContainerException(
                    f"Import error while resolving dependencies for '{target_name}' in module '{module_name}':\n"
                    f"{str(e)}"
                ) from e

        except Exception as e:

            # More robust attribute extraction with fallbacks
            target_type = "class" if isinstance(target, type) else "function"
            target_name = getattr(target, '__name__', str(target))
            module_name = getattr(target, '__module__', "unknown module")

            # More detailed error message with context about the failure
            error_msg = (
                f"Error resolving dependencies for {target_type} '{target_name}' in '{module_name}':\n"
                f"{str(e)}\n"
            )

            # Add specific guidance based on error type
            if isinstance(e, TypeError):
                error_msg += "This may be caused by incompatible argument types or missing required parameters."
            elif isinstance(e, AttributeError):
                error_msg += "This may be caused by accessing undefined attributes in the dependency chain."
            error_msg += "\nCheck that all dependencies are properly registered in the container."

            # Raise a more informative exception
            raise OrionisContainerException(error_msg) from e
