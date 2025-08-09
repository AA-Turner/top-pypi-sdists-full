from dataclasses import dataclass
from typing import Any, Dict, List
from orionis.services.introspection.dependencies.entities.known_dependencies import KnownDependency
from orionis.services.introspection.exceptions import ReflectionTypeError

@dataclass(frozen=True, kw_only=True)
class ClassDependency:
    """
    Represents the dependencies of a class, distinguishing between resolved and unresolved dependencies.

    Parameters
    ----------
    resolved : dict of KnownDependency to Any
        Dictionary mapping KnownDependency instances to their resolved values or instances.
    unresolved : list of str
        List of dependency names or identifiers that could not be resolved.

    Attributes
    ----------
    resolved : dict of KnownDependency to Any
        The resolved dependencies for the class.
    unresolved : list of str
        The unresolved dependency names or identifiers.

    Raises
    ------
    ReflectionTypeError
        If 'resolved' is not a dictionary with KnownDependency keys or 'unresolved' is not a list.
    ValueError
        If 'resolved' contains None keys or 'unresolved' contains empty strings.
    """

    # Resolved dependencies mapped to their values
    resolved: Dict[KnownDependency, Any]

    # Unresolved dependencies as a list of parameter names
    unresolved: List[str]

    def __post_init__(self):
        """
        Validates the types of the 'resolved' and 'unresolved' attributes after initialization.

        Raises
        ------
        ReflectionTypeError
            If 'resolved' is not a dict or 'unresolved' is not a list.
        ValueError
            If 'resolved' contains None keys or 'unresolved' contains empty strings.
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