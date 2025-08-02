from dataclasses import dataclass
from typing import Any, Dict, List
from orionis.services.introspection.dependencies.entities.known_dependencies import KnownDependency
from orionis.services.introspection.exceptions import ReflectionTypeError

@dataclass(frozen=True, kw_only=True)
class ClassDependency:
    """
    Represents the dependencies of a class, separating resolved and unresolved dependencies.

    Parameters
    ----------
    resolved : Dict[KnownDependency, Any]
        A dictionary mapping resolved dependency descriptors to their corresponding resolved instances or values.
        All keys must be KnownDependency instances.
    unresolved : List[str]
        A list of dependency names or identifiers that could not be resolved.
        Must contain only strings.

    Attributes
    ----------
    resolved : Dict[KnownDependency, Any]
        Dictionary of resolved dependencies.
    unresolved : List[str]
        List of unresolved dependency names.
    """
    resolved: Dict[KnownDependency, Any]
    unresolved: List[str]

    def __post_init__(self):
        """
        Validates types of attributes during initialization.

        Raises
        ------
        ReflectionTypeError
            If types don't match the expected:
                - resolved: Dict[KnownDependency, Any]
                - unresolved: List[str]
        ValueError
            If resolved contains None keys or unresolved contains empty strings.
        """
        # Validate 'resolved' is a dict with KnownDependency keys
        if not isinstance(self.resolved, dict):
            raise ReflectionTypeError(
                f"'resolved' must be a dict, got {type(self.resolved).__name__}"
            )

        # Validate 'unresolved' is a list of non-empty strings
        if not isinstance(self.unresolved, list):
            raise ReflectionTypeError(
                f"'unresolved' must be a list, got {type(self.unresolved).__name__}"
            )