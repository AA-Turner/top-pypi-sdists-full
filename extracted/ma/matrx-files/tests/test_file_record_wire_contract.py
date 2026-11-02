"""GET /files/{id} speaks the published durable-URL contract.

The incident (2026-08): the standalone service (files.matrxserver.com) carried
a second, independent record shape — ``{file_id, folder_id, version}`` with no
URL fields — and a ``/url`` envelope with no ``expires_in``, while the
published OpenAPI contract (what matrx-frontend's generated types are built
from) says ``{id, parent_folder_id, current_version, checksum, public_url,
url, cdn_url, download_url, thumbnail_url}``. Every cold FE metadata
hydration lost its fileId.

The fix: ONE deserializer — ``matrx_files.api.records`` — consumed by both
the standalone router and the aidream host router. These tests pin the wire
shape offline so the drift class cannot silently return.

Since the 2026-08 signed-URL eradication the contract is durable-only:
``signed_url`` / ``signed_url_expires_at`` must NEVER reappear on
``FileRecord``, ``SignedUrlResponse`` is deleted, and ``GET /files/{id}/url``
does not exist.
"""

from __future__ import annotations

import ast
from matrx_utils.source_guard import stable_source
import json
from types import SimpleNamespace

import matrx_files.api.records as records_module
from matrx_files.api.records import FileRecord, to_file_record
from matrx_files.api.router_files import build_file_router


# The published FileRecord contract — matrx-frontend
# types/python-generated/api-types.ts ``components.schemas.FileRecord``.
CONTRACT_FIELDS = {
    "id",
    "owner_id",
    "organization_id",
    "file_path",
    "file_name",
    "mime_type",
    "size_bytes",
    "checksum",
    "published_to_web",
    "shown_to",
    "visibility",
    "current_version",
    "parent_folder_id",
    "parent_file_id",
    "derivation_kind",
    "derivation_metadata",
    "duplicate_of_file_id",
    "canonical_processed_document_id",
    "metadata",
    "created_at",
    "updated_at",
    "deleted_at",
    "public_url",
    "thumbnail_url",
    "url",
    "cdn_url",
    "download_url",
}


def test_buffered_upload_relocates_transcript_origin_for_standalone():
    """The package router must not depend on aidream's host relocation hook."""
    from fastapi import FastAPI
    from fastapi.testclient import TestClient

    class _Service:
        call: dict | None = None

        async def upload_simple(self, content, **kwargs):
            self.call = kwargs
            return SimpleNamespace(
                file_id="file-1",
                size_bytes=len(content),
                checksum="abc",
                url=None,
                cdn_url=None,
                download_url=None,
                published_to_web=False,
                shown_to="only_me",
            )

    service = _Service()
    app = FastAPI()
    app.include_router(build_file_router(service, user_id_dep=lambda: "user-1"))
    client = TestClient(app)

    response = client.post(
        "/files/upload",
        files={"file": ("rec.webm", b"audio", "audio/webm")},
        data={
            "file_path": "Transcripts/Recordings/rec.webm",
            "metadata_json": json.dumps({"origin": "transcripts"}),
        },
    )

    assert response.status_code == 200, response.text
    assert service.call is not None
    assert service.call["file_path"] == "system-files/transcripts/Recordings/rec.webm"
    assert response.json()["file_path"] == "system-files/transcripts/Recordings/rec.webm"


def test_buffered_upload_force_new_copy_uses_strict_intent_service():
    """A user's explicit Make-a-copy decision must create a distinct row.

    The old buffered route always called ``upload_simple``. That method aliases
    checksum-identical content, so the UI displayed a renamed optimistic row
    backed by the original file id and no durable copy existed.
    """
    from fastapi import FastAPI
    from fastapi.testclient import TestClient

    class _Service:
        strict_call: dict | None = None

        async def upload_simple(self, *_args, **_kwargs):
            raise AssertionError("force_new_copy must not use upload_simple")

        async def upload_with_intent(self, content, **kwargs):
            self.strict_call = {"content": content, **kwargs}
            result = SimpleNamespace(
                file_id="copy-file-2",
                size_bytes=len(content),
                checksum="same-checksum",
                url=None,
                cdn_url=None,
                download_url=None,
                published_to_web=False,
                shown_to="only_me",
            )
            return {
                "outcome": "force_copy_created",
                "file_id": result.file_id,
                "file_path": "Q1-DUPLICATE (1).txt",
                "duplicate_of_file_id": "original-file-1",
                "result": result,
            }

    service = _Service()
    app = FastAPI()
    app.include_router(build_file_router(service, user_id_dep=lambda: "user-1"))
    client = TestClient(app)

    response = client.post(
        "/files/upload",
        files={"file": ("Q1-DUPLICATE.txt", b"same bytes", "text/plain")},
        data={
            "file_path": "Q1-DUPLICATE (1).txt",
            "intent": "force_new_copy",
            "reason": "User selected Make a copy in the duplicate dialog",
        },
    )

    assert response.status_code == 200, response.text
    assert response.json()["file_id"] == "copy-file-2"
    assert response.json()["file_path"] == "Q1-DUPLICATE (1).txt"
    assert service.strict_call is not None
    assert service.strict_call["intent"] == "force_new_copy"
    assert service.strict_call["reason"] == ("User selected Make a copy in the duplicate dialog")
    assert service.strict_call["owner_id"] == "user-1"


# The drifted spellings that broke the FE, plus the retired signed-URL
# fields (eradicated 2026-08). None may ever reappear.
FORBIDDEN_DRIFT_FIELDS = {
    "file_id",
    "folder_id",
    "version",
    "signed_url",
    "signed_url_expires_at",
}

_ROW = {
    "id": "11111111-1111-1111-1111-111111111111",
    "owner_id": "22222222-2222-2222-2222-222222222222",
    "organization_id": "aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa",
    "file_path": "Images/hero.png",
    "file_name": "hero.png",
    "mime_type": "image/png",
    "size_bytes": 123,
    "checksum": "abc123",
    "published_to_web": False,
    "shown_to": "only_me",
    "current_version": 3,
    "parent_folder_id": "33333333-3333-3333-3333-333333333333",
    "parent_file_id": "44444444-4444-4444-4444-444444444444",
    "derivation_kind": "pdf_text_extract",
    "derivation_metadata": {"pages": 12},
    "duplicate_of_file_id": "55555555-5555-5555-5555-555555555555",
    "canonical_processed_document_id": "66666666-6666-6666-6666-666666666666",
    "metadata": {"tag": "x"},
    "created_at": "2026-08-01T00:00:00+00:00",
    "updated_at": "2026-08-02T00:00:00+00:00",
    "deleted_at": None,
}


def test_file_record_fields_match_published_contract_exactly():
    assert set(FileRecord.model_fields.keys()) == CONTRACT_FIELDS
    assert not (set(FileRecord.model_fields.keys()) & FORBIDDEN_DRIFT_FIELDS)


def test_signed_url_contract_is_fully_retired():
    """The 2026-08 eradication: no signed_url field, no SignedUrlResponse."""
    assert "signed_url" not in FileRecord.model_fields
    assert "signed_url_expires_at" not in FileRecord.model_fields
    assert not hasattr(records_module, "SignedUrlResponse")

    import matrx_files.api.router_files as router_files_module

    assert not hasattr(router_files_module, "SignedUrlResponse")


def test_to_file_record_maps_row_to_contract_names():
    rec = to_file_record(_ROW)
    assert rec.id == _ROW["id"]
    assert rec.parent_folder_id == _ROW["parent_folder_id"]
    assert rec.current_version == 3
    assert rec.checksum == "abc123"
    dumped = rec.model_dump()
    assert not (set(dumped.keys()) & FORBIDDEN_DRIFT_FIELDS)
    # Every contract key present on the wire, even when null.
    assert set(dumped.keys()) == CONTRACT_FIELDS


def test_file_record_mappers_do_not_import_on_the_event_loop():
    """Cold module loads belong at process startup, never inside a request mapper."""

    tree = ast.parse(stable_source(records_module))
    mapper_names = {"to_file_record", "to_file_record_with_urls_async"}
    mappers = [
        node
        for node in tree.body
        if isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef) and node.name in mapper_names
    ]
    assert {node.name for node in mappers} == mapper_names
    for mapper in mappers:
        assert not any(
            isinstance(node, ast.Import | ast.ImportFrom) for node in ast.walk(mapper)
        ), f"{mapper.name} imports a module while serving a request"


def test_patch_basic_path_returns_file_record():
    """A visibility/metadata-only PATCH answers with the canonical FileRecord.

    The FE derefs FileRecord fields off the PATCH response and upserts it
    into the store (thunks.ts → apiFileRecordToCloudFile); an envelope
    response here corrupts the row (`id: undefined`). Combined-op bodies /
    an X-Idempotency-Key still get the AssetCombinedOpResponse envelope.
    """
    from fastapi import FastAPI
    from fastapi.testclient import TestClient

    row = dict(_ROW)

    class _FakeSyncEngine:
        async def build_urls_for_record_async(self, record):
            return {"url": "u", "cdn_url": None, "download_url": "d"}

        class variants:  # noqa: N801 — thumbnail resolver looks up .variants
            @staticmethod
            async def list_existing_async(record):
                return {}

    class _FakeFm:
        sync_engine = _FakeSyncEngine()

    class _FakeService:
        file_manager = _FakeFm()
        calls: list[dict] = []

        async def read_record(self, file_id, *, user_id, level="read"):
            return row

        async def mutate_file(self, file_id, **kwargs):
            self.calls.append(kwargs)
            return {"asset": None, "share_link": None, "errors": []}

    svc = _FakeService()
    app = FastAPI()
    app.include_router(build_file_router(svc))
    client = TestClient(app)

    # Basic path (metadata only) → FileRecord, not the envelope.
    resp = client.patch(f"/files/{row['id']}", json={"metadata": {"tag": "y"}})
    assert resp.status_code == 200, resp.text
    data = resp.json()
    assert data["id"] == row["id"]
    assert "asset" not in data
    assert set(data.keys()) == CONTRACT_FIELDS
    # metadata_merge default rides through as merge (metadata_replace=False).
    assert svc.calls[-1]["metadata_replace"] is False

    # Replace semantics reach the primitive via ?metadata_merge=false.
    resp = client.patch(f"/files/{row['id']}?metadata_merge=false", json={"metadata": {"tag": "z"}})
    assert resp.status_code == 200, resp.text
    assert svc.calls[-1]["metadata_replace"] is True

    # Empty body → current record, still FileRecord-shaped.
    resp = client.patch(f"/files/{row['id']}", json={})
    assert resp.status_code == 200, resp.text
    assert resp.json()["id"] == row["id"]


def test_router_endpoints_declare_canonical_response_models():
    """The standalone router serves the SAME models — not a local fork."""

    class _StubService:  # never called; route table inspection only
        pass

    router = build_file_router(_StubService())
    by_path = {}
    for route in router.routes:
        methods = getattr(route, "methods", set()) or set()
        if "GET" in methods:
            by_path[route.path] = route
    assert by_path["/files/{file_id}"].response_model is FileRecord
    assert "/files/{file_id}/url" not in by_path
