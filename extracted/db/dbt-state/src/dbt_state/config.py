from __future__ import annotations

import os
import typing as t
import dataclasses
from dataclasses import dataclass, field, Field
from enum import Enum
from pathlib import Path
import yaml

import pytimeparse2

try:
    from dbt.artifacts.resources.v1.config import TestConfig
except ImportError:
    from dbt.contracts.graph.model_config import TestConfig

from dbt.config.profile import read_profile
from dbt.config.runtime import RuntimeConfig
from dbt_state import events

try:
    from dbt_common.exceptions import DbtRuntimeError
except ImportError:
    # dbt 1.7
    from dbt.exceptions import DbtRuntimeError

from query_cache_common.models import shared_models
from dbt_state.utils import str_to_bool
from query_cache_common.utils import to_bool

if t.TYPE_CHECKING:
    from dbt.artifacts.resources.v1.model import ModelConfig
    from dbt.artifacts.resources.v1.seed import SeedConfig
    from dbt.artifacts.resources.v1.snapshot import SnapshotConfig


ENV_VAR_PREFIXES = ("DBT_ENGINE_STATE_", "DBT_ENV_SECRET_STATE_", "RUN_CACHE_", "DBT_RUN_CACHE_")
CONFIG_KEY_PREFIX = "run_cache_"
LOCKED_CONFIG = ("disable_telemetry",)
DISABLE_TELEMETRY = False


def get_env(name: str, default: str = "") -> str:
    """Get an environment variable checking a variety of prefixes.

    RUN_CACHE_ takes precedence over DBT_RUN_CACHE_.

    dbt State (DBT_ENGINE_STATE_ / DBT_ENV_SECRET_STATE_) takes precedence over run cache
    """
    for prefix in ENV_VAR_PREFIXES:
        value = os.environ.get(f"{prefix}{name.upper()}")
        if value is not None:
            return value
    return default


def _resolve_home_path() -> Path:
    env_override = get_env("HOME")
    if env_override:
        return Path(env_override)
    return Path.home() / ".dbt"


DBT_RUN_CACHE_PATH = _resolve_home_path()

DBT_CLOUD_YML_PATH = (
    DBT_RUN_CACHE_PATH / "dbt_cloud.yml"
)  # dbt Platform users create this when setting up the pre-Fusion CLI


DEFER_TO_DEFAULT = "prod"
DEFER_LOG_LEVEL_DEFAULT = "off"
FRESHNESS_TOLERANCE_DEFAULT = 2700  # 45 minutes
METADATA_CACHE_TTL_DEFAULT = 0  # infinite (cache never expires)
API_CLIENT_TIMEOUT_DEFAULT = 60  # seconds
CLIENT_ID_DEFAULT = "2fd87cd5-69a6-4c5f-9097-747a58f0edf6"


# can be replaced with enum.StrEnum if we drop support for python below 3.11
class _StringEnum(str, Enum):
    pass


class CloneIncrementalInDev(_StringEnum):
    NEVER = "NEVER"
    IF_TABLE_MISSING = "IF_TABLE_MISSING"
    ALWAYS = "ALWAYS"


class CacheMode(_StringEnum):
    READ_WRITE = "READ_WRITE"
    """Cache is consulted to make decisions and outcome of those decisions is recorded"""

    WRITE_ONLY = "WRITE_ONLY"
    """Cache is bypassed for decision making but the model/seed execution results are still recorded.
    The point of this is to hit the ground running if the cache mode is flipped to READ_WRITE in future"""

    @property
    def is_read_write(self) -> bool:
        return self.value == CacheMode.READ_WRITE

    @property
    def is_write_only(self) -> bool:
        return self.value == CacheMode.WRITE_ONLY


@dataclass
class DbtPlatformToken:
    host: str
    token: str


FieldAndType = tuple[Field, type]


def _parse_time(value: str) -> int:
    result = pytimeparse2.parse(value)
    if isinstance(result, float):
        return int(result)
    if not isinstance(result, int):
        raise ValueError(f"Cannot parse time value '{value}'")
    return result


TEnum = t.TypeVar("TEnum", bound=_StringEnum)


def _parse_enum(typ: type[TEnum], name: str, value: str) -> TEnum:
    normalized = value.upper()
    try:
        return typ(normalized)
    except ValueError:
        options = [e.value for e in typ]
        raise ValueError(f"Invalid {name} value: '{value}'. Must be one of {options}")


def _parse_clone_incremental_in_dev(value: str) -> CloneIncrementalInDev:
    # map if_missing -> if_table_missing so the enum value still matches
    if value and value.lower() == "if_missing":
        value = "if_table_missing"
    return _parse_enum(CloneIncrementalInDev, "clone_incremental_in_dev", value)


def _parse_cache_mode(value: str) -> CacheMode:
    return _parse_enum(CacheMode, "cache_mode", value)


def _get_active_dbt_project_details(
    runtime_config: RuntimeConfig, dbt_cloud_yml_contents: t.Dict[str, t.Any]
) -> t.Optional[t.Tuple[str, str]]:
    # resolution order from here: https://github.com/dbt-labs/fs/blob/df4e8677c278902f196ad951ca54376feef01b24/crates/dbt-platform-auth/src/resolver/cloud_yaml.rs#L10
    # tl;dr: env takes precedence over dbt_project.yml which takes precedence over dbt_cloud.yml
    # note: both host and project-id are required to match, not just project-id, but they can come from different sources

    context = dbt_cloud_yml_contents.get("context", {})
    if not isinstance(context, dict):
        context = {}

    dbt_cloud = runtime_config.dbt_cloud or {}

    host = (
        os.environ.get("DBT_CLOUD_ACCOUNT_HOST")
        or dbt_cloud.get("account-host")
        or context.get("active-host")
    )
    project_id = (
        os.environ.get("DBT_CLOUD_PROJECT_ID")
        or dbt_cloud.get("project-id")
        or context.get("active-project")
    )

    # Both host and project-id are required to match, but they can resolve from different sources.
    if host and project_id:
        return host, project_id

    return None


