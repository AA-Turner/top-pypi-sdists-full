from __future__ import annotations

import re
from collections.abc import Mapping
from dataclasses import dataclass, field
from typing import Any, Union

PUNCTUATORS = frozenset("!$&()[]{}:=@|")
BLOCK_QUOTE = '"' * 3
NAME = re.compile(r"[_A-Za-z][_0-9A-Za-z]*")
NUMBER = re.compile(r"-?(0|[1-9][0-9]*)(\.[0-9]+)?([eE][+-]?[0-9]+)?")
ESCAPES = {
    '"': '"',
    "\\": "\\",
    "/": "/",
    "b": "\b",
    "f": "\f",
    "n": "\n",
    "r": "\r",
    "t": "\t",
}


class GraphQLSyntaxError(ValueError):
    pass


@dataclass(frozen=True)
class Variable:
    name: str


@dataclass(frozen=True)
class Field:
    name: str
    alias: str | None
    arguments: dict[str, Any]
    selections: list[Selection] | None
    directives: list[tuple[str, dict[str, Any]]] = field(default_factory=list)

    @property
    def key(self) -> str:
        return self.alias or self.name


@dataclass(frozen=True)
class FragmentSpread:
    name: str
    directives: list[tuple[str, dict[str, Any]]]


@dataclass(frozen=True)
class InlineFragment:
    type_condition: str | None
    selections: list[Selection]
    directives: list[tuple[str, dict[str, Any]]]


Selection = Union[Field, FragmentSpread, InlineFragment]


@dataclass(frozen=True)
class Fragment:
    name: str
    type_condition: str
    selections: list[Selection]


@dataclass(frozen=True)
class Operation:
    kind: str
    name: str | None
    defaults: dict[str, Any]
    selections: list[Selection]


@dataclass(frozen=True)
class Document:
    operations: list[Operation]
    fragments: dict[str, Fragment]


def _block_string(raw: str) -> str:
    lines = raw.replace("\r\n", "\n").split("\n")
    indents = [
        len(line) - len(line.lstrip(" \t")) for line in lines[1:] if line.strip()
    ]
    common = min(indents, default=0)
    kept = [lines[0], *(line[common:] for line in lines[1:])]
    while kept and not kept[0].strip():
        kept.pop(0)
    while kept and not kept[-1].strip():
        kept.pop()
    return "\n".join(kept).replace("\\" + BLOCK_QUOTE, BLOCK_QUOTE)


def _string(source: str, start: int) -> tuple[str, int]:
    chars: list[str] = []
    index = start + 1
    while index < len(source):
        char = source[index]
        if char == '"':
            return "".join(chars), index + 1
        if char == "\n":
            break
        if char != "\\":
            chars.append(char)
            index += 1
            continue
        escaped = source[index + 1 : index + 2]
        if escaped == "u":
            chars.append(chr(int(source[index + 2 : index + 6], 16)))
            index += 6
            continue
        chars.append(ESCAPES.get(escaped, escaped))
        index += 2
    raise GraphQLSyntaxError("A string in the GraphQL document is not closed.")


def tokenize(source: str) -> list[tuple[str, Any]]:
    tokens: list[tuple[str, Any]] = []
    index = 0
    while index < len(source):
        char = source[index]
        if char in " \t\r\n,﻿":
            index += 1
        elif char == "#":
            end = source.find("\n", index)
            index = len(source) if end < 0 else end
        elif source.startswith("...", index):
            tokens.append(("punct", "..."))
            index += 3
        elif char in PUNCTUATORS:
            tokens.append(("punct", char))
            index += 1
        elif source.startswith(BLOCK_QUOTE, index):
            end = source.find(BLOCK_QUOTE, index + 3)
            while end > 0 and source[end - 1] == "\\":
                end = source.find(BLOCK_QUOTE, end + 3)
            if end < 0:
                raise GraphQLSyntaxError(
                    "A block string in the GraphQL document is not closed."
                )
            tokens.append(("string", _block_string(source[index + 3 : end])))
            index = end + 3
        elif char == '"':
            text, index = _string(source, index)
            tokens.append(("string", text))
        elif (matched := NUMBER.match(source, index)) and (
            char.isdigit() or char == "-"
        ):
            text = matched.group(0)
            is_float = matched.group(2) or matched.group(3)
            tokens.append(("number", float(text) if is_float else int(text)))
            index = matched.end()
        elif matched := NAME.match(source, index):
            tokens.append(("name", matched.group(0)))
            index = matched.end()
        else:
            raise GraphQLSyntaxError(
                f"The GraphQL document has an unexpected character {char!r}."
            )
    return tokens


