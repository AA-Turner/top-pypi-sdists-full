from __future__ import annotations

import copy
import datetime
import json
import os
import urllib.error
import urllib.request
from collections.abc import Callable
from contextvars import ContextVar
from dataclasses import dataclass, field
from typing import Any, NoReturn

from bitfab import service_calls
from bitfab.linear_graphql import (
    Document,
    Field,
    GraphQLSyntaxError,
    arguments_of,
    fields_of,
    operation_of,
    parse,
    variables_with_defaults,
)
from bitfab.linear_whole import run_reads, whole_issue_reads
from bitfab.mock_override import MockOverrideCtx, SpanNodeMeta
from bitfab.sandbox import Sandbox, SandboxStartCtx, fail_replay_item, sandbox_now
from bitfab.whole_objects import is_whole, mark_whole

LINEAR_SANDBOX_NAME = "Linear"
LINEAR_INTEGRATION = "linear"
LINEAR_SPAN_PREFIX = "linear."
QUERY_SPAN_PREFIX = "linear.query."
MUTATION_SPAN_PREFIX = "linear.mutation."
RECORDED = "recorded"
READ_WHOLE_OBJECT = "test-read-whole-object"
LINEAR_MODES = (READ_WHOLE_OBJECT, RECORDED)
ISSUE = "Issue"
LINEAR_API_URL = "https://api.linear.app/graphql"
TOKEN_ENV = "BITFAB_LINEAR_TOKEN"
TIMEOUT_SECONDS = 60.0
AUTH_ERROR_CODES = frozenset({"AUTHENTICATION_ERROR", "FORBIDDEN"})
CURSOR_PREFIX = "bitfab-offset:"
DEFAULT_PAGE_SIZE = 50
QUERY = "Query"
MUTATION = "Mutation"
SANDBOX_ID_PREFIX = "00000000-0000-4000-8000-"
PRIORITY_LABELS = {0: "No priority", 1: "Urgent", 2: "High", 3: "Medium", 4: "Low"}

ROOT_LOOKUPS = {
    "issue": "Issue",
    "team": "Team",
    "project": "Project",
    "workflowState": "WorkflowState",
    "comment": "Comment",
    "user": "User",
    "issueLabel": "IssueLabel",
    "cycle": "Cycle",
}
ROOT_LISTS = {
    "issues": "Issue",
    "teams": "Team",
    "projects": "Project",
    "workflowStates": "WorkflowState",
    "comments": "Comment",
    "users": "User",
    "issueLabels": "IssueLabel",
    "cycles": "Cycle",
}
FIELD_TYPES = {
    (QUERY, "viewer"): "User",
    (QUERY, "organization"): "Organization",
    ("Issue", "team"): "Team",
    ("Issue", "state"): "WorkflowState",
    ("Issue", "assignee"): "User",
    ("Issue", "creator"): "User",
    ("Issue", "delegate"): "User",
    ("Issue", "project"): "Project",
    ("Issue", "parent"): "Issue",
    ("Issue", "cycle"): "Cycle",
    ("Comment", "issue"): "Issue",
    ("Comment", "user"): "User",
    ("Comment", "parent"): "Comment",
    ("WorkflowState", "team"): "Team",
    ("Project", "lead"): "User",
    ("Project", "creator"): "User",
    ("IssueLabel", "team"): "Team",
    ("IssueLabel", "parent"): "IssueLabel",
    ("Cycle", "team"): "Team",
    ("Team", "defaultIssueState"): "WorkflowState",
    ("IssuePayload", "issue"): "Issue",
    ("IssueArchivePayload", "entity"): "Issue",
    ("CommentPayload", "comment"): "Comment",
    ("IssueRelation", "issue"): "Issue",
    ("IssueRelation", "relatedIssue"): "Issue",
    ("Attachment", "issue"): "Issue",
}
CONNECTIONS: dict[tuple[str, str], tuple[str, str, str | None]] = {
    ("Issue", "comments"): ("Comment", "back", "issue"),
    ("Issue", "children"): ("Issue", "back", "parent"),
    ("Issue", "labels"): ("IssueLabel", "ids", "labelIds"),
    ("Issue", "subscribers"): ("User", "list", None),
    ("Team", "issues"): ("Issue", "back", "team"),
    ("Team", "states"): ("WorkflowState", "back", "team"),
    ("Team", "labels"): ("IssueLabel", "back", "team"),
    ("Team", "cycles"): ("Cycle", "back", "team"),
    ("Team", "projects"): ("Project", "list", None),
    ("Team", "members"): ("User", "list", None),
    ("Project", "issues"): ("Issue", "back", "project"),
    ("Project", "teams"): ("Team", "list", None),
    ("Project", "members"): ("User", "list", None),
    ("User", "assignedIssues"): ("Issue", "back", "assignee"),
    ("User", "createdIssues"): ("Issue", "back", "creator"),
    ("User", "teams"): ("Team", "list", None),
    ("Comment", "children"): ("Comment", "back", "parent"),
    ("Issue", "relations"): ("IssueRelation", "back", "issue"),
    ("Issue", "inverseRelations"): ("IssueRelation", "back", "relatedIssue"),
    ("Issue", "attachments"): ("Attachment", "back", "issue"),
}
PAYLOADS = {
    "issueCreate": ("IssuePayload", "issue"),
    "issueUpdate": ("IssuePayload", "issue"),
    "issueAddLabel": ("IssuePayload", "issue"),
    "issueRemoveLabel": ("IssuePayload", "issue"),
    "issueArchive": ("IssueArchivePayload", "entity"),
    "issueUnarchive": ("IssueArchivePayload", "entity"),
    "issueDelete": ("IssueArchivePayload", "entity"),
    "commentCreate": ("CommentPayload", "comment"),
    "commentUpdate": ("CommentPayload", "comment"),
    "commentDelete": ("DeletePayload", None),
}
CREATED_BY = {"issueCreate": "Issue", "commentCreate": "Comment"}
CHANGED_BY = {
    "issueUpdate": "Issue",
    "issueAddLabel": "Issue",
    "issueRemoveLabel": "Issue",
    "issueArchive": "Issue",
    "issueUnarchive": "Issue",
    "issueDelete": "Issue",
    "commentUpdate": "Comment",
    "commentDelete": "Comment",
}
ANSWERED_OK = frozenset(
    {
        "attachmentCreate",
        "attachmentDelete",
        "attachmentLinkURL",
        "favoriteCreate",
        "issueRelationCreate",
        "issueRelationDelete",
        "issueReminder",
        "issueSubscribe",
        "issueUnsubscribe",
        "notificationArchive",
        "notificationUpdate",
        "reactionCreate",
        "reactionDelete",
    }
)
COMPARATORS = frozenset(
    {
        "eq",
        "neq",
        "in",
        "nin",
        "lt",
        "lte",
        "gt",
        "gte",
        "null",
        "contains",
        "containsIgnoreCase",
        "notContains",
        "notContainsIgnoreCase",
        "startsWith",
        "startsWithIgnoreCase",
        "notStartsWith",
        "endsWith",
        "notEndsWith",
        "eqIgnoreCase",
        "neqIgnoreCase",
    }
)
SEED_KEYS = {
    "teams": "Team",
    "projects": "Project",
    "workflowStates": "WorkflowState",
    "issues": "Issue",
    "comments": "Comment",
    "users": "User",
    "issueLabels": "IssueLabel",
    "cycles": "Cycle",
}
STATE_KEYS = (
    "entities",
    "lists",
    "root",
    "created",
    "changed",
    "deleted",
    "writes",
    "readsFromTrace",
    "liveReads",
    "missing",
    "wholeObjects",
    "wholeLists",
    "lookups",
    "nextId",
    "lastSyncId",
)


class LinearNotRecordedError(RuntimeError):
    pass


class LinearCallRefusedError(RuntimeError):
    pass


class LinearModeError(ValueError):
    pass


class LinearCredentialError(RuntimeError):
    pass


class _NotAnswerable(Exception):
    def __init__(self, message: str, ref: str | None = None) -> None:
        super().__init__(message)
        self.ref = ref


class _FieldError(Exception):
    def __init__(self, message: str, code: str = "INPUT_ERROR") -> None:
        super().__init__(message)
        self.code = code

    def as_error(self, path: list[str]) -> dict[str, Any]:
        return {
            "message": str(self),
            "path": path,
            "extensions": {
                "code": self.code,
                "type": "invalid input",
                "userPresentableMessage": str(self),
            },
        }


