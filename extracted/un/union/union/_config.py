import base64
import os
import sys
import textwrap
from dataclasses import dataclass
from enum import Enum
from functools import partial
from importlib.metadata import version
from os import getenv
from pathlib import Path
from string import Template
from textwrap import dedent
from typing import List, Optional, Tuple, Union

import click
import grpc
from flyteidl.service.identity_pb2 import UserInfoRequest
from flyteidl.service.identity_pb2_grpc import IdentityServiceStub
from flytekit.clients.auth_helper import (
    get_channel,
    upgrade_channel_to_authenticated,
    upgrade_channel_to_proxy_authenticated,
    wrap_exceptions_channel,
)
from flytekit.configuration import AuthType, Config, PlatformConfig, get_config_file
from flytekit.configuration.default_images import DefaultImages

_DEFAULT_GCP_SERVERLESS_ENDPOINT: str = "serverless-1.us-east-2.s.union.ai"
_VANITY_UNION_URLS: dict[str, str] = {
    "serverless.union.ai": _DEFAULT_GCP_SERVERLESS_ENDPOINT,
    "serverless.staging.union.ai": "serverless-gcp.cloud-staging.union.ai",
    "serverless.canary.union.ai": "serverless-preview.canary.unionai.cloud",
}
_SERVERLESS_ENDPOINTS = {
    "serverless-1.us-east-2.s.union.ai",
    "serverless-gcp.cloud-staging.union.ai",
    "utt-srv-staging-1.cloud-staging.union.ai",
    "serverless-preview.canary.unionai.cloud",
    "utt-srv-canary-1.canary.unionai.cloud",
}

_UNION_CONFIG_ENV_VARS: List[str] = ["UNION_CONFIG", "UNIONAI_CONFIG"]
_UNION_SERVERLESS_ENDPOINT_ENV_VAR: str = "UNION_SERVERLESS_ENDPOINT"
_UNION_EAGER_API_KEY_ENV_VAR: str = "_UNION_EAGER_API_KEY"
_UNION_API_KEY_ENV_VARS: List[str] = [
    "UNION_API_KEY",
    "UNION_SERVERLESS_API_KEY",
    "UNIONAI_SERVERLESS_API_KEY",
    _UNION_EAGER_API_KEY_ENV_VAR,
    "_UNION_UNION_API_KEY",
]
_UNION_DEFAULT_CONFIG_PATHS: List[Path] = [
    Path.home() / ".union" / "config.yaml",
    Path.home() / ".uctl" / "config.yaml",
]
_UNION_DEFAULT_CONFIG_PATH: Path = _UNION_DEFAULT_CONFIG_PATHS[0]
_DEFAULT_PROJECT_BYOC: str = "flytesnacks"
_DEFAULT_PROJECT_SERVERLESS: str = "default"
_DEFAULT_DOMAIN: str = "development"


@dataclass
class _UnionConfig:
    org: Optional[str] = None
    is_direct_union_cli_call: bool = False

    # These fields are populated when _get_config_obj is called.
    config_obj: Optional[Config] = None
    config_source: str = ""


_UNION_CONFIG = _UnionConfig()


def _is_serverless_endpoint(endpoint: str) -> bool:
    """Check if endpoint is serverless."""
    return endpoint in (endpoint, f"dns:///{endpoint}") and (
        endpoint in _SERVERLESS_ENDPOINTS or getenv(_UNION_SERVERLESS_ENDPOINT_ENV_VAR)
    )


def _get_image_builder_priority(endpoint: str) -> int:
    """Return image builder priority for union image builder.

    - Serverless gets the highest priority (10)
    - BYOC gets a priority (0) lower than the default OSS image builder (1). This
      keeps backward compatibility.
    """
    return 10 if _is_serverless_endpoint(endpoint) else 0


@dataclass
class AppClientCredentials:
    endpoint: str
    client_id: str
    client_secret: str
    org: str


def _encode_app_client_credentials(app_credentials: AppClientCredentials) -> str:
    """Encode app_credentials with base64."""
    data = (
        f"{app_credentials.endpoint}:{app_credentials.client_id}:{app_credentials.client_secret}:{app_credentials.org}"
    )
    return base64.b64encode(data.encode("utf-8")).decode("utf-8")


def _decode_app_client_credentials(encoded_str: str) -> AppClientCredentials:
    """Decode encoded base64 string into app credentials."""
    endpoint, client_id, client_secret, org = base64.b64decode(encoded_str.encode("utf-8")).decode("utf-8").split(":")
    # In byoc, the org is encoded as the 'None' string which we want to marshal back to a proper None type.
    if org == "None" or not _is_serverless_endpoint(endpoint):
        org = None
    return AppClientCredentials(endpoint=endpoint, client_id=client_id, client_secret=client_secret, org=org)


