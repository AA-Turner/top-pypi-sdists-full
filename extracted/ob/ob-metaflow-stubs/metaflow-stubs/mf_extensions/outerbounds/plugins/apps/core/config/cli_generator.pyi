######################################################################################################
#                                 Auto-generated Metaflow stub file                                  #
# MF version: 2.15.21.1+obcheckpoint(0.2.4);ob(v1)                                                   #
# Generated on 2025-07-11T23:29:18.599805                                                            #
######################################################################################################

from __future__ import annotations

import typing
if typing.TYPE_CHECKING:
    import metaflow_extensions.outerbounds.plugins.apps.core.config.unified_config

from ......._vendor import click as click
from .unified_config import CoreConfig as CoreConfig
from .config_utils import CLIOption as CLIOption
from .config_utils import ConfigMeta as ConfigMeta
from .config_utils import PureStringKVPairType as PureStringKVPairType
from .config_utils import JsonFriendlyKeyValuePairType as JsonFriendlyKeyValuePairType
from .config_utils import CommaSeparatedListType as CommaSeparatedListType

class CLIGenerator(object, metaclass=type):
    """
    Generates Click CLI options from CoreConfig dataclass.
    """
    def __init__(self, config_class: type = metaflow_extensions.outerbounds.plugins.apps.core.config.unified_config.CoreConfig):
        ...
    def generate_options(self):
        """
        Generate all CLI options from the configuration class.
        """
        ...
    def create_decorator(self, command_type: str = 'deploy') -> callable:
        """
        Create a decorator that applies all CLI options to a command.
        """
        ...
    ...

def auto_cli_options(config_class: type = metaflow_extensions.outerbounds.plugins.apps.core.config.unified_config.CoreConfig, command_type: str = 'deploy'):
    """
    Decorator that automatically adds CLI options from CoreConfig.
    
    Args:
        command_type: Type of command (e.g., "deploy", "list", "delete")
    
    Usage:
        @auto_cli_options("deploy")
        def deploy_command(**kwargs):
            config = CoreConfig.from_cli(kwargs)
            # ... use config
    """
    ...

