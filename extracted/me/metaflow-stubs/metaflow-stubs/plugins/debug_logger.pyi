######################################################################################################
#                                 Auto-generated Metaflow stub file                                  #
# MF version: 2.19.38                                                                                #
# Generated on 2026-08-18T00:36:54.505714                                                            #
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

