from __future__ import annotations

import json
from collections.abc import Awaitable, Callable, Generator
from dataclasses import dataclass, field
from typing import Any

ISSUE = "Issue"
QUERY = "Query"
SCHEMA_OPERATION = "bitfabLinearSchema"
WHOLE_OPERATION = "bitfabWholeIssue"
LOOKUP_OPERATION = "bitfabWholeIssueLookups"
FIRST_PAGE = 100
LOOKUP_BATCH = 50
MAX_REQUESTS = 400
MAX_INLINE_DEPTH = 2
LEAF_KINDS = ("SCALAR", "ENUM")
ABSTRACT_KINDS = ("INTERFACE", "UNION")
TOO_BIG_WORDS = ("complex", "too large", "too big")
BASE = "@base"

TYPE_REF = (
    "kind name ofType { kind name ofType { kind name ofType { kind name "
    "ofType { kind name } } } }"
)
SCHEMA_QUERY = (
    f"query {SCHEMA_OPERATION} {{ __schema {{ queryType {{ name }} types {{ kind "
    "name fields(includeDeprecated: true) { name args { name defaultValue type { "
    "...TypeRef } } type { ...TypeRef } } } } } "
    f"fragment TypeRef on __Type {{ {TYPE_REF} }}"
)
MEMBERS_OPERATION = f"{SCHEMA_OPERATION}Members"
MEMBERS_QUERY = f"query {MEMBERS_OPERATION} {{ __schema {{ types {{ name possibleTypes {{ name }} }} }} }}"

Reads = Generator[dict, Any, Any]


@dataclass(frozen=True)
class SchemaField:
    name: str
    kind: str
    type_name: str
    args: frozenset[str]
    needs_args: bool


@dataclass
class LinearSchema:
    kinds: dict[str, str]
    fields: dict[str, list[SchemaField]]
    possible: dict[str, list[str]]
    lookups: dict[str, str]

    def field(self, typename: str, name: str) -> SchemaField | None:
        return next((f for f in self.fields.get(typename, []) if f.name == name), None)

    def has_id(self, typename: str) -> bool:
        return self.field(typename, "id") is not None

    def node_type(self, typename: str) -> str | None:
        nodes = self.field(typename, "nodes")
        if nodes is None or self.field(typename, "pageInfo") is None:
            return None
        return nodes.type_name if nodes.kind == "OBJECT" else None


_schemas: dict[str, LinearSchema] = {}


def _unwrapped(type_ref: Any) -> dict[str, Any]:
    found = type_ref if isinstance(type_ref, dict) else {}
    while isinstance(found.get("ofType"), dict):
        found = found["ofType"]
    return found


def _required(arg: dict[str, Any]) -> bool:
    kind = (arg.get("type") or {}).get("kind")
    return kind == "NON_NULL" and arg.get("defaultValue") is None


def _schema_types(answer: Any) -> list[Any]:
    data = answer.get("data") if isinstance(answer, dict) else None
    found = data.get("__schema") if isinstance(data, dict) else None
    types = found.get("types") if isinstance(found, dict) else None
    return types if isinstance(types, list) else []


def _lookup_name(typename: str) -> str:
    return typename[:1].lower() + typename[1:]


def parse_schema(answer: Any, members: Any = None) -> LinearSchema | None:
    member_types = {
        each.get("name"): each.get("possibleTypes")
        for each in _schema_types(members)
        if isinstance(each, dict)
    }
    data = answer.get("data") if isinstance(answer, dict) else None
    found = data.get("__schema") if isinstance(data, dict) else None
    if not isinstance(found, dict) or not isinstance(found.get("types"), list):
        return None
    kinds: dict[str, str] = {}
    fields: dict[str, list[SchemaField]] = {}
    possible: dict[str, list[str]] = {}
    for each in found["types"]:
        name = each.get("name") if isinstance(each, dict) else None
        if not isinstance(name, str) or name.startswith("__"):
            continue
        kinds[name] = str(each.get("kind"))
        possible[name] = [str(p.get("name")) for p in member_types.get(name) or [] if p]
        fields[name] = [
            SchemaField(
                name=str(f.get("name")),
                kind=str(_unwrapped(f.get("type")).get("kind")),
                type_name=str(_unwrapped(f.get("type")).get("name")),
                args=frozenset(str(a.get("name")) for a in f.get("args") or []),
                needs_args=any(_required(a) for a in f.get("args") or []),
            )
            for f in each.get("fields") or []
            if isinstance(f, dict)
        ]
    root = str((found.get("queryType") or {}).get("name") or QUERY)
    lookups: dict[str, str] = {}
    for each in found["types"]:
        if not isinstance(each, dict) or each.get("name") != root:
            continue
        for f in each.get("fields") or []:
            args = f.get("args") or []
            target = _unwrapped(f.get("type"))
            typename = str(target.get("name"))
            name = str(f.get("name"))
            if (
                target.get("kind") == "OBJECT"
                and [a.get("name") for a in args if _required(a)] == ["id"]
                and (typename not in lookups or name == _lookup_name(typename))
            ):
                lookups[typename] = name
    if ISSUE not in fields or ISSUE not in lookups:
        return None
    return LinearSchema(kinds, fields, possible, lookups)