def _clean_endpoint(endpoint: str) -> str:
    """Clean endpoint."""
    prefixes = ("dns:///", "http://", "https://")

    for prefix in prefixes:
        if endpoint.startswith(prefix):
            n_prefix = len(prefix)
            endpoint = endpoint[n_prefix:]
            break

    return endpoint.rstrip("/")


def _get_endpoint_for_login(*, host: Optional[str] = None, serverless: bool = False) -> str:
    """Get endpoint for login."""
    if host is None and not serverless:
        msg = "--host HOST or --serverless must be passed in for login"
        raise click.ClickException(msg)

    if host is not None and serverless:
        msg = "Can not pass in both --host and --serverless for login, please choose one"
        raise click.ClickException(msg)

    if serverless:
        host = getenv(_UNION_SERVERLESS_ENDPOINT_ENV_VAR, default=_DEFAULT_GCP_SERVERLESS_ENDPOINT)

    endpoint = _clean_endpoint(host)

    if endpoint in _VANITY_UNION_URLS:
        return _VANITY_UNION_URLS[endpoint]
    return endpoint


def _get_env_var(env_vars: List[str]) -> Tuple[Optional[str], Optional[str]]:
    """Get environment variable from a list of env_vars."""
    for env_var in env_vars:
        if env_var in os.environ:
            return os.environ[env_var], env_var
    return None, None


def _get_config_path(config_paths: List[Path] = _UNION_DEFAULT_CONFIG_PATHS) -> Optional[Path]:
    """Get configuration path."""
    for path in config_paths:
        if path.exists():
            return path
    return None


_get_union_config_env_var = partial(_get_env_var, env_vars=_UNION_CONFIG_ENV_VARS)
_get_union_api_env_var = partial(_get_env_var, env_vars=_UNION_API_KEY_ENV_VARS)


def _check_yaml_config_is_empty(config_file: Union[str, os.PathLike]):
    with open(config_file, "r") as f:
        contents = f.read().strip()

    if not contents:
        raise click.ClickException(
            f"Unable to load yaml at {config_file} because it is empty. Delete file or pass a config that is not empty"
        )


def _decode_union_api_key(serverless_api_value: str) -> Config:
    """Decode union serverless api key and return Config."""
    config = Config.auto()
    try:
        app_credentials = _decode_app_client_credentials(serverless_api_value)
    except Exception as e:
        raise ValueError("Unable to read UNION_API_KEY") from e

    if _UNION_CONFIG.org is None and app_credentials.org != "":
        _UNION_CONFIG.org = app_credentials.org

    return config.with_params(
        platform=PlatformConfig(
            endpoint=app_credentials.endpoint,
            insecure=False,
            auth_mode=AuthType.CLIENTSECRET,
            client_id=app_credentials.client_id,
            client_credentials_secret=app_credentials.client_secret,
        )
    )


def _should_default_to_union_semantics() -> bool:
    return bool(_UNION_CONFIG.is_direct_union_cli_call or os.getenv(_UNION_EAGER_API_KEY_ENV_VAR))


class ConfigSource(Enum):
    CLI = "--config passed in"
    REMOTE = "Set by Remote"


@dataclass
class ConfigWithSource:
    config: Union[Config, str]
    source: ConfigSource


def _get_config_obj(
    config_in: Optional[Union[str, ConfigWithSource]] = None, default_to_union_semantics: bool = False
) -> Config:
    """Get Config object.

    If `config_in` is not None, then it will be used as the Config file.

    If the `union` CLI is called directly or `default_to_union_semantics=True`, then the config_in is set
    in the following order:
        1. `UNION_SERVERLESS_ENDPOINT` environment variable (Used for development)
        2. `UNION_SERVERLESS_API_KEY` environment variable
        3. `UNION_CONFIG` environment variable
        4. ~/.union/config.yaml if it exists

    If `pyflyte` CLI is called and `flytekit`'s `get_config_file` did not return a `ConfigFile`,
    then serverless it the default endpoint.
    """
    default_to_union_semantics = default_to_union_semantics or _should_default_to_union_semantics()

    config_out = None
    if config_in is not None:
        if isinstance(config_in, str):
            config_out = Config.auto(config_in)
        else:  # ConfigWithSource object
            if isinstance(config_in.config, str):
                config_out = Config.auto(config_in.config)
            else:  # Config object
                config_out = config_in.config
            _UNION_CONFIG.config_source = config_in.source.value

    elif _UNION_CONFIG.config_obj is not None and _UNION_CONFIG.config_source == ConfigSource.CLI.value:
        # Config came from --config, it will have the highest precedence.
        config_out = _UNION_CONFIG.config_obj

    elif default_to_union_semantics:
        if (endpoint := getenv(_UNION_SERVERLESS_ENDPOINT_ENV_VAR)) is not None:
            # If UNION_SERVERLESS_ENDPOINT is set in `_UnionConfig`, use it instead
            _UNION_CONFIG.config_source = f"{_UNION_SERVERLESS_ENDPOINT_ENV_VAR} env variable"
            config_out = Config.for_endpoint(endpoint=endpoint)

        elif (api_value_tuple := _get_union_api_env_var()) and (api_value_tuple[0] not in ("", None)):
            _UNION_CONFIG.config_source = f"{api_value_tuple[1]} env variable"
            config_out = _decode_union_api_key(api_value_tuple[0])

        elif (api_config_tuple := _get_union_config_env_var()) and (api_config_tuple[0] not in ("", None)):
            _UNION_CONFIG.config_source = f"{api_config_tuple[1]} env variable"
            config_out = Config.auto(api_config_tuple[0])

        elif (config_path := _get_config_path()) is not None:
            # Check if config is empty:
            _check_yaml_config_is_empty(config_path)
            # Read config from file system
            _UNION_CONFIG.config_source = f"{config_path} file"
            config_out = Config.auto(str(config_path.absolute()))

    elif _UNION_CONFIG.config_obj is not None and _UNION_CONFIG.config_source == ConfigSource.REMOTE.value:
        # Configured through remote, use this configuration if none of the automatic configurations are found
        config_out = _UNION_CONFIG.config_obj

    if config_out is None:
        # Raise union config error if directly called by CLI or default_to_union_semantics
        is_local_cli = os.getenv("FLYTE_INTERNAL_EXECUTION_ID") is None

        if is_local_cli and default_to_union_semantics:
            msg = dedent("""\
            Please login to Union.

            - On Union Serverless run: `union create login --serverless`
            - On Union BYOC run: `union create login --host UNION_TENANT`

            You can also pass a configuration with `union --config` or set UNION_CONFIG.\
            """)
            from union._exceptions import UnionRequireConfigException

            raise UnionRequireConfigException(msg)

        # Otherwise, try flyte configuration
        cfg_file = get_config_file(config_in)

        if cfg_file is None:
            if is_local_cli:
                from union._exceptions import UnionRequireConfigException

                msg = dedent("""\
                Please configure pyflyte with FLYTECTL_CONFIG or pass in --config.

                Alternatively, use the union CLI and login with `union create login`:

                - On Union Serverless run: `union create login --serverless`
                - On Union BYOC run: `union create login --host UNION_TENANT`\
                """)
                raise UnionRequireConfigException(msg)
            config_out = Config.for_sandbox()
        else:
            config_out = Config.auto(cfg_file)

    _UNION_CONFIG.config_obj = config_out
    return config_out


def _config_from_api_key(api_key: str) -> Config:
    """Get config from api key."""
    config_out = _decode_union_api_key(api_key)

    _UNION_CONFIG.config_source = "manual API key"
    _UNION_CONFIG.config_obj = config_out
    return config_out


def _get_organization(platform_config: PlatformConfig, channel: Optional[grpc.Channel] = None) -> Optional[str]:
    """Get organization based on endpoint."""
    if _UNION_CONFIG.org is not None:
        return _UNION_CONFIG.org
    elif _is_serverless_endpoint(platform_config.endpoint):
        org = _get_user_handle(platform_config, channel)
        _UNION_CONFIG.org = org
        return org
    else:
        # Managed+ users, the org is not required for requests and we set it None
        # to replicate default flytekit behavior.
        return None


def _get_user_handle(platform_config: PlatformConfig, channel: Optional[grpc.Channel] = None) -> str:
    """Get user_handle for PlatformConfig."""
    if channel is None:
        channel = _get_authenticated_channel(platform_config)

    client = IdentityServiceStub(channel)
    user_info = client.UserInfo(UserInfoRequest())
    user_handle = user_info.additional_claims.fields["userhandle"]
    return user_handle.string_value


def _get_authenticated_channel(platform_config: PlatformConfig, **kwargs) -> grpc.Channel:
    """
    Get an authenticated channel based on the platform config.

    :param platform_config: PlatformConfig object to define the connection settings (endpoint, auth_type, etc.)

    :return: grpc.Channel
    """
    return wrap_exceptions_channel(
        platform_config,
        upgrade_channel_to_authenticated(
            platform_config,
            upgrade_channel_to_proxy_authenticated(platform_config, get_channel(platform_config, **kwargs)),
        ),
    )


