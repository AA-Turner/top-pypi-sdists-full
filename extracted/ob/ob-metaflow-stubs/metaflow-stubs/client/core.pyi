######################################################################################################
#                                 Auto-generated Metaflow stub file                                  #
# MF version: 2.15.17.1+obcheckpoint(0.2.1);ob(v1)                                                   #
# Generated on 2025-06-16T20:11:02.873953                                                            #
######################################################################################################

from __future__ import annotations

import metaflow
import typing
if typing.TYPE_CHECKING:
    import metaflow.client.core
    import tempfile
    import metaflow.events
    import datetime
    import tarfile
    import typing

from ..metaflow_current import current as current
from ..events import Trigger as Trigger
from ..exception import MetaflowInternalError as MetaflowInternalError
from ..exception import MetaflowInvalidPathspec as MetaflowInvalidPathspec
from ..exception import MetaflowNamespaceMismatch as MetaflowNamespaceMismatch
from ..exception import MetaflowNotFound as MetaflowNotFound
from ..includefile import IncludedFile as IncludedFile
from .filecache import FileCache as FileCache

TYPE_CHECKING: bool

DEFAULT_METADATA: str

MAX_ATTEMPTS: int

ENVIRONMENTS: list

METADATA_PROVIDERS: list

CONTROL_TASK_TAG: str

INFO_FILE: str

