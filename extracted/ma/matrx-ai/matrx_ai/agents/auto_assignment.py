from __future__ import annotations

from typing import Any, Literal

from pydantic import BaseModel, ConfigDict

AUTO_ASSIGN_TYPE = "auto_assign"


class AutoAssignRequest(BaseModel):
    type: Literal["auto_assign"]
    strategy: Literal["random"]

    model_config = ConfigDict(extra="forbid")


def is_auto_assign_request(value: Any) -> bool:
    if not isinstance(value, dict):
        return False
    try:
        AutoAssignRequest.model_validate(value)
    except ValueError:
        return False
    return True


def has_auto_assign_tag(value: Any) -> bool:
    return isinstance(value, dict) and value.get("type") == AUTO_ASSIGN_TYPE


def random_assignment_bindings_from_variables(
    variable_defaults: dict[str, Any] | None,
) -> dict[str, dict[str, Any]]:
    bindings: dict[str, dict[str, Any]] = {}
    for name, variable in (variable_defaults or {}).items():
        custom_component = getattr(variable, "custom_component", None)
        if not isinstance(custom_component, dict):
            continue
        assignment = custom_component.get("assignment")
        if not isinstance(assignment, dict) or assignment.get("random") is not True:
            continue

        structured_list = custom_component.get("structured_list") or custom_component.get(
            "picklist"
        )
        if isinstance(structured_list, dict):
            list_id = structured_list.get("listId") or structured_list.get("list_id")
            if isinstance(list_id, str) and list_id:
                bindings[name] = {
                    "source": "structured_list",
                    "list_id": list_id,
                    "group_name": structured_list.get("groupName")
                    or structured_list.get("group_name"),
                }
                continue

        options = custom_component.get("options")
        if not isinstance(options, list):
            stash = custom_component.get("stash")
            options = stash.get("options") if isinstance(stash, dict) else None
        if isinstance(options, list):
            unique_options = list(
                dict.fromkeys(option for option in options if isinstance(option, str) and option)
            )
            if unique_options:
                bindings[name] = {"source": "static", "options": unique_options}
    return bindings
