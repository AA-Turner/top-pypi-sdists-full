######################################################################################################
#                                 Auto-generated Metaflow stub file                                  #
# MF version: 2.19.17                                                                                #
# Generated on 2026-01-22T21:47:05.908247                                                            #
######################################################################################################

from __future__ import annotations

import metaflow
import typing
if typing.TYPE_CHECKING:
    import metaflow.plugins.pypi.conda_environment

from .conda_environment import CondaEnvironment as CondaEnvironment

class PyPIEnvironment(metaflow.plugins.pypi.conda_environment.CondaEnvironment, metaclass=type):
    ...

