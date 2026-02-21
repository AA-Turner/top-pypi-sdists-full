######################################################################################################
#                                 Auto-generated Metaflow stub file                                  #
# MF version: 2.19.19.2+obcheckpoint(0.2.10);<unk>(<unk>);ob(v1)                                     #
# Generated on 2026-02-20T21:41:16.044607                                                            #
######################################################################################################

from __future__ import annotations

import metaflow
import typing
if typing.TYPE_CHECKING:
    import metaflow.mf_extensions.torchrun.plugins.torchrun_libs.exceptions
    import metaflow.exception

from .....exception import MetaflowException as MetaflowException

class TorchrunException(metaflow.exception.MetaflowException, metaclass=type):
    def __init__(self, cmd):
        ...
    ...

class TorchNotInstalledException(TorchrunException, metaclass=type):
    def __init__(self):
        ...
    ...

class DatastoreKeyNotFoundError(metaflow.exception.MetaflowException, metaclass=type):
    def __init__(self, datastore_path_name):
        ...
    ...

class BarrierTimeoutException(metaflow.exception.MetaflowException, metaclass=type):
    def __init__(self, lock_name, description):
        ...
    ...

class AllNodesStartupTimeoutException(metaflow.exception.MetaflowException, metaclass=type):
    def __init__(self):
        ...
    ...

