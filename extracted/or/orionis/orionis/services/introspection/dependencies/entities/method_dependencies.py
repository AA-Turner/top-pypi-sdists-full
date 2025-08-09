from dataclasses import dataclass
from typing import Any, Dict, List
from orionis.services.introspection.dependencies.entities.known_dependencies import KnownDependency
from orionis.services.introspection.exceptions import ReflectionTypeError

@dataclass(frozen=True, kw_only=True)
class MethodDependency:
    """
    Represents the dependencies of a method, distinguishing between resolved and unresolved dependencies.

    Parameters
    ----------
    resolved : dict of KnownDependency to Any
        Dictionary mapping each resolved KnownDependency to its corresponding instance or value.
    unresolved : list of str
        List of parameter names or dependency identifiers that could not be resolved.

    Raises
    ------
    ReflectionTypeError
        If `resolved` is not a dictionary with KnownDependency keys, or if `unresolved` is not a list of strings.
    ValueError
        If `resolved` contains None keys or `unresolved` contains empty strings.

    Attributes
    ----------
    resolved : dict of KnownDependency to Any
        The resolved dependencies for the method.
    unresolved : list of str
        The unresolved dependencies for the method.
    """

    # Resolved dependencies mapped to their values
    resolved: Dict[KnownDependency, Any]

    # Unresolved dependencies as a list of parameter names
    unresolved: List[str]

    def __post_init__(self):
        """
        Validates the types and values of the attributes after initialization.

        Raises
        ------
        ReflectionTypeError
            If `resolved` is not a dictionary or `unresolved` is not a list.
        ValueError
            If `resolved` contains None keys or `unresolved` contains empty strings.
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