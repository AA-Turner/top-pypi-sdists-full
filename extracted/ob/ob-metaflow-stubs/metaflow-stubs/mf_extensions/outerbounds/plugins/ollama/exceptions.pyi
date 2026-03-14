######################################################################################################
#                                 Auto-generated Metaflow stub file                                  #
# MF version: 2.19.21.1+obcheckpoint(0.2.10);<unk>(<unk>);ob(v1)                                     #
# Generated on 2026-03-13T19:53:26.924633                                                            #
######################################################################################################

from __future__ import annotations

import metaflow
import typing
if typing.TYPE_CHECKING:
    import metaflow.exception

from .....exception import MetaflowException as MetaflowException

class UnspecifiedRemoteStorageRootException(metaflow.exception.MetaflowException, metaclass=type):
    def __init__(self, message):
        ...
    ...

class EmptyOllamaManifestCacheException(metaflow.exception.MetaflowException, metaclass=type):
    def __init__(self, message):
        ...
    ...

class EmptyOllamaBlobCacheException(metaflow.exception.MetaflowException, metaclass=type):
    def __init__(self, message):
        ...
    ...

