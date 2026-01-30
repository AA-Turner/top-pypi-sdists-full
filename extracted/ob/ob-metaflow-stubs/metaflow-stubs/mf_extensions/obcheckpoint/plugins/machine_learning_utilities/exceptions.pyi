######################################################################################################
#                                 Auto-generated Metaflow stub file                                  #
# MF version: 2.19.18.1+obcheckpoint(0.2.10);ob(v1)                                                  #
# Generated on 2026-01-28T23:54:14.451850                                                            #
######################################################################################################

from __future__ import annotations

import metaflow
import typing
if typing.TYPE_CHECKING:
    import metaflow.exception

from .....exception import MetaflowException as MetaflowException

class TODOException(metaflow.exception.MetaflowException, metaclass=type):
    def __init__(self, message):
        ...
    ...

class KeyNotFoundError(metaflow.exception.MetaflowException, metaclass=type):
    def __init__(self, url):
        ...
    ...

class KeyNotCompatibleException(metaflow.exception.MetaflowException, metaclass=type):
    def __init__(self, key, supported_types):
        ...
    ...

class KeyNotCompatibleWithObjectException(metaflow.exception.MetaflowException, metaclass=type):
    def __init__(self, key, store, message = None):
        ...
    ...

class IncompatibleObjectTypeException(metaflow.exception.MetaflowException, metaclass=type):
    def __init__(self, message):
        ...
    ...

