######################################################################################################
#                                 Auto-generated Metaflow stub file                                  #
# MF version: 2.19.29.2+obcheckpoint(0.2.10);<unk>(<unk>);ob(v1)                                     #
# Generated on 2026-05-21T21:10:55.250643                                                            #
######################################################################################################

from __future__ import annotations

import enum
import typing
if typing.TYPE_CHECKING:
    import metaflow.system_context
    import enum
    import typing


TYPE_CHECKING: bool

class ExecutionPhase(enum.Enum, metaclass=enum.EnumType):
    """
    Represents which process phase Metaflow is currently executing in.
    
    Metaflow can execute across up to three separate processes:
    
    LAUNCH: The initial `myflow.py` process. This is where the flow is parsed,
        decorators are initialized, code is packaged, and (for local runs) the
        runtime scheduler operates. Hooks called here are:
          - For FlowDecorators: `flow_init`
          - For StepDecorators: `step_init`, `package_init`, `runtime_*`
        For deployment commands (e.g. `argo-workflows create`), only `flow_init`,
        `step_init` and `package_init` are called.
    
    TRAMPOLINE: A per-task subprocess that delegates execution to a remote system
        (e.g. AWS Batch, Kubernetes). Hooks called here are:
          - For FlowDecorators: `flow_init`
          - For StepDecorators: `step_init`
        This phase does NOT exist for local
        runs (where the subprocess directly executes user code) or for Argo/Step
        Functions deployments (where the orchestrator launches tasks directly).
    
    TASK: The process where user code actually runs. Hooks called here are:
           - For FlowDecorators: `flow_init`
           - For StepDecorators: `step_init`, `task_*`
        For local runs, this is the per-task subprocess. For remote runs, this is
        the process running on Batch/Kubernetes/etc.
    """
    def __new__(cls, value):
        ...
    ...

class SystemContext(object, metaclass=type):
    """
    Singleton holding infrastructure/system data and the current execution phase.
    
    This object is created once per process and progressively populated by the
    runtime as information becomes available. Decorators access it via the
    ``system_ctx`` property on the decorator base class.
    
    1. **Phase awareness**: decorators can check which execution phase they are
       in, allowing the same hook implementation (e.g. ``step_init``) to behave
       differently in the launch process vs. a task subprocess.
    
    2. **Progressive updates**: the runtime system calls ``_update()`` to add
       information as it becomes available (e.g. ``run_id`` is set at
       ``runtime_init`` time, ``task_id`` at ``task_pre_step`` time).
    """
    def __init__(self):
        ...
    @property
    def phase(self) -> ExecutionPhase:
        """
        The current :class:`ExecutionPhase`.
        """
        ...
    @property
    def is_launch(self) -> bool:
        """
        True if executing in the initial CLI / orchestrator process.
        """
        ...
    @property
    def is_trampoline(self) -> bool:
        """
        True if executing in a per-task subprocess that delegates remotely.
        """
        ...
    @property
    def is_task(self) -> bool:
        """
        True if executing in the process where user code runs.
        """
        ...
    @property
    def flow(self) -> typing.Union[typing.Any, None]:
        """
        The FlowSpec instance (available after ``flow_init``).
        """
        ...
    @property
    def graph(self) -> typing.Union[typing.Any, None]:
        """
        The FlowGraph (available after ``flow_init``).
        """
        ...
    @property
    def environment(self) -> typing.Union[typing.Any, None]:
        """
        The MetaflowEnvironment instance.
        """
        ...
    @property
    def flow_datastore(self) -> typing.Union[typing.Any, None]:
        """
        The FlowDataStore instance.
        """
        ...
    @property
    def logger(self) -> typing.Union[typing.Callable[..., typing.Any], None]:
        """
        The logger callable.
        """
        ...
    @property
    def metadata(self) -> typing.Union[typing.Any, None]:
        """
        The metadata provider.
        """
        ...
    @property
    def input_paths(self) -> typing.Union[typing.List[str], None]:
        """
        List of input pathspec strings (available after ``runtime_task_created``).
        """
        ...
    @property
    def package(self) -> typing.Union[typing.Any, None]:
        """
        The code package (available after ``runtime_init``, LAUNCH only).
        """
        ...
    @property
    def run_id(self) -> typing.Union[str, None]:
        """
        The run ID (available after ``runtime_init`` or ``task_pre_step``).
        """
        ...
    @property
    def task_id(self) -> typing.Union[str, None]:
        """
        The task ID (available during task hooks).
        """
        ...
    @property
    def task_datastore(self) -> typing.Union[typing.Any, None]:
        """
        The task's output datastore (available during task hooks).
        """
        ...
    @property
    def retry_count(self) -> typing.Union[int, None]:
        """
        Current retry attempt number (available during task hooks).
        """
        ...
    @property
    def max_user_code_retries(self) -> typing.Union[int, None]:
        """
        Maximum user code retries configured (available during task hooks).
        """
        ...
    @property
    def ubf_context(self) -> typing.Union[typing.Any, None]:
        """
        Unbounded foreach context (available during task hooks).
        """
        ...
    @property
    def is_cloned(self) -> typing.Union[bool, None]:
        """
        Whether the task is resumed from a prior run (available after ``runtime_task_created``).
        """
        ...
    @property
    def inputs(self) -> typing.Union[typing.List[typing.Any], None]:
        """
        List of input datastores (available during task hooks).
        """
        ...
    @property
    def split_index(self) -> typing.Union[int, None]:
        """
        Foreach split index (available during task hooks).
        """
        ...
    def register_step_decorators(self, step_name: str, decorators: typing.List[typing.Any]):
        """
        Register the list of decorator instances for a step.
        """
        ...
    def get_step_decorators(self, step_name: str) -> typing.List[typing.Any]:
        """
        Return the decorator instances for a step.
        """
        ...
    def publish(self, step_name: str, namespace: str, key: str, value: typing.Any):
        """
        Publish a value for other decorators to read.
        
        By convention, use the decorator's ``name`` as the namespace to avoid
        collisions. The value is scoped to the given step.
        
        Parameters
        ----------
        step_name : str
            The step this value is scoped to.
        namespace : str
            Typically the publishing decorator's name.
        key : str
            Identifier for the value within the namespace.
        value : any
            The value to publish.
        """
        ...
    def get_published(self, step_name: str, namespace: str, key: str, default: typing.Any = None) -> typing.Any:
        """
        Read a value published by another decorator.
        
        Parameters
        ----------
        step_name : str
            The step to look up.
        namespace : str
            The publishing decorator's namespace.
        key : str
            The key to look up.
        default : any
            Returned if the namespace or key is not found.
        
        Returns
        -------
        any
        """
        ...
    def has_published(self, step_name: str, namespace: str, key: typing.Union[str, None] = None) -> bool:
        """
        Check whether a decorator has published data.
        
        Parameters
        ----------
        step_name : str
            The step to look up.
        namespace : str
        key : str or None
            If None, checks whether the namespace exists at all.
        
        Returns
        -------
        bool
        """
        ...
    def get_all_published(self, step_name: str, namespace: str) -> typing.Dict[str, typing.Any]:
        """
        Return all key-value pairs published under a namespace.
        
        Parameters
        ----------
        step_name : str
            The step to look up.
        namespace : str
        
        Returns
        -------
        dict
        """
        ...
    ...

system_context: SystemContext

