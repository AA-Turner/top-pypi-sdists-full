from dataclasses import dataclass
from typing import Type, Any
from orionis.services.introspection.exceptions import ReflectionTypeError

@dataclass(frozen=True, kw_only=True)
class KnownDependency:
    """
    Represents a fully resolved dependency with complete type information.

    Parameters
    ----------
    module_name : str
        The name of the module where the dependency is defined.
        Must be a non-empty string without spaces.
    class_name : str
        The name of the class/type being resolved.
        Must be a valid Python identifier.
    type : Type
        The actual Python type object of the resolved dependency.
    full_class_path : str
        The full import path to the class (e.g., 'package.module.ClassName').
        Must match 'module_name.class_name' pattern.

    Raises
    ------
    ReflectionTypeError
        If any field has incorrect type.
    ValueError
        If string fields are empty or don't meet format requirements.
    """
    module_name: str
    class_name: str
    type: Type[Any]
    full_class_path: str

    def __post_init__(self):
        """
        Validates all fields during initialization.

        Raises
        ------
        ReflectionTypeError
            If any field has incorrect type.
        ValueError
            If string fields are empty or don't meet format requirements.
        """
        # Validate module_name
        if not isinstance(self.module_name, str):
            raise ReflectionTypeError(f"module_name must be str, got {type(self.module_name).__name__}")

        # Validate class_name
        if not isinstance(self.class_name, str):
            raise ReflectionTypeError(f"class_name must be str, got {type(self.class_name).__name__}")

        # Validate type
        if self.type is None:
            raise ValueError("The 'type' field must not be None. Please provide a valid Python type object for the dependency.")

        # Validate full_class_path
        if not isinstance(self.full_class_path, str):
            raise ReflectionTypeError(f"full_class_path must be str, got {type(self.full_class_path).__name__}")