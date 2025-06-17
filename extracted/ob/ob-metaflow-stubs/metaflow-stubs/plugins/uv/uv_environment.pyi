######################################################################################################
#                                 Auto-generated Metaflow stub file                                  #
# MF version: 2.15.17.1+obcheckpoint(0.2.1);ob(v1)                                                   #
# Generated on 2025-06-16T20:11:02.932795                                                            #
######################################################################################################

from __future__ import annotations

import metaflow
import typing
if typing.TYPE_CHECKING:
    import metaflow.exception
    import metaflow.metaflow_environment

from ...exception import MetaflowException as MetaflowException

class UVException(metaflow.exception.MetaflowException, metaclass=type):
    ...

class UVEnvironment(metaflow.metaflow_environment.MetaflowEnvironment, metaclass=type):
    def __init__(self, flow):
        ...
    def validate_environment(self, logger, datastore_type):
        ...
    def init_environment(self, echo, only_steps = None):
        ...
    def executable(self, step_name, default = None):
        ...
    def add_to_package(self):
        ...
    def pylint_config(self):
        ...
    def bootstrap_commands(self, step_name, datastore_type):
        ...
    ...

