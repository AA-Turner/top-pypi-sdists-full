######################################################################################################
#                                 Auto-generated Metaflow stub file                                  #
# MF version: 2.15.17.1+obcheckpoint(0.2.1);ob(v1)                                                   #
# Generated on 2025-06-16T20:11:02.882399                                                            #
######################################################################################################

from __future__ import annotations


from ._vendor import click as click
from . import parameters as parameters
from . import plugins as plugins
from .cli_components.utils import LazyGroup as LazyGroup
from .cli_components.utils import LazyPluginCommandCollection as LazyPluginCommandCollection
from .exception import CommandException as CommandException
from .exception import MetaflowException as MetaflowException
from .metaflow_current import current as current
from .pylint_wrapper import PyLint as PyLint
from .user_configs.config_options import LocalFileInput as LocalFileInput
from .user_configs.config_options import config_options as config_options
from .user_configs.config_parameters import ConfigValue as ConfigValue
from .cli_components.utils import cli as cli
from .cli_components.utils import start as start

DEFAULT_DATASTORE: str

DEFAULT_DECOSPECS: str

DEFAULT_ENVIRONMENT: str

DEFAULT_EVENT_LOGGER: str

DEFAULT_METADATA: str

DEFAULT_MONITOR: str

DEFAULT_PACKAGE_SUFFIXES: str

DATASTORES: list

ENVIRONMENTS: list

LOGGING_SIDECARS: dict

METADATA_PROVIDERS: list

MONITOR_SIDECARS: dict

ERASE_TO_EOL: str

HIGHLIGHT: str

INDENT: str

LOGGER_TIMESTAMP: str

LOGGER_COLOR: str

LOGGER_BAD_COLOR: str

def echo_dev_null(*args, **kwargs):
    ...

def echo_always(line, **kwargs):
    ...

def logger(body = '', system_msg = False, head = '', bad = False, timestamp = True, nl = True):
    ...

def print_metaflow_exception(ex):
    ...

def print_unknown_exception(ex):
    ...

class CliState(object, metaclass=type):
    def __init__(self, flow):
        ...
    ...

def main(flow, args = None, handle_exceptions = True, entrypoint = None):
    ...