@dataclass
class _Walk:
    state: dict[str, Any]
    document: Document
    variables: dict[str, Any]
    protected: set[str] = field(default_factory=set)
    skipped: set[str] = field(default_factory=set)
    live: LinearLive | None = None
    touched: set[str] = field(default_factory=set)


def _text(value: Any) -> str | None:
    return value if isinstance(value, str) and value != "" else None


def _canonical(args: dict[str, Any]) -> dict[str, Any]:
    return {name: value for name, value in args.items() if value is not None}


def _storage_key(name: str, args: dict[str, Any]) -> str:
    args = _canonical(args)
    if not args:
        return name
    return f"{name}({json.dumps(args, sort_keys=True, default=str)})"


def _ref_key(typename: str, entity_id: str) -> str:
    return f"{typename}:{entity_id}"


def _list_key(owner: str, name: str, args: dict[str, Any]) -> str:
    return json.dumps([owner, name, _canonical(args)], sort_keys=True, default=str)


def _ref(typename: str, entity_id: str) -> dict[str, str]:
    return {"__typename": typename, "id": entity_id}


def _ref_id(value: Any) -> str | None:
    return _text(value.get("id")) if isinstance(value, dict) else None


def _entities(state: dict[str, Any], typename: str) -> dict[str, dict[str, Any]]:
    return state["entities"].setdefault(typename, {})


def _mark(state: dict[str, Any], kind: str, ref: str) -> None:
    if ref not in state[kind]:
        state[kind].append(ref)


def _connection_info(
    owner_type: str | None, name: str
) -> tuple[str, str, str | None] | None:
    if owner_type == QUERY and name in ROOT_LISTS:
        return (ROOT_LISTS[name], "all", None)
    return CONNECTIONS.get((owner_type or "", name))


def _lookup_type(state: dict[str, Any], name: str) -> str | None:
    return ROOT_LOOKUPS.get(name) or state.get("lookups", {}).get(name)


def _hint(owner_type: str | None, name: str) -> str | None:
    if owner_type == QUERY and name in ROOT_LOOKUPS:
        return ROOT_LOOKUPS[name]
    return FIELD_TYPES.get((owner_type or "", name))


def _sub_fields(walk: _Walk, field_node: Field) -> list[Field]:
    return fields_of(field_node.selections or [], walk.document, None, walk.variables)


def _asks_connection(walk: _Walk, field_node: Field) -> bool:
    return field_node.selections is not None and any(
        sub.name in ("nodes", "edges") for sub in _sub_fields(walk, field_node)
    )


def _empty_state(mode: str = RECORDED) -> dict[str, Any]:
    return {
        "mode": mode,
        "entities": {},
        "lists": {},
        "root": {},
        "created": [],
        "changed": [],
        "deleted": [],
        "writes": [],
        "readsFromTrace": [],
        "liveReads": [],
        "missing": [],
        "wholeObjects": {},
        "wholeLists": {},
        "lookups": {},
        "nextId": 1,
        "lastSyncId": 0,
    }


def _normalize_fields(
    walk: _Walk,
    typename: str | None,
    obj: dict[str, Any],
    selections: list[Any],
    owner: str | None,
) -> dict[str, Any]:
    stored: dict[str, Any] = {}
    extra: dict[str, Any] = {}
    for field_node in fields_of(selections, walk.document, typename, walk.variables):
        if field_node.key not in obj or field_node.name == "__typename":
            continue
        value = obj[field_node.key]
        args = arguments_of(field_node, walk.variables)
        if field_node.selections is None:
            stored[_storage_key(field_node.name, args)] = copy.deepcopy(value)
            continue
        if (
            owner is not None
            and isinstance(value, dict)
            and _asks_connection(walk, field_node)
        ):
            extra.update(
                _normalize_connection(walk, typename, owner, field_node, args, value)
            )
            continue
        stored[_storage_key(field_node.name, args)] = _normalize_value(
            walk,
            _hint(typename, field_node.name),
            _with_lookup_id(walk, typename, field_node, args, value),
            field_node.selections,
        )
    return {**{k: v for k, v in extra.items() if k not in stored}, **stored}


def _with_lookup_id(
    walk: _Walk,
    typename: str | None,
    field_node: Field,
    args: dict[str, Any],
    value: Any,
) -> Any:
    wanted = _text(args.get("id"))
    looked_up = _lookup_type(walk.state, field_node.name)
    if (
        typename != QUERY
        or looked_up is None
        or not isinstance(value, dict)
        or _text(value.get("id"))
        or wanted is None
    ):
        return value
    known = _find(walk.state, looked_up, wanted)
    return {**value, "id": known["id"] if known is not None else wanted}


def _normalize_value(
    walk: _Walk, hint: str | None, value: Any, selections: list[Any]
) -> Any:
    if isinstance(value, list):
        return [_normalize_value(walk, hint, item, selections) for item in value]
    if not isinstance(value, dict):
        return copy.deepcopy(value)
    typename = _text(value.get("__typename")) or hint
    entity_id = _text(value.get("id"))
    if typename is not None and entity_id is not None:
        _normalize_entity(walk, typename, value, selections)
        return _ref(typename, entity_id)
    return _normalize_fields(walk, typename, value, selections, None)


def _normalize_entity(
    walk: _Walk, typename: str, obj: dict[str, Any], selections: list[Any]
) -> str | None:
    entity_id = str(obj["id"])
    ref = _ref_key(typename, entity_id)
    if ref in walk.skipped:
        return None
    fields = _normalize_fields(walk, typename, obj, selections, ref)
    entities = _entities(walk.state, typename)
    existing = entities.get(entity_id, {})
    if ref in walk.protected:
        entities[entity_id] = {**fields, **existing, "id": entity_id}
    else:
        entities[entity_id] = {**existing, **fields, "id": entity_id}
    return entity_id


def _connection_nodes(
    walk: _Walk, field_node: Field, value: dict[str, Any]
) -> tuple[list[Any], list[Any]]:
    for sub in _sub_fields(walk, field_node):
        if sub.name == "nodes" and isinstance(value.get(sub.key), list):
            return value[sub.key], sub.selections or []
        if sub.name == "edges" and isinstance(value.get(sub.key), list):
            node = next((n for n in _sub_fields(walk, sub) if n.name == "node"), None)
            if node is None:
                return [], []
            return [
                edge.get(node.key) for edge in value[sub.key] if isinstance(edge, dict)
            ], node.selections or []
    return [], []


def _page_info_of(walk: _Walk, field_node: Field, value: dict[str, Any]) -> Any:
    found = next(
        (sub for sub in _sub_fields(walk, field_node) if sub.name == "pageInfo"), None
    )
    if found is None or not isinstance(value.get(found.key), dict):
        return None
    return _normalize_fields(
        walk, "PageInfo", value[found.key], found.selections or [], None
    )


def _normalize_connection(
    walk: _Walk,
    owner_type: str | None,
    owner: str,
    field_node: Field,
    args: dict[str, Any],
    value: dict[str, Any],
) -> dict[str, Any]:
    info = _connection_info(owner_type, field_node.name)
    raw_nodes, node_selections = _connection_nodes(walk, field_node, value)
    owner_id = owner.split(":", 1)[1] if ":" in owner else None
    node_type = info[0] if info else None
    ids: list[str] = []
    for node in raw_nodes:
        if not isinstance(node, dict) or _text(node.get("id")) is None:
            continue
        typename = _text(node.get("__typename")) or node_type
        if typename is None:
            continue
        node_type = typename
        entity_id = _normalize_entity(walk, typename, node, node_selections)
        if entity_id is None:
            continue
        ids.append(entity_id)
        entity = _entities(walk.state, typename)[entity_id]
        if info and info[1] == "back" and owner_id and info[2] not in entity:
            entity[info[2]] = _ref(owner_type or "", owner_id)
    page_info = _page_info_of(walk, field_node, value)
    walk.state["lists"][_list_key(owner, field_node.name, args)] = {
        "type": node_type,
        "ids": ids,
        "pageInfo": page_info,
    }
    complete = not (isinstance(page_info, dict) and page_info.get("hasNextPage"))
    if info and info[1] == "ids" and complete and not args.get("filter"):
        return {info[2] or "": ids}
    return {}


def _visible(state: dict[str, Any], typename: str, entity: dict[str, Any]) -> bool:
    return _ref_key(typename, entity["id"]) not in state["deleted"]


def _is_made(state: dict[str, Any], ref: str) -> bool:
    return ref in state["created"]


