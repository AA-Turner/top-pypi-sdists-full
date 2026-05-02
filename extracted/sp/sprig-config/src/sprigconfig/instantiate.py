"""
Dynamic Class Instantiation (_target_ Support)

This module provides Hydra-style _target_ support for instantiating classes
from configuration. This enables powerful patterns like hexagonal architecture
with swappable adapters.

Example:
    >>> from sprigconfig import ConfigSingleton, instantiate
    >>>
    >>> # Config:
    >>> # adapters:
    >>> #   database:
    >>> #     _target_: myapp.adapters.PostgresAdapter
    >>> #     host: localhost
    >>> #     port: 5432
    >>>
    >>> cfg = ConfigSingleton.get()
    >>> db = instantiate(cfg.adapters.database)
    >>> # Returns: PostgresAdapter(host="localhost", port=5432)

Features:
    - Automatic parameter extraction from config
    - Type conversion based on type hints
    - Recursive instantiation for nested objects
    - LazySecret preservation
    - Rich error messages with context

Design Principles:
    - 100% backward compatible (opt-in feature)
    - Pure Python (uses inspect + importlib)
    - Follows existing injection.py patterns
    - Secure error handling (no sensitive data in logs)
"""

import importlib
import inspect
from typing import Any, Union, get_type_hints

from sprigconfig.config import Config
from sprigconfig.exceptions import ConfigLoadError
from sprigconfig.lazy_secret import LazySecret


def instantiate(
    config_section: Union[Config, dict],
    *,
    _recursive_: bool = True,
    _convert_types_: bool = True
) -> Any:
    """
    Instantiate a class from config using _target_ key.

    This function reads a _target_ key from the config section, dynamically
    imports the specified class, extracts matching constructor parameters from
    the config, applies type conversion, and instantiates the class.

    Args:
        config_section: Config object or dict containing _target_ key
        _recursive_: If True, recursively instantiate nested _target_ objects (default: True)
        _convert_types_: If True, apply type conversion to constructor params (default: True)

    Returns:
        Instance of the class specified by _target_

    Raises:
        ConfigLoadError: If _target_ missing, class not found, invalid format, missing params, or instantiation fails

    Example:
        >>> from sprigconfig import ConfigSingleton, instantiate
        >>> cfg = ConfigSingleton.get()
        >>> adapter = instantiate(cfg.database)
    """

    # Step 1: Validate input and extract _target_
    if isinstance(config_section, Config):
        config_dict = config_section.to_dict()
    elif isinstance(config_section, dict):
        config_dict = config_section
    else:
        raise ConfigLoadError(
            f"instantiate() requires Config or dict, got {type(config_section).__name__}\n"
            f"Hint: Pass a config section with _target_ key"
        )

    target = config_dict.get("_target_")
    if not target:
        available_keys = [k for k in config_dict.keys() if not k.startswith("_")]
        raise ConfigLoadError(
            f"No _target_ key found in config section\n"
            f"Available keys: {available_keys if available_keys else '(none)'}\n"
            f"Hint: Add '_target_: your.module.ClassName' to the config"
        )

    # Step 2: Dynamically import the target class
    try:
        module_path, class_name = target.rsplit(".", 1)
    except ValueError:
        raise ConfigLoadError(
            f"Invalid _target_ format: '{target}'\n"
            f"Expected format: 'module.path.ClassName'\n"
            f"Hint: _target_ must contain at least one dot separating module and class name"
        )

    try:
        module = importlib.import_module(module_path)
    except ModuleNotFoundError as e:
        raise ConfigLoadError(
            f"Module not found for _target_: '{target}'\n"
            f"Module path: '{module_path}'\n"
            f"Reason: {e}\n"
            f"Hint: Check that the module is installed and importable"
        )

    try:
        target_class = getattr(module, class_name)
    except AttributeError:
        available = [n for n in dir(module) if not n.startswith("_")]
        raise ConfigLoadError(
            f"Class '{class_name}' not found in module '{module_path}'\n"
            f"Target: '{target}'\n"
            f"Available in module: {available[:10] if available else '(none)'}\n"
            f"Hint: Check the class name spelling and that it's defined in the module"
        )

    # Step 3: Inspect __init__ signature to get required parameters
    try:
        sig = inspect.signature(target_class.__init__)
    except (ValueError, TypeError) as e:
        raise ConfigLoadError(
            f"Failed to inspect {target_class.__name__}.__init__ signature\n"
            f"Target: '{target}'\n"
            f"Reason: {e}"
        )

    # Get type hints if available (for type conversion)
    try:
        type_hints = get_type_hints(target_class.__init__)
    except Exception:
        # If get_type_hints fails, we'll just skip type conversion for that param
        type_hints = {}

    # Step 4: Extract matching parameters from config
    init_params = {}
    missing_required = []

    for param_name, param in sig.parameters.items():
        if param_name == "self":
            continue

        # Check if parameter exists in config
        if param_name in config_dict:
            value = config_dict[param_name]

            # Step 4a: Recursive instantiation (if value has _target_)
            if _recursive_ and isinstance(value, (dict, Config)) and "_target_" in value:
                try:
                    value = instantiate(
                        value,
                        _recursive_=_recursive_,
                        _convert_types_=_convert_types_
                    )
                except ConfigLoadError:
                    # Re-raise with added context
                    raise
                except Exception as e:
                    raise ConfigLoadError(
                        f"Failed to recursively instantiate parameter '{param_name}'\n"
                        f"Parent class: {target_class.__name__}\n"
                        f"Nested _target_: {value.get('_target_') if isinstance(value, dict) else 'N/A'}\n"
                        f"Reason: {e}"
                    )

            # Step 4b: Type conversion (if type hint present)
            if _convert_types_ and param_name in type_hints:
                target_type = type_hints[param_name]
                try:
                    value = _convert_type(value, target_type)
                except ConfigLoadError:
                    # Re-raise with added context
                    raise
                except Exception as e:
                    raise ConfigLoadError(
                        f"Failed to convert parameter '{param_name}' to {target_type.__name__}\n"
                        f"Class: {target_class.__name__}\n"
                        f"Value: {value!r} (type: {type(value).__name__})\n"
                        f"Reason: {e}\n"
                        f"Hint: Check that the config value matches the expected type"
                    )

            init_params[param_name] = value

        # Check if parameter is required (no default value)
        elif param.default is inspect.Parameter.empty:
            missing_required.append(param_name)

    # Step 5: Validate required parameters
    if missing_required:
        available_keys = [k for k in config_dict.keys() if k != "_target_"]
        raise ConfigLoadError(
            f"Missing required parameters for {target_class.__name__}.__init__\n"
            f"Required: {missing_required}\n"
            f"Available in config: {available_keys if available_keys else '(none)'}\n"
            f"Target: '{target}'\n"
            f"Hint: Add missing parameters to config section or make them optional with defaults"
        )

    # Step 6: Instantiate the class
    try:
        instance = target_class(**init_params)
    except TypeError as e:
        raise ConfigLoadError(
            f"Failed to instantiate {target_class.__name__}\n"
            f"Parameters passed: {list(init_params.keys())}\n"
            f"Target: '{target}'\n"
            f"Reason: {e}\n"
            f"Hint: Check that parameter names match __init__ signature"
        )
    except Exception as e:
        raise ConfigLoadError(
            f"Error during {target_class.__name__} instantiation\n"
            f"Target: '{target}'\n"
            f"Reason: {e}\n"
            f"Hint: Check the __init__ method for runtime errors"
        )

    return instance


