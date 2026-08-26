######################################################################################################
#                                 Auto-generated Metaflow stub file                                  #
# MF version: 2.19.37.1+obcheckpoint(0.2.10);<unk>(<unk>);ob(v1)                                     #
# Generated on 2026-08-25T23:04:30.415337                                                            #
######################################################################################################

from __future__ import annotations

import threading
import typing
if typing.TYPE_CHECKING:
    import threading
    import metaflow.mf_extensions.torchrun.plugins.torchrun_libs.status_notifier
    import metaflow.mf_extensions.torchrun.plugins.torchrun_libs.datastore

from .datastore import TorchrunDatastore as TorchrunDatastore

class TaskStatus(tuple, metaclass=type):
    """
    TaskStatus(status, timestamp, node_index)
    """
    @staticmethod
    def __new__(_cls, status, timestamp, node_index):
        """
        Create new instance of TaskStatus(status, timestamp, node_index)
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

class TASK_STATUS(object, metaclass=type):
    ...

class TaskStatusNotifier(object, metaclass=type):
    def __init__(self, datastore: metaflow.mf_extensions.torchrun.plugins.torchrun_libs.datastore.TorchrunDatastore):
        ...
    def heartbeat(self, node_index: int):
        ...
    def running(self, node_index: int):
        ...
    def finished(self, node_index: int):
        ...
    def failed(self, node_index: int):
        ...
    def read(self, node_index: int) -> TaskStatus:
        ...
    ...

class TaskUnreachableException(Exception, metaclass=type):
    ...

class TaskFailedException(Exception, metaclass=type):
    ...

class HeartbeatTimeoutException(Exception, metaclass=type):
    ...

def wait_for_task_to_be_reachable(task_status_notifier: TaskStatusNotifier, node_index: int, timeout: int):
    ...

def wait_for_task_completion(task_status_notifier: TaskStatusNotifier, node_index: int, heartbeat_timeout: int = 3600, unreachable_timeout: int = 300):
    ...

class HeartbeatThread(threading.Thread, metaclass=type):
    def __init__(self, task_status_notifier: TaskStatusNotifier, node_index: int, heartbeat_interval: int = 10):
        ...
    def run(self):
        ...
    def stop(self):
        ...
    ...