def _find(
    state: dict[str, Any], typename: str, wanted: str | None
) -> dict[str, Any] | None:
    if wanted is None:
        return None
    entities = _entities(state, typename)
    if wanted in entities:
        return entities[wanted]
    lowered = wanted.lower()
    alias = {"Issue": "identifier", "Team": "key"}.get(typename)
    if alias is None:
        return None
    return next(
        (e for e in entities.values() if str(e.get(alias) or "").lower() == lowered),
        None,
    )


def _project(
    walk: _Walk,
    typename: str | None,
    entity: dict[str, Any],
    selections: list[Any],
    made: bool,
) -> dict[str, Any]:
    projected: dict[str, Any] = {}
    entity_id = _text(entity.get("id"))
    owner = (
        QUERY
        if typename == QUERY
        else (_ref_key(typename, entity_id) if typename and entity_id else None)
    )
    if typename == ISSUE and entity_id:
        walk.touched.add(entity_id)
    for field_node in fields_of(selections, walk.document, typename, walk.variables):
        args = arguments_of(field_node, walk.variables)
        if field_node.name == "__typename":
            projected[field_node.key] = typename
            continue
        looked_up = (
            _lookup_type(walk.state, field_node.name) if typename == QUERY else None
        )
        if looked_up is not None:
            projected[field_node.key] = _lookup(walk, looked_up, args, field_node)
            continue
        stored_key = _storage_key(field_node.name, args)
        if (
            owner is not None
            and stored_key not in entity
            and _asks_connection(walk, field_node)
        ):
            projected[field_node.key] = _connection(
                walk, typename, entity, owner, field_node, args
            )
            continue
        if stored_key not in entity:
            if made:
                projected[field_node.key] = None
                continue
            raise _NotAnswerable(f"{typename or 'an object'}.{field_node.name}", owner)
        projected[field_node.key] = _project_value(
            walk,
            _hint(typename, field_node.name),
            entity[stored_key],
            field_node.selections,
            made,
        )
    return projected


def _project_value(
    walk: _Walk, hint: str | None, value: Any, selections: list[Any] | None, made: bool
) -> Any:
    if selections is None or value is None:
        return copy.deepcopy(value)
    if isinstance(value, list):
        return [_project_value(walk, hint, item, selections, made) for item in value]
    if not isinstance(value, dict):
        return copy.deepcopy(value)
    typename = _text(value.get("__typename")) or hint
    entity_id = _text(value.get("id"))
    if typename is not None and entity_id is not None:
        ref = _ref_key(typename, entity_id)
        if ref in walk.state["deleted"]:
            return None
        known = _entities(walk.state, typename).get(entity_id) or {}
        return _project(
            walk,
            typename,
            {**value, **known},
            selections,
            _is_made(walk.state, ref),
        )
    return _project(walk, typename, value, selections, made)


def _not_found(typename: str) -> _FieldError:
    return _FieldError(f"Entity not found: {typename}")


def _is_gone(state: dict[str, Any], typename: str, wanted: str) -> bool:
    return _ref_key(typename, wanted) in state["deleted"] or _ref_key(
        typename, wanted
    ) in state.get("missing", [])


def _lookup(
    walk: _Walk, typename: str, args: dict[str, Any], field_node: Field
) -> dict[str, Any]:
    wanted = _text(args.get("id"))
    entity = _find(walk.state, typename, wanted)
    if entity is None:
        if wanted and _is_gone(walk.state, typename, wanted):
            raise _not_found(typename)
        raise _NotAnswerable(f"{typename} {wanted}", _ref_key(typename, wanted or ""))
    ref = _ref_key(typename, entity["id"])
    if ref in walk.state["deleted"]:
        raise _not_found(typename)
    return _project(
        walk, typename, entity, field_node.selections or [], _is_made(walk.state, ref)
    )


def _all(results: list[bool | None]) -> bool | None:
    if False in results:
        return False
    return None if None in results else True


def _any(results: list[bool | None]) -> bool | None:
    if True in results:
        return True
    return None if None in results else False


def _comparable(value: Any) -> Any:
    return _ref_id(value) if isinstance(value, dict) else value


def _ordered(value: Any, other: Any) -> bool:
    numbers = (int, float)
    both_numbers = isinstance(value, numbers) and isinstance(other, numbers)
    both_text = isinstance(value, str) and isinstance(other, str)
    is_duration = both_text and other.lstrip("-").startswith("P")
    return (both_numbers or both_text) and not is_duration


def _compare_one(value: Any, operator: str, argument: Any) -> bool | None:
    if operator == "null":
        return (value is None) == bool(argument)
    if operator == "eq":
        return value == argument
    if operator == "neq":
        return value != argument
    if operator in ("in", "nin"):
        if not isinstance(argument, list):
            return None
        return (value in argument) == (operator == "in")
    if operator in ("lt", "lte", "gt", "gte"):
        if value is None:
            return False
        if not _ordered(value, argument):
            return None
        return {
            "lt": value < argument,
            "lte": value <= argument,
            "gt": value > argument,
            "gte": value >= argument,
        }[operator]
    if value is None:
        return operator.startswith("not") or operator == "neqIgnoreCase"
    if not isinstance(value, str) or not isinstance(argument, str):
        return None
    folded = "IgnoreCase" in operator
    text, wanted = (value.lower(), argument.lower()) if folded else (value, argument)
    base = operator.replace("IgnoreCase", "")
    checks = {
        "contains": wanted in text,
        "notContains": wanted not in text,
        "startsWith": text.startswith(wanted),
        "notStartsWith": not text.startswith(wanted),
        "endsWith": text.endswith(wanted),
        "notEndsWith": not text.endswith(wanted),
        "eq": text == wanted,
        "neq": text != wanted,
    }
    return checks.get(base)


def _compare(value: Any, condition: dict[str, Any]) -> bool | None:
    compared = _comparable(value)
    return _all(
        [_compare_one(compared, operator, arg) for operator, arg in condition.items()]
    )


def _members(
    walk: _Walk, owner_type: str, entity: dict[str, Any], name: str
) -> list[tuple[str, dict[str, Any]]] | None:
    info = _connection_info(owner_type, name)
    if info is None:
        return None
    try:
        ids = _candidates(walk, info, owner_type, entity)
    except _NotAnswerable:
        return None
    entities = _entities(walk.state, info[0])
    return [(info[0], entities[i]) for i in ids if i in entities]


def _collection_match(
    walk: _Walk,
    owner_type: str,
    entity: dict[str, Any],
    name: str,
    condition: dict[str, Any],
) -> bool | None:
    members = _members(walk, owner_type, entity, name)
    if members is None:
        return None
    results: list[bool | None] = []
    for operator, nested in condition.items():
        if operator == "some" and isinstance(nested, dict):
            results.append(_any([_matches(walk, t, m, nested) for t, m in members]))
        elif operator == "every" and isinstance(nested, dict):
            results.append(_all([_matches(walk, t, m, nested) for t, m in members]))
        elif operator == "length" and isinstance(nested, dict):
            results.append(_compare(len(members), nested))
        else:
            results.append(None)
    return _all(results)


def _matches(
    walk: _Walk, typename: str, entity: dict[str, Any], condition: Any
) -> bool | None:
    if not isinstance(condition, dict):
        return None
    results: list[bool | None] = []
    for name, wanted in condition.items():
        if wanted is None:
            continue
        if name in ("and", "or") and isinstance(wanted, list):
            nested = [_matches(walk, typename, entity, each) for each in wanted]
            results.append(_all(nested) if name == "and" else _any(nested))
        elif not isinstance(wanted, dict):
            results.append(None)
        elif wanted and set(wanted) <= COMPARATORS:
            results.append(_compare(entity[name], wanted) if name in entity else None)
        elif _connection_info(typename, name) is not None:
            results.append(_collection_match(walk, typename, entity, name, wanted))
        elif name not in entity:
            results.append(None)
        elif entity[name] is None:
            results.append(False)
        elif isinstance(entity[name], dict):
            related = entity[name]
            related_type = _text(related.get("__typename")) or _hint(typename, name)
            related_id = _text(related.get("id"))
            known = (
                _entities(walk.state, related_type).get(related_id or "") or {}
                if related_type
                else {}
            )
            results.append(
                _matches(walk, related_type or "", {**related, **known}, wanted)
            )
        else:
            results.append(None)
    return _all(results)