def _convert_type(value: Any, target_type: type) -> Any:
    """
    Convert a value to the target type.

    Follows the same type conversion logic as injection.py for consistency.

    Special handling:
    - LazySecret: never converted, always pass through
    - Config: never converted, always pass through

    Args:
        value: Raw value from config
        target_type: Target type hint

    Returns:
        Converted value

    Raises:
        ValueError: If conversion fails
    """
    # Special cases: never convert these types
    if isinstance(value, (LazySecret, Config)):
        return value

    # If already correct type, return as-is (fast path)
    if type(value) is target_type:
        return value

    # Type conversion matrix
    try:
        if target_type is str:
            return str(value)
        elif target_type is int:
            return int(value)
        elif target_type is float:
            return float(value)
        elif target_type is bool:
            # Handle string boolean conversion
            if isinstance(value, str):
                return value.lower() in ('true', '1', 'yes', 'on')
            return bool(value)
        elif target_type is list:
            if not isinstance(value, list):
                raise TypeError(f"Cannot convert {type(value).__name__} to list")
            return value
        elif target_type is dict:
            if not isinstance(value, dict):
                raise TypeError(f"Cannot convert {type(value).__name__} to dict")
            return value
        else:
            # Unknown type - return as-is (may be custom class)
            return value
    except (ValueError, TypeError) as e:
        raise ValueError(
            f"Cannot convert {value!r} (type: {type(value).__name__}) to {target_type.__name__}: {e}"
        )
