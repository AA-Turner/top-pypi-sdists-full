import json
import os
import sys
import unittest
from types import SimpleNamespace

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from cpsl.clients.capsule import UpsertCollectionSchemaResponse
from cpsl.constants import CollectionDecl, Column, HEADER_ORG_ID, HEADER_SESSION_ID, HEADER_USER_ID
from cpsl.runner.routes import RunnerRouteMixin


class _Request:
    def __init__(
        self,
        *,
        match_info: dict,
        body: dict,
        headers: dict | None = None,
        query: dict | None = None,
    ) -> None:
        self.match_info = match_info
        self._body = body
        self.headers = headers or {}
        self.query = query or {}

    async def json(self) -> dict:
        return self._body


class _Rows:
    def __init__(self, row: dict) -> None:
        self.row = dict(row)
        self.last_filter: dict | None = None
        self.last_updates: dict | None = None

    async def update_one(self, filter_doc: dict, updates: dict) -> dict:
        self.last_filter = dict(filter_doc)
        self.last_updates = dict(updates)
        if await self.find_one(filter_doc) is None:
            return {"matched": 0, "modified": 0}
        self.row.update(updates)
        return {"matched": 1, "modified": 1}

    async def find_one(self, filter_doc: dict) -> dict | None:
        if all(self.row.get(key) == value for key, value in filter_doc.items()):
            return dict(self.row)
        return None


class _SchemaStub:
    def __init__(self) -> None:
        self.last_request = None

    def upsert_collection_schema(self, request):
        self.last_request = request
        return UpsertCollectionSchemaResponse(schema=request.schema)


class _RouteHarness(RunnerRouteMixin):
    def __init__(self, *, collections: list[CollectionDecl], db=None, data_stub=None) -> None:
        self._instance = SimpleNamespace(db=db) if db is not None else SimpleNamespace()
        self._collections = {decl.name: decl for decl in collections}
        self._data_stub = data_stub
        self._data_app_id = "app-1"

    def _get_all_collections(self):
        return self._collections

    def _get_all_settings(self):
        return {}

    async def _run_rpc(self, fn, *args):
        return fn(*args)


class CollectionTableRouteTests(unittest.IsolatedAsyncioTestCase):
    async def test_patch_collection_row_uses_collection_scope(self):
        rows = _Rows({"_id": "row-1", "_team_id": "org-1", "name": "Ada"})
        runner = _RouteHarness(
            collections=[CollectionDecl(name="leads", scope="owner")],
            db=SimpleNamespace(leads=rows),
        )
        handler = runner._wrap_collection_update()

        response = await handler(
            _Request(
                match_info={"name": "leads", "row_id": "row-1"},
                body={"updates": {"name": "Grace"}},
                headers={HEADER_USER_ID: "user-1", HEADER_ORG_ID: "org-1"},
            )
        )

        self.assertEqual(response.status, 200)
        self.assertEqual(rows.last_filter, {"_id": "row-1", "_team_id": "org-1"})
        self.assertEqual(rows.last_updates, {"name": "Grace"})
        self.assertEqual(json.loads(response.text)["row"]["name"], "Grace")

    async def test_put_collection_columns_persists_full_ordered_schema(self):
        stub = _SchemaStub()
        runner = _RouteHarness(
            collections=[
                CollectionDecl(
                    name="leads",
                    scope="owner",
                    columns=(Column("name"), Column("email", type="email", label="Email")),
                )
            ],
            data_stub=stub,
        )
        handler = runner._wrap_collection_columns_update()

        response = await handler(
            _Request(
                match_info={"name": "leads"},
                body={
                    "columns": [
                        {"key": "email", "type": "email", "label": "Email"},
                        {"key": "name", "type": "text", "label": "Name"},
                    ]
                },
                headers={
                    HEADER_USER_ID: "user-1",
                    HEADER_ORG_ID: "org-1",
                    HEADER_SESSION_ID: "session-1",
                },
            )
        )

        self.assertEqual(response.status, 200)
        schema = stub.last_request.schema
        self.assertEqual(schema.name, "leads")
        self.assertEqual(schema.scope, "owner")
        self.assertEqual(schema.owner_id, "org-1")
        self.assertEqual([col.key for col in schema.columns], ["email", "name"])
        self.assertEqual([col.type for col in schema.columns], ["email", "text"])
        self.assertEqual(
            [col["key"] for col in json.loads(response.text)["columns"]],
            ["email", "name"],
        )

    async def test_put_collection_columns_reset_uses_app_default_columns(self):
        stub = _SchemaStub()
        runner = _RouteHarness(
            collections=[
                CollectionDecl(
                    name="leads",
                    scope="owner",
                    columns=(Column("name"), Column("email", type="email")),
                )
            ],
            data_stub=stub,
        )
        handler = runner._wrap_collection_columns_update()

        response = await handler(
            _Request(
                match_info={"name": "leads"},
                body={"reset": True},
                headers={HEADER_ORG_ID: "org-1"},
            )
        )

        self.assertEqual(response.status, 200)
        self.assertEqual([col.key for col in stub.last_request.schema.columns], ["name", "email"])


if __name__ == "__main__":
    unittest.main()
