######################################################################################################
#                                 Auto-generated Metaflow stub file                                  #
# MF version: 2.19.19                                                                                #
# Generated on 2026-02-09T14:58:07.188400                                                            #
######################################################################################################

from __future__ import annotations

import metaflow
import typing
if typing.TYPE_CHECKING:
    import metaflow.exception

from ..exception import MetaflowException as MetaflowException

SERVICE_HEADERS: dict

HB_URL_KEY: str

class HeartBeatException(metaflow.exception.MetaflowException, metaclass=type):
    def __init__(self, msg):
        ...
    ...

class MetadataHeartBeat(object, metaclass=type):
    def __init__(self):
        ...
    def process_message(self, msg):
        ...
    @classmethod
    def get_worker(cls):
        ...
    ...