class Metadata(tuple, metaclass=type):
    """
    Metadata(name, value, created_at, type, task)
    """
    @staticmethod
    def __new__(_cls, name, value, created_at, type, task):
        """
        Create new instance of Metadata(name, value, created_at, type, task)
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

filecache: None

current_namespace: bool

current_metadata: bool

def metadata(ms: str) -> str:
    """
    Switch Metadata provider.
    
    This call has a global effect. Selecting the local metadata will,
    for example, not allow access to information stored in remote
    metadata providers.
    
    Note that you don't typically have to call this function directly. Usually
    the metadata provider is set through the Metaflow configuration file. If you
    need to switch between multiple providers, you can use the `METAFLOW_PROFILE`
    environment variable to switch between configurations.
    
    Parameters
    ----------
    ms : str
        Can be a path (selects local metadata), a URL starting with http (selects
        the service metadata) or an explicit specification <metadata_type>@<info>; as an
        example, you can specify local@<path> or service@<url>.
    
    Returns
    -------
    str
        The description of the metadata selected (equivalent to the result of
        get_metadata()).
    """
    ...

def get_metadata() -> str:
    """
    Returns the current Metadata provider.
    
    If this is not set explicitly using `metadata`, the default value is
    determined through the Metaflow configuration. You can use this call to
    check that your configuration is set up properly.
    
    If multiple configuration profiles are present, this call returns the one
    selected through the `METAFLOW_PROFILE` environment variable.
    
    Returns
    -------
    str
        Information about the Metadata provider currently selected. This information typically
        returns provider specific information (like URL for remote providers or local paths for
        local providers).
    """
    ...

def default_metadata() -> str:
    """
    Resets the Metadata provider to the default value, that is, to the value
    that was used prior to any `metadata` calls.
    
    Returns
    -------
    str
        The result of get_metadata() after resetting the provider.
    """
    ...

def namespace(ns: typing.Optional[str]) -> typing.Optional[str]:
    """
    Switch namespace to the one provided.
    
    This call has a global effect. No objects outside this namespace
    will be accessible. To access all objects regardless of namespaces,
    pass None to this call.
    
    Parameters
    ----------
    ns : str, optional
        Namespace to switch to or None to ignore namespaces.
    
    Returns
    -------
    str, optional
        Namespace set (result of get_namespace()).
    """
    ...

def get_namespace() -> typing.Optional[str]:
    """
    Return the current namespace that is currently being used to filter objects.
    
    The namespace is a tag associated with all objects in Metaflow.
    
    Returns
    -------
    str, optional
        The current namespace used to filter objects.
    """
    ...

def default_namespace() -> str:
    """
    Resets the namespace used to filter objects to the default one, i.e. the one that was
    used prior to any `namespace` calls.
    
    Returns
    -------
    str
        The result of get_namespace() after the namespace has been reset.
    """
    ...

class MetaflowObject(object, metaclass=type):
    """
    Base class for all Metaflow objects.
    
    Creates a new object of a specific type (Flow, Run, Step, Task, DataArtifact) given
    a path to it (its `pathspec`).
    
    Accessing Metaflow objects is done through one of two methods:
      - either by directly instantiating it with this class
      - or by accessing it through its parent (iterating over
        all children or accessing directly using the [] operator)
    
    With this class, you can:
      - Get a `Flow`; use `Flow('FlowName')`.
      - Get a `Run` of a flow; use `Run('FlowName/RunID')`.
      - Get a `Step` of a run; use `Step('FlowName/RunID/StepName')`.
      - Get a `Task` of a step, use `Task('FlowName/RunID/StepName/TaskID')`
      - Get a `DataArtifact` of a task; use
           `DataArtifact('FlowName/RunID/StepName/TaskID/ArtifactName')`.
    
    Attributes
    ----------
    tags : FrozenSet[str]
        Tags associated with the run this object belongs to (user and system tags).
    user_tags: FrozenSet[str]
        User tags associated with the run this object belongs to.
    system_tags: FrozenSet[str]
        System tags associated with the run this object belongs to.
    created_at : datetime
        Date and time this object was first created.
    parent : MetaflowObject
        Parent of this object. The parent of a `Run` is a `Flow` for example
    pathspec : str
        Pathspec of this object (for example: 'FlowName/RunID' for a `Run`)
    path_components : List[str]
        Components of the pathspec
    origin_pathspec : str, optional
        Pathspec of the original object this object was cloned from (in the case of a resume).
        None if not applicable.
    """
    def __init__(self, pathspec: typing.Optional[str] = None, attempt: typing.Optional[int] = None, _object: typing.Optional["MetaflowObject"] = None, _parent: typing.Optional["MetaflowObject"] = None, _namespace_check: bool = True, _metaflow: typing.Optional["Metaflow"] = None, _current_namespace: typing.Optional[str] = None, _current_metadata: typing.Optional[str] = None):
        ...
    def __iter__(self) -> typing.Iterator["MetaflowObject"]:
        """
        Iterate over all child objects of this object if any.
        
        Note that only children present in the current namespace are returned if and
        only if _namespace_check is set.
        
        Yields
        ------
        MetaflowObject
            Children of this object
        """
        ...
    def is_in_namespace(self) -> bool:
        """
        Returns whether this object is in the current namespace.
        
        If the current namespace is None, this will always return True.
        
        Returns
        -------
        bool
            Whether or not the object is in the current namespace
        """
        ...
    def __str__(self):
        ...
    def __repr__(self):
        ...
    def __getitem__(self, id: str) -> "MetaflowObject":
        """
        Returns the child object named 'id'.
        
        Parameters
        ----------
        id : str
            Name of the child object
        
        Returns
        -------
        MetaflowObject
            Child object
        
        Raises
        ------
        KeyError
            If the name does not identify a valid child object
        """
        ...
    def __contains__(self, id: str):
        """
        Tests whether a child named 'id' exists.
        
        Parameters
        ----------
        id : str
            Name of the child object
        
        Returns
        -------
        bool
            True if the child exists or False otherwise
        """
        ...
    def __setstate__(self, state):
        """
        This function is used during the unpickling operation.
        More info here https://docs.python.org/3/library/pickle.html#object.__setstate__
        """
        ...
    def __getstate__(self):
        """
        This function is used during the pickling operation.
        More info here https://docs.python.org/3/library/pickle.html#object.__getstate__
        
        This function is not forward compatible i.e., if this object (or any of the objects deriving
        from this object) are pickled (serialized) in a later version of Metaflow, it may not be possible
        to unpickle (deserialize) them in a previous version of Metaflow.
        """
        ...
    @property
    def tags(self) -> typing.FrozenSet[str]:
        """
        Tags associated with this object.
        
        Tags can be user defined or system defined. This returns all tags associated
        with the object.
        
        Returns
        -------
        Set[str]
            Tags associated with the object
        """
        ...
    @property
    def system_tags(self) -> typing.FrozenSet[str]:
        """
        System defined tags associated with this object.
        
        Returns
        -------
        Set[str]
            System tags associated with the object
        """
        ...
    @property
    def user_tags(self) -> typing.FrozenSet[str]:
        """
        User defined tags associated with this object.
        
        Returns
        -------
        Set[str]
            User tags associated with the object
        """
        ...
    @property
    def created_at(self) -> datetime.datetime:
        """
        Creation time for this object.
        
        This corresponds to the time the object's existence was first created which typically means
        right before any code is run.
        
        Returns
        -------
        datetime
            Date time of this object's creation.
        """
        ...
    @property
    def origin_pathspec(self) -> typing.Optional[str]:
        """
        The pathspec of the object from which the current object was cloned.
        
        Returns:
            str, optional
                pathspec of the origin object from which current object was cloned.
        """
        ...
    @property
    def parent(self) -> typing.Optional["MetaflowObject"]:
        """
        Returns the parent object of this object or None if none exists.
        
        Returns
        -------
        MetaflowObject, optional
            The parent of this object
        """
        ...
    @property
    def pathspec(self) -> str:
        """
        Returns a string representation uniquely identifying this object.
        
        The string is the same as the one you would pass into the constructor
        to build this object except if you are looking for a specific attempt of
        a task or a data artifact (in which case you need to add `attempt=<attempt>`
        in the constructor).
        
        Returns
        -------
        str
            Unique representation of this object
        """
        ...
    @property
    def path_components(self) -> typing.List[str]:
        """
        List of individual components of the pathspec.
        
        Returns
        -------
        List[str]
            Individual components of the pathspec
        """
        ...
    ...

class MetaflowCode(object, metaclass=type):
    """
    Snapshot of the code used to execute this `Run`. Instantiate the object through
    `Run(...).code` (if any step is executed remotely) or `Task(...).code` for an
    individual task. The code package is the same for all steps of a `Run`.
    
    `MetaflowCode` includes a package of the user-defined `FlowSpec` class and supporting
    files, as well as a snapshot of the Metaflow library itself.
    
    Currently, `MetaflowCode` objects are stored only for `Run`s that have at least one `Step`
    executing outside the user's local environment.
    
    The `TarFile` for the `Run` is given by `Run(...).code.tarball`
    
    Attributes
    ----------
    path : str
        Location (in the datastore provider) of the code package.
    info : Dict[str, str]
        Dictionary of information related to this code-package.
    flowspec : str
        Source code of the file containing the `FlowSpec` in this code package.
    tarball : TarFile
        Python standard library `tarfile.TarFile` archive containing all the code.
    """
    def __init__(self, flow_name: str, code_package: str):
        ...
    @property
    def path(self) -> str:
        """
        Location (in the datastore provider) of the code package.
        
        Returns
        -------
        str
            Full path of the code package
        """
        ...
    @property
    def info(self) -> typing.Dict[str, str]:
        """
        Metadata associated with the code package.
        
        Returns
        -------
        Dict[str, str]
            Dictionary of metadata. Keys and values are strings
        """
        ...
    @property
    def flowspec(self) -> str:
        """
        Source code of the Python file containing the FlowSpec.
        
        Returns
        -------
        str
            Content of the Python file
        """
        ...
    @property
    def tarball(self) -> tarfile.TarFile:
        """
        TarFile for this code package.
        
        Returns
        -------
        TarFile
            TarFile for everything in this code package
        """
        ...
    def extract(self) -> tempfile.TemporaryDirectory:
        """
        Extracts the code package to a temporary directory.
        
        This creates a temporary directory containing all user code
        files from the code package. The temporary directory is
        automatically deleted when the returned TemporaryDirectory
        object is garbage collected or when its cleanup() is called.
        
        To preserve the contents to a permanent location, use
        os.replace() which performs a zero-copy move on the same
        filesystem:
        
        ```python
        with task.code.extract() as tmp_dir:
            # Move contents to permanent location
            for item in os.listdir(tmp_dir):
                src = os.path.join(tmp_dir, item)
                dst = os.path.join('/path/to/permanent/dir', item)
                os.makedirs(os.path.dirname(dst), exist_ok=True)
                os.replace(src, dst)  # Atomic move operation
        ```
        Returns
        -------
        TemporaryDirectory
            A temporary directory containing the extracted code files.
            The directory and its contents are automatically deleted when
            this object is garbage collected.
        """
        ...
    @property
    def script_name(self) -> str:
        """
        Returns the filename of the Python script containing the FlowSpec.
        
        This is the main Python file that was used to execute the flow. For example,
        if your flow is defined in 'myflow.py', this property will return 'myflow.py'.
        
        Returns
        -------
        str
            Name of the Python file containing the FlowSpec
        """
        ...
    def __str__(self):
        ...
    ...

class DataArtifact(MetaflowObject, metaclass=type):
    """
    A single data artifact and associated metadata. Note that this object does
    not contain other objects as it is the leaf object in the hierarchy.
    
    Attributes
    ----------
    data : object
        The data contained in this artifact, that is, the object produced during
        execution of this run.
    sha : string
        A unique ID of this artifact.
    finished_at : datetime
        Corresponds roughly to the `Task.finished_at` time of the parent `Task`.
        An alias for `DataArtifact.created_at`.
    """
    @property
    def data(self) -> typing.Any:
        """
        Unpickled representation of the data contained in this artifact.
        
        Returns
        -------
        object
            Object contained in this artifact
        """
        ...
    @property
    def size(self) -> int:
        """
        Returns the size (in bytes) of the pickled object representing this
        DataArtifact
        
        Returns
        -------
        int
            size of the pickled representation of data artifact (in bytes)
        """
        ...
    @property
    def sha(self) -> str:
        """
        Unique identifier for this artifact.
        
        This is a unique hash of the artifact (historically SHA1 hash)
        
        Returns
        -------
        str
            Hash of this artifact
        """
        ...
    @property
    def finished_at(self) -> datetime.datetime:
        """
        Creation time for this artifact.
        
        Alias for created_at.
        
        Returns
        -------
        datetime
            Creation time
        """
        ...
    def __getstate__(self):
        ...
    def __setstate__(self, state):
        ...
    ...

class MetaflowData(object, metaclass=type):
    """
    Container of data artifacts produced by a `Task`. This object is
    instantiated through `Task.data`.
    
    `MetaflowData` allows results to be retrieved by their name
    through a convenient dot notation:
    
    ```python
    Task(...).data.my_object
    ```
    
    You can also test the existence of an object
    
    ```python
    if 'my_object' in Task(...).data:
        print('my_object found')
    ```
    
    Note that this container relies on the local cache to load all data
    artifacts. If your `Task` contains a lot of data, a more efficient
    approach is to load artifacts individually like so
    
    ```
    Task(...)['my_object'].data
    ```
    """
    def __init__(self, artifacts: typing.Iterable[metaflow.client.core.DataArtifact]):
        ...
    def __getattr__(self, name: str):
        ...
    def __contains__(self, var):
        ...
    def __str__(self):
        ...
    def __repr__(self):
        ...
    ...

class Task(MetaflowObject, metaclass=type):
    """
    A `Task` represents an execution of a `Step`.
    
    It contains all `DataArtifact` objects produced by the task as
    well as metadata related to execution.
    
    Note that the `@retry` decorator may cause multiple attempts of
    the task to be present. Usually you want the latest attempt, which
    is what instantiating a `Task` object returns by default. If
    you need to e.g. retrieve logs from a failed attempt, you can
    explicitly get information about a specific attempt by using the
    following syntax when creating a task:
    
    `Task('flow/run/step/task', attempt=<attempt>)`
    
    where `attempt=0` corresponds to the first attempt etc.
    
    Attributes
    ----------
    metadata : List[Metadata]
        List of all metadata events associated with the task.
    metadata_dict : Dict[str, str]
        A condensed version of `metadata`: A dictionary where keys
        are names of metadata events and values the latest corresponding event.
    data : MetaflowData
        Container of all data artifacts produced by this task. Note that this
        call downloads all data locally, so it can be slower than accessing
        artifacts individually. See `MetaflowData` for more information.
    artifacts : MetaflowArtifacts
        Container of `DataArtifact` objects produced by this task.
    successful : bool
        True if the task completed successfully.
    finished : bool
        True if the task completed.
    exception : object
        Exception raised by this task if there was one.
    finished_at : datetime
        Time this task finished.
    runtime_name : str
        Runtime this task was executed on.
    stdout : str
        Standard output for the task execution.
    stderr : str
        Standard error output for the task execution.
    code : MetaflowCode
        Code package for this task (if present). See `MetaflowCode`.
    environment_info : Dict[str, str]
        Information about the execution environment.
    """
    def __init__(self, *args, **kwargs):
        ...
    @property
    def parent_tasks(self) -> typing.Iterator["Task"]:
        """
        Yields all parent tasks of the current task if one exists.
        
        Yields
        ------
        Task
            Parent task of the current task
        """
        ...
    @property
    def child_tasks(self) -> typing.Iterator["Task"]:
        """
        Yield all child tasks of the current task if one exists.
        
        Yields
        ------
        Task
            Child task of the current task
        """
        ...
    @property
    def metadata(self) -> typing.List[metaflow.client.core.Metadata]:
        """
        Metadata events produced by this task across all attempts of the task
        *except* if you selected a specific task attempt.
        
        Note that Metadata is different from tags.
        
        Returns
        -------
        List[Metadata]
            Metadata produced by this task
        """
        ...
    @property
    def metadata_dict(self) -> typing.Dict[str, str]:
        """
        Dictionary mapping metadata names (keys) and their associated values.
        
        Note that unlike the metadata() method, this call will only return the latest
        metadata for a given name. For example, if a task executes multiple times (retries),
        the same metadata name will be generated multiple times (one for each execution of the
        task). The metadata() method returns all those metadata elements whereas this call will
        return the metadata associated with the latest execution of the task.
        
        Returns
        -------
        Dict[str, str]
            Dictionary mapping metadata name with value
        """
        ...
    @property
    def index(self) -> typing.Optional[int]:
        """
        Returns the index of the innermost foreach loop if this task is run inside at least
        one foreach.
        
        The index is what distinguishes the various tasks inside a given step.
        This call returns None if this task was not run in a foreach loop.
        
        Returns
        -------
        int, optional
            Index in the innermost loop for this task
        """
        ...
    @property
    def data(self) -> MetaflowData:
        """
        Returns a container of data artifacts produced by this task.
        
        You can access data produced by this task as follows:
        ```
        print(task.data.my_var)
        ```
        
        Returns
        -------
        MetaflowData
            Container of all artifacts produced by this task
        """
        ...
    @property
    def artifacts(self) -> typing.NamedTuple:
        """
        Returns a container of DataArtifacts produced by this task.
        
        You can access each DataArtifact by name like so:
        ```
        print(task.artifacts.my_var)
        ```
        This method differs from data() because it returns DataArtifact objects
        (which contain additional metadata) as opposed to just the data.
        
        Returns
        -------
        MetaflowArtifacts
            Container of all DataArtifacts produced by this task
        """
        ...
    @property
    def successful(self) -> bool:
        """
        Indicates whether or not the task completed successfully.
        
        This information is always about the latest task to have completed (in case
        of retries).
        
        Returns
        -------
        bool
            True if the task completed successfully and False otherwise
        """
        ...
    @property
    def finished(self) -> bool:
        """
        Indicates whether or not the task completed.
        
        This information is always about the latest task to have completed (in case
        of retries).
        
        Returns
        -------
        bool
            True if the task completed and False otherwise
        """
        ...
    @property
    def exception(self) -> typing.Optional[typing.Any]:
        """
        Returns the exception that caused the task to fail, if any.
        
        This information is always about the latest task to have completed (in case
        of retries). If successful() returns False and finished() returns True,
        this method can help determine what went wrong.
        
        Returns
        -------
        object
            Exception raised by the task or None if not applicable
        """
        ...
    @property
    def finished_at(self) -> typing.Optional[datetime.datetime]:
        """
        Returns the datetime object of when the task finished (successfully or not).
        
        This information is always about the latest task to have completed (in case
        of retries). This call will return None if the task is not finished.
        
        Returns
        -------
        datetime
            Datetime of when the task finished
        """
        ...
    @property
    def runtime_name(self) -> typing.Optional[str]:
        """
        Returns the name of the runtime this task executed on.
        
        
        Returns
        -------
        str
            Name of the runtime this task executed on
        """
        ...
    @property
    def stdout(self) -> str:
        """
        Returns the full standard out of this task.
        
        If you specify a specific attempt for this task, it will return the
        standard out for that attempt. If you do not specify an attempt,
        this will return the current standard out for the latest *started*
        attempt of the task. In both cases, multiple calls to this
        method will return the most up-to-date log (so if an attempt is not
        done, each call will fetch the latest log).
        
        Returns
        -------
        str
            Standard output of this task
        """
        ...
    @property
    def stdout_size(self) -> int:
        """
        Returns the size of the stdout log of this task.
        
        Similar to `stdout`, the size returned is the latest size of the log
        (so for a running attempt, this value will increase as the task produces
        more output).
        
        Returns
        -------
        int
            Size of the stdout log content (in bytes)
        """
        ...
    @property
    def stderr(self) -> str:
        """
        Returns the full standard error of this task.
        
        If you specify a specific attempt for this task, it will return the
        standard error for that attempt. If you do not specify an attempt,
        this will return the current standard error for the latest *started*
        attempt. In both cases, multiple calls to this
        method will return the most up-to-date log (so if an attempt is not
        done, each call will fetch the latest log).
        
        Returns
        -------
        str
            Standard error of this task
        """
        ...
    @property
    def stderr_size(self) -> int:
        """
        Returns the size of the stderr log of this task.
        
        Similar to `stderr`, the size returned is the latest size of the log
        (so for a running attempt, this value will increase as the task produces
        more output).
        
        Returns
        -------
        int
            Size of the stderr log content (in bytes)
        """
        ...
    @property
    def current_attempt(self) -> int:
        """
        Get the relevant attempt for this Task.
        
        Returns the specific attempt used when
        initializing the instance, or the latest *started* attempt for the Task.
        
        Returns
        -------
        int
            attempt id for this task object
        """
        ...
    @property
    def code(self) -> typing.Optional[metaflow.client.core.MetaflowCode]:
        """
        Returns the MetaflowCode object for this task, if present.
        
        Not all tasks save their code so this call may return None in those cases.
        
        Returns
        -------
        MetaflowCode
            Code package for this task
        """
        ...
    @property
    def environment_info(self) -> typing.Dict[str, typing.Any]:
        """
        Returns information about the environment that was used to execute this task. As an
        example, if the Conda environment is selected, this will return information about the
        dependencies that were used in the environment.
        
        This environment information is only available for tasks that have a code package.
        
        Returns
        -------
        Dict
            Dictionary describing the environment
        """
        ...
    def loglines(self, stream: str, as_unicode: bool = True, meta_dict: typing.Optional[typing.Dict[str, typing.Any]] = None) -> typing.Iterator[typing.Tuple[datetime.datetime, str]]:
        """
        Return an iterator over (utc_timestamp, logline) tuples.
        
        Parameters
        ----------
        stream : str
            Either 'stdout' or 'stderr'.
        as_unicode : bool, default: True
            If as_unicode=False, each logline is returned as a byte object. Otherwise,
            it is returned as a (unicode) string.
        
        Yields
        ------
        Tuple[datetime, str]
            Tuple of timestamp, logline pairs.
        """
        ...
    def __iter__(self) -> typing.Iterator[metaflow.client.core.DataArtifact]:
        """
        Iterate over all children DataArtifact of this Task
        
        Yields
        ------
        DataArtifact
            A DataArtifact in this Step
        """
        ...
    def __getitem__(self, name: str) -> DataArtifact:
        """
        Returns the DataArtifact object with the artifact name 'name'
        
        Parameters
        ----------
        name : str
            Data artifact name
        
        Returns
        -------
        DataArtifact
            DataArtifact for this artifact name in this task
        
        Raises
        ------
        KeyError
            If the name does not identify a valid DataArtifact object
        """
        ...
    def __getstate__(self):
        ...
    def __setstate__(self, state):
        ...
    ...

class Step(MetaflowObject, metaclass=type):
    """
    A `Step` represents a user-defined step, that is, a method annotated with the `@step` decorator.
    
    It contains `Task` objects associated with the step, that is, all executions of the
    `Step`. The step may contain multiple `Task`s in the case of a foreach step.
    
    Attributes
    ----------
    task : Task
        The first `Task` object in this step. This is a shortcut for retrieving the only
        task contained in a non-foreach step.
    finished_at : datetime
        Time when the latest `Task` of this step finished. Note that in the case of foreaches,
        this time may change during execution of the step.
    environment_info : Dict[str, Any]
        Information about the execution environment.
    """
    @property
    def task(self) -> typing.Optional[metaflow.client.core.Task]:
        """
        Returns a Task object belonging to this step.
        
        This is useful when the step only contains one task (a linear step for example).
        
        Returns
        -------
        Task
            A task in the step
        """
        ...
    def tasks(self, *tags: str) -> typing.Iterable[metaflow.client.core.Task]:
        """
        [Legacy function - do not use]
        
        Returns an iterator over all `Task` objects in the step. This is an alias
        to iterating the object itself, i.e.
        ```
        list(Step(...)) == list(Step(...).tasks())
        ```
        
        Parameters
        ----------
        tags : str
            No op (legacy functionality)
        
        Yields
        ------
        Task
            `Task` objects in this step.
        """
        ...
    @property
    def control_task(self) -> typing.Optional[metaflow.client.core.Task]:
        """
        [Unpublished API - use with caution!]
        
        Returns a Control Task object belonging to this step.
        This is useful when the step only contains one control task.
        
        Returns
        -------
        Task
            A control task in the step
        """
        ...
    def control_tasks(self, *tags: str) -> typing.Iterator[metaflow.client.core.Task]:
        """
        [Unpublished API - use with caution!]
        
        Returns an iterator over all the control tasks in the step.
        An optional filter is available that allows you to filter on tags. The
        control tasks returned if the filter is specified will contain all the
        tags specified.
        Parameters
        ----------
        tags : str
            Tags to match
        
        Yields
        ------
        Task
            Control Task objects for this step
        """
        ...
    def __iter__(self) -> typing.Iterator[metaflow.client.core.Task]:
        """
        Iterate over all children Task of this Step
        
        Yields
        ------
        Task
            A Task in this Step
        """
        ...
    def __getitem__(self, task_id: str) -> Task:
        """
        Returns the Task object with the task ID 'task_id'
        
        Parameters
        ----------
        task_id : str
            Task ID
        
        Returns
        -------
        Task
            Task for this task ID in this Step
        
        Raises
        ------
        KeyError
            If the task_id does not identify a valid Task object
        """
        ...
    def __getstate__(self):
        ...
    def __setstate__(self, state):
        ...
    @property
    def finished_at(self) -> typing.Optional[datetime.datetime]:
        """
        Returns the datetime object of when the step finished (successfully or not).
        
        A step is considered finished when all the tasks that belong to it have
        finished. This call will return None if the step has not finished
        
        Returns
        -------
        datetime
            Datetime of when the step finished
        """
        ...
    @property
    def environment_info(self) -> typing.Optional[typing.Dict[str, typing.Any]]:
        """
        Returns information about the environment that was used to execute this step. As an
        example, if the Conda environment is selected, this will return information about the
        dependencies that were used in the environment.
        
        This environment information is only available for steps that have tasks
        for which the code package has been saved.
        
        Returns
        -------
        Dict[str, Any], optional
            Dictionary describing the environment
        """
        ...
    @property
    def parent_steps(self) -> typing.Iterator["Step"]:
        """
        Yields parent steps for the current step.
        
        Yields
        ------
        Step
            Parent step
        """
        ...
    @property
    def child_steps(self) -> typing.Iterator["Step"]:
        """
        Yields child steps for the current step.
        
        Yields
        ------
        Step
            Child step
        """
        ...
    ...

class Run(MetaflowObject, metaclass=type):
    """
    A `Run` represents an execution of a `Flow`. It is a container of `Step`s.
    
    Attributes
    ----------
    data : MetaflowData
        a shortcut to run['end'].task.data, i.e. data produced by this run.
    successful : bool
        True if the run completed successfully.
    finished : bool
        True if the run completed.
    finished_at : datetime
        Time this run finished.
    code : MetaflowCode
        Code package for this run (if present). See `MetaflowCode`.
    trigger : MetaflowTrigger
        Information about event(s) that triggered this run (if present). See `MetaflowTrigger`.
    end_task : Task
        `Task` for the end step (if it is present already).
    """
    def steps(self, *tags: str) -> typing.Iterator[metaflow.client.core.Step]:
        """
        [Legacy function - do not use]
        
        Returns an iterator over all `Step` objects in the step. This is an alias
        to iterating the object itself, i.e.
        ```
        list(Run(...)) == list(Run(...).steps())
        ```
        
        Parameters
        ----------
        tags : str
            No op (legacy functionality)
        
        Yields
        ------
        Step
            `Step` objects in this run.
        """
        ...
    @property
    def code(self) -> typing.Optional[metaflow.client.core.MetaflowCode]:
        """
        Returns the MetaflowCode object for this run, if present.
        Code is packed if atleast one `Step` runs remotely, else None is returned.
        
        Returns
        -------
        MetaflowCode, optional
            Code package for this run
        """
        ...
    @property
    def data(self) -> typing.Optional[metaflow.client.core.MetaflowData]:
        """
        Returns a container of data artifacts produced by this run.
        
        You can access data produced by this run as follows:
        ```
        print(run.data.my_var)
        ```
        This is a shorthand for `run['end'].task.data`. If the 'end' step has not yet
        executed, returns None.
        
        Returns
        -------
        MetaflowData, optional
            Container of all artifacts produced by this task
        """
        ...
    @property
    def successful(self) -> bool:
        """
        Indicates whether or not the run completed successfully.
        
        A run is successful if its 'end' step is successful.
        
        Returns
        -------
        bool
            True if the run completed successfully and False otherwise
        """
        ...
    @property
    def finished(self) -> bool:
        """
        Indicates whether or not the run completed.
        
        A run completed if its 'end' step completed.
        
        Returns
        -------
        bool
            True if the run completed and False otherwise
        """
        ...
    @property
    def finished_at(self) -> typing.Optional[datetime.datetime]:
        """
        Returns the datetime object of when the run finished (successfully or not).
        
        The completion time of a run is the same as the completion time of its 'end' step.
        If the 'end' step has not completed, returns None.
        
        Returns
        -------
        datetime, optional
            Datetime of when the run finished
        """
        ...
    @property
    def end_task(self) -> typing.Optional[metaflow.client.core.Task]:
        """
        Returns the Task corresponding to the 'end' step.
        
        This returns None if the end step does not yet exist.
        
        Returns
        -------
        Task, optional
            The 'end' task
        """
        ...
    def add_tag(self, tag: str):
        """
        Add a tag to this `Run`.
        
        Note that if the tag is already a system tag, it is not added as a user tag,
        and no error is thrown.
        
        Parameters
        ----------
        tag : str
            Tag to add.
        """
        ...
    def add_tags(self, tags: typing.Iterable[str]):
        """
        Add one or more tags to this `Run`.
        
        Note that if any tag is already a system tag, it is not added as a user tag
        and no error is thrown.
        
        Parameters
        ----------
        tags : Iterable[str]
            Tags to add.
        """
        ...
    def remove_tag(self, tag: str):
        """
        Remove one tag from this `Run`.
        
        Removing a system tag is an error. Removing a non-existent
        user tag is a no-op.
        
        Parameters
        ----------
        tag : str
            Tag to remove.
        """
        ...
    def remove_tags(self, tags: typing.Iterable[str]):
        """
        Remove one or more tags to this `Run`.
        
        Removing a system tag will result in an error. Removing a non-existent
        user tag is a no-op.
        
        Parameters
        ----------
        tags : Iterable[str]
            Tags to remove.
        """
        ...
    def replace_tag(self, tag_to_remove: str, tag_to_add: str):
        """
        Remove a tag and add a tag atomically. Removal is done first.
        The rules for `Run.add_tag` and `Run.remove_tag` also apply here.
        
        Parameters
        ----------
        tag_to_remove : str
            Tag to remove.
        tag_to_add : str
            Tag to add.
        """
        ...
    def replace_tags(self, tags_to_remove: typing.Iterable[str], tags_to_add: typing.Iterable[str]):
        """
        Remove and add tags atomically; the removal is done first.
        The rules for `Run.add_tag` and `Run.remove_tag` also apply here.
        
        Parameters
        ----------
        tags_to_remove : Iterable[str]
            Tags to remove.
        tags_to_add : Iterable[str]
            Tags to add.
        """
        ...
    def __iter__(self) -> typing.Iterator[metaflow.client.core.Step]:
        """
        Iterate over all children Step of this Run
        
        Yields
        ------
        Step
            A Step in this Run
        """
        ...
    def __getitem__(self, name: str) -> Step:
        """
        Returns the Step object with the step name 'name'
        
        Parameters
        ----------
        name : str
            Step name
        
        Returns
        -------
        Step
            Step for this step name in this Run
        
        Raises
        ------
        KeyError
            If the name does not identify a valid Step object
        """
        ...
    def __getstate__(self):
        ...
    def __setstate__(self, state):
        ...
    @property
    def trigger(self) -> typing.Optional[metaflow.events.Trigger]:
        """
        Returns a container of events that triggered this run.
        
        This returns None if the run was not triggered by any events.
        
        Returns
        -------
        Trigger, optional
            Container of triggering events
        """
        ...
    ...

class Flow(MetaflowObject, metaclass=type):
    """
    A Flow represents all existing flows with a certain name, in other words,
    classes derived from `FlowSpec`. A container of `Run` objects.
    
    Attributes
    ----------
    latest_run : Run
        Latest `Run` (in progress or completed, successfully or not) of this flow.
    latest_successful_run : Run
        Latest successfully completed `Run` of this flow.
    """
    def __init__(self, *args, **kwargs):
        ...
    @property
    def latest_run(self) -> typing.Optional[metaflow.client.core.Run]:
        """
        Returns the latest run (either in progress or completed) of this flow.
        
        Note that an in-progress run may be returned by this call. Use latest_successful_run
        to get an object representing a completed successful run.
        
        Returns
        -------
        Run, optional
            Latest run of this flow
        """
        ...
    @property
    def latest_successful_run(self) -> typing.Optional[metaflow.client.core.Run]:
        """
        Returns the latest successful run of this flow.
        
        Returns
        -------
        Run, optional
            Latest successful run of this flow
        """
        ...
    def runs(self, *tags: str) -> typing.Iterator[metaflow.client.core.Run]:
        """
        Returns an iterator over all `Run`s of this flow.
        
        An optional filter is available that allows you to filter on tags.
        If multiple tags are specified, only runs that have all the
        specified tags are returned.
        
        Parameters
        ----------
        tags : str
            Tags to match.
        
        Yields
        ------
        Run
            `Run` objects in this flow.
        """
        ...
    def __iter__(self) -> typing.Iterator[metaflow.client.core.Task]:
        """
        Iterate over all children Run of this Flow.
        
        Note that only runs in the current namespace are returned unless
        _namespace_check is False
        
        Yields
        ------
        Run
            A Run in this Flow
        """
        ...
    def __getitem__(self, run_id: str) -> Run:
        """
        Returns the Run object with the run ID 'run_id'
        
        Parameters
        ----------
        run_id : str
            Run OD
        
        Returns
        -------
        Run
            Run for this run ID in this Flow
        
        Raises
        ------
        KeyError
            If the run_id does not identify a valid Run object
        """
        ...
    def __getstate__(self):
        ...
    def __setstate__(self, state):
        ...
    ...

class Metaflow(object, metaclass=type):
    """
    Entry point to all objects in the Metaflow universe.
    
    This object can be used to list all the flows present either through the explicit property
    or by iterating over this object.
    
    Attributes
    ----------
    flows : List[Flow]
        Returns the list of all `Flow` objects known to this metadata provider. Note that only
        flows present in the current namespace will be returned. A `Flow` is present in a namespace
        if it has at least one run in the namespace.
    """
    def __init__(self, _current_metadata: typing.Optional[str] = None):
        ...
    @property
    def flows(self) -> typing.List[metaflow.client.core.Flow]:
        """
        Returns a list of all the flows present.
        
        Only flows present in the set namespace are returned. A flow is present in a namespace if
        it has at least one run that is in the namespace.
        
        Returns
        -------
        List[Flow]
            List of all flows present.
        """
        ...
    def __iter__(self) -> typing.Iterator[metaflow.client.core.Flow]:
        """
        Iterator over all flows present.
        
        Only flows present in the set namespace are returned. A flow is present in a
        namespace if it has at least one run that is in the namespace.
        
        Yields
        -------
        Flow
            A Flow present in the Metaflow universe.
        """
        ...
    def __str__(self) -> str:
        ...
    def __getitem__(self, name: str) -> Flow:
        """
        Returns a specific flow by name.
        
        The flow will only be returned if it is present in the current namespace.
        
        Parameters
        ----------
        name : str
            Name of the Flow
        
        Returns
        -------
        Flow
            Flow with the given name.
        """
        ...
    ...

