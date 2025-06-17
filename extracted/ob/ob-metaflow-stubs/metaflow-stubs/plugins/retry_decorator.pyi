######################################################################################################
#                                 Auto-generated Metaflow stub file                                  #
# MF version: 2.15.17.1+obcheckpoint(0.2.1);ob(v1)                                                   #
# Generated on 2025-06-16T20:11:02.901819                                                            #
######################################################################################################

from __future__ import annotations

import metaflow
import typing
if typing.TYPE_CHECKING:
    import metaflow.decorators

from ..exception import MetaflowException as MetaflowException

MAX_ATTEMPTS: int

class RetryDecorator(metaflow.decorators.StepDecorator, metaclass=type):
    """
    Specifies the number of times the task corresponding
    to a step needs to be retried.
    
    This decorator is useful for handling transient errors, such as networking issues.
    If your task contains operations that can't be retried safely, e.g. database updates,
    it is advisable to annotate it with `@retry(times=0)`.
    
    This can be used in conjunction with the `@catch` decorator. The `@catch`
    decorator will execute a no-op task after all retries have been exhausted,
    ensuring that the flow execution can continue.
    
    Parameters
    ----------
    times : int, default 3
        Number of times to retry this task.
    minutes_between_retries : int, default 2
        Number of minutes between retries.
    """
    def step_init(self, flow, graph, step, decos, environment, flow_datastore, logger):
        ...
    def step_task_retry_count(self):
        ...
    ...

