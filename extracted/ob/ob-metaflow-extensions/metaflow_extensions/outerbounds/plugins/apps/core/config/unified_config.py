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

UNASSIGNED_PROJECT_BRANCH = "__unassigned__"

from .config_utils import (
    ConfigFieldContext,
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

from collections import namedtuple


# Result of image baking operation
# - image: The fully qualified Docker image URL
# - python_path: Path to the Python executable in the baked image
BakedImage = namedtuple("BakedImage", ["image", "python_path"])

# Result of code packaging operation
# - url: The package URL in object storage
# - key: Unique content-addressed key identifying this package
PackagedCode = namedtuple("PackagedCode", ["url", "key"])


class classproperty(property):
    def __get__(self, owner_self, owner_cls):
        return self.fget(owner_cls)


class AuthType:
    BROWSER = "Browser"
    API = "API"
    BROWSER_AND_API = "BrowserAndApi"

    @classmethod
    def enums(cls):
        return [cls.BROWSER, cls.API, cls.BROWSER_AND_API]

    @classproperty
    def default(cls):
        return cls.BROWSER

    @classmethod
    def choices(cls):
        return [cls.BROWSER, cls.API, cls.BROWSER_AND_API]


class CapsuleType:
    # What the platform actually runs for a capsule.
    # - Standard: the image/commands configured on the capsule itself.
    # - Proxy: nothing of its own; it only fronts a workload that is already
    #   running in the cluster (see ProxyConfig).
    STANDARD = "Standard"
    PROXY = "Proxy"

    @classmethod
    def enums(cls):
        return [cls.STANDARD, cls.PROXY]

    @classproperty
    def default(cls):
        return cls.STANDARD

    @classmethod
    def choices(cls):
        return [cls.STANDARD, cls.PROXY]


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
        ),
        field_type=str,
        help="CPU requests",
        example="500m",
        validation_fn=UnitParser.validation_wrapper_fn("cpu"),
        parsing_fn=UnitParser("cpu").parse,
    )
    memory = ConfigField(
        default="4Gi",
        cli_meta=CLIOption(
            name="memory",
            cli_option_str="--memory",
        ),
        field_type=str,
        help="Memory requests",
        example="512Mi",
        validation_fn=UnitParser.validation_wrapper_fn("memory"),
        parsing_fn=UnitParser("memory").parse,
    )
    gpu = ConfigField(
        cli_meta=CLIOption(
            name="gpu",
            cli_option_str="--gpu",
        ),
        field_type=str,
        help="GPU requests",
        example="1",
        validation_fn=UnitParser.validation_wrapper_fn("gpu"),
        parsing_fn=UnitParser("gpu").parse,
    )
    disk = ConfigField(
        default="20Gi",
        cli_meta=CLIOption(
            name="disk",
            cli_option_str="--disk",
        ),
        field_type=str,
        help="Storage disk size.",
        example="1Gi",
        validation_fn=UnitParser.validation_wrapper_fn("disk"),
        parsing_fn=UnitParser("disk").parse,
    )

    shared_memory = ConfigField(
        cli_meta=CLIOption(
            name="shared_memory",
            cli_option_str="--shared-memory",
        ),
        field_type=str,
        help="Shared memory",
        example="1Gi",
        validation_fn=UnitParser.validation_wrapper_fn("memory"),
        parsing_fn=UnitParser("memory").parse,
    )


class HealthCheckConfig(metaclass=ConfigMeta):
    """Health check configuration."""

    enabled = ConfigField(
        default=False,
        cli_meta=CLIOption(
            name="health_check_enabled",
            cli_option_str="--health-check-enabled",
            is_flag=True,
        ),
        field_type=bool,
        help="Whether to enable health checks.",
        example=True,
    )
    path = ConfigField(
        cli_meta=CLIOption(
            name="health_check_path",
            cli_option_str="--health-check-path",
        ),
        field_type=str,
        help="The path for health checks.",
        example="/health",
    )
    initial_delay_seconds = ConfigField(
        cli_meta=CLIOption(
            name="health_check_initial_delay",
            cli_option_str="--health-check-initial-delay",
        ),
        field_type=int,
        help="Number of seconds to wait before performing the first health check.",
        example=10,
    )
    period_seconds = ConfigField(
        cli_meta=CLIOption(
            name="health_check_period",
            cli_option_str="--health-check-period",
        ),
        field_type=int,
        help="How often to perform the health check.",
        example=30,
    )


class AuthConfig(metaclass=ConfigMeta):
    """Authentication configuration."""

    type = ConfigField(
        default=AuthType.BROWSER,
        cli_meta=CLIOption(
            name="auth_type",
            cli_option_str="--auth-type",
            choices=AuthType.choices(),
        ),
        field_type=str,
        help="The type of authentication to use for the app.",
        example="Browser",
    )
    public = ConfigField(
        default=True,
        cli_meta=CLIOption(
            name="auth_public",
            cli_option_str="--public-access/--private-access",
            is_flag=True,
        ),
        field_type=bool,
        help="Whether the app is public or not.",
        example=True,
    )

    @staticmethod
    def validate(auth_config: "AuthConfig"):
        if auth_config.type is None:
            return True
        return BasicValidations(AuthConfig, "type").enum_validation(
            AuthType.choices(), auth_config.type
        )


class ProxyConfig(metaclass=ConfigMeta):
    """
    The workload a `Proxy` capsule forwards traffic to. Only applies when
    `capsule_type` is `Proxy`.

    The target is named in exactly one of two ways:
    - `service_url`: a service that already exists. The port is carried in the URL,
      so the capsule's `port` need not be set in this mode.
    - `namespace` + `selector_labels`: the pods to put a service in front of. The
      namespace must already exist and the labels must match those pods.
    """

    # These mirror the validations the Capsule CRD enforces on `proxySettings`, so
    # that a bad target is reported here instead of coming back as an API error.
    SERVICE_URL_REGEX = r"^(https?://)?[a-zA-Z0-9._~%-]+(:[0-9]{1,5})?(/[^\s]*)?$"
    # Kubernetes DNS-1123 label (namespaces) and label key/value rules.
    DNS_1123_LABEL_REGEX = r"^[a-z0-9]([-a-z0-9]*[a-z0-9])?$"
    DNS_1123_SUBDOMAIN_REGEX = (
        r"^[a-z0-9]([-a-z0-9]*[a-z0-9])?(\.[a-z0-9]([-a-z0-9]*[a-z0-9])?)*$"
    )
    LABEL_NAME_REGEX = r"^[A-Za-z0-9]([-A-Za-z0-9_.]*[A-Za-z0-9])?$"
    LABEL_VALUE_REGEX = r"^(([A-Za-z0-9][-A-Za-z0-9_.]*)?[A-Za-z0-9])?$"

    _TARGETING_MESSAGE = (
        "proxy must set either `service_url`, or both `namespace` and "
        "`selector_labels`, but not a mix of the two."
    )

    namespace = ConfigField(
        cli_meta=CLIOption(
            name="proxy_namespace",
            cli_option_str="--proxy-namespace",
        ),
        field_type=str,
        help=(
            "The namespace where the pods being proxied live. The service fronting them "
            "is created here. Required unless `service_url` is set."
        ),
        example="jobs-default",
    )
    selector_labels = ConfigField(
        cli_meta=CLIOption(
            name="proxy_selector_labels",
            cli_option_str="--proxy-selector-label",
            multiple=True,
            click_type=PureStringKVPairType,
        ),
        field_type=dict,
        help=(
            "The labels of the pods being proxied. They become the selector of the service "
            "that fronts those pods, so they must match the labels on them. "
            "Required unless `service_url` is set."
        ),
        example={"app": "my-app"},
    )
    service_url = ConfigField(
        cli_meta=CLIOption(
            name="proxy_service_url",
            cli_option_str="--proxy-service-url",
        ),
        field_type=str,
        help=(
            "The address of a service that already exists, e.g. "
            "`my-svc.my-ns.svc.cluster.local:8080`. The scheme is optional and defaults to "
            "http, a port must be included if the target isn't on the scheme's default port, "
            "and a path may be appended to rewrite requests into a subpath of the target. "
            "The address is not checked at deploy time: if it doesn't resolve, the proxy "
            "crashloops until it does."
        ),
        example="my-svc.my-ns.svc.cluster.local:8080",
    )

    @staticmethod
    def is_set(proxy_config: Optional["ProxyConfig"]) -> bool:
        if proxy_config is None:
            return False
        return any(
            [
                proxy_config.namespace,
                proxy_config.selector_labels,
                proxy_config.service_url,
            ]
        )

    @staticmethod
    def targets_existing_service(proxy_config: Optional["ProxyConfig"]) -> bool:
        return proxy_config is not None and bool(proxy_config.service_url)

    @staticmethod
    def targets_pods(proxy_config: Optional["ProxyConfig"]) -> bool:
        if proxy_config is None:
            return False
        return bool(proxy_config.namespace or proxy_config.selector_labels)

    @staticmethod
    def _targeting_error(proxy_config: "ProxyConfig", field_name: str):
        return ConfigValidationFailedException(
            field_name=field_name,
            field_info=proxy_config._get_field(field_name),  # type: ignore
            current_value=getattr(proxy_config, field_name),
            message=ProxyConfig._TARGETING_MESSAGE,
        )

    @staticmethod
    def validate(proxy_config: "ProxyConfig"):
        if not ProxyConfig.is_set(proxy_config):
            return True

        targets_service = ProxyConfig.targets_existing_service(proxy_config)
        targets_pods = ProxyConfig.targets_pods(proxy_config)
        if targets_service == targets_pods:
            raise ProxyConfig._targeting_error(proxy_config, "service_url")

        if targets_service:
            return BasicValidations(ProxyConfig, "service_url").regex_validation(
                ProxyConfig.SERVICE_URL_REGEX, proxy_config.service_url
            )

        if not (proxy_config.namespace and proxy_config.selector_labels):
            _missing = "namespace" if not proxy_config.namespace else "selector_labels"
            raise ProxyConfig._targeting_error(proxy_config, _missing)

        # The namespace and the labels are what the service fronting the target pods is
        # built from, so reject anything Kubernetes would refuse later on.
        _namespace_validator = BasicValidations(ProxyConfig, "namespace")
        _namespace_validator.length_validation(63, proxy_config.namespace)
        _namespace_validator.regex_validation(
            ProxyConfig.DNS_1123_LABEL_REGEX, proxy_config.namespace
        )

        for key, value in proxy_config.selector_labels.items():  # type: ignore
            ProxyConfig._validate_label(proxy_config, key, value)

        return True

    @staticmethod
    def _validate_label(proxy_config: "ProxyConfig", key, value):
        def _fail(message):
            raise ConfigValidationFailedException(
                field_name="selector_labels",
                field_info=proxy_config._get_field("selector_labels"),  # type: ignore
                current_value=proxy_config.selector_labels,
                message=message,
            )

        if not everything_is_string(key, value):
            _fail(
                "proxy `selector_labels` must be a mapping of strings to strings. "
                "`%s` is set to `%s`." % (key, value)
            )

        # A label key is an optional `prefix/` (a DNS subdomain) followed by a name.
        prefix, _, name = key.rpartition("/")
        if prefix and not (
            len(prefix) <= 253
            and re.match(ProxyConfig.DNS_1123_SUBDOMAIN_REGEX, prefix)
        ):
            _fail(
                "proxy `selector_labels` key `%s` has an invalid prefix `%s`. The prefix "
                "must be a DNS subdomain of at most 253 characters." % (key, prefix)
            )
        if not (len(name) <= 63 and re.match(ProxyConfig.LABEL_NAME_REGEX, name)):
            _fail(
                "proxy `selector_labels` key `%s` is not a valid label name. It must be at "
                "most 63 characters and match `%s`."
                % (key, ProxyConfig.LABEL_NAME_REGEX)
            )
        if not (len(value) <= 63 and re.match(ProxyConfig.LABEL_VALUE_REGEX, value)):
            _fail(
                "proxy `selector_labels` value `%s` for key `%s` is not a valid label "
                "value. It must be at most 63 characters and match `%s`."
                % (value, key, ProxyConfig.LABEL_VALUE_REGEX)
            )


class ScalingPolicyConfig(metaclass=ConfigMeta):
    """
    Policies for autoscaling replicas. Available policies:
    - Request based Autoscaling (rpm)
    """

    # TODO Change the defaulting if we have more autoscaling policies.
    rpm = ConfigField(
        field_type=int,
        cli_meta=CLIOption(
            name="scaling_rpm",
            cli_option_str="--scaling-rpm",
        ),
        help=(
            "Scale up replicas when the requests per minute crosses this threshold. "
            "If nothing is provided and the replicas.max and replicas.min is set then "
            "the default rpm would be 60."
        ),
        default=60,
    )


class ReplicaConfig(metaclass=ConfigMeta):
    """Replica configuration."""

    fixed = ConfigField(
        cli_meta=CLIOption(
            name="fixed_replicas",
            cli_option_str="--fixed-replicas",
        ),
        field_type=int,
        help="The fixed number of replicas to deploy the app with. If min and max are set, this will raise an error.",
        example=1,
    )

    min = ConfigField(
        cli_meta=CLIOption(
            name="min_replicas",
            cli_option_str="--min-replicas",
        ),
        field_type=int,
        help="The minimum number of replicas to deploy the app with.",
        example=1,
    )
    max = ConfigField(
        cli_meta=CLIOption(
            name="max_replicas",
            cli_option_str="--max-replicas",
        ),
        field_type=int,
        help="The maximum number of replicas to deploy the app with.",
        example=10,
    )

    scaling_policy = ConfigField(
        cli_meta=None,
        field_type=ScalingPolicyConfig,
        help=(
            "Scaling policy defines the the metric based on which the replicas will horizontally scale. "
            "If min and max replicas are set and are not the same, then a scaling policy will be applied. "
            "Default scaling policies can be 60 rpm (ie 1 rps). "
        ),
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
        ),
        field_type=str,
        help="The path to the requirements.txt file to attach to the app.",
        behavior=FieldBehavior.NOT_ALLOWED,
        example="requirements.txt",
    )
    from_pyproject_toml = ConfigField(
        cli_meta=CLIOption(
            name="dep_from_pyproject",
            cli_option_str="--dep-from-pyproject",
        ),
        field_type=str,
        help="The path to the pyproject.toml file to attach to the app.",
        behavior=FieldBehavior.NOT_ALLOWED,
        example="pyproject.toml",
    )
    python = ConfigField(
        cli_meta=CLIOption(
            name="python",
            cli_option_str="--python",
        ),
        field_type=str,
        help="The Python version to use for the app.",
        behavior=FieldBehavior.UNION,
        example="3.10",
    )
    pypi = ConfigField(
        cli_meta=CLIOption(
            name="pypi",  # TODO: Can set CLI meta to None
            cli_option_str="--pypi",
            hidden=True,  # Complex structure, better handled in config file
        ),
        field_type=dict,
        help="A dictionary of pypi dependencies to attach to the app. The key is the package name and the value is the version.",
        behavior=FieldBehavior.NOT_ALLOWED,
        example={"numpy": "1.23.0", "pandas": ""},
    )
    conda = ConfigField(
        cli_meta=CLIOption(  # TODO: Can set CLI meta to None
            name="conda",
            cli_option_str="--conda",
            hidden=True,  # Complex structure, better handled in config file
        ),
        field_type=dict,
        help="A dictionary of conda dependencies to attach to the app. The key is the package name and the value is the version.",
        behavior=FieldBehavior.NOT_ALLOWED,
        example={"numpy": "1.23.0", "pandas": ""},
    )
    anaconda = ConfigField(
        cli_meta=CLIOption(  # TODO: Can set CLI meta to None
            name="anaconda",
            cli_option_str="--anaconda",
            hidden=True,  # Complex structure, better handled in config file
        ),
        field_type=dict,
        help=(
            "A dictionary of Anaconda dependencies to attach to the app. The key is the "
            "package name and the value is the version."
        ),
        behavior=FieldBehavior.NOT_ALLOWED,
        example={
            "numpy": "1.23.0",
        },
    )

    extra_configs = ConfigField(
        cli_meta=CLIOption(
            name="extra_configs",
            cli_option_str="--deps-extra-configs",
            hidden=True,  # Complex structure, better handled in config file
        ),
        field_type=dict,
        help=("A dictionary of extra configuration passed to the image bakery."),
        behavior=FieldBehavior.NOT_ALLOWED,
        example={"channel_priority": "strict"},
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
        if any(
            [
                dependency_config.pypi,
                dependency_config.conda,
                dependency_config.anaconda,
            ]
        ) and any(
            [
                dependency_config.from_requirements_file,
                dependency_config.from_pyproject_toml,
            ]
        ):
            raise ConfigValidationFailedException(
                field_name="pypi"
                if dependency_config.pypi
                else ("conda" if dependency_config.conda else "anaconda"),
                field_info=dependency_config._get_field(  # type: ignore
                    "pypi"
                    if dependency_config.pypi
                    else ("conda" if dependency_config.conda else "anaconda")
                ),
                current_value=dependency_config.pypi or dependency_config.conda,
                message="Cannot set pypi or conda when from_requirements_file or from_pyproject_toml is set",
            )
        if more_than_n_not_none(
            1,
            dependency_config.pypi,
            dependency_config.conda,
            dependency_config.anaconda,
        ):
            raise ConfigValidationFailedException(
                field_name="pypi"
                if dependency_config.pypi
                else ("conda" if dependency_config.conda else "anaconda"),
                field_info=dependency_config._get_field(  # type: ignore
                    "pypi"
                    if dependency_config.pypi
                    else ("conda" if dependency_config.conda else "anaconda")
                ),
                current_value=dependency_config.pypi or dependency_config.conda,
                message="Cannot add dependencies from pypi and conda at the same time. Please use only one.",
            )

        return True


class PackageConfig(metaclass=ConfigMeta):
    """Package configuration."""

    src_paths = ConfigField(
        cli_meta=CLIOption(
            name="package_src_path",
            cli_option_str="--package-src-path",
            multiple=True,
            click_type=str,
        ),
        field_type=list,
        help="The path to the source code to deploy with the App.",
        example=["./"],
    )
    suffixes = ConfigField(
        cli_meta=CLIOption(
            name="package_suffixes",
            cli_option_str="--package-suffixes",
        ),
        field_type=list,
        help="A list of suffixes to add to the source code to deploy with the App.",
        example=[".py", ".ipynb"],
    )

    @staticmethod
    def validate(package_config: "PackageConfig"):
        if package_config.src_paths is None:
            return True
        if package_config.src_paths:
            for path in package_config.src_paths:
                if not os.path.exists(path):
                    raise ConfigValidationFailedException(
                        field_name="src_paths",
                        field_info=package_config._get_field("src_paths"),  # type: ignore
                        current_value=package_config.src_paths,
                        message=f"Path does not exist : `{path}`",
                    )
                if not os.path.isdir(path):
                    raise ConfigValidationFailedException(
                        field_name="src_paths",
                        field_info=package_config._get_field("src_paths"),  # type: ignore
                        current_value=package_config.src_paths,
                        message=f"Path is not a directory : `{path}`",
                    )
        return True


def everything_is_string(*args):
    return all(isinstance(arg, str) for arg in args)


class BasicAppValidations:
    @staticmethod
    def name(name):
        if name is None:
            return True
        regex = r"^[a-z0-9-]+$"  # Only allow lowercase letters, numbers, and hyphens
        validator = BasicValidations(CoreConfig, "name")
        return validator.length_validation(150, name) and validator.regex_validation(
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
        if not all(
            isinstance(tag, dict)
            and len(tag) == 1
            and all(
                [everything_is_string(*tag.keys()), everything_is_string(*tag.values())]
            )
            for tag in tags
        ):
            raise ConfigValidationFailedException(
                field_name="tags",
                field_info=CoreConfig._get_field(CoreConfig, "tags"),  # type: ignore
                current_value=tags,
                message="Tags must be a list of dictionaries with one key and the value must be a string. Currently they are set to %s "
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

    @staticmethod
    def capsule_type(capsule_type):
        if capsule_type is None:
            return True
        return BasicValidations(CoreConfig, "capsule_type").enum_validation(
            CapsuleType.choices(), capsule_type
        )

    @staticmethod
    def url_slug(url_slug):
        # An empty slug means "generate a URL for me", which is what the platform
        # reads it as too, and what `CapsuleInput` sends by leaving the field out.
        if not url_slug:
            return True
        # These mirror the validations the platform applies to the slug, so that a
        # bad one is reported here instead of coming back as an API error.
        regex = r"^[a-z0-9]([-a-z0-9]*[a-z0-9])?$"
        # The slug becomes one DNS label, so it gets that 63 character limit less
        # the longest prefix the platform prepends to it (`api-`).
        max_length = 59
        # Every URL the platform generates for itself starts with `c-`.
        reserved_prefix = "c-"

        validator = BasicValidations(CoreConfig, "url_slug")
        validator.length_validation(max_length, url_slug)
        validator.regex_validation(regex, url_slug)
        if url_slug.startswith(reserved_prefix):
            raise ConfigValidationFailedException(
                field_name="url_slug",
                field_info=CoreConfig._get_field(CoreConfig, "url_slug"),  # type: ignore
                current_value=url_slug,
                message=(
                    "url_slug cannot start with `%s`, that prefix is reserved for "
                    "generated URLs." % reserved_prefix
                ),
            )
        return True

    @staticmethod
    def port_required(core_config: "CoreConfig") -> bool:
        # A Proxy capsule pointing at an existing service carries the port in the
        # service URL, so it has no port of its own.
        if core_config.capsule_type != CapsuleType.PROXY:
            return True
        return not ProxyConfig.targets_existing_service(core_config.proxy)

    @staticmethod
    def proxy_agreement(core_config: "CoreConfig"):
        """Proxy settings belong to a Proxy capsule and nothing else."""
        proxy_is_set = ProxyConfig.is_set(core_config.proxy)
        is_proxy = core_config.capsule_type == CapsuleType.PROXY

        if is_proxy and not proxy_is_set:
            raise ConfigValidationFailedException(
                field_name="proxy",
                field_info=CoreConfig._get_field(CoreConfig, "proxy"),  # type: ignore
                current_value=None,
                message=(
                    "proxy is required when capsule_type is `%s`. Set either "
                    "`proxy.service_url`, or both `proxy.namespace` and "
                    "`proxy.selector_labels`." % CapsuleType.PROXY
                ),
            )
        if proxy_is_set and not is_proxy:
            raise ConfigValidationFailedException(
                field_name="proxy",
                field_info=CoreConfig._get_field(CoreConfig, "proxy"),  # type: ignore
                current_value=None,
                message=(
                    "proxy can only be set when capsule_type is `%s`. It is currently "
                    "set to `%s`." % (CapsuleType.PROXY, core_config.capsule_type)
                ),
            )
        return True

    @staticmethod
    def url_generation_agreement(core_config: "CoreConfig"):
        """An app's URL is either named by `url_slug` or generated from its name."""
        # Both are checked for truthiness rather than for being set: defaults are
        # applied after validation, so `generate_static_url` is None here until
        # somebody asks for it, and an explicit False is the same as not asking.
        if not (core_config.url_slug and core_config.generate_static_url):
            return True
        raise ConfigValidationFailedException(
            field_name="url_slug",
            field_info=CoreConfig._get_field(CoreConfig, "url_slug"),  # type: ignore
            current_value=core_config.url_slug,
            message=(
                "url_slug and generate_static_url cannot both be set, since they are "
                "two ways of deciding the same URL. Drop generate_static_url to be "
                "served at the URL `url_slug` names, or drop url_slug to have one "
                "generated from the app name."
            ),
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
        # Required everywhere except for a Proxy capsule that targets an existing
        # service, which carries its port in `proxy.service_url`.
        required=BasicAppValidations.port_required,
        help=(
            "Port where the app is hosted. When deployed this will be port on which we will "
            "deploy the app. For a `Proxy` capsule this is the port of the pods being proxied, "
            "and it is not needed when `proxy.service_url` is used."
        ),
        example=8000,
    )

    # Optional basic fields
    description = ConfigField(
        cli_meta=CLIOption(
            name="description",
            cli_option_str="--description",
        ),
        field_type=str,
        help="The description of the app to deploy.",
        example="This is a description of my app.",
    )
    app_type = ConfigField(
        cli_meta=CLIOption(
            name="app_type",
            cli_option_str="--app-type",
        ),
        field_type=str,
        help="The User defined type of app to deploy. Its only used for bookkeeping purposes.",
        example="MyCustomAgent",
    )
    image = ConfigField(
        cli_meta=CLIOption(
            name="image",
            cli_option_str="--image",
        ),
        field_type=str,
        help="The Docker image to deploy with the App.",
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
        help="Outerbounds integrations to attach to the app. You can use the value you set in the `@secrets` decorator in your code without the outerbounds prefix.",
        example=["hf-token"],
        validation_fn=BasicAppValidations.secrets,
    )
    compute_pools = ConfigField(
        cli_meta=CLIOption(
            name="compute_pools",
            cli_option_str="--compute-pools",
            multiple=True,
            click_type=str,
        ),
        field_type=list,
        help="A list of compute pools to deploy the app to.",
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
        required=False,  # Not required when use_base_image_command=True or no_deps is used in CLI
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
        available_in=ConfigFieldContext.CLI,
        help="The dependencies to attach to the app. ",
    )
    package = ConfigField(
        cli_meta=None,  # No top-level CLI option, only nested fields have CLI options
        field_type=PackageConfig,
        help="Configurations associated with packaging the app.",
        validation_fn=PackageConfig.validate,
        available_in=ConfigFieldContext.CLI,
    )

    # Programmatic-only field for pre-packaged code
    code_package = ConfigField(
        cli_meta=None,
        field_type=tuple,  # PackagedCode is a namedtuple (tuple subclass)
        strict_types=False,  # Accept PackagedCode namedtuple from package_code()
        available_in=ConfigFieldContext.PROGRAMMATIC,
        help="Pre-packaged code from package_code(). A PackagedCode namedtuple containing url and key.",
    )

    no_deps = ConfigField(
        cli_meta=CLIOption(
            name="no_deps",
            cli_option_str="--no-deps",
            help="Do not any dependencies. Directly used the image provided",
            is_flag=True,
        ),
        available_in=ConfigFieldContext.CLI,
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

    use_base_image_command = ConfigField(
        cli_meta=None,
        available_in=ConfigFieldContext.PROGRAMMATIC,
        field_type=bool,
        default=False,
        help=(
            "When True, skip providing startup commands and rely on the container's "
            "entrypoint/CMD. Only available in the programmatic API. "
            "In CLI mode, use `--no-deps` along side passing no command "
            "to enable this behavior."
        ),
    )

    skip_code_package = ConfigField(
        cli_meta=CLIOption(
            name="skip_code_package",
            cli_option_str="--skip-code-package",
            help=(
                "When True, skip code packaging and rely on the container's embedded source code. "
                "This option will ONLY work in conjunction with --no-deps on the CLI since images "
                "baked with fast-bakery require a code package."
            ),
            is_flag=True,
        ),
        field_type=bool,
        default=False,
        help=(
            "When True, skip code packaging and rely on the container's embedded source code. "
            "When running the deployer programmatically, If this field is set, then the user cannot pass `code_package` parameter to the AppDeployer"
        ),
    )

    # ------- Proxy Capsules -------------

    capsule_type = ConfigField(
        cli_meta=CLIOption(
            name="capsule_type",
            cli_option_str="--capsule-type",
            choices=CapsuleType.choices(),
        ),
        validation_fn=BasicAppValidations.capsule_type,
        field_type=str,
        help=(
            "What the platform runs for this deployment. `Standard` (the default) runs the "
            "image and commands configured here. `Proxy` runs nothing of its own and only "
            "fronts a workload that is already running in the cluster, described by `proxy`."
        ),
        example="Proxy",
    )

    proxy = ConfigField(
        cli_meta=None,  # No top-level CLI option, only nested fields have CLI options
        field_type=ProxyConfig,
        validation_fn=ProxyConfig.validate,
        help=(
            "The workload a `Proxy` capsule forwards traffic to. Can only be set when "
            "`capsule_type` is `Proxy`."
        ),
    )

    # ------- URL generation -------------

    url_slug = ConfigField(
        cli_meta=CLIOption(
            name="url_slug",
            cli_option_str="--url-slug",
        ),
        validation_fn=BasicAppValidations.url_slug,
        field_type=str,
        help=(
            "Names the app's URL instead of having one generated for it: "
            "`api-<url_slug>.<your platform domain>`, or `ui-<url_slug>` for an app with "
            "browser-only auth. Cannot be combined with `generate_static_url`, which is "
            "the other way of deciding the same URL. A slug belongs to a single app "
            "across the whole platform deployment, and cannot be changed once an app "
            "has one."
        ),
        example="my-app",
    )

    # ------- Experimental -------------
    # These options get treated in the `..experimental` module.
    # If we move any option as a first class citizen then we need to move
    # its capsule parsing from the `..experimental` module to the `..capsule.CapsuleInput` module.

    persistence = ConfigField(
        cli_meta=CLIOption(
            name="persistence",
            cli_option_str="--persistence",
            choices=["none", "postgres"],
        ),
        validation_fn=BasicAppValidations.persistence,
        field_type=str,
        help="The persistence mode to deploy the app with.",
        default="none",
        example="postgres",
        is_experimental=True,
    )

    project = ConfigField(
        cli_meta=CLIOption(
            name="project",
            cli_option_str="--project",
        ),
        field_type=str,
        help="The project name for the app. Defaults to __unassigned__.",
        default="__unassigned__",
        example="my-project",
    )
    branch = ConfigField(
        cli_meta=CLIOption(
            name="branch",
            cli_option_str="--branch",
        ),
        field_type=str,
        help="The branch name for the app. Defaults to __unassigned__.",
        default="__unassigned__",
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
    generate_static_url = ConfigField(
        cli_meta=CLIOption(
            name="generate_static_url",
            cli_option_str="--generate-static-url",
            is_flag=True,
        ),
        field_type=bool,
        help=(
            "Generate a static URL for the app based on its name. Cannot be combined "
            "with `url_slug`, which names the URL instead."
        ),
        default=False,
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
        # Validations that span more than one field cannot live on a single
        # ConfigField, so they are run here.
        BasicAppValidations.proxy_agreement(self)
        BasicAppValidations.url_generation_agreement(self)

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

        # Options that are repeatable KEY=VALUE pairs on the CLI arrive as a list of
        # single item dicts and need to be collapsed into the one dict the field holds.
        _kv_pair_keys = {
            cls.environment.name,
            ProxyConfig.selector_labels.cli_meta.name,
        }

        def get_cli_value(source_data, key):
            value = source_data.get(key)
            # Only return non-None values since None means not set in CLI
            if value is None:
                return None
            if key in _kv_pair_keys:
                _kv_dict = {}
                for v in value:
                    _kv_dict.update(v)
                return _kv_dict
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