def schema_request() -> dict[str, Any]:
    return {"query": SCHEMA_QUERY, "operationName": SCHEMA_OPERATION}


def members_request() -> dict[str, Any]:
    return {"query": MEMBERS_QUERY, "operationName": MEMBERS_OPERATION}


def _is_ref(schema: LinearSchema, typename: str) -> bool:
    return schema.has_id(typename) and typename in schema.lookups


def _abstract_selection(schema: LinearSchema, typename: str) -> str:
    if schema.has_id(typename):
        return "__typename id"
    members = [m for m in schema.possible.get(typename, []) if schema.has_id(m)]
    return " ".join(["__typename", *(f"... on {m} {{ id }}" for m in members)])


def selection(
    schema: LinearSchema,
    typename: str,
    skip: set[tuple[str, str]],
    depth: int = 0,
) -> str:
    parts = ["__typename"]
    for each in schema.fields.get(typename, []):
        if each.needs_args or (typename, each.name) in skip:
            continue
        if each.kind in LEAF_KINDS:
            parts.append(each.name)
        elif each.kind in ABSTRACT_KINDS:
            parts.append(
                f"{each.name} {{ {_abstract_selection(schema, each.type_name)} }}"
            )
        elif each.kind != "OBJECT" or schema.node_type(each.type_name) is not None:
            continue
        elif _is_ref(schema, each.type_name):
            parts.append(f"{each.name} {{ __typename id }}")
        elif depth < MAX_INLINE_DEPTH:
            parts.append(
                f"{each.name} {{ {selection(schema, each.type_name, skip, depth + 1)} }}"
            )
        elif schema.has_id(each.type_name):
            parts.append(f"{each.name} {{ __typename id }}")
    return " ".join(parts)


def _too_big(errors: list[Any]) -> bool:
    return any(
        any(
            word in str(error.get("message", "")).lower()
            or word in json.dumps(error.get("extensions") or {}).lower()
            for word in TOO_BIG_WORDS
        )
        for error in errors
        if isinstance(error, dict)
    )


def _failed_roots(answer: Any, roots: dict[str, str]) -> set[str]:
    return {
        error["path"][0]
        for error in _errors(answer)
        if isinstance(error, dict)
        and isinstance(error.get("path"), list)
        and len(error["path"]) == 1
        and error["path"][0] in roots
    }


def _errors(answer: Any) -> list[Any]:
    errors = answer.get("errors") if isinstance(answer, dict) else None
    return errors if isinstance(errors, list) else []


@dataclass
class _Connection:
    name: str
    node_type: str
    archived: bool
    page: int = FIRST_PAGE
    cursor: str | None = None
    done: bool = False


