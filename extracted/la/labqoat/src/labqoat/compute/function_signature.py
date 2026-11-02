"""Capture an explicit context-first callable without serializing Python process state."""

import inspect
from collections.abc import Callable, Mapping
from typing import get_args, get_origin, get_type_hints

from labqoat.compute.value_codec import ValueCodec
from labqoat.json_document import JsonValue
from labqoat.run_context import RunContext


class FunctionSignature:
    """Bind authored parameters, defaults and typed schemas at the publication boundary."""

    def __init__(self, function: Callable[..., object]) -> None:
        """Capture public annotations and require one explicit context parameter."""
        signature = inspect.signature(function)
        self.annotations = get_type_hints(function)
        parameters = tuple(signature.parameters.values())
        if not parameters or self.annotations.get(parameters[0].name) is not RunContext:
            raise TypeError("A root function must declare RunContext as its first parameter")
        self.context_parameter = parameters[0].name
        self.signature = signature.replace(parameters=parameters[1:])

    def input_schema(self) -> dict[str, JsonValue]:
        """Capture complete bound keyword arguments; defaults are materialized before acceptance."""
        properties: dict[str, JsonValue] = {}
        for name, parameter in self.signature.parameters.items():
            if parameter.kind not in (inspect.Parameter.POSITIONAL_OR_KEYWORD, inspect.Parameter.KEYWORD_ONLY):
                raise TypeError("Compute parameters must have explicit names")
            schema = ValueCodec(self.annotations[name]).schema()
            if parameter.default is not inspect.Parameter.empty:
                schema["default"] = ValueCodec(self.annotations[name]).encode(parameter.default)
            properties[name] = schema
        return {"type": "object", "properties": properties, "required": list(properties), "additionalProperties": False}

    def checkpoint_parameters(self) -> tuple[str, ...]:
        """Parameters annotated `Checkpoint[...] | None`: the ones a function can resume from."""
        from labqoat.references.checkpoint_ref import CheckpointRef

        names = []
        for name in self.signature.parameters:
            options = get_args(self.annotations[name])
            if len(options) == 2 and type(None) in options:
                other = next(option for option in options if option is not type(None))
                if (get_origin(other) or other) is CheckpointRef:
                    names.append(name)
        return tuple(names)

    def encode(self, args: tuple[object, ...], kwargs: Mapping[str, object]) -> dict[str, JsonValue]:
        """Apply the authored Python signature before encoding every argument by its declared type."""
        bound = self.signature.bind(*args, **kwargs)
        bound.apply_defaults()
        return {name: ValueCodec(self.annotations[name]).encode(value) for name, value in bound.arguments.items()}

    def decode(self, values: Mapping[str, JsonValue]) -> dict[str, object]:
        """Restore typed arguments only after the whole captured input document is validated."""
        from labqoat.schemas.schema_document import SchemaDocument

        SchemaDocument.capture(self.input_schema()).validate(dict(values))
        return {name: ValueCodec(self.annotations[name]).decode(value) for name, value in values.items()}
