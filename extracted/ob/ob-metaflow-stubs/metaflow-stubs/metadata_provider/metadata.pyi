######################################################################################################
#                                 Auto-generated Metaflow stub file                                  #
# MF version: 2.15.17.1+obcheckpoint(0.2.1);ob(v1)                                                   #
# Generated on 2025-06-16T20:11:02.889601                                                            #
######################################################################################################

from __future__ import annotations

import metaflow
import typing
if typing.TYPE_CHECKING:
    import metaflow.metadata_provider.metadata

from ..exception import MetaflowInternalError as MetaflowInternalError
from ..exception import MetaflowTaggingError as MetaflowTaggingError
from ..tagging_util import validate_tag as validate_tag

class DataArtifact(tuple, metaclass=type):
    """
    DataArtifact(name, ds_type, ds_root, url, type, sha)
    """
    @staticmethod
    def __new__(_cls, name, ds_type, ds_root, url, type, sha):
        """
        Create new instance of DataArtifact(name, ds_type, ds_root, url, type, sha)
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

class MetaDatum(tuple, metaclass=type):
    """
    MetaDatum(field, value, type, tags)
    """
    @staticmethod
    def __new__(_cls, field, value, type, tags):
        """
        Create new instance of MetaDatum(field, value, type, tags)
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

class MetadataProviderMeta(type, metaclass=type):
    @staticmethod
    def __new__(metaname, classname, bases, attrs):
        ...
    def __init__(classobject, classname, bases, attrs):
        ...
    @property
    def INFO(classobject):
        ...
    @INFO.setter
    def INFO(classobject, val):
        ...
    ...

def with_metaclass(mcls):
    ...

class ObjectOrder(object, metaclass=type):
    @staticmethod
    def order_to_type(order):
        ...
    @staticmethod
    def type_to_order(obj_type):
        ...
    ...