def _get_default_image() -> str:
    """Get default image version."""
    from union._exceptions import UnionRequireConfigException

    try:
        cfg_obj = _get_config_obj(default_to_union_semantics=False)

        # TODO: This is only temporary to support GCP endpoints. When the union images are public,
        # we will always use union images
        endpoint = cfg_obj.platform.endpoint
        if _is_serverless_endpoint(endpoint):
            major, minor = sys.version_info.major, sys.version_info.minor
            union_version = version("union")
            if "dev" in union_version:
                suffix = "latest"
            else:
                suffix = union_version

            return f"cr.union.ai/v1/unionai/union:py{major}.{minor}-{suffix}"
        else:
            return DefaultImages().find_image_for()

    except UnionRequireConfigException:
        return DefaultImages().find_image_for()


def _write_config_to_path(endpoint: str, auth_type: str, config_path: Path = _UNION_DEFAULT_CONFIG_PATH):
    """Write config to config directory."""
    config_dir = config_path.parent
    config_dir.mkdir(exist_ok=True, parents=True)

    config_template = Template(
        textwrap.dedent(
            """\
    admin:
      endpoint: $endpoint
      insecure: false
      authType: $auth_type
    logger:
      show-source: true
      level: 0
    union:
      connection:
        host: $endpoint
        insecure: false
      auth:
        type: $auth_type
    """
        )
    )
    config_path.write_text(config_template.substitute(endpoint=f"dns:///{endpoint}", auth_type=auth_type))
    return config_path


def _get_default_project(previous_default: str, cfg_obj: Optional[Config] = None) -> str:
    from union._exceptions import UnionRequireConfigException

    try:
        if cfg_obj is None:
            cfg_obj = _get_config_obj()
        if _is_serverless_endpoint(cfg_obj.platform.endpoint):
            return _DEFAULT_PROJECT_SERVERLESS
    except UnionRequireConfigException:
        return previous_default

    return previous_default


class _GetDefaultProject:
    """Give a better repr when calling _get_default_project from the CLI"""

    def __init__(self, previous_default: str):
        self.previous_default = previous_default

    def __call__(self):
        return _get_default_project(previous_default=self.previous_default)

    def __repr__(self):
        return "default or flytesnacks"


def _get_auth_success_html(endpoint: str) -> str:
    """Get default success html. Return None to use flytekit's default success html."""
    if endpoint.endswith(("union.ai", "unionai.cloud")):
        SUCCESS_HTML = textwrap.dedent(
            """
        <html>
        <head>
            <title>OAuth2 Authentication to Union Successful</title>
        </head>
        <body style="background:white;font-family:Arial">
            <div style="position: absolute;top:40%;left:50%;transform: translate(-50%, -50%);text-align:center;">
                <div style="margin:auto">
                    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 300 65" fill="currentColor"
                        style="color:#fdb51e;width:360px;">
                        <title>Union.ai</title>
                        <path d="M32,64.8C14.4,64.8,0,51.5,0,34V3.6h17.6v41.3c0,1.9,1.1,3,3,3h23c1.9,0,3-1.1,3-3V3.6H64V34
                        C64,51.5,49.6,64.8,32,64.8z M69.9,30.9v30.4h17.6V20c0-1.9,1.1-3,3-3h23c1.9,0,3,1.1,3,3v41.3H134V30.9c0-17.5-14.4-30.8-32.1-30.8
                        S69.9,13.5,69.9,30.9z M236,30.9v30.4h17.6V20c0-1.9,1.1-3,3-3h23c1.9,0,3,1.1,3,3v41.3H300V30.9c0-17.5-14.4-30.8-32-30.8
                        S236,13.5,236,30.9L236,30.9z M230.1,32.4c0,18.2-14.2,32.5-32.2,32.5s-32-14.3-32-32.5s14-32.1,32-32.1S230.1,14.3,230.1,32.4
                        L230.1,32.4z M213.5,20.2c0-1.9-1.1-3-3-3h-24.8c-1.9,0-3,1.1-3,3v24.5c0,1.9,1.1,3,3,3h24.8c1.9,0,3-1.1,3-3V20.2z M158.9,3.6
                        h-17.6v57.8h17.6V3.6z"></path>
                    </svg>
                    <h2>You've successfully authenticated to Union!</h2>
                    <p style="font-size:20px;">Return to your terminal for next steps</p>
                </div>
            </div>
        </body>
        </html>
        """  # noqa: E501
        )
        return SUCCESS_HTML
    return None
