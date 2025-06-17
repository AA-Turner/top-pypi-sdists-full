######################################################################################################
#                                 Auto-generated Metaflow stub file                                  #
# MF version: 2.15.17.1+obcheckpoint(0.2.1);ob(v1)                                                   #
# Generated on 2025-06-16T20:11:02.879007                                                            #
######################################################################################################

from __future__ import annotations

import metaflow
import typing
if typing.TYPE_CHECKING:
    import metaflow.exception
    import metaflow
    import metaflow.mf_extensions.obcheckpoint.plugins.machine_learning_utilities.datastore.context

from ......exception import MetaflowException as MetaflowException

TYPE_CHECKING: bool

ARTIFACT_STORE_CONFIG_ENV_VAR: str

def will_switch_context(func):
    """
    A decorator that wraps methods in ArtifactStoreContext.
    It takes the return value of the decorated method and passes it to
    self.switch_context(), then returns None.
    """
    ...

class DatastoreContextValidation(tuple, metaclass=type):
    """
    DatastoreContextInfo(is_valid, needs_external_context, context_mismatch)
    """
    @staticmethod
    def __new__(_cls, is_valid, needs_external_context, context_mismatch):
        """
        Create new instance of DatastoreContextInfo(is_valid, needs_external_context, context_mismatch)
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

class UnresolvableDatastoreException(metaflow.exception.MetaflowException, metaclass=type):
    ...

class ArtifactStoreContext(object, metaclass=type):
    """
    This class will act as a singleton to switch the datastore so that
    Any checkpoint operations will be done in the correct datastore. This
    can be a useful way of short-circuting a datastore switch between runtime
    And post-runtime retrieval operations.
    """
    @property
    def MF_DATASTORES(self):
        ...
    def __init__(self):
        ...
    def flow_init_context(self, *args, **kwargs):
        ...
    def switch_context(self, context):
        ...
    def get(self):
        ...
    def context_from_run(self, *args, **kwargs):
        ...
    def context_from_task(self, *args, **kwargs):
        ...
    def current_context_matches_task_metadata(self, task: "metaflow.Task"):
        ...
    def to_task_metadata(self):
        ...
    def default(self):
        ...
    ...

datastore_context: ArtifactStoreContext

def artifact_store_from(run = None, task = None, config = None):
    """
    This context manager can be used to switch the artifact store
    for a block of code. This is useful when users maybe accessing
    checkpoints/models from a different datastore using the
    `@with_artifact_store` decorator.
    """
    ...

