######################################################################################################
#                                 Auto-generated Metaflow stub file                                  #
# MF version: 2.19.38                                                                                #
# Generated on 2026-08-18T00:36:54.520604                                                            #
######################################################################################################

from __future__ import annotations

import metaflow
import typing
if typing.TYPE_CHECKING:
    import metaflow.exception

from ...exception import MetaflowException as MetaflowException

class AirflowException(metaflow.exception.MetaflowException, metaclass=type):
    def __init__(self, msg):
        ...
    ...

class NotSupportedException(metaflow.exception.MetaflowException, metaclass=type):
    ...

