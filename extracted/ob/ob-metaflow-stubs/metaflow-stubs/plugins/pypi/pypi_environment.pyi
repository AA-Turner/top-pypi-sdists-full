######################################################################################################
#                                 Auto-generated Metaflow stub file                                  #
# MF version: 2.15.21.4+obcheckpoint(0.2.4);ob(v1)                                                   #
# Generated on 2025-07-25T18:05:14.925831                                                            #
######################################################################################################

from __future__ import annotations

import metaflow
import typing
if typing.TYPE_CHECKING:
    import metaflow.plugins.pypi.conda_environment

from .conda_environment import CondaEnvironment as CondaEnvironment

class PyPIEnvironment(metaflow.plugins.pypi.conda_environment.CondaEnvironment, metaclass=type):
    ...

