import inspect
from typing import Any, Callable, Dict, Set, Type

from pydantic import TypeAdapter
from temporalio.exceptions import ApplicationError

from mistralai.workflows.core.execution.concurrency.types import (
    WorkflowResults,
)


def dict_to_workflow_results(results: Dict[int, Any]) -> WorkflowResults:
    """Convert a dictionary of results to WorkflowResults."""
    return WorkflowResults(values=[results[i] for i in sorted(results)])


def workflow_results_to_dict(results: WorkflowResults) -> Dict[int, Any]:
    """Convert WorkflowResults to a dictionary."""
    return {i: result for i, result in enumerate(results.values)}


def build_type_adapters(user_params_dict: Dict[str, Type]) -> Dict[str, TypeAdapter]:
    """Build TypeAdapter instances once for reuse across items."""
    return {k: TypeAdapter(t) for k, t in user_params_dict.items()}


def build_required_keys(func: Callable) -> Set[str]:
    """Return the set of parameter names that have no default value."""
    sig = inspect.signature(func)
    return {
        name
        for name, param in sig.parameters.items()
        if param.default is inspect.Parameter.empty and param.kind not in (param.VAR_POSITIONAL, param.VAR_KEYWORD)
    }


def coerce_multi_params(
    item: Dict[str, Any],
    adapters: Dict[str, TypeAdapter],
    required_keys: Set[str] | None = None,
    allow_extra: bool = False,
) -> Dict[str, Any]:
    """Coerce multi-param dict values to their expected types.

    After serialization, Pydantic models become plain dicts. This coerces
    them back before the activity wrapper's type validator runs.
    """
    if not isinstance(item, dict):
        raise ApplicationError(
            f"Expected a dict for multi-param activity, got {type(item).__name__}",
            non_retryable=True,
        )
    extra_keys = item.keys() - adapters.keys()
    if extra_keys and not allow_extra:
        raise ApplicationError(
            f"Unexpected keys {extra_keys} in item. Expected keys: {set(adapters.keys())}",
            non_retryable=True,
        )
    if required_keys is not None:
        missing_keys = required_keys - item.keys()
        if missing_keys:
            raise ApplicationError(
                f"Missing required keys {missing_keys} in item. Expected keys: {set(adapters.keys())}",
                non_retryable=True,
            )
    try:
        coerced_item = {k: adapters[k].validate_python(v) for k, v in item.items() if k in adapters}
        if allow_extra:
            coerced_item.update({k: v for k, v in item.items() if k not in adapters})
        return coerced_item
    except Exception as e:
        raise ApplicationError(
            f"Type coercion failed for item: {e}",
            non_retryable=True,
        ) from e
