######################################################################################################
#                                 Auto-generated Metaflow stub file                                  #
# MF version: 2.15.17.1+obcheckpoint(0.2.1);ob(v1)                                                   #
# Generated on 2025-06-16T20:11:02.946360                                                            #
######################################################################################################

from __future__ import annotations

import metaflow
import typing
if typing.TYPE_CHECKING:
    import metaflow.exception
    import metaflow

from ......exception import MetaflowException as MetaflowException

TYPE_CHECKING: bool

MAX_HASH_LEN: int

class AttemptEnum(object, metaclass=type):
    @classmethod
    def values(cls):
        ...
    ...

class IdentityException(metaflow.exception.MetaflowException, metaclass=type):
    ...

class UnhashableValueException(metaflow.exception.MetaflowException, metaclass=type):
    def __init__(self, type):
        ...
    ...

class FlowNotRunningException(metaflow.exception.MetaflowException, metaclass=type):
    ...

def pathspec_hash(pathspec: str):
    ...

def safe_hash(value):
    """
    Safely hash arbitrary values and a created a sha for that object, including those that are not natively hashable.
    """
    ...

class TaskIdentifier(object, metaclass=type):
    """
    Any change to this class's core logic can create SEVERE backwards compatibility issues
    since this class helps derive the task identifier for the checkpoints.
    
    IDEALLY, the identifier construction logic of this file should be kept as is.
    """
    @classmethod
    def for_parallel_task_index(cls, run: "metaflow.FlowSpec", index: int):
        """
        This class is meant to mint a task-identifier for a parallel task based on the
        index of the task in the gang.
        """
        ...
    @classmethod
    def from_flowspec(cls, run: "metaflow.FlowSpec"):
        ...
    def from_task(cls, task: "metaflow.Task", use_origin = True):
        ...
    ...

