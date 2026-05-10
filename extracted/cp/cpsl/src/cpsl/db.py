"""Document collection interface.

``CollectionRef`` is the primary public API — returned by ``app.collection()``
and used directly for CRUD.  Plain dict updates are treated as field patches
(auto-wrapped in ``$set``); explicit Mongo operator docs pass through unchanged.

``DatabaseProxy`` and ``ScopedDatabaseProxy`` back ``self.db`` and
``session.db`` respectively.
"""

from __future__ import annotations

import asyncio
import contextvars
import json
import re
from typing import TYPE_CHECKING

from .constants import (
    Column,
    CollectionDecl,
    CollectionScope,
    SCOPE_APP,
    SCOPE_SESSION,
    SCOPE_OWNER,
    SCOPE_USER,
    SCOPE_FIELD_SESSION,
    SCOPE_FIELD_OWNER,
    SCOPE_FIELD_USER,
    VALID_SCOPES,
)

if TYPE_CHECKING:
    from .clients.capsule import DataServiceStub


VALID_COLUMN_TYPES = {
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
}


_active_identity: contextvars.ContextVar[object | None] = contextvars.ContextVar(
    "_cpsl_active_identity", default=None
)


def set_active_identity(identity: object | None) -> contextvars.Token:
    return _active_identity.set(identity)


def reset_active_identity(token: contextvars.Token) -> None:
    _active_identity.reset(token)


def get_active_identity() -> object | None:
    return _active_identity.get()


def _normalize_update(update: dict) -> dict:
    """Normalize an update document for MongoDB.

    Plain field dicts are wrapped in ``$set`` so callers can write::

        await col.update_one({"_id": lid}, {"status": "sent"})

    instead of the raw Mongo form::

        await col.update_one({"_id": lid}, {"$set": {"status": "sent"}})

    Explicit operator docs (all keys start with ``$``) pass through unchanged.
    Mixed operator/plain keys and empty updates raise ``ValueError``.
    """
    if not update:
        raise ValueError("update document must not be empty")

    has_ops = any(k.startswith("$") for k in update)
    has_plain = any(not k.startswith("$") for k in update)

    if has_ops and has_plain:
        raise ValueError(
            "update document mixes operator keys (e.g. $set) with plain field "
            "keys — use either plain fields for a patch or raw operator syntax, "
            "not both"
        )

    if has_plain:
        return {"$set": update}
    return update


def _with_id_alias(doc: dict) -> dict:
    """Expose ``id`` as a convenience alias for ``_id`` on result docs."""
    if "_id" in doc and "id" not in doc:
        doc["id"] = _normalize_id(doc["_id"])
    return doc


LOOKUP_OPS = {
    "ne": "$ne",
    "gt": "$gt",
    "gte": "$gte",
    "lt": "$lt",
    "lte": "$lte",
    "in": "$in",
    "nin": "$nin",
}


def _mongo_field(field: str) -> str:
    return "_id" if field == "id" else field


def _normalize_id(value):
    if isinstance(value, dict) and "$oid" in value:
        return value["$oid"]
    return value


def _normalize_lookup_value(field: str, value):
    if field != "_id":
        return value
    if isinstance(value, (list, tuple)):
        return [_normalize_id(v) for v in value]
    return _normalize_id(value)


def _regex_lookup(value: object, *, prefix: str = "", suffix: str = "") -> dict:
    return {"$regex": prefix + re.escape(str(value)) + suffix, "$options": "i"}


def compile_lookups(lookups: dict) -> dict:
    """Compile Django-style keyword lookups to a Mongo filter document."""
    compiled: dict = {}
    for raw_key, value in lookups.items():
        if raw_key.startswith("_"):
            continue
        parts = raw_key.split("__")
        field = _mongo_field(parts[0])
        op = parts[1] if len(parts) > 1 else "exact"
        if len(parts) > 2:
            raise ValueError(f"invalid lookup {raw_key!r}")

        value = _normalize_lookup_value(field, value)
        if op == "exact":
            compiled[field] = value
        elif op in LOOKUP_OPS:
            compiled.setdefault(field, {})[LOOKUP_OPS[op]] = value
        elif op == "contains":
            compiled.setdefault(field, {}).update(_regex_lookup(value))
        elif op == "startswith":
            compiled.setdefault(field, {}).update(_regex_lookup(value, prefix="^"))
        elif op == "endswith":
            compiled.setdefault(field, {}).update(_regex_lookup(value, suffix="$"))
        else:
            raise ValueError(f"unsupported lookup operator {op!r}")
    return compiled


def _row_id(row_or_id) -> object:
    if isinstance(row_or_id, dict):
        return _normalize_id(row_or_id.get("_id") or row_or_id.get("id"))
    return _normalize_id(row_or_id)


def _ids_filter(rows_or_ids) -> dict:
    if isinstance(rows_or_ids, (str, bytes)) or not hasattr(rows_or_ids, "__iter__"):
        rows_or_ids = [rows_or_ids]
    ids = [_row_id(v) for v in rows_or_ids]
    ids = [v for v in ids if v]
    if not ids:
        raise ValueError("delete_rows requires at least one row id")
    return {"_id": {"$in": ids}}


def _scope_filter(
    scope: str, *, user_id: str = "", owner_id: str = "", session_id: str = ""
) -> dict[str, str]:
    if scope == SCOPE_APP:
        return {}
    if scope == SCOPE_USER:
        if not user_id:
            raise ValueError("scope='user' requires user_id")
        return {SCOPE_FIELD_USER: user_id}
    if scope == SCOPE_OWNER:
        owner = owner_id or user_id
        if not owner:
            raise ValueError("scope='owner' requires owner_id or user_id")
        return {SCOPE_FIELD_OWNER: owner}
    if scope == SCOPE_SESSION:
        if not session_id:
            raise ValueError("scope='session' requires session_id")
        return {SCOPE_FIELD_SESSION: session_id}
    raise ValueError(f"scope must be one of {VALID_SCOPES}, got {scope!r}")


def _normalize_column(column: str | Column | dict) -> Column:
    if isinstance(column, Column):
        col = column
    elif isinstance(column, str):
        col = Column(key=column)
    elif isinstance(column, dict):
        col = Column.from_dict(column)
    else:
        raise TypeError("columns must be strings, Column objects, or column dictionaries")

    if not col.key or col.key.startswith("$") or "." in col.key or "\x00" in col.key:
        raise ValueError(f"invalid column key {col.key!r}")
    if col.type not in VALID_COLUMN_TYPES:
        raise ValueError(f"invalid column type {col.type!r}")
    return col


def _normalize_dynamic_columns(
    columns: list[str | Column | dict] | tuple[str | Column | dict, ...],
) -> list[Column]:
    normalized: list[Column] = []
    seen: set[str] = set()
    for raw in columns:
        col = _normalize_column(raw)
        if col.key in seen:
            raise ValueError(f"duplicate column key {col.key!r}")
        seen.add(col.key)
        normalized.append(col)
    return normalized


class CollectionRow(dict):
    """Dict-compatible row with Django-style persistence helpers."""

    def __init__(self, data: dict, collection) -> None:
        super().__init__(_with_id_alias(data))
        self._collection = collection

    @property
    def id(self):
        return self.get("id") or self.get("_id")

    async def delete(self) -> dict:
        if not self.id:
            raise ValueError("row has no id")
        return await self._collection.delete_rows([self.id])

    async def update(self, patch: dict) -> dict:
        if not self.id:
            raise ValueError("row has no id")
        result = await self._collection.update_one({"_id": self.id}, patch)
        dict.update(self, patch)
        return result


class CollectionQuery:
    """Lazy Django-style query object for a collection."""

    def __init__(
        self,
        collection,
        filter_doc: dict | None = None,
        *,
        limit_value: int = 0,
        skip_value: int = 0,
        sort_doc: dict | None = None,
    ) -> None:
        self._collection = collection
        self._filter = filter_doc or {}
        self._limit = limit_value
        self._skip = skip_value
        self._sort = sort_doc

    def __await__(self):
        return self.all().__await__()

    def filter(self, **lookups) -> "CollectionQuery":
        merged = dict(self._filter)
        merged.update(compile_lookups(lookups))
        return CollectionQuery(
            self._collection,
            merged,
            limit_value=self._limit,
            skip_value=self._skip,
            sort_doc=self._sort,
        )

    def limit(self, n: int) -> "CollectionQuery":
        return CollectionQuery(
            self._collection,
            self._filter,
            limit_value=int(n),
            skip_value=self._skip,
            sort_doc=self._sort,
        )

    def offset(self, n: int) -> "CollectionQuery":
        return CollectionQuery(
            self._collection,
            self._filter,
            limit_value=self._limit,
            skip_value=int(n),
            sort_doc=self._sort,
        )

    def order_by(self, *fields: str) -> "CollectionQuery":
        sort = {}
        for field in fields:
            if field.startswith("-"):
                sort[_mongo_field(field[1:])] = -1
            else:
                sort[_mongo_field(field)] = 1
        return CollectionQuery(
            self._collection,
            self._filter,
            limit_value=self._limit,
            skip_value=self._skip,
            sort_doc=sort or None,
        )

    async def all(self) -> list[CollectionRow]:
        return await self._collection.raw_filter(
            self._filter,
            limit=self._limit,
            skip=self._skip,
            sort=self._sort,
        )

    async def first(self) -> CollectionRow | None:
        rows = await self.limit(1).all()
        return rows[0] if rows else None

    async def one(self) -> CollectionRow:
        rows = await self.limit(2).all()
        if len(rows) != 1:
            raise ValueError(f"expected exactly one row, got {len(rows)}")
        return rows[0]

    async def delete(self) -> dict:
        return await self._collection.delete_many(self._filter)


class Collection:
    """Proxy for a single document collection."""

    __slots__ = ("_stub", "_app_id", "_name")

    def __init__(self, stub: DataServiceStub, app_id: str, name: str) -> None:
        self._stub = stub
        self._app_id = app_id
        self._name = name

    async def insert_one(self, document: dict) -> dict:
        from .clients.capsule import InsertOneRequest

        doc_json = json.dumps(document).encode()
        resp = await asyncio.get_running_loop().run_in_executor(
            None,
            self._stub.insert_one,
            InsertOneRequest(app_id=self._app_id, collection=self._name, document_json=doc_json),
        )
        result = dict(document)
        result["_id"] = resp.id
        return CollectionRow(result, self)

    async def insert_many(self, documents: list[dict]) -> list[dict]:
        from .clients.capsule import InsertManyRequest

        docs_json = [json.dumps(d).encode() for d in documents]
        resp = await asyncio.get_running_loop().run_in_executor(
            None,
            self._stub.insert_many,
            InsertManyRequest(app_id=self._app_id, collection=self._name, documents_json=docs_json),
        )
        results = []
        for doc, id_ in zip(documents, resp.ids):
            r = dict(doc)
            r["_id"] = id_
            results.append(CollectionRow(r, self))
        return results

    async def raw_get(self, filter: dict | None = None) -> CollectionRow | None:
        from .clients.capsule import FindOneRequest

        filter_json = json.dumps(filter or {}).encode()
        resp = await asyncio.get_running_loop().run_in_executor(
            None,
            self._stub.find_one,
            FindOneRequest(app_id=self._app_id, collection=self._name, filter_json=filter_json),
        )
        if not resp.document_json:
            return None
        return CollectionRow(json.loads(resp.document_json), self)

    async def raw_filter(
        self, filter: dict | None = None, limit: int = 0, skip: int = 0, sort: dict | None = None
    ) -> list[CollectionRow]:
        from .clients.capsule import FindRequest

        filter_json = json.dumps(filter or {}).encode()
        sort_json = json.dumps(sort or {}).encode() if sort else b""
        resp = await asyncio.get_running_loop().run_in_executor(
            None,
            self._stub.find,
            FindRequest(
                app_id=self._app_id,
                collection=self._name,
                filter_json=filter_json,
                limit=limit,
                skip=skip,
                sort_json=sort_json,
            ),
        )
        return [CollectionRow(json.loads(d), self) for d in resp.documents_json]

    async def find_one(self, filter: dict | None = None) -> CollectionRow | None:
        return await self.raw_get(filter)

    async def find(
        self, filter: dict | None = None, limit: int = 0, skip: int = 0, sort: dict | None = None
    ) -> list[CollectionRow]:
        return await self.raw_filter(filter=filter, limit=limit, skip=skip, sort=sort)

    def all(self) -> CollectionQuery:
        return CollectionQuery(self)

    def filter(self, **lookups) -> CollectionQuery:
        return CollectionQuery(self, compile_lookups(lookups))

    async def get(self, **lookups) -> CollectionRow | None:
        return await self.filter(**lookups).first()

    async def update_one(self, filter: dict, update: dict, *, upsert: bool = False) -> dict:
        """Patch fields on a single document.

        Plain field dicts are treated as patches::

            await col.update_one({"_id": lid}, {"status": "sent"})

        Explicit operator docs (``$set``, ``$inc``, etc.) pass through::

            await col.update_one({"_id": lid}, {"$set": {"status": "sent"}})
        """
        from .clients.capsule import UpdateOneRequest

        normalized = _normalize_update(update)
        filter_json = json.dumps(filter).encode()
        update_json = json.dumps(normalized).encode()
        resp = await asyncio.get_running_loop().run_in_executor(
            None,
            self._stub.update_one,
            UpdateOneRequest(
                app_id=self._app_id,
                collection=self._name,
                filter_json=filter_json,
                update_json=update_json,
                upsert=upsert,
            ),
        )
        return {"matched": resp.matched, "modified": resp.modified}

    async def delete_one(self, filter: dict) -> dict:
        from .clients.capsule import DeleteOneRequest

        filter_json = json.dumps(filter).encode()
        resp = await asyncio.get_running_loop().run_in_executor(
            None,
            self._stub.delete_one,
            DeleteOneRequest(app_id=self._app_id, collection=self._name, filter_json=filter_json),
        )
        return {"deleted": resp.deleted}

    async def delete_many(self, filter: dict) -> dict:
        from .clients.capsule import DeleteManyRequest

        filter_json = json.dumps(filter).encode()
        resp = await asyncio.get_running_loop().run_in_executor(
            None,
            self._stub.delete_many,
            DeleteManyRequest(app_id=self._app_id, collection=self._name, filter_json=filter_json),
        )
        return {"deleted": resp.deleted}

    async def delete_rows(self, rows_or_ids) -> dict:
        return await self.delete_many(_ids_filter(rows_or_ids))

    async def count(self, filter: dict | None = None) -> int:
        from .clients.capsule import CountRequest

        filter_json = json.dumps(filter or {}).encode()
        resp = await asyncio.get_running_loop().run_in_executor(
            None,
            self._stub.count,
            CountRequest(app_id=self._app_id, collection=self._name, filter_json=filter_json),
        )
        return resp.count


class DynamicCollection:
    """Schema-aware collection handle for runtime-created collections."""

    def __init__(
        self,
        stub: DataServiceStub,
        app_id: str,
        name: str,
        scope: CollectionScope,
        *,
        user_id: str = "",
        owner_id: str = "",
        session_id: str = "",
    ) -> None:
        self.name = name
        self.scope = scope
        self._stub = stub
        self._app_id = app_id
        self._user_id = user_id
        self._owner_id = owner_id
        self._session_id = session_id
        inner = Collection(stub, app_id, name)
        self._collection: Collection | ScopedCollection
        if scope == SCOPE_APP:
            self._collection = inner
        else:
            self._collection = ScopedCollection(
                inner,
                _scope_filter(
                    scope,
                    user_id=user_id,
                    owner_id=owner_id,
                    session_id=session_id,
                ),
            )

    def _schema_kwargs(self) -> dict:
        return {
            "app_id": self._app_id,
            "name": self.name,
            "scope": self.scope,
            "user_id": self._user_id,
            "owner_id": self._owner_id,
            "session_id": self._session_id,
        }

    @staticmethod
    def _proto_columns(columns: list[Column]):
        from .clients.capsule import CollectionColumnSpec

        return [
            CollectionColumnSpec(
                key=col.key,
                type=col.type,
                label=col.label or "",
                format=col.format or "",
            )
            for col in columns
        ]

    @staticmethod
    def _columns_from_schema(schema) -> list[Column]:
        return [
            Column(
                key=col.key,
                type=col.type or "text",
                label=col.label or None,
                format=col.format or None,
            )
            for col in schema.columns
        ]

    async def list_columns(self) -> list[Column]:
        from .clients.capsule import GetCollectionSchemaRequest

        resp = await asyncio.get_running_loop().run_in_executor(
            None,
            self._stub.get_collection_schema,
            GetCollectionSchemaRequest(**self._schema_kwargs()),
        )
        if not resp.found or resp.schema is None:
            return []
        return self._columns_from_schema(resp.schema)

    async def set_columns(self, columns: list[str | Column | dict]) -> list[Column]:
        from .clients.capsule import CollectionSchema, UpsertCollectionSchemaRequest

        normalized = _normalize_dynamic_columns(columns)
        schema = CollectionSchema(
            name=self.name,
            scope=self.scope,
            columns=self._proto_columns(normalized),
            user_id=self._user_id,
            owner_id=self._owner_id,
            session_id=self._session_id,
        )
        resp = await asyncio.get_running_loop().run_in_executor(
            None,
            self._stub.upsert_collection_schema,
            UpsertCollectionSchemaRequest(app_id=self._app_id, schema=schema),
        )
        return self._columns_from_schema(resp.schema)

    async def add_column(
        self,
        key: str,
        *,
        type: str = "text",
        label: str | None = None,
        format: str | None = None,
        default=None,
        backfill: bool = False,
    ) -> list[Column]:
        if backfill or default is not None:
            raise NotImplementedError(
                "column backfill is not supported yet; update rows explicitly"
            )
        columns = await self.list_columns()
        if any(col.key == key for col in columns):
            raise ValueError(f"column {key!r} already exists")
        return await self.set_columns(
            [*columns, Column(key=key, type=type, label=label, format=format)]
        )

    async def remove_column(self, key: str, *, drop_values: bool = False) -> list[Column]:
        if drop_values:
            raise NotImplementedError("dropping stored column values is not supported yet")
        columns = [col for col in await self.list_columns() if col.key != key]
        return await self.set_columns(columns)

    async def rename_column(
        self,
        old_key: str,
        new_key: str,
        *,
        migrate_values: bool = False,
    ) -> list[Column]:
        if migrate_values:
            raise NotImplementedError("stored value migration is not supported yet")
        columns = await self.list_columns()
        renamed: list[Column] = []
        found = False
        for col in columns:
            if col.key == old_key:
                renamed.append(
                    Column(key=new_key, type=col.type, label=col.label, format=col.format)
                )
                found = True
            else:
                renamed.append(col)
        if not found:
            raise ValueError(f"column {old_key!r} does not exist")
        return await self.set_columns(renamed)

    async def insert_one(self, document: dict) -> dict:
        return await self._collection.insert_one(document)

    async def insert_many(self, documents: list[dict]) -> list[dict]:
        return await self._collection.insert_many(documents)

    async def find_one(self, filter: dict | None = None) -> dict | None:
        return await self._collection.find_one(filter)

    async def find(
        self, filter: dict | None = None, limit: int = 0, skip: int = 0, sort: dict | None = None
    ) -> list[dict]:
        return await self._collection.find(filter=filter, limit=limit, skip=skip, sort=sort)

    async def raw_get(self, filter: dict | None = None) -> CollectionRow | None:
        return await self._collection.find_one(filter)

    async def raw_filter(
        self, filter: dict | None = None, limit: int = 0, skip: int = 0, sort: dict | None = None
    ) -> list[CollectionRow]:
        return await self._collection.find(filter=filter, limit=limit, skip=skip, sort=sort)

    def all(self) -> CollectionQuery:
        return CollectionQuery(self)

    def filter(self, **lookups) -> CollectionQuery:
        return CollectionQuery(self, compile_lookups(lookups))

    async def get(self, **lookups) -> CollectionRow | None:
        return await self.filter(**lookups).first()

    async def update_one(self, filter: dict, update: dict, *, upsert: bool = False) -> dict:
        return await self._collection.update_one(filter, update, upsert=upsert)

    async def delete_one(self, filter: dict) -> dict:
        return await self._collection.delete_one(filter)

    async def delete_many(self, filter: dict) -> dict:
        return await self._collection.delete_many(filter)

    async def delete_rows(self, rows_or_ids) -> dict:
        return await self.delete_many(_ids_filter(rows_or_ids))

    async def count(self, filter: dict | None = None) -> int:
        return await self._collection.count(filter)


class CollectionManager:
    """Factory for runtime-created, schema-aware collections."""

    def __init__(
        self,
        stub: DataServiceStub,
        app_id: str,
        *,
        default_scope: CollectionScope = SCOPE_APP,
        user_id: str = "",
        owner_id: str = "",
        session_id: str = "",
        collection_scopes: dict[str, str] | None = None,
    ) -> None:
        self._stub = stub
        self._app_id = app_id
        self._default_scope = default_scope
        self._user_id = user_id
        self._owner_id = owner_id
        self._session_id = session_id
        self._scopes = collection_scopes or {}

    async def get(self, name: str, *, scope: CollectionScope | None = None) -> DynamicCollection:
        resolved = scope or self._scopes.get(name)
        if resolved is None:
            raise ValueError(
                f"scope is required for dynamic collection {name!r} because it has no static declaration"
            )
        if resolved not in VALID_SCOPES:
            raise ValueError(f"scope must be one of {VALID_SCOPES}, got {resolved!r}")
        static_scope = self._scopes.get(name)
        if scope is not None and static_scope is not None and scope != static_scope:
            raise ValueError(
                f"collection {name!r} is statically declared with scope={static_scope!r}, got {scope!r}"
            )
        return DynamicCollection(
            self._stub,
            self._app_id,
            name,
            resolved,  # type: ignore[arg-type]
            user_id=self._user_id,
            owner_id=self._owner_id,
            session_id=self._session_id,
        )


class CollectionRef:
    """First-class handle returned by ``app.collection()``.

    Carries declaration metadata at import time. After boot the runner binds
    a live ``Collection`` so CRUD methods work directly on the ref.

    For scoped collections (user/owner/session), the runner installs the
    active handler identity in a context-local slot before each handler call
    and clears it after. Every CRUD call delegates to a ``ScopedCollection``
    that injects identity fields automatically. If no compatible identity is
    active, a clear error is raised.
    """

    def __init__(self, name: str, decl: CollectionDecl) -> None:
        self.name = name
        self._decl = decl
        self._bound: Collection | None = None
        self._active_session: object | None = None

    def _require_bound(self) -> Collection:
        if self._bound is None:
            raise RuntimeError(
                f"Collection '{self.name}' is not bound yet. "
                "CRUD methods are only available after the app has booted."
            )
        return self._bound

    def _resolve(self) -> Collection | ScopedCollection:
        col = self._require_bound()
        if self._decl.scope == SCOPE_APP:
            return col

        identity = get_active_identity() or self._active_session
        if identity is None:
            raise RuntimeError(
                f"Collection '{self.name}' has scope='{self._decl.scope}' "
                "but no active handler context. Use this inside a @message, "
                "@task, @data, or @endpoint handler."
            )

        user = getattr(identity, "user", None)
        user_id = getattr(user, "id", "") if user else ""
        owner_id = getattr(user, "owner_id", "") if user else ""
        session_id = getattr(identity, "id", "")

        if self._decl.scope == SCOPE_OWNER and not (owner_id or user_id):
            raise RuntimeError(
                f"Collection '{self.name}' has scope='owner' but no authenticated user context."
            )
        if self._decl.scope != SCOPE_OWNER and self._decl.scope != SCOPE_SESSION and not user_id:
            raise RuntimeError(
                f"Collection '{self.name}' has scope='{self._decl.scope}' but no authenticated user context."
            )
        if self._decl.scope == SCOPE_SESSION and not session_id:
            raise RuntimeError(
                f"Collection '{self.name}' has scope='session' but no active session id."
            )

        sf = self._decl.scope_filter(
            user_id=user_id,
            owner_id=owner_id,
            session_id=session_id,
        )
        return ScopedCollection(col, sf)

    def _static_columns(self) -> list[Column]:
        return list(self._decl.columns or [])

    def _schema_handle(self) -> DynamicCollection:
        col = self._require_bound()
        if self._decl.scope == SCOPE_APP:
            return DynamicCollection(col._stub, col._app_id, self.name, SCOPE_APP)

        identity = get_active_identity() or self._active_session
        if identity is None:
            raise RuntimeError(
                f"Collection '{self.name}' has scope='{self._decl.scope}' "
                "but no active handler context. Use this inside a @message, "
                "@task, @data, or @endpoint handler."
            )
        user = getattr(identity, "user", None)
        user_id = getattr(user, "id", "") if user else ""
        owner_id = getattr(user, "owner_id", "") if user else ""
        session_id = getattr(identity, "id", "")
        return DynamicCollection(
            col._stub,
            col._app_id,
            self.name,
            self._decl.scope,
            user_id=user_id,
            owner_id=owner_id,
            session_id=session_id,
        )

    async def list_columns(self) -> list[Column]:
        if self._bound is None:
            return self._static_columns()
        columns = await self._schema_handle().list_columns()
        return columns or self._static_columns()

    async def set_columns(self, columns: list[str | Column | dict]) -> list[Column]:
        return await self._schema_handle().set_columns(columns)

    async def add_column(
        self,
        key: str,
        *,
        type: str = "text",
        label: str | None = None,
        format: str | None = None,
        default=None,
        backfill: bool = False,
    ) -> list[Column]:
        if backfill or default is not None:
            raise NotImplementedError(
                "column backfill is not supported yet; update rows explicitly"
            )
        columns = await self.list_columns()
        if any(col.key == key for col in columns):
            raise ValueError(f"column {key!r} already exists")
        return await self.set_columns(
            [*columns, Column(key=key, type=type, label=label, format=format)]
        )

    async def remove_column(self, key: str, *, drop_values: bool = False) -> list[Column]:
        if drop_values:
            raise NotImplementedError("dropping stored column values is not supported yet")
        columns = [col for col in await self.list_columns() if col.key != key]
        return await self.set_columns(columns)

    async def rename_column(
        self,
        old_key: str,
        new_key: str,
        *,
        migrate_values: bool = False,
    ) -> list[Column]:
        if migrate_values:
            raise NotImplementedError("stored value migration is not supported yet")
        columns = await self.list_columns()
        renamed: list[Column] = []
        found = False
        for col in columns:
            if col.key == old_key:
                renamed.append(
                    Column(key=new_key, type=col.type, label=col.label, format=col.format)
                )
                found = True
            else:
                renamed.append(col)
        if not found:
            raise ValueError(f"column {old_key!r} does not exist")
        return await self.set_columns(renamed)

    async def insert_one(self, document: dict) -> dict:
        return await self._resolve().insert_one(document)

    async def insert_many(self, documents: list[dict]) -> list[dict]:
        return await self._resolve().insert_many(documents)

    async def raw_get(self, filter: dict | None = None) -> CollectionRow | None:
        return await self._resolve().find_one(filter)

    async def find_one(self, filter: dict | None = None) -> CollectionRow | None:
        return await self.raw_get(filter)

    async def raw_filter(
        self, filter: dict | None = None, limit: int = 0, skip: int = 0, sort: dict | None = None
    ) -> list[CollectionRow]:
        return await self._resolve().find(filter=filter, limit=limit, skip=skip, sort=sort)

    async def find(
        self, filter: dict | None = None, limit: int = 0, skip: int = 0, sort: dict | None = None
    ) -> list[CollectionRow]:
        return await self.raw_filter(filter=filter, limit=limit, skip=skip, sort=sort)

    def all(self) -> CollectionQuery:
        return CollectionQuery(self)

    def filter(self, **lookups) -> CollectionQuery:
        return CollectionQuery(self, compile_lookups(lookups))

    async def get(self, **lookups) -> CollectionRow | None:
        return await self.filter(**lookups).first()

    async def update_one(self, filter: dict, update: dict) -> dict:
        return await self._resolve().update_one(filter, update)

    async def delete_one(self, filter: dict) -> dict:
        return await self._resolve().delete_one(filter)

    async def delete_many(self, filter: dict) -> dict:
        return await self._resolve().delete_many(filter)

    async def delete_rows(self, rows_or_ids) -> dict:
        return await self.delete_many(_ids_filter(rows_or_ids))

    async def count(self, filter: dict | None = None) -> int:
        return await self._resolve().count(filter)

    def __repr__(self) -> str:
        bound = "bound" if self._bound else "unbound"
        return f"CollectionRef({self.name!r}, scope={self._decl.scope!r}, {bound})"


class DatabaseProxy:
    """Backs ``self.db`` — attribute access returns a ``Collection`` by name."""

    def __init__(self, stub: DataServiceStub, app_id: str) -> None:
        self._stub = stub
        self._app_id = app_id
        self._collections: dict[str, Collection] = {}

    def __getattr__(self, name: str) -> Collection:
        if name.startswith("_"):
            raise AttributeError(name)
        if name not in self._collections:
            self._collections[name] = Collection(self._stub, self._app_id, name)
        return self._collections[name]


class ScopedCollection:
    """Wraps a Collection with automatic scope filters (_user_id / _owner_id / _session_id)."""

    __slots__ = ("_inner", "_scope_filter")

    def __init__(self, inner: Collection, scope_filter: dict[str, str]) -> None:
        self._inner = inner
        self._scope_filter = scope_filter

    def _merge(self, filter: dict | None) -> dict:
        merged = dict(self._scope_filter)
        if filter:
            merged.update(filter)
        return merged

    async def insert_one(self, document: dict) -> dict:
        doc = {**self._scope_filter, **document}
        row = await self._inner.insert_one(doc)
        return CollectionRow(dict(row), self)

    async def insert_many(self, documents: list[dict]) -> list[dict]:
        docs = [{**self._scope_filter, **d} for d in documents]
        rows = await self._inner.insert_many(docs)
        return [CollectionRow(dict(row), self) for row in rows]

    async def raw_get(self, filter: dict | None = None) -> CollectionRow | None:
        row = await self._inner.find_one(self._merge(filter))
        return CollectionRow(dict(row), self) if row else None

    async def find_one(self, filter: dict | None = None) -> CollectionRow | None:
        return await self.raw_get(filter)

    async def raw_filter(
        self, filter: dict | None = None, limit: int = 0, skip: int = 0, sort: dict | None = None
    ) -> list[CollectionRow]:
        rows = await self._inner.find(filter=self._merge(filter), limit=limit, skip=skip, sort=sort)
        return [CollectionRow(dict(row), self) for row in rows]

    async def find(
        self, filter: dict | None = None, limit: int = 0, skip: int = 0, sort: dict | None = None
    ) -> list[CollectionRow]:
        return await self.raw_filter(filter=filter, limit=limit, skip=skip, sort=sort)

    def all(self) -> CollectionQuery:
        return CollectionQuery(self)

    def filter(self, **lookups) -> CollectionQuery:
        return CollectionQuery(self, compile_lookups(lookups))

    async def get(self, **lookups) -> CollectionRow | None:
        return await self.filter(**lookups).first()

    async def update_one(self, filter: dict, update: dict, *, upsert: bool = False) -> dict:
        return await self._inner.update_one(self._merge(filter), update, upsert=upsert)

    async def delete_one(self, filter: dict) -> dict:
        return await self._inner.delete_one(self._merge(filter))

    async def delete_many(self, filter: dict) -> dict:
        return await self._inner.delete_many(self._merge(filter))

    async def delete_rows(self, rows_or_ids) -> dict:
        return await self.delete_many(_ids_filter(rows_or_ids))

    async def count(self, filter: dict | None = None) -> int:
        return await self._inner.count(self._merge(filter))


class ScopedDatabaseProxy:
    """Scoped db proxy for ``session.db`` — auto-injects user/owner/session identity."""

    def __init__(
        self,
        stub: DataServiceStub,
        app_id: str,
        user_id: str,
        owner_id: str,
        session_id: str,
        collection_scopes: dict[str, str],
    ) -> None:
        self._stub = stub
        self._app_id = app_id
        self._user_id = user_id
        self._owner_id = owner_id
        self._session_id = session_id
        self._scopes = collection_scopes
        self._collections: dict[str, ScopedCollection] = {}

    def __getattr__(self, name: str) -> ScopedCollection:
        if name.startswith("_"):
            raise AttributeError(name)
        if name not in self._collections:
            scope = self._scopes.get(name, SCOPE_APP)
            if scope == SCOPE_APP:
                raise ValueError(
                    f"Collection '{name}' has scope='app'. "
                    f"Use self.db.{name} instead of session.db.{name}"
                )
            if scope == SCOPE_SESSION:
                scope_filter = {SCOPE_FIELD_SESSION: self._session_id}
            elif scope == SCOPE_OWNER:
                scope_filter = {SCOPE_FIELD_OWNER: self._owner_id or self._user_id}
            else:
                scope_filter = {SCOPE_FIELD_USER: self._user_id}
            inner = Collection(self._stub, self._app_id, name)
            self._collections[name] = ScopedCollection(inner, scope_filter)
        return self._collections[name]
