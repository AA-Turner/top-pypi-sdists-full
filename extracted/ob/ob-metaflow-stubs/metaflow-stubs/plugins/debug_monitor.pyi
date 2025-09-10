######################################################################################################
#                                 Auto-generated Metaflow stub file                                  #
# MF version: 2.18.3.2+obcheckpoint(0.2.4);ob(v1)                                                    #
# Generated on 2025-09-09T09:20:35.553577                                                            #
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

