# sprigconfig/injection.py
"""
Spring Boot-style dependency injection for SprigConfig.

This module provides three patterns for dependency injection:
1. ConfigValue - Field-level descriptor for lazy config binding
2. @ConfigurationProperties - Class-level auto-binding decorator
3. @config_inject - Function parameter injection with override support

All patterns integrate with ConfigSingleton and support:
- Lazy resolution from current config
- Type conversion based on type hints
- LazySecret handling with configurable decryption
- Clear error messages with full context
"""

from typing import Any, Callable
import functools
import inspect

from .config_singleton import ConfigSingleton
from .config import Config
from .lazy_secret import LazySecret
from .exceptions import ConfigLoadError


# =============================================================================
# ConfigValue Descriptor
# =============================================================================

_MISSING = object()  # Sentinel for missing default


class ConfigValue:
    """
    Descriptor that lazily resolves config values from ConfigSingleton.

    Features:
    - Lazy resolution on attribute access (no caching)
    - Type conversion based on type hints
    - LazySecret handling with configurable decrypt parameter
    - Default value support
    - Clear error messages for missing keys

    Args:
        key: Dotted config key (e.g., "database.url")
        default: Default value if key missing (default: _MISSING sentinel)
        decrypt: For LazySecret values (default: False)
            - False: Return LazySecret object, decrypt on .get()
            - True: Auto-decrypt immediately at binding time

    Example:
        class MyService:
            db_url: str = ConfigValue("database.url")
            api_key: str = ConfigValue("api.key", decrypt=True)
            timeout: int = ConfigValue("service.timeout", default=30)

        service = MyService()
        print(service.db_url)  # Resolves from config

    Security:
        - decrypt=False (default) keeps secrets encrypted in memory
        - decrypt=True auto-decrypts (use only for frequently-accessed secrets)
    """

    def __init__(self, key: str, *, default: Any = _MISSING, decrypt: bool = False):
        self.key = key
        self.default = default
        self.decrypt = decrypt
        self._type_hint = None  # Set by __set_name__
        self._owner_name = None
        self._attr_name = None

    def __set_name__(self, owner, name):
        """
        Called when descriptor is assigned to a class attribute.
        Captures type hint from owner class annotations.
        """
        self._owner_name = owner.__name__
        self._attr_name = name
        self._type_hint = owner.__annotations__.get(name)

    def __get__(self, obj, objtype=None):
        """
        Resolve value from ConfigSingleton on attribute access.

        Called every time the attribute is accessed (no caching).
        This enables test refresh behavior.
        """
        if obj is None:
            return self  # Class access returns descriptor

        # Get current config from singleton
        try:
            cfg = ConfigSingleton.get()
        except ConfigLoadError as e:
            raise ConfigLoadError(
                f"ConfigSingleton not initialized when accessing "
                f"{self._owner_name}.{self._attr_name}\n"
                f"Original error: {e}\n"
                f"Hint: Call ConfigSingleton.initialize(profile, config_dir) at startup"
            )

        # Resolve from config (use sentinel if no default)
        default_to_use = None if self.default is _MISSING else self.default
        value = cfg.get(self.key, default_to_use)

        # Check if value is missing and no default provided
        if value is None and self.default is _MISSING:
            # Try to provide helpful context
            key_parts = self.key.split(".")
            if len(key_parts) > 1:
                parent_key = ".".join(key_parts[:-1])
                parent = cfg.get(parent_key)
                if isinstance(parent, (dict, Config)):
                    available = list(parent.keys()) if isinstance(parent, dict) else list(parent)
                    raise ConfigLoadError(
                        f"Config key '{self.key}' not found and no default provided.\n"
                        f"Descriptor: ConfigValue('{self.key}') on {self._owner_name}.{self._attr_name}\n"
                        f"Available keys at '{parent_key}': {available}\n"
                        f"Hint: Check your config files or add default= parameter"
                    )

            raise ConfigLoadError(
                f"Config key '{self.key}' not found and no default provided.\n"
                f"Descriptor: ConfigValue('{self.key}') on {self._owner_name}.{self._attr_name}\n"
                f"Hint: Check your config files or add default= parameter"
            )

        # Handle LazySecret
        if isinstance(value, LazySecret):
            if self.decrypt:
                try:
                    value = value.get()  # Auto-decrypt
                except Exception as e:
                    raise ConfigLoadError(
                        f"Failed to decrypt LazySecret for key '{self.key}'\n"
                        f"Descriptor: ConfigValue('{self.key}', decrypt=True) "
                        f"on {self._owner_name}.{self._attr_name}\n"
                        f"Reason: {e}\n"
                        f"Hint: Check APP_SECRET_KEY environment variable"
                    )
            # else: return LazySecret object (decrypt on .get())

        # Type conversion (only if not LazySecret and type hint present)
        if self._type_hint and value is not None and not isinstance(value, LazySecret):
            value = self._convert_type(value, self._type_hint)

        return value

    def __set__(self, obj, value):
        """Prevent overwriting descriptor (make it read-only)."""
        raise AttributeError(
            f"Cannot set config value '{self.key}' on {self._owner_name}.{self._attr_name}. "
            f"ConfigValue descriptors are read-only."
        )

    def resolve(self):
        """
        Resolve value directly without instance (for @config_inject).

        This method performs the same logic as __get__ but without
        requiring an instance object.

        Returns:
            Resolved config value

        Raises:
            ConfigLoadError: If config key is missing or resolution fails
        """
        # Get current config from singleton
        try:
            cfg = ConfigSingleton.get()
        except ConfigLoadError as e:
            raise ConfigLoadError(
                f"ConfigSingleton not initialized when resolving "
                f"ConfigValue('{self.key}')\n"
                f"Original error: {e}\n"
                f"Hint: Call ConfigSingleton.initialize(profile, config_dir) at startup"
            )

        # Resolve from config
        default_to_use = None if self.default is _MISSING else self.default
        value = cfg.get(self.key, default_to_use)

        # Check if value is missing and no default provided
        if value is None and self.default is _MISSING:
            raise ConfigLoadError(
                f"Config key '{self.key}' not found and no default provided.\n"
                f"ConfigValue('{self.key}')\n"
                f"Hint: Check your config files or add default= parameter"
            )

        # Handle LazySecret
        if isinstance(value, LazySecret):
            if self.decrypt:
                try:
                    value = value.get()  # Auto-decrypt
                except Exception as e:
                    raise ConfigLoadError(
                        f"Failed to decrypt LazySecret for key '{self.key}'\n"
                        f"ConfigValue('{self.key}', decrypt=True)\n"
                        f"Reason: {e}\n"
                        f"Hint: Check APP_SECRET_KEY environment variable"
                    )

        # Type conversion (only if not LazySecret and type hint present)
        if self._type_hint and value is not None and not isinstance(value, LazySecret):
            value = self._convert_type(value, self._type_hint)

        return value

    def _convert_type(self, value: Any, target_type: type) -> Any:
        """
        Convert YAML value to Python type hint.

        Supported conversions:
        - str, int, float, bool (primitives)
        - list, dict (collections, pass through)
        - Config (pass through)

        Args:
            value: Raw value from config
            target_type: Type hint from annotation

        Returns:
            Converted value

        Raises:
            ConfigLoadError: If conversion fails
        """
        # Already correct type
        if type(value) is target_type:
            return value

        # Special cases: never convert
        if isinstance(value, (LazySecret, Config)):
            return value

        # Type conversion logic
        try:
            if target_type is str:
                return str(value)
            elif target_type is int:
                return int(value)
            elif target_type is float:
                return float(value)
            elif target_type is bool:
                # Handle string bool conversion
                if isinstance(value, str):
                    return value.lower() in ('true', '1', 'yes', 'on')
                return bool(value)
            elif target_type is list:
                if isinstance(value, list):
                    return value
                raise TypeError(f"Cannot convert {type(value).__name__} to list")
            elif target_type is dict:
                if isinstance(value, dict):
                    return value
                raise TypeError(f"Cannot convert {type(value).__name__} to dict")
            else:
                # Unknown type - return as-is (may be custom class)
                return value
        except (ValueError, TypeError) as e:
            raise ConfigLoadError(
                f"Cannot convert config value to type '{target_type.__name__}'\n"
                f"Key: {self.key}\n"
                f"Value: {value!r} (type: {type(value).__name__})\n"
                f"Expected: {target_type.__name__}\n"
                f"Descriptor: ConfigValue('{self.key}') on {self._owner_name}.{self._attr_name}\n"
                f"Reason: {e}\n"
                f"Hint: Check your config file and ensure the value is a valid {target_type.__name__}"
            )


