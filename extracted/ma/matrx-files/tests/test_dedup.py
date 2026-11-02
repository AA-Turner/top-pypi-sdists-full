"""
Tests for the dedup module — strict-intent contract for content-hash-
based file deduplication.

Covers the three intents (``create``, ``alias_existing``,
``force_new_copy``), the checksum computation primitives, the policy
resolver, and the end-to-end ``resolve_async`` path through the REAL
``DatabaseClient`` checksum query evaluated over the captured ``files.files``
constraints (``_files_db_double``). No double owns the scope decision: a
cross-owner / cross-org / trashed / derivative / alias row is only ever
returned if the production query lets it through.
"""

from __future__ import annotations

import hashlib
import io

import pytest
from _files_db_double import FilesDB

from matrx_files.dedup import (  # noqa: E402
    DuplicateFileError,
    InvalidIntentError,
    MissingReasonError,
    UploadIntent,
    VALID_INTENTS,
    DedupLookupResult,
    coerce_intent,
    compute_checksum,
    compute_checksum_stream,
    resolve_async,
    resolve_dedup_policy,
    validate_force_new_copy_reason,
)

# SHA-256("hello world") — published test vector, independent of the SUT.
HELLO_WORLD_SHA256 = "b94d27b9934d3e08a52e52d7da7dabfac484efe37a5380ee9088f7ace2efcde9"
EMPTY_SHA256 = "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"


# ── compute_checksum ─────────────────────────────────────────────────────


def test_compute_checksum_known_vector():
    assert compute_checksum(b"hello world") == HELLO_WORLD_SHA256


def test_compute_checksum_empty():
    assert compute_checksum(b"") == EMPTY_SHA256


@pytest.mark.parametrize("wrap", [bytearray, memoryview, bytes])
def test_compute_checksum_hashes_the_payload_bytes_for_every_buffer_type(wrap):
    assert compute_checksum(wrap(b"hello world")) == HELLO_WORLD_SHA256


def test_compute_checksum_rejects_str():
    with pytest.raises(TypeError, match="requires bytes"):
        compute_checksum("hello world")  # type: ignore[arg-type]


def test_compute_checksum_stream_hashes_every_chunk_of_a_multi_buffer_payload():
    payload = b"x" * (1024 * 1024 * 2 + 17)  # > 2 MiB: three reads
    assert compute_checksum_stream(io.BytesIO(payload)) == hashlib.sha256(payload).hexdigest()


# ── coerce_intent ────────────────────────────────────────────────────────


def test_coerce_intent_strings():
    assert coerce_intent("create") is UploadIntent.CREATE
    assert coerce_intent("alias_existing") is UploadIntent.ALIAS_EXISTING
    assert coerce_intent("force_new_copy") is UploadIntent.FORCE_NEW_COPY


def test_coerce_intent_enum_passthrough():
    assert coerce_intent(UploadIntent.CREATE) is UploadIntent.CREATE


def test_coerce_intent_none_raises():
    with pytest.raises(InvalidIntentError):
        coerce_intent(None)


def test_coerce_intent_unknown_raises():
    with pytest.raises(InvalidIntentError) as exc:
        coerce_intent("upsert")
    assert "unknown intent" in str(exc.value)


def test_valid_intents_matches_enum():
    assert VALID_INTENTS == {"create", "alias_existing", "force_new_copy"}


# ── validate_force_new_copy_reason ───────────────────────────────────────


def test_reason_required():
    with pytest.raises(MissingReasonError):
        validate_force_new_copy_reason(None)
    with pytest.raises(MissingReasonError):
        validate_force_new_copy_reason("")
    with pytest.raises(MissingReasonError):
        validate_force_new_copy_reason("   ")


def test_reason_too_short():
    with pytest.raises(MissingReasonError):
        validate_force_new_copy_reason("ok")


def test_reason_strips_whitespace():
    assert validate_force_new_copy_reason("  legitimate reason  ") == ("legitimate reason")


# ── resolve_dedup_policy ─────────────────────────────────────────────────


def _no_dupe() -> DedupLookupResult:
    return DedupLookupResult(checksum=HELLO_WORLD_SHA256, existing=None, scope="none")


def _with_dupe(scope: str = "org") -> DedupLookupResult:
    return DedupLookupResult(
        checksum=HELLO_WORLD_SHA256,
        existing={
            "id": "11111111-1111-1111-1111-111111111111",
            "file_path": "documents/report.pdf",
            "created_at": "2026-05-01T00:00:00Z",
        },
        scope=scope,
    )


def test_policy_create_no_dupe_writes_new():
    decision = resolve_dedup_policy(UploadIntent.CREATE, _no_dupe(), reason=None)
    assert decision.action == "write_new"
    assert decision.canonical_file_id is None


def test_policy_create_with_dupe_raises():
    with pytest.raises(DuplicateFileError) as exc:
        resolve_dedup_policy(UploadIntent.CREATE, _with_dupe(), reason=None)
    err = exc.value
    assert err.existing_file_id == "11111111-1111-1111-1111-111111111111"
    assert err.scope == "org"
    payload = err.to_dict()
    assert payload["error"] == "duplicate_file"
    assert payload["status_code"] == 409
    assert "alias_existing" in payload["allowed_intents"]
    assert "force_new_copy" in payload["allowed_intents"]
    assert payload["existing_path"] == "documents/report.pdf"


def test_policy_alias_existing_with_dupe_returns_existing():
    decision = resolve_dedup_policy(UploadIntent.ALIAS_EXISTING, _with_dupe("org"), reason=None)
    assert decision.action == "return_existing"
    assert decision.canonical_file_id == "11111111-1111-1111-1111-111111111111"


def test_policy_alias_existing_no_dupe_writes_new():
    decision = resolve_dedup_policy(UploadIntent.ALIAS_EXISTING, _no_dupe(), reason=None)
    assert decision.action == "write_new"
    assert decision.canonical_file_id is None


def test_policy_force_new_copy_with_dupe_writes_alias():
    decision = resolve_dedup_policy(
        UploadIntent.FORCE_NEW_COPY,
        _with_dupe(),
        reason="client wants an isolated copy",
    )
    assert decision.action == "write_alias"
    assert decision.canonical_file_id == "11111111-1111-1111-1111-111111111111"
    assert decision.reason == "client wants an isolated copy"


def test_policy_force_new_copy_no_dupe_degenerates_to_write_new():
    decision = resolve_dedup_policy(
        UploadIntent.FORCE_NEW_COPY,
        _no_dupe(),
        reason="legitimate explanation",
    )
    # No dupe to alias — fall through to a normal create.
    assert decision.action == "write_new"
    assert decision.canonical_file_id is None
    # Reason still recorded in the decision.
    assert decision.reason == "legitimate explanation"


def test_policy_force_new_copy_requires_reason():
    with pytest.raises(MissingReasonError):
        resolve_dedup_policy(UploadIntent.FORCE_NEW_COPY, _with_dupe(), reason=None)


# ── End-to-end resolve_async: real DatabaseClient over the files double ──

OWNER = "owner-aaaa"
OTHER_MEMBER = "owner-bbbb"
ORG = "org-shared"
OTHER_ORG = "org-elsewhere"


@pytest.fixture
def files_db():
    db = FilesDB()
    with db.bound():
        yield db


def _seed(db: FilesDB, **overrides):
    values = {
        "created_by": OWNER,
        "organization_id": ORG,
        "file_path": "docs/hello.txt",
        "checksum": HELLO_WORLD_SHA256,
    }
    values.update(overrides)
    return db.seed_file(**values)


async def _resolve(db: FilesDB, intent: str, *, content: bytes = b"hello world", **kw):
    kw.setdefault("owner_id", OWNER)
    kw.setdefault("organization_id", ORG)
    return await resolve_async(db.client(), intent=intent, content=content, **kw)


async def test_create_refuses_when_caller_already_owns_the_content_in_that_org(files_db):
    row = _seed(files_db)

    with pytest.raises(DuplicateFileError) as exc:
        await _resolve(files_db, "create")

    assert exc.value.existing_file_id == row["id"]
    assert exc.value.existing_path == "docs/hello.txt"
    assert exc.value.scope == "org"
    assert exc.value.checksum == HELLO_WORLD_SHA256


async def test_alias_returns_the_callers_own_canonical_row(files_db):
    row = _seed(files_db)

    decision = await _resolve(files_db, "alias_existing")

    assert decision.action == "return_existing"
    assert decision.canonical_file_id == row["id"]
    assert decision.lookup.scope == "org"


async def test_hash_identity_is_over_the_uploaded_bytes(files_db):
    """A row whose stored checksum is SHA-256 of b"hello world" matches ONLY
    an upload of exactly those bytes."""
    _seed(files_db)

    hit = await _resolve(files_db, "alias_existing", content=b"hello world")
    miss = await _resolve(files_db, "alias_existing", content=b"hello world!")

    assert hit.action == "return_existing"
    assert miss.action == "write_new"


