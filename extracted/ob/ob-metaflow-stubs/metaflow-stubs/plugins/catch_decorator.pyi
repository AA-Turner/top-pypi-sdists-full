######################################################################################################
#                                 Auto-generated Metaflow stub file                                  #
# MF version: 2.15.17.1+obcheckpoint(0.2.1);ob(v1)                                                   #
# Generated on 2025-06-16T20:11:02.901189                                                            #
######################################################################################################

from __future__ import annotations

import metaflow
import typing
if typing.TYPE_CHECKING:
    import metaflow.exception
    import metaflow.decorators

from ..exception import MetaflowException as MetaflowException
from ..exception import MetaflowExceptionWrapper as MetaflowExceptionWrapper
from ..metaflow_current import current as current

NUM_FALLBACK_RETRIES: int

class FailureHandledByCatch(metaflow.exception.MetaflowException, metaclass=type):
    def __init__(self, retry_count):
        ...
    ...

class CatchDecorator(metaflow.decorators.StepDecorator, metaclass=type):
    """
    Specifies that the step will success under all circumstances.
    
    The decorator will create an optional artifact, specified by `var`, which
    contains the exception raised. You can use it to detect the presence
    of errors, indicating that all happy-path artifacts produced by the step
    are missing.
    
    Parameters
    ----------
    var : str, optional, default None
        Name of the artifact in which to store the caught exception.
        If not specified, the exception is not stored.
    print_exception : bool, default True
        Determines whether or not the exception is printed to
        stdout when caught.
    """
    def step_init(self, flow, graph, step, decos, environment, flow_datastore, logger):
        ...
    def task_exception(self, exception, step, flow, graph, retry_count, max_user_code_retries):
        ...
    def task_post_step(self, step_name, flow, graph, retry_count, max_user_code_retries):
        ...
    def step_task_retry_count(self):
        ...
    def task_decorate(self, step_func, flow, graph, retry_count, max_user_code_retries, ubf_context):
        ...
    ...

