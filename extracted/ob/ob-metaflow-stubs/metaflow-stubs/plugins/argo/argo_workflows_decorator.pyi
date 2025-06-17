######################################################################################################
#                                 Auto-generated Metaflow stub file                                  #
# MF version: 2.15.17.1+obcheckpoint(0.2.1);ob(v1)                                                   #
# Generated on 2025-06-16T20:11:02.929703                                                            #
######################################################################################################

from __future__ import annotations

import metaflow
import typing
if typing.TYPE_CHECKING:
    import metaflow.graph
    import metaflow.flowspec
    import metaflow.decorators

from ...metaflow_current import current as current
from ...events import Trigger as Trigger
from ...metadata_provider.metadata import MetaDatum as MetaDatum
from ...flowspec import FlowSpec as FlowSpec
from .argo_events import ArgoEvent as ArgoEvent

class ArgoWorkflowsInternalDecorator(metaflow.decorators.StepDecorator, metaclass=type):
    def task_pre_step(self, step_name, task_datastore, metadata, run_id, task_id, flow, graph, retry_count, max_user_code_retries, ubf_context, inputs):
        ...
    def task_finished(self, step_name, flow: metaflow.flowspec.FlowSpec, graph: metaflow.graph.FlowGraph, is_task_ok, retry_count, max_user_code_retries):
        ...
    ...

