######################################################################################################
#                                 Auto-generated Metaflow stub file                                  #
# MF version: 2.19.39.1+obcheckpoint(0.2.14);<unk>(<unk>);ob(v1)                                     #
# Generated on 2026-09-30T13:33:32.396812                                                            #
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

