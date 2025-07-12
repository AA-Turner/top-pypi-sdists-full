######################################################################################################
#                                 Auto-generated Metaflow stub file                                  #
# MF version: 2.15.21.1+obcheckpoint(0.2.4);ob(v1)                                                   #
# Generated on 2025-07-11T23:29:18.667292                                                            #
######################################################################################################

from __future__ import annotations

import typing
if typing.TYPE_CHECKING:
    import metaflow
    import metaflow.mf_extensions.obcheckpoint.plugins.machine_learning_utilities.checkpoints.decorator
    import metaflow.mf_extensions.obcheckpoint.plugins.machine_learning_utilities.modeling_utils.core
    import metaflow.mf_extensions.obcheckpoint.plugins.machine_learning_utilities.hf_hub.decorator
    import metaflow.mf_extensions.outerbounds.plugins.apps.core
    import typing
    import metaflow.events
    import metaflow.metaflow_current
    import metaflow.plugins.cards.component_serializer


TYPE_CHECKING: bool

TEMPDIR: str

class Parallel(tuple, metaclass=type):
    """
    Parallel(main_ip, num_nodes, node_index, control_task_id)
    """
    @staticmethod
    def __new__(_cls, main_ip, num_nodes, node_index, control_task_id):
        """
        Create new instance of Parallel(main_ip, num_nodes, node_index, control_task_id)
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

class Current(object, metaclass=type):
    def __init__(self):
        ...
    def __contains__(self, key: str):
        ...
    def get(self, key: str, default = None) -> typing.Optional[typing.Any]:
        ...
    @property
    def is_running_flow(self) -> bool:
        """
        Returns True if called inside a running Flow, False otherwise.
        
        You can use this property e.g. inside a library to choose the desired
        behavior depending on the execution context.
        
        Returns
        -------
        bool
            True if called inside a run, False otherwise.
        """
        ...
    @property
    def flow_name(self) -> typing.Optional[str]:
        """
        The name of the currently executing flow.
        
        Returns
        -------
        str, optional
            Flow name.
        """
        ...
    @property
    def run_id(self) -> typing.Optional[str]:
        """
        The run ID of the currently executing run.
        
        Returns
        -------
        str, optional
            Run ID.
        """
        ...
    @property
    def step_name(self) -> typing.Optional[str]:
        """
        The name of the currently executing step.
        
        Returns
        -------
        str, optional
            Step name.
        """
        ...
    @property
    def task_id(self) -> typing.Optional[str]:
        """
        The task ID of the currently executing task.
        
        Returns
        -------
        str, optional
            Task ID.
        """
        ...
    @property
    def retry_count(self) -> int:
        """
        The index of the task execution attempt.
        
        This property returns 0 for the first attempt to execute the task.
        If the @retry decorator is used and the first attempt fails, this
        property returns the number of times the task was attempted prior
        to the current attempt.
        
        Returns
        -------
        int
            The retry count.
        """
        ...
    @property
    def origin_run_id(self) -> typing.Optional[str]:
        """
        The run ID of the original run this run was resumed from.
        
        This property returns None for ordinary runs. If the run
        was started by the resume command, the property returns
        the ID of the original run.
        
        You can use this property to detect if the run is resumed
        or not.
        
        Returns
        -------
        str, optional
            Run ID of the original run.
        """
        ...
    @property
    def pathspec(self) -> typing.Optional[str]:
        """
        Pathspec of the current task, i.e. a unique
        identifier of the current task. The returned
        string follows this format:
        ```
        {flow_name}/{run_id}/{step_name}/{task_id}
        ```
        
        This is a shorthand to `current.task.pathspec`.
        
        Returns
        -------
        str, optional
            Pathspec.
        """
        ...
    @property
    def task(self) -> typing.Optional["metaflow.Task"]:
        """
        Task object of the current task.
        
        Returns
        -------
        Task, optional
            Current task.
        """
        ...
    @property
    def run(self) -> typing.Optional["metaflow.Run"]:
        """
        Run object of the current run.
        
        Returns
        -------
        Run, optional
            Current run.
        """
        ...
    @property
    def namespace(self) -> str:
        """
        The current namespace.
        
        Returns
        -------
        str
            Namespace.
        """
        ...
    @property
    def username(self) -> typing.Optional[str]:
        """
        The name of the user who started the run, if available.
        
        Returns
        -------
        str, optional
            User name.
        """
        ...
    @property
    def tags(self):
        """
        [Legacy function - do not use]
        
        Access tags through the Run object instead.
        """
        ...
    @property
    def tempdir(self) -> typing.Optional[str]:
        """
        Currently configured temporary directory.
        
        Returns
        -------
        str, optional
            Temporary director.
        """
        ...
    @property
    def graph(self):
        ...
    @property
    def apps(self) -> "metaflow.mf_extensions.outerbounds.plugins.apps.core.apps":
        """
        (only in the presence of the @app_deploy decorator)
        
        
        Returns
        ----------
        apps
            The object carrying the Deployer class to deploy apps.
        """
        ...
    @property
    def checkpoint(self) -> "metaflow.mf_extensions.obcheckpoint.plugins.machine_learning_utilities.checkpoints.decorator.CurrentCheckpointer":
        """
        (only in the presence of the @checkpoint decorator)
        
        The `@checkpoint` decorator makes saving/loading checkpoints available through the `current.checkpoint`.
        The object exposes `save`/`load`/`list` methods for saving/loading checkpoints.
        
        You can check if a checkpoint is loaded by `current.checkpoint.is_loaded` and get the checkpoint information
        by using `current.checkpoint.info`. The `current.checkpoint.directory` returns the path to the checkpoint directory
        where the checkpoint maybe loaded or saved.
        
        Returns
        ----------
        CurrentCheckpointer
            The object for handling checkpointing within a step.
        """
        ...
    @property
    def card(self) -> "metaflow.plugins.cards.component_serializer.CardComponentCollector":
        """
        (only in the presence of the @card decorator)
        
        The `@card` decorator makes the cards available through the `current.card`
        object. If multiple `@card` decorators are present, you can add an `ID` to
        distinguish between them using `@card(id=ID)` as the decorator. You will then
        be able to access that specific card using `current.card[ID].
        
        Methods available are `append` and `extend`
        
        Returns
        -------
        CardComponentCollector
            The or one of the cards attached to this step.
        """
        ...
    @property
    def parallel(self) -> "metaflow.metaflow_current.Parallel":
        """
        (only in the presence of the @parallel decorator)
        
        Returns a namedtuple with relevant information about the parallel task.
        
        Returns
        -------
        Parallel
            `namedtuple` with the following fields:
                - main_ip (`str`)
                    The IP address of the control task.
                - num_nodes (`int`)
                    The total number of tasks created by @parallel
                - node_index (`int`)
                    The index of the current task in all the @parallel tasks.
                - control_task_id (`Optional[str]`)
                    The task ID of the control task. Available to all tasks.
        """
        ...
    @property
    def is_parallel(self) -> bool:
        """
        (only in the presence of the @parallel decorator)
        
        True if the current step is a @parallel step.
        """
        ...
    @property
    def model(self) -> "metaflow.mf_extensions.obcheckpoint.plugins.machine_learning_utilities.modeling_utils.core.ModelSerializer":
        """
        (only in the presence of the @model decorator)
        
        The object used for loading / saving models.
        `current.model` exposes a `save` method to save models and a `load` method to load models.
        `current.model.loaded` exposes the paths to the models loaded via the `load` argument in the @model decorator
        or models loaded via `current.model.load`.
        
        Returns
        ----------
        ModelSerializer
            The object used for loading / saving models.
        """
        ...
    @property
    def huggingface_hub(self) -> "metaflow.mf_extensions.obcheckpoint.plugins.machine_learning_utilities.hf_hub.decorator.HuggingfaceRegistry":
        """
        (only in the presence of the @huggingface_hub decorator)
        
        
        The `@huggingface_hub` injects a `huggingface_hub` object into the `current` object. This object provides syntactic sugar over [huggingface_hub](https://github.com/huggingface/huggingface_hub)'s [snapshot_download](https://huggingface.co/docs/huggingface_hub/main/en/package_reference/file_download#huggingface_hub.snapshot_download) function. The `current.huggingface_hub.snapshot_download` function downloads objects from huggingface hub and saves them to the Metaflow's datastore under the `<repo_type>/<repo_id>` name. The `repo_type` is by default `model` and can be overriden by passing the `repo_type` parameter to the `snapshot_download` function.
        """
        ...
    @property
    def project_name(self) -> str:
        """
        (only in the presence of the @project decorator)
        
        The name of the project assigned to this flow, i.e. `X` in `@project(name=X)`.
        
        Returns
        -------
        str
            Project name.
        """
        ...
    @property
    def project_flow_name(self) -> str:
        """
        (only in the presence of the @project decorator)
        
        The flow name prefixed with the current project and branch. This name identifies
        the deployment on a production scheduler.
        
        Returns
        -------
        str
            Flow name prefixed with project information.
        """
        ...
    @property
    def branch_name(self) -> str:
        """
        (only in the presence of the @project decorator)
        
        The current branch, i.e. `X` in `--branch=X` set during deployment or run.
        
        Returns
        -------
        str
            Branch name.
        """
        ...
    @property
    def is_user_branch(self) -> bool:
        """
        (only in the presence of the @project decorator)
        
        True if the flow is deployed without a specific `--branch` or a `--production`
        flag.
        
        Returns
        -------
        bool
            True if the deployment does not correspond to a specific branch.
        """
        ...
    @property
    def is_production(self) -> bool:
        """
        (only in the presence of the @project decorator)
        
        True if the flow is deployed with the `--production` flag
        
        Returns
        -------
        bool
            True if the flow is deployed with `--production`.
        """
        ...
    @property
    def trigger(self) -> "metaflow.events.Trigger":
        """
        (only in the presence of the @trigger, or @trigger_on_finish decorators)
        
        Returns `Trigger` if the current run is triggered by an event
        
        Returns
        -------
        Trigger
            `Trigger` if triggered by an event
        """
        ...
    ...

current: Current

