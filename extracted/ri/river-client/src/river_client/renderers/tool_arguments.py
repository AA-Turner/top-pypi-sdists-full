"""Decode tool-call argument values written without type markers.

GLM and the Qwen family write string arguments verbatim and every other value
as JSON. A parameter's JSON Schema decides which reading the model meant; see
``docs/tool-call-parsing.md`` for the contract this implements.
"""

from __future__ import annotations

import json
import os
import re
import warnings
from collections.abc import Iterable, Iterator
from dataclasses import dataclass
from typing import TYPE_CHECKING, Any
from urllib.parse import quote

from jsonschema.protocols import Validator
from jsonschema.validators import (
    Draft3Validator,
    Draft201909Validator,
    Draft4Validator,
    Draft6Validator,
    Draft7Validator,
    validator_for,
)
from referencing import Registry, Specification
from referencing.exceptions import Unresolvable
from referencing.jsonschema import specification_with

if TYPE_CHECKING:
    # referencing documents Resolver but exports it only from its core module.
    from referencing._core import Resolver

    from river_client.renderers.base import ToolSpec

# Warnings about how river_client is called name the caller's line, not ours.
_PACKAGE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + os.sep


# Before 2019-09, $ref replaced its sibling keywords instead of joining them.
_REF_REPLACES_SIBLINGS = (
    Draft3Validator,
    Draft4Validator,
    Draft6Validator,
    Draft7Validator,
)


def specification(validator_class: type[Validator]) -> Specification:
    """Return the dialect jsonschema resolves this validator's schemas in."""
    return specification_with(
        validator_class.ID_OF(validator_class.META_SCHEMA) or "urn:unknown-dialect",
        default=Specification.OPAQUE,
    )


def _accepts_every_string(schema: Any, validator_class: type[Validator]) -> bool:
    """Whether every string satisfies ``schema``; False when unsure."""
    if isinstance(schema, bool):
        return schema
    validator_class = validator_for(schema, default=validator_class)
    for keyword, value in schema.items():
        if keyword not in validator_class.VALIDATORS:
            continue  # An annotation, or unknown to this dialect.
        types = value if isinstance(value, list) else [value]
        if keyword != "type" or not any(
            isinstance(name, str) and validator_class.TYPE_CHECKER.is_type("", name)
            for name in types
        ):
            return False
    return True


def admits_strings(
    schema: Any,
    validator_class: type[Validator],
    resolver: Resolver[Any],
    references: frozenset[int] = frozenset(),
) -> bool:
    """Whether some string may satisfy ``schema``; False only if none can.

    Follows the keywords that limit a value's JSON type (type, enum, const,
    $ref and the applicators combining subschemas) through references as
    jsonschema does. Everything else, such as pattern, $dynamicRef or a
    subschema in another dialect, is assumed to admit some string, so errors
    lean to True.
    """
    if isinstance(schema, bool):
        return schema
    if validator_for(schema, default=validator_class) is not validator_class:
        # jsonschema then mixes the parent's and the subschema's rules.
        return True
    keywords = {k: v for k, v in schema.items() if k in validator_class.VALIDATORS}
    dialect = specification(validator_class)

    def admits(subschema: Any) -> bool:
        if isinstance(subschema, bool):
            return subschema
        resource = dialect.create_resource(subschema)
        return admits_strings(
            subschema,
            validator_class,
            resolver.in_subresource(resource),
            references,
        )

    if "$ref" in keywords:
        try:
            resolved = resolver.lookup(keywords["$ref"])
        except Unresolvable:
            # Validation never reached this reference, or it would have raised.
            target = True
        else:
            seen = id(resolved.contents)
            target = seen in references or admits_strings(
                resolved.contents,
                validator_class,
                resolved.resolver,
                references | {seen},
            )
        if issubclass(validator_class, _REF_REPLACES_SIBLINGS) or not target:
            return target
    if "type" in keywords:
        types = keywords["type"]
        if not any(
            admits(name)
            if isinstance(name, dict)  # Draft 3 also accepts schemas here.
            else validator_class.TYPE_CHECKER.is_type("", name)
            for name in (types if isinstance(types, list) else [types])
        ):
            return False
    if "enum" in keywords and not any(isinstance(v, str) for v in keywords["enum"]):
        return False
    if "const" in keywords and not isinstance(keywords["const"], str):
        return False
    if "allOf" in keywords and not all(map(admits, keywords["allOf"])):
        return False
    for keyword in ("anyOf", "oneOf"):
        if keyword in keywords and not any(map(admits, keywords[keyword])):
            return False
    if "not" in keywords and _accepts_every_string(keywords["not"], validator_class):
        return False
    if "if" in keywords:
        condition = keywords["if"]
        via_then = admits(condition) and admits(schema.get("then", True))
        via_else = not _accepts_every_string(condition, validator_class) and admits(
            schema.get("else", True)
        )
        if not (via_then or via_else):
            return False
    return True


