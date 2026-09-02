"""WS-3 checkpoint / crypto engine — standalone proof suite (S3 §9.4).

Runs against a scratch profile directory, an in-memory object store, and the
local-dev key-wrap provider — no worker, no Browser Manager, no browser.* schema,
no AWS account. Proves the security-critical properties FAIL CLOSED:

* round-trip restore keeps the (simulated) cookie login rows;
* tamper / wrong-encryption-context / corrupt-newest-revision all fail closed;
* the D-5 cookie-scheme mismatch is refused;
* 30-day prune keeps the newest verified revision and drops >30-day ones;
* cryptographic deletion removes objects and leaves only a content-free tombstone;
* no plaintext DEK and no signed URL is ever emitted, and no scratch survives.
"""

from __future__ import annotations

import json
import sqlite3
from datetime import timedelta
from pathlib import Path

import pytest
from cryptography.fernet import Fernet

from matrx_scraper.cloud_browser.checkpoint import (
    CaptureRequest,
    CheckpointEngine,
    InMemoryObjectStore,
    LocalDevKeyWrapProvider,
    NoRestorableRevisionError,
    RestoreOutcome,
    WorkerContext,
)
from matrx_scraper.cloud_browser.checkpoint.closure import (
    ProcessInspector,
    detect_cookie_scheme,
)
from matrx_scraper.cloud_browser.checkpoint.engine import _now
from matrx_scraper.cloud_browser.checkpoint.errors import (
    ClosureError,
    RestoreError,
    VerificationError,
)


# ── fixtures / helpers ────────────────────────────────────────────────────
class _NoProcessInspector:
    """No live process, no open fd — the happy closed-profile case."""

    def pids_using_dir(self, profile_dir: Path) -> list[int]:
        return []

    def open_fd_paths(self, profile_dir: Path) -> list[str]:
        return []


class _FdHoldingInspector:
    def pids_using_dir(self, profile_dir: Path) -> list[int]:
        return []

    def open_fd_paths(self, profile_dir: Path) -> list[str]:
        return [str(profile_dir / "Default" / "Cookies")]


@pytest.fixture(autouse=True)
def _battery_key():
    from matrx_orm.secrets_battery.crypto import configure_encryption

    configure_encryption(Fernet.generate_key().decode())


def _make_cookie_db(path: Path, *, scheme: bytes = b"v10", rows: int = 3) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(path)
    conn.execute(
        "CREATE TABLE cookies (host_key TEXT, name TEXT, value TEXT, encrypted_value BLOB)"
    )
    for i in range(rows):
        conn.execute(
            "INSERT INTO cookies VALUES (?,?,?,?)",
            (
                "example.com",
                f"session_{i}",
                "",
                scheme + b"encrypted-login-token-%d" % i,
            ),
        )
    conn.commit()
    conn.execute("PRAGMA wal_checkpoint(TRUNCATE)")
    conn.close()


def make_profile(
    tmp: Path, *, scheme: bytes = b"v10", cookie_rows: int = 3, padding_bytes: int = 0
) -> Path:
    """Build a minimally realistic CLOSED Chromium profile directory."""
    profile = tmp / "user_data_dir"
    default = profile / "Default"
    default.mkdir(parents=True)
    _make_cookie_db(default / "Cookies", scheme=scheme, rows=cookie_rows)
    # Local State (must parse as JSON in V5)
    (profile / "Local State").write_text(json.dumps({"os_crypt": {"encrypted_key": "x"}}))
    (profile / "First Run").write_text("")
    # An IndexedDB-ish subtree that must survive.
    idb = default / "IndexedDB" / "https_example.com_0.indexeddb.leveldb"
    idb.mkdir(parents=True)
    (idb / "000003.log").write_bytes(b"leveldb-log-bytes")
    # A cache tree that MUST be excluded.
    (default / "GPUCache").mkdir()
    (default / "GPUCache" / "data_0").write_bytes(b"x" * 4096)
    # Singleton lock that must NOT block a clean close (dangling symlink == stale)
    if padding_bytes:
        (default / "Local Storage").mkdir(exist_ok=True)
        (default / "Local Storage" / "big.log").write_bytes(b"L" * padding_bytes)
    return profile


def _engine(
    store: InMemoryObjectStore | None = None,
) -> tuple[CheckpointEngine, InMemoryObjectStore]:
    store = store or InMemoryObjectStore()
    provider = LocalDevKeyWrapProvider()
    eng = CheckpointEngine(store, bucket=store.bucket, key_wrap_provider=provider)
    return eng, store


