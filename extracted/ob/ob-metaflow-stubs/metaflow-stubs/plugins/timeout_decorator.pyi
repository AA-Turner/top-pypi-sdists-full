######################################################################################################
#                                 Auto-generated Metaflow stub file                                  #
# MF version: 2.15.17.1+obcheckpoint(0.2.1);ob(v1)                                                   #
# Generated on 2025-06-16T20:11:02.900536                                                            #
######################################################################################################

from __future__ import annotations

import metaflow
import typing
if typing.TYPE_CHECKING:
    import metaflow.exception
    import metaflow.decorators

from ..exception import MetaflowException as MetaflowException

UBF_CONTROL: str

DEFAULT_RUNTIME_LIMIT: int

class TimeoutException(metaflow.exception.MetaflowException, metaclass=type):
    ...

class TimeoutDecorator(metaflow.decorators.StepDecorator, metaclass=type):
    """
    Specifies a timeout for your step.
    
    This decorator is useful if this step may hang indefinitely.
    
    This can be used in conjunction with the `@retry` decorator as well as the `@catch` decorator.
    A timeout is considered to be an exception thrown by the step. It will cause the step to be
    retried if needed and the exception will be caught by the `@catch` decorator, if present.
    
    Note that all the values specified in parameters are added together so if you specify
    60 seconds and 1 hour, the decorator will have an effective timeout of 1 hour and 1 minute.
    
    Parameters
    ----------
    seconds : int, default 0
        Number of seconds to wait prior to timing out.
    minutes : int, default 0
        Number of minutes to wait prior to timing out.
    hours : int, default 0
        Number of hours to wait prior to timing out.
    """
    def init(self):
        ...
    def step_init(self, flow, graph, step, decos, environment, flow_datastore, logger):
        ...
    def task_pre_step(self, step_name, task_datastore, metadata, run_id, task_id, flow, graph, retry_count, max_user_code_retries, ubf_context, inputs):
        ...
    def task_post_step(self, step_name, flow, graph, retry_count, max_user_code_retries):
        ...
    ...

def get_run_time_limit_for_task(step_decos):
    ...

