######################################################################################################
#                                 Auto-generated Metaflow stub file                                  #
# MF version: 2.19.39.2+obcheckpoint(0.2.14);<unk>(<unk>);ob(v1)                                     #
# Generated on 2026-10-30T13:34:58.246699                                                            #
######################################################################################################

from __future__ import annotations

import metaflow
import typing
if typing.TYPE_CHECKING:
    import metaflow.plugins.pypi.conda_environment

from .conda_environment import CondaEnvironment as CondaEnvironment

class PyPIEnvironment(metaflow.plugins.pypi.conda_environment.CondaEnvironment, metaclass=type):
    ...

