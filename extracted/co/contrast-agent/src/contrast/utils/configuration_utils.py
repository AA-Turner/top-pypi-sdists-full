# Copyright © 2025 Contrast Security, Inc.
# See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
from __future__ import annotations
import platform
from enum import Enum, EnumMeta
from functools import lru_cache
import itertools
import os
import socket

from contrast import AGENT_CURR_WORKING_DIR
from contrast.utils.string_utils import truncate
from contrast_vendor.ruamel import yaml

from contrast.agent.protect.rule.mode import Mode

from contrast_vendor import structlog as logging

logger = logging.getLogger("contrast")


CONFIG_LOCATIONS = [
    AGENT_CURR_WORKING_DIR,
    os.path.join(AGENT_CURR_WORKING_DIR, "settings"),
    "/etc/contrast/python/",
    "/etc/contrast/",
    "/etc/",
]

CONFIG_FILE_NAMES = ["contrast_security.yaml", "contrast_security.yml"]

DEFAULT_PATHS = [
    os.path.join(path, filename)
    for path, filename in itertools.product(CONFIG_LOCATIONS, CONFIG_FILE_NAMES)
]
"""
DEFAULT_PATHS are the default locations to search for the config file.

Current order of precedence:
    file specified by CONTRAST_CONFIG_PATH env var
    os.getcwd()
    os.path.join(os.getcwd(), 'settings')
    /etc/contrast/python/
    /etc/contrast/
    /etc/
"""

# Valid options are defined in the spec:
# https://github.com/Contrast-Security-Inc/assess-specifications/blob/master/vulnerability/capture-stacktrace.md
STACKTRACE_OPTIONS = ["ALL", "SOME", "NONE", "SINK"]


@lru_cache(maxsize=1)
def get_hostname() -> str:
    """
    Returns the hostname from the socket or "localhost"
    """
    hostname = "localhost"

    try:
        hostname = socket.gethostname() or hostname
    except Exception as e:
        logger.debug(e)

    return truncate(hostname)


@lru_cache(maxsize=1)
def get_platform():
    try:
        platform_str = platform.platform()
    except Exception:
        try:
            platform_str = platform.platform(terse=True)
        except Exception:
            platform_str = "unknown"

    return platform_str


def load_yaml_config(paths: list[str]) -> list[tuple[dict, str]]:
    """
    Loads yaml files at $CONTRAST_CONFIG_PATH or paths as dictionaries.

    See official documentation because this is valid across agents.

    :return: a list of flattened dict object representation of the yaml config. {'enable': True, ....} and filename pairs
    """
    if filename := os.environ.get("CONTRAST_CONFIG_PATH"):
        if os.path.isfile(filename):
            paths = [filename]
        else:
            logger.warning(
                "The path specified by CONTRAST_CONFIG_PATH is not a file -"
                " searching for configuration file in default locations",
                contrast_config_path=filename,
            )

    configs = [
        (flatten_config(cfg), path)
        for path in paths
        if (cfg := _load_config(path)) is not None
    ]

    return configs


def _load_config(file_path):
    try:
        with open(file_path) as config_file:
            logger.info("Loading configuration file: %s", os.path.abspath(file_path))
            return yaml.YAML(typ="safe", pure=True).load(config_file)
    except yaml.scanner.ScannerError as ex:
        # config yaml cannot be loaded but agent should continue on in case
        # env vars are configured
        msg_prefix = "YAML validator found an error."
        msg = f"{msg_prefix} Configuration path: [{ex.problem_mark.name}]. Line [{ex.problem_mark.line}]. Error: {ex.problem}"
        logger.warning(msg)
    except FileNotFoundError:
        # Most paths are system defaults, so we don't want to log a warning.
        # For the user specified CONTRAST_CONFIG_PATH, warnings are logged
        # in load_yaml_config.
        logger.debug("Configuration file not found: %s", file_path)

    return None


def flatten_config(config) -> dict:
    """
    Convert a nested dict such as
        {'enable': True,
        'application':
            {'name': 'dani-flask'},
        'foo':
        'agent':
            {'python':

    into
        'enable': True,
        'application.name': 'dani-flask',

    :param config: dict config with nested keys and values
    :return: dict, flattened where each key has one value.
    """
    flattened_config = {}

    def flatten(x, name=""):
        if isinstance(x, dict):
            for key in x:
                flatten(x[key], name + key + ".")
        elif x is not None:
            flattened_config[name[:-1]] = x

    flatten(config)
    return flattened_config


def str_to_bool(val) -> bool:
    """
    Converts a str to a bool

    true -> True, false -> False
    """
    if isinstance(val, bool):
        return val
    if not isinstance(val, str):
        return False

    # The remainder of this function was ported from distutils
    val = val.lower()

    if val in ("y", "yes", "t", "true", "on", "1"):
        return True
    if val in ("n", "no", "f", "false", "off", "0"):
        return False
    raise ValueError(f"invalid truth value {val!r}")


def parse_disabled_rules(disabled_rules) -> list[str]:
    if not disabled_rules:
        return []

    return [rule.lower() for rule in disabled_rules.split(",")]


def parse_stacktraces_options(option) -> str:
    option = option.upper()
    if option in STACKTRACE_OPTIONS:
        return option

    return "ALL"


def parse_event_detail_option(option) -> str:
    return "full" if option.lower() == "full" else "minimal"


def str_to_enum(enum: EnumMeta, *, default: Enum | None = None):
    def _str_to_enum(val: str) -> Enum | None:
        if not val:
            return default
        try:
            return enum[val.upper()]
        except KeyError:
            raise ValueError(f"Invalid value for {enum.__name__}: {val}") from None

    return _str_to_enum


def str_to_protect_mode_enum(mode) -> Mode:
    """
    Converts str config value to protect mode enum that the agent understands
    """
    if not mode:
        return Mode.OFF

    return getattr(Mode, mode.upper(), Mode.MONITOR)
