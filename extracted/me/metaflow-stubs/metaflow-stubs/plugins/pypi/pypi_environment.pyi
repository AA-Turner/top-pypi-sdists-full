######################################################################################################
#                                 Auto-generated Metaflow stub file                                  #
# MF version: 2.19.32                                                                                #
# Generated on 2026-06-03T21:26:43.581751                                                            #
######################################################################################################

from __future__ import annotations

import metaflow
import typing
if typing.TYPE_CHECKING:
    import metaflow.plugins.pypi.conda_environment

from .conda_environment import CondaEnvironment as CondaEnvironment

class PyPIEnvironment(metaflow.plugins.pypi.conda_environment.CondaEnvironment, metaclass=type):
    ...

