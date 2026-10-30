######################################################################################################
#                                 Auto-generated Metaflow stub file                                  #
# MF version: 2.19.40                                                                                #
# Generated on 2026-10-29T20:14:39.476025                                                            #
######################################################################################################

from __future__ import annotations

import metaflow
import typing
if typing.TYPE_CHECKING:
    import metaflow.plugins.pypi.conda_environment

from .conda_environment import CondaEnvironment as CondaEnvironment

class PyPIEnvironment(metaflow.plugins.pypi.conda_environment.CondaEnvironment, metaclass=type):
    ...

