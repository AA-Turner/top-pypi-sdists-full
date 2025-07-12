import os
import json
from typing import Any, Dict, List, Optional, Union, Type, Callable
from ..click_importer import click


class FieldBehavior:
    """
    Defines how configuration fields behave when merging values from multiple sources.

    FieldBehavior controls the merging logic when the same field receives values from
    different configuration sources (CLI options, config files, environment variables).
    This is crucial for maintaining consistent and predictable configuration behavior
    across different deployment scenarios.

    The behavior system allows fine-grained control over how different types of fields
    should handle conflicting values, ensuring that sensitive configuration (like
    dependency specifications) cannot be accidentally overridden while still allowing
    flexible configuration for runtime parameters.

    Behavior Types:

    UNION (Default):
        - **For Primitive Types**: Override value takes precedence
        - **For Lists**: Values are merged by extending the base list with override values
        - **For Dictionaries**: Values are merged by updating base dict with override values
        - **For Nested Objects**: Recursively merge nested configuration objects

        Example:
        ```python
        # Base config: {"tags": ["prod", "web"]}
        # CLI config: {"tags": ["urgent"]}
        # Result: {"tags": ["prod", "web", "urgent"]}
        ```

    NOT_ALLOWED:
        - CLI values cannot override config file values
        - CLI values are only used if config file value is None
        - Ensures critical configuration is only set in one place to avoid ambiguity.

        Example:
        ```python
        # Base config: {"dependencies": {"numpy": "1.21.0"}}
        # CLI config: {"dependencies": {"numpy": "1.22.0"}}
        # Result: Exception is raised
        ```

        ```python
        # Base config: {"dependencies": {"pypi": null, "conda": null}}
        # CLI config: {"dependencies": {"pypi": {"numpy": "1.22.0"}}}
        # Result: {"dependencies": {"pypi": {"numpy": "1.22.0"}}} # since there is nothing in base config, the CLI config is used.
        ```

    Integration with Merging:
        The behavior is enforced by the `merge_field_values` function during configuration
        merging. Each field's behavior is checked and the appropriate merging logic is applied.
    """

    UNION = "union"  # CLI values are merged with config file values
    # CLI values are not allowed to ovveride the config values
    # unless config values are not specified
    NOT_ALLOWED = "not_allowed"


class CLIOption:
    """Metadata container for automatic CLI option generation from configuration fields.

    CLIOption defines how a ConfigField should be exposed as a command-line option in the
    generated CLI interface. It provides a declarative way to specify CLI parameter names,
    help text, validation rules, and Click-specific behaviors without tightly coupling
    configuration definitions to CLI implementation details.

    This class bridges the gap between configuration field definitions and Click option
    generation, allowing the same field definition to work seamlessly across different
    interfaces (CLI, config files, programmatic usage).

    Click Integration:
    The CLIOption metadata is used by CLIGenerator to create Click options:
    ```python
    @click.option("--port", "port", type=int, help="Application port")
    ```

    This is automatically generated from:
    ```python
    port = ConfigField(
        cli_meta=CLIOption(
            name="port",
            cli_option_str="--port",
            help="Application port"
        ),
        field_type=int
    )
    ```


    Parameters
    ----------
    name : str
        Parameter name used in Click option and function signature (e.g., "my_foo").
    cli_option_str : str
        Command-line option string (e.g., "--foo", "--enable/--disable").
    help : Optional[str], optional
        Help text displayed in CLI help output.
    short : Optional[str], optional
        Short option character (e.g., "-f" for "--foo").
    multiple : bool, optional
        Whether the option accepts multiple values.
    is_flag : bool, optional
        Whether this is a boolean flag option.
    choices : Optional[List[str]], optional
        List of valid choices for the option.
    default : Any, optional
        Default value for the CLI option (separate from ConfigField default).
    hidden : bool, optional
        Whether to hide this option from CLI (config file only).
    click_type : Optional[Any], optional
        Custom Click type for specialized parsing (e.g., KeyValuePair).
    """

    def __init__(
        self,
        name: str,  # This name corresponds to the `"my_foo"` in `@click.option("--foo","my_foo")`
        cli_option_str: str,  # This corresponds to the `--foo` in the `@click.option("--foo","my_foo")`
        help: Optional[str] = None,
        short: Optional[str] = None,
        multiple: bool = False,
        is_flag: bool = False,
        choices: Optional[List[str]] = None,
        default: Any = None,
        hidden: bool = False,
        click_type: Optional[Any] = None,
    ):
        self.name = name
        self.cli_option_str = cli_option_str
        self.help = help
        self.short = short
        self.multiple = multiple
        self.is_flag = is_flag
        self.choices = choices
        self.default = default
        self.hidden = hidden
        self.click_type = click_type


