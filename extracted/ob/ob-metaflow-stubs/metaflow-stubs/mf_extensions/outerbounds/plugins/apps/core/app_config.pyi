######################################################################################################
#                                 Auto-generated Metaflow stub file                                  #
# MF version: 2.15.21.1+obcheckpoint(0.2.4);ob(v1)                                                   #
# Generated on 2025-07-11T23:29:18.559676                                                            #
######################################################################################################

from __future__ import annotations

import typing
if typing.TYPE_CHECKING:
    import metaflow.mf_extensions.outerbounds.plugins.apps.core.config.unified_config
    import typing

from .config.unified_config import CoreConfig as CoreConfig
from .config.config_utils import MergingNotAllowedFieldsException as MergingNotAllowedFieldsException
from .config.config_utils import ConfigValidationFailedException as ConfigValidationFailedException
from .config.config_utils import RequiredFieldMissingException as RequiredFieldMissingException

CODE_PACKAGE_PREFIX: str

CAPSULE_DEBUG: bool

class classproperty(property, metaclass=type):
    def __get__(self, owner_self, owner_cls):
        ...
    ...

class AppConfigError(Exception, metaclass=type):
    """
    Exception raised when app configuration is invalid.
    """
    ...

class AuthType(object, metaclass=type):
    @classmethod
    def enums(cls):
        ...
    @property
    def default(cls):
        ...
    ...

class AppConfig(object, metaclass=type):
    """
    Class representing an Outerbounds App configuration.
    """
    def __init__(self, core_config: metaflow.mf_extensions.outerbounds.plugins.apps.core.config.unified_config.CoreConfig):
        """
        Initialize configuration from a dictionary.
        """
        ...
    def set_state(self, key, value):
        ...
    def get_state(self, key, default = None):
        ...
    def dump_state(self):
        ...
    def commit(self):
        ...
    def get(self, key: str, default: typing.Any = None) -> typing.Any:
        """
        Get a configuration value by key.
        """
        ...
    def to_json(self):
        ...
    def to_yaml(self):
        ...
    def to_dict(self):
        ...
    @classmethod
    def from_file(cls, file_path: str) -> "AppConfig":
        """
        Create a configuration from a file.
        """
        ...
    @classmethod
    def from_cli(cls, options: typing.Dict[str, typing.Any]):
        ...
    def update_from_cli_options(self, options):
        ...
    ...

