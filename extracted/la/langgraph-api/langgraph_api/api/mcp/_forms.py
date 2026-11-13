from collections.abc import Collection, Mapping
from dataclasses import dataclass, field, replace
from typing import Self

import jsonschema_rs
from pydantic import JsonValue

from langgraph_api.serde import json_dumpb
from langgraph_api.validation import SchemaValidator

Schema = dict[str, JsonValue]

WRAPPED_FIELD = "response"
MAX_FORM_FIELDS = 100
MAX_FORM_BYTES = 1024 * 1024
STRING_FORMATS = frozenset({"email", "uri", "date", "date-time"})
DEFS_PREFIX = "#/$defs/"
ROOT_KEYS = frozenset({"type", "properties", "required"})
DROPPED_ROOT_KEYS = frozenset(
    {"$schema", "$defs", "title", "description", "additionalProperties"}
)
DROPPED_KEYS = frozenset(
    {"$defs", "$schema", "examples", "$comment", "deprecated", "readOnly", "writeOnly"}
)
ANNOTATIONS = frozenset({"title", "description", "default"})
TEXT_KEYWORDS = ANNOTATIONS | {"type", "minLength", "maxLength", "format"}
CHOICE_KEYWORDS = ANNOTATIONS | {"type", "enum", "enumNames"}
TITLED_CHOICE_KEYWORDS = ANNOTATIONS | {"type", "oneOf"}
NUMBER_KEYWORDS = ANNOTATIONS | {"type", "minimum", "maximum"}
BOOLEAN_KEYWORDS = ANNOTATIONS | {"type"}
MULTI_SELECT_KEYWORDS = ANNOTATIONS | {"type", "items", "minItems", "maxItems"}
TITLED = frozenset({"const", "title"})
NULL: Schema = {"type": "null"}


class UnsupportedSchema(ValueError):
    pass


class FormTooLarge(UnsupportedSchema):
    pass


@dataclass(frozen=True, slots=True)
class Definitions:
    schemas: Mapping[str, JsonValue]

    @classmethod
    def of(cls, source: Mapping[str, JsonValue]) -> Self:
        schemas = source.get("$defs")
        return cls(schemas if isinstance(schemas, dict) else {})

    def resolved(self, node: Schema) -> Schema:
        match node:
            case {"allOf": [{"$ref": str()} as reference], **siblings}:
                return self.resolved({**reference, **siblings})
            case {"$ref": str() as ref, **siblings} if ref.startswith(DEFS_PREFIX):
                target = self.schemas.get(ref.removeprefix(DEFS_PREFIX))
                if not isinstance(target, dict):
                    raise UnsupportedSchema("Form schemas may only use known $defs")
                untitled = {
                    key: value for key, value in target.items() if key != "title"
                }
                return {**untitled, **siblings}
            case {"$ref": _}:
                raise UnsupportedSchema("Form schemas may only use local $defs")
            case _:
                return node


@dataclass(frozen=True, slots=True)
class FormSize:
    used: int = 0

    def plus(self, value: JsonValue) -> Self:
        encoded = _encoded(value)
        if encoded is None or self.used + len(encoded) > MAX_FORM_BYTES:
            raise FormTooLarge(f"A form can't be over {MAX_FORM_BYTES} bytes")
        return replace(self, used=self.used + len(encoded))


@dataclass(frozen=True, slots=True)
class FormSchema:
    schema: Schema
    validator: SchemaValidator = field(compare=False, repr=False)
    wrapped: bool = False

    @classmethod
    def of(cls, source: Mapping[str, JsonValue]) -> Self:
        if source.get("type") != "object":
            raise UnsupportedSchema("A form schema must describe an object")
        return cls._built(_form_root(dict(source), Definitions.of(source)))

    @classmethod
    def wrapping(cls, source: Mapping[str, JsonValue]) -> Self:
        if source.get("type") == "object":
            return cls.of(source)
        one_field: Schema = {
            "type": "object",
            "properties": _form_fields(
                {WRAPPED_FIELD: dict(source)}, Definitions.of(source)
            ),
            "required": [WRAPPED_FIELD],
        }
        return replace(cls._built(one_field), wrapped=True)

    @classmethod
    def _built(cls, schema: Schema) -> Self:
        FormSize().plus(schema)
        _check_fields(schema)
        return cls(schema, _validator({**schema, "additionalProperties": False}))

    def parse(
        self, content: Mapping[str, JsonValue] | None
    ) -> dict[str, JsonValue] | None:
        if content is None:
            return None
        answer = {
            key: _each_once(value)
            for key, value in content.items()
            if value is not None or key not in self._fields
        }
        if not self.validator.is_valid(answer) or _encoded(answer) is None:
            return None
        return answer

    def value(self, content: Mapping[str, JsonValue]) -> JsonValue:
        return content[WRAPPED_FIELD] if self.wrapped else dict(content)

    @property
    def _fields(self) -> Collection[str]:
        properties = self.schema.get("properties")
        return properties.keys() if isinstance(properties, dict) else ()


def _validator(schema: Schema) -> SchemaValidator:
    try:
        return jsonschema_rs.validator_for(schema, validate_formats=True)
    except jsonschema_rs.ValidationError:
        raise UnsupportedSchema("Invalid form schema") from None


def _each_once(value: JsonValue) -> JsonValue:
    match value:
        case [*choices] if all(isinstance(choice, str) for choice in choices):
            return list(dict.fromkeys(choices))
        case _:
            return value


def _encoded(value: JsonValue) -> bytes | None:
    try:
        return json_dumpb(value)
    except TypeError:
        return None