class ConfigField:
    """Descriptor for configuration fields with comprehensive metadata and behavior control.

    ConfigField is a Python descriptor that provides a declarative way to define configuration
    fields with rich metadata, validation, CLI integration, and merging behavior. It acts as
    both a data descriptor (controlling get/set access) and a metadata container.

    Key Functionality:
    - **Descriptor Protocol**: Implements __get__, __set__, and __set_name__ to control
      field access and automatically capture the field name during class creation.
    - **Type Safety**: Optional strict type checking during value assignment.
    - **CLI Integration**: Automatic CLI option generation via CLIOption metadata.
    - **Validation**: Built-in validation functions and required field checks.
    - **Merging Behavior**: Controls how values are merged from different sources (CLI, config files).
    - **Default Values**: Supports both static defaults and callable defaults for dynamic initialization.

    Merging Behaviors:
    - **UNION**: Values from different sources are merged (lists extended, dicts updated).
    - **NOT_ALLOWED**: Override values are ignored if base value exists.

    Field Lifecycle:
    1. **Definition**: Field is defined in a ConfigMeta-based class
    2. **Registration**: __set_name__ is called to register the field name
    3. **Initialization**: Field is initialized with None or nested config objects
    4. **Population**: Values are set from CLI options, config files, or direct assignment
    5. **Validation**: Validation functions are called during commit phase
    6. **Default Application**: Default values are applied to None fields

    Examples:
        Basic field definition:
        ```python
        name = ConfigField(
            field_type=str,
            required=True,
            help="Application name",
            example="myapp"
        )
        ```

        Field with CLI integration:
        ```python
        port = ConfigField(
            cli_meta=CLIOption(
                name="port",
                cli_option_str="--port",
                help="Application port"
            ),
            field_type=int,
            required=True,
            validation_fn=lambda x: 1 <= x <= 65535
        )
        ```

        Nested configuration field:
        ```python
        resources = ConfigField(
            field_type=ResourceConfig,
            help="Resource configuration"
        )
        ```

    Parameters
    ----------
    default : Any or Callable[["ConfigField"], Any], optional
        Default value for the field. Can be a static value or a callable for dynamic defaults.
    cli_meta : CLIOption, optional
        CLIOption instance defining CLI option generation parameters.
    field_type : type, optional
        Expected type of the field value (used for validation and nesting).
    required : bool, optional
        Whether the field must have a non-None value after configuration.
    help : str, optional
        Help text describing the field's purpose.
    behavior : str, optional
        FieldBehavior controlling how values are merged from different sources.
    example : Any, optional
        Example value for documentation and schema generation.
    strict_types : bool, optional
        Whether to enforce type checking during value assignment.
    validation_fn : callable, optional
        Optional function to validate field values.
    is_experimental : bool, optional
        Whether this field is experimental (for documentation).
    """

    def __init__(
        self,
        default: Union[Any, Callable[["ConfigField"], Any]] = None,
        cli_meta=None,
        field_type=None,
        required=False,
        help=None,
        behavior: str = FieldBehavior.UNION,
        example=None,
        strict_types=True,
        validation_fn: Optional[Callable] = None,
        is_experimental=False,  # This property is for bookkeeping purposes and for export in schema.
        parsing_fn: Optional[Callable] = None,
    ):
        if behavior == FieldBehavior.NOT_ALLOWED and ConfigMeta.is_instance(field_type):
            raise ValueError(
                "NOT_ALLOWED behavior cannot be set for ConfigMeta-based objects."
            )
        if callable(default) and not ConfigMeta.is_instance(field_type):
            raise ValueError(
                f"Default value for {field_type} is a callable but it is not a ConfigMeta-based object."
            )

        self.default = default
        self.cli_meta = cli_meta
        self.field_type = field_type
        self.strict_types = strict_types
        # Strict types means that the __set__ will raise an error if the type of the valu
        # doesn't match the type of the field.
        self.required = required
        self.help = help
        self.behavior = behavior
        self.example = example
        self.name = None
        self.validation_fn = validation_fn
        self.is_experimental = is_experimental
        self.parsing_fn = parsing_fn
        self._qual_name_stack = []

    # This function allows config fields to be made aware of the
    # owner instance's names. It's called from the `commit_owner_names_across_tree`
    # Decorator. Its called once the config instance is completely ready and
    # it wil not have any further runtime instance modifications done to it.
    # The core intent is to ensure that the full config lineage tree is captured and
    # we have a full trace of where the config is coming from so that we can showcase it
    # to users when they make configurational errors. It also allows us to reference those
    # config values in the error messages across different types of errors.
    def _set_owner_name(self, owner_name: str):
        self._qual_name_stack.append(owner_name)

    def fully_qualified_name(self):
        return ".".join(self._qual_name_stack + [self.name])

    def __set_name__(self, owner, name):
        self.name = name

    def __get__(self, instance, owner):
        if instance is None:
            return self
        # DEFAULTS need to be explicilty set to ensure that
        # only explicitly set values are return on get
        return instance.__dict__.get(self.name)

    def __set__(self, instance, value):
        if self.parsing_fn:
            value = self.parsing_fn(value)

        # TODO: handle this exception at top level if necessary.
        if value is not None and self.strict_types and self.field_type is not None:
            if not isinstance(value, self.field_type):
                raise ValueError(
                    f"Value {value} is not of type {self.field_type} for the field {self.name}"
                )

        instance.__dict__[self.name] = value

    def __str__(self) -> str:
        type_name = (
            getattr(self.field_type, "__name__", "typing.Any")
            if self.field_type
            else "typing.Any"
        )
        return f"<ConfigField name='{self.name}' type={type_name} default={self.default!r}>"


