######################################################################################################
#                                 Auto-generated Metaflow stub file                                  #
# MF version: 2.15.17.1+obcheckpoint(0.2.1);ob(v1)                                                   #
# Generated on 2025-06-16T20:11:02.907447                                                            #
######################################################################################################

from __future__ import annotations

import metaflow
import typing
if typing.TYPE_CHECKING:
    import metaflow.exception

from ......exception import MetaflowException as MetaflowException

class CheckpointNotAvailableException(metaflow.exception.MetaflowException, metaclass=type):
    def __init__(self, message):
        ...
    ...

class CheckpointException(metaflow.exception.MetaflowException, metaclass=type):
    def __init__(self, message):
        ...
    ...

