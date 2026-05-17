"""Single source of truth for wire-format strings and limits.

Every constant here corresponds to a value that crosses a module boundary
or appears in serialized JSON / HTTP headers / gRPC metadata.  If a string
is used in only one place, it doesn't belong here.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Literal

# ---------------------------------------------------------------------------
# Collection scopes — stored in Mongo docs as filter keys
# ---------------------------------------------------------------------------

SCOPE_APP: Literal["app"] = "app"
SCOPE_USER: Literal["user"] = "user"
SCOPE_OWNER: Literal["owner"] = "owner"
SCOPE_SESSION: Literal["session"] = "session"

CollectionScope = Literal["app", "user", "owner", "session"]

VALID_SCOPES: frozenset[str] = frozenset({SCOPE_APP, SCOPE_USER, SCOPE_OWNER, SCOPE_SESSION})

SCOPE_FIELD_USER = "_user_id"
SCOPE_FIELD_OWNER = "_team_id"
SCOPE_FIELD_SESSION = "_session_id"

# ---------------------------------------------------------------------------
# Access control levels — pages, data sources, endpoints
# ---------------------------------------------------------------------------

ACCESS_PUBLIC: Literal["public"] = "public"
ACCESS_AUTHENTICATED: Literal["authenticated"] = "authenticated"

AccessLevel = Literal["public", "authenticated"]

# ---------------------------------------------------------------------------
# HTTP headers injected by the Go gateway → runner
# ---------------------------------------------------------------------------

HEADER_AUTHENTICATED = "X-Capsule-Authenticated"
HEADER_EMAIL = "X-Capsule-Email"
HEADER_USER_ID = "X-Capsule-User-Id"
HEADER_ORG_ID = "X-Capsule-Org-Id"
HEADER_SESSION_ID = "X-Capsule-Session-Id"

# ---------------------------------------------------------------------------
# Collection query defaults
# ---------------------------------------------------------------------------

DEFAULT_PAGE_SIZE = 50
MAX_PAGE_SIZE = 200

# ---------------------------------------------------------------------------
# Pricing types — stored on apps, sent in DeployRequest
# ---------------------------------------------------------------------------

PRICING_ONE_TIME: Literal["one_time"] = "one_time"
PRICING_MONTHLY: Literal["monthly"] = "monthly"

PricingType = Literal["one_time", "monthly"]

# ---------------------------------------------------------------------------
# Page types
# ---------------------------------------------------------------------------

PAGE_TYPE_REACT: Literal["react"] = "react"
PAGE_TYPE_DSL: Literal["dsl"] = "dsl"

# ---------------------------------------------------------------------------
# Workflow types
# ---------------------------------------------------------------------------

WorkflowScope = Literal["user", "owner", "app"]

VALID_WORKFLOW_SCOPES: frozenset[str] = frozenset({SCOPE_USER, SCOPE_OWNER, SCOPE_APP})

# ---------------------------------------------------------------------------
# Session defaults
# ---------------------------------------------------------------------------

DEFAULT_CHANNEL_TYPE = "chat"
DEFAULT_TOKEN_TYPE = "Bearer"

HISTORY_FETCH_COUNT = 50

# ---------------------------------------------------------------------------
# Collection declaration — typed struct instead of dict[str, Any]
# ---------------------------------------------------------------------------


ColumnType = Literal[
    "text",
    "number",
    "currency",
    "date",
    "link",
    "file",
    "email",
    "status",
    "tags",
    "boolean",
    "score",
]


@dataclass(frozen=True, slots=True)
class Column:
    """Typed column definition for collection declarations.

    Can be used in place of a plain string in ``app.collection(columns=[...])``.

    Example::

        app.collection("venues", columns=[
            Column("name"),
            Column("status", type="status"),
            Column("revenue", type="currency", format="$"),
            Column("website", type="link"),
        ])
    """

    key: str
    type: ColumnType = "text"
    label: str | None = None
    format: str | None = None

    def to_dict(self) -> dict:
        d: dict[str, Any] = {"key": self.key, "type": self.type}
        if self.label is not None:
            d["label"] = self.label
        if self.format is not None:
            d["format"] = self.format
        return d

    @classmethod
    def from_dict(cls, d: dict | str) -> Column:
        if isinstance(d, str):
            return cls(key=d)
        return cls(
            key=d["key"],
            type=d.get("type", "text"),
            label=d.get("label"),
            format=d.get("format"),
        )


def _normalize_columns(
    cols: tuple[str | Column, ...] | None,
) -> tuple[Column, ...] | None:
    if cols is None:
        return None
    return tuple(Column(key=c) if isinstance(c, str) else c for c in cols)


@dataclass(frozen=True, slots=True)
class CollectionDecl:
    """Immutable declaration of a named collection (scope, columns, UI hints)."""

    name: str
    scope: CollectionScope = SCOPE_APP
    columns: tuple[Column, ...] | None = None
    sortable: bool = False
    filterable: bool = False
    paginate: int = 0

    def column_keys(self) -> list[str] | None:
        if self.columns is None:
            return None
        return [c.key for c in self.columns]

    def to_dict(self) -> dict:
        cols: list | None = None
        if self.columns:
            has_types = any(c.type != "text" or c.label or c.format for c in self.columns)
            cols = (
                [c.to_dict() for c in self.columns] if has_types else [c.key for c in self.columns]
            )
        return {
            "name": self.name,
            "columns": cols,
            "scope": self.scope,
            "sortable": self.sortable,
            "filterable": self.filterable,
            "paginate": self.paginate,
        }

    @classmethod
    def from_dict(cls, d: dict) -> CollectionDecl:
        raw_cols = d.get("columns")
        cols: tuple[Column, ...] | None = None
        if raw_cols:
            cols = tuple(Column.from_dict(c) for c in raw_cols)
        return cls(
            name=d["name"],
            scope=d.get("scope", SCOPE_APP),
            columns=cols,
            sortable=d.get("sortable", False),
            filterable=d.get("filterable", False),
            paginate=d.get("paginate", 0),
        )

    def scope_filter(self, *, user_id: str, owner_id: str = "", session_id: str) -> dict[str, str]:
        if self.scope == SCOPE_USER:
            return {SCOPE_FIELD_USER: user_id}
        if self.scope == SCOPE_OWNER:
            return {SCOPE_FIELD_OWNER: owner_id or user_id}
        if self.scope == SCOPE_SESSION:
            return {SCOPE_FIELD_SESSION: session_id}
        return {}


# ---------------------------------------------------------------------------
# Setting declaration — scoped key-value configuration for apps
# ---------------------------------------------------------------------------

SettingScope = Literal["app", "owner", "user"]

VALID_SETTING_SCOPES: frozenset[str] = frozenset({SCOPE_APP, SCOPE_OWNER, SCOPE_USER})

_TYPE_TO_STR: dict[type, str] = {bool: "bool", str: "str", int: "int", float: "float"}
_STR_TO_TYPE: dict[str, type] = {v: k for k, v in _TYPE_TO_STR.items()}

SETTINGS_COLLECTION = "_settings"
SETTINGS_KEY_FIELD = "_setting"

KV_COLLECTION = "_kv"
KV_KEY_FIELD = "_key"


@dataclass(frozen=True, slots=True)
class SettingDecl:
    """Immutable declaration of a named app setting."""

    name: str
    scope: SettingScope = SCOPE_APP
    type: type = str
    default: Any = None
    options: tuple[str, ...] | None = None
    label: str | None = None

    def to_dict(self) -> dict:
        d: dict[str, Any] = {
            "name": self.name,
            "scope": self.scope,
            "type": _TYPE_TO_STR.get(self.type, "str"),
            "default": self.default,
        }
        if self.options:
            d["options"] = list(self.options)
        if self.label:
            d["label"] = self.label
        return d

    def scope_filter(self, *, user_id: str, owner_id: str = "") -> dict[str, str]:
        if self.scope == SCOPE_USER:
            return {SCOPE_FIELD_USER: user_id}
        if self.scope == SCOPE_OWNER:
            return {SCOPE_FIELD_OWNER: owner_id or user_id}
        return {}