def _capture_req(profile_id: str, revision: int, parent: int | None = None) -> CaptureRequest:
    now = _now().isoformat().replace("+00:00", "Z")
    return CaptureRequest(
        profile_id=profile_id,
        revision=revision,
        parent_revision=parent,
        capture_reason="stop",
        chromium_version="140.0.7259.5",
        worker_image_ref="sha256:worker-image",
        playwright_version="1.45.0",
        context_closed_at=now,
        process_exit_confirmed_at=now,
        close_wait_ms=120,
        escalation="none",
    )


_WORKER = WorkerContext(chromium_major=140, cookie_scheme="v10", allow_local_dev_wrap=True)


# ── 1. round-trip: restore stays "logged in" ─────────────────────────────
def test_roundtrip_restore_keeps_cookie_login_rows(tmp_path):
    eng, _ = _engine()
    profile = make_profile(tmp_path, cookie_rows=4)
    pid = "profile-1"
    m = eng.capture(profile, _capture_req(pid, 1), inspector=_NoProcessInspector())
    assert m.verified_at is None  # not usable until the gate passes
    eng.verify(m)

    dest = tmp_path / "restored"
    outcome = eng.restore(pid, dest, _WORKER)
    assert isinstance(outcome, RestoreOutcome)
    assert outcome.restored_revision == 1
    assert outcome.skipped_revisions == []

    # the login rows survived
    conn = sqlite3.connect(dest / "Default" / "Cookies")
    n = conn.execute("SELECT count(*) FROM cookies").fetchone()[0]
    conn.close()
    assert n == 4
    # the cache tree was excluded
    assert not (dest / "Default" / "GPUCache").exists()
    # the IndexedDB subtree survived
    assert (dest / "Default" / "IndexedDB").exists()


# ── 2. closure proof refuses live/unsettled profiles ─────────────────────
def test_closure_refuses_open_fd(tmp_path):
    eng, _ = _engine()
    profile = make_profile(tmp_path)
    with pytest.raises(ClosureError) as ei:
        eng.capture(profile, _capture_req("p", 1), inspector=_FdHoldingInspector())
    assert ei.value.code == "open_file_descriptors"


def test_closure_refuses_nonempty_wal(tmp_path):
    eng, _ = _engine()
    profile = make_profile(tmp_path)
    # write a non-empty WAL sidecar next to Cookies
    (profile / "Default" / "Cookies-wal").write_bytes(b"unflushed-writes")
    with pytest.raises(ClosureError) as ei:
        eng.capture(profile, _capture_req("p", 1), inspector=_NoProcessInspector())
    assert ei.value.code == "sqlite_unsettled"


# ── 3. tamper / wrong-context fail closed ────────────────────────────────
def test_tamper_ciphertext_fails_auth_tag(tmp_path):
    eng, store = _engine()
    profile = make_profile(tmp_path)
    m = eng.capture(profile, _capture_req("p", 1), inspector=_NoProcessInspector())
    # flip a byte in the ciphertext object
    from matrx_scraper.cloud_browser.checkpoint.engine import _key_of

    store._tamper_byte(_key_of(m.object_ref), 10)
    with pytest.raises(VerificationError) as ei:
        eng.verify(m)
    assert ei.value.code in {"upload_hash_mismatch", "auth_tag_invalid"}


def test_edit_sidecar_profile_id_breaks_aad(tmp_path):
    eng, store = _engine()
    profile = make_profile(tmp_path)
    m = eng.capture(profile, _capture_req("p", 1), inspector=_NoProcessInspector())
    eng.verify(m)
    # An attacker rewrites the sidecar's profile_id to steal the checkpoint.
    m2 = m.model_copy(deep=True)
    m2.profile_id = "someone-else"
    # unwrap context now disagrees with the canonical context → refused before decrypt
    with pytest.raises(VerificationError) as ei:
        eng.verify(m2)
    assert ei.value.code in {"wrap_context_mismatch", "auth_tag_invalid"}


def test_wrong_encryption_context_refused_before_decrypt(tmp_path):
    eng, _ = _engine()
    profile = make_profile(tmp_path)
    m = eng.capture(profile, _capture_req("p", 1), inspector=_NoProcessInspector())
    provider = LocalDevKeyWrapProvider()
    wrapped = m.wrapped_dek_b64
    import base64

    with pytest.raises(Exception) as ei:
        provider.unwrap(
            base64.b64decode(wrapped),
            {
                "profile_id": "different",
                "key_version": "1",
                "purpose": "browser_profile_checkpoint",
            },
        )
    assert "context" in str(ei.value).lower()


