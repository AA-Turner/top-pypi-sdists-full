######################################################################################################
#                                 Auto-generated Metaflow stub file                                  #
# MF version: 2.15.17.1+obcheckpoint(0.2.1);ob(v1)                                                   #
# Generated on 2025-06-16T20:11:02.908201                                                            #
######################################################################################################

from __future__ import annotations

import metaflow
import typing
if typing.TYPE_CHECKING:
    import metaflow.exception
    import metaflow

from ......metaflow_current import current as current
from ......exception import MetaflowException as MetaflowException
from .context import datastore_context as datastore_context

TYPE_CHECKING: bool

class UnresolvableDatastoreException(metaflow.exception.MetaflowException, metaclass=type):
    ...

def init_datastorage_object():
    ...

def resolve_storage_backend(pathspec: typing.Union[str, "metaflow.Task"] = None):
    """
    This function is ONLY called when the user is calling `Checkpoint.list`.
    What happens when users call list:
        1. The task has completed so the list call is using the `_task_checkpoints` data-artifact to list the checkpoints.
        2. The task is still running or has crashed. This means that in order to list the checkpoints, we need access to the datastore.
    
    For case `1`, this code path wont even be called because the data-artifact is already a separate object.
    For case `2` is where this code path is important. But since we now expose a `artifact_store_from` context manager, we
    know pre-hand what the datastore needs to be and the datastore context has already been switched.
    
    SO in turn, one can make the argument that this function is not needed and we can just have a
    users do a `Checkpoint.list` under the context manager if they need to access objects in a different datastore.
    
    This is a respectible pattern since directly reading the task metadata and trying to do a list call is not a good pattern
    since the creds of metaflow default datastore might not be the same as the datastore the user wants to access.
    
    There is a function that can help verify if the datastore set in the task metadata
    is the same as the default datastore. If it is not, then we should shout warning messages
    to the user. In case the permissions are the same, nothing wrong happens, if they are not then
    user will have some hint in the logs to help them figure out the issue.
    """
    ...

class FlowNotRunningException(metaflow.exception.MetaflowException, metaclass=type):
    ...

def storage_backend_from_flow(flow: "metaflow.FlowSpec"):
    ...

