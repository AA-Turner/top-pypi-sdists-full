"""Shared helpers for typed message annotations."""

from pydantic import BaseModel, TypeAdapter

from mistralai.vibe_agents.session_workflow.commands import JsonObject

_JsonObjectAdapter: TypeAdapter[JsonObject] = TypeAdapter(JsonObject)


def annotations_for(key: str, model: BaseModel, *, exclude_none: bool = False) -> JsonObject:
    dumped = {
        key: model.model_dump(
            mode="json",
            by_alias=True,
            exclude_none=exclude_none,
        )
    }
    return _JsonObjectAdapter.validate_python(dumped)
