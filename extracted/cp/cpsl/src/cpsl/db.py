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
from typing import TYPE_CHECKING

from .constants import (
    CollectionDecl,
    SCOPE_APP, SCOPE_SESSION, SCOPE_OWNER,
    SCOPE_FIELD_SESSION, SCOPE_FIELD_OWNER, SCOPE_FIELD_USER,
)

if TYPE_CHECKING:
    from .clients.capsule import DataServiceStub


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
        doc["id"] = doc["_id"]
    return doc


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
            None, self._stub.insert_one,
            InsertOneRequest(app_id=self._app_id, collection=self._name, document_json=doc_json),
        )
        result = dict(document)
        result["_id"] = resp.id
        return _with_id_alias(result)

    async def insert_many(self, documents: list[dict]) -> list[dict]:
        from .clients.capsule import InsertManyRequest
        docs_json = [json.dumps(d).encode() for d in documents]
        resp = await asyncio.get_running_loop().run_in_executor(
            None, self._stub.insert_many,
            InsertManyRequest(app_id=self._app_id, collection=self._name, documents_json=docs_json),
        )
        results = []
        for doc, id_ in zip(documents, resp.ids):
            r = dict(doc)
            r["_id"] = id_
            results.append(_with_id_alias(r))
        return results

    async def find_one(self, filter: dict | None = None) -> dict | None:
        from .clients.capsule import FindOneRequest
        filter_json = json.dumps(filter or {}).encode()
        resp = await asyncio.get_running_loop().run_in_executor(
            None, self._stub.find_one,
            FindOneRequest(app_id=self._app_id, collection=self._name, filter_json=filter_json),
        )
        if not resp.document_json:
            return None
        return _with_id_alias(json.loads(resp.document_json))

    async def find(self, filter: dict | None = None, limit: int = 0, skip: int = 0,
                   sort: dict | None = None) -> list[dict]:
        from .clients.capsule import FindRequest
        filter_json = json.dumps(filter or {}).encode()
        sort_json = json.dumps(sort or {}).encode() if sort else b''
        resp = await asyncio.get_running_loop().run_in_executor(
            None, self._stub.find,
            FindRequest(
                app_id=self._app_id,
                collection=self._name,
                filter_json=filter_json,
                limit=limit,
                skip=skip,
                sort_json=sort_json,
            ),
        )
        return [_with_id_alias(json.loads(d)) for d in resp.documents_json]

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
            None, self._stub.update_one,
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
            None, self._stub.delete_one,
            DeleteOneRequest(app_id=self._app_id, collection=self._name, filter_json=filter_json),
        )
        return {"deleted": resp.deleted}

    async def count(self, filter: dict | None = None) -> int:
        from .clients.capsule import CountRequest
        filter_json = json.dumps(filter or {}).encode()
        resp = await asyncio.get_running_loop().run_in_executor(
            None, self._stub.count,
            CountRequest(app_id=self._app_id, collection=self._name, filter_json=filter_json),
        )
        return resp.count


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

    async def insert_one(self, document: dict) -> dict:
        return await self._resolve().insert_one(document)

    async def insert_many(self, documents: list[dict]) -> list[dict]:
        return await self._resolve().insert_many(documents)

    async def find_one(self, filter: dict | None = None) -> dict | None:
        return await self._resolve().find_one(filter)

    async def find(self, filter: dict | None = None, limit: int = 0, skip: int = 0,
                   sort: dict | None = None) -> list[dict]:
        return await self._resolve().find(filter=filter, limit=limit, skip=skip, sort=sort)

    async def update_one(self, filter: dict, update: dict) -> dict:
        return await self._resolve().update_one(filter, update)

    async def delete_one(self, filter: dict) -> dict:
        return await self._resolve().delete_one(filter)

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
        return await self._inner.insert_one(doc)

    async def insert_many(self, documents: list[dict]) -> list[dict]:
        docs = [{**self._scope_filter, **d} for d in documents]
        return await self._inner.insert_many(docs)

    async def find_one(self, filter: dict | None = None) -> dict | None:
        return await self._inner.find_one(self._merge(filter))

    async def find(self, filter: dict | None = None, limit: int = 0, skip: int = 0,
                   sort: dict | None = None) -> list[dict]:
        return await self._inner.find(filter=self._merge(filter), limit=limit, skip=skip, sort=sort)

    async def update_one(self, filter: dict, update: dict) -> dict:
        return await self._inner.update_one(self._merge(filter), update)

    async def delete_one(self, filter: dict) -> dict:
        return await self._inner.delete_one(self._merge(filter))

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
