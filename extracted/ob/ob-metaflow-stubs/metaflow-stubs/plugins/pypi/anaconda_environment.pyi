######################################################################################################
#                                 Auto-generated Metaflow stub file                                  #
# MF version: 2.19.33.1+obcheckpoint(0.2.10);<unk>(<unk>);ob(v1)                                     #
# Generated on 2026-06-09T20:21:00.290348                                                            #
######################################################################################################

from __future__ import annotations

import metaflow
import typing
if typing.TYPE_CHECKING:
    import metaflow.plugins.pypi.conda_environment

from .conda_environment import CondaEnvironment as CondaEnvironment

class AnacondaEnvironment(metaflow.plugins.pypi.conda_environment.CondaEnvironment, metaclass=type):
    def decospecs(self):
        ...
    ...

