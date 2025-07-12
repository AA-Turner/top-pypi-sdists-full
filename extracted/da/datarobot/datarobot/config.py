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

import os
from typing import Any, cast, Dict, Optional, TYPE_CHECKING, Union

import trafaret as t
from urllib3 import Retry
import yaml

from ._compat import Int, String
from .context import ENABLE_API_CONSUMER_TRACKING_DEFAULT, env_to_bool
from .rest import DataRobotClientConfig

if TYPE_CHECKING:
    from mypy_extensions import TypedDict

    class ConfigDict(TypedDict, total=False):
        """TypedDict for config"""

        token: Optional[str]
        endpoint: Optional[str]
        config_path: Optional[str]
        connect_timeout: Optional[int]
        ssl_verify: Optional[bool]
        max_retries: Optional[Union[int, Retry]]
        token_type: Optional[str]
        default_use_case: Optional[str]
        enable_api_consumer_tracking: Optional[bool]
        trace_context: Optional[str]
        use_tcp_keepalive: Optional[bool]


_file_exists = os.path.isfile

_converter = t.Dict(
    {
        t.Key("endpoint"): String(),
        t.Key("token"): String(),
        t.Key("connect_timeout", optional=True): Int(),
        t.Key("ssl_verify", optional=True): t.Or(t.Bool(), String()),
        t.Key("max_retries", optional=True): Int(),
        t.Key("token_type", optional=True): String(),
        t.Key("default_use_case", optional=True): String(),
        t.Key("enable_api_consumer_tracking", optional=True): t.Bool(),
        t.Key("trace_context", optional=True): String(),
        t.Key("use_tcp_keepalive", optional=True): t.Bool(),
    }
).allow_extra("*")

_fields = {k.to_name or k.name for k in _converter.keys}


def _get_first_non_none_value(*args: Any) -> Union[Any, None]:
    return next((arg for arg in args if arg is not None), None)


# Custom function to get the first non-none value and its source
def _get_value_and_source(*values: Any) -> Union[tuple[Any, int], tuple[None, None]]:
    return next(
        ((value, index) for index, value in enumerate(values) if value is not None), (None, None)
    )


def _config_dict_from_data(data: Dict[str, Any]) -> Dict[str, Any]:
    return {k: v for k, v in _converter.check(data).items() if k in _fields}


def _get_config_file_from_env() -> Optional[str]:
    if "DATAROBOT_CONFIG_FILE" in os.environ:
        config_path = os.environ["DATAROBOT_CONFIG_FILE"]
        expanded_config_path = os.path.expanduser(config_path)
        if os.path.exists(expanded_config_path):
            return expanded_config_path
        else:
            raise ValueError("Environment variable DATAROBOT_CONFIG_FILE points to a missing file")
    return None


def _get_config_dir() -> str:
    return os.path.expanduser("~/.config/datarobot")


def _get_default_config_file() -> Optional[str]:
    first_choice_config_path = os.path.join(_get_config_dir(), "drconfig.yaml")
    if _file_exists(first_choice_config_path):
        return first_choice_config_path
    else:
        return None


def _config_from_env() -> ConfigDict:
    """
    Create and return a DataRobotClientConfig from environment variables. This method only allows
    for configuration of endpoint, token, max retries, and a default use case.
    More advanced configuration must be done through a yaml file.

    Returns
    -------
    config : ConfigDict

    Raises
    ------
    ValueError
        If either of DATAROBOT_ENDPOINT or DATAROBOT_API_TOKEN is not specified as an environment
        variable
    IOError
        If the config file that DATAROBOT_CONFIG_FILE points to does not exist
    """
    endpoint: Optional[str] = os.environ.get("DATAROBOT_ENDPOINT")
    token: Optional[str] = os.environ.get("DATAROBOT_API_TOKEN")
    ssl_verify: Optional[Union[str, bool]] = os.environ.get("DATAROBOT_SSL_VERIFY")
    if ssl_verify is not None:
        ssl_verify = env_to_bool(ssl_verify)
    trace_context: Optional[str] = os.environ.get("DATAROBOT_TRACE_CONTEXT")
    max_retries: Optional[Union[str, int]] = os.environ.get("DATAROBOT_MAX_RETRIES")
    if max_retries is not None:
        max_retries = int(max_retries)
    use_case_id: Optional[str] = os.environ.get("DATAROBOT_DEFAULT_USE_CASE")
    enable_api_consumer_tracking: Optional[Union[str, bool]] = os.environ.get(
        "DATAROBOT_API_CONSUMER_TRACKING_ENABLED"
    )
    if enable_api_consumer_tracking is not None:
        enable_api_consumer_tracking = env_to_bool(enable_api_consumer_tracking)
    use_tcp_keepalive: Optional[Union[str, bool]] = os.environ.get("DATAROBOT_USE_TCP_KEEPALIVE")
    if use_tcp_keepalive is not None:
        use_tcp_keepalive = env_to_bool(use_tcp_keepalive)

    return cast(
        "ConfigDict",
        {
            "endpoint": endpoint,
            "token": token,
            "ssl_verify": ssl_verify,
            "max_retries": max_retries,
            "default_use_case": use_case_id,
            "enable_api_consumer_tracking": enable_api_consumer_tracking,
            "trace_context": trace_context,
            "connect_timeout": None,
            "use_tcp_keepalive": use_tcp_keepalive,
        },
    )


def _config_from_file(config_path: str) -> ConfigDict:
    """
    Create and return a DataRobotClientConfig from a config path. The file must be
    a yaml formatted file

    Parameters
    ----------
    config_path : str
        Path to the configuration file

    Returns
    -------
    config : ConfigDict
    """
    with open(config_path, "rb") as f:
        data: Dict[str, Any] = yaml.load(f, Loader=yaml.SafeLoader)
    return cast("ConfigDict", _config_dict_from_data(data))


# Create client config section
def create_drconfig(
    token: Optional[str] = None,
    endpoint: Optional[str] = None,
    config_path: Optional[str] = None,
    connect_timeout: Optional[int] = None,
    ssl_verify: Optional[bool] = None,
    max_retries: Optional[Union[int, Retry]] = None,
    token_type: Optional[str] = None,
    default_use_case: Optional[str] = None,
    enable_api_consumer_tracking: Optional[bool] = None,
    trace_context: Optional[str] = None,
    use_tcp_keepalive: Optional[bool] = None,
) -> DataRobotClientConfig:
    """
    Create a DataRobotClientConfig object from the provided arguments, from environment
    variables or a config file.

    Notes
    -----
    Token and endpoint must be specified from one source only. This is a restriction
    to prevent token leakage if environment variables or config file are used.

    The DataRobotClientConfig params will be looking up to find the configuration parameters
    in one of the following ways,

      1. From call kwargs if specified;
      2. From a YAML file at the path specified in the ``config_path`` kwarg;
      3. From a YAML file at the path specified in the environment variables ``DATAROBOT_CONFIG_FILE``;
      4. From environment variables;
      5. From the default values in the default YAML file
         at the path `$HOME/.config/datarobot/drconfig.yaml`.

    Parameters
    ----------
    token : Optional[str]
        API token.
    endpoint : Optional[str]
        Base URL of API.
    config_path : Optional[str]
        An alternate location of the config file.
    connect_timeout : Optional[int]
        How long the client should be willing to wait before giving up on establishing
        a connection with the server.
    ssl_verify : bool or Optional[str]
        Whether to check SSL certificate.
        Could be set to path with certificates of trusted certification authorities. Default: True.
    max_retries : int or urllib3.util.retry.Retry, optional
        Either an integer number of times to retry connection errors,
        or a `urllib3.util.retry.Retry` object to configure retries.
    token_type: Optional[str]
        Authentication token type: Token, Bearer.
        "Bearer" is for DataRobot OAuth2 token, "Token" for token generated in Developer Tools.
        Default: "Token".
    default_use_case: Optional[str]
        The entity ID of the default Use Case to use with any requests made by this Client instance.
    enable_api_consumer_tracking: Optional[bool]
        Enable and disable user metrics tracking within the datarobot module. Default: False.
    trace_context: Optional[str]
        An ID or other string for identifying which code template or AI Accelerator was used to make
        a request.
    use_tcp_keepalive : Optional[bool]
        Enable TCP keepalive for the client. If None is set to True. Default: None.

    Returns
    -------
    config : DataRobotClientConfig
    """

    # Validate that if endpoint is specified, token is also specified
    if endpoint and not token:
        raise ValueError("Token must be specified if endpoint is specified")

    env_config = _get_config_file_from_env()
    # If a config path is specified, use that
    if config_path:
        config_path_expanded = os.path.expanduser(config_path)
        if not _file_exists(config_path_expanded):
            raise ValueError(f"Invalid config path - no file at {config_path_expanded}")
        config = _config_from_file(config_path_expanded)
    # If no config path is specified, check for an env var
    elif env_config:
        if not _file_exists(env_config):
            raise ValueError(f"Invalid config path - no file at {env_config}")
        config = _config_from_file(env_config)
    # If no config path is specified, check for a environmet variables config file
    else:
        config = _config_from_env()
    default_config = cast("ConfigDict", {})
    default_config_path = _get_default_config_file()
    if default_config_path is not None:
        default_config = _config_from_file(default_config_path)
    if not config.get("max_retries", None):
        config["max_retries"] = Retry(backoff_factor=0.1, respect_retry_after_header=True)

    token, token_source = _get_value_and_source(
        token, config.get("token"), default_config.get("token")
    )
    endpoint, endpoint_source = _get_value_and_source(
        endpoint, config.get("endpoint"), default_config.get("endpoint")
    )
    # Raise an error if no endpoint or token is specified
    if endpoint is None or token is None:
        e_msg = (
            "No valid configuration found"
            "enpoint and token must be specified"
            "Can be specified via arguments, environment variables or a config file"
        )
        raise ValueError(e_msg)

    # Raise an error if token or endpoint are from different sources
    # This should prevent token leakage
    if token_source != endpoint_source:
        raise ValueError("Endpoint and token must come from the same configuration source")

    ssl_verify = _get_first_non_none_value(
        ssl_verify, config.get("ssl_verify"), default_config.get("ssl_verify")
    )

    max_retries = _get_first_non_none_value(
        max_retries, config.get("max_retries"), default_config.get("max_retries")
    )

    connect_timeout = _get_first_non_none_value(
        connect_timeout,
        config.get("connect_timeout"),
        default_config.get("connect_timeout"),
    )
    token_type = _get_first_non_none_value(
        token_type, config.get("token_type"), default_config.get("token_type", "Token")
    )
    default_use_case = _get_first_non_none_value(
        default_use_case,
        config.get("default_use_case"),
        default_config.get("default_use_case"),
    )
    enable_api_consumer_tracking = _get_first_non_none_value(
        enable_api_consumer_tracking,
        config.get("enable_api_consumer_tracking"),
        default_config.get("enable_api_consumer_tracking", ENABLE_API_CONSUMER_TRACKING_DEFAULT),
    )
    trace_context = _get_first_non_none_value(
        trace_context, config.get("trace_context"), default_config.get("trace_context")
    )

    use_tcp_keepalive = _get_first_non_none_value(
        use_tcp_keepalive, config.get("use_tcp_keepalive"), default_config.get("use_tcp_keepalive")
    )

    return DataRobotClientConfig(
        token=token,
        endpoint=endpoint,
        ssl_verify=ssl_verify if ssl_verify is not None else True,
        max_retries=max_retries,
        connect_timeout=connect_timeout,
        token_type=token_type,
        default_use_case=default_use_case,
        enable_api_consumer_tracking=enable_api_consumer_tracking,
        trace_context=trace_context,
        use_tcp_keepalive=use_tcp_keepalive if use_tcp_keepalive is not None else True,
    )
