######################################################################################################
#                                 Auto-generated Metaflow stub file                                  #
# MF version: 2.15.17.1+obcheckpoint(0.2.1);ob(v1)                                                   #
# Generated on 2025-06-16T20:11:02.936365                                                            #
######################################################################################################

from __future__ import annotations

import typing
if typing.TYPE_CHECKING:
    import metaflow

from ......metaflow_current import current as current
from .identity_utils import TaskIdentifier as TaskIdentifier
from .identity_utils import FlowNotRunningException as FlowNotRunningException

TYPE_CHECKING: bool

class ResolvedTask(tuple, metaclass=type):
    """
    ResolvedTask(flow_name, run_id, step_name, task_id, is_foreach, current_attempt, pathspec, control_task_pathspec)
    """
    @staticmethod
    def __new__(_cls, flow_name, run_id, step_name, task_id, is_foreach, current_attempt, pathspec, control_task_pathspec):
        """
        Create new instance of ResolvedTask(flow_name, run_id, step_name, task_id, is_foreach, current_attempt, pathspec, control_task_pathspec)
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

class OriginInfo(tuple, metaclass=type):
    """
    OriginInfo(origin_run_id, origin_task_id, origin_attempt, is_foreach)
    """
    @staticmethod
    def __new__(_cls, origin_run_id, origin_task_id, origin_attempt, is_foreach):
        """
        Create new instance of OriginInfo(origin_run_id, origin_task_id, origin_attempt, is_foreach)
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

def resolve_pathspec_for_flowspec(run: "metaflow.FlowSpec" = None):
    ...

def resolve_storage_backend(run: "metaflow.FlowSpec" = None):
    ...

def resolve_task_identifier(run: "metaflow.FlowSpec", gang_scheduled_task = False, gang_schedule_task_idf_index = 0):
    ...