# =============================================================================
# @ConfigurationProperties Decorator
# =============================================================================

def ConfigurationProperties(prefix: str):
    """
    Class decorator for automatic configuration binding.

    Features:
    - Auto-binds all type-hinted attributes from config prefix
    - Nested object auto-instantiation (recursive binding)
    - Preserves original Config object via ._config attribute
    - Type conversion for primitives
    - LazySecret handling (stays encrypted by default)

    Args:
        prefix: Dotted config prefix (e.g., "app.database")

    Usage:
        @ConfigurationProperties(prefix="database")
        class DatabaseConfig:
            url: str
            port: int
            pool: ConnectionPoolConfig  # Auto-instantiate nested

        db = DatabaseConfig()
        print(db.url)          # Bound from config["database"]["url"]
        print(db._config.url)  # Access to Config object features

    Notes:
    - Only binds type-hinted attributes (explicit > implicit)
    - Nested classes must be decorated with @ConfigurationProperties
    - ._config provides escape hatch for Config methods (to_dict, dump, etc.)
    """

    def decorator(cls):
        original_init = cls.__init__

        def __init__(self, *args, **kwargs):
            # Call original __init__ if user-defined
            if original_init != object.__init__:
                try:
                    original_init(self, *args, **kwargs)
                except TypeError:
                    # Handle case where __init__ expects no args but we're calling with self
                    pass

            # Resolve config section
            try:
                cfg = ConfigSingleton.get()
            except ConfigLoadError as e:
                raise ConfigLoadError(
                    f"ConfigSingleton not initialized for @ConfigurationProperties "
                    f"on {cls.__name__}\n"
                    f"Original error: {e}\n"
                    f"Hint: Call ConfigSingleton.initialize(profile, config_dir) at startup"
                )

            section = cfg.get(prefix)

            # Store Config object for flexibility
            if isinstance(section, Config):
                self._config = section
            elif isinstance(section, dict):
                self._config = Config(section)
            elif section is None:
                raise ConfigLoadError(
                    f"Config prefix '{prefix}' not found in config.\n"
                    f"Class: {cls.__name__}\n"
                    f"Hint: Check your config files and ensure '{prefix}' exists"
                )
            else:
                raise ConfigLoadError(
                    f"Config prefix '{prefix}' resolved to non-dict type: "
                    f"{type(section).__name__}\n"
                    f"Class: {cls.__name__}\n"
                    f"Hint: Ensure '{prefix}' points to a config section (dict)"
                )

            # Auto-bind type-hinted attributes
            if hasattr(cls, '__annotations__'):
                for attr_name, attr_type in cls.__annotations__.items():
                    if attr_name.startswith('_'):
                        continue  # Skip private attributes

                    value = self._config.get(attr_name)

                    if value is None:
                        # Skip missing keys (could add default support later)
                        continue

                    # Handle LazySecret (don't try to instantiate it!)
                    if isinstance(value, LazySecret):
                        # Keep encrypted by default
                        setattr(self, attr_name, value)
                    # Handle nested objects (auto-instantiate if class type)
                    elif _is_config_class(attr_type):
                        try:
                            # Recursively instantiate nested config class
                            # Assumes nested class also has @ConfigurationProperties
                            nested_instance = attr_type()
                            setattr(self, attr_name, nested_instance)
                        except Exception as e:
                            raise ConfigLoadError(
                                f"Failed to instantiate nested config class "
                                f"{attr_type.__name__}\n"
                                f"Parent: {cls.__name__}.{attr_name}\n"
                                f"Reason: {e}\n"
                                f"Hint: Ensure nested class has @ConfigurationProperties decorator"
                            )
                    else:
                        # Type conversion
                        try:
                            converted = _convert_type_for_properties(value, attr_type, cls.__name__, attr_name)
                            setattr(self, attr_name, converted)
                        except Exception as e:
                            raise ConfigLoadError(
                                f"Type conversion failed for {cls.__name__}.{attr_name}\n"
                                f"Value: {value!r} (type: {type(value).__name__})\n"
                                f"Expected: {attr_type.__name__ if hasattr(attr_type, '__name__') else str(attr_type)}\n"
                                f"Reason: {e}"
                            )

        cls.__init__ = __init__
        return cls

    return decorator


