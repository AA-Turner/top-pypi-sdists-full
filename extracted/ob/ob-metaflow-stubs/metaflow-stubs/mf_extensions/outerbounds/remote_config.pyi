######################################################################################################
#                                 Auto-generated Metaflow stub file                                  #
# MF version: 2.15.17.1+obcheckpoint(0.2.1);ob(v1)                                                   #
# Generated on 2025-06-16T20:11:02.911895                                                            #
######################################################################################################

from __future__ import annotations

import typing
if typing.TYPE_CHECKING:
    import pathlib

from ...exception import MetaflowException as MetaflowException
from ...plugins.perimeters import get_perimeter_config_url_if_set_in_ob_config as get_perimeter_config_url_if_set_in_ob_config

OBP_REMOTE_CONFIG_KEY: str

HOSTNAME_KEY: str

AUTH_KEY: str

PERIMETER_KEY: str

CONFIG_READ_ONCE_KEY: str

def read_config_from_local() -> typing.Optional[pathlib.Path]:
    ...

def resolve_config_from_remote(remote_url: str, auth_token: str) -> typing.Dict[str, str]:
    ...

def init_config() -> typing.Dict[str, str]:
    """
    OSS Metaflow reads the config file on every step initialization. This is because OSS assumes config files change
    relatively infrequently. We want to avoid config values changing between flow steps. Our solution to prevent this
    is to read a config once and cache it on an environment variable. Environment variables carry over between steps
    because steps are executed in subprocesses (local) or environments which expect environment variables to be set.
    """
    ...

DEBUG_CONFIG: None

def reload_config():
    """
    This function is used to reload the config. Currently its a best effort implementation
    that will only reload auth token.
    """
    ...

