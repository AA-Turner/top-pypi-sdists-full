import inspect
from typing import Any, Dict
from orionis.services.introspection.dependencies.contracts.reflection import IReflectDependencies
from orionis.services.introspection.dependencies.entities.argument import Argument
from orionis.services.introspection.dependencies.entities.resolve_argument import ResolveArguments
from orionis.services.introspection.exceptions import ReflectionValueError

class ReflectDependencies(IReflectDependencies):

    def __init__(self, target = None):
        """
        Initializes the ReflectDependencies instance with the given object.

        Parameters
        ----------
        target : Any
            The object whose dependencies are to be reflected.
        """
        self.__target = target

    def __paramSkip(self, param_name: str, param: inspect.Parameter) -> bool:
        """
        Determines whether a parameter should be skipped during dependency inspection.

        Parameters
        ----------
        param_name : str
            The name of the parameter.
        param : inspect.Parameter
            The parameter object to inspect.

        Returns
        -------
        bool
            True if the parameter should be skipped, False otherwise.
        """
        # Skip common parameters like 'self', 'cls', or special argument names
        if param_name in {'self', 'cls', 'args', 'kwargs'}:
            return True

        # Skip 'self' in class methods or instance methods
        if param_name == 'self' and isinstance(self.__target, type):
            return True

        # Skip special parameters like *args and **kwargs
        if param.kind in {param.VAR_POSITIONAL, param.VAR_KEYWORD}:
            return True

        return False

    def __inspectSignature(self, target) -> inspect.Signature:
        """
        Safely retrieves the signature of a given target.

        Parameters
        ----------
        target : Any
            The target object (function, method, or callable) to inspect.

        Returns
        -------
        inspect.Signature
            The signature of the target.

        Raises
        ------
        ReflectionValueError
            If the signature cannot be inspected.
        """
        if not callable(target):
            raise ReflectionValueError(f"Target {target} is not callable and cannot have a signature.")

        try:
            return inspect.signature(target)
        except (ReflectionValueError, TypeError, Exception) as e:
            raise ReflectionValueError(f"Unable to inspect signature of {target}: {str(e)}")

    def __getDependencies(self, signature: inspect.Signature) -> ResolveArguments:
        """
        Analyze function signature parameters to categorize dependencies as resolved or unresolved.

        This method examines each parameter in a function signature and determines whether
        it can be automatically resolved for dependency injection based on type annotations
        and default values. Parameters are categorized into two groups: those that can be
        automatically resolved by the dependency injection system and those that require
        manual intervention.

        Parameters
        ----------
        signature : inspect.Signature
            The function signature to analyze for dependencies. Must be a valid signature
            object obtained from inspect.signature().

        Returns
        -------
        ResolveArguments
            A data structure containing two dictionaries:

            - resolved : Dict[str, Argument]
                Parameters that can be automatically resolved. Includes parameters with:
                - Type annotations from non-builtin modules
                - Default values (regardless of type annotation)

            - unresolved : Dict[str, Argument]
                Parameters that cannot be automatically resolved. Includes parameters with:
                - No type annotation and no default value
                - Builtin type annotations without default values (int, str, bool, etc.)

        Notes
        -----
        - Parameters named 'self', 'cls', 'args', 'kwargs' and variadic parameters
          (*args, **kwargs) are automatically excluded from analysis
        - Parameters with default values are always considered resolved, regardless
          of their type annotation
        - Builtin types (int, str, bool, etc.) without default values are considered
          unresolved as they typically require explicit values
        - Custom classes and imported types with annotations are considered resolved
          as they can be instantiated by the dependency injection system
        """

        # Initialize dictionaries to store categorized dependencies
        resolved_dependencies: Dict[str, Argument] = {}
        unresolved_dependencies: Dict[str, Argument] = {}
        ordered_dependencies: Dict[str, Argument] = {}

        # Iterate through all parameters in the signature
        for param_name, param in signature.parameters.items():

            # Skip parameters that are not relevant for dependency resolution
            # (self, cls, *args, **kwargs, etc.)
            if self.__paramSkip(param_name, param):
                continue

            # Case 1: Parameters with no annotation and no default value
            # These cannot be resolved automatically and require manual provision
            if param.annotation is param.empty and param.default is param.empty:
                unresolved_dependencies[param_name] = Argument(
                    resolved=False,
                    module_name=None,
                    class_name=None,
                    type=Any,
                    full_class_path=None,
                )
                ordered_dependencies[param_name] = unresolved_dependencies[param_name]
                continue

            # Case 2: Parameters with default values
            # These are always considered resolved since they have fallback values
            if param.default is not param.empty:
                resolved_dependencies[param_name] = Argument(
                    resolved=True,
                    module_name=type(param.default).__module__,
                    class_name=type(param.default).__name__,
                    type=type(param.default),
                    full_class_path=f"{type(param.default).__module__}.{type(param.default).__name__}",
                    default=param.default
                )
                ordered_dependencies[param_name] = resolved_dependencies[param_name]
                continue

            # Case 3: Parameters with type annotations
            if param.annotation is not param.empty:
                # Special handling for builtin types without defaults
                # Builtin types (int, str, bool, etc.) are considered unresolved
                # when they lack default values, as they typically need explicit values
                if param.annotation.__module__ == 'builtins' and param.default is param.empty:
                    unresolved_dependencies[param_name] = Argument(
                        resolved=False,
                        module_name=param.annotation.__module__,
                        class_name=param.annotation.__name__,
                        type=param.annotation,
                        full_class_path=f"{param.annotation.__module__}.{param.annotation.__name__}"
                    )
                    ordered_dependencies[param_name] = unresolved_dependencies[param_name]
                else:
                    # Non-builtin types with annotations are considered resolved
                    # as they can be instantiated by the dependency injection system
                    resolved_dependencies[param_name] = Argument(
                        resolved=True,
                        module_name=param.annotation.__module__,
                        class_name=param.annotation.__name__,
                        type=param.annotation,
                        full_class_path=f"{param.annotation.__module__}.{param.annotation.__name__}"
                    )
                    ordered_dependencies[param_name] = resolved_dependencies[param_name]
                continue

        # Return the categorized dependencies
        return ResolveArguments(
            resolved=resolved_dependencies,
            unresolved=unresolved_dependencies,
            ordered=ordered_dependencies
        )

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

        # Extract the constructor signature from the target class
        return self.__getDependencies(self.__inspectSignature(self.__target.__init__))

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

        # Extract the method signature from the target class
        return self.__getDependencies(self.__inspectSignature(getattr(self.__target, method_name)))

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

        # Extract the callable signature from the target object
        return self.__getDependencies(inspect.signature(self.__target))