# Add this decorator function before the ConfigMeta class
# One of the core utilities of the ConfigMeta class
# is that we can track the tree of elements in the Config
# class that allow us to make those visible at runtime when
# the user has some configurational error. it also allows us to
# Figure out what the user is trying to extactly configure and where
# that configuration is coming from.
# Hence this decorator is set on what ever configMeta class based function
# so that when it gets called, the full call tree is properly set.
def commit_owner_names_across_tree(func):
    """
    Decorator that commits owner names across the configuration tree before executing the decorated function.

    This decorator ensures that all ConfigField instances in the configuration tree are aware of their
    fully qualified names by traversing the tree and calling _set_owner_name on each field.
    """

    def wrapper(self, *args, **kwargs):
        def _commit_owner_names_recursive(instance, field_name_stack=None):
            if field_name_stack is None:
                field_name_stack = []

            if not ConfigMeta.is_instance(instance):
                return

            fields = instance._fields  # type: ignore
            # fields is a dictionary of field_name: ConfigField
            for field_name, field_info in fields.items():
                if ConfigMeta.is_instance(field_info.field_type):
                    # extract the actual instance of the ConfigMeta class
                    _instance = instance.__dict__[field_name]
                    # The instance should hold the _commit_owner_names_across_tree
                    _commit_owner_names_recursive(
                        _instance, field_name_stack + [field_name]
                    )
                else:
                    if len(field_name_stack) > 0:
                        for x in field_name_stack:
                            field_info._set_owner_name(x)  # type: ignore

        # Commit owner names before executing the original function
        _commit_owner_names_recursive(self)

        # Execute the original function
        return func(self, *args, **kwargs)

    return wrapper


