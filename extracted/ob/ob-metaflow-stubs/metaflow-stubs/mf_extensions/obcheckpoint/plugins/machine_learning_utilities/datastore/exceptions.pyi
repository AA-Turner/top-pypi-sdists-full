######################################################################################################
#                                 Auto-generated Metaflow stub file                                  #
# MF version: 2.19.19.1+obcheckpoint(0.2.10);<unk>(<unk>);ob(v1)                                     #
# Generated on 2026-02-11T23:40:09.266765                                                            #
######################################################################################################

from __future__ import annotations

import metaflow
import typing
if typing.TYPE_CHECKING:
    import metaflow.exception

from ......exception import MetaflowException as MetaflowException

class DatastoreReadInitException(metaflow.exception.MetaflowException, metaclass=type):
    def __init__(self, message):
        ...
    ...

class DatastoreWriteInitException(metaflow.exception.MetaflowException, metaclass=type):
    def __init__(self, message):
        ...
    ...

class DatastoreNotReadyException(metaflow.exception.MetaflowException, metaclass=type):
    def __init__(self, message):
        ...
    ...