def _candidates(
    walk: _Walk,
    info: tuple[str, str, str | None],
    owner_type: str | None,
    owner_entity: dict[str, Any],
) -> list[str]:
    node_type, kind, link = info
    entities = _entities(walk.state, node_type)
    if kind == "all":
        return list(entities)
    if kind == "back":
        owner_id = owner_entity.get("id")
        return [
            entity_id
            for entity_id, entity in entities.items()
            if _ref_id(entity.get(link or "")) == owner_id
        ]
    if kind == "ids" and isinstance(owner_entity.get(link or ""), list):
        return [str(each) for each in owner_entity[link or ""]]
    raise _NotAnswerable(
        f"{owner_type}.{node_type}",
        _ref_key(owner_type or "", str(owner_entity.get("id"))),
    )


def _offset(cursor: Any) -> int:
    text = _text(cursor) or ""
    if not text.startswith(CURSOR_PREFIX):
        return 0
    try:
        return max(int(text[len(CURSOR_PREFIX) :]), 0)
    except ValueError:
        return 0


def _sorted(
    entities: dict[str, dict[str, Any]], ids: list[str], args: dict[str, Any]
) -> list[str]:
    order_by = _text(args.get("orderBy")) or "createdAt"
    values = [entities.get(i, {}).get(order_by) for i in ids]
    if not all(isinstance(v, str) for v in values):
        return ids
    return sorted(ids, key=lambda i: entities[i][order_by], reverse=True)


def _is_descending(entities: dict[str, dict[str, Any]], ids: list[str]) -> bool:
    dates = [entities.get(i, {}).get("createdAt") for i in ids]
    known = [d for d in dates if isinstance(d, str)]
    return known == sorted(known, reverse=True)


def _belongs(
    walk: _Walk,
    info: tuple[str, str, str | None] | None,
    owner_entity: dict[str, Any],
    entity: dict[str, Any],
    owner_type: str | None,
) -> bool:
    if owner_type == QUERY:
        return True
    if info is None:
        return False
    if info[1] == "back":
        return _ref_id(entity.get(info[2] or "")) == owner_entity.get("id")
    if info[1] == "ids":
        return entity["id"] in (owner_entity.get(info[2] or "") or [])
    return False


def _shown(
    walk: _Walk,
    typename: str,
    entity: dict[str, Any],
    condition: dict[str, Any],
    include_archived: bool,
) -> bool:
    ref = _ref_key(typename, entity["id"])
    if not _visible(walk.state, typename, entity):
        return False
    if ref not in walk.state["changed"]:
        return True
    if entity.get("archivedAt") and not include_archived:
        return False
    return _matches(walk, typename, entity, condition) is not False


def _needs_whole(
    walk: _Walk, owner_type: str | None, owner_entity: dict[str, Any]
) -> bool:
    owner_id = _text(owner_entity.get("id"))
    return (
        walk.live is not None
        and owner_type == ISSUE
        and owner_id is not None
        and not is_whole(walk.state, ISSUE, owner_id)
        and not _is_made(walk.state, _ref_key(ISSUE, owner_id))
    )


def _connection(
    walk: _Walk,
    owner_type: str | None,
    owner_entity: dict[str, Any],
    owner: str,
    field_node: Field,
    args: dict[str, Any],
) -> dict[str, Any]:
    info = _connection_info(owner_type, field_node.name)
    recorded = walk.state["lists"].get(_list_key(owner, field_node.name, args))
    node_type = (recorded or {}).get("type") or (info[0] if info else None)
    condition = args.get("filter") if isinstance(args.get("filter"), dict) else {}
    include_archived = args.get("includeArchived") is True
    paging = args.get("after") is not None or args.get("before") is not None
    owner_changed = owner in walk.state["changed"]
    from_ids = (
        info is not None
        and info[1] == "ids"
        and isinstance(owner_entity.get(info[2] or ""), list)
        and (recorded is None or owner_changed)
    )
    if recorded is not None and node_type is not None and not from_ids:
        entities = _entities(walk.state, node_type)
        kept = [
            i
            for i in recorded["ids"]
            if i in entities
            and _shown(walk, node_type, entities[i], condition, include_archived)
        ]
        if not paging:
            added = [
                ref.split(":", 1)[1]
                for ref in walk.state["created"]
                if ref.startswith(f"{node_type}:")
            ]
            added = [
                i
                for i in added
                if i not in kept
                and i in entities
                and _visible(walk.state, node_type, entities[i])
                and _belongs(walk, info, owner_entity, entities[i], owner_type)
                and _matches(walk, node_type, entities[i], condition) is True
            ]
            descending = _is_descending(entities, recorded["ids"])
            kept = [*reversed(added), *kept] if descending else [*kept, *added]
        return _connection_value(
            walk, node_type, kept, recorded.get("pageInfo"), field_node, 0
        )
    if _needs_whole(walk, owner_type, owner_entity):
        raise _NotAnswerable(f"{owner_type}.{field_node.name}", owner)
    whole = walk.state.get("wholeLists", {}).get(owner, {}).get(field_node.name)
    if args.get("last") is not None or args.get("before") is not None:
        raise _NotAnswerable(f"{owner_type}.{field_node.name}", owner)
    if whole is not None and (info is None or info[1] == "list"):
        return _page_of(walk, owner_type, field_node, args, whole["type"], whole["ids"])
    if walk.live is not None and owner_type != ISSUE:
        raise _NotAnswerable(f"{owner_type}.{field_node.name}")
    if info is None:
        raise _NotAnswerable(f"{owner_type}.{field_node.name}", owner)
    return _page_of(
        walk,
        owner_type,
        field_node,
        args,
        info[0],
        _candidates(walk, info, owner_type, owner_entity),
    )


def _page_of(
    walk: _Walk,
    owner_type: str | None,
    field_node: Field,
    args: dict[str, Any],
    node_type: str,
    candidates: list[str],
) -> dict[str, Any]:
    condition = args.get("filter") if isinstance(args.get("filter"), dict) else {}
    include_archived = args.get("includeArchived") is True
    entities = _entities(walk.state, node_type)
    matched: list[str] = []
    for entity_id in candidates:
        entity = entities.get(entity_id)
        if entity is None:
            raise _NotAnswerable(
                f"{node_type} {entity_id}", _ref_key(node_type, entity_id)
            )
        if not _visible(walk.state, node_type, entity):
            continue
        if entity.get("archivedAt") and not include_archived:
            continue
        found = _matches(walk, node_type, entity, condition)
        if found is None:
            raise _NotAnswerable(
                f"the filter on {owner_type}.{field_node.name}",
                _ref_key(node_type, entity_id),
            )
        if found:
            matched.append(entity_id)
    matched = _sorted(entities, matched, args)
    first = (
        args.get("first") if isinstance(args.get("first"), int) else DEFAULT_PAGE_SIZE
    )
    start = _offset(args.get("after"))
    page = matched[start : start + max(first, 0)]
    page_info = {
        "hasNextPage": start + len(page) < len(matched),
        "hasPreviousPage": start > 0,
        "startCursor": f"{CURSOR_PREFIX}{start}" if page else None,
        "endCursor": f"{CURSOR_PREFIX}{start + len(page)}" if page else None,
    }
    return _connection_value(walk, node_type, page, page_info, field_node, start)


def _project_node(
    walk: _Walk, node_type: str, entity_id: str, selections: list[Any]
) -> dict[str, Any]:
    entity = _entities(walk.state, node_type).get(entity_id)
    if entity is None:
        raise _NotAnswerable(f"{node_type} {entity_id}", _ref_key(node_type, entity_id))
    ref = _ref_key(node_type, entity_id)
    return _project(walk, node_type, entity, selections, _is_made(walk.state, ref))


def _connection_value(
    walk: _Walk,
    node_type: str,
    ids: list[str],
    page_info: Any,
    field_node: Field,
    start: int,
) -> dict[str, Any]:
    value: dict[str, Any] = {}
    for sub in _sub_fields(walk, field_node):
        if sub.name == "__typename":
            value[sub.key] = f"{node_type}Connection"
        elif sub.name == "nodes":
            value[sub.key] = [
                _project_node(walk, node_type, i, sub.selections or []) for i in ids
            ]
        elif sub.name == "edges":
            value[sub.key] = [
                _edge(walk, node_type, i, sub, start + index + 1)
                for index, i in enumerate(ids)
            ]
        elif sub.name == "pageInfo":
            value[sub.key] = _project_value(
                walk, "PageInfo", page_info or {}, sub.selections, True
            )
        else:
            value[sub.key] = None
    return value


def _edge(
    walk: _Walk, node_type: str, entity_id: str, edge: Field, position: int
) -> dict[str, Any]:
    value: dict[str, Any] = {}
    for sub in _sub_fields(walk, edge):
        if sub.name == "node":
            value[sub.key] = _project_node(
                walk, node_type, entity_id, sub.selections or []
            )
        elif sub.name == "cursor":
            value[sub.key] = f"{CURSOR_PREFIX}{position}"
        elif sub.name == "__typename":
            value[sub.key] = f"{node_type}Edge"
    return value


def _now() -> str:
    now = sandbox_now() or datetime.datetime.now(datetime.timezone.utc)
    utc = now.astimezone(datetime.timezone.utc)
    return utc.strftime("%Y-%m-%dT%H:%M:%S.") + f"{utc.microsecond // 1000:03d}Z"


def _new_id(state: dict[str, Any]) -> str:
    number = int(state.get("nextId") or 1)
    state["nextId"] = number + 1
    return f"{SANDBOX_ID_PREFIX}{number:012d}"


def _sync_id(state: dict[str, Any]) -> int:
    state["lastSyncId"] = int(state.get("lastSyncId") or 0) + 1
    return state["lastSyncId"]


def _team_key(state: dict[str, Any], team_id: str) -> str | None:
    team = _entities(state, "Team").get(team_id) or {}
    if _text(team.get("key")):
        return team["key"]
    for issue in _entities(state, "Issue").values():
        identifier = _text(issue.get("identifier"))
        if _ref_id(issue.get("team")) == team_id and identifier and "-" in identifier:
            return identifier.rsplit("-", 1)[0]
    return None


def _issue_number(issue: dict[str, Any], key: str) -> int | None:
    if isinstance(issue.get("number"), (int, float)):
        return int(issue["number"])
    identifier = _text(issue.get("identifier")) or ""
    prefix, _, number = identifier.rpartition("-")
    return int(number) if prefix == key and number.isdigit() else None


def _next_number(state: dict[str, Any], team_id: str, key: str) -> int:
    numbers = [
        number
        for issue in _entities(state, "Issue").values()
        if _ref_id(issue.get("team")) == team_id
        or (_text(issue.get("identifier")) or "").startswith(f"{key}-")
        for number in [_issue_number(issue, key)]
        if number is not None
    ]
    return max(numbers, default=0) + 1


def _issue_url_base(state: dict[str, Any]) -> str:
    for issue in _entities(state, "Issue").values():
        url = _text(issue.get("url"))
        if url and "/issue/" in url:
            return url.split("/issue/", 1)[0] + "/issue/"
    return "https://linear.app/issue/"


def _default_state(state: dict[str, Any], team_id: str) -> dict[str, str] | None:
    team = _entities(state, "Team").get(team_id) or {}
    default = _ref_id(team.get("defaultIssueState"))
    if default:
        return _ref("WorkflowState", default)
    states = [
        s
        for s in _entities(state, "WorkflowState").values()
        if _ref_id(s.get("team")) == team_id
    ]
    for kind in ("backlog", "unstarted"):
        found = sorted(
            (s for s in states if s.get("type") == kind),
            key=lambda s: (
                s.get("position") if isinstance(s.get("position"), (int, float)) else 0
            ),
        )
        if found:
            return _ref("WorkflowState", found[0]["id"])
    return None


def _apply_state_times(
    state: dict[str, Any], issue: dict[str, Any], state_id: Any, now: str
) -> None:
    workflow_state = _entities(state, "WorkflowState").get(str(state_id)) or {}
    kind = workflow_state.get("type")
    if kind == "completed":
        issue["completedAt"] = now
    elif kind == "canceled":
        issue["canceledAt"] = now
    elif kind == "started" and not issue.get("startedAt"):
        issue["startedAt"] = now


def _apply_issue_input(
    state: dict[str, Any], issue: dict[str, Any], given: dict[str, Any], now: str
) -> None:
    for name, value in given.items():
        if name == "id":
            continue
        if name == "labelIds":
            issue["labelIds"] = [str(each) for each in value or []]
        elif name == "addedLabelIds":
            current = list(issue.get("labelIds") or [])
            issue["labelIds"] = current + [
                str(v) for v in value or [] if str(v) not in current
            ]
        elif name == "removedLabelIds":
            removed = {str(v) for v in value or []}
            issue["labelIds"] = [
                v for v in issue.get("labelIds") or [] if v not in removed
            ]
        elif name.endswith("Id") and len(name) > 2:
            related = name[:-2]
            related_type = FIELD_TYPES.get(("Issue", related))
            if related_type is None:
                issue[name] = value
            else:
                issue[related] = _ref(related_type, str(value)) if value else None
        else:
            issue[name] = copy.deepcopy(value)
    if "priority" in given:
        issue["priorityLabel"] = PRIORITY_LABELS.get(given["priority"])
    if given.get("stateId"):
        _apply_state_times(state, issue, given["stateId"], now)
    issue["updatedAt"] = now


def _payload(
    state: dict[str, Any], mutation: str, typename: str, entity_id: str
) -> tuple[str, dict[str, Any]]:
    payload_type, link = PAYLOADS[mutation]
    return payload_type, {
        "success": True,
        "lastSyncId": _sync_id(state),
        link or "entityId": _ref(typename, entity_id),
    }


def _input_of(args: dict[str, Any]) -> dict[str, Any]:
    given = args.get("input")
    return given if isinstance(given, dict) else {}


def _issue_create(walk: _Walk, args: dict[str, Any]) -> tuple[str, dict[str, Any]]:
    state = walk.state
    given = _input_of(args)
    team_id = _text(given.get("teamId"))
    if team_id is None:
        raise _FieldError("Argument Validation Error: teamId must be given.")
    entity_id = _text(given.get("id")) or _new_id(state)
    key = _team_key(state, team_id) or "ISSUE"
    number = _next_number(state, team_id, key)
    identifier = f"{key}-{number}"
    now = _now()
    viewer = state["root"].get("viewer")
    issue: dict[str, Any] = {
        "id": entity_id,
        "identifier": identifier,
        "number": number,
        "title": "",
        "description": None,
        "priority": 0,
        "priorityLabel": PRIORITY_LABELS[0],
        "estimate": None,
        "dueDate": None,
        "createdAt": now,
        "updatedAt": now,
        "archivedAt": None,
        "canceledAt": None,
        "completedAt": None,
        "startedAt": None,
        "trashed": False,
        "url": f"{_issue_url_base(state)}{identifier}",
        "branchName": identifier.lower(),
        "labelIds": [],
        "previousIdentifiers": [],
        "reactionData": [],
        "reactions": [],
        "sharedAccess": {
            "isShared": False,
            "sharedWithCount": 0,
            "viewerHasOnlySharedAccess": False,
            "disallowedIssueFields": [],
            "sharedWithUsers": [],
        },
        "inheritsSharedAccess": True,
        "customerTicketCount": 0,
        "sortOrder": 0,
        "boardOrder": 0,
        "team": _ref("Team", team_id),
        "state": None,
        "assignee": None,
        "creator": copy.deepcopy(viewer) if isinstance(viewer, dict) else None,
        "project": None,
        "parent": None,
        "cycle": None,
    }
    _apply_issue_input(state, issue, given, now)
    if issue["state"] is None:
        issue["state"] = _default_state(state, team_id)
    _entities(state, "Issue")[entity_id] = issue
    _mark(state, "created", _ref_key("Issue", entity_id))
    _mark(state, "changed", _ref_key("Issue", entity_id))
    return _payload(state, "issueCreate", "Issue", entity_id)


def _existing(walk: _Walk, typename: str, wanted: Any) -> dict[str, Any]:
    entity = _find(walk.state, typename, _text(wanted))
    if entity is None:
        if _text(wanted) and _is_gone(walk.state, typename, str(wanted)):
            raise _not_found(typename)
        raise _NotAnswerable(f"{typename} {wanted}", _ref_key(typename, str(wanted)))
    if _ref_key(typename, entity["id"]) in walk.state["deleted"]:
        raise _not_found(typename)
    return entity


def _issue_change(
    change: Callable[[dict[str, Any], dict[str, Any], str], None],
) -> Callable[[_Walk, dict[str, Any], str], tuple[str, dict[str, Any]]]:
    def run(
        walk: _Walk, args: dict[str, Any], mutation: str
    ) -> tuple[str, dict[str, Any]]:
        issue = _existing(walk, "Issue", args.get("id"))
        now = _now()
        change(issue, args, now)
        if mutation == "issueUpdate":
            _apply_issue_input(walk.state, issue, _input_of(args), now)
        issue["updatedAt"] = now
        _mark(walk.state, "changed", _ref_key("Issue", issue["id"]))
        return _payload(walk.state, mutation, "Issue", issue["id"])

    return run


