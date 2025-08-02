from dataclasses import dataclass
from typing import Any, Dict, List
from orionis.services.introspection.dependencies.entities.known_dependencies import KnownDependency
from orionis.services.introspection.exceptions import ReflectionTypeError

@dataclass(frozen=True, kw_only=True)
class MethodDependency:
    """
    Represents the dependencies of a method, separating resolved and unresolved dependencies.

    Parameters
    ----------
    resolved : Dict[KnownDependency, Any]
        A dictionary mapping resolved dependency descriptors to their corresponding
        resolved instances or values for the method. All keys must be KnownDependency instances.
    unresolved : List[str]
        A list of method parameter names or dependency identifiers that could not be resolved.
        Must contain only non-empty strings.

    Raises
    ------
    ReflectionTypeError
        If types don't match the expected:
            - resolved: Dict[KnownDependency, Any]
            - unresolved: List[str]
    ValueError
        If resolved contains None keys or unresolved contains empty strings
    """
    resolved: Dict[KnownDependency, Any]
    unresolved: List[str]

    def __post_init__(self):
        """
        Validates types and values of attributes during initialization.

        Raises
        ------
        ReflectionTypeError
            If types don't match the expected:
                - resolved: Dict[KnownDependency, Any]
                - unresolved: List[str]
        ValueError
            If resolved contains None keys or unresolved contains empty strings
        """
        # Validate 'resolved' is a dict with proper key types
        if not isinstance(self.resolved, dict):
            raise ReflectionTypeError(
                f"'resolved' must be a dict, got {type(self.resolved).__name__}"
            )

        # Validate 'unresolved' is a list of valid parameter names
        if not isinstance(self.unresolved, list):
            raise ReflectionTypeError(
                f"'unresolved' must be a list, got {type(self.unresolved).__name__}"
            )