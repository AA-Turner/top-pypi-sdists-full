#
# Copyright 2021-2025 DataRobot, Inc. and its affiliates.
#
# All rights reserved.
#
# DataRobot, Inc.
#
# This is proprietary source code of DataRobot, Inc. and its
# affiliates.
#
# Released under the terms of DataRobot Tool and Utility Agreement.
from __future__ import annotations

from enum import Enum
import json
import os
from pathlib import Path
from typing import Any, Dict, Mapping, Optional, Tuple, Type, Union, cast

from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic_settings.sources import EnvSettingsSource, PydanticBaseSettingsSource

from datarobot.utils.deprecation import deprecation_warning

# Support both old and new locations of parse_env_vars
try:
    # Older versions (< 2.3.0) have parse_env_vars in pydantic_settings.sources
    from pydantic_settings.sources import parse_env_vars  # type: ignore[attr-defined,unused-ignore]
except ImportError:
    # Newer versions have it in pydantic_settings.sources.utils
    from pydantic_settings.sources.utils import parse_env_vars  # type: ignore[no-redef,unused-ignore]

_RuntimeParamPayload = Union[str, float, bool, None]

DEFAULT_DATAROBOT_ENDPOINT = "https://app.datarobot.com/api/v2"
DEFAULT_MODEL_NAME_FOR_DEPLOYED_LLM = "datarobot-deployed-llm"
DEFAULT_LLM_NAME = "llm"


def getenv(name: str, default: Optional[str] = None) -> _RuntimeParamPayload:
    """
    Custom getenv function that checks for Runtime Parameters first.
    """
    rt_name = f"MLOPS_RUNTIME_PARAM_{name}"

    raw = os.getenv(rt_name)

    if raw is None:
        return os.getenv(name, default)

    try:
        value = json.loads(raw)
    except json.JSONDecodeError:
        # not a json, but some primitive type, so return it right away
        return raw

    if isinstance(value, dict):
        if value.get("type") in ("string", "boolean", "numeric", "deployment"):
            return cast(_RuntimeParamPayload, value["payload"])
        if len(value) == 1:
            return str(list(value.values())[0])
        elif "payload" in value:
            payload = value["payload"]
            if isinstance(payload, dict) and "apiToken" in payload:
                return str(payload["apiToken"])

    return raw


# Two per-LLM runtime parameters were renamed into the `{instance}_` namespace:
# `NIM_DEPLOYMENT_ID` and `USE_DATAROBOT_LLM_GATEWAY`. Deployments created before the
# rename still set the bare names, which are no longer declared fields and so are
# dropped by `extra="ignore"`; they can only be read straight from the environment.
# The two helpers below let `resolve_llm_config` do that as a fallback, and are meant
# to be removed along with it once those deployments are gone.


def _coerce_bool(value: object) -> bool:
    """Coerce a runtime-parameter value (a bool, or a ``"1"``/``"0"`` string) to a bool."""
    if isinstance(value, bool):
        return value
    return str(value).strip().lower() in {"1", "true", "t", "yes", "y", "on"}


def _deprecated_param(old_name: str, new_name: str) -> _RuntimeParamPayload:
    """Read a param from its pre-rename name, warning when it is there and ``None`` when not."""
    old_value = getenv(old_name)
    if old_value is None:
        return None
    deprecation_warning(
        subject=old_name,
        deprecated_since_version="3.19",
        will_remove_version="3.21",
        message=(f"Rename this runtime parameter to `{new_name}`. Falling back to the deprecated value for now."),
    )
    return old_value


class PulumiConfigSettingsSource(EnvSettingsSource):  # type: ignore[misc,unused-ignore]
    """A source class that takes settings from a pulumi_config.json file."""

    def __init__(
        self,
        settings_cls: Type[BaseSettings],
        pulumi_config_file: Optional[str] = None,
        pulumi_config_file_encoding: Optional[str] = None,
        **kwargs: Any,
    ):
        self.pulumi_config_file = pulumi_config_file
        self.pulumi_config_file_encoding = pulumi_config_file_encoding
        super().__init__(settings_cls, **kwargs)

    def _find_config_file(self, config_file: str) -> Optional[Path]:
        """Find config file by searching up the directory tree like .env files."""
        config_path = Path(config_file)

        # If it's an absolute path, just return it if it exists
        if config_path.is_absolute():
            return config_path if config_path.is_file() else None

        # Search from current directory up to root
        cwd = Path.cwd()
        for path in [cwd, *cwd.parents]:
            potential_path = path / config_file
            if potential_path.is_file():
                return potential_path

        return None

    def _load_env_vars(self) -> Mapping[str, Optional[str]]:
        """Load environment variables with pulumi config values as fallback."""
        # Get normal environment variables first
        env_vars = dict(super()._load_env_vars())

        # Load pulumi config and add to env_vars (not os.environ)
        pulumi_config_file = self.pulumi_config_file or "pulumi_config.json"
        pulumi_config_path = self._find_config_file(pulumi_config_file)

        if pulumi_config_path is not None:
            encoding = self.pulumi_config_file_encoding or "utf-8"
            with open(pulumi_config_path, encoding=encoding) as f:
                file_data = json.load(f)

            if isinstance(file_data, dict):
                # Add pulumi config values for each field (only if not already in env)
                for field_name in self.settings_cls.model_fields.keys():
                    env_key = field_name.upper()

                    # Skip if already set in environment
                    if env_key in env_vars and env_vars[env_key]:
                        continue

                    value = None
                    if field_name in file_data:
                        value = file_data[field_name]
                    elif env_key in file_data:
                        value = file_data[env_key]

                    if value is not None and value != "":
                        env_vars[env_key] = str(value)

        return parse_env_vars(  # type: ignore[no-any-return,unused-ignore]
            env_vars,
            self.case_sensitive,
            self.env_ignore_empty,
            self.env_parse_none_str,
        )

    def __repr__(self) -> str:
        return (
            f"PulumiConfigSettingsSource("
            f"pulumi_config_file={self.pulumi_config_file!r}, "
            f"pulumi_config_file_encoding={self.pulumi_config_file_encoding!r})"
        )


class GetenvSettingsSource(EnvSettingsSource):  # type: ignore[misc,unused-ignore]
    """A source class that uses the custom getenv function."""

    def _load_env_vars(self) -> Mapping[str, Optional[str]]:
        """Load environment variables using the custom getenv function."""
        # Start with normal environment variables
        env_vars: Dict[str, _RuntimeParamPayload] = dict(super()._load_env_vars())

        # Override with custom getenv for each field
        for field_name in self.settings_cls.model_fields.keys():
            env_key = field_name.upper()
            value = getenv(env_key)
            if value is not None and value != "":
                env_vars[env_key] = value

        return parse_env_vars(  # type: ignore[no-any-return,unused-ignore]
            env_vars,
            self.case_sensitive,
            self.env_ignore_empty,
            self.env_parse_none_str,
        )

    def __repr__(self) -> str:
        return "GetenvSettingsSource()"


class DataRobotAppFrameworkBaseSettings(BaseSettings):  # type: ignore[misc,unused-ignore]
    """
    Base settings class that reads each setting from the first source that defines it:

    1. Environment variables, including runtime parameters
    2. The ``.env`` file
    3. File secrets
    4. ``pulumi_config.json`` (fallback)

    However a variable is set, it is picked up, so the same settings class works both
    locally and once deployed in DataRobot. This covers credentials and plain variables
    for runtime parameters in both custom applications and custom models.

    Examples
    --------
    .. code-block:: python

        class Config(DataRobotAppFrameworkBaseSettings):
            my_variable: str = "default_value"
            another_variable: Optional[int]


        config = Config()
        assert config.my_variable == "value_from_env_or_pulumi_or_default"
    """

    @classmethod
    def settings_customise_sources(
        cls,
        settings_cls: Type[BaseSettings],
        init_settings: PydanticBaseSettingsSource,
        env_settings: PydanticBaseSettingsSource,
        dotenv_settings: PydanticBaseSettingsSource,
        file_secret_settings: PydanticBaseSettingsSource,
    ) -> Tuple[PydanticBaseSettingsSource, ...]:
        return (
            init_settings,
            env_settings,
            GetenvSettingsSource(settings_cls),
            dotenv_settings,
            file_secret_settings,
            PulumiConfigSettingsSource(settings_cls),
        )

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore",
    )

    def resolve_datarobot_endpoint(self) -> str:
        """Resolve the DataRobot endpoint from this config, or fall back to the public default."""
        # This base class declares no fields of its own, so the resolvers read the
        # subclass's fields through `getattr` with a default.
        endpoint = getattr(self, "datarobot_endpoint", None)
        return endpoint or DEFAULT_DATAROBOT_ENDPOINT

    def resolve_datarobot_api_token(self) -> Optional[str]:
        """Resolve the DataRobot API token from this config, treating an empty value as unset."""
        return getattr(self, "datarobot_api_token", None) or None

    def resolve_llm_config(self, name: str = DEFAULT_LLM_NAME) -> "LLMConfig":
        """Build the config for one named LLM instance from this settings object.

        Call this once per configured LLM to support more than one LLM in a single app.

        Parameters
        ----------
        name : str
            Name of the LLM component instance, used as the prefix of its
            ``{name}_*`` fields. Defaults to ``"llm"``.

        Returns
        -------
        LLMConfig
            That instance's routing fields, combined with the endpoint and API token
            resolved from this config.

        Notes
        -----
        Two routing fields fall back to their pre-rename bare parameter names,
        ``NIM_DEPLOYMENT_ID`` and ``USE_DATAROBOT_LLM_GATEWAY``, when the namespaced
        ``{name}_*`` field was not set explicitly. That keeps deployments created before
        the rename working, warns when it happens, and is meant to be removed later.
        """
        nim_deployment_id = getattr(self, f"{name}_nim_deployment_id", None)
        use_datarobot_llm_gateway = getattr(self, f"{name}_use_datarobot_llm_gateway", True)

        # `model_fields_set` distinguishes an explicitly-provided value from a default,
        # so the deprecated bare name is only consulted when the namespaced field was
        # left alone. That check is what makes the bool work, since its default is truthy.
        fields_set = self.model_fields_set
        if f"{name}_nim_deployment_id" not in fields_set:
            legacy = _deprecated_param("NIM_DEPLOYMENT_ID", f"{name.upper()}_NIM_DEPLOYMENT_ID")
            if legacy is not None:
                nim_deployment_id = str(legacy)
        if f"{name}_use_datarobot_llm_gateway" not in fields_set:
            legacy = _deprecated_param("USE_DATAROBOT_LLM_GATEWAY", f"{name.upper()}_USE_DATAROBOT_LLM_GATEWAY")
            if legacy is not None:
                use_datarobot_llm_gateway = _coerce_bool(legacy)

        return LLMConfig(
            datarobot_endpoint=self.resolve_datarobot_endpoint(),
            datarobot_api_token=self.resolve_datarobot_api_token(),
            llm_deployment_id=getattr(self, f"{name}_deployment_id", None),
            llm_nim_deployment_id=nim_deployment_id,
            llm_use_datarobot_llm_gateway=use_datarobot_llm_gateway,
            llm_default_model=getattr(self, f"{name}_default_model", None),
        )


class LLMType(str, Enum):
    """How an :class:`LLMConfig` routes its requests."""

    GATEWAY = "gateway"
    DEPLOYMENT = "deployment"
    NIM = "nim"
    EXTERNAL = "external"


_DATAROBOT_MODEL_PREFIX = "datarobot/"
_API_V2_SUFFIX = "/api/v2"


def _with_datarobot_prefix(model_name: str) -> str:
    if model_name.startswith(_DATAROBOT_MODEL_PREFIX):
        return model_name
    return _DATAROBOT_MODEL_PREFIX + model_name


def _without_datarobot_prefix(model_name: str) -> str:
    if model_name.startswith(_DATAROBOT_MODEL_PREFIX):
        return model_name[len(_DATAROBOT_MODEL_PREFIX) :]
    return model_name


def deployment_url(deployment_id: str, datarobot_endpoint: str) -> str:
    return f"{datarobot_endpoint}/deployments/{deployment_id}/chat/completions"


def llm_gateway_url(datarobot_endpoint: str) -> str:
    if datarobot_endpoint.endswith(_API_V2_SUFFIX):
        return datarobot_endpoint[: -len(_API_V2_SUFFIX)]
    return datarobot_endpoint


class LLMConfig(BaseModel):
    """Resolved connection parameters for a single LLM instance.

    An app can hold one of these per configured LLM. Each carries the routing fields
    for its own LLM plus a copy of the DataRobot endpoint and API token, so building
    a client from it never requires reading a global config.

    Attributes
    ----------
    datarobot_endpoint : str or None
        DataRobot API endpoint. Defaults to ``DEFAULT_DATAROBOT_ENDPOINT`` when unset.
    datarobot_api_token : str or None
        DataRobot API token used to authenticate LLM requests.
    llm_deployment_id : str or None
        ID of the deployment serving the LLM, when routing to a deployment.
    llm_nim_deployment_id : str or None
        ID of the deployment serving a NIM model, when routing to a NIM.
    llm_use_datarobot_llm_gateway : bool
        Whether to route through the DataRobot LLM gateway. Takes precedence over both
        deployment IDs. Defaults to ``True``.
    llm_default_model : str or None
        Model name to request. Defaults to ``DEFAULT_MODEL_NAME_FOR_DEPLOYED_LLM``.

    Notes
    -----
    This is intentionally a plain model rather than a
    :class:`DataRobotAppFrameworkBaseSettings` subclass. The settings class is the
    single app-wide source of configuration, so keeping ``LLMConfig`` separate is what
    lets one app configure several LLMs, including fallbacks.
    """

    datarobot_endpoint: Optional[str] = None
    datarobot_api_token: Optional[str] = None
    llm_deployment_id: Optional[str] = None
    llm_nim_deployment_id: Optional[str] = None
    llm_use_datarobot_llm_gateway: bool = True
    llm_default_model: Optional[str] = None

    def get_llm_type(self) -> LLMType:
        """Report which route this config uses, checking the routing fields in precedence order."""
        if self.llm_use_datarobot_llm_gateway:
            return LLMType.GATEWAY
        elif self.llm_deployment_id:
            return LLMType.DEPLOYMENT
        elif self.llm_nim_deployment_id:
            return LLMType.NIM
        else:
            return LLMType.EXTERNAL

    def to_litellm_params(self) -> Dict[str, Any]:
        """Render this config as a ``litellm_params`` entry for a ``litellm.Router`` model list.

        Returns
        -------
        dict
            The ``litellm`` connection parameters: ``model``, ``api_key``, and, for every
            route other than an external provider, ``api_base``.
        """
        api_key = self.datarobot_api_token
        endpoint = self.datarobot_endpoint or DEFAULT_DATAROBOT_ENDPOINT
        model_name = self.llm_default_model or DEFAULT_MODEL_NAME_FOR_DEPLOYED_LLM
        llm_type = self.get_llm_type()

        if llm_type == LLMType.GATEWAY:
            return {
                "model": _with_datarobot_prefix(model_name),
                "api_base": llm_gateway_url(endpoint),
                "api_key": api_key,
            }
        elif llm_type == LLMType.DEPLOYMENT:
            # get_llm_type only returns DEPLOYMENT when this field is set, but that
            # narrowing does not survive the call, so assert it for mypy.
            assert self.llm_deployment_id is not None
            return {
                "model": _with_datarobot_prefix(model_name),
                "api_base": deployment_url(self.llm_deployment_id, endpoint),
                "api_key": api_key,
            }
        elif llm_type == LLMType.NIM:
            assert self.llm_nim_deployment_id is not None
            return {
                "model": _with_datarobot_prefix(model_name),
                "api_base": deployment_url(self.llm_nim_deployment_id, endpoint),
                "api_key": api_key,
            }
        else:  # EXTERNAL
            return {
                "model": _without_datarobot_prefix(model_name),
                "api_key": api_key,
            }
