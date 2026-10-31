######################################################################################################
#                                 Auto-generated Metaflow stub file                                  #
# MF version: 2.19.39.2+obcheckpoint(0.2.14);<unk>(<unk>);ob(v1)                                     #
# Generated on 2026-10-30T13:34:58.211330                                                            #
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

