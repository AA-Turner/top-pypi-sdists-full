from enum import Enum
from typing import Any, Dict, List, Optional

import attr
import attrs

from grazie.api.client.utils import _check_parameters_schema


@attr.define(auto_attribs=True, frozen=True)
class FunctionDefinition:
    name: str
    description: Optional[str] = None
    parameters: Dict = attr.field(
        factory=lambda: {"type": "object", "properties": {}},
        validator=_check_parameters_schema,
    )

    class FunctionParameterTypes(Enum):
        BOOLEAN = "boolean"
        INTEGER = "integer"
        FLOAT = "float"
        STRING = "string"
        ARRAY = "array"

    def add_argument(
        self,
        name: str,
        description: Optional[str] = None,
        _type: Optional[FunctionParameterTypes] = None,
        required: bool = False,
        enum: Optional[List[Any]] = None,
    ) -> "FunctionDefinition":
        parameters = self.parameters
        parameters["properties"][name] = {}
        if description:
            parameters["properties"][name]["description"] = description
        if _type:
            parameters["properties"][name]["type"] = _type.value
        if enum is not None:
            parameters["properties"][name]["enum"] = enum
        if required:
            if "required" not in parameters:
                parameters["required"] = []
            parameters["required"].append(name)
        return attrs.evolve(self, parameters=parameters)