def _check_fields(schema: Schema) -> None:
    properties = schema.get("properties")
    if not isinstance(properties, dict):
        raise UnsupportedSchema("A form schema must be one flat object")
    for name, prop in properties.items():
        _check_field(name, prop)
    required = schema.get("required", [])
    if not isinstance(required, list) or not all(
        isinstance(key, str) and key in properties for key in required
    ):
        raise UnsupportedSchema("A form can only require its own fields")


def _check_field(name: str, prop: JsonValue) -> None:
    if not isinstance(prop, dict) or not _is_form_field(prop):
        raise UnsupportedSchema(f"A form can't ask for field {name!r}")
    if "default" in prop and not _validator(prop).is_valid(prop["default"]):
        raise UnsupportedSchema(f"Field {name!r} has an invalid default")


def _is_form_field(prop: Schema) -> bool:
    match prop:
        case {"type": "string", "oneOf": choices}:
            return prop.keys() <= TITLED_CHOICE_KEYWORDS and _is_titled_choices(choices)
        case {"type": "string", "enum": choices}:
            names = prop.get("enumNames", choices)
            return prop.keys() <= CHOICE_KEYWORDS and _is_named_choice(choices, names)
        case {"type": "string"}:
            return prop.keys() <= TEXT_KEYWORDS and _has_form_format(prop)
        case {"type": "number" | "integer"}:
            return prop.keys() <= NUMBER_KEYWORDS
        case {"type": "boolean"}:
            return prop.keys() <= BOOLEAN_KEYWORDS
        case {"type": "array", "items": items}:
            return prop.keys() <= MULTI_SELECT_KEYWORDS and _is_multi_select(items)
        case _:
            return False


def _has_form_format(prop: Schema) -> bool:
    string_format = prop.get("format")
    return "format" not in prop or (
        isinstance(string_format, str) and string_format in STRING_FORMATS
    )


def _is_named_choice(choices: JsonValue, names: JsonValue) -> bool:
    return (
        isinstance(choices, list)
        and isinstance(names, list)
        and _is_string_enum(choices)
        and len(names) == len(choices)
        and all(isinstance(name, str) for name in names)
    )


def _is_multi_select(items: JsonValue) -> bool:
    match items:
        case {"type": "string", "enum": enum, **rest} if not rest:
            return _is_string_enum(enum)
        case {"anyOf": choices, **rest} if not rest:
            return _is_titled_choices(choices)
        case _:
            return False


def _is_string_enum(values: JsonValue) -> bool:
    return (
        isinstance(values, list)
        and bool(values)
        and all(isinstance(value, str) for value in values)
        and len(set(values)) == len(values)
    )


def _is_titled_choices(choices: JsonValue) -> bool:
    if not isinstance(choices, list):
        return False
    consts = [
        choice["const"]
        for choice in choices
        if isinstance(choice, dict)
        and choice.keys() == TITLED
        and isinstance(choice["title"], str)
    ]
    return len(consts) == len(choices) and _is_string_enum(consts)


def _form_root(schema: Schema, definitions: Definitions) -> Schema:
    properties = schema.get("properties")
    if (
        schema.keys() - ROOT_KEYS - DROPPED_ROOT_KEYS
        or schema.get("additionalProperties", False)
        or not isinstance(properties, dict)
    ):
        raise UnsupportedSchema("A form schema must be one flat object")
    if not 0 < len(properties) <= MAX_FORM_FIELDS:
        raise UnsupportedSchema(f"A form needs 1 to {MAX_FORM_FIELDS} fields")
    return {
        **{key: value for key, value in schema.items() if key in ROOT_KEYS},
        "properties": _form_fields(properties, definitions),
    }


def _form_fields(
    properties: Mapping[str, JsonValue], definitions: Definitions
) -> Schema:
    fields: Schema = {}
    size = FormSize()
    for name, prop in properties.items():
        fields[name] = _form_field(prop, definitions)
        size = size.plus({name: fields[name]})
    return fields


def _form_field(prop: JsonValue, definitions: Definitions) -> JsonValue:
    if not isinstance(prop, dict):
        return prop
    kept = {
        key: value
        for key, value in _without_null(definitions.resolved(prop), definitions).items()
        if key not in DROPPED_KEYS and not key.startswith("x-")
    }
    if "default" in kept and kept["default"] is None:
        del kept["default"]
    const = kept.get("const")
    if isinstance(const, str):
        del kept["const"]
        kept |= {"type": "string", "enum": [const]}
    items = kept.get("items")
    if kept.get("type") == "array" and isinstance(items, dict):
        kept.pop("uniqueItems", None)
        kept["items"] = _multi_select_items(definitions.resolved(items))
    return kept


def _without_null(prop: Schema, definitions: Definitions) -> Schema:
    for union in ("anyOf", "oneOf"):
        options = prop.get(union)
        if isinstance(options, list) and NULL in options:
            match [option for option in options if option != NULL]:
                case [dict() as only]:
                    outer = {key: value for key, value in prop.items() if key != union}
                    return {**definitions.resolved(only), **outer}
                case _:
                    raise UnsupportedSchema("A form field can't mix several types")
    kind = prop.get("type")
    if isinstance(kind, list) and "null" in kind:
        rest = [option for option in kind if option != "null"]
        if len(rest) != 1:
            raise UnsupportedSchema("A form field can't mix several types")
        return {**prop, "type": rest[0]}
    return prop


def _multi_select_items(items: Schema) -> Schema:
    if "enum" in items:
        return {"type": "string", "enum": items["enum"]}
    if "anyOf" in items:
        return {"anyOf": items["anyOf"]}
    return items