@dataclass
class RunCacheConfig:
    defer_to: str = DEFER_TO_DEFAULT
    # Mostly used for demo purposes to output defer to console
    defer_log_level: str = DEFER_LOG_LEVEL_DEFAULT
    # Decision logger configuration
    enable_response_logging: bool = True
    enable_data_tests: bool = True
    log_file_limit: int = 20
    log_dir_override: t.Optional[str] = None
    log_prefix: str = "responses_"
    freshness_tolerance: int = field(
        default=FRESHNESS_TOLERANCE_DEFAULT, metadata={"parser": _parse_time}
    )
    tolerate_nondeterminism: bool = True
    enable_lenient_dependencies: bool = True
    clone_incremental_in_dev: CloneIncrementalInDev = field(
        default=CloneIncrementalInDev.IF_TABLE_MISSING,
        metadata={"parser": _parse_clone_incremental_in_dev},
    )
    clone_time_travel_limit: t.Optional[int] = field(default=None, metadata={"parser": _parse_time})
    metadata_cache_ttl: int = field(
        default=METADATA_CACHE_TTL_DEFAULT, metadata={"parser": _parse_time}
    )
    api_client_timeout: int = field(
        default=API_CLIENT_TIMEOUT_DEFAULT, metadata={"parser": _parse_time}
    )
    oauth_client_id: str = field(default=CLIENT_ID_DEFAULT, metadata={"sensitive": True})
    oauth_client_secret: t.Optional[str] = field(default=None, metadata={"sensitive": True})
    dbt_platform_tokens: t.List[DbtPlatformToken] = field(
        default_factory=list, metadata={"sensitive": True}
    )
    org_id: t.Optional[str] = None
    run_hooks_on_no_op: bool = False
    emit_reused_status: bool = False
    snowflake_get_view_ddl_override: t.Optional[str] = None
    snowflake_metadata_warehouse: t.Optional[str] = None
    cache_mode: CacheMode = field(
        default=CacheMode.READ_WRITE, metadata={"parser": _parse_cache_mode}
    )
    disable_telemetry: bool = field(default_factory=lambda: DISABLE_TELEMETRY)

    @classmethod
    def from_runtime_config(cls, config: RuntimeConfig) -> RunCacheConfig:
        """
        Load configuration from multiple sources with precedence (highest to lowest):
        0. ~/.dbt/dbt_cloud.yml (`state:` section only)
        1. Environment variables (prefixed with DBT_RUN_CACHE_)
        2. Current target configuration in profiles.yml (prefixed with run_cache_)
        3. dbt_project.yml flags section (prefixed with run_cache_)
        4. Default values from the dataclass
        """
        config_fields = cls._fields_and_types()
        dbt_platform_config = cls._load_from_dbt_platform_config(
            config,
            cloud_yml_path=DBT_CLOUD_YML_PATH,
        )
        project_config = cls._load_from_project_flags(config, config_fields)
        profile_config = cls._load_from_profile(config, config_fields)
        env_config = cls._load_from_env(config_fields)
        merged_config = {**project_config, **profile_config, **dbt_platform_config, **env_config}
        return cls(**merged_config)

    @classmethod
    def _load_from_env(cls, config_fields: t.Dict[str, FieldAndType]) -> t.Dict[str, t.Any]:
        """Load configuration from environment variables."""
        config = {}
        for field_name, field_and_type in config_fields.items():
            env_var_value = get_env(field_name)
            if env_var_value:
                config[field_name] = cls._convert_value(env_var_value, field_and_type)

        return config

    @classmethod
    def _load_from_profile(
        cls, runtime_config: RuntimeConfig, config_fields: t.Dict[str, FieldAndType]
    ) -> t.Dict[str, t.Any]:
        """Load configuration from the current target configuration as defined in profiles.yml."""
        config = {}
        raw_profiles = read_profile(runtime_config.args.profiles_dir)
        profile_name = runtime_config.profile_name
        target_name = runtime_config.target_name

        if profile_name in raw_profiles:
            profile = raw_profiles[profile_name]
            outputs = profile.get("outputs", {})
            if target_name in outputs:
                target_config = outputs[target_name]
                for field_name, field_and_type in config_fields.items():
                    config_key = f"{CONFIG_KEY_PREFIX}{field_name}"
                    if config_key in target_config:
                        config[field_name] = cls._convert_value(
                            target_config[config_key], field_and_type
                        )

                # map metadata_warehouse -> snowflake_metadata_warehouse for snowflake targets
                if (
                    (target_type := target_config.get("type"))
                    and target_type == "snowflake"
                    and (metadata_warehouse := target_config.get("metadata_warehouse"))
                ):
                    value = cls._convert_value(
                        metadata_warehouse, config_fields["snowflake_metadata_warehouse"]
                    )
                    config["snowflake_metadata_warehouse"] = value

                # support for outputs.[target name].defer_to_target
                if defer_to_target := target_config.get("defer_to_target"):
                    defer_to_field_type = config_fields["defer_to"]
                    config["defer_to"] = cls._convert_value(defer_to_target, defer_to_field_type)

        return config

    @classmethod
    def _load_from_project_flags(
        cls, runtime_config: RuntimeConfig, config_fields: t.Dict[str, FieldAndType]
    ) -> t.Dict[str, t.Any]:
        """Load configuration from flags section of dbt_project.yml."""
        config = {}
        if hasattr(runtime_config, "flags"):
            flags = runtime_config.flags
        else:
            from dbt.config.renderer import DbtProjectYamlRenderer

            raw_project_config = yaml.safe_load(
                (Path(runtime_config.project_root) / "dbt_project.yml").read_text()
            )
            flags = raw_project_config.get("flags", {})
            renderer = DbtProjectYamlRenderer(
                profile=runtime_config, cli_vars=runtime_config.cli_vars
            )
            flags = renderer.render_data(flags)

        for field_name, field_and_type in config_fields.items():
            config_key = f"{CONFIG_KEY_PREFIX}{field_name}"
            if config_key in flags:
                config[field_name] = cls._convert_value(flags[config_key], field_and_type)

        # state-org-id in the dbt-cloud section takes precedence over flags
        if runtime_config.dbt_cloud and (org_id := runtime_config.dbt_cloud.get("state-org-id")):
            config["org_id"] = org_id

        return config

    @classmethod
    def _load_from_dbt_platform_config(
        cls, runtime_config: RuntimeConfig, cloud_yml_path: Path
    ) -> t.Dict[str, t.Any]:
        config: t.Dict[str, t.Any] = {}

        # if present, these dbt platform tokens can be exchanged for tokens compatible with the state service
        tokens: t.List[DbtPlatformToken] = []

        # first precedence for dbt platform tokens - env vars
        # both service tokens and personal access tokens can be set using this method
        # ref: https://github.com/dbt-labs/fs/blob/df4e8677c278902f196ad951ca54376feef01b24/crates/dbt-platform-auth/src/resolver/env_var.rs#L27
        if (host := os.environ.get("DBT_CLOUD_ACCOUNT_HOST")) and (
            token := os.environ.get("DBT_CLOUD_TOKEN")
        ):
            tokens.append(DbtPlatformToken(host=host, token=token))

        # second precedence for dbt platform tokens - oauth_sessions.json
        # note that the `dbt login` command produces this and it's only present in 1.12
        # so this is not relevant for dbt versions prior to 1.12
        try:
            from dbt.auth.resolvers import OAuthPassiveResolver  # type: ignore[unresolved-import]
            from dbt.auth.credentials import PlatformCredential  # type: ignore[unresolved-import]

            # use the dbt core code to resolve a valid credential
            # rather than trying to parse oauth_sessions.json ourselves
            cred = OAuthPassiveResolver().resolve()
            if isinstance(cred, PlatformCredential):
                tokens.append(DbtPlatformToken(host=cred.account_host, token=cred.token))
        except ImportError:
            # the installed version of the dbt cli doesnt support `dbt login`
            pass
        except Exception as e:
            events.fire_debug_event(
                "Unable to resolve a valid dbt platform oauth token: {}", str(e)
            )

        # third precedence for dbt platform tokens - dbt_cloud.yml
        # note that if specific dbt State oauth credentials exist in the `state:` section, these take precedence
        # over exchanging any platform tokens
        if cloud_yml_path.exists():
            try:
                cloud_yml = yaml.safe_load(cloud_yml_path.read_text())
                if not isinstance(cloud_yml, dict):
                    raise
            except Exception as e:
                raise DbtRuntimeError(
                    f"dbt_cloud.yml found at '{str(cloud_yml_path)}' but we are unable to interpret the contents.\n"
                    "Please ensure it's formatted correctly. For more information, see: https://docs.getdbt.com/docs/platform/configure-cloud-cli#configure-the-dbt-cli"
                ) from e

            # check for user personal access tokens
            if (
                (projects := cloud_yml.get("projects", []))
                and isinstance(projects, list)
                and (project_details := _get_active_dbt_project_details(runtime_config, cloud_yml))
            ):
                # scrape credentials from the active project
                # If no projects match, we dont fallback to any default, it's the same as no credentials being present at all
                active_project_host, active_project_id = project_details
                project = next(
                    (
                        p
                        for p in projects
                        if isinstance(p, dict)
                        and p.get("account-host") == active_project_host
                        and p.get("project-id") == active_project_id
                    ),
                    None,
                )
                if isinstance(project, dict):
                    # in practice, project["token-value"] is a personal access token, but nothing prevents
                    # a service account token from being used as a token-value in future
                    if token_value := project.get("token-value"):
                        tokens.append(DbtPlatformToken(host=active_project_host, token=token_value))

            # dbt_cloud.yml can also have a `state:` section containing `client-id` and `client-secret`
            client_id = None
            client_secret = None
            if (state_section := cloud_yml.get("state")) and isinstance(state_section, dict):
                client_id = state_section.get("client-id")
                client_secret = state_section.get("client-secret")

                if client_id and client_secret:
                    config["oauth_client_id"] = client_id
                    config["oauth_client_secret"] = client_secret

        if tokens:
            config["dbt_platform_tokens"] = tokens

        return config

    @classmethod
    def _convert_value(cls, value: t.Any, field_and_type: FieldAndType) -> t.Any:
        """If the value is string, coerce it to the target type."""
        if not isinstance(value, str):
            return value

        target_field, target_type = field_and_type

        if target_type == str:
            return value

        # Handle Optional types by checking whether the given type is a generic Union type with
        # one of its arguments being NoneType
        if t.get_origin(target_type) is t.Union:
            non_none_types = [t for t in t.get_args(target_type) if t != type(None)]
            if non_none_types:
                return cls._convert_value(value, (target_field, non_none_types[0]))

        try:
            custom_parser = target_field.metadata.get("parser")
            if callable(custom_parser):
                return custom_parser(value)
            if target_type == int:
                return int(value)
            if target_type == float:
                return float(value)
            if target_type == bool:
                return str_to_bool(value)
        except Exception as e:
            raise ValueError(f"Cannot convert value '{value}' to type {target_type}") from e

        return value

    @classmethod
    def _fields_and_types(cls) -> t.Dict[str, FieldAndType]:
        fields = {f.name: f for f in dataclasses.fields(cls) if f.name not in LOCKED_CONFIG}
        type_hints = t.get_type_hints(cls)
        return {n: (fields[n], type_hints[n]) for n in fields}

    def to_json(self, exclude_sensitive: bool = True) -> dict:
        result = {}
        for field in dataclasses.fields(self):
            if exclude_sensitive and field.metadata.get("sensitive", False):
                continue
            value = getattr(self, field.name)
            result[field.name] = value.value if isinstance(value, Enum) else value
        return result

    def _get_node_config_value(
        self,
        node_config: t.Union["ModelConfig", "SnapshotConfig", "SeedConfig", "TestConfig"],
        key: str,
    ) -> t.Any:
        """Look up a per-model config key from config.meta, falling back to root-level config.

        Returns None if the key is not found in either location.
        """
        prefixed_key = f"{CONFIG_KEY_PREFIX}{key}"

        # Check meta first to avoid the deprecation warning that newer dbt versions emit
        # when BaseConfig.get() finds a key in meta but not in _extra.
        if hasattr(node_config, "meta_get"):
            value = node_config.meta_get(prefixed_key)
        else:
            value = (getattr(node_config, "meta", None) or {}).get(prefixed_key)
        if value is not None:
            return value
        return node_config.get(prefixed_key)

    def _get_node_config_state_value(
        self, node_config: t.Union[ModelConfig, SnapshotConfig, SeedConfig, TestConfig], key: str
    ) -> t.Optional[t.Any]:
        """Similar to self._get_node_config_value() except looks for the key nested in a 'state' dict in the "extra" fields"""

        state = node_config.extra.get("state")
        if isinstance(state, dict):
            return state.get(key)

        return None

    def resolve_tolerate_nondeterminism(
        self, node_config: t.Union[ModelConfig, SnapshotConfig, TestConfig]
    ) -> bool:
        # `evaluate_volatile_sql` is the logical inverse of `tolerate_nondeterminism`:
        # evaluating volatile SQL means treating non-deterministic functions (e.g. now())
        # as *changing*, i.e. NOT tolerating non-determinism. Negate it accordingly.
        evaluate_volatile_sql = self._get_node_config_state_value(
            node_config, "evaluate_volatile_sql"
        )
        if evaluate_volatile_sql is not None:
            return not to_bool(evaluate_volatile_sql)

        value = self._get_node_config_value(node_config, "tolerate_nondeterminism")
        if value is None:
            return self.tolerate_nondeterminism
        return to_bool(value)

    def resolve_clone_incremental_in_dev(
        self, node_config: t.Union[ModelConfig, SnapshotConfig]
    ) -> CloneIncrementalInDev:
        value = self._get_node_config_state_value(node_config, "pre_clone")
        if value is not None:
            return _parse_clone_incremental_in_dev(value)

        return self.clone_incremental_in_dev

    def resolve_run_hooks_on_no_op(
        self, node_config: t.Union[ModelConfig, SnapshotConfig, SeedConfig, TestConfig]
    ) -> bool:
        value = self._get_node_config_state_value(node_config, "execute_hooks_on_any_reuse")
        if value is None:
            value = self._get_node_config_value(node_config, "run_hooks_on_no_op")
        if value is None:
            return self.run_hooks_on_no_op
        if not isinstance(value, str):
            value = str(value)
        return str_to_bool(value)

    def resolve_freshness_tolerance(
        self, node_config: t.Union[ModelConfig, SnapshotConfig, TestConfig]
    ) -> int:
        if isinstance(node_config, TestConfig):
            # Since tests can run in a separate command invocation from models / snapshots, we cannot accurately
            # determine which upstream changes the test needs to react to vs. which ones it can tolerate. Therefore,
            # we take a conservative approach and disable tolerance to always react to upstream data changes
            return 0
        value = self._get_node_config_state_value(node_config, "lag_tolerance")
        if value is None:
            value = self._get_node_config_value(node_config, "freshness_tolerance")
        if value is None:
            return self.freshness_tolerance
        if isinstance(value, bool):
            raise ValueError(
                f"Invalid run_cache_freshness_tolerance model config value: {value!r}. "
                "Expected int (seconds) or time string (e.g., '30s', '5m')."
            )
        if isinstance(value, int):
            return value
        if isinstance(value, str):
            return _parse_time(value)
        raise ValueError(
            f"Invalid run_cache_freshness_tolerance model config value of type {type(value).__name__}: {value!r}. "
            "Expected int (seconds) or time string (e.g., '30s', '5m')."
        )

    def resolve_stale_upstream_policy(
        self,
        node_config: t.Union[ModelConfig, SnapshotConfig, SeedConfig, TestConfig],
    ) -> shared_models.StaleUpstreamPolicy:
        """Resolve StaleUpstreamPolicy from dbt's native model freshness config.

        Reads freshness.build_after.updates_on from the node config and maps it to
        StaleUpstreamPolicy. Defaults to ANY when the attribute is absent (older dbt
        versions) or not set. Accepts both typed dbt freshness objects (dbt 1.10+)
        and raw dicts that land in `_extra` on older dbt versions where ModelFreshness
        is unknown.
        """

        value = self._get_node_config_state_value(node_config, "require_fresh_data_from")

        if value is None:

            def read(obj: t.Any, key: str) -> t.Any:
                if obj is None:
                    return None
                if isinstance(obj, dict):
                    return obj.get(key)
                return getattr(obj, key, None)

            freshness = node_config.get("freshness")
            build_after = read(freshness, "build_after")
            updates_on = read(build_after, "updates_on")
            if updates_on is None:
                return shared_models.StaleUpstreamPolicy.ANY
            value = updates_on.value if hasattr(updates_on, "value") else str(updates_on)
        else:
            value = str(value)

        if value.lower() == "all":
            return shared_models.StaleUpstreamPolicy.ALL
        return shared_models.StaleUpstreamPolicy.ANY

    @property
    def defer_logging_enabled(self) -> bool:
        return self.defer_log_level.lower() != "off"
