######################################################################################################
#                                 Auto-generated Metaflow stub file                                  #
# MF version: 2.19.39                                                                                #
# Generated on 2026-09-02T21:19:46.767864                                                            #
######################################################################################################

from __future__ import annotations

import metaflow
import typing
if typing.TYPE_CHECKING:
    import metaflow.plugins.pypi.conda_environment

from .conda_environment import CondaEnvironment as CondaEnvironment

class PyPIEnvironment(metaflow.plugins.pypi.conda_environment.CondaEnvironment, metaclass=type):
    ...