async def test_precomputed_checksum_is_the_lookup_identity(files_db):
    row = _seed(files_db)

    decision = await _resolve(
        files_db,
        "alias_existing",
        content=b"bytes already hashed upstream",
        precomputed_checksum=HELLO_WORLD_SHA256,
    )

    assert decision.canonical_file_id == row["id"]
    assert decision.lookup.checksum == HELLO_WORLD_SHA256


async def test_another_members_private_row_in_the_same_org_is_never_a_dedup_hit(files_db):
    """Cross-member reuse would hand the caller a row they cannot read."""
    _seed(files_db, created_by=OTHER_MEMBER)

    create = await _resolve(files_db, "create")
    alias = await _resolve(files_db, "alias_existing")

    assert create.action == "write_new"
    assert alias.action == "write_new"
    assert alias.canonical_file_id is None


async def test_same_owner_in_another_org_is_never_a_dedup_hit(files_db):
    _seed(files_db, organization_id=OTHER_ORG)

    decision = await _resolve(files_db, "alias_existing")

    assert decision.action == "write_new"


async def test_trashed_row_is_never_reused(files_db):
    _seed(files_db, deleted_at="2026-06-14T08:18:49Z")

    decision = await _resolve(files_db, "alias_existing")

    assert decision.action == "write_new"


@pytest.mark.parametrize(
    "lineage",
    [
        {"parent_file_id": "some-parent", "derivation_kind": "variant"},
        {"duplicate_of_file_id": "some-canonical"},
    ],
    ids=["derivative", "force-copy-alias"],
)
async def test_derivatives_and_force_copies_are_never_canonical(files_db, lineage):
    _seed(files_db, **lineage)

    decision = await _resolve(files_db, "alias_existing")

    assert decision.action == "write_new"


async def test_organization_lookup_without_owner_finds_nothing(files_db):
    """The live unique key is owner + org; an ownerless org lookup must not
    fall back to any member's row."""
    _seed(files_db)

    decision = await _resolve(files_db, "alias_existing", owner_id=None)

    assert decision.action == "write_new"


async def test_owner_only_lookup_never_matches_org_scoped_rows(files_db):
    _seed(files_db)

    decision = await _resolve(files_db, "alias_existing", organization_id=None)

    assert decision.action == "write_new"


async def test_owner_only_lookup_matches_the_owners_org_less_row(files_db):
    row = _seed(files_db, organization_id=None)

    decision = await _resolve(files_db, "alias_existing", organization_id=None)

    assert decision.canonical_file_id == row["id"]
    assert decision.lookup.scope == "owner"


async def test_force_new_copy_with_dupe_plans_an_alias_of_the_canonical(files_db):
    row = _seed(files_db)

    decision = await _resolve(
        files_db,
        "force_new_copy",
        reason="client X requires a separate version",
    )

    assert decision.action == "write_alias"
    assert decision.canonical_file_id == row["id"]
    assert decision.reason == "client X requires a separate version"


async def test_force_new_copy_missing_reason_raises(files_db):
    _seed(files_db)

    with pytest.raises(MissingReasonError):
        await _resolve(files_db, "force_new_copy", reason="")


async def test_resolve_async_unknown_intent_raises(files_db):
    with pytest.raises(InvalidIntentError):
        await _resolve(files_db, "upsert")


# ── Error envelope shape (used by HTTP layer) ───────────────────────────


def test_duplicate_file_error_envelope_has_required_fields():
    err = DuplicateFileError(
        checksum=HELLO_WORLD_SHA256,
        existing_file_id="abc",
        existing_path="foo.pdf",
        existing_created_at="2026-05-01T00:00:00Z",
        scope="org",
    )
    payload = err.to_dict()
    required = {
        "error",
        "status_code",
        "message",
        "existing_file_id",
        "existing_path",
        "existing_created_at",
        "scope",
        "checksum",
        "allowed_intents",
    }
    assert required.issubset(payload.keys())
    assert payload["status_code"] == 409


def test_prepared_share_link_generates_real_token_and_org() -> None:
    """Canonical platform.share_links insert prep: a missing token is filled
    with a 64-hex token (matching the create_share_link RPC's format) and the
    organization_id is resolved from the resource when absent."""
    from matrx_files.cloud_sync.db import DatabaseClient

    out = DatabaseClient._prepared_share_link(
        {"resource_type": "file", "resource_id": "x", "permission_level": "viewer"},
        org_id="org-123",
    )
    assert out["token"]
    assert len(out["token"]) == 64
    assert all(c in "0123456789abcdef" for c in out["token"])
    assert out["organization_id"] == "org-123"

    # an explicit token is respected
    keep = DatabaseClient._prepared_share_link({"token": "mytoken"}, org_id=None)
    assert keep["token"] == "mytoken"