@dataclass
class _Reading:
    schema: LinearSchema
    wanted: str
    skip: set[tuple[str, str]] = field(default_factory=set)
    exchanges: list[dict[str, Any]] = field(default_factory=list)
    lists: dict[str, dict[str, Any]] = field(default_factory=dict)
    refs: dict[str, tuple[str, str]] = field(default_factory=dict)
    full: set[str] = field(default_factory=set)
    issue_id: str | None = None
    complete: bool = True
    sent: int = 0

    def connections(self) -> list[_Connection]:
        found = []
        for each in self.schema.fields.get(ISSUE, []):
            node_type = (
                self.schema.node_type(each.type_name) if each.kind == "OBJECT" else None
            )
            if node_type is None or each.needs_args:
                continue
            found.append(
                _Connection(each.name, node_type, "includeArchived" in each.args)
            )
        return found

    def issue_request(self, parts: list[Any]) -> dict[str, Any]:
        pieces = []
        for part in parts:
            if part == BASE:
                pieces.append(selection(self.schema, ISSUE, self.skip))
                continue
            args = [f"first: {part.page}"]
            if part.archived:
                args.append("includeArchived: true")
            if part.cursor is not None:
                args.append(f"after: {json.dumps(part.cursor)}")
            nodes = selection(self.schema, part.node_type, self.skip)
            pieces.append(
                f"{part.name}({', '.join(args)}) {{ nodes {{ {nodes} }} "
                "pageInfo { hasNextPage endCursor } }"
            )
        if BASE not in parts:
            pieces.insert(0, "__typename id")
        return {
            "query": (
                f"query {WHOLE_OPERATION}($id: String!) {{ issue(id: $id) "
                f"{{ {' '.join(pieces)} }} }}"
            ),
            "operationName": WHOLE_OPERATION,
            "variables": {"id": self.wanted},
        }

    def owner_of(
        self, path: list[Any], roots: dict[str, str]
    ) -> tuple[str, str] | None:
        names = [p for p in path if isinstance(p, str)]
        if len(names) < 2 or names[0] not in roots:
            return None
        typename = roots[names[0]]
        for name in names[1:-1]:
            found = self.schema.field(typename, name) or next(
                (
                    self.schema.field(m, name)
                    for m in self.schema.possible.get(typename, [])
                    if self.schema.field(m, name)
                ),
                None,
            )
            if found is None:
                return None
            typename = found.type_name
            nodes = self.schema.node_type(typename)
            if nodes is not None:
                typename = nodes
        return (typename, names[-1])

    def broken_fields(self, answer: Any, roots: dict[str, str]) -> set[tuple[str, str]]:
        found = set()
        for error in _errors(answer):
            path = error.get("path") if isinstance(error, dict) else None
            owner = self.owner_of(path, roots) if isinstance(path, list) else None
            if owner is not None and owner[1] not in ("nodes", "pageInfo"):
                found.add(owner)
        return found - self.skip

    def note(self, value: Any) -> None:
        if isinstance(value, list):
            for item in value:
                self.note(item)
            return
        if not isinstance(value, dict):
            return
        typename, entity_id = value.get("__typename"), value.get("id")
        if isinstance(typename, str) and isinstance(entity_id, str):
            key = f"{typename}:{entity_id}"
            if set(value) - {"__typename", "id"}:
                self.full.add(key)
            else:
                self.refs.setdefault(key, (typename, entity_id))
        for item in value.values():
            self.note(item)

    def take_issue(self, parts: list[Any], answer: Any) -> str:
        if not isinstance(answer, dict):
            self.complete = False
            return "stop"
        errors = _errors(answer)
        if errors and _too_big(errors):
            return "too-big"
        broken = self.broken_fields(answer, {"issue": ISSUE})
        if broken:
            self.skip |= broken
            return "retry"
        data = answer.get("data")
        issue = data.get("issue") if isinstance(data, dict) else None
        if not isinstance(issue, dict):
            if BASE in parts:
                return "missing"
            self.complete = False
            return "stop"
        if errors:
            self.complete = False
        self.issue_id = self.issue_id or str(issue.get("id"))
        for part in parts:
            if part == BASE:
                continue
            value = issue.get(part.name)
            listed = self.lists.setdefault(
                part.name, {"type": part.node_type, "ids": []}
            )
            nodes = value.get("nodes") if isinstance(value, dict) else None
            for node in nodes or []:
                if isinstance(node, dict) and isinstance(node.get("id"), str):
                    listed["ids"].append(node["id"])
            page_info = (
                (value or {}).get("pageInfo") if isinstance(value, dict) else None
            )
            if isinstance(page_info, dict) and page_info.get("hasNextPage"):
                part.cursor = page_info.get("endCursor")
                part.done = not isinstance(part.cursor, str)
                if part.done:
                    self.complete = False
            else:
                part.done = True
        self.note(issue)
        return "ok"

    def read_issue(self) -> Reads:
        connections = self.connections()
        pending: list[Any] = [BASE, *connections]
        size = len(pending)
        while pending:
            if self.sent >= MAX_REQUESTS:
                self.complete = False
                return "ok"
            group = pending[:size]
            body = self.issue_request(group)
            answer = yield body
            self.sent += 1
            outcome = self.take_issue(group, answer)
            if outcome == "missing":
                return "missing"
            if outcome == "stop":
                return "ok"
            if outcome == "retry":
                continue
            if outcome == "too-big":
                if size > 1:
                    size = max(1, size // 2)
                    continue
                part = group[0]
                if part == BASE or part.page <= 1:
                    self.complete = False
                    pending = pending[1:]
                    continue
                part.page = max(1, part.page // 2)
                continue
            self.exchanges.append({"request": body, "response": answer})
            pending = [p for p in pending if p != BASE and not p.done]
            size = max(size, 1)
        return "ok"

    def lookup_request(self, batch: list[tuple[str, str]]) -> tuple[dict, dict]:
        pieces, variables, roots = [], {}, {}
        for index, (typename, entity_id) in enumerate(batch):
            alias = f"e{index}"
            roots[alias] = typename
            variables[alias] = entity_id
            pieces.append(
                f"{alias}: {self.schema.lookups[typename]}(id: ${alias}) "
                f"{{ {selection(self.schema, typename, self.skip)} }}"
            )
        declared = ", ".join(f"${alias}: String!" for alias in variables)
        return {
            "query": f"query {LOOKUP_OPERATION}({declared}) {{ {' '.join(pieces)} }}",
            "operationName": LOOKUP_OPERATION,
            "variables": variables,
        }, roots

    def read_lookups(self) -> Reads:
        wanted = [
            ref
            for key, ref in self.refs.items()
            if key not in self.full and ref[0] in self.schema.lookups
        ]
        size = LOOKUP_BATCH
        while wanted:
            if self.sent >= MAX_REQUESTS:
                self.complete = False
                return
            batch = wanted[:size]
            body, roots = self.lookup_request(batch)
            answer = yield body
            self.sent += 1
            errors = _errors(answer)
            if errors and _too_big(errors):
                if size > 1:
                    size = max(1, size // 2)
                    continue
                wanted = wanted[1:]
                self.complete = False
                continue
            broken = self.broken_fields(answer, roots)
            if broken:
                self.skip |= broken
                continue
            gone = _failed_roots(answer, roots)
            if gone:
                wanted = [
                    ref for index, ref in enumerate(batch) if f"e{index}" not in gone
                ] + wanted[len(batch) :]
                continue
            data = answer.get("data") if isinstance(answer, dict) else None
            if not isinstance(data, dict):
                self.complete = False
                wanted = wanted[len(batch) :]
                continue
            self.exchanges.append({"request": body, "response": answer})
            for value in data.values():
                if isinstance(value, dict):
                    self.full.add(f"{value.get('__typename')}:{value.get('id')}")
            wanted = wanted[len(batch) :]

    def result(self) -> dict[str, Any]:
        types = {key.split(":", 1)[0] for key in (*self.full, *self.refs)}
        return {
            "id": self.issue_id,
            "exchanges": self.exchanges,
            "lists": self.lists,
            "lookups": {
                self.schema.lookups[t]: t
                for t in sorted(types)
                if t in self.schema.lookups
            },
            "complete": self.complete,
            "requests": self.sent,
        }


def whole_issue_reads(wanted: str) -> Reads:
    schema = _schemas.get("linear")
    if schema is None:
        types = yield schema_request()
        members = yield members_request()
        schema = parse_schema(types, members)
        if schema is None:
            return None
        _schemas["linear"] = schema
    reading = _Reading(schema, wanted)
    outcome = yield from reading.read_issue()
    if outcome == "missing" or reading.issue_id is None:
        return None
    yield from reading.read_lookups()
    return reading.result()


def run_reads(reads: Reads, send: Callable[[dict[str, Any]], Any]) -> Any:
    try:
        body = next(reads)
        while True:
            body = reads.send(send(body))
    except StopIteration as stop:
        return stop.value


async def run_reads_async(
    reads: Reads, send: Callable[[dict[str, Any]], Awaitable[Any]]
) -> Any:
    try:
        body = next(reads)
        while True:
            body = reads.send(await send(body))
    except StopIteration as stop:
        return stop.value


def forget_schema() -> None:
    _schemas.clear()