class _Parser:
    def __init__(self, source: str) -> None:
        self.tokens = tokenize(source)
        self.index = 0

    def peek(self, kind: str, value: Any = None) -> bool:
        if self.index >= len(self.tokens):
            return False
        found_kind, found_value = self.tokens[self.index]
        return found_kind == kind and (value is None or found_value == value)

    def take(self, kind: str, value: Any = None) -> Any:
        if not self.peek(kind, value):
            found = (
                self.tokens[self.index][1]
                if self.index < len(self.tokens)
                else "the end"
            )
            wanted = value if value is not None else kind
            raise GraphQLSyntaxError(
                f"The GraphQL document has {found!r} where {wanted!r} belongs."
            )
        self.index += 1
        return self.tokens[self.index - 1][1]

    def skip(self, kind: str, value: Any = None) -> bool:
        if self.peek(kind, value):
            self.index += 1
            return True
        return False

    def document(self) -> Document:
        operations: list[Operation] = []
        fragments: dict[str, Fragment] = {}
        while self.index < len(self.tokens):
            if self.peek("punct", "{"):
                operations.append(Operation("query", None, {}, self.selections()))
            elif self.peek("name", "fragment"):
                fragment = self.fragment()
                fragments[fragment.name] = fragment
            else:
                operations.append(self.operation())
        return Document(operations, fragments)

    def operation(self) -> Operation:
        kind = self.take("name")
        if kind not in ("query", "mutation", "subscription"):
            raise GraphQLSyntaxError(
                f"The GraphQL document has {kind!r} where an operation belongs."
            )
        name = self.take("name") if self.peek("name") else None
        defaults = self.variable_definitions()
        self.directives()
        return Operation(kind, name, defaults, self.selections())

    def variable_definitions(self) -> dict[str, Any]:
        defaults: dict[str, Any] = {}
        if not self.skip("punct", "("):
            return defaults
        while not self.skip("punct", ")"):
            self.take("punct", "$")
            name = self.take("name")
            self.take("punct", ":")
            self.type_reference()
            if self.skip("punct", "="):
                defaults[name] = self.value()
            self.directives()
        return defaults

    def type_reference(self) -> None:
        if self.skip("punct", "["):
            self.type_reference()
            self.take("punct", "]")
        else:
            self.take("name")
        self.skip("punct", "!")

    def fragment(self) -> Fragment:
        self.take("name", "fragment")
        name = self.take("name")
        self.take("name", "on")
        type_condition = self.take("name")
        self.directives()
        return Fragment(name, type_condition, self.selections())

    def selections(self) -> list[Selection]:
        self.take("punct", "{")
        found: list[Selection] = []
        while not self.skip("punct", "}"):
            found.append(self.selection())
        return found

    def selection(self) -> Selection:
        if self.skip("punct", "..."):
            if self.peek("name") and not self.peek("name", "on"):
                return FragmentSpread(self.take("name"), self.directives())
            type_condition = None
            if self.skip("name", "on"):
                type_condition = self.take("name")
            directives = self.directives()
            return InlineFragment(type_condition, self.selections(), directives)
        name = self.take("name")
        alias = None
        if self.skip("punct", ":"):
            alias, name = name, self.take("name")
        arguments = self.arguments()
        directives = self.directives()
        selections = self.selections() if self.peek("punct", "{") else None
        return Field(name, alias, arguments, selections, directives)

    def arguments(self) -> dict[str, Any]:
        found: dict[str, Any] = {}
        if not self.skip("punct", "("):
            return found
        while not self.skip("punct", ")"):
            name = self.take("name")
            self.take("punct", ":")
            found[name] = self.value()
        return found

    def directives(self) -> list[tuple[str, dict[str, Any]]]:
        found: list[tuple[str, dict[str, Any]]] = []
        while self.skip("punct", "@"):
            found.append((self.take("name"), self.arguments()))
        return found

    def value(self) -> Any:
        if self.skip("punct", "$"):
            return Variable(self.take("name"))
        if self.skip("punct", "["):
            items = []
            while not self.skip("punct", "]"):
                items.append(self.value())
            return items
        if self.skip("punct", "{"):
            fields: dict[str, Any] = {}
            while not self.skip("punct", "}"):
                name = self.take("name")
                self.take("punct", ":")
                fields[name] = self.value()
            return fields
        if self.peek("string") or self.peek("number"):
            return self.take(self.tokens[self.index][0])
        word = self.take("name")
        return {"true": True, "false": False, "null": None}.get(word, word)


