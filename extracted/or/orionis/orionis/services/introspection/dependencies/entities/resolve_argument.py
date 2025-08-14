from dataclasses import dataclass
from typing import Dict
from orionis.services.introspection.dependencies.entities.argument import Argument
from orionis.services.introspection.exceptions import ReflectionTypeError
from orionis.support.entities.base import BaseEntity

@dataclass(frozen=True, kw_only=True)
class ResolveArguments(BaseEntity):
    """
    Represents the dependencies of a class, distinguishing between resolved and unresolved dependencies.

    This class encapsulates both successfully resolved dependencies (with their corresponding
    Argument instances) and unresolved dependencies that could not be satisfied during
    dependency injection or reflection analysis.

    Parameters
    ----------
    resolved : Dict[str, Argument]
        Dictionary mapping dependency names to their corresponding Argument instances
        that have been successfully resolved.
    unresolved : Dict[str, Argument]
        Dictionary mapping dependency names to their corresponding Argument instances
        that could not be resolved during dependency analysis.

    Attributes
    ----------
    resolved : Dict[str, Argument]
        The resolved dependencies for the class, where each key is a dependency name
        and each value is an Argument instance containing the resolved information.
    unresolved : Dict[str, Argument]
        The unresolved dependency names mapped to their Argument instances, representing
        dependencies that could not be satisfied.

    Raises
    ------
    ReflectionTypeError
        If 'resolved' is not a dictionary or 'unresolved' is not a dictionary.
    """

    # Resolved dependencies as a dictionary of names to Argument instances
    resolved: Dict[str, Argument]

    # Unresolved dependencies as a dictionary of names to Argument instances
    unresolved: Dict[str, Argument]

    def __post_init__(self):
        """
        Validates the types and contents of the resolved and unresolved attributes.

        This method is automatically called by the dataclass after object initialization
        to ensure that both attributes are dictionaries with the correct types. It performs
        runtime type checking to maintain data integrity and provide clear error messages
        when invalid types are provided.

        Parameters
        ----------
        None

        Returns
        -------
        None
            This method performs validation only and does not return any value.

        Raises
        ------
        ReflectionTypeError
            If 'resolved' is not a dict or 'unresolved' is not a dict.
        """

        # Validate that the 'resolved' attribute is a dictionary type
        # This ensures that resolved dependencies can be properly accessed by name
        if not isinstance(self.resolved, dict):
            raise ReflectionTypeError(
                f"'resolved' must be a dict, got {type(self.resolved).__name__}"
            )

        # Validate that the 'unresolved' attribute is a dictionary type
        # This ensures that unresolved dependencies maintain the same structure as resolved ones
        if not isinstance(self.unresolved, dict):
            raise ReflectionTypeError(
                f"'unresolved' must be a dict, got {type(self.unresolved).__name__}"
            )