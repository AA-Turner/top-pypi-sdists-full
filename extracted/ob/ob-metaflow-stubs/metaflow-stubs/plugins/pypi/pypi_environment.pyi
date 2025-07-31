######################################################################################################
#                                 Auto-generated Metaflow stub file                                  #
# MF version: 2.15.21.5+obcheckpoint(0.2.4);ob(v1)                                                   #
# Generated on 2025-07-30T20:52:28.317039                                                            #
######################################################################################################

from __future__ import annotations

import metaflow
import typing
if typing.TYPE_CHECKING:
    import metaflow.plugins.pypi.conda_environment

from .conda_environment import CondaEnvironment as CondaEnvironment

class PyPIEnvironment(metaflow.plugins.pypi.conda_environment.CondaEnvironment, metaclass=type):
    ...

