######################################################################################################
#                                 Auto-generated Metaflow stub file                                  #
# MF version: 2.19.29.1+obcheckpoint(0.2.10);<unk>(<unk>);ob(v1)                                     #
# Generated on 2026-05-12T17:11:58.104417                                                            #
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