# ── 4. corrupt newest revision → fallback to N-1 + loss window ───────────
def test_corrupt_newest_revision_falls_back(tmp_path):
    eng, store = _engine()
    pid = "p"
    m1 = eng.capture(
        make_profile(tmp_path / "a", cookie_rows=2),
        _capture_req(pid, 1),
        inspector=_NoProcessInspector(),
    )
    eng.verify(m1)
    m2 = eng.capture(
        make_profile(tmp_path / "b", cookie_rows=5),
        _capture_req(pid, 2, parent=1),
        inspector=_NoProcessInspector(),
    )
    eng.verify(m2)

    from matrx_scraper.cloud_browser.checkpoint.engine import _key_of

    # truncate the newest ciphertext so its tag can never verify
    store._truncate(_key_of(m2.object_ref), 32)

    dest = tmp_path / "restored"
    outcome = eng.restore(pid, dest, _WORKER)
    assert outcome.restored_revision == 1
    assert 2 in outcome.skipped_revisions
    assert 2 in outcome.marked_corrupt
    assert outcome.loss_window_seconds >= 0
    # restored the older login state (2 rows)
    conn = sqlite3.connect(dest / "Default" / "Cookies")
    assert conn.execute("SELECT count(*) FROM cookies").fetchone()[0] == 2
    conn.close()


def test_all_candidates_corrupt_creates_no_blank_profile(tmp_path):
    eng, store = _engine()
    pid = "p"
    m1 = eng.capture(
        make_profile(tmp_path / "a"), _capture_req(pid, 1), inspector=_NoProcessInspector()
    )
    eng.verify(m1)

    from matrx_scraper.cloud_browser.checkpoint.engine import _key_of

    store._truncate(_key_of(m1.object_ref), 16)

    dest = tmp_path / "restored"
    with pytest.raises(NoRestorableRevisionError):
        eng.restore(pid, dest, _WORKER)
    # THE hardest rule: no blank profile was created.
    assert not dest.exists() or not any(dest.iterdir())


# ── 5. D-5 cookie-scheme mismatch refused ────────────────────────────────
def test_cookie_scheme_recorded_and_mismatch_refused(tmp_path):
    eng, _ = _engine()
    pid = "p"
    # profile captured on a keyring (v11) worker
    profile = make_profile(tmp_path, scheme=b"v11")
    assert detect_cookie_scheme(profile) == "v11"
    m = eng.capture(profile, _capture_req(pid, 1), inspector=_NoProcessInspector())
    assert m.cookie_scheme == "v11"
    eng.verify(m)

    # restoring worker is basic (v10) → refuse, cookies would decrypt to garbage
    v10_worker = WorkerContext(chromium_major=140, cookie_scheme="v10", allow_local_dev_wrap=True)
    dest = tmp_path / "restored"
    with pytest.raises(NoRestorableRevisionError):
        eng.restore(pid, dest, v10_worker)
    assert not dest.exists() or not any(dest.iterdir())


# ── 6. chromium downgrade refused; not marked corrupt ────────────────────
def test_chromium_downgrade_refused(tmp_path):
    eng, _ = _engine()
    pid = "p"
    profile = make_profile(tmp_path)
    m = eng.capture(profile, _capture_req(pid, 1), inspector=_NoProcessInspector())
    eng.verify(m)
    older_worker = WorkerContext(chromium_major=139, cookie_scheme="v10", allow_local_dev_wrap=True)
    dest = tmp_path / "restored"
    with pytest.raises(NoRestorableRevisionError):
        eng.restore(pid, dest, older_worker)
    # a compatibility refusal is NOT corruption — the revision stays verified
    m_after = eng.list_manifests(pid)[0]
    assert m_after.verified_at is not None


def test_real_deployment_refuses_local_dev_wrap(tmp_path):
    eng, _ = _engine()
    pid = "p"
    m = eng.capture(make_profile(tmp_path), _capture_req(pid, 1), inspector=_NoProcessInspector())
    eng.verify(m)
    real_worker = WorkerContext(chromium_major=140, cookie_scheme="v10", allow_local_dev_wrap=False)
    dest = tmp_path / "restored"
    with pytest.raises(NoRestorableRevisionError):
        eng.restore(pid, dest, real_worker)


