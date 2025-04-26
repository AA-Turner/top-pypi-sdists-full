import warnings
from typing import TYPE_CHECKING, Any, Dict, Optional, Union

from flytekit.core.array_node_map_task import ArrayNodeMapTask
from flytekit.core.launch_plan import LaunchPlan
from flytekit.core.python_function_task import PythonFunctionTask
from flytekit.core.task import ReferenceTask

from union.map._union_array_node import UnionArrayNode

if TYPE_CHECKING:
    from flytekit.remote import FlyteLaunchPlan


def map(
    target: Union[LaunchPlan, PythonFunctionTask, "FlyteLaunchPlan"],
    bound_inputs: Optional[Dict[str, Any]] = None,
    concurrency: Optional[int] = None,
    min_successes: Optional[int] = None,
    min_success_ratio: float = 1.0,
    **kwargs,
):
    """
    Use to map over tasks, actors, launch plans, reference tasks and launch plans, and remote tasks and
    launch plans.

    :param target: The Flyte entity of which will be mapped over
    :param bound_inputs: Inputs that are bound to the array node and will not be mapped over
    :param concurrency: If specified, this limits the number of mapped tasks than can run in parallel to the given batch
        size. If the size of the input exceeds the concurrency value, then multiple batches will be run serially until
        all inputs are processed. If set to 0, this means unbounded concurrency. If left unspecified, this means the
        array node will inherit parallelism from the workflow
    :param min_successes: The minimum number of successful executions
    :param min_success_ratio: The minimum ratio of successful executions
    """
    from flytekit.remote import FlyteLaunchPlan

    if isinstance(target, (LaunchPlan, FlyteLaunchPlan, ReferenceTask)):
        if isinstance(target, ReferenceTask):
            if bound_inputs:
                warnings.warn("bound_inputs are not supported for tasks yet")
        return UnionArrayNode(
            target=target,
            bound_inputs=bound_inputs,
            concurrency=concurrency,
            min_successes=min_successes,
            min_success_ratio=min_success_ratio,
        )
    return ArrayNodeMapTask(
        target,
        bound_inputs_values=bound_inputs,
        concurrency=concurrency,
        min_success_ratio=min_success_ratio,
        min_successes=min_successes,
        **kwargs,
    )
