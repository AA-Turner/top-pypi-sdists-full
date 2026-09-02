import abc
import json
from typing import Any, Dict, List

import attrs

from grazie.api.client.llm_functions import FunctionDefinition


class BaseParameters:
    @attrs.define(auto_attribs=True, frozen=True)
    class Key:
        fqdn: str
        type: str

        def serialize(self) -> Dict[str, Any]:
            return {"type": self.type, "fqdn": self.fqdn}

    @attrs.define(auto_attribs=True, frozen=True)
    class BooleanKey(Key):
        type: str = "bool"

    @attrs.define(auto_attribs=True, frozen=True)
    class IntKey(Key):
        type: str = "int"

    @attrs.define(auto_attribs=True, frozen=True)
    class FloatKey(Key):
        type: str = "double"

    @attrs.define(auto_attribs=True, frozen=True)
    class StrKey(Key):
        type: str = "text"

    @attrs.define(auto_attribs=True, frozen=True)
    class JsonKey(Key):
        type: str = "json"

    @attrs.define(auto_attribs=True, frozen=True)
    class Value:
        @abc.abstractmethod
        def serialize(self) -> Dict[str, Any]:
            pass

    @attrs.define(auto_attribs=True, frozen=True)
    class BooleanValue(Value):
        value: bool

        def serialize(self) -> Dict[str, Any]:
            return {"type": "bool", "value": self.value, "modified": 0}

    @attrs.define(auto_attribs=True, frozen=True)
    class IntValue(Value):
        value: int

        def serialize(self) -> Dict[str, Any]:
            return {"type": "int", "value": self.value, "modified": 0}

    @attrs.define(auto_attribs=True, frozen=True)
    class FloatValue(Value):
        value: float

        def serialize(self) -> Dict[str, Any]:
            return {"type": "double", "value": self.value, "modified": 0}

    @attrs.define(auto_attribs=True, frozen=True)
    class StrValue(Value):
        value: str

        def serialize(self) -> Dict[str, Any]:
            return {"type": "text", "value": self.value, "modified": 0}

    @attrs.define(auto_attribs=True, frozen=True)
    class JsonValue(Value):
        value: Any

        def serialize(self) -> Dict[str, Any]:
            return {"type": "json", "value": json.dumps(self.value), "modified": 0}

    @classmethod
    def serialize(cls, parameters: Dict[Key, Value]) -> List[Dict[str, Any]]:
        parameters_data: List[Dict[str, Any]] = []
        for key, value in parameters.items():
            if not (key.__class__, value.__class__) in cls._allowed_type_mapping:
                raise ValueError(
                    f"Types for key and value should be the same. "
                    f"Got {key.__class__.__name__}:{value.__class__.__name__}"
                )
            parameters_data.extend(
                [
                    key.serialize(),
                    value.serialize(),
                ]
            )
        return parameters_data

    _allowed_type_mapping = {
        (BooleanKey, BooleanValue),
        (IntKey, IntValue),
        (FloatKey, FloatValue),
        (StrKey, StrValue),
        (JsonKey, JsonValue),
    }


class Parameters(BaseParameters):
    @attrs.define(auto_attribs=True, frozen=True)
    class JsonValue(BaseParameters.Value):  # type: ignore[reportIncompatibleVariableOverride]
        value: Any

        def serialize(self) -> Dict[str, Any]:
            return {"type": "json", "value": json.dumps(self.value), "modified": 0}

        @classmethod
        def from_functions(cls, *funcs: FunctionDefinition):
            return cls(value=[attrs.asdict(func) for func in funcs])

    _allowed_type_mapping = {
        (BaseParameters.BooleanKey, BaseParameters.BooleanValue),
        (BaseParameters.IntKey, BaseParameters.IntValue),
        (BaseParameters.FloatKey, BaseParameters.FloatValue),
        (BaseParameters.StrKey, BaseParameters.StrValue),
        (BaseParameters.JsonKey, JsonValue),
    }
