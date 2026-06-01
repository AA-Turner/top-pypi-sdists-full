import json
from typing import Any, Dict

import attrs

from grazie.api.client.parameters import BaseParameters
from grazie.api.client.v8.llm_tools import ToolDefinition


class Parameters(BaseParameters):
    @attrs.define(auto_attribs=True, frozen=True)
    class JsonValue(BaseParameters.Value):  # type: ignore[reportIncompatibleVariableOverride]
        value: Any

        def serialize(self) -> Dict[str, Any]:
            return {"type": "json", "value": json.dumps(self.value), "modified": 0}

        @classmethod
        def from_tools(cls, *tools: ToolDefinition):
            return cls(value=[attrs.asdict(tool) for tool in tools])

    _allowed_type_mapping = {
        (BaseParameters.BooleanKey, BaseParameters.BooleanValue),
        (BaseParameters.IntKey, BaseParameters.IntValue),
        (BaseParameters.FloatKey, BaseParameters.FloatValue),
        (BaseParameters.StrKey, BaseParameters.StrValue),
        (BaseParameters.JsonKey, JsonValue),
    }
