######################################################################################################
#                                 Auto-generated Metaflow stub file                                  #
# MF version: 2.19.33.1+obcheckpoint(0.2.10);<unk>(<unk>);ob(v1)                                     #
# Generated on 2026-06-09T20:21:00.224326                                                            #
######################################################################################################

from __future__ import annotations

import typing


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
    def __init__(self, interval = 1, duration = 300, max_samples_per_gpu = None):
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
    def read(self, max_points = None):
        ...
    def cleanup(self):
        ...
    ...

class GPUProfiler(object, metaclass=type):
    @staticmethod
    def read_gpu_info():
        """
        Query nvidia-smi for driver info, device list, and interconnect topology.
        
        Returns a dict with keys:
            driver_version, cuda_version, error, devices, interconnect
        """
        ...
    ...

