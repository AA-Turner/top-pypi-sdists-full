######################################################################################################
#                                 Auto-generated Metaflow stub file                                  #
# MF version: 2.19.19.2+obcheckpoint(0.2.10);<unk>(<unk>);ob(v1)                                     #
# Generated on 2026-02-20T21:41:16.047595                                                            #
######################################################################################################

from __future__ import annotations

import typing
if typing.TYPE_CHECKING:
    import metaflow.monitor


class SystemMonitor(object, metaclass=type):
    def __init__(self):
        ...
    def __del__(self):
        ...
    def init_system_monitor(self, flow_name: str, monitor: "metaflow.monitor.NullMonitor"):
        ...
    @property
    def monitor(self) -> typing.Optional["metaflow.monitor.NullMonitor"]:
        ...
    def measure(self, name: str):
        """
        Context manager to measure the execution duration and counter of a block of code.
        
        Parameters
        ----------
        name : str
            The name to associate with the timer and counter.
        
        Yields
        ------
        None
        """
        ...
    def count(self, name: str):
        """
        Context manager to increment a counter.
        
        Parameters
        ----------
        name : str
            The name of the counter.
        
        Yields
        ------
        None
        """
        ...
    def gauge(self, gauge: "metaflow.monitor.Gauge"):
        """
        Log a gauge.
        
        Parameters
        ----------
        gauge : metaflow.monitor.Gauge
            The gauge to log.
        """
        ...
    ...

