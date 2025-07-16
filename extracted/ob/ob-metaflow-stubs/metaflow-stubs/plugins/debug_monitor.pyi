######################################################################################################
#                                 Auto-generated Metaflow stub file                                  #
# MF version: 2.16.1.1+obcheckpoint(0.2.4);ob(v1)                                                    #
# Generated on 2025-07-15T20:32:21.519773                                                            #
######################################################################################################

from __future__ import annotations

import metaflow
import typing
if typing.TYPE_CHECKING:
    import metaflow.monitor


class DebugMonitor(metaflow.monitor.NullMonitor, metaclass=type):
    @classmethod
    def get_worker(cls):
        ...
    ...

class DebugMonitorSidecar(object, metaclass=type):
    def __init__(self):
        ...
    def process_message(self, msg):
        ...
    ...

