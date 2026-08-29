import inspect
from dataclasses import dataclass
from typing import Callable, Type, cast

from pydantic import BaseModel

from mistralai.workflows.models import WorkflowSpec

_on_behalf_of_by_name: dict[str, bool] = {}

_display_names_by_workflow: dict[str, str] = {}


@dataclass(frozen=True)
class _SearchKeyInfo:
    search_keys: tuple[str, ...]
    entrypoint_param_names: tuple[str, ...]
    input_model: type[BaseModel]


_search_key_info_by_name: dict[str, _SearchKeyInfo] = {}


def _get_workflow_entrypoint_method(cls_type: Type) -> Callable | None:
    for _, method in inspect.getmembers(cls_type, predicate=inspect.isfunction):
        if hasattr(method, "__workflows_workflow_entrypoint"):
            return method
    return None


def get_workflow_definition(workflow: Type | Callable) -> WorkflowSpec:
    definition = getattr(workflow, "__workflows_workflow_def", None)
    if definition is None:
        raise ValueError(f"Cannot get definition from {workflow}. Make sure it was decorated with @define")
    return cast(WorkflowSpec, definition)


def set_workflow_definition(workflow: Type | Callable, definition: WorkflowSpec) -> None:
    setattr(workflow, "__workflows_workflow_def", definition)
    _on_behalf_of_by_name[definition.name] = definition.on_behalf_of
    if definition.display_name is not None:
        _display_names_by_workflow[definition.name] = definition.display_name


def is_workflow_on_behalf_of(workflow_name: str) -> bool:
    return _on_behalf_of_by_name.get(workflow_name, False)


def get_workflow_display_name(workflow_name: str) -> str | None:
    return _display_names_by_workflow.get(workflow_name)


def set_workflow_search_key_info(
    workflow_name: str,
    search_keys: tuple[str, ...],
    entrypoint_param_names: tuple[str, ...],
    input_model: type[BaseModel],
) -> None:
    _search_key_info_by_name[workflow_name] = _SearchKeyInfo(search_keys, entrypoint_param_names, input_model)


def get_workflow_search_key_info(workflow_name: str) -> _SearchKeyInfo:
    info = _search_key_info_by_name.get(workflow_name)
    if info is None:
        raise KeyError(workflow_name)
    return info


def set_workflow_entrypoint(method: Callable) -> None:
    setattr(method, "__workflows_workflow_entrypoint", True)