class ConfigMeta(type):
    """Metaclass implementing the configuration system's class transformation layer.

    This metaclass exists to solve the fundamental problem of creating a declarative configuration
    system that can automatically generate runtime behavior from field definitions. Without a
    metaclass, each configuration class would need to manually implement field discovery,
    validation, CLI integration, and nested object handling, leading to boilerplate code and
    inconsistent behavior across the system.

    Technical Implementation:

    During class creation (__new__), this metaclass intercepts the class namespace and performs
    several critical transformations:

    1. Field Discovery: Scans the class namespace for ConfigField instances and extracts their
       metadata into a `_fields` registry. This registry becomes the source of truth for all
       runtime operations including validation, CLI generation, and serialization.

    2. Method Injection: Adds the `_get_field` method to enable programmatic access to field
       metadata. This method is used throughout the system by validation functions, CLI
       generators, and configuration mergers.

    3. __init__ Override: Replaces the class's __init__ method with a standardized version that
       handles three critical initialization phases:
       - Field initialization to None (explicit defaulting happens later via apply_defaults)
       - Nested config object instantiation for ConfigMeta-based field types
       - Keyword argument processing for programmatic configuration

    System Integration and Lifecycle:

    The metaclass integrates with the broader configuration system through several key interfaces:

    - populate_config_recursive: Uses the _fields registry to map external data sources
      (CLI options, config files) to object attributes
    - apply_defaults: Traverses the _fields registry to apply default values after population
    - validate_config_meta: Uses field metadata to execute validation functions
    - merge_field_values: Consults field behavior settings to determine merge strategies
    - config_meta_to_dict: Converts instances back to dictionaries for serialization

    Lifecycle Phases:

    1. Class Definition: Metaclass transforms the class, creating _fields registry
    2. Instance Creation: Auto-generated __init__ initializes fields and nested objects
    3. Population: External systems use _fields to populate from CLI/config files
    4. Validation: Field metadata drives validation and required field checking
    5. Default Application: Fields with None values receive their defaults
    6. Runtime Usage: Descriptor protocol provides controlled field access

    Why a Metaclass:

    The alternatives to a metaclass would be:
    - Manual field registration in each class (error-prone, inconsistent)
    - Inheritance-based approach (doesn't solve the field discovery problem)
    - Decorator-based approach (requires manual application, less automatic)
    - Runtime introspection (performance overhead, less reliable)

    The metaclass provides automatic, consistent behavior while maintaining the declarative
    syntax that makes configuration classes readable and maintainable.

    Usage Pattern:
    ```python
    class MyConfig(metaclass=ConfigMeta):
        name = ConfigField(field_type=str, required=True)
        port = ConfigField(field_type=int, default=8080)
        resources = ConfigField(field_type=ResourceConfig)
    ```
    """

    @staticmethod
    def is_instance(value) -> bool:
        return hasattr(value, "_fields")

    def __new__(mcs, name, bases, namespace):
        # Collect field metadata
        fields = {}
        for key, value in namespace.items():
            if isinstance(value, ConfigField):
                fields[key] = value

        # Store fields metadata on the class
        namespace["_fields"] = fields

        # Inject a function to get configField from a field name
        def get_field(cls, field_name: str) -> ConfigField:
            return fields[field_name]

        namespace["_get_field"] = get_field

        # Auto-generate __init__ method;
        # Override it for all classes.
        def __init__(self, **kwargs):
            # Initialize all fields with Nones or other values
            # We initiaze with None because defaulting should be a
            # constant behavior
            for field_name, field_info in fields.items():
                default_value = None

                # Handle nested config objects
                if ConfigMeta.is_instance(field_info.field_type):
                    # Create nested config instance with defaults
                    default_value = field_info.field_type()

                # Set from kwargs or use default
                if field_name in kwargs:
                    setattr(self, field_name, kwargs[field_name])
                else:
                    setattr(self, field_name, default_value)

        return super().__new__(mcs, name, bases, namespace)


