"""Forcing-function tests for the matrx-utils variant primitive.

``render_variant_async`` is the single primitive that turns
``(master_file_id, variant_key)`` into a deterministic, idempotent,
encoder-injected derived file. These tests pin two properties:

1. **Encoder injection works without matrx-ai installed.** A test-local
   encoder is registered for a fake family and the renderer must call it.
2. **Idempotency.** A second call for the same ``(master, key)`` must
   hit the cached row and NOT re-invoke the encoder. This is what makes
   the lazy ``MediaRef.vision_class`` resolver safe to call on every
   request — the cost of a hit is one DB lookup.

We use an in-memory FakeSyncEngine (DB + storage) — the system under
test (``render_variant_async``) is exercised end-to-end. Every
forcing-function check pins behavior the renderer itself must produce.
"""

from __future__ import annotations

import threading
from dataclasses import dataclass, field
from typing import Any

import pytest

from matrx_files.cloud_sync.models import SyncResult
from matrx_files.cloud_sync.variants import (
    get_variant_encoder,
    has_variant_encoder,
    register_variant_encoder,
    render_variant_async,
    variant_file_path,
)


# ---------------------------------------------------------------------------
# In-memory fakes (stub the dependencies; SUT is render_variant_async)
# ---------------------------------------------------------------------------


@dataclass
class _Row:
    id: str
    owner_id: str
    file_path: str
    storage_uri: str
    mime_type: str
    file_size: int
    published_to_web: bool = False
    shown_to: str | None = "only_me"
    metadata: dict[str, Any] = field(default_factory=dict)
    organization_id: str | None = None
    parent_file_id: str | None = None
    derivation_kind: str | None = None


class _FakeDB:
    def __init__(self) -> None:
        self.by_id: dict[str, _Row] = {}
        self.by_owner_path: dict[tuple[str, str], _Row] = {}

    async def get_file_async(self, file_id: str) -> dict | None:
        row = self.by_id.get(file_id)
        return _row_to_dict(row) if row else None

    async def get_file_by_path_async(self, owner: str, path: str) -> dict | None:
        row = self.by_owner_path.get((owner, path))
        return _row_to_dict(row) if row else None

    async def list_variants_by_master_async(self, master_file_id: str) -> list[dict]:
        # Mirrors DatabaseClient: every row whose metadata.derived_from
        # matches the master — the metadata-based variant cache probe.
        return [
            _row_to_dict(row)
            for row in self.by_id.values()
            if (row.metadata or {}).get("derived_from") == master_file_id
        ]


def _row_to_dict(row: _Row) -> dict:
    return {
        "id": row.id,
        "owner_id": row.owner_id,
        "file_path": row.file_path,
        "storage_uri": row.storage_uri,
        "mime_type": row.mime_type,
        "file_size": row.file_size,
        "published_to_web": row.published_to_web,
        "shown_to": row.shown_to,
        "metadata": row.metadata,
        "organization_id": row.organization_id,
    }


class _FakeRouter:
    def __init__(self, storage: dict[str, bytes]) -> None:
        self._storage = storage
        self.read_calls: list[str] = []

    async def read_async(self, storage_uri: str) -> bytes:
        self.read_calls.append(storage_uri)
        return self._storage[storage_uri]


class _FakeSyncEngine:
    def __init__(self) -> None:
        self._storage: dict[str, bytes] = {}
        self._db = _FakeDB()
        self._router = _FakeRouter(self._storage)
        self.write_calls: list[tuple[str, int, str | None]] = []

    # Mirror the real SyncEngine's public accessors used by render_variant_async.
    @property
    def db(self) -> _FakeDB:
        return self._db

    @property
    def router(self) -> _FakeRouter:
        return self._router

    async def build_urls_for_record_async(self, record: dict) -> dict[str, Any]:
        # Mirrors the real durable contract: three keys, no signed anything.
        file_id = record["id"]
        return {
            "url": f"https://fake.host/files/{file_id}/download?inline=1",
            "cdn_url": None,
            "download_url": f"https://fake.host/files/{file_id}/download",
        }

    async def managed_write_async(
        self,
        file_path: str,
        content: bytes,
        *,
        mime_type: str | None = None,
        published_to_web: bool | None = None,
        shown_to: str | None = None,
        user_id: str | None = None,
        metadata: dict | None = None,
        parent_file_id: str | None = None,
        derivation_kind: str | None = None,
    ) -> SyncResult:
        owner = user_id or "test-owner"
        self.write_calls.append((file_path, len(content), mime_type))
        existing = self._db.by_owner_path.get((owner, file_path))
        if existing:
            existing.storage_uri = f"s3://bucket/{file_path}"
            existing.file_size = len(content)
            existing.mime_type = mime_type or existing.mime_type
            existing.metadata = metadata or existing.metadata
            self._storage[existing.storage_uri] = content
            return SyncResult(
                file_id=existing.id,
                storage_uri=existing.storage_uri,
                version_number=2,
                file_size=existing.file_size,
                is_new=False,
                url=f"https://fake.cdn/{existing.storage_uri}",
            )
        new_id = f"fake-uuid-{len(self._db.by_id) + 1}"
        storage_uri = f"s3://bucket/{file_path}"
        row = _Row(
            id=new_id,
            owner_id=owner,
            file_path=file_path,
            storage_uri=storage_uri,
            mime_type=mime_type or "application/octet-stream",
            file_size=len(content),
            published_to_web=bool(published_to_web),
            shown_to=shown_to,
            metadata=metadata or {},
            # The fake mirrors the real engine's org channel: metadata org wins.
            organization_id=(metadata or {}).get("organization_id"),
            parent_file_id=parent_file_id,
            derivation_kind=derivation_kind,
        )
        self._db.by_id[new_id] = row
        self._db.by_owner_path[(owner, file_path)] = row
        self._storage[storage_uri] = content
        return SyncResult(
            file_id=new_id,
            storage_uri=storage_uri,
            version_number=1,
            file_size=len(content),
            is_new=True,
            url=f"https://fake.cdn/{storage_uri}",
        )


class _FakeFileManager:
    def __init__(self) -> None:
        self.sync_engine = _FakeSyncEngine()

    def _require_sync_engine(self) -> _FakeSyncEngine:
        return self.sync_engine


@pytest.fixture
def fm_with_master() -> tuple[_FakeFileManager, str, bytes]:
    fm = _FakeFileManager()
    master_bytes = b"\xff\xd8" + b"\x00" * 1000 + b"\xff\xd9"  # fake JPEG
    se = fm.sync_engine
    row = _Row(
        id="master-1",
        owner_id="user-42",
        file_path="screens/abc/master.jpg",
        storage_uri="s3://bucket/screens/abc/master.jpg",
        mime_type="image/jpeg",
        file_size=len(master_bytes),
    )
    se._db.by_id[row.id] = row
    se._db.by_owner_path[(row.owner_id, row.file_path)] = row
    se._storage[row.storage_uri] = master_bytes
    return fm, row.id, master_bytes


@pytest.fixture(autouse=True)
def _restore_encoders():
    """Snapshot/restore the encoder registry around each test."""
    from matrx_files.cloud_sync import variants as v_mod

    snapshot = dict(v_mod._ENCODERS)
    yield
    v_mod._ENCODERS.clear()
    v_mod._ENCODERS.update(snapshot)


def test_register_variant_encoder_stores_and_lookups(fm_with_master) -> None:
    """A registered encoder is reachable through the public lookup API."""
    fm, _, _ = fm_with_master

    def _enc(master: bytes, key: str) -> tuple[bytes, str]:
        return b"out", "image/jpeg"

    register_variant_encoder("test_family", _enc)
    assert has_variant_encoder("test_family")
    assert get_variant_encoder("test_family") is _enc


@pytest.mark.asyncio
async def test_render_variant_invokes_injected_encoder_on_miss(fm_with_master) -> None:
    """Cache miss must call the encoder exactly once with the master bytes
    and the variant key. The encoder return value must shape the row."""
    fm, master_id, master_bytes = fm_with_master
    calls: list[tuple[bytes, str]] = []

    def _enc(master: bytes, key: str) -> tuple[bytes, str]:
        calls.append((master, key))
        return b"X" * 42, "image/jpeg"

    register_variant_encoder("vision", _enc)

    info = await render_variant_async(
        fm, master_id, variant_key="anthropic_opus_hires", family="vision"
    )

    assert calls == [(master_bytes, "anthropic_opus_hires")]
    assert info["is_new"] is True
    assert info["mime_type"] == "image/jpeg"
    assert info["size_bytes"] == 42
    assert info["file_path"] == "screens/abc/v/master-1/anthropic_opus_hires.jpg"
    assert info["metadata"] == {
        "derived_from": master_id,
        "variant_family": "vision",
        "variant_key": "anthropic_opus_hires",
    }


@pytest.mark.asyncio
async def test_render_variant_is_idempotent(fm_with_master) -> None:
    """Second call for the same (master, key) hits the cached row. The
    encoder must NOT be invoked the second time — that's the cache. The
    forcing function: if idempotency breaks, encoder call count is 2."""
    fm, master_id, _ = fm_with_master
    calls: list[str] = []

    def _enc(master: bytes, key: str) -> tuple[bytes, str]:
        calls.append(key)
        return b"X" * 99, "image/jpeg"

    register_variant_encoder("vision", _enc)

    info1 = await render_variant_async(
        fm, master_id, variant_key="anthropic_sonnet_default", family="vision"
    )
    info2 = await render_variant_async(
        fm, master_id, variant_key="anthropic_sonnet_default", family="vision"
    )

    assert len(calls) == 1, f"encoder invoked {len(calls)} times — expected 1"
    assert info1["file_id"] == info2["file_id"]
    assert info1["is_new"] is True
    assert info2["is_new"] is False
    # Storage write count: the second call must NOT have written.
    write_paths = [c[0] for c in fm.sync_engine.write_calls]
    assert write_paths.count("screens/abc/v/master-1/anthropic_sonnet_default.jpg") == 1


@pytest.mark.asyncio
async def test_render_variant_different_keys_render_independently(fm_with_master) -> None:
    fm, master_id, _ = fm_with_master
    calls: list[str] = []

    def _enc(master: bytes, key: str) -> tuple[bytes, str]:
        calls.append(key)
        return b"Y" * 17, "image/jpeg"

    register_variant_encoder("vision", _enc)

    a = await render_variant_async(fm, master_id, variant_key="openai_high", family="vision")
    b = await render_variant_async(fm, master_id, variant_key="openai_low", family="vision")

    assert calls == ["openai_high", "openai_low"]
    assert a["file_id"] != b["file_id"]
    assert a["file_path"].endswith("openai_high.jpg")
    assert b["file_path"].endswith("openai_low.jpg")


@pytest.mark.asyncio
async def test_two_masters_in_same_directory_render_distinct_variants(
    fm_with_master,
) -> None:
    """THE grader-bug regression (end-to-end). Two DIFFERENT masters uploaded
    into the SAME directory (like every photo landing in
    ``system-files/image-grade/responses/``) must each get their OWN variant —
    the encoder runs per master and the two variant file_ids differ. Before the
    fix, master B path-hit master A's variant and was served A's bytes."""
    fm, master_a, _ = fm_with_master
    se = fm.sync_engine

    # A second master in the SAME directory as master A ("screens/abc/").
    other_bytes = b"\xff\xd8" + b"\x11" * 500 + b"\xff\xd9"
    row_b = _Row(
        id="master-2",
        owner_id="user-42",
        file_path="screens/abc/other.jpg",  # same dir, different file
        storage_uri="s3://bucket/screens/abc/other.jpg",
        mime_type="image/jpeg",
        file_size=len(other_bytes),
    )
    se._db.by_id[row_b.id] = row_b
    se._db.by_owner_path[(row_b.owner_id, row_b.file_path)] = row_b
    se._storage[row_b.storage_uri] = other_bytes

    seen: list[bytes] = []

    def _enc(master: bytes, key: str) -> tuple[bytes, str]:
        seen.append(master)
        # Encode distinctly per master so a collision would be observable.
        return b"ENC:" + master[:4], "image/jpeg"

    register_variant_encoder("vision", _enc)

    info_a = await render_variant_async(
        fm, master_a, variant_key="gemini25_default", family="vision"
    )
    info_b = await render_variant_async(
        fm, row_b.id, variant_key="gemini25_default", family="vision"
    )

    assert len(seen) == 2, "encoder must run once PER master, not be short-circuited"
    assert info_a["file_id"] != info_b["file_id"], "distinct masters => distinct variants"
    assert info_a["file_path"] == "screens/abc/v/master-1/gemini25_default.jpg"
    assert info_b["file_path"] == "screens/abc/v/master-2/gemini25_default.jpg"
    assert info_a["metadata"]["derived_from"] == master_a
    assert info_b["metadata"]["derived_from"] == row_b.id


@pytest.mark.asyncio
async def test_render_variant_never_serves_other_masters_bytes(fm_with_master) -> None:
    """A variant derived from a DIFFERENT master must never be served for this
    one. The metadata-based cache probe queries ``metadata.derived_from ==
    master_file_id`` directly, so a wrong-master row (the old shared-path
    collision bug that graded every photo as the first image) is structurally
    unreachable — the probe misses and a fresh, correctly-derived variant is
    rendered. Simulated by planting a variant row at the exact path this master
    would compute, but tagged as derived from a different master."""
    fm, master_id, _ = fm_with_master
    se = fm.sync_engine
    register_variant_encoder("vision", lambda b, k: (b"CORRECT", "image/jpeg"))

    # Plant a poisoned variant at the master-scoped path but derived from someone else.
    poisoned_path = f"screens/abc/v/{master_id}/gemini25_default.jpg"
    poisoned = _Row(
        id="poison-1",
        owner_id="user-42",
        file_path=poisoned_path,
        storage_uri="s3://bucket/poison",
        mime_type="image/jpeg",
        file_size=3,
        metadata={"derived_from": "SOMEONE-ELSE", "variant_key": "gemini25_default"},
    )
    se._db.by_id[poisoned.id] = poisoned
    se._db.by_owner_path[(poisoned.owner_id, poisoned_path)] = poisoned
    se._storage[poisoned.storage_uri] = b"BAD"

    info = await render_variant_async(
        fm, master_id, variant_key="gemini25_default", family="vision"
    )

    # Re-render with the CORRECT bytes + corrected derived_from — never the
    # poisoned (wrong-master) bytes. (The write upserts by path, so the
    # poisoned row is healed in place rather than duplicated.)
    assert info["size_bytes"] == len(b"CORRECT")
    assert info["metadata"]["derived_from"] == master_id


@pytest.mark.asyncio
async def test_render_variant_raises_when_no_encoder_registered(fm_with_master) -> None:
    fm, master_id, _ = fm_with_master
    # No encoder registered for "missing_family"
    assert not has_variant_encoder("missing_family")
    with pytest.raises(RuntimeError, match="no variant encoder registered"):
        await render_variant_async(
            fm, master_id, variant_key="anything", family="missing_family"
        )


@pytest.mark.asyncio
async def test_render_variant_raises_for_unknown_master(fm_with_master) -> None:
    fm, _, _ = fm_with_master
    register_variant_encoder("vision", lambda b, k: (b"x", "image/jpeg"))
    with pytest.raises(FileNotFoundError):
        await render_variant_async(
            fm, "no-such-master-id", variant_key="anthropic_opus_hires", family="vision"
        )


@pytest.mark.asyncio
async def test_render_variant_uses_explicit_encoder_override(fm_with_master) -> None:
    """The ``encoder=`` kwarg overrides the family-registered one. Useful
    for one-off renders without polluting the registry."""
    fm, master_id, _ = fm_with_master
    register_variant_encoder("vision", lambda b, k: (b"WRONG", "image/jpeg"))

    def _override(master: bytes, key: str) -> tuple[bytes, str]:
        return b"OVERRIDDEN", "image/png"

    info = await render_variant_async(
        fm,
        master_id,
        variant_key="custom_key",
        family="vision",
        encoder=_override,
    )
    assert info["size_bytes"] == len(b"OVERRIDDEN")
    assert info["mime_type"] == "image/png"
    assert info["file_path"].endswith("custom_key.png")


@pytest.mark.asyncio
async def test_render_variant_supports_async_encoder(fm_with_master) -> None:
    fm, master_id, _ = fm_with_master

    async def _async_enc(master: bytes, key: str) -> tuple[bytes, str]:
        return b"ASYNC", "image/webp"

    register_variant_encoder("vision", _async_enc)
    info = await render_variant_async(
        fm, master_id, variant_key="async_test", family="vision"
    )
    assert info["mime_type"] == "image/webp"
    assert info["file_path"].endswith("async_test.webp")


@pytest.mark.asyncio
async def test_render_variant_runs_sync_encoder_off_event_loop(fm_with_master) -> None:
    fm, master_id, _ = fm_with_master
    loop_thread_id = threading.get_ident()
    encoder_thread_ids: list[int] = []

    def _sync_enc(master: bytes, key: str) -> tuple[bytes, str]:
        encoder_thread_ids.append(threading.get_ident())
        return b"SYNC", "image/jpeg"

    register_variant_encoder("vision", _sync_enc)
    info = await render_variant_async(
        fm, master_id, variant_key="sync_thread_test", family="vision"
    )

    assert info["mime_type"] == "image/jpeg"
    assert encoder_thread_ids and encoder_thread_ids[0] != loop_thread_id


def test_variant_file_path_is_deterministic() -> None:
    """The variant path is derived from the master path, the master's file_id,
    and the key. A regression here would silently leak variants into the wrong
    folder — or worse, collide two masters onto one variant (the grader bug)."""
    assert (
        variant_file_path(
            "screens/abc/master.jpg", "anthropic_opus_hires", "jpg", "MID"
        )
        == "screens/abc/v/MID/anthropic_opus_hires.jpg"
    )
    assert variant_file_path("master.jpg", "k", "jpg", "MID") == "v/MID/k.jpg"
    assert (
        variant_file_path("a/b/c/d/master.png", "openai_high", "webp", "MID")
        == "a/b/c/d/v/MID/openai_high.webp"
    )


def test_variant_file_path_is_master_scoped_across_shared_directory() -> None:
    """THE regression guard for the Education grader bug: two DIFFERENT masters
    that share ONE directory must produce DIFFERENT variant paths. Before the
    fix, both mapped to ``<dir>/v/<key>.<ext>`` and the second silently served
    the first's bytes."""
    p1 = variant_file_path("responses/imgA.jpg", "gemini25_default", "jpg", "id-A")
    p2 = variant_file_path("responses/imgB.jpg", "gemini25_default", "jpg", "id-B")
    assert p1 != p2, "shared-directory masters must not collide on one variant"
    assert p1 == "responses/v/id-A/gemini25_default.jpg"
    assert p2 == "responses/v/id-B/gemini25_default.jpg"


# ---------------------------------------------------------------------------
# Derived-file access-context inheritance (FOUND_DEFECTS E-ii regression)
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_variant_of_crawl_artifact_inherits_access_context(fm_with_master) -> None:
    """A variant of a web-crawl artifact must inherit the master's ACCESS
    CONTEXT: web lane and list filter, organization (master org, never the writer's
    personal org), and the contextual policy tags the DB access policy keys
    on (system_artifact / artifact_domain / web_site_id / crawl_session_id).
    Before the fix the vision variant of a crawl screenshot was written
    untagged in the wrong org, so every non-creator org member 403'd on it."""
    fm, master_id, _ = fm_with_master
    se = fm.sync_engine
    master = se._db.by_id[master_id]
    master.published_to_web = True
    master.shown_to = "my_team"
    master.organization_id = "org-77"
    master.metadata = {
        "system_artifact": True,
        "system_immutable": True,
        "artifact_domain": "web_crawl",
        "artifact_kind": "screenshot:full_page",
        "web_site_id": "site-9",
        "crawl_session_id": "sess-3",
        "capture_id": "cap-1",
    }

    register_variant_encoder("vision", lambda b, k: (b"V" * 10, "image/jpeg"))
    info = await render_variant_async(
        fm, master_id, variant_key="gemini25_default", family="vision"
    )

    vrow = se._db.by_id[info["file_id"]]
    assert vrow.published_to_web is True
    assert vrow.shown_to == "my_team"
    md = vrow.metadata
    assert md["system_artifact"] is True
    assert md["artifact_domain"] == "web_crawl"
    assert md["web_site_id"] == "site-9"
    assert md["crawl_session_id"] == "sess-3"
    assert md["capture_id"] == "cap-1"
    # Master org via the metadata org channel — never the writer's personal org.
    assert md["organization_id"] == "org-77"
    # Derived output is re-renderable, not canonical evidence.
    assert "system_immutable" not in md
    # The variant's own identity keys always survive inheritance.
    assert md["derived_from"] == master_id
    assert md["variant_family"] == "vision"
    assert md["variant_key"] == "gemini25_default"
    # Native lineage columns identify the row by data shape.
    assert vrow.parent_file_id == master_id
    assert vrow.derivation_kind == "variant"


@pytest.mark.asyncio
async def test_variant_of_plain_file_gets_no_phantom_tags(fm_with_master) -> None:
    """Inheritance must not invent policy tags on a variant of an ordinary
    (non-crawl) master — only forward what the master actually carries."""
    fm, master_id, _ = fm_with_master
    register_variant_encoder("vision", lambda b, k: (b"V" * 10, "image/jpeg"))
    info = await render_variant_async(
        fm, master_id, variant_key="gemini25_default", family="vision"
    )
    md = fm.sync_engine._db.by_id[info["file_id"]].metadata
    assert "system_artifact" not in md
    assert "artifact_domain" not in md
    assert "organization_id" not in md  # fixture master carries no org
