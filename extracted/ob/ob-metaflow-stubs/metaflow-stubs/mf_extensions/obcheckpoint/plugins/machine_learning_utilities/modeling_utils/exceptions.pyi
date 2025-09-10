######################################################################################################
#                                 Auto-generated Metaflow stub file                                  #
# MF version: 2.18.3.2+obcheckpoint(0.2.4);ob(v1)                                                    #
# Generated on 2025-09-09T09:20:35.596161                                                            #
######################################################################################################

from __future__ import annotations

import metaflow
import typing
if typing.TYPE_CHECKING:
    import metaflow.exception

from ......exception import MetaflowException as MetaflowException

class LoadingException(metaflow.exception.MetaflowException, metaclass=type):
    def __init__(self, message):
        ...
    ...

class ModelException(metaflow.exception.MetaflowException, metaclass=type):
    def __init__(self, message):
        ...
    ...