class MetadataProvider(object, metaclass=MetadataProviderMeta):
    @classmethod
    def metadata_str(cls):
        ...
    @classmethod
    def compute_info(cls, val):
        """
        Compute the new information for this provider
        
        The computed value should be returned and will then be accessible directly as cls.INFO.
        This information will be printed by the client when describing this metadata provider
        
        Parameters
        ----------
        val : str
            Provider specific information used in computing the new information. For example, this
            can be a path.
        
        Returns
        -------
        str :
            Value to be set to INFO
        """
        ...
    @classmethod
    def default_info(cls):
        """
        Returns the default information for this provider
        
        This should compute and return the default value for the information regarding this provider.
        For example, this can compute where the metadata is stored
        
        Returns
        -------
        str
            Value to be set by default in INFO
        """
        ...
    def version(self):
        """
        Returns the version of this provider
        
        Returns
        -------
        str
            Version of the provider
        """
        ...
    def new_run_id(self, tags = None, sys_tags = None):
        """
        Creates an ID and registers this new run.
        
        The run ID will be unique within a given flow.
        
        Parameters
        ----------
        tags : list, optional
            Tags to apply to this particular run, by default None
        sys_tags : list, optional
            System tags to apply to this particular run, by default None
        
        Returns
        -------
        int
            Run ID for the run
        """
        ...
    def register_run_id(self, run_id, tags = None, sys_tags = None):
        """
        No-op operation in this implementation.
        
        Parameters
        ----------
        run_id : int
            Run ID for this run
        tags : list, optional
            Tags to apply to this particular run, by default None
        sys_tags : list, optional
            System tags to apply to this particular run, by default None
        Returns
        -------
        bool
            True if a new run was registered; False if it already existed
        """
        ...
    def new_task_id(self, run_id, step_name, tags = None, sys_tags = None):
        """
        Creates an ID and registers this new task.
        
        The task ID will be unique within a flow, run and step
        
        Parameters
        ----------
        run_id : int
            ID of the run
        step_name : string
            Name of the step
        tags : list, optional
            Tags to apply to this particular task, by default None
        sys_tags : list, optional
            System tags to apply to this particular task, by default None
        
        Returns
        -------
        int
            Task ID for the task
        """
        ...
    def register_task_id(self, run_id, step_name, task_id, attempt = 0, tags = None, sys_tags = None):
        """
        No-op operation in this implementation.
        
        Parameters
        ----------
        run_id : int or convertible to int
            Run ID for this run
        step_name : string
            Name of the step
        task_id : int
            Task ID
        tags : list, optional
            Tags to apply to this particular run, by default []
        sys_tags : list, optional
            System tags to apply to this particular run, by default []
        Returns
        -------
        bool
            True if a new run was registered; False if it already existed
        """
        ...
    def get_runtime_environment(self, runtime_name):
        """
        Returns a dictionary of environment variables to be set
        
        Parameters
        ----------
        runtime_name : string
            Name of the runtime for which to get the environment
        
        Returns
        -------
        dict[string] -> string
            Environment variables from this metadata provider
        """
        ...
    def register_data_artifacts(self, run_id, step_name, task_id, attempt_id, artifacts):
        """
        Registers the fact that the data-artifacts are associated with
        the particular task.
        
        Artifacts produced by a given task can be associated with the
        task using this call
        
        Parameters
        ----------
        run_id : int
            Run ID for the task
        step_name : string
            Step name for the task
        task_id : int
            Task ID for the task
        attempt_id : int
            Attempt for the task
        artifacts : List of DataArtifact
            Artifacts associated with this task
        """
        ...
    def register_metadata(self, run_id, step_name, task_id, metadata):
        """
        Registers metadata with a task.
        
        Note that the same metadata can be registered multiple times for the same task (for example
        by multiple attempts). Internally, the timestamp of when the registration call is made is
        also recorded allowing the user to determine the latest value of the metadata.
        
        Parameters
        ----------
        run_id : int
            Run ID for the task
        step_name : string
            Step name for the task
        task_id : int
            Task ID for the task
        metadata : List of MetaDatum
            Metadata associated with this task
        """
        ...
    def start_task_heartbeat(self, flow_id, run_id, step_name, task_id):
        ...
    def start_run_heartbeat(self, flow_id, run_id):
        ...
    def stop_heartbeat(self):
        ...
    def add_sticky_tags(self, tags = None, sys_tags = None):
        """
        Adds tags to be added to every run and task
        
        Tags can be added to record information about a run/task. Such tags can be specified on a
        per run or task basis using the new_run_id/register_run_id or new_task_id/register_task_id
        functions but can also be set globally using this function. Tags added here will be
        added to every run/task created after this call is made.
        
        Parameters
        ----------
        tags : list, optional
            Tags to add to every run/task, by default None
        sys_tags : list, optional
            System tags to add to every run/task, by default None
        """
        ...
    @classmethod
    def get_object(cls, obj_type, sub_type, filters, attempt, *args):
        """
        Returns the requested object depending on obj_type and sub_type
        
        obj_type can be one of 'root', 'flow', 'run', 'step', 'task',
        or 'artifact'
        
        sub_type describes the aggregation required and can be either:
        'metadata', 'self' or any of obj_type provided that it is slotted below
        the object itself. For example, if obj_type is 'flow', you can
        specify 'run' to get all the runs in that flow.
        A few special rules:
            - 'metadata' is only allowed for obj_type 'task'
            - For obj_type 'artifact', only 'self' is allowed
        A few examples:
            - To get a list of all flows:
                - set obj_type to 'root' and sub_type to 'flow'
            - To get a list of all tasks:
                - set obj_type to 'root' and sub_type to 'task'
            - To get a list of all artifacts in a task:
                - set obj_type to 'task' and sub_type to 'artifact'
            - To get information about a specific flow:
                - set obj_type to 'flow' and sub_type to 'self'
        
        Parameters
        ----------
        obj_type : string
            One of 'root', 'flow', 'run', 'step', 'task', 'artifact' or 'metadata'
        sub_type : string
            Same as obj_type with the addition of 'self'
        filters : dict
            Dictionary with keys 'any_tags', 'tags' and 'system_tags'. If specified
            will return only objects that have the specified tags present. Filters
            are ANDed together so all tags must be present for the object to be returned.
        attempt : int or None
            If None, for metadata and artifacts:
              - returns information about the latest attempt for artifacts
              - returns all metadata across all attempts
            Otherwise, returns information about metadata and artifacts for that
            attempt only.
            NOTE: For older versions of Metaflow (pre 2.4.0), the attempt for
            metadata is not known; in that case, all metadata is returned (as
            if None was passed in).
        
        Return
        ------
            object or list :
                Depending on the call, the type of object return varies
        """
        ...
    @classmethod
    def mutate_user_tags_for_run(cls, flow_id, run_id, tags_to_remove = None, tags_to_add = None):
        """
        Mutate the set of user tags for a run.
        
        Removals logically get applied after additions.  Operations occur as a batch atomically.
        Parameters
        ----------
        flow_id : str
            Flow id, that the run belongs to.
        run_id: str
            Run id, together with flow_id, that identifies the specific Run whose tags to mutate
        tags_to_remove: iterable over str
            Iterable over tags to remove
        tags_to_add: iterable over str
            Iterable over tags to add
        
        Return
        ------
        Run tags after mutation operations
        """
        ...
    @classmethod
    def filter_tasks_by_metadata(cls, flow_name: str, run_id: str, step_name: str, field_name: str, pattern: str) -> typing.List[str]:
        """
        Filter tasks by metadata field and pattern, returning task pathspecs that match criteria.
        
        Parameters
        ----------
        flow_name : str
            Flow name, that the run belongs to.
        run_id: str
            Run id, together with flow_id, that identifies the specific Run whose tasks to query
        step_name: str
            Step name to query tasks from
        field_name: str
            Metadata field name to query
        pattern: str
            Pattern to match in metadata field value
        
        Returns
        -------
        List[str]
            List of task pathspecs that satisfy the query
        """
        ...
    def __init__(self, environment, flow, event_logger, monitor):
        ...
    ...