def decode_value(raw: str, validator: Validator, resolver: Resolver[Any]) -> Any:
    """Choose the string or JSON reading of an untyped GLM argument value.

    GLM writes strings verbatim and other values as JSON, with no marker
    between them. A reading the schema accepts wins, the raw string first so
    ambiguous unions keep the model's text. A value neither reading satisfies
    still reaches the tool, which reports the violation. It stays the text the
    model wrote unless no string could satisfy the schema; then the JSON value
    is the only reading of the right type.
    """
    if validator.is_valid(raw):
        return raw
    value = _json_reading(raw)
    if value is _NO_READING:
        return raw
    if validator.is_valid(value):
        return value
    if admits_strings(validator.schema, type(validator), resolver):
        return raw
    return value


_NO_READING = object()


def _unique_members(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    members = dict(pairs)
    if len(members) != len(pairs):
        raise ValueError("JSON object has a duplicate key")
    return members


# serde_json's default recursion limit: River Serve rejects anything deeper.
_MAX_JSON_DEPTH = 127


def _nesting_depth(raw: str) -> int:
    """The deepest array or object nesting in ``raw``, outside strings."""
    depth = deepest = 0
    in_string = escaped = False
    for char in raw:
        if in_string:
            if escaped:
                escaped = False
            elif char == "\\":
                escaped = True
            elif char == '"':
                in_string = False
        elif char == '"':
            in_string = True
        elif char in "[{":
            depth += 1
            deepest = max(deepest, depth)
        elif char in "]}":
            depth -= 1
    return deepest


def standard_json(raw: str) -> Any:
    """Decode ``raw`` as standard JSON, raising ValueError for anything else.

    Python's json also accepts NaN, Infinity and numbers that overflow to
    them, and keeps only the last of duplicate keys, at any depth. No value
    must reach a tool in a form other readers would not return, or with part
    of what the model wrote silently dropped. Nesting deeper than River
    Serve's JSON reader allows is refused before decoding, which would
    otherwise exhaust the interpreter's recursion limit.
    """
    if _nesting_depth(raw) > _MAX_JSON_DEPTH:
        raise ValueError(f"JSON nests deeper than {_MAX_JSON_DEPTH} levels")
    value = json.loads(raw, object_pairs_hook=_unique_members)
    json.dumps(value, allow_nan=False)
    return value


def find_outside_json_strings(
    text: str, markers: tuple[str, ...], start: int = 0
) -> tuple[int, str | None]:
    """The first of ``markers`` in ``text`` from ``start`` outside a JSON string.

    Where a format carries JSON, marker text inside a string value is content,
    so a block runs to the first end marker outside a string. Returns
    ``(len(text), None)`` when there is none, including while a string is
    still open.
    """
    firsts = {marker[0] for marker in markers}
    in_string = escaped = False
    for index in range(start, len(text)):
        char = text[index]
        if in_string:
            if escaped:
                escaped = False
            elif char == "\\":
                escaped = True
            elif char == '"':
                in_string = False
        elif char == '"':
            in_string = True
        elif char in firsts:
            for marker in markers:
                if text.startswith(marker, index):
                    return index, marker
    return len(text), None


def protect_value_ends(value: Any, ends: Iterable[str]) -> Any:
    """``value`` as a format that leaves types unmarked can write it back.

    Such a format writes a string verbatim and anything else as JSON, and its
    parser ends a value, or the call around it, at the first of ``ends``.
    Text read raw stops there, so a value whose text holds one was decoded
    from JSON. It comes back as JSON text with each such tag's ``<`` escaped,
    which decodes to the same value; any other value is unchanged.
    """
    ends = tuple(ends)
    text = value if isinstance(value, str) else json.dumps(value, ensure_ascii=False)
    if not any(tag in text for tag in ends):
        return value
    text = json.dumps(value, ensure_ascii=False)
    for tag in ends:
        text = text.replace(tag, "\\u003c" + tag[1:])
    return text


def decode_json_marked(raw: str) -> Any:
    """Decode a value its format marks as JSON: standard JSON, else the text."""
    try:
        return standard_json(raw)
    except ValueError:
        return raw


def _json_reading(raw: str) -> Any:
    """The standard non-string JSON value ``raw`` spells, or ``_NO_READING``.

    Untyped formats never JSON-quote a string, so a decoded string is not a
    reading.
    """
    try:
        value = standard_json(raw)
    except ValueError:
        return _NO_READING
    return _NO_READING if isinstance(value, str) else value


def decode_without_schema(raw: str) -> Any:
    """Decode a value no schema covers: its JSON reading, else the text."""
    value = _json_reading(raw)
    return raw if value is _NO_READING else value


# Keywords whose verdict on an object never depends on a property's value:
# they apply to other instance types, or to an object's keys and size.
_VALUE_NEUTRAL = frozenset(
    {
        "required",
        "minProperties",
        "maxProperties",
        "propertyNames",
        "dependentRequired",
        "format",
        "minLength",
        "maxLength",
        "pattern",
        "minimum",
        "maximum",
        "exclusiveMinimum",
        "exclusiveMaximum",
        "multipleOf",
        "divisibleBy",
        "items",
        "additionalItems",
        "prefixItems",
        "contains",
        "minItems",
        "maxItems",
        "uniqueItems",
        "unevaluatedItems",
    }
)
# Keywords that place schemas on property values, read by ToolArguments.
_PROPERTY_SCHEMAS = (
    "properties",
    "patternProperties",
    "additionalProperties",
    "unevaluatedProperties",
)


def _value_independent(schema: Any, validator_class: type[Validator]) -> bool:
    """Whether ``schema`` judges an object the same whatever its values are.

    Lists what is known to be independent, so anything unrecognized, such as
    an object-valued const or a reference, counts as dependent.
    """
    if isinstance(schema, bool):
        return True
    if validator_for(schema, default=validator_class) is not validator_class:
        return False
    return all(
        _keyword_value_independent(keyword, value, schema, validator_class)
        for keyword, value in schema.items()
        if keyword in validator_class.VALIDATORS
    )


def _keyword_value_independent(
    keyword: str, value: Any, schema: Any, validator_class: type[Validator]
) -> bool:
    def independent(subschemas: Iterable[Any]) -> bool:
        return all(_value_independent(s, validator_class) for s in subschemas)

    if keyword == "type":  # Draft 3 also accepts schemas here.
        return all(
            isinstance(t, str) for t in (value if isinstance(value, list) else [value])
        )
    if keyword in _VALUE_NEUTRAL:
        return True
    if keyword in ("allOf", "anyOf", "oneOf"):
        return independent(value)
    if keyword == "not":
        return independent([value])
    if keyword == "if":
        return independent([value, schema.get("then", True), schema.get("else", True)])
    if keyword == "dependentSchemas":
        return independent(value.values())
    if keyword == "dependencies":  # Before 2019-09; a list or name is required keys.
        return independent(v for v in value.values() if not isinstance(v, (list, str)))
    return False


def _pointer_segment(key: str) -> str:
    return quote(key.replace("~", "~0").replace("/", "~1"), safe="")


def _pointers(node: Any, pointer: str = "") -> Iterator[tuple[int, str]]:
    """Yield (id, JSON pointer) for every object in a schema document."""
    if isinstance(node, dict):
        yield id(node), pointer
        for key, child in node.items():
            yield from _pointers(child, f"{pointer}/{_pointer_segment(key)}")
    elif isinstance(node, list):
        for index, child in enumerate(node):
            yield from _pointers(child, f"{pointer}/{index}")


@dataclass(frozen=True)
class _Scope:
    """An object schema every valid arguments object satisfies.

    ``members`` are its ``allOf`` members and ``$ref`` target, which apply in
    place. Under a ``$ref`` that replaces its siblings, the schema's own
    keywords do not apply (``own`` is False) and the target is its only member.
    """

    schema: Any
    pointer: str
    own: bool
    members: tuple[_Scope, ...]


class _Unsatisfiable(Exception):
    """No value for the key can make the arguments object valid."""


def _own_schemas(scope: _Scope) -> Iterator[dict[str, Any]]:
    """The object schemas whose own keywords apply in ``scope``."""
    if scope.own and isinstance(scope.schema, dict):
        yield scope.schema
    for member in scope.members:
        yield from _own_schemas(member)


def _evaluation_as_specified(root: _Scope, validator_class: type[Validator]) -> bool:
    """Whether jsonschema decides which keys are unevaluated as the spec does.

    For 2019-09 it takes a schema-valued additionalProperties or
    unevaluatedProperties to evaluate the keys named like that schema's
    keywords, not the keys it validates. Where that meets an
    unevaluatedProperties, the two disagree, so neither reading is chosen.
    """
    if not issubclass(validator_class, Draft201909Validator):
        return True
    schemas = list(_own_schemas(root))
    return not any("unevaluatedProperties" in s for s in schemas) or not any(
        isinstance(s.get(keyword), dict)
        for s in schemas
        for keyword in ("additionalProperties", "unevaluatedProperties")
    )


class ToolArguments:
    """Decode one call's untyped argument values by its tool's schema.

    A key's schema is what JSON Schema applies to that property: matching
    ``properties`` and ``patternProperties`` entries, else
    ``additionalProperties``, in the tool's ``parameters`` and in every object
    schema it requires in place through ``allOf`` and ``$ref``, plus
    ``unevaluatedProperties`` within each schema's own scope. Each is
    referenced by its JSON pointer in the tool's schema document, so its base
    URI, ``$defs`` and dialect resolve exactly as when jsonschema validates the
    whole object.

    Values have no schema when the tool is unknown, ``tools`` is None, or the
    object schema could judge one property's value by the others: object-level
    alternatives, conditions, ``const`` or ``enum`` that read properties,
    dynamic references, or a part declaring another dialect.
    """

    def __init__(self, tools: list[ToolSpec] | None, name: str) -> None:
        tool = next((tool for tool in tools or [] if tool["name"] == name), None)
        self._root: _Scope | None = None
        if tool is None:
            return
        schema = tool["parameters"]
        self._class = validator_for(schema)
        self._class.check_schema(schema)
        # Resolve local $defs, but never fetch external references while
        # parsing a completion. Invalid schemas are caller configuration errors.
        self._validator = self._class(schema, registry=Registry())
        self._resolver = Registry().resolver_with_root(
            specification(self._class).create_resource(schema)
        )
        self._pointer_of = dict(_pointers(schema))
        root = self._scope(schema, "", self._resolver, frozenset({""}))
        if root is not None and not _evaluation_as_specified(root, self._class):
            root = None
        self._root = root

    def decode(self, key: str, raw: str) -> Any:
        """Decode ``raw``, the text the model wrote for argument ``key``."""
        if self._root is None:
            return decode_without_schema(raw)
        return decode_value(
            raw, self._validator.evolve(schema=self._key_schema(key)), self._resolver
        )

    @property
    def determined(self) -> bool:
        """Whether values are decoded by a schema."""
        return self._root is not None

    def _key_schema(self, key: str) -> Any:
        """The schema a value for ``key`` must satisfy, as JSON Schema defines it."""
        assert self._root is not None
        try:
            schemas, _ = self._applicable(self._root, key)
        except _Unsatisfiable:
            return False
        if not schemas:
            return True
        return schemas[0] if len(schemas) == 1 else {"allOf": schemas}

    def _scope(
        self,
        schema: Any,
        pointer: str,
        resolver: Resolver[Any],
        seen: frozenset[str],
    ) -> _Scope | None:
        """The object scope ``schema`` defines, or None if undetermined."""
        if isinstance(schema, bool):
            return _Scope(schema, pointer, True, ())
        if validator_for(schema, default=self._class) is not self._class:
            # jsonschema then mixes the parent's and the subschema's rules.
            return None
        keywords = {k: v for k, v in schema.items() if k in self._class.VALIDATORS}
        own = not (
            "$ref" in keywords and issubclass(self._class, _REF_REPLACES_SIBLINGS)
        )
        if own and not all(
            _keyword_value_independent(keyword, value, schema, self._class)
            for keyword, value in keywords.items()
            if keyword not in (*_PROPERTY_SCHEMAS, "allOf", "$ref")
        ):
            return None
        members: list[_Scope] = []
        if "$ref" in keywords:
            try:
                resolved = resolver.lookup(keywords["$ref"])
            except Unresolvable:
                return None
            target = resolved.contents
            target_pointer = self._pointer_of.get(id(target))
            if isinstance(target, bool):
                members.append(_Scope(target, pointer, True, ()))
            elif target_pointer is None:
                return None  # Outside this document, such as a meta-schema.
            elif target_pointer not in seen:
                member = self._scope(
                    target, target_pointer, resolved.resolver, seen | {target_pointer}
                )
                if member is None:
                    return None
                members.append(member)
        if own:
            dialect = specification(self._class)
            for index, subschema in enumerate(keywords.get("allOf", [])):
                member = self._scope(
                    subschema,
                    f"{pointer}/allOf/{index}",
                    resolver.in_subresource(dialect.create_resource(subschema))
                    if isinstance(subschema, dict)
                    else resolver,
                    seen,
                )
                if member is None:
                    return None
                members.append(member)
        return _Scope(schema, pointer, own, tuple(members))

    def _applicable(self, scope: _Scope, key: str) -> tuple[list[Any], bool]:
        """The schemas ``scope`` applies to ``key``'s value, and whether it
        evaluates ``key``, as ``unevaluatedProperties`` defines evaluation."""
        if scope.schema is False:
            raise _Unsatisfiable
        if scope.schema is True:
            return [], False
        schema, pointer = scope.schema, scope.pointer
        known = self._class.VALIDATORS
        locations: list[str] = []
        if scope.own:
            if "properties" in known and key in schema.get("properties", {}):
                locations.append(f"{pointer}/properties/{_pointer_segment(key)}")
            if "patternProperties" in known:
                locations.extend(
                    f"{pointer}/patternProperties/{_pointer_segment(pattern)}"
                    for pattern in schema.get("patternProperties", {})
                    if re.search(pattern, key)
                )
            if not locations and "additionalProperties" in known:
                if "additionalProperties" in schema:
                    locations.append(f"{pointer}/additionalProperties")
        evaluated = bool(locations)
        schemas: list[Any] = [{"$ref": f"#{location}"} for location in locations]
        for member in scope.members:
            member_schemas, member_evaluated = self._applicable(member, key)
            schemas.extend(member_schemas)
            evaluated = evaluated or member_evaluated
        if (
            scope.own
            and not evaluated
            and "unevaluatedProperties" in known
            and "unevaluatedProperties" in schema
        ):
            # It covers only keys nothing in its own scope evaluated.
            schemas.append({"$ref": f"#{pointer}/unevaluatedProperties"})
            evaluated = True
        return schemas, evaluated


def warn_untyped_without_tools(family: str) -> None:
    """Warn that a response's tool calls were parsed without ``tools``."""
    warnings.warn(
        f"{family} tool calls carry no argument types, so without tools= each "
        "value is guessed: standard JSON is decoded and anything else stays "
        "text. Pass the ToolSpec list used to render the prompt, or tools=[] "
        "if it had none",
        skip_file_prefixes=(_PACKAGE_DIR,),
    )
