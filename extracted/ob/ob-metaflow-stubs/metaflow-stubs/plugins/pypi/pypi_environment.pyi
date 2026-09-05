######################################################################################################
#                                 Auto-generated Metaflow stub file                                  #
# MF version: 2.19.37.3+obcheckpoint(0.2.10);<unk>(<unk>);ob(v1)                                     #
# Generated on 2026-09-04T19:03:46.142517                                                            #
######################################################################################################

from __future__ import annotations

import metaflow
import typing
if typing.TYPE_CHECKING:
    import metaflow.plugins.pypi.conda_environment

from .conda_environment import CondaEnvironment as CondaEnvironment

class PyPIEnvironment(metaflow.plugins.pypi.conda_environment.CondaEnvironment, metaclass=type):
    ...

