from enum import Enum
from typing import Dict, Optional

import attr
import attrs

from grazie.api.client.utils import _check_parameters_schema


@attr.define(auto_attribs=True, frozen=True)
class ToolDefinition:
    name: str
    description: Optional[str] = None
    parameters: Dict = attr.field(
        factory=lambda: {"schema": {"type": "object", "properties": {}}},
        validator=_check_parameters_schema,
    )

    class ToolParameterTypes(Enum):
        BOOLEAN = "boolean"
        INTEGER = "integer"
        FLOAT = "float"
        STRING = "string"
        ARRAY = "array"

    def add_parameter(
        self,
        name: str,
        description: Optional[str] = None,
        _type: Optional[ToolParameterTypes] = None,
        required: bool = False,
    ) -> "ToolDefinition":
        parameters = self.parameters
        schema = parameters["schema"]
        schema["properties"][name] = {}
        if description:
            schema["properties"][name]["description"] = description
        if _type:
            schema["properties"][name]["type"] = _type.value
        if required:
            if "required" not in schema:
                schema["required"] = []
            schema["required"].append(name)
        return attrs.evolve(self, parameters=parameters)
