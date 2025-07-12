"""
Unified Configuration System for Outerbounds Apps

This module provides a type-safe, declarative configuration system that serves as the
single source of truth for app configuration. It automatically generates CLI options,
handles config file parsing, and manages field merging behavior.

No external dependencies required - uses only Python standard library.
"""


import os
import json
from typing import Any, Dict, List, Optional, Union, Type
import re

from .config_utils import (
    ConfigField,
    ConfigMeta,
    JsonFriendlyKeyValuePairType,
    PureStringKVPairType,
    CommaSeparatedListType,
    FieldBehavior,
    CLIOption,
    config_meta_to_dict,
    merge_field_values,
    apply_defaults,
    populate_config_recursive,
    validate_config_meta,
    validate_required_fields,
    ConfigValidationFailedException,
    commit_owner_names_across_tree,
)


class AuthType:
    BROWSER = "Browser"
    API = "API"

    @classmethod
    def choices(cls):
        return [cls.BROWSER, cls.API]


class UnitParser:
    UNIT_FREE_REGEX = r"^\d+$"

    metrics = {
        "memory": {
            "default_unit": "Mi",
            "requires_unit": True,  # if a Unit free value is provided then we will add the default unit to it.
            # Regex to match values with units (e.g., "512Mi", "4Gi", "1024Ki")
            "correct_unit_regex": r"^\d+(\.\d+)?(Ki|Mi|Gi|Ti|Pi|Ei)$",
        },
        "cpu": {
            "default_unit": None,
            "requires_unit": False,  # if a Unit free value is provided then we will not add the default unit to it.
            # Accepts values like 400m, 4, 0.4, 1000n, etc.
            # Regex to match values with units (e.g., "400m", "1000n", "2", "0.5")
            "correct_unit_regex": r"^(\d+(\.\d+)?(m|n)?|\d+(\.\d+)?)$",
        },
        "disk": {
            "default_unit": "Mi",
            "requires_unit": True,  # if a Unit free value is provided then we will add the default unit to it.
            # Regex to match values with units (e.g., "100Mi", "1Gi", "500Ki")
            "correct_unit_regex": r"^\d+(\.\d+)?(Ki|Mi|Gi|Ti|Pi|Ei)$",
        },
        "gpu": {
            "default_unit": None,
            "requires_unit": False,
            # Regex to match values with units (usually just integer count, e.g., "1", "2")
            "correct_unit_regex": r"^\d+$",
        },
    }

    def __init__(self, metric_name: str):
        self.metric_name = metric_name

    def validate(self, value: str):
        if re.match(self.metrics[self.metric_name]["correct_unit_regex"], value):
            return True
        return False

    def process(self, value: str):
        value = str(value)
        if self.metrics[self.metric_name]["requires_unit"]:
            if re.match(self.UNIT_FREE_REGEX, value):
                # This means the value is unit free and we need to add the default unit to it.
                value = "%s%s" % (
                    value.strip(),
                    self.metrics[self.metric_name]["default_unit"],
                )
                return value

        return value

    def parse(self, value: Union[str, None]):
        if value is None:
            return None
        return self.process(value)

    @staticmethod
    def validation_wrapper_fn(
        metric_name: str,
    ):
        def validation_fn(value: str):
            if value is None:
                return True
            field_info = ResourceConfig._get_field(ResourceConfig, metric_name)  # type: ignore
            parser = UnitParser(metric_name)
            validation = parser.validate(value)
            if not validation:
                raise ConfigValidationFailedException(
                    field_name=metric_name,
                    field_info=field_info,
                    current_value=value,
                    message=f"Invalid value for `{metric_name}`. Must be of the format {parser.metrics[metric_name]['correct_unit_regex']}.",
                )
            return validation

        return validation_fn


class BasicValidations:
    def __init__(self, config_meta_class, field_name):
        self.config_meta_class = config_meta_class
        self.field_name = field_name

    def _get_field(self):
        return self.config_meta_class._get_field(self.config_meta_class, self.field_name)  # type: ignore

    def enum_validation(self, enums: List[str], current_value):
        if current_value not in enums:
            raise ConfigValidationFailedException(
                field_name=self.field_name,
                field_info=self._get_field(),
                current_value=current_value,
                message=f"Configuration field {self.field_name} has invalid value {current_value}. Value must be one of: {'/'.join(enums)}",
            )
        return True

    def range_validation(self, min_value, max_value, current_value):
        if current_value < min_value or current_value > max_value:
            raise ConfigValidationFailedException(
                field_name=self.field_name,
                field_info=self._get_field(),
                current_value=current_value,
                message=f"Configuration field {self.field_name} has invalid value {current_value}. Value must be between {min_value} and {max_value}",
            )
        return True

    def length_validation(self, max_length, current_value):
        if len(current_value) > max_length:
            raise ConfigValidationFailedException(
                field_name=self.field_name,
                field_info=self._get_field(),
                current_value=current_value,
                message=f"Configuration field {self.field_name} has invalid value {current_value}. Value must be less than {max_length}",
            )
        return True

    def regex_validation(self, regex, current_value):
        if not re.match(regex, current_value):
            raise ConfigValidationFailedException(
                field_name=self.field_name,
                field_info=self._get_field(),
                current_value=current_value,
                message=f"Configuration field {self.field_name} has invalid value {current_value}. Value must match regex {regex}",
            )
        return True


class ResourceConfig(metaclass=ConfigMeta):
    """Resource configuration for the app."""

    # TODO: Add Unit Validation/Parsing Support for the Fields.
    cpu = ConfigField(
        default="1",
        cli_meta=CLIOption(
            name="cpu",
            cli_option_str="--cpu",
            help="CPU resource request and limit.",
        ),
        field_type=str,
        example="500m",
        validation_fn=UnitParser.validation_wrapper_fn("cpu"),
        parsing_fn=UnitParser("cpu").parse,
    )
    memory = ConfigField(
        default="4Gi",
        cli_meta=CLIOption(
            name="memory",
            cli_option_str="--memory",
            help="Memory resource request and limit.",
        ),
        field_type=str,
        example="512Mi",
        validation_fn=UnitParser.validation_wrapper_fn("memory"),
        parsing_fn=UnitParser("memory").parse,
    )
    gpu = ConfigField(
        cli_meta=CLIOption(
            name="gpu",
            cli_option_str="--gpu",
            help="GPU resource request and limit.",
        ),
        field_type=str,
        example="1",
        validation_fn=UnitParser.validation_wrapper_fn("gpu"),
        parsing_fn=UnitParser("gpu").parse,
    )
    disk = ConfigField(
        default="20Gi",
        cli_meta=CLIOption(
            name="disk",
            cli_option_str="--disk",
            help="Storage resource request and limit.",
        ),
        field_type=str,
        example="1Gi",
        validation_fn=UnitParser.validation_wrapper_fn("disk"),
        parsing_fn=UnitParser("disk").parse,
    )


class HealthCheckConfig(metaclass=ConfigMeta):
    """Health check configuration."""

    enabled = ConfigField(
        default=False,
        cli_meta=CLIOption(
            name="health_check_enabled",
            cli_option_str="--health-check-enabled",
            help="Whether to enable health checks.",
            is_flag=True,
        ),
        field_type=bool,
        example=True,
    )
    path = ConfigField(
        cli_meta=CLIOption(
            name="health_check_path",
            cli_option_str="--health-check-path",
            help="The path for health checks.",
        ),
        field_type=str,
        example="/health",
    )
    initial_delay_seconds = ConfigField(
        cli_meta=CLIOption(
            name="health_check_initial_delay",
            cli_option_str="--health-check-initial-delay",
            help="Number of seconds to wait before performing the first health check.",
        ),
        field_type=int,
        example=10,
    )
    period_seconds = ConfigField(
        cli_meta=CLIOption(
            name="health_check_period",
            cli_option_str="--health-check-period",
            help="How often to perform the health check.",
        ),
        field_type=int,
        example=30,
    )


class AuthConfig(metaclass=ConfigMeta):
    """Authentication configuration."""

    type = ConfigField(
        default=AuthType.BROWSER,
        cli_meta=CLIOption(
            name="auth_type",
            cli_option_str="--auth-type",
            help="The type of authentication to use for the app.",
            choices=AuthType.choices(),
        ),
        field_type=str,
        example="Browser",
    )
    public = ConfigField(
        default=True,
        cli_meta=CLIOption(
            name="auth_public",
            cli_option_str="--public-access/--private-access",
            help="Whether the app is public or not.",
            is_flag=True,
        ),
        field_type=bool,
        example=True,
    )

    @staticmethod
    def validate(auth_config: "AuthConfig"):
        if auth_config.type is None:
            return True
        return BasicValidations(AuthConfig, "type").enum_validation(
            AuthType.choices(), auth_config.type
        )


class ReplicaConfig(metaclass=ConfigMeta):
    """Replica configuration."""

    fixed = ConfigField(
        cli_meta=CLIOption(
            name="fixed_replicas",
            cli_option_str="--fixed-replicas",
            help="The fixed number of replicas to deploy the app with. If min and max are set, this will raise an error.",
        ),
        field_type=int,
        example=1,
    )

    min = ConfigField(
        cli_meta=CLIOption(
            name="min_replicas",
            cli_option_str="--min-replicas",
            help="The minimum number of replicas to deploy the app with.",
        ),
        field_type=int,
        example=1,
    )
    max = ConfigField(
        cli_meta=CLIOption(
            name="max_replicas",
            cli_option_str="--max-replicas",
            help="The maximum number of replicas to deploy the app with.",
        ),
        field_type=int,
        example=10,
    )

    @staticmethod
    def defaults(replica_config: "ReplicaConfig"):
        if all(
            [
                replica_config.min is None,
                replica_config.max is None,
                replica_config.fixed is None,
            ]
        ):
            # if nothing is set then set
            replica_config.fixed = 1
        elif replica_config.min is not None and replica_config.max is None:
            replica_config.max = replica_config.min
        return

    @staticmethod
    def validate(replica_config: "ReplicaConfig"):
        both_min_max_set = (
            replica_config.min is not None and replica_config.max is not None
        )
        fixed_set = replica_config.fixed is not None
        max_is_set = replica_config.max is not None
        min_is_set = replica_config.min is not None
        any_min_max_set = (
            replica_config.min is not None or replica_config.max is not None
        )

        def _greater_than_equals_zero(x):
            return x is not None and x >= 0

        if both_min_max_set and replica_config.min > replica_config.max:  # type: ignore
            raise ConfigValidationFailedException(
                field_name="min",
                field_info=replica_config._get_field("min"),  # type: ignore
                current_value=replica_config.min,
                message="Min replicas cannot be greater than max replicas",
            )
        if fixed_set and any_min_max_set:
            raise ConfigValidationFailedException(
                field_name="fixed",
                field_info=replica_config._get_field("fixed"),  # type: ignore
                current_value=replica_config.fixed,
                message="Fixed replicas cannot be set when min or max replicas are set",
            )

        if max_is_set and not min_is_set:
            raise ConfigValidationFailedException(
                field_name="min",
                field_info=replica_config._get_field("min"),  # type: ignore
                current_value=replica_config.min,
                message="If max replicas is set then min replicas must be set too.",
            )

        if fixed_set and replica_config.fixed < 0:  # type: ignore
            raise ConfigValidationFailedException(
                field_name="fixed",
                field_info=replica_config._get_field("fixed"),  # type: ignore
                current_value=replica_config.fixed,
                message="Fixed replicas cannot be less than 0",
            )

        if min_is_set and not _greater_than_equals_zero(replica_config.min):
            raise ConfigValidationFailedException(
                field_name="min",
                field_info=replica_config._get_field("min"),  # type: ignore
                current_value=replica_config.min,
                message="Min replicas cannot be less than 0",
            )

        if max_is_set and not _greater_than_equals_zero(replica_config.max):
            raise ConfigValidationFailedException(
                field_name="max",
                field_info=replica_config._get_field("max"),  # type: ignore
                current_value=replica_config.max,
                message="Max replicas cannot be less than 0",
            )
        return True


def more_than_n_not_none(n, *args):
    return sum(1 for arg in args if arg is not None) > n


class DependencyConfig(metaclass=ConfigMeta):
    """Dependency configuration."""

    from_requirements_file = ConfigField(
        cli_meta=CLIOption(
            name="dep_from_requirements",
            cli_option_str="--dep-from-requirements",
            help="The path to the requirements.txt file to attach to the app.",
        ),
        field_type=str,
        behavior=FieldBehavior.NOT_ALLOWED,
        example="requirements.txt",
    )
    from_pyproject_toml = ConfigField(
        cli_meta=CLIOption(
            name="dep_from_pyproject",
            cli_option_str="--dep-from-pyproject",
            help="The path to the pyproject.toml file to attach to the app.",
        ),
        field_type=str,
        behavior=FieldBehavior.NOT_ALLOWED,
        example="pyproject.toml",
    )
    python = ConfigField(
        cli_meta=CLIOption(
            name="python",
            cli_option_str="--python",
            help="The Python version to use for the app.",
        ),
        field_type=str,
        behavior=FieldBehavior.NOT_ALLOWED,
        example="3.10",
    )
    pypi = ConfigField(
        cli_meta=CLIOption(
            name="pypi",  # TODO: Can set CLI meta to None
            cli_option_str="--pypi",
            help="A dictionary of pypi dependencies to attach to the app. The key is the package name and the value is the version.",
            hidden=True,  # Complex structure, better handled in config file
        ),
        field_type=dict,
        behavior=FieldBehavior.NOT_ALLOWED,
        example={"numpy": "1.23.0", "pandas": ""},
    )
    conda = ConfigField(
        cli_meta=CLIOption(  # TODO: Can set CLI meta to None
            name="conda",
            cli_option_str="--conda",
            help="A dictionary of conda dependencies to attach to the app. The key is the package name and the value is the version.",
            hidden=True,  # Complex structure, better handled in config file
        ),
        field_type=dict,
        behavior=FieldBehavior.NOT_ALLOWED,
        example={"numpy": "1.23.0", "pandas": ""},
    )

    @staticmethod
    def validate(dependency_config: "DependencyConfig"):
        # You can either have from_requirements_file or from_pyproject_toml or python with pypi or conda
        # but not more than one of them.
        if more_than_n_not_none(
            1,
            dependency_config.from_requirements_file,
            dependency_config.from_pyproject_toml,
        ):
            raise ConfigValidationFailedException(
                field_name="from_requirements_file",
                field_info=dependency_config._get_field("from_requirements_file"),  # type: ignore
                current_value=dependency_config.from_requirements_file,
                message="Cannot set from_requirements_file and from_pyproject_toml at the same time",
            )
        if any([dependency_config.pypi, dependency_config.conda]) and any(
            [
                dependency_config.from_requirements_file,
                dependency_config.from_pyproject_toml,
            ]
        ):
            raise ConfigValidationFailedException(
                field_name="pypi" if dependency_config.pypi else "conda",
                field_info=dependency_config._get_field(  # type: ignore
                    "pypi" if dependency_config.pypi else "conda"
                ),
                current_value=dependency_config.pypi or dependency_config.conda,
                message="Cannot set pypi or conda when from_requirements_file or from_pyproject_toml is set",
            )
        return True


class PackageConfig(metaclass=ConfigMeta):
    """Package configuration."""

    src_path = ConfigField(
        cli_meta=CLIOption(
            name="package_src_path",
            cli_option_str="--package-src-path",
            help="The path to the source code to deploy with the App.",
        ),
        field_type=str,
        example="./",
    )
    suffixes = ConfigField(
        cli_meta=CLIOption(
            name="package_suffixes",
            cli_option_str="--package-suffixes",
            help="A list of suffixes to add to the source code to deploy with the App.",
        ),
        field_type=list,
        example=[".py", ".ipynb"],
    )


class BasicAppValidations:
    @staticmethod
    def name(name):
        if name is None:
            return True
        regex = r"^[a-z0-9-]+$"  # Only allow lowercase letters, numbers, and hyphens
        validator = BasicValidations(CoreConfig, "name")
        return validator.length_validation(20, name) and validator.regex_validation(
            regex, name
        )

    @staticmethod
    def port(port):
        if port is None:
            return True
        return BasicValidations(CoreConfig, "port").range_validation(1, 65535, port)

    @staticmethod
    def tags(tags):
        if tags is None:
            return True
        if not all(isinstance(tag, dict) and len(tag) == 1 for tag in tags):
            raise ConfigValidationFailedException(
                field_name="tags",
                field_info=CoreConfig._get_field(CoreConfig, "tags"),  # type: ignore
                current_value=tags,
                message="Tags must be a list of dictionaries with one key. Currently they are set to %s "
                % (str(tags)),
            )
        return True

    @staticmethod
    def secrets(secrets):
        if secrets is None:  # If nothing is set we dont care.
            return True

        if not isinstance(secrets, list):
            raise ConfigValidationFailedException(
                field_name="secrets",
                field_info=CoreConfig._get_field(CoreConfig, "secrets"),  # type: ignore
                current_value=secrets,
                message="Secrets must be a list of strings. Currently they are set to %s "
                % (str(secrets)),
            )
        from ..validations import secrets_validator

        try:
            secrets_validator(secrets)
        except Exception as e:
            raise ConfigValidationFailedException(
                field_name="secrets",
                field_info=CoreConfig._get_field(CoreConfig, "secrets"),  # type: ignore
                current_value=secrets,
                message=f"Secrets validation failed, {e}",
            )
        return True

    @staticmethod
    def persistence(persistence):
        if persistence is None:
            return True
        return BasicValidations(CoreConfig, "persistence").enum_validation(
            ["none", "postgres"], persistence
        )


class CoreConfig(metaclass=ConfigMeta):
    """Unified App Configuration - The single source of truth for application configuration.

    CoreConfig is the central configuration class that defines all application settings using the
    ConfigMeta metaclass and ConfigField descriptors. It provides a declarative, type-safe way
    to manage configuration from multiple sources (CLI, config files, environment) with automatic
    validation, merging, and CLI generation.

    Core Features:
    - **Declarative Configuration**: All fields are defined using ConfigField descriptors
    - **Multi-Source Configuration**: Supports CLI options, config files (JSON/YAML), and programmatic setting
    - **Automatic CLI Generation**: CLI options are automatically generated from field metadata
    - **Type Safety**: Built-in type checking and validation for all fields
    - **Hierarchical Structure**: Supports nested configuration objects (resources, auth, dependencies)
    - **Intelligent Merging**: Configurable merging behavior for different field types
    - **Validation Framework**: Comprehensive validation with custom validation functions

    Configuration Lifecycle:
    1. **Definition**: Fields are defined declaratively using ConfigField descriptors
    2. **Instantiation**: Objects are created with all fields initialized to None or nested objects
    3. **Population**: Values are populated from CLI options, config files, or direct assignment
    4. **Merging**: Multiple config sources are merged according to field behavior settings
    5. **Validation**: Field validation functions and required field checks are performed
    6. **Default Application**: Default values are applied to any remaining None fields
    7. **Commit**: Final validation and preparation for use


    Usage Examples:
        Create from CLI options:
        ```python
        config = CoreConfig.from_cli({
            'name': 'myapp',
            'port': 8080,
            'commands': ['python app.py']
        })
        ```

        Create from config file:
        ```python
        config = CoreConfig.from_file('config.yaml')
        ```

        Create from dictionary:
        ```python
        config = CoreConfig.from_dict({
            'name': 'myapp',
            'port': 8080,
            'resources': {
                'cpu': '500m',
                'memory': '1Gi'
            }
        })
        ```

        Merge configurations:
        ```python
        file_config = CoreConfig.from_file('config.yaml')
        cli_config = CoreConfig.from_cli(cli_options)
        final_config = CoreConfig.merge_configs(file_config, cli_config)
        final_config.commit()  # Validate and apply defaults
        ```
    """

    # TODO: We can add Force Upgrade / No Deps flags here too if we need to.
    # Since those can be exposed on the CLI side and the APP state will anyways
    # be expored before being worked upon.

    SCHEMA_DOC = """Schema for defining Outerbounds Apps configuration. This schema is what we will end up using on the CLI/programmatic interface.
How to read this schema:
1. If the a property has `mutation_behavior` set to `union` then it will allow overrides of values at runtime from the CLI.
2. If the property has `mutation_behavior`set to `not_allowed` then either the CLI or the config file value will be used (which ever is not None). If the user supplies something in both then an error will be raised.
3. If a property has `experimental` set to true then a lot its validations may-be skipped and parsing handled somewhere else.
"""

    # Required fields
    name = ConfigField(
        cli_meta=CLIOption(
            name="name",
            cli_option_str="--name",
        ),
        validation_fn=BasicAppValidations.name,
        field_type=str,
        required=True,
        help="The name of the app to deploy.",
        example="myapp",
    )
    port = ConfigField(
        cli_meta=CLIOption(
            name="port",
            cli_option_str="--port",
        ),
        validation_fn=BasicAppValidations.port,
        field_type=int,
        required=True,
        help="Port where the app is hosted. When deployed this will be port on which we will deploy the app.",
        example=8000,
    )

    # Optional basic fields
    description = ConfigField(
        cli_meta=CLIOption(
            name="description",
            cli_option_str="--description",
            help="The description of the app to deploy.",
        ),
        field_type=str,
        example="This is a description of my app.",
    )
    app_type = ConfigField(
        cli_meta=CLIOption(
            name="app_type",
            cli_option_str="--app-type",
            help="The User defined type of app to deploy. Its only used for bookkeeping purposes.",
        ),
        field_type=str,
        example="MyCustomAgent",
    )
    image = ConfigField(
        cli_meta=CLIOption(
            name="image",
            cli_option_str="--image",
            help="The Docker image to deploy with the App.",
        ),
        field_type=str,
        example="python:3.10-slim",
    )

    # List fields
    tags = ConfigField(
        cli_meta=CLIOption(
            name="tags",
            cli_option_str="--tag",
            multiple=True,
            click_type=PureStringKVPairType,
        ),
        field_type=list,
        validation_fn=BasicAppValidations.tags,
        help="The tags of the app to deploy.",
        example=[{"foo": "bar"}, {"x": "y"}],
    )
    secrets = ConfigField(
        cli_meta=CLIOption(
            name="secrets", cli_option_str="--secret", multiple=True, click_type=str
        ),
        field_type=list,
        help="Outerbounds integrations to attach to the app. You can use the value you set in the `@secrets` decorator in your code.",
        example=["hf-token"],
        validation_fn=BasicAppValidations.secrets,
    )
    compute_pools = ConfigField(
        cli_meta=CLIOption(
            name="compute_pools",
            cli_option_str="--compute-pools",
            help="A list of compute pools to deploy the app to.",
            multiple=True,
            click_type=str,
        ),
        field_type=list,
        example=["default", "large"],
    )
    environment = ConfigField(
        cli_meta=CLIOption(
            name="environment",
            cli_option_str="--env",
            multiple=True,
            click_type=JsonFriendlyKeyValuePairType,  # TODO: Fix me.
        ),
        field_type=dict,
        help="Environment variables to deploy with the App.",
        example={
            "DEBUG": True,
            "DATABASE_CONFIG": {"host": "localhost", "port": 5432},
            "ALLOWED_ORIGINS": ["http://localhost:3000", "https://myapp.com"],
        },
    )
    commands = ConfigField(
        cli_meta=None,  # We dont expose commands as an options. We rather expose it like `--` with click.
        field_type=list,
        required=True,  # Either from CLI or from config file.
        help="A list of commands to run the app with.",  # TODO: Fix me: make me configurable via the -- stuff in click.
        example=["python app.py", "python app.py --foo bar"],
        behavior=FieldBehavior.NOT_ALLOWED,
    )

    # Complex nested fields
    resources = ConfigField(
        cli_meta=None,  # No top-level CLI option, only nested fields have CLI options
        field_type=ResourceConfig,
        # TODO : see if we can add a validation func for resources.
        help="Resource configuration for the app.",
    )
    auth = ConfigField(
        cli_meta=None,  # No top-level CLI option, only nested fields have CLI options
        field_type=AuthConfig,
        help="Auth related configurations.",
        validation_fn=AuthConfig.validate,
    )
    replicas = ConfigField(
        cli_meta=None,  # No top-level CLI option, only nested fields have CLI options
        validation_fn=ReplicaConfig.validate,
        field_type=ReplicaConfig,
        default=ReplicaConfig.defaults,
        help="The number of replicas to deploy the app with.",
    )
    dependencies = ConfigField(
        cli_meta=None,  # No top-level CLI option, only nested fields have CLI options
        validation_fn=DependencyConfig.validate,
        field_type=DependencyConfig,
        help="The dependencies to attach to the app. ",
    )
    package = ConfigField(
        cli_meta=None,  # No top-level CLI option, only nested fields have CLI options
        field_type=PackageConfig,
        help="Configurations associated with packaging the app.",
    )

    no_deps = ConfigField(
        cli_meta=CLIOption(
            name="no_deps",
            cli_option_str="--no-deps",
            help="Do not any dependencies. Directly used the image provided",
            is_flag=True,
        ),
        field_type=bool,
        default=False,
        help="Do not bake any dependencies. Directly used the image provided",
    )

    force_upgrade = ConfigField(
        cli_meta=CLIOption(
            name="force_upgrade",
            cli_option_str="--force-upgrade",
            help="Force upgrade the app even if it is currently being upgraded.",
            is_flag=True,
        ),
        field_type=bool,
        default=False,
        help="Force upgrade the app even if it is currently being upgraded.",
    )

    # ------- Experimental -------------
    # These options get treated in the `..experimental` module.
    # If we move any option as a first class citizen then we need to move
    # its capsule parsing from the `..experimental` module to the `..capsule.CapsuleInput` module.

    persistence = ConfigField(
        cli_meta=CLIOption(
            name="persistence",
            cli_option_str="--persistence",
            help="The persistence mode to deploy the app with.",
            choices=["none", "postgres"],
        ),
        validation_fn=BasicAppValidations.persistence,
        field_type=str,
        default="none",
        example="postgres",
        is_experimental=True,
    )

    project = ConfigField(
        cli_meta=CLIOption(
            name="project",
            cli_option_str="--project",
            help="The project name to deploy the app to.",
        ),
        field_type=str,
        is_experimental=True,
        example="my-project",
    )
    branch = ConfigField(
        cli_meta=CLIOption(
            name="branch",
            cli_option_str="--branch",
            help="The branch name to deploy the app to.",
        ),
        field_type=str,
        is_experimental=True,
        example="main",
    )
    models = ConfigField(
        cli_meta=None,
        field_type=list,
        is_experimental=True,
        example=[{"asset_id": "model-123", "asset_instance_id": "instance-456"}],
    )
    data = ConfigField(
        cli_meta=None,
        field_type=list,
        is_experimental=True,
        example=[{"asset_id": "data-789", "asset_instance_id": "instance-101"}],
    )
    # ------- /Experimental -------------

    def to_dict(self):
        return config_meta_to_dict(self)

    @staticmethod
    def merge_configs(
        base_config: "CoreConfig", override_config: "CoreConfig"
    ) -> "CoreConfig":
        """
        Merge two configurations with override taking precedence.

        Handles FieldBehavior for proper merging:
        - UNION: Merge values (for lists, dicts)
        - NOT_ALLOWED: Base config value takes precedence (override is ignored)

        Args:
            base_config: Base configuration (lower precedence)
            override_config: Override configuration (higher precedence)

        Returns:
            Merged CoreConfig instance
        """
        merged_config = CoreConfig()

        # Process each field according to its behavior
        for field_name, field_info in CoreConfig._fields.items():  # type: ignore
            base_value = getattr(base_config, field_name, None)
            override_value = getattr(override_config, field_name, None)

            # Get the behavior for this field
            behavior = getattr(field_info, "behavior", FieldBehavior.UNION)

            merged_value = merge_field_values(
                base_value, override_value, field_info, behavior
            )

            setattr(merged_config, field_name, merged_value)

        return merged_config

    def set_defaults(self):
        apply_defaults(self)

    def validate(self):
        validate_config_meta(self)

    @commit_owner_names_across_tree
    def commit(self):
        self.validate()
        validate_required_fields(self)
        self.set_defaults()

    @classmethod
    def from_dict(cls, config_data: Dict[str, Any]) -> "CoreConfig":
        config = cls()
        # Define functions for dict source
        def get_dict_key(field_name, field_info):
            return field_name

        def get_dict_value(source_data, key):
            return source_data.get(key)

        populate_config_recursive(
            config, cls, config_data, get_dict_key, get_dict_value
        )
        return config

    @classmethod
    def from_cli(cls, cli_options: Dict[str, Any]) -> "CoreConfig":
        config = cls()
        # Define functions for CLI source
        def get_cli_key(field_name, field_info):
            # Need to have a special Exception for commands since the Commands
            # are passed down via unprocessed args after `--` in click
            if field_name == cls.commands.name:
                return field_name
            # Return the CLI parameter name if CLI metadata exists
            if field_info.cli_meta and not field_info.cli_meta.hidden:
                return field_info.cli_meta.name
            return None

        def get_cli_value(source_data, key):
            value = source_data.get(key)
            # Only return non-None values since None means not set in CLI
            if value is None:
                return None
            if key == cls.environment.name:
                _env_dict = {}
                for v in value:
                    _env_dict.update(v)
                return _env_dict
            if type(value) == tuple or type(value) == list:
                obj = list(x for x in source_data[key])
                if len(obj) == 0:
                    return None  # Dont return Empty Lists so that we can set Nones
                return obj
            return value

        # Use common recursive population function with nested value checking
        populate_config_recursive(
            config,
            cls,
            cli_options,
            get_cli_key,
            get_cli_value,
        )
        return config