def parse(source: str) -> Document:
    return _Parser(source).document()


def resolve(value: Any, variables: Mapping[str, Any]) -> Any:
    if isinstance(value, Variable):
        return variables.get(value.name)
    if isinstance(value, list):
        return [resolve(item, variables) for item in value]
    if isinstance(value, dict):
        return {
            name: resolved
            for name, item in value.items()
            if not (isinstance(item, Variable) and item.name not in variables)
            for resolved in [resolve(item, variables)]
        }
    return value


def arguments_of(field_node: Field, variables: Mapping[str, Any]) -> dict[str, Any]:
    return {
        name: resolve(value, variables)
        for name, value in field_node.arguments.items()
        if not (isinstance(value, Variable) and value.name not in variables)
    }


def operation_of(document: Document, name: str | None) -> Operation:
    if name:
        found = next((op for op in document.operations if op.name == name), None)
        if found is None:
            raise GraphQLSyntaxError(f"The GraphQL document has no operation {name}.")
        return found
    if len(document.operations) != 1:
        raise GraphQLSyntaxError(
            "The GraphQL document has more than one operation and the request "
            "names none of them."
        )
    return document.operations[0]


def variables_with_defaults(
    operation: Operation, variables: Mapping[str, Any] | None
) -> dict[str, Any]:
    given = dict(variables or {})
    for name, default in operation.defaults.items():
        if name not in given:
            given[name] = resolve(default, given)
    return given


def _included(
    directives: list[tuple[str, dict[str, Any]]], variables: Mapping[str, Any]
) -> bool:
    for name, arguments in directives:
        condition = resolve(arguments.get("if"), variables)
        if name == "skip" and condition is True:
            return False
        if name == "include" and condition is False:
            return False
    return True


def fields_of(
    selections: list[Selection],
    document: Document,
    typename: str | None,
    variables: Mapping[str, Any],
) -> list[Field]:
    found: list[Field] = []
    for selection in selections:
        if not _included(selection.directives, variables):
            continue
        if isinstance(selection, Field):
            found.append(selection)
            continue
        if isinstance(selection, FragmentSpread):
            fragment = document.fragments.get(selection.name)
            if fragment is None:
                raise GraphQLSyntaxError(
                    f"The GraphQL document spreads a fragment {selection.name} "
                    "it does not define."
                )
            condition, nested = fragment.type_condition, fragment.selections
        else:
            condition, nested = selection.type_condition, selection.selections
        if condition is None or typename is None or condition in (typename, "Node"):
            found.extend(fields_of(nested, document, typename, variables))
    return found