def apply_defaults(config) -> None:
    """
    Apply default values to any fields that are still None.

    Args:
        config: instance of a ConfigMeta object
    """
    for field_name, field_info in config._fields.items():
        current_value = getattr(config, field_name, None)

        if current_value is None:
            # The nested configs will never be set to None
            # Since we always override the init function.
            # The init function will always instantiate the
            # sub-objects under the class
            # Set default value for regular fields
            setattr(config, field_name, field_info.default)
        elif ConfigMeta.is_instance(field_info.field_type) and ConfigMeta.is_instance(
            current_value
        ):

            # Apply defaults to nested config (to any sub values that might need it)
            apply_defaults(current_value)
            # also apply defaults to the current value if a defaults callable is provided.
            # Certain top level config fields might require default setting based on the
            # what the current value in the fields is set.
            if field_info.default:
                field_info.default(current_value)


class ConfigValidationFailedException(Exception):
    def __init__(
        self,
        field_name: str,
        field_info: ConfigField,
        current_value,
        message: Optional[str] = None,
    ):
        self.field_name = field_name
        self.field_info = field_info
        self.current_value = current_value
        self.message = (
            f"Validation failed for field {field_name} with value {current_value}"
        )
        if message is not None:
            self.message = message

        suffix = "\n\tThis configuration is set via the the following interfaces:\n\n"
        suffix += "\t\t1. Config file: `%s`\n" % field_info.fully_qualified_name()
        suffix += (
            "\t\t2. Programatic API (Python): `%s`\n"
            % field_info.fully_qualified_name()
        )
        if field_info.cli_meta:
            suffix += "\t\t3. CLI: `%s`\n" % field_info.cli_meta.cli_option_str

        self.message += suffix

        super().__init__(self.message)


class RequiredFieldMissingException(ConfigValidationFailedException):
    pass


class MergingNotAllowedFieldsException(ConfigValidationFailedException):
    def __init__(
        self,
        field_name: str,
        field_info: ConfigField,
        current_value: Any,
        override_value: Any,
    ):
        super().__init__(
            field_name=field_name,
            field_info=field_info,
            current_value=current_value,
            message=f"Merging not allowed for field {field_name} with value {current_value} and override value {override_value}",
        )
        self.override_value = override_value


def validate_required_fields(config_instance):
    for field_name, field_info in config_instance._fields.items():
        if field_info.required:
            current_value = getattr(config_instance, field_name, None)
            if current_value is None:
                raise RequiredFieldMissingException(
                    field_name, field_info, current_value
                )
        if ConfigMeta.is_instance(field_info.field_type) and ConfigMeta.is_instance(
            current_value
        ):
            validate_required_fields(current_value)
            # TODO: Fix the exception handling over here.


def validate_config_meta(config_instance):
    for field_name, field_info in config_instance._fields.items():
        current_value = getattr(config_instance, field_name, None)

        if ConfigMeta.is_instance(field_info.field_type) and ConfigMeta.is_instance(
            current_value
        ):
            validate_config_meta(current_value)

        if field_info.validation_fn:
            if not field_info.validation_fn(current_value):
                raise ConfigValidationFailedException(
                    field_name, field_info, current_value
                )


def config_meta_to_dict(config_instance) -> Optional[Dict[str, Any]]:
    """Convert a configuration instance to a nested dictionary.

    Recursively converts ConfigMeta-based configuration instances to dictionaries,
    handling nested config objects and preserving the structure.

    Args:
        config_instance: Instance of a ConfigMeta-based configuration class

    Returns:
        Nested dictionary representation of the configuration

    Examples:
        # Convert a config instance to dict

        config_dict = to_dict(config)

        # Result will be:
        # {
        #     "name": "myapp",
        #     "port": 8000,
        #     "resources": {
        #         "cpu": "500m",
        #         "memory": "1Gi",
        #         "gpu": None,
        #         "disk": "20Gi"
        #     },
        #     "auth": None,
        #     ...
        # }
    """
    if config_instance is None:
        return None

    # Check if this is a ConfigMeta-based class
    if not ConfigMeta.is_instance(config_instance):
        # If it's not a config object, return as-is
        return config_instance

    result = {}

    # Iterate through all fields defined in the class
    for field_name, field_info in config_instance._fields.items():
        # Get the current value
        value = getattr(config_instance, field_name, None)

        # Handle nested config objects recursively
        if value is not None and ConfigMeta.is_instance(value):
            # It's a nested config object
            result[field_name] = config_meta_to_dict(value)
        elif isinstance(value, list) and value:
            # Handle lists that might contain config objects
            result[field_name] = [
                config_meta_to_dict(item) if ConfigMeta.is_instance(item) else item
                for item in value
            ]
        elif isinstance(value, dict) and value:
            # Handle dictionaries that might contain config objects
            result[field_name] = {
                k: config_meta_to_dict(v) if ConfigMeta.is_instance(v) else v
                for k, v in value.items()
            }
        else:
            # Primitive type or None
            result[field_name] = value

    return result


def merge_field_values(
    base_value: Any, override_value: Any, field_info, behavior: str
) -> Any:
    """
    Merge individual field values based on behavior.

    Args:
        base_value: Value from base config
        override_value: Value from override config
        field_info: Field metadata
        behavior: FieldBehavior for this field

    Returns:
        Merged value
    """
    # Handle NOT_ALLOWED behavior
    if behavior == FieldBehavior.NOT_ALLOWED:
        if base_value is not None and override_value is not None:
            raise MergingNotAllowedFieldsException(
                field_name=field_info.name,
                field_info=field_info,
                current_value=base_value,
                override_value=override_value,
            )
        if base_value is None:
            return override_value
        return base_value

    # Handle UNION behavior (default)
    if behavior == FieldBehavior.UNION:
        # If override is None, use base value
        if override_value is None:
            return (
                base_value if base_value is not None else None
            )  # We will not set defaults!

        # If base is None, use override value
        if base_value is None:
            return override_value

        # Handle nested config objects
        if ConfigMeta.is_instance(field_info.field_type):
            if isinstance(base_value, field_info.field_type) and isinstance(
                override_value, field_info.field_type
            ):
                # Merge nested configs recursively
                merged_nested = field_info.field_type()
                for (
                    nested_field_name,
                    nested_field_info,
                ) in field_info.field_type._fields.items():
                    nested_base = getattr(base_value, nested_field_name, None)
                    nested_override = getattr(override_value, nested_field_name, None)
                    nested_behavior = getattr(
                        nested_field_info, "behavior", FieldBehavior.UNION
                    )

                    merged_nested_value = merge_field_values(
                        nested_base, nested_override, nested_field_info, nested_behavior
                    )
                    setattr(merged_nested, nested_field_name, merged_nested_value)

                return merged_nested
            else:
                # One is not a config object, use override
                return override_value

        # Handle lists (union behavior merges lists)
        if isinstance(base_value, list) and isinstance(override_value, list):
            # Merge lists by extending
            merged_list = base_value.copy()
            merged_list.extend(override_value)
            return merged_list

        # Handle dicts (union behavior merges dicts)
        if isinstance(base_value, dict) and isinstance(override_value, dict):
            merged_dict = base_value.copy()
            merged_dict.update(override_value)
            return merged_dict

        # For other types, override takes precedence
        return override_value

    # Default: override takes precedence
    return (
        override_value
        if override_value is not None
        else (base_value if base_value is not None else None)
    )