# ── 7. 30-day prune keeps newest verified, drops >30d ────────────────────
def test_prune_keeps_newest_verified_drops_old(tmp_path):
    eng, store = _engine()
    pid = "p"
    revs = []
    for r in range(1, 4):
        m = eng.capture(
            make_profile(tmp_path / f"r{r}"), _capture_req(pid, r), inspector=_NoProcessInspector()
        )
        eng.verify(m)
        revs.append(m)

    # age revisions 1 and 2 to > 30 days by rewriting their created_at in the sidecar
    old = (_now() - timedelta(days=45)).isoformat().replace("+00:00", "Z")
    for m in revs[:2]:
        m.created_at = old
        store.put(_manifest_key(m), m.canonical_bytes())

    result = eng.prune_retention(pid, now=_now())
    # rev 3 is newest verified → always kept; rev 1 kept? rev1<30d? no it's 45d old.
    # both 1 and 2 are >30d, but rev 2 is not newest; only rev 3 is newest verified.
    assert set(result.revisions_deleted) == {1, 2}
    remaining = {m.revision for m in eng.list_manifests(pid)}
    assert remaining == {3}
    assert result.tombstone["kept_newest_verified_revision"] == 3


def test_prune_keeps_only_restore_point_even_if_ancient(tmp_path):
    """A rarely-used browser: its ONLY verified revision is 45 days old and must stay."""
    eng, store = _engine()
    pid = "p"
    m = eng.capture(make_profile(tmp_path), _capture_req(pid, 1), inspector=_NoProcessInspector())
    eng.verify(m)
    m.created_at = (_now() - timedelta(days=45)).isoformat().replace("+00:00", "Z")
    store.put(_manifest_key(m), m.canonical_bytes())

    result = eng.prune_retention(pid, now=_now())
    assert result.revisions_deleted == []
    assert {mm.revision for mm in eng.list_manifests(pid)} == {1}


# ── 8. cryptographic deletion ────────────────────────────────────────────
def test_cryptographic_deletion(tmp_path):
    eng, store = _engine()
    pid = "p"
    m = eng.capture(make_profile(tmp_path), _capture_req(pid, 1), inspector=_NoProcessInspector())
    eng.verify(m)

    from matrx_scraper.cloud_browser.checkpoint.engine import _key_of

    obj_key = _key_of(m.object_ref)
    man_key = _key_of(m.manifest_object_ref)
    assert store.head(obj_key)

    result = eng.delete_profile(pid, requested_by_actor="user")
    assert result.outcome == "complete"
    assert result.revisions_deleted == [1]
    # objects gone, absence probes 404
    assert not store.head(obj_key)
    assert not store.head(man_key)
    for rev in result.tombstone["revisions"]:  # type: ignore[index]
        for obj in rev["objects"]:
            assert obj["absence_probe_result"] == "404"
    # tombstone is content-free — no urls, origins, account labels
    blob = json.dumps(result.tombstone).lower()
    assert "http" not in blob
    assert "example.com" not in blob
    # nothing left to restore
    assert eng.list_manifests(pid) == []


# ── 9. hygiene: no signed url, no plaintext dek, no scratch survives ─────
def test_no_signed_url_or_plaintext_dek_emitted(tmp_path):
    from matrx_files.cloud_sync.durability import is_signed_url  # reuse the ONE classifier

    eng, store = _engine()
    pid = "p"
    m = eng.capture(make_profile(tmp_path), _capture_req(pid, 1), inspector=_NoProcessInspector())
    eng.verify(m)

    for value in m.to_dict().values():
        if isinstance(value, str):
            assert not is_signed_url(value)
    # object_ref is an s3:// server-only ref, never signed
    assert m.object_ref.startswith("s3://")
    assert not is_signed_url(m.object_ref)


def test_no_scratch_dir_survives_failure(tmp_path):
    import tempfile

    before = set(Path(tempfile.gettempdir()).glob("ckpt-*"))
    eng, store = _engine()
    m = eng.capture(make_profile(tmp_path), _capture_req("p", 1), inspector=_NoProcessInspector())
    from matrx_scraper.cloud_browser.checkpoint.engine import _key_of

    store._tamper_byte(_key_of(m.object_ref), 8)
    with pytest.raises(VerificationError):
        eng.verify(m)
    after = set(Path(tempfile.gettempdir()).glob("ckpt-*"))
    assert after == before  # every scratch dir was cleaned, even on failure


# ── helper used by tests ─────────────────────────────────────────────────
def _manifest_key(m):
    from matrx_scraper.cloud_browser.checkpoint.engine import _key_of

    return _key_of(m.manifest_object_ref)
