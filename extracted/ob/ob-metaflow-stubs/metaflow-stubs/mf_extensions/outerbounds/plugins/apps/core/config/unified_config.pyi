######################################################################################################
#                                 Auto-generated Metaflow stub file                                  #
# MF version: 2.19.37.2+obcheckpoint(0.2.10);<unk>(<unk>);ob(v1)                                     #
# Generated on 2026-08-28T18:11:58.375074                                                            #
######################################################################################################

from __future__ import annotations

import metaflow
import typing
if typing.TYPE_CHECKING:
    import metaflow.mf_extensions.outerbounds.plugins.apps.core.config.unified_config
    import typing
    import metaflow.mf_extensions.outerbounds.plugins.apps.core.config.config_utils

from .config_utils import ConfigFieldContext as ConfigFieldContext
from .config_utils import ConfigField as ConfigField
from .config_utils import ConfigMeta as ConfigMeta
from .config_utils import JsonFriendlyKeyValuePairType as JsonFriendlyKeyValuePairType
from .config_utils import PureStringKVPairType as PureStringKVPairType
from .config_utils import CommaSeparatedListType as CommaSeparatedListType
from .config_utils import FieldBehavior as FieldBehavior
from .config_utils import CLIOption as CLIOption
from .config_utils import config_meta_to_dict as config_meta_to_dict
from .config_utils import merge_field_values as merge_field_values
from .config_utils import apply_defaults as apply_defaults
from .config_utils import populate_config_recursive as populate_config_recursive
from .config_utils import validate_config_meta as validate_config_meta
from .config_utils import validate_required_fields as validate_required_fields
from .config_utils import ConfigValidationFailedException as ConfigValidationFailedException
from .config_utils import commit_owner_names_across_tree as commit_owner_names_across_tree

UNASSIGNED_PROJECT_BRANCH: str

class BakedImage(tuple, metaclass=type):
    """
    BakedImage(image, python_path)
    """
    @staticmethod
    def __new__(_cls, image, python_path):
        """
        Create new instance of BakedImage(image, python_path)
        """
        ...
    def __repr__(self):
        """
        Return a nicely formatted representation string
        """
        ...
    def __getnewargs__(self):
        """
        Return self as a plain tuple.  Used by copy and pickle.
        """
        ...
    ...

class PackagedCode(tuple, metaclass=type):
    """
    PackagedCode(url, key)
    """
    @staticmethod
    def __new__(_cls, url, key):
        """
        Create new instance of PackagedCode(url, key)
        """
        ...
    def __repr__(self):
        """
        Return a nicely formatted representation string
        """
        ...
    def __getnewargs__(self):
        """
        Return self as a plain tuple.  Used by copy and pickle.
        """
        ...
    ...

class classproperty(property, metaclass=type):
    def __get__(self, owner_self, owner_cls):
        ...
    ...

class AuthType(object, metaclass=type):
    @classmethod
    def enums(cls):
        ...
    @property
    def default(cls):
        ...
    @classmethod
    def choices(cls):
        ...
    ...

class CapsuleType(object, metaclass=type):
    @classmethod
    def enums(cls):
        ...
    @property
    def default(cls):
        ...
    @classmethod
    def choices(cls):
        ...
    ...

class UnitParser(object, metaclass=type):
    def __init__(self, metric_name: str):
        ...
    def validate(self, value: str):
        ...
    def process(self, value: str):
        ...
    def parse(self, value: typing.Union[str, None]):
        ...
    @staticmethod
    def validation_wrapper_fn(metric_name: str):
        ...
    ...

class BasicValidations(object, metaclass=type):
    def __init__(self, config_meta_class, field_name):
        ...
    def enum_validation(self, enums: typing.List[str], current_value):
        ...
    def range_validation(self, min_value, max_value, current_value):
        ...
    def length_validation(self, max_length, current_value):
        ...
    def regex_validation(self, regex, current_value):
        ...
    ...

class ResourceConfig(object, metaclass=metaflow.mf_extensions.outerbounds.plugins.apps.core.config.config_utils.ConfigMeta):
    """
    Resource configuration for the app.
    """
    def _get_field(cls, field_name: str) -> metaflow.mf_extensions.outerbounds.plugins.apps.core.config.config_utils.ConfigField:
        ...
    ...

class HealthCheckConfig(object, metaclass=metaflow.mf_extensions.outerbounds.plugins.apps.core.config.config_utils.ConfigMeta):
    """
    Health check configuration.
    """
    def _get_field(cls, field_name: str) -> metaflow.mf_extensions.outerbounds.plugins.apps.core.config.config_utils.ConfigField:
        ...
    ...

class AuthConfig(object, metaclass=metaflow.mf_extensions.outerbounds.plugins.apps.core.config.config_utils.ConfigMeta):
    """
    Authentication configuration.
    """
    @staticmethod
    def validate(auth_config: "AuthConfig"):
        ...
    def _get_field(cls, field_name: str) -> metaflow.mf_extensions.outerbounds.plugins.apps.core.config.config_utils.ConfigField:
        ...
    ...

class ProxyConfig(object, metaclass=metaflow.mf_extensions.outerbounds.plugins.apps.core.config.config_utils.ConfigMeta):
    """
    The workload a `Proxy` capsule forwards traffic to. Only applies when
    `capsule_type` is `Proxy`.
    
    The target is named in exactly one of two ways:
    - `service_url`: a service that already exists. The port is carried in the URL,
      so the capsule's `port` need not be set in this mode.
    - `namespace` + `selector_labels`: the pods to put a service in front of. The
      namespace must already exist and the labels must match those pods.
    """
    @staticmethod
    def is_set(proxy_config: typing.Union["ProxyConfig", None]) -> bool:
        ...
    @staticmethod
    def targets_existing_service(proxy_config: typing.Union["ProxyConfig", None]) -> bool:
        ...
    @staticmethod
    def targets_pods(proxy_config: typing.Union["ProxyConfig", None]) -> bool:
        ...
    @staticmethod
    def validate(proxy_config: "ProxyConfig"):
        ...
    def _get_field(cls, field_name: str) -> metaflow.mf_extensions.outerbounds.plugins.apps.core.config.config_utils.ConfigField:
        ...
    ...

class ScalingPolicyConfig(object, metaclass=metaflow.mf_extensions.outerbounds.plugins.apps.core.config.config_utils.ConfigMeta):
    """
    Policies for autoscaling replicas. Available policies:
    - Request based Autoscaling (rpm)
    """
    def _get_field(cls, field_name: str) -> metaflow.mf_extensions.outerbounds.plugins.apps.core.config.config_utils.ConfigField:
        ...
    ...

class ReplicaConfig(object, metaclass=metaflow.mf_extensions.outerbounds.plugins.apps.core.config.config_utils.ConfigMeta):
    """
    Replica configuration.
    """
    @staticmethod
    def defaults(replica_config: "ReplicaConfig"):
        ...
    @staticmethod
    def validate(replica_config: "ReplicaConfig"):
        ...
    def _get_field(cls, field_name: str) -> metaflow.mf_extensions.outerbounds.plugins.apps.core.config.config_utils.ConfigField:
        ...
    ...

def more_than_n_not_none(n, *args):
    ...

class DependencyConfig(object, metaclass=metaflow.mf_extensions.outerbounds.plugins.apps.core.config.config_utils.ConfigMeta):
    """
    Dependency configuration.
    """
    @staticmethod
    def validate(dependency_config: "DependencyConfig"):
        ...
    def _get_field(cls, field_name: str) -> metaflow.mf_extensions.outerbounds.plugins.apps.core.config.config_utils.ConfigField:
        ...
    ...

class PackageConfig(object, metaclass=metaflow.mf_extensions.outerbounds.plugins.apps.core.config.config_utils.ConfigMeta):
    """
    Package configuration.
    """
    @staticmethod
    def validate(package_config: "PackageConfig"):
        ...
    def _get_field(cls, field_name: str) -> metaflow.mf_extensions.outerbounds.plugins.apps.core.config.config_utils.ConfigField:
        ...
    ...

def everything_is_string(*args):
    ...

class BasicAppValidations(object, metaclass=type):
    @staticmethod
    def name(name):
        ...
    @staticmethod
    def port(port):
        ...
    @staticmethod
    def tags(tags):
        ...
    @staticmethod
    def secrets(secrets):
        ...
    @staticmethod
    def persistence(persistence):
        ...
    @staticmethod
    def capsule_type(capsule_type):
        ...
    @staticmethod
    def url_slug(url_slug):
        ...
    @staticmethod
    def port_required(core_config: CoreConfig) -> bool:
        ...
    @staticmethod
    def proxy_agreement(core_config: CoreConfig):
        """
        Proxy settings belong to a Proxy capsule and nothing else.
        """
        ...
    @staticmethod
    def url_generation_agreement(core_config: CoreConfig):
        """
        An app's URL is either named by `url_slug` or generated from its name.
        """
        ...
    ...

class CoreConfig(object, metaclass=metaflow.mf_extensions.outerbounds.plugins.apps.core.config.config_utils.ConfigMeta):
    """
    Unified App Configuration - The single source of truth for application configuration.
    
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
    def to_dict(self):
        ...
    @staticmethod
    def merge_configs(base_config: "CoreConfig", override_config: "CoreConfig") -> "CoreConfig":
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
        ...
    def set_defaults(self):
        ...
    def validate(self):
        ...
    def commit(self, *args, **kwargs):
        ...
    @classmethod
    def from_dict(cls, config_data: typing.Dict[str, typing.Any]) -> "CoreConfig":
        ...
    @classmethod
    def from_cli(cls, cli_options: typing.Dict[str, typing.Any]) -> "CoreConfig":
        ...
    def _get_field(cls, field_name: str) -> metaflow.mf_extensions.outerbounds.plugins.apps.core.config.config_utils.ConfigField:
        ...
    ...