class JsonFriendlyKeyValuePair(click.ParamType):  # type: ignore
    name = "KV-PAIR"  # type: ignore

    def convert(self, value, param, ctx):
        # Parse a string of the form KEY=VALUE into a dict {KEY: VALUE}
        if len(value.split("=", 1)) != 2:
            self.fail(
                f"Invalid format for {value}. Expected format: KEY=VALUE", param, ctx
            )

        key, _value = value.split("=", 1)
        try:
            return {key: json.loads(_value)}
        except json.JSONDecodeError:
            return {key: _value}
        except Exception as e:
            self.fail(f"Invalid value for {value}. Error: {e}", param, ctx)

    def __str__(self):
        return repr(self)

    def __repr__(self):
        return "KV-PAIR"


class CommaSeparatedList(click.ParamType):  # type: ignore
    name = "COMMA-SEPARATED-LIST"  # type: ignore

    def convert(self, value, param, ctx):
        if isinstance(value, list):
            return value
        if isinstance(value, str):
            return [item.strip() for item in value.split(",") if item.strip()]
        return value

    def __str__(self):
        return repr(self)

    def __repr__(self):
        return "COMMA-SEPARATED-LIST"


class PureStringKVPair(click.ParamType):  # type: ignore
    """Click type for key-value pairs (KEY=VALUE)."""

    name = "key=value"

    def convert(self, value, param, ctx):
        if isinstance(value, dict):
            return value
        try:
            key, val = value.split("=", 1)
            return {key: val}
        except ValueError:
            self.fail(f"'{value}' is not a valid key=value pair", param, ctx)


PureStringKVPairType = PureStringKVPair()
CommaSeparatedListType = CommaSeparatedList()
JsonFriendlyKeyValuePairType = JsonFriendlyKeyValuePair()


def populate_config_recursive(
    config_instance,
    config_class,
    source_data,
    get_source_key_fn,
    get_source_value_fn,
):
    """
    Recursively populate a config instance from source data.

    Args:
        config_instance: Config object to populate
        config_class: Class of the config object
        source_data: Source data (dict, CLI options, etc.)
        get_source_key_fn: Function to get the source key for a field
        get_source_value_fn: Function to get the value from source for a key
    """

    for field_name, field_info in config_class._fields.items():
        # When we populate the ConfigMeta based objects, we want to do the following:
        # If we find some key associated to the object inside the source data, then we populate the object
        # with it. If that key corresponds to a nested config meta object then we just recusively pass down the
        # value of the key from source data and populate the nested object other wise just end up setting the object
        source_key = get_source_key_fn(field_name, field_info)
        if source_key and source_key in source_data:
            value = get_source_value_fn(source_data, source_key)
            if value is not None:
                # Handle nested config objects (for dict sources with nested data)
                if ConfigMeta.is_instance(field_info.field_type) and isinstance(
                    value, dict
                ):
                    nested_config = field_info.field_type()
                    populate_config_recursive(
                        nested_config,
                        field_info.field_type,
                        value,  # For dict, use the nested dict as source
                        get_source_key_fn,
                        get_source_value_fn,
                    )
                    setattr(config_instance, field_name, nested_config)
                else:
                    # Direct value assignment for regular fields
                    setattr(config_instance, field_name, value)
        elif ConfigMeta.is_instance(field_info.field_type):
            # It might be possible that the source key that respresents a subfield is
            # is present at the root level but there is no field pertainig to the ConfigMeta
            # itself. So always recurisvely check the subtree and no matter what keep instantiating
            # any nested config objects.
            _nested_config = field_info.field_type()
            populate_config_recursive(
                _nested_config,
                field_info.field_type,
                source_data,
                get_source_key_fn,
                get_source_value_fn,
            )
            setattr(config_instance, field_name, _nested_config)
        else:
            pass
