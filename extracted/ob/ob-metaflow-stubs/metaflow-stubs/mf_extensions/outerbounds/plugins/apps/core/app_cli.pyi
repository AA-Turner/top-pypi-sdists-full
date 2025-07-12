######################################################################################################
#                                 Auto-generated Metaflow stub file                                  #
# MF version: 2.15.21.1+obcheckpoint(0.2.4);ob(v1)                                                   #
# Generated on 2025-07-11T23:29:18.567193                                                            #
######################################################################################################

from __future__ import annotations

import metaflow
import typing
if typing.TYPE_CHECKING:
    import metaflow._vendor.click.types
    import metaflow.mf_extensions.outerbounds.plugins.apps.core.app_cli

from ......_vendor import click as click
from .app_config import AppConfig as AppConfig
from .app_config import AppConfigError as AppConfigError
from .app_config import AuthType as AuthType
from .config.cli_generator import auto_cli_options as auto_cli_options
from .config.unified_config import CoreConfig as CoreConfig
from .perimeters import PerimeterExtractor as PerimeterExtractor
from .utils import MultiStepSpinner as MultiStepSpinner
from .code_package.code_packager import CodePackager as CodePackager
from .capsule import CapsuleDeployer as CapsuleDeployer
from .capsule import list_and_filter_capsules as list_and_filter_capsules
from .capsule import CapsuleApi as CapsuleApi
from ._state_machine import DEPLOYMENT_READY_CONDITIONS as DEPLOYMENT_READY_CONDITIONS
from .capsule import CapsuleApiException as CapsuleApiException
from .capsule import CapsuleDeploymentException as CapsuleDeploymentException
from .dependencies import bake_deployment_image as bake_deployment_image

CODE_PACKAGE_PREFIX: str

CAPSULE_DEBUG: bool

class KeyValueDictPair(metaflow._vendor.click.types.ParamType, metaclass=type):
    def convert(self, value, param, ctx):
        ...
    def __str__(self):
        ...
    def __repr__(self):
        ...
    ...

class KeyValuePair(metaflow._vendor.click.types.ParamType, metaclass=type):
    def convert(self, value, param, ctx):
        ...
    def __str__(self):
        ...
    def __repr__(self):
        ...
    ...

class CommaSeparatedList(metaflow._vendor.click.types.ParamType, metaclass=type):
    def convert(self, value, param, ctx):
        ...
    def __str__(self):
        ...
    def __repr__(self):
        ...
    ...

KVPairType: KeyValuePair

CommaSeparatedListType: CommaSeparatedList

KVDictType: KeyValueDictPair

class ColorTheme(object, metaclass=type):
    ...

class CliState(object, metaclass=type):
    ...

def print_table(data, headers):
    """
    Print data in a formatted table.
    """
    ...

def parse_cli_commands(cli_command_input):
    ...

def deployment_instance_options(func):
    ...

