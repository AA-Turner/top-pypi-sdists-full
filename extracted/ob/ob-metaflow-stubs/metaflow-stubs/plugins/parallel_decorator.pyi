######################################################################################################
#                                 Auto-generated Metaflow stub file                                  #
# MF version: 2.15.17.1+obcheckpoint(0.2.1);ob(v1)                                                   #
# Generated on 2025-06-16T20:11:02.899747                                                            #
######################################################################################################

from __future__ import annotations

import metaflow
import typing
if typing.TYPE_CHECKING:
    import metaflow.decorators

from ..exception import MetaflowException as MetaflowException
from ..metadata_provider.metadata import MetaDatum as MetaDatum
from ..metaflow_current import current as current
from ..metaflow_current import Parallel as Parallel

UBF_CONTROL: str

CONTROL_TASK_TAG: str

class ParallelDecorator(metaflow.decorators.StepDecorator, metaclass=type):
    """
    MF Add To Current
    -----------------
    parallel -> metaflow.metaflow_current.Parallel
        Returns a namedtuple with relevant information about the parallel task.
    
        @@ Returns
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
    
    is_parallel -> bool
        True if the current step is a @parallel step.
    """
    def __init__(self, attributes = None, statically_defined = False):
        ...
    def runtime_step_cli(self, cli_args, retry_count, max_user_code_retries, ubf_context):
        ...
    def step_init(self, flow, graph, step_name, decorators, environment, flow_datastore, logger):
        ...
    def task_pre_step(self, step_name, task_datastore, metadata, run_id, task_id, flow, graph, retry_count, max_user_code_retries, ubf_context, inputs):
        ...
    def task_decorate(self, step_func, flow, graph, retry_count, max_user_code_retries, ubf_context):
        ...
    def setup_distributed_env(self, flow):
        ...
    ...