def _is_config_class(type_hint) -> bool:
    """Check if type hint is a class (for nested object detection)."""
    return isinstance(type_hint, type) and type_hint not in (str, int, float, bool, list, dict)


def _convert_type_for_properties(value: Any, target_type: type, class_name: str, attr_name: str) -> Any:
    """Type conversion for @ConfigurationProperties (same logic as ConfigValue)."""
    # Already correct type
    if type(value) is target_type:
        return value

    # Special cases
    if isinstance(value, (LazySecret, Config)):
        return value

    # Type conversion
    try:
        if target_type is str:
            return str(value)
        elif target_type is int:
            return int(value)
        elif target_type is float:
            return float(value)
        elif target_type is bool:
            if isinstance(value, str):
                return value.lower() in ('true', '1', 'yes', 'on')
            return bool(value)
        elif target_type is list:
            if isinstance(value, list):
                return value
            raise TypeError(f"Cannot convert {type(value).__name__} to list")
        elif target_type is dict:
            if isinstance(value, dict):
                return value
            raise TypeError(f"Cannot convert {type(value).__name__} to dict")
        else:
            # Unknown type - return as-is
            return value
    except (ValueError, TypeError) as e:
        raise ConfigLoadError(
            f"Cannot convert config value to type '{target_type.__name__}'\n"
            f"Class: {class_name}.{attr_name}\n"
            f"Value: {value!r} (type: {type(value).__name__})\n"
            f"Expected: {target_type.__name__}\n"
            f"Reason: {e}"
        )


