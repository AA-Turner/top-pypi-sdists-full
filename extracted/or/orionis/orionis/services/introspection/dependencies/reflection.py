import inspect
from typing import Any, Dict, List
from orionis.services.introspection.dependencies.contracts.reflection import IReflectDependencies
from orionis.services.introspection.dependencies.entities.callable_dependencies import CallableDependency
from orionis.services.introspection.dependencies.entities.class_dependencies import ClassDependency
from orionis.services.introspection.dependencies.entities.method_dependencies import MethodDependency
from orionis.services.introspection.dependencies.entities.known_dependencies import KnownDependency
from orionis.services.introspection.exceptions import ReflectionValueError

class ReflectDependencies(IReflectDependencies):
    """
    This class is used to reflect dependencies of a given object.
    """

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

    def getConstructorDependencies(self) -> ClassDependency:
        """
        Get the resolved and unresolved dependencies from the constructor of the instance's class.

        Returns
        -------
        ClassDependency
            A structured representation of the constructor dependencies, containing:
            - resolved: Dictionary of resolved dependencies with their names and values.
            - unresolved: List of unresolved dependencies (parameter names without default values or annotations).
        """
        signature = self.__inspectSignature(self.__target.__init__)
        resolved_dependencies: Dict[str, Any] = {}
        unresolved_dependencies: List[str] = []

        for param_name, param in signature.parameters.items():

            # Skip parameters that are not relevant for dependency resolution
            if self.__paramSkip(param_name, param):
                continue

            # Add to the list of unresolved dependencies if it has no default value or annotation
            if param.annotation is param.empty and param.default is param.empty:
                unresolved_dependencies.append(param_name)
                continue

            # Parameters with default values
            if param.default is not param.empty:
                resolved_dependencies[param_name] = param.default
                continue

            # If the parameter has an annotation, it is added to the list of resolved dependencies
            if param.annotation is not param.empty:
                module_path = param.annotation.__module__
                resolved_dependencies[param_name] = KnownDependency(
                    module_name=module_path,
                    class_name=param.annotation.__name__,
                    type=param.annotation,
                    full_class_path=f"{module_path}.{param.annotation.__name__}"
                )

        return ClassDependency(
            resolved=resolved_dependencies,
            unresolved=unresolved_dependencies
        )

    def getMethodDependencies(self, method_name: str) -> MethodDependency:
        """
        Get the resolved and unresolved dependencies from a method of the instance's class.

        Parameters
        ----------
        method_name : str
            The name of the method to inspect

        Returns
        -------
        MethodDependency
            A structured representation of the method dependencies, containing:
            - resolved: Dictionary of resolved dependencies with their names and values.
            - unresolved: List of unresolved dependencies (parameter names without default values or annotations).
        """
        signature = self.__inspectSignature(getattr(self.__target, method_name))
        resolved_dependencies: Dict[str, Any] = {}
        unresolved_dependencies: List[str] = []

        for param_name, param in signature.parameters.items():

            # Skip parameters that are not relevant for dependency resolution
            if self.__paramSkip(param_name, param):
                continue

            # Add to the list of unresolved dependencies if it has no default value or annotation
            if param.annotation is param.empty and param.default is param.empty:
                unresolved_dependencies.append(param_name)
                continue

            # Parameters with default values
            if param.default is not param.empty:
                resolved_dependencies[param_name] = param.default
                continue

            # If the parameter has an annotation, it is added to the list of resolved dependencies
            if param.annotation is not param.empty:
                module_path = param.annotation.__module__
                resolved_dependencies[param_name] = KnownDependency(
                    module_name=module_path,
                    class_name=param.annotation.__name__,
                    type=param.annotation,
                    full_class_path=f"{module_path}.{param.annotation.__name__}"
                )

        return MethodDependency(
            resolved=resolved_dependencies,
            unresolved=unresolved_dependencies
        )

    def getCallableDependencies(self, fn: callable) -> CallableDependency:
        """
        Get the resolved and unresolved dependencies from a callable function.

        Parameters
        ----------
        fn : callable
            The function to inspect.

        Returns
        -------
        MethodDependency
            A structured representation of the callable dependencies, containing:
            - resolved: Dictionary of resolved dependencies with their names and values.
            - unresolved: List of unresolved dependencies (parameter names without default values or annotations).
        """
        signature = inspect.signature(fn)
        resolved_dependencies: Dict[str, Any] = {}
        unresolved_dependencies: List[str] = []

        for param_name, param in signature.parameters.items():

            # Skip parameters that are not relevant for dependency resolution
            if self.__paramSkip(param_name, param):
                continue

            # Add to the list of unresolved dependencies if it has no default value or annotation
            if param.annotation is param.empty and param.default is param.empty:
                unresolved_dependencies.append(param_name)
                continue

            # Parameters with default values
            if param.default is not param.empty:
                resolved_dependencies[param_name] = param.default
                continue

            # If the parameter has an annotation, it is added to the list of resolved dependencies
            if param.annotation is not param.empty:
                module_path = param.annotation.__module__
                resolved_dependencies[param_name] = KnownDependency(
                    module_name=module_path,
                    class_name=param.annotation.__name__,
                    type=param.annotation,
                    full_class_path=f"{module_path}.{param.annotation.__name__}"
                )

        return CallableDependency(
            resolved=resolved_dependencies,
            unresolved=unresolved_dependencies
        )