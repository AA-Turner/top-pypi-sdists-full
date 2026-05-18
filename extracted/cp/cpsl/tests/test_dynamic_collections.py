import json
import os
import sys
import unittest
from types import SimpleNamespace

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from cpsl.constants import CollectionDecl, Column
from cpsl.clients.capsule import (
    DeleteManyResponse,
    DeleteOneResponse,
    FindResponse,
    GetCollectionSchemaResponse,
    InsertManyResponse,
    InsertOneResponse,
    UpsertCollectionSchemaResponse,
    UpdateOneResponse,
)
from cpsl.db import (
    Collection,
    CollectionManager,
    CollectionRef,
    reset_active_identity,
    set_active_identity,
)
from cpsl.session import UserInfo


class FakeDataStub:
    def __init__(self):
        self.schemas = {}
        self.last_find = None
        self.last_delete_many = None
        self.find_docs = []

    def _key(self, schema_or_req):
        return (
            schema_or_req.app_id if hasattr(schema_or_req, "app_id") else "",
            schema_or_req.name,
            schema_or_req.scope,
            schema_or_req.user_id,
            schema_or_req.owner_id,
            schema_or_req.session_id,
        )

    def get_collection_schema(self, req):
        schema = self.schemas.get(self._key(req))
        return GetCollectionSchemaResponse(found=schema is not None, schema=schema)

    def upsert_collection_schema(self, req):
        schema = req.schema
        self.schemas[
            (
                req.app_id,
                schema.name,
                schema.scope,
                schema.user_id,
                schema.owner_id,
                schema.session_id,
            )
        ] = schema
        return UpsertCollectionSchemaResponse(schema=schema)

    def find(self, req):
        self.last_find = req
        return FindResponse(documents_json=[json.dumps(d).encode() for d in self.find_docs])

    def delete_many(self, req):
        self.last_delete_many = req
        return DeleteManyResponse(deleted=2)

    def insert_one(self, req):
        return InsertOneResponse(id="row-1")

    def insert_many(self, req):
        return InsertManyResponse(
            ids=[f"row-{i + 1}" for i, _ in enumerate(req.documents_json)]
        )

    def update_one(self, req):
        return UpdateOneResponse(matched=1, modified=1)

    def delete_one(self, req):
        return DeleteOneResponse(deleted=1)


class DynamicCollectionTests(unittest.IsolatedAsyncioTestCase):
    async def test_collection_mutations_emit_widget_update_for_active_session(self):
        stub = FakeDataStub()
        blocks: list[dict] = []

        async def block_cb(block_json: str):
            blocks.append(json.loads(block_json))

        token = set_active_identity(SimpleNamespace(id="sess-1", _block_callback=block_cb))
        try:
            col = Collection(stub, "app-1", "leads")
            await col.insert_one({"name": "Ada"})
            await col.update_one({"_id": "row-1"}, {"name": "Grace"})
            await col.delete_many({})
        finally:
            reset_active_identity(token)

        self.assertEqual([b["type"] for b in blocks], ["widget_update"] * 3)
        self.assertEqual([b["payload"]["collection"] for b in blocks], ["leads"] * 3)
        self.assertEqual([b["payload"]["reason"] for b in blocks], ["data"] * 3)
        self.assertEqual([b["payload"]["session_id"] for b in blocks], ["sess-1"] * 3)

    async def test_schema_mutation_emits_widget_update_for_active_session(self):
        stub = FakeDataStub()
        blocks: list[dict] = []

        async def block_cb(block_json: str):
            blocks.append(json.loads(block_json))

        token = set_active_identity(SimpleNamespace(id="sess-1", _block_callback=block_cb))
        try:
            manager = CollectionManager(
                stub,
                "app-1",
                collection_scopes={"leads": "owner"},
                user_id="u1",
                owner_id="org:o1",
            )
            leads = await manager.get("leads")
            await leads.set_columns(["name"])
        finally:
            reset_active_identity(token)

        self.assertEqual(len(blocks), 1)
        self.assertEqual(blocks[0]["type"], "widget_update")
        self.assertEqual(blocks[0]["payload"]["collection"], "leads")
        self.assertEqual(blocks[0]["payload"]["reason"], "schema")

    async def test_dynamic_collection_columns_round_trip(self):
        stub = FakeDataStub()
        manager = CollectionManager(
            stub,
            "app-1",
            collection_scopes={"leads": "owner"},
            user_id="u1",
            owner_id="org:o1",
        )

        leads = await manager.get("leads")
        columns = await leads.set_columns(
            [
                "name",
                Column("score", type="number", label="Lead Score"),
            ]
        )

        self.assertEqual([c.key for c in columns], ["name", "score"])
        self.assertEqual([c.key for c in await leads.list_columns()], ["name", "score"])

        await leads.add_column("status")
        self.assertEqual([c.key for c in await leads.list_columns()], ["name", "score", "status"])

        await leads.remove_column("name")
        self.assertEqual([c.key for c in await leads.list_columns()], ["score", "status"])

    async def test_dynamic_collection_scope_filter_applies_to_rows(self):
        stub = FakeDataStub()
        manager = CollectionManager(stub, "app-1", user_id="u1", owner_id="org:o1")

        leads = await manager.get("leads", scope="owner")
        await leads.find({"status": "open"})

        self.assertEqual(
            json.loads(stub.last_find.filter_json), {"_team_id": "org:o1", "status": "open"}
        )

    async def test_lazy_filter_limit_order_and_query_delete(self):
        stub = FakeDataStub()
        stub.find_docs = [{"_id": "row-1", "status": "archived"}]
        manager = CollectionManager(
            stub, "app-1", collection_scopes={"leads": "owner"}, user_id="u1", owner_id="org:o1"
        )

        leads = await manager.get("leads")
        rows = await leads.filter(status="archived", score__gt=80).order_by("-created_at").limit(10)

        self.assertEqual(rows[0]["id"], "row-1")
        self.assertEqual(
            json.loads(stub.last_find.filter_json),
            {
                "_team_id": "org:o1",
                "status": "archived",
                "score": {"$gt": 80},
            },
        )
        self.assertEqual(stub.last_find.limit, 10)
        self.assertEqual(json.loads(stub.last_find.sort_json), {"created_at": -1})

        await leads.filter(status="archived").delete()
        self.assertEqual(
            json.loads(stub.last_delete_many.filter_json),
            {
                "_team_id": "org:o1",
                "status": "archived",
            },
        )

    async def test_row_delete_and_delete_rows_use_ids(self):
        stub = FakeDataStub()
        stub.find_docs = [{"_id": {"$oid": "507f1f77bcf86cd799439011"}}, {"id": "row-2"}]
        manager = CollectionManager(stub, "app-1", collection_scopes={"leads": "app"})

        leads = await manager.get("leads")
        rows = await leads.all().limit(2)
        await rows[0].delete()
        self.assertEqual(
            json.loads(stub.last_delete_many.filter_json),
            {"_id": {"$in": ["507f1f77bcf86cd799439011"]}},
        )

        await leads.delete_rows(rows)
        self.assertEqual(
            json.loads(stub.last_delete_many.filter_json),
            {"_id": {"$in": ["507f1f77bcf86cd799439011", "row-2"]}},
        )

    async def test_dynamic_collection_requires_scope_without_static_declaration(self):
        manager = CollectionManager(FakeDataStub(), "app-1")

        with self.assertRaisesRegex(ValueError, "scope is required"):
            await manager.get("leads")

    async def test_dynamic_collection_rejects_conflicting_static_scope(self):
        manager = CollectionManager(FakeDataStub(), "app-1", collection_scopes={"leads": "user"})

        with self.assertRaisesRegex(ValueError, "statically declared"):
            await manager.get("leads", scope="owner")

    async def test_collection_ref_lists_static_columns_before_binding(self):
        ref = CollectionRef(
            "notes",
            CollectionDecl(name="notes", columns=(Column("title"), Column("body")), scope="app"),
        )

        self.assertEqual([c.key for c in await ref.list_columns()], ["title", "body"])

    async def test_collection_ref_schema_helpers_use_decl_scope(self):
        stub = FakeDataStub()
        ref = CollectionRef(
            "notes",
            CollectionDecl(name="notes", columns=(Column("title"),), scope="owner"),
        )
        ref._bound = Collection(stub, "app-1", "notes")
        token = set_active_identity(
            type(
                "Identity",
                (),
                {
                    "id": "",
                    "user": UserInfo(id="u1", org_id="org_1"),
                },
            )()
        )
        try:
            columns = await ref.add_column("body")
        finally:
            reset_active_identity(token)

        self.assertEqual([c.key for c in columns], ["title", "body"])
        schema = next(iter(stub.schemas.values()))
        self.assertEqual(schema.scope, "owner")
        self.assertEqual(schema.owner_id, "org:org_1")


if __name__ == "__main__":
    unittest.main()