# =============================================================================
# @config_inject Decorator
# =============================================================================

def config_inject(func: Callable) -> Callable:
    """
    Function decorator for parameter injection from config.

    Features:
    - Injects ConfigValue defaults into function parameters
    - Allows explicit overrides at call time
    - Type conversion based on parameter annotations
    - LazySecret handling with decrypt parameter

    Usage:
        @config_inject
        def connect_db(
            host: str = ConfigValue("database.host"),
            port: int = ConfigValue("database.port", default=5432),
            user: str = None  # Required parameter (no default)
        ):
            return connect(host, port, user)

        connect_db(user="admin")                # Uses config for host/port
        connect_db(user="admin", host="local")  # Override host

    Notes:
    - Explicit arguments take precedence over config
    - ConfigValue parameters resolved lazily at call time
    - Non-ConfigValue defaults work as normal
    """

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        sig = inspect.signature(func)

        # Build arguments dict
        bound_args = {}

        # Bind positional arguments
        param_names = list(sig.parameters.keys())
        for i, arg in enumerate(args):
            if i < len(param_names):
                bound_args[param_names[i]] = arg

        # Bind keyword arguments (overrides positional)
        bound_args.update(kwargs)

        # Resolve ConfigValue defaults for missing parameters
        for param_name, param in sig.parameters.items():
            if param_name in bound_args:
                continue  # Already provided

            if isinstance(param.default, ConfigValue):
                # Resolve from config using resolve() method
                try:
                    resolved = param.default.resolve()
                    bound_args[param_name] = resolved
                except Exception as e:
                    raise ConfigLoadError(
                        f"Failed to resolve ConfigValue parameter '{param_name}' "
                        f"in function {func.__name__}\n"
                        f"Reason: {e}"
                    )
            elif param.default != inspect.Parameter.empty:
                # Regular default value
                bound_args[param_name] = param.default

        return func(**bound_args)

    return wrapper
