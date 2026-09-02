from abc import ABC
from typing import Optional, ParamSpec, Any
import traceback
from ..utils.stats import TaskMonitor

P = ParamSpec("P")

class StatSupport(ABC):
    """StatSupport.

    Adding Support for Task Monitor (Statistics Collector.)
    """

    def __init__(
        self,
        *args: P.args,
        **kwargs: P.kwargs
    ):
        # stats object:
        self._stat_: bool = True
        stat: Optional[TaskMonitor] = kwargs.pop('stat', None)
        if stat:
            self.stat: Optional[TaskMonitor] = stat
        else:
            self.stat = None
            self._stat_ = False
        super().__init__(*args, **kwargs)

    def save_traceback(self):
        try:
            self.stat.stacktrace(traceback.format_exc())
        finally:
            pass

    def add_metric(self, name, value):
        try:
            self.stat.add_metric(name, value)
        except AttributeError:
            pass
