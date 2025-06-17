######################################################################################################
#                                 Auto-generated Metaflow stub file                                  #
# MF version: 2.15.17.1+obcheckpoint(0.2.1);ob(v1)                                                   #
# Generated on 2025-06-16T20:11:02.887390                                                            #
######################################################################################################

from __future__ import annotations

import typing

from ....plugins.cards.card_modules.components import Markdown as Markdown
from ....plugins.cards.card_modules.components import Table as Table
from ....plugins.cards.card_modules.components import VegaChart as VegaChart
from ....metaflow_current import current as current
from ....plugins.cards.card_modules.components import Image as Image

MEM_COLOR: str

GPU_COLOR: str

NVIDIA_TS_FORMAT: str

MONITOR_FIELDS: list

MONITOR: str

class ProcessUUID(tuple, metaclass=type):
    """
    ProcessUUID(uuid, start_time, end_time)
    """
    @staticmethod
    def __new__(_cls, uuid, start_time, end_time):
        """
        Create new instance of ProcessUUID(uuid, start_time, end_time)
        """
        ...
    def __repr__(self):
        """
        Return a nicely formatted representation string
        """
        ...
    def __getnewargs__(self):
        """
        Return self as a plain tuple.  Used by copy and pickle.
        """
        ...
    ...

class AsyncProcessManager(object, metaclass=type):
    """
    This class is responsible for managing the nvidia SMI subprocesses
    """
    @classmethod
    def get(cls, procid):
        ...
    @classmethod
    def spawn(cls, procid, cmd, file):
        ...
    @classmethod
    def remove(cls, procid, delete_item = True):
        ...
    @classmethod
    def cleanup(cls):
        ...
    @classmethod
    def is_running(cls, procid):
        ...
    def __init__(self, processes: typing.Dict[str, typing.Dict]):
        ...
    ...

class GPUMonitor(object, metaclass=type):
    """
    The `GPUMonitor` class is designed to monitor GPU usage.
    
    When an instance of `GPUMonitor` is created, it initializes with a specified `interval` and `duration`.
    The `duration` is the timeperiod it will run the NVIDIA SMI command for and the `interval` is the timeperiod between each reading.
    The class exposes a `_monitor_update_thread` method which runs as a background thread that continuously updates the GPU usage readings.
    It will keep running unitl the `_finished` flag is set to `True`.
    
    The class will statefully manage the the spawned NVIDI-SMI processes.
    It will start a new NVIDI-SMI process after the current one has ran for the specified `duration`.
    At a time this class will only maintain readings for the `_current_process` and will have all the aggregated
    readings for the past processes stored in the `_past_readings` dictionary.
    When a process finishes completion, the readings are appended to the `_past_readings` dictionary and a new process is started.
    
    If the caller of this class wishes to read the GPU usage, they can call the `read` method which will return the readings in a dictionary format.
    The `read` method will aggregate the readings from the `_current_readings` and `_past_readings`.
    """
    def __init__(self, interval = 1, duration = 300):
        ...
    @property
    def _current_file(self):
        ...
    def get_file_name(self, uuid):
        ...
    def create_new_monitor(self):
        ...
    def clear_current_monitor(self):
        ...
    def current_process_has_ended(self):
        ...
    def current_process_is_running(self):
        ...
    def read(self):
        ...
    def cleanup(self):
        ...
    ...

class GPUProfiler(object, metaclass=type):
    def __init__(self, interval = 1, monitor_batch_duration = 200, artifact_name = 'gpu_profile_data', max_check_timeout = 60):
        ...
    def finish(self):
        ...
    ...

class gpu_profile(object, metaclass=type):
    def __init__(self, include_artifacts = True, artifact_prefix = 'gpu_profile_', interval = 1):
        ...
    def __call__(self, f):
        ...
    ...

def translate_to_vegalite(tstamps, vals, description, y_label, legend, line_color = None, percentage_format = False):
    ...

def profile_plots(device_id, ts, gpu, mem_used, mem_total):
    ...

