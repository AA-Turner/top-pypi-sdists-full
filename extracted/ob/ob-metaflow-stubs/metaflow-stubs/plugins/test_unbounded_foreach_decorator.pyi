######################################################################################################
#                                 Auto-generated Metaflow stub file                                  #
# MF version: 2.15.17.1+obcheckpoint(0.2.1);ob(v1)                                                   #
# Generated on 2025-06-16T20:11:02.898136                                                            #
######################################################################################################

from __future__ import annotations

import metaflow
import typing
if typing.TYPE_CHECKING:
    import metaflow.unbounded_foreach
    import metaflow.decorators

from ..exception import MetaflowException as MetaflowException
from ..metadata_provider.metadata import MetaDatum as MetaDatum

UBF_CONTROL: str

UBF_TASK: str

CONTROL_TASK_TAG: str

class InternalTestUnboundedForeachInput(metaflow.unbounded_foreach.UnboundedForeachInput, metaclass=type):
    """
    Test class that wraps around values (any iterator) and simulates an
    unbounded-foreach instead of a bounded foreach.
    """
    def __init__(self, iterable):
        ...
    def __iter__(self):
        ...
    def __next__(self):
        ...
    def __getitem__(self, key):
        ...
    def __len__(self):
        ...
    def __str__(self):
        ...
    def __repr__(self):
        ...
    ...

class InternalTestUnboundedForeachDecorator(metaflow.decorators.StepDecorator, metaclass=type):
    def __init__(self, attributes = None, statically_defined = False):
        ...
    def step_init(self, flow, graph, step_name, decorators, environment, flow_datastore, logger):
        ...
    def task_pre_step(self, step_name, task_datastore, metadata, run_id, task_id, flow, graph, retry_count, max_user_code_retries, ubf_context, inputs):
        ...
    def control_task_step_func(self, flow, graph, retry_count):
        ...
    def task_decorate(self, step_func, flow, graph, retry_count, max_user_code_retries, ubf_context):
        ...
    def step_task_retry_count(self):
        ...
    ...

