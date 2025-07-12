######################################################################################################
#                                 Auto-generated Metaflow stub file                                  #
# MF version: 2.15.21.1+obcheckpoint(0.2.4);ob(v1)                                                   #
# Generated on 2025-07-11T23:29:18.598830                                                            #
######################################################################################################

from __future__ import annotations

import typing
import metaflow
if typing.TYPE_CHECKING:
    import typing
    import metaflow.mf_extensions.outerbounds.plugins.apps.core.config.config_utils
    import metaflow._vendor.click.types

from ......._vendor import click as click

class FieldBehavior(object, metaclass=type):
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
    ...

class CLIOption(object, metaclass=type):
    """
    Metadata container for automatic CLI option generation from configuration fields.
    
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
    def __init__(self, name: str, cli_option_str: str, help: typing.Optional[str] = None, short: typing.Optional[str] = None, multiple: bool = False, is_flag: bool = False, choices: typing.Optional[typing.List[str]] = None, default: typing.Any = None, hidden: bool = False, click_type: typing.Optional[typing.Any] = None):
        ...
    ...

class ConfigField(object, metaclass=type):
    """
    Descriptor for configuration fields with comprehensive metadata and behavior control.
    
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
    def __init__(self, default: typing.Union[typing.Any, typing.Callable[["ConfigField"], typing.Any]] = None, cli_meta = None, field_type = None, required = False, help = None, behavior: str = 'union', example = None, strict_types = True, validation_fn: typing.Optional[typing.Callable] = None, is_experimental = False, parsing_fn: typing.Optional[typing.Callable] = None):
        ...
    def fully_qualified_name(self):
        ...
    def __set_name__(self, owner, name):
        ...
    def __get__(self, instance, owner):
        ...
    def __set__(self, instance, value):
        ...
    def __str__(self) -> str:
        ...
    ...

def commit_owner_names_across_tree(func):
    """
    Decorator that commits owner names across the configuration tree before executing the decorated function.
    
    This decorator ensures that all ConfigField instances in the configuration tree are aware of their
    fully qualified names by traversing the tree and calling _set_owner_name on each field.
    """
    ...

class ConfigMeta(type, metaclass=type):
    """
    Metaclass implementing the configuration system's class transformation layer.
    
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
        ...
    @staticmethod
    def __new__(mcs, name, bases, namespace):
        ...
    ...

def apply_defaults(config):
    """
    Apply default values to any fields that are still None.
    
    Args:
        config: instance of a ConfigMeta object
    """
    ...

class ConfigValidationFailedException(Exception, metaclass=type):
    def __init__(self, field_name: str, field_info: ConfigField, current_value, message: typing.Optional[str] = None):
        ...
    ...

class RequiredFieldMissingException(ConfigValidationFailedException, metaclass=type):
    ...

class MergingNotAllowedFieldsException(ConfigValidationFailedException, metaclass=type):
    def __init__(self, field_name: str, field_info: ConfigField, current_value: typing.Any, override_value: typing.Any):
        ...
    ...

def validate_required_fields(config_instance):
    ...

def validate_config_meta(config_instance):
    ...

def config_meta_to_dict(config_instance) -> typing.Optional[typing.Dict[str, typing.Any]]:
    """
    Convert a configuration instance to a nested dictionary.
    
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
    ...

def merge_field_values(base_value: typing.Any, override_value: typing.Any, field_info, behavior: str) -> typing.Any:
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
    ...

class JsonFriendlyKeyValuePair(metaflow._vendor.click.types.ParamType, metaclass=type):
    def convert(self, value, param, ctx):
        ...
    def __str__(self):
        ...
    def __repr__(self):
        ...
    ...

class CommaSeparatedList(metaflow._vendor.click.types.ParamType, metaclass=type):
    def convert(self, value, param, ctx):
        ...
    def __str__(self):
        ...
    def __repr__(self):
        ...
    ...

class PureStringKVPair(metaflow._vendor.click.types.ParamType, metaclass=type):
    """
    Click type for key-value pairs (KEY=VALUE).
    """
    def convert(self, value, param, ctx):
        ...
    ...

PureStringKVPairType: PureStringKVPair

CommaSeparatedListType: CommaSeparatedList

JsonFriendlyKeyValuePairType: JsonFriendlyKeyValuePair

def populate_config_recursive(config_instance, config_class, source_data, get_source_key_fn, get_source_value_fn):
    """
    Recursively populate a config instance from source data.
    
    Args:
        config_instance: Config object to populate
        config_class: Class of the config object
        source_data: Source data (dict, CLI options, etc.)
        get_source_key_fn: Function to get the source key for a field
        get_source_value_fn: Function to get the value from source for a key
    """
    ...