def _nothing(_issue: dict[str, Any], _args: dict[str, Any], _now: str) -> None:
    return None


def _archive(issue: dict[str, Any], _args: dict[str, Any], now: str) -> None:
    issue["archivedAt"] = now


def _unarchive(issue: dict[str, Any], _args: dict[str, Any], _now: str) -> None:
    issue["archivedAt"] = None
    issue["trashed"] = False


def _trash(issue: dict[str, Any], _args: dict[str, Any], now: str) -> None:
    issue["archivedAt"] = now
    issue["trashed"] = True


def _add_label(issue: dict[str, Any], args: dict[str, Any], _now: str) -> None:
    label = str(args.get("labelId"))
    current = list(issue.get("labelIds") or [])
    issue["labelIds"] = current if label in current else [*current, label]


def _remove_label(issue: dict[str, Any], args: dict[str, Any], _now: str) -> None:
    label = str(args.get("labelId"))
    issue["labelIds"] = [v for v in issue.get("labelIds") or [] if v != label]


def _comment_create(
    walk: _Walk, args: dict[str, Any], mutation: str
) -> tuple[str, dict[str, Any]]:
    state = walk.state
    given = _input_of(args)
    issue_given = _text(given.get("issueId"))
    if issue_given is None:
        raise _FieldError("Argument Validation Error: issueId must be given.")
    issue = _find(state, "Issue", issue_given)
    issue_id = issue["id"] if issue is not None else issue_given
    entity_id = _text(given.get("id")) or _new_id(state)
    now = _now()
    viewer = state["root"].get("viewer")
    issue_url = _text((issue or {}).get("url"))
    comment: dict[str, Any] = {
        "id": entity_id,
        "body": given.get("body") or "",
        "createdAt": now,
        "updatedAt": now,
        "editedAt": None,
        "archivedAt": None,
        "resolvedAt": None,
        "reactionData": [],
        "reactions": [],
        "url": f"{issue_url}#comment-{entity_id[:8]}" if issue_url else None,
        "issue": _ref("Issue", issue_id),
        "user": copy.deepcopy(viewer) if isinstance(viewer, dict) else None,
        "parent": _ref("Comment", str(given["parentId"]))
        if given.get("parentId")
        else None,
    }
    _entities(state, "Comment")[entity_id] = comment
    _mark(state, "created", _ref_key("Comment", entity_id))
    _mark(state, "changed", _ref_key("Comment", entity_id))
    return _payload(state, mutation, "Comment", entity_id)


def _comment_update(
    walk: _Walk, args: dict[str, Any], mutation: str
) -> tuple[str, dict[str, Any]]:
    comment = _existing(walk, "Comment", args.get("id"))
    now = _now()
    for name, value in _input_of(args).items():
        if name != "id":
            comment[name] = copy.deepcopy(value)
    comment["updatedAt"] = now
    comment["editedAt"] = now
    _mark(walk.state, "changed", _ref_key("Comment", comment["id"]))
    return _payload(walk.state, mutation, "Comment", comment["id"])


def _comment_delete(
    walk: _Walk, args: dict[str, Any], _mutation: str
) -> tuple[str, dict[str, Any]]:
    comment = _existing(walk, "Comment", args.get("id"))
    ref = _ref_key("Comment", comment["id"])
    _mark(walk.state, "deleted", ref)
    _mark(walk.state, "changed", ref)
    return "DeletePayload", {
        "success": True,
        "lastSyncId": _sync_id(walk.state),
        "entityId": comment["id"],
    }


MUTATIONS: dict[
    str, Callable[[_Walk, dict[str, Any], str], tuple[str, dict[str, Any]]]
] = {
    "issueCreate": lambda walk, args, _mutation: _issue_create(walk, args),
    "issueUpdate": _issue_change(_nothing),
    "issueArchive": _issue_change(_archive),
    "issueUnarchive": _issue_change(_unarchive),
    "issueDelete": _issue_change(_trash),
    "issueAddLabel": _issue_change(_add_label),
    "issueRemoveLabel": _issue_change(_remove_label),
    "commentCreate": _comment_create,
    "commentUpdate": _comment_update,
    "commentDelete": _comment_delete,
}


def _refuse(error: Exception) -> NoReturn:
    fail_replay_item(error)
    raise error


def _mutate(walk: _Walk, field_node: Field) -> Any:
    args = arguments_of(field_node, walk.variables)
    handler = MUTATIONS.get(field_node.name)
    if handler is not None:
        payload_type, payload = handler(walk, args, field_node.name)
    elif field_node.name in ANSWERED_OK:
        payload_type = None
        payload = {"success": True, "lastSyncId": _sync_id(walk.state)}
    else:
        _refuse(
            LinearCallRefusedError(
                f"The Linear sandbox does not know the {field_node.name} mutation, "
                "so it refused the call instead of sending it to Linear. Answer it "
                "with your own sandbox in replay's sandboxes, or mock the function "
                "that makes the call."
            )
        )
    walk.state["writes"].append(
        {"mutation": field_node.name, "arguments": copy.deepcopy(args)}
    )
    return _project(walk, payload_type, payload, field_node.selections or [], True)


def _not_recorded(what: str, operation: str) -> LinearNotRecordedError:
    return LinearNotRecordedError(
        f"The Linear sandbox answers reads from the Linear calls the original "
        f"trace recorded, and the recording has nothing for {what} (asked by "
        f"{operation}), so it failed the call instead of sending it to Linear. "
        f'In mode="{READ_WHOLE_OBJECT}" it reads whole issues and other missing '
        "queries from Linear; a write it cannot place still fails. "
        'Record Linear calls on the original run with Bitfab(integrations={"linear": '
        "True}) or BITFAB_ENABLED_INTEGRATIONS=linear, or seed Linear's state for "
        "the trace in a sandbox store."
    )


def _read_entry(field_node: Field, args: dict[str, Any], found: bool) -> dict[str, Any]:
    entry: dict[str, Any] = {"field": field_node.name}
    if _text(args.get("id")):
        entry["id"] = args["id"]
    if isinstance(args.get("filter"), dict):
        entry["filter"] = args["filter"]
    return {**entry, "found": found}


Transport = Callable[[str, dict[str, Any]], "tuple[int, Any]"]

reading_linear: ContextVar[bool] = ContextVar("bitfab_reading_linear", default=False)


def urllib_transport(token: str, body: dict[str, Any]) -> tuple[int, Any]:
    request = urllib.request.Request(
        LINEAR_API_URL,
        data=json.dumps(body).encode("utf-8"),
        method="POST",
        headers={"Authorization": token, "Content-Type": "application/json"},
    )
    reading = reading_linear.set(True)
    try:
        with urllib.request.urlopen(request, timeout=TIMEOUT_SECONDS) as response:
            return response.status, _decoded(response.read())
    except urllib.error.HTTPError as error:
        return error.code, _decoded(error.read())
    finally:
        reading_linear.reset(reading)


def _decoded(raw: bytes) -> Any:
    try:
        return json.loads(raw.decode("utf-8")) if raw else {}
    except (UnicodeDecodeError, ValueError):
        return {}


def _auth_refused(status: int, body: Any) -> bool:
    if status in (401, 403):
        return True
    errors = body.get("errors") if isinstance(body, dict) else None
    return any(
        isinstance(error, dict)
        and (error.get("extensions") or {}).get("code") in AUTH_ERROR_CODES
        for error in errors or []
    )


@dataclass
class LinearLive:
    token: str | None
    transport: Transport | None = None

    def read(
        self, state: dict[str, Any], body: dict[str, Any], entry: dict[str, Any]
    ) -> Any:
        token = self.token
        if not token:
            _refuse(
                LinearCredentialError(
                    "The Linear sandbox reads from Linear in "
                    f"{READ_WHOLE_OBJECT} mode, but has no token for "
                    f"{entry.get('id') or entry.get('operation')}. Pass "
                    f"linear_sandbox(token=...), set {TOKEN_ENV}, or replay with "
                    f'sandbox_modes={{"linear": "{RECORDED}"}}.'
                )
            )
        status, answer = (self.transport or urllib_transport)(token, body)
        state["liveReads"].append({**entry, "ok": status == 200})
        if _auth_refused(status, answer):
            _refuse(
                LinearCredentialError(
                    f"Linear refused the token the Linear sandbox read with ({status}). "
                    f"Pass linear_sandbox(token=...) or set {TOKEN_ENV} to a token "
                    "that can read this workspace."
                )
            )
        return answer if isinstance(answer, dict) else {}


def _sandbox_refs(state: dict[str, Any]) -> set[str]:
    return {*state["created"], *state["changed"]}


def load_whole_issue(
    state: dict[str, Any],
    wanted: str,
    output: Any,
    source: str,
    protected: set[str] | None = None,
    skipped: set[str] | None = None,
) -> str | None:
    issue_id = _text(output.get("id")) if isinstance(output, dict) else None
    if issue_id is None or not isinstance(output, dict):
        return None
    skipped = skipped or set()
    if _ref_key(ISSUE, issue_id) in skipped:
        return None
    kept = _sandbox_refs(state) if protected is None else protected
    for exchange in output.get("exchanges") or []:
        if not isinstance(exchange, dict):
            continue
        parsed = _parsed_call(exchange.get("request"))
        response = exchange.get("response")
        data = response.get("data") if isinstance(response, dict) else None
        if parsed is None or not isinstance(data, dict):
            continue
        document, operation, variables = parsed
        walk = _Walk(state, document, variables, protected=kept, skipped=skipped)
        state["root"].update(
            _normalize_fields(walk, QUERY, data, operation.selections, QUERY)
        )
    owner = _ref_key(ISSUE, issue_id)
    for name, listed in (output.get("lists") or {}).items():
        if not isinstance(listed, dict) or not isinstance(listed.get("type"), str):
            continue
        state["wholeLists"].setdefault(owner, {})[name] = {
            "type": listed["type"],
            "ids": [
                str(each)
                for each in listed.get("ids") or []
                if _ref_key(listed["type"], str(each)) not in skipped
            ],
        }
    state["lookups"].update(
        {
            name: typename
            for name, typename in (output.get("lookups") or {}).items()
            if isinstance(name, str) and isinstance(typename, str)
        }
    )
    issue = _entities(state, ISSUE).get(issue_id) or {}
    mark_whole(
        state,
        ISSUE,
        issue_id,
        {
            "source": source,
            "identifier": issue.get("identifier"),
            "complete": output.get("complete") is not False,
        },
    )
    return issue_id


def _whole_wanted(walk: _Walk, ref: str | None) -> str | None:
    if walk.live is None or ref is None or not ref.startswith(f"{ISSUE}:"):
        return None
    wanted = ref.split(":", 1)[1]
    entity = _find(walk.state, ISSUE, wanted)
    entity_id = entity["id"] if entity is not None else wanted
    if (
        not wanted
        or is_whole(walk.state, ISSUE, entity_id)
        or _is_gone(walk.state, ISSUE, wanted)
        or _is_made(walk.state, _ref_key(ISSUE, entity_id))
    ):
        return None
    return wanted


def _read_whole(walk: _Walk, wanted: str) -> None:
    live = walk.live
    if live is None:
        return
    answer = run_reads(
        whole_issue_reads(wanted),
        lambda body: live.read(
            walk.state,
            body,
            {"whole": ISSUE, "id": wanted, "operation": body.get("operationName")},
        ),
    )
    if load_whole_issue(walk.state, wanted, answer, "live") is not None:
        return
    known = _find(walk.state, ISSUE, wanted)
    if known is None:
        _mark(walk.state, "missing", _ref_key(ISSUE, wanted))
        return
    mark_whole(walk.state, ISSUE, known["id"], {"source": "trace", "complete": False})


def _read_live(walk: _Walk, request: dict[str, Any], operation: Any) -> Any:
    live = walk.live
    if live is None:
        return None
    answer = live.read(
        walk.state,
        {
            key: request[key]
            for key in ("query", "variables", "operationName")
            if key in request
        },
        {"operation": operation.name or "an unnamed operation"},
    )
    data = answer.get("data")
    if isinstance(data, dict):
        reading = _Walk(
            walk.state,
            walk.document,
            walk.variables,
            protected=_sandbox_refs(walk.state),
        )
        walk.state["root"].update(
            _normalize_fields(reading, QUERY, data, operation.selections, QUERY)
        )
    return answer


def _answer_field(
    walk: _Walk, field_node: Field, root_type: str, is_mutation: bool
) -> Any:
    if field_node.name == "__typename":
        return root_type
    if is_mutation:
        return _mutate(walk, field_node)
    return _project(walk, QUERY, walk.state["root"], [field_node], False)[
        field_node.key
    ]


def _load_touched(walk: _Walk) -> None:
    for entity_id in sorted(walk.touched):
        wanted = _whole_wanted(walk, _ref_key(ISSUE, entity_id))
        if wanted is not None:
            _read_whole(walk, wanted)


def answer_linear_request(
    state: dict[str, Any],
    request: dict[str, Any],
    live: LinearLive | None = None,
) -> dict[str, Any]:
    query = request.get("query")
    if not isinstance(query, str):
        return {"errors": [{"message": "Must provide query string."}]}
    try:
        document = parse(query)
        operation = operation_of(document, _text(request.get("operationName")))
    except GraphQLSyntaxError as error:
        return {
            "errors": [
                {"message": str(error), "extensions": {"code": "GRAPHQL_PARSE_FAILED"}}
            ]
        }
    if operation.kind == "subscription":
        _refuse(
            LinearCallRefusedError(
                "The Linear sandbox does not answer subscriptions; it refused the "
                "call instead of sending it to Linear."
            )
        )
    variables = (
        request.get("variables") if isinstance(request.get("variables"), dict) else {}
    )
    walk = _Walk(
        state, document, variables_with_defaults(operation, variables), live=live
    )
    name = operation.name or "an unnamed operation"
    is_mutation = operation.kind == "mutation"
    data: dict[str, Any] = {}
    errors: list[dict[str, Any]] = []
    root_type = MUTATION if is_mutation else QUERY
    read_live = False
    for field_node in fields_of(
        operation.selections, document, root_type, walk.variables
    ):
        args = arguments_of(field_node, walk.variables)
        while True:
            try:
                data[field_node.key] = _answer_field(
                    walk, field_node, root_type, is_mutation
                )
                if not is_mutation:
                    state["readsFromTrace"].append(_read_entry(field_node, args, True))
                break
            except _FieldError as error:
                errors.append(error.as_error([field_node.key]))
                data[field_node.key] = None
                break
            except _NotAnswerable as missing:
                wanted = _whole_wanted(walk, missing.ref)
                if wanted is not None:
                    _read_whole(walk, wanted)
                    continue
                if live is not None and not is_mutation and not read_live:
                    read_live = True
                    answer = _read_live(walk, request, operation)
                    if not isinstance(answer.get("data"), dict):
                        return answer
                    continue
                if not is_mutation:
                    state["readsFromTrace"].append(_read_entry(field_node, args, False))
                _refuse(_not_recorded(str(missing), name))
    _load_touched(walk)
    if errors:
        return {"data": None, "errors": errors}
    return {"data": data}


def _parsed_call(params: Any) -> tuple[Document, Any, dict[str, Any]] | None:
    if not isinstance(params, dict) or not isinstance(params.get("query"), str):
        return None
    try:
        document = parse(params["query"])
        operation = operation_of(document, _text(params.get("operationName")))
    except GraphQLSyntaxError:
        return None
    variables = (
        params.get("variables") if isinstance(params.get("variables"), dict) else {}
    )
    return document, operation, variables_with_defaults(operation, variables)


def issue_ids_read(params: Any, output: Any) -> list[str]:
    parsed = _parsed_call(params)
    data = output.get("data") if isinstance(output, dict) else None
    if parsed is None or parsed[1].kind == "mutation" or not isinstance(data, dict):
        return []
    document, operation, variables = parsed
    scratch = _empty_state()
    walk = _Walk(scratch, document, variables)
    _normalize_fields(walk, QUERY, data, operation.selections, QUERY)
    return list(_entities(scratch, ISSUE))


def issue_ids_written(params: Any) -> list[str]:
    parsed = _parsed_call(params)
    if parsed is None or parsed[1].kind != "mutation":
        return []
    document, operation, variables = parsed
    found: list[str] = []
    for field_node in fields_of(operation.selections, document, MUTATION, variables):
        args = arguments_of(field_node, variables)
        given = (
            _text(args.get("id"))
            if CHANGED_BY.get(field_node.name) == ISSUE
            else _text(_input_of(args).get("issueId"))
            if field_node.name == "commentCreate"
            else None
        )
        if given is not None and given not in found:
            found.append(given)
    return found


def issue_ids_created(params: Any, output: Any) -> list[str]:
    parsed = _parsed_call(params)
    if parsed is None or parsed[1].kind != "mutation":
        return []
    created = _payload_ids(*parsed, output)[0]
    return [ref.split(":", 1)[1] for ref in created if ref.startswith(f"{ISSUE}:")]


def operation_span_name(params: dict[str, Any]) -> str:
    """The span name a Linear request is recorded under: ``linear.query.<name>`` or ``linear.mutation.<name>``."""
    parsed = _parsed_call(params)
    if parsed is None:
        return f"{QUERY_SPAN_PREFIX}request"
    document, operation, variables = parsed
    kind = "mutation" if operation.kind == "mutation" else "query"
    named = operation.name or "_".join(
        f.name for f in fields_of(operation.selections, document, None, variables)
    )
    return f"{LINEAR_SPAN_PREFIX}{kind}.{named or 'request'}"


def _payload_ids(
    document: Document, operation: Any, variables: dict[str, Any], output: Any
) -> tuple[set[str], set[str]]:
    data = output.get("data") if isinstance(output, dict) else None
    created: set[str] = set()
    changed: set[str] = set()
    for field_node in fields_of(operation.selections, document, MUTATION, variables):
        payload = data.get(field_node.key) if isinstance(data, dict) else None
        link = PAYLOADS.get(field_node.name, (None, None))[1]
        entity_id = (
            _ref_id(payload.get(link)) if isinstance(payload, dict) and link else None
        )
        if field_node.name in CREATED_BY and entity_id:
            created.add(_ref_key(CREATED_BY[field_node.name], entity_id))
        if field_node.name in CHANGED_BY:
            typename = CHANGED_BY[field_node.name]
            given = _text(arguments_of(field_node, variables).get("id"))
            for each in (given, entity_id):
                if each:
                    changed.add(_ref_key(typename, each))
    return created, changed


@dataclass
class LinearRecording:
    state: dict[str, Any] = field(default_factory=_empty_state)
    changed: set[str] = field(default_factory=set)
    created: set[str] = field(default_factory=set)


def record_call(recording: LinearRecording, params: Any, output: Any) -> None:
    parsed = _parsed_call(params)
    if parsed is None:
        return
    document, operation, variables = parsed
    if operation.kind == "mutation":
        created, changed = _payload_ids(document, operation, variables, output)
        recording.created |= created
        recording.changed |= changed
        return
    data = output.get("data") if isinstance(output, dict) else None
    if not isinstance(data, dict):
        return
    walk = _Walk(
        recording.state, document, variables, recording.changed, recording.created
    )
    recording.state["root"].update(
        _normalize_fields(walk, QUERY, data, operation.selections, QUERY)
    )


def record_whole_issue(recording: LinearRecording, issue_id: str, output: Any) -> None:
    load_whole_issue(
        recording.state,
        issue_id,
        output,
        "trace",
        recording.changed,
        recording.created,
    )


def _seed_value(state: dict[str, Any], hint: str | None, value: Any) -> Any:
    if isinstance(value, list):
        return [_seed_value(state, hint, item) for item in value]
    if not isinstance(value, dict):
        return copy.deepcopy(value)
    typename = _text(value.get("__typename")) or hint
    if typename is not None and _text(value.get("id")) is not None:
        _seed_entity(state, typename, value)
        return _ref(typename, value["id"])
    return {name: _seed_value(state, None, item) for name, item in value.items()}


def _seed_entity(state: dict[str, Any], typename: str, value: dict[str, Any]) -> None:
    entity_id = str(value["id"])
    fields: dict[str, Any] = {}
    for name, item in value.items():
        if name == "__typename":
            continue
        info = CONNECTIONS.get((typename, name))
        nodes = item.get("nodes") if isinstance(item, dict) else item
        if info is not None and isinstance(nodes, list):
            ids = []
            for node in nodes:
                if isinstance(node, dict) and _text(node.get("id")):
                    node = dict(node)
                    if info[1] == "back":
                        node.setdefault(info[2] or "", _ref(typename, entity_id))
                    _seed_entity(state, info[0], node)
                    ids.append(str(node["id"]))
            if info[1] == "ids":
                fields[info[2] or ""] = ids
            continue
        fields[name] = _seed_value(state, FIELD_TYPES.get((typename, name)), item)
    entities = _entities(state, typename)
    entities[entity_id] = {**entities.get(entity_id, {}), **fields, "id": entity_id}


def _loaded_state(value: Any, mode: str) -> dict[str, Any]:
    given = value if isinstance(value, dict) else {}
    stored = given.get("mode") or mode
    if stored not in LINEAR_MODES:
        raise LinearModeError(
            f'The state saved for Linear is a workspace from mode="{stored}", '
            f"which the Linear sandbox does not have. Its modes are "
            f"{', '.join(repr(m) for m in LINEAR_MODES)}. Seed Linear's state for "
            "the trace again."
        )
    state = _empty_state(mode)
    for key in STATE_KEYS:
        if key in given and isinstance(given[key], type(state[key])):
            state[key] = copy.deepcopy(given[key])
    for key, typename in SEED_KEYS.items():
        for item in given.get(key) or []:
            if isinstance(item, dict) and _text(item.get("id")):
                _seed_entity(state, typename, item)
                if typename == ISSUE:
                    mark_whole(state, ISSUE, str(item["id"]), {"source": "seed"})
    viewer = given.get("viewer")
    if isinstance(viewer, dict) and _text(viewer.get("id")):
        _seed_entity(state, "User", viewer)
        state["root"]["viewer"] = _ref("User", viewer["id"])
    return state


def load_linear_state(ctx: SandboxStartCtx, value: Any) -> dict[str, Any]:
    """Builds the Linear sandbox's state from a sandbox store entry or ``start``'s return.

    Takes the state a replay saved, or a seed such as
    ``{"viewer": {...}, "teams": [...], "workflowStates": [...], "issues": [...],
    "comments": [...], "users": [...], "projects": [...], "issueLabels": [...]}``,
    each a list of objects shaped as Linear's GraphQL API returns them. A
    nested object with an ``id``, such as an issue's ``team`` or ``state``,
    links to that entity, and an issue's ``comments`` (a list, or
    ``{"nodes": [...]}``) become its comments. Each seeded issue counts as
    whole, so no read of it goes to Linear.
    """
    given = value if isinstance(value, dict) else {}
    return _loaded_state(given, _text(given.get("mode")) or RECORDED)


@dataclass(frozen=True)
class LinearCallAccess:
    token: str | None = None


def is_linear_call(node: SpanNodeMeta) -> bool:
    call = service_calls.current_call()
    return (
        call is not None
        and call.integration == LINEAR_INTEGRATION
        and node.trace_function_key.startswith(LINEAR_SPAN_PREFIX)
    )


def is_linear_write(call: MockOverrideCtx) -> bool:
    return call.node.trace_function_key.startswith(MUTATION_SPAN_PREFIX)


def linear_accessed_object(call: MockOverrideCtx) -> str | None:
    parsed = _parsed_call(dict(call.kwargs))
    if parsed is None:
        return None
    document, operation, variables = parsed
    root = MUTATION if operation.kind == "mutation" else QUERY
    for field_node in fields_of(operation.selections, document, root, variables):
        if field_node.name == "__typename":
            continue
        args = arguments_of(field_node, variables)
        given = _text(args.get("id")) or _text(_input_of(args).get("issueId"))
        return f"{field_node.name}/{given}" if given else field_node.name
    return None


def _call_token() -> str | None:
    held = service_calls.current_call()
    access = held.request if held is not None else None
    return access.token if isinstance(access, LinearCallAccess) else None


def build_linear_sandbox(
    start: Callable[[SandboxStartCtx], Any] | None = None,
    mode: str = READ_WHOLE_OBJECT,
    token: str | None = None,
    transport: Transport | None = None,
) -> Sandbox:
    def handle(state: dict[str, Any], call: MockOverrideCtx) -> dict[str, Any]:
        live = (
            LinearLive(
                token or _text(os.environ.get(TOKEN_ENV)) or _call_token(), transport
            )
            if mode == READ_WHOLE_OBJECT
            else None
        )
        return answer_linear_request(state, dict(call.kwargs), live)

    return Sandbox(
        name=LINEAR_SANDBOX_NAME,
        match=is_linear_call,
        handle=handle,
        start=(
            (lambda _ctx: _empty_state(mode))
            if start is None
            else lambda ctx: _loaded_state(start(ctx), mode)
        ),
        integration=LINEAR_INTEGRATION,
        mode=mode,
        load=lambda _ctx, value: _loaded_state(value, mode),
        is_write=is_linear_write,
        accessed_object=linear_accessed_object,
    )
