######################################################################################################
#                                 Auto-generated Metaflow stub file                                  #
# MF version: 2.18.2.1+obcheckpoint(0.2.4);ob(v1)                                                    #
# Generated on 2025-09-03T10:45:51.789283                                                            #
######################################################################################################

from __future__ import annotations

import metaflow
import typing
if typing.TYPE_CHECKING:
    import metaflow.event_logger


class DebugEventLogger(metaflow.event_logger.NullEventLogger, metaclass=type):
    @classmethod
    def get_worker(cls):
        ...
    ...

class DebugEventLoggerSidecar(object, metaclass=type):
    def __init__(self):
        ...
    def process_message(self, msg):
        ...
    ...

