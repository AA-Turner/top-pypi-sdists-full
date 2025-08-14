from dataclasses import dataclass
from typing import Optional, Type, Any
from orionis.services.introspection.exceptions import ReflectionTypeError

@dataclass(frozen=True, kw_only=True)
class Argument:
    """
    Represents a function or method argument with type information and resolution status.

    This class encapsulates metadata about an argument including its type information,
    module location, resolution status, and optional default value. It is primarily
    used in dependency injection and introspection systems to track argument details
    and validate type consistency.

    Attributes
    ----------
    resolved : bool
        Flag indicating whether the argument has been resolved or processed.
    module_name : str
        The name of the module where the argument's type is defined.
    class_name : str
        The name of the class representing the argument's type.
    type : Type[Any]
        The Python type object representing the argument's type.
    full_class_path : str
        The complete dotted path to the argument's type (module.class).
    default : Optional[Any], default=None
        The default value for the argument, if any. When None, indicates
        the argument is required and must be explicitly provided.

    Notes
    -----
    The class performs automatic validation during initialization through the
    __post_init__ method. Validation ensures type consistency and completeness
    of required fields when no default value is provided.
    """
    resolved: bool
    module_name: str
    class_name: str
    type: Type[Any]
    full_class_path: str
    default: Optional[Any] = None

    def __post_init__(self):
        """
        Validate all fields during initialization to ensure data integrity.

        This method performs comprehensive validation of the Argument instance fields
        after dataclass initialization. Validation ensures that all required string
        fields are properly typed and that the type field is not None when no default
        value is provided.

        Returns
        -------
        None
            This method does not return any value. It performs in-place validation
            and raises exceptions if validation fails.

        Raises
        ------
        ReflectionTypeError
            If module_name, class_name, or full_class_path are not string types.
        ValueError
            If the 'type' field is None when default is None, indicating missing
            type information for a required argument.

        Notes
        -----
        Validation is conditionally performed only when default is None. Arguments
        with default values are assumed to have sufficient type information and
        skip the validation process.
        """
        # Skip validation when default value is provided
        # Arguments with defaults have implicit type information
        if self.default is None and self.resolved:

            # Validate module_name is a string type
            # Module names must be valid string identifiers
            if not isinstance(self.module_name, str):
                raise ReflectionTypeError(f"module_name must be str, got {type(self.module_name).__name__}")

            # Validate class_name is a string type
            # Class names must be valid string identifiers
            if not isinstance(self.class_name, str):
                raise ReflectionTypeError(f"class_name must be str, got {type(self.class_name).__name__}")

            # Validate type field is not None for required arguments
            # Type information is essential for dependency resolution
            if self.type is None:
                raise ValueError("The 'type' field must not be None. Please provide a valid Python type object for the dependency.")

            # Validate full_class_path is a string type
            # Full class path must be a valid dotted string notation
            if not isinstance(self.full_class_path, str):
                raise ReflectionTypeError(f"full_class_path must be str, got {type(self.full_class_path).__name__}")
