"""The checkpoint engine — capture, verify, restore (+ last-verified fallback),
cryptographic deletion, and 30-day retention pruning (S3 §3–§8, D-20).

This is a PURE library: it reaches no worker, no Browser Manager, and no
``browser.*`` database schema. Its source of truth is the object store and the
self-describing sidecar manifests (S3 §7.5, database-less recovery) — the control
plane owns the ``browser.profile_checkpoint`` rows and the ``is_current`` CAS, and
mirrors what this engine returns.

Every secret (DEK, plaintext archive, extracted profile) lives only in a temp
directory removed in a ``finally``; the DEK is zeroized. A test asserts no scratch
survives any path, including failures, and that no signed URL is ever emitted.
"""

from __future__ import annotations

import base64
import json
import logging
import secrets
import shutil
import sqlite3
import tempfile
import time
from dataclasses import dataclass, field
from datetime import datetime, timedelta, UTC
from pathlib import Path

from matrx_orm import check_local_sqlite_integrity

from .archive import (
    ArchiveResult,
    archive_profile,
    assert_expected_members,
    extract_archive,
)
from .closure import ProcessInspector, detect_cookie_scheme, prove_closed
from .constants import (
    ARCHIVE_FORMAT,
    CONTENT_CIPHER,
    DEK_BYTES,
    ENCRYPTION_PURPOSE,
    GCM_NONCE_BYTES,
    KEY_VERSION,
    MANIFEST_VERSION,
    MAX_FALLBACK_CANDIDATES,
    PROFILE_FORMAT_VERSION,
    RETENTION_DAYS,
    SUPPORTED_ARCHIVE_FORMATS,
    SUPPORTED_COOKIE_SCHEMES,
    SUPPORTED_MANIFEST_VERSIONS,
)
from .crypto import decrypt_stream_to_file, encrypt_archive, zeroize
from .errors import (
    CheckpointError,
    NoRestorableRevisionError,
    RestoreError,
    VerificationError,
)
from .key_wrap import KeyWrapProvider, get_key_wrap_provider
from .manifest import (
    CheckpointManifest,
    ClosureProof,
    FailureBlock,
    VerificationBlock,
)
from .object_store import ObjectStore

logger = logging.getLogger(__name__)

_VERIFICATION_CHECKS = [
    "upload_hash",
    "dek_unwrap",
    "auth_tag",
    "archive_probe",
    "profile_probe",
]


def _now() -> datetime:
    return datetime.now(UTC)


def _iso(dt: datetime) -> str:
    return dt.isoformat().replace("+00:00", "Z")


def _b64(data: bytes) -> str:
    return base64.b64encode(data).decode("ascii")


def _unb64(s: str) -> bytes:
    return base64.b64decode(s)


def _encryption_context(profile_id: str) -> dict[str, str]:
    return {
        "profile_id": str(profile_id),
        "key_version": KEY_VERSION,
        "purpose": ENCRYPTION_PURPOSE,
    }


@dataclass(frozen=True)
class WorkerContext:
    """The restoring/capturing worker's compatibility facts (S3 §6, D-5)."""

    chromium_major: int
    cookie_scheme: str
    max_profile_format_version: int = PROFILE_FORMAT_VERSION
    allow_local_dev_wrap: bool = False  # R9: real deployments set this False


@dataclass(frozen=True)
class CaptureRequest:
    profile_id: str
    revision: int
    parent_revision: int | None
    capture_reason: str
    chromium_version: str
    worker_image_ref: str
    playwright_version: str
    # closure evidence (check 1 — worker's record of the shutdown it performed)
    context_closed_at: str
    process_exit_confirmed_at: str
    close_wait_ms: int
    escalation: str = "none"
    retention_expires_at: str | None = None


@dataclass
class RestoreOutcome:
    restored_revision: int
    requested_revision: int | None
    skipped_revisions: list[int]
    loss_window_from: str | None
    loss_window_to: str | None
    loss_window_seconds: int
    marked_corrupt: list[int] = field(default_factory=list)


@dataclass
class DeletionOutcome:
    profile_id: str
    revisions_deleted: list[int]
    tombstone: dict[str, object]
    outcome: str  # complete | partial_retryable | partial_manual


class CheckpointEngine:
    """Envelope-encrypted profile checkpointing over an injected object store and
    key-wrap provider."""

    def __init__(
        self,
        object_store: ObjectStore,
        *,
        bucket: str,
        key_wrap_provider: KeyWrapProvider | None = None,
        verifier_image_ref: str = "sha256:local-dev-verifier",
    ) -> None:
        self.store = object_store
        self.bucket = bucket
        self.provider = key_wrap_provider or get_key_wrap_provider()
        self.verifier_image_ref = verifier_image_ref

    # ── object key shape (S3 §2.3) ──────────────────────────────────────
    def _prefix(self, profile_id: str) -> str:
        return f"profiles/{profile_id}/"

    def _object_key(self, profile_id: str, revision: int, checkpoint_id: str) -> str:
        return f"profiles/{profile_id}/{revision:010d}/{checkpoint_id}.bin"

    def _manifest_key(self, object_key: str) -> str:
        return f"{object_key}.manifest.json"

    def _uri(self, key: str) -> str:
        return f"s3://{self.bucket}/{key}"

    # ── capture (S3 §3, §4) ─────────────────────────────────────────────
    def capture(
        self,
        profile_dir: Path,
        req: CaptureRequest,
        *,
        inspector: ProcessInspector | None = None,
    ) -> CheckpointManifest:
        """Archive a CLOSED profile → encrypt → wrap DEK → upload. Returns an
        UNVERIFIED manifest; ``verify`` must pass before it becomes usable."""
        profile_dir = Path(profile_dir).resolve()
        checkpoint_id = _uuid()
        object_key = self._object_key(req.profile_id, req.revision, checkpoint_id)
        manifest_key = self._manifest_key(object_key)

        closure: ClosureProof = prove_closed(
            profile_dir,
            context_closed_at=req.context_closed_at,
            process_exit_confirmed_at=req.process_exit_confirmed_at,
            close_wait_ms=req.close_wait_ms,
            escalation=req.escalation,
            inspector=inspector,
        )
        if closure.escalation == "sigkill":
            logger.warning(
                "[checkpoint] LOUD RECOVERY: profile %s required SIGKILL to close "
                "Chromium before capture — the checkpoint is valid but the worker has "
                "a shutdown bug.",
                req.profile_id,
            )

        cookie_scheme = detect_cookie_scheme(profile_dir)
        tmp = Path(tempfile.mkdtemp(prefix="ckpt-cap-"))
        dek = bytearray(secrets.token_bytes(DEK_BYTES))
        nonce = secrets.token_bytes(GCM_NONCE_BYTES)
        try:
            archive: ArchiveResult = archive_profile(profile_dir, tmp / "profile.tzst")

            manifest = CheckpointManifest(
                manifest_version=MANIFEST_VERSION,
                checkpoint_id=checkpoint_id,
                profile_id=req.profile_id,
                revision=req.revision,
                parent_revision=req.parent_revision,
                object_ref=self._uri(object_key),
                object_version_id=None,
                manifest_object_ref=self._uri(manifest_key),
                archive_format=ARCHIVE_FORMAT,
                profile_format_version=PROFILE_FORMAT_VERSION,
                content_cipher=CONTENT_CIPHER,
                nonce_b64=_b64(nonce),
                auth_tag_b64=None,
                wrapped_dek_b64="",  # post-encryption; excluded from AAD header
                wrap_alg=self.provider.wrap_alg,
                key_version=KEY_VERSION,
                kms_key_id=None,
                encryption_context=_encryption_context(req.profile_id),
                content_hash=None,
                plaintext_hash=archive.plaintext_hash,
                byte_count=None,
                plaintext_byte_count=archive.plaintext_byte_count,
                chromium_version=req.chromium_version,
                chromium_major=_major(req.chromium_version),
                cookie_scheme=cookie_scheme,
                worker_image_ref=req.worker_image_ref,
                playwright_version=req.playwright_version,
                closure_proof=closure,
                created_at=_iso(_now()),
                capture_reason=req.capture_reason,  # type: ignore[arg-type]
                retention_expires_at=req.retention_expires_at,
            )

            aad = manifest.header_aad()
            enc = encrypt_archive(archive.path, tmp / "profile.enc", bytes(dek), nonce, aad)
            wrapped, kms_key_id = self.provider.wrap(bytes(dek), manifest.encryption_context)

            # upload ciphertext, capture version id
            with open(enc.path, "rb") as fh:
                put = self.store.put(object_key, fh.read())

            manifest.content_hash = enc.content_hash
            manifest.byte_count = enc.byte_count
            manifest.auth_tag_b64 = _b64(enc.tag)
            manifest.wrapped_dek_b64 = _b64(wrapped)
            manifest.kms_key_id = kms_key_id
            manifest.object_version_id = put.version_id

            self.store.put(manifest_key, manifest.canonical_bytes())
            return manifest
        finally:
            zeroize(dek)
            shutil.rmtree(tmp, ignore_errors=True)

    # ── verification gate (S3 §5) ───────────────────────────────────────
    def verify(self, manifest: CheckpointManifest) -> CheckpointManifest:
        """Run the five-check gate. Returns the manifest with ``verified_at`` +
        ``verification`` set and the sidecar re-PUT. Raises ``VerificationError`` on
        any failure (leaving any prior current revision untouched)."""
        started = time.monotonic()
        object_key = _key_of(manifest.object_ref)
        scratch = Path(tempfile.mkdtemp(prefix="ckpt-verify-"))
        dek = bytearray(b"\x00" * DEK_BYTES)
        bytes_read = 0
        try:
            # V1 — upload hash (read what the store actually holds)
            import hashlib

            h = hashlib.sha256()
            n = 0
            with self.store.open_stream(object_key, manifest.object_version_id) as st:
                while True:
                    block = st.read(8 * 1024 * 1024)
                    if not block:
                        break
                    h.update(block)
                    n += len(block)
            bytes_read = n
            if h.hexdigest() != manifest.content_hash or n != manifest.byte_count:
                raise VerificationError(
                    "stored object hash/byte-count differs from manifest",
                    code="upload_hash_mismatch",
                )

            # V2 — unwrap (assert context equals what code would build)
            want_ctx = _encryption_context(manifest.profile_id)
            if manifest.encryption_context != want_ctx:
                raise VerificationError(
                    "manifest encryption_context differs from the canonical context",
                    code="wrap_context_mismatch",
                )
            dek[:] = self.provider.unwrap(
                _unb64(manifest.wrapped_dek_b64), manifest.encryption_context
            )

            # V3 — decrypt + authenticate
            aad = manifest.header_aad()
            with self.store.open_stream(object_key, manifest.object_version_id) as st:
                pt_hash, pt_len = decrypt_stream_to_file(
                    st,
                    scratch / "profile.tzst",
                    bytes(dek),
                    _unb64(manifest.nonce_b64),
                    aad,
                    _unb64(manifest.auth_tag_b64 or ""),
                )
            if pt_hash != manifest.plaintext_hash or pt_len != manifest.plaintext_byte_count:
                raise VerificationError(
                    "recovered plaintext hash/byte-count differs from manifest",
                    code="plaintext_hash_mismatch",
                )

            # V4 — archive probe
            extract_dir = scratch / "extract"
            extract_archive(scratch / "profile.tzst", extract_dir)
            assert_expected_members(extract_dir)

            # V5 — content probe
            _profile_probe(extract_dir)

            manifest.verified_at = _iso(_now())
            manifest.verification = VerificationBlock(
                verified_at=manifest.verified_at,
                checks=list(_VERIFICATION_CHECKS),
                verifier_image_ref=self.verifier_image_ref,
                duration_ms=int((time.monotonic() - started) * 1000),
                bytes_read=bytes_read,
            )
            manifest.failure = None
            self.store.put(_key_of(manifest.manifest_object_ref), manifest.canonical_bytes())
            return manifest
        except VerificationError as exc:
            manifest.verified_at = None
            manifest.failure = FailureBlock(
                code=exc.code,
                detected_at=_iso(_now()),
                stage="verify",
                detail=str(exc),
                detected_by="verify_gate",
            )
            self.store.put(_key_of(manifest.manifest_object_ref), manifest.canonical_bytes())
            raise
        finally:
            zeroize(dek)
            shutil.rmtree(scratch, ignore_errors=True)

    # ── manifest enumeration (sidecars are the source of truth here) ─────
    def _load_manifest(self, manifest_key: str) -> CheckpointManifest:
        raw = self.store.open_stream(manifest_key).read()
        data = json.loads(raw.decode("utf-8"))
        # manifest_hash integrity (R3): the sidecar's canonical form is self-hashing.
        return CheckpointManifest.model_validate(data)

    def list_manifests(self, profile_id: str) -> list[CheckpointManifest]:
        out: list[CheckpointManifest] = []
        for key in self.store.list_prefix(self._prefix(profile_id)):
            if key.endswith(".manifest.json"):
                try:
                    out.append(self._load_manifest(key))
                except Exception:
                    logger.warning("[checkpoint] unreadable sidecar %s", key)
        out.sort(key=lambda m: m.revision, reverse=True)
        return out

    # ── restore + last-verified fallback (S3 §6, §7) ────────────────────
    def restore(
        self,
        profile_id: str,
        dest_dir: Path,
        worker: WorkerContext,
        *,
        requested_revision: int | None = None,
    ) -> RestoreOutcome:
        """Restore the profile into ``dest_dir``. Walks verified revisions newest-first
        and takes the first that passes every check AND actually decrypts. NEVER creates
        a blank profile: if every candidate fails, raises ``NoRestorableRevisionError``
        and writes nothing into ``dest_dir``."""
        dest_dir = Path(dest_dir)
        manifests = [m for m in self.list_manifests(profile_id) if m.verified_at]
        if requested_revision is not None:
            manifests = [m for m in manifests if m.revision <= requested_revision]
        candidates = manifests[:MAX_FALLBACK_CANDIDATES]
        if not candidates:
            raise NoRestorableRevisionError(
                f"no verified checkpoint revision for profile {profile_id}",
                attempts=[],
            )

        skipped: list[int] = []
        marked_corrupt: list[int] = []
        attempts: list[dict[str, object]] = []

        for m in candidates:
            try:
                self._restore_prelaunch_checks(m, profile_id, worker)
                self._decrypt_into(m, dest_dir)
            except (RestoreError, VerificationError, CheckpointError) as exc:
                attempts.append(
                    {"revision": m.revision, "code": getattr(exc, "code", "?"), "detail": str(exc)}
                )
                skipped.append(m.revision)
                # Only a decrypt/tag failure marks the revision corrupt; a
                # compatibility refusal (e.g. chromium_downgrade) is NOT corruption.
                if getattr(exc, "code", "") in {
                    "auth_tag_invalid",
                    "plaintext_hash_mismatch",
                    "archive_unreadable",
                    "profile_probe_failed",
                    "upload_hash_mismatch",
                    "object_missing",
                }:
                    self._mark_corrupt(m, exc)
                    marked_corrupt.append(m.revision)
                    logger.warning(
                        "[checkpoint] LOUD RECOVERY: revision %s of profile %s failed "
                        "restore and was marked corrupt (%s) — a fallback firing means "
                        "a bug got past the verification gate.",
                        m.revision,
                        profile_id,
                        getattr(exc, "code", "?"),
                    )
                continue

            newest_created = _newest_created(manifests)
            loss_from = m.created_at
            loss_secs = 0
            if newest_created and newest_created != m.created_at:
                loss_secs = max(
                    0,
                    int((_parse(newest_created) - _parse(m.created_at)).total_seconds()),
                )
            return RestoreOutcome(
                restored_revision=m.revision,
                requested_revision=requested_revision,
                skipped_revisions=skipped,
                loss_window_from=loss_from if skipped else None,
                loss_window_to=newest_created if skipped else None,
                loss_window_seconds=loss_secs,
                marked_corrupt=marked_corrupt,
            )

        # Every candidate failed — no blank profile.
        _assert_empty(dest_dir)
        raise NoRestorableRevisionError(
            f"every verified checkpoint for profile {profile_id} failed restore; "
            f"NO blank profile was created. Recover from an operator path.",
            attempts=attempts,
        )

    def _restore_prelaunch_checks(
        self, m: CheckpointManifest, profile_id: str, worker: WorkerContext
    ) -> None:
        object_key = _key_of(m.object_ref)
        # R2 — objects exist
        if not self.store.head(object_key, m.object_version_id):
            raise RestoreError("ciphertext object missing", code="object_missing")
        if not self.store.head(_key_of(m.manifest_object_ref)):
            raise RestoreError("manifest sidecar missing", code="manifest_missing")
        # R3/R4 handled by sidecar being the record; R5 — owner (profile id match)
        if m.profile_id != profile_id:
            raise RestoreError("manifest names a different profile", code="owner_mismatch")
        # R6 — manifest version
        if m.manifest_version not in SUPPORTED_MANIFEST_VERSIONS:
            raise RestoreError(
                f"unsupported manifest_version {m.manifest_version}",
                code="manifest_version_unsupported",
            )
        # R7 — archive format
        if m.archive_format not in SUPPORTED_ARCHIVE_FORMATS:
            raise RestoreError(
                f"unsupported archive_format {m.archive_format!r}",
                code="archive_format_unsupported",
            )
        # R8 — profile format not newer than the worker supports
        if m.profile_format_version > worker.max_profile_format_version:
            raise RestoreError(
                "profile_format_version is newer than this worker supports",
                code="profile_format_too_new",
            )
        # R9 — wrap algorithm permitted (refuse local-dev on a real deployment)
        if m.wrap_alg.startswith("local-dev-") and not worker.allow_local_dev_wrap:
            raise RestoreError(
                "local-dev wrapped checkpoint refused on a real deployment",
                code="wrap_alg_not_permitted",
            )
        # R10 — Chromium compatibility (equal/older fine; newer refused)
        if m.chromium_major > worker.chromium_major:
            raise RestoreError(
                f"checkpoint chromium major {m.chromium_major} is newer than the "
                f"worker's {worker.chromium_major}",
                code="chromium_downgrade_refused",
            )
        # D-5 — cookie scheme must match the restoring worker's, else garbage cookies
        if m.cookie_scheme not in SUPPORTED_COOKIE_SCHEMES:
            raise RestoreError(
                f"unknown cookie_scheme {m.cookie_scheme!r}", code="cookie_scheme_mismatch"
            )
        if m.cookie_scheme != worker.cookie_scheme:
            raise RestoreError(
                f"cookie scheme mismatch: checkpoint recorded {m.cookie_scheme!r}, "
                f"restoring worker is {worker.cookie_scheme!r} — cookies would decrypt "
                f"to garbage (D-5)",
                code="cookie_scheme_mismatch",
            )

    def _decrypt_into(self, m: CheckpointManifest, dest_dir: Path) -> None:
        object_key = _key_of(m.object_ref)
        tmp = Path(tempfile.mkdtemp(prefix="ckpt-restore-"))
        dek = bytearray(b"\x00" * DEK_BYTES)
        try:
            want_ctx = _encryption_context(m.profile_id)
            if m.encryption_context != want_ctx:
                raise VerificationError(
                    "encryption_context mismatch on restore", code="wrap_context_mismatch"
                )
            dek[:] = self.provider.unwrap(_unb64(m.wrapped_dek_b64), m.encryption_context)
            aad = m.header_aad()
            with self.store.open_stream(object_key, m.object_version_id) as st:
                pt_hash, _ = decrypt_stream_to_file(
                    st,
                    tmp / "p.tzst",
                    bytes(dek),
                    _unb64(m.nonce_b64),
                    aad,
                    _unb64(m.auth_tag_b64 or ""),
                )
            if pt_hash != m.plaintext_hash:
                raise VerificationError(
                    "plaintext hash mismatch on restore", code="plaintext_hash_mismatch"
                )
            # Extract into the real profile mount only after the tag verified.
            extract_archive(tmp / "p.tzst", dest_dir)
            assert_expected_members(dest_dir)
        finally:
            zeroize(dek)
            shutil.rmtree(tmp, ignore_errors=True)

    def _mark_corrupt(self, m: CheckpointManifest, exc: Exception) -> None:
        m.verified_at = None
        m.failure = FailureBlock(
            code=getattr(exc, "code", "auth_tag_invalid"),
            detected_at=_iso(_now()),
            stage="restore",
            detail=str(exc),
            detected_by="restore",
        )
        self.store.put(_key_of(m.manifest_object_ref), m.canonical_bytes())

    # ── cryptographic deletion (S3 §8) ──────────────────────────────────
    def delete_profile(
        self,
        profile_id: str,
        *,
        requested_by_actor: str = "user",
        engine_image_ref: str = "sha256:local-dev-deletion-worker",
    ) -> DeletionOutcome:
        """Cryptographically delete every revision of a profile: delete objects,
        destroy the wrapped-DEK sidecar copy, absence-probe, and write a content-free
        tombstone (S3 §8)."""
        manifests = self.list_manifests(profile_id)
        return self._delete_revisions(profile_id, manifests, requested_by_actor, engine_image_ref)

    def _delete_revisions(
        self,
        profile_id: str,
        manifests: list[CheckpointManifest],
        requested_by_actor: str,
        engine_image_ref: str,
    ) -> DeletionOutcome:
        per_revision: list[dict[str, object]] = []
        outcome = "complete"
        revisions_deleted: list[int] = []
        for m in manifests:
            object_key = _key_of(m.object_ref)
            manifest_key = _key_of(m.manifest_object_ref)
            obj_versions = self.store.delete_all_versions(object_key)  # step 4
            man_versions = self.store.delete_all_versions(manifest_key)  # steps 4/5
            # step 6 — absence probe
            obj_absent = not self.store.head(object_key)
            man_absent = not self.store.head(manifest_key)
            if not (obj_absent and man_absent):
                outcome = "partial_retryable"
            per_revision.append(
                {
                    "revision": m.revision,
                    "objects": [
                        {
                            "object_ref": m.object_ref,
                            "version_ids": obj_versions,
                            "absence_probe_at": _iso(_now()),
                            "absence_probe_result": "404" if obj_absent else "present",
                        },
                        {
                            "object_ref": m.manifest_object_ref,
                            "version_ids": man_versions,
                            "absence_probe_at": _iso(_now()),
                            "absence_probe_result": "404" if man_absent else "present",
                        },
                    ],
                    "dek_destroyed_at": _iso(_now()),
                    "dek_destruction_method": "wrapped_dek_sidecar_deleted",
                    "kms_key_id": m.kms_key_id,
                    "key_version": m.key_version,
                    "byte_count": m.byte_count,
                }
            )
            revisions_deleted.append(m.revision)

        tombstone: dict[str, object] = {
            "deleted_at": _iso(_now()),
            "requested_by_actor": requested_by_actor,
            "profile_id": profile_id,
            "revisions": per_revision,
            "engine_image_ref": engine_image_ref,
            "verified_by": "deletion_worker",
            "outcome": outcome,
        }
        return DeletionOutcome(
            profile_id=profile_id,
            revisions_deleted=revisions_deleted,
            tombstone=tombstone,
            outcome=outcome,
        )

    # ── 30-day retention pruning (D-20) ─────────────────────────────────
    def prune_retention(
        self,
        profile_id: str,
        *,
        now: datetime | None = None,
        engine_image_ref: str = "sha256:local-dev-retention-worker",
    ) -> DeletionOutcome:
        """Prune revisions older than 30 days, but ALWAYS keep the newest verified
        revision regardless of age (D-20). Pruning uses the same cryptographic
        deletion + proof as ``delete_profile``."""
        now = now or _now()
        cutoff = now - timedelta(days=RETENTION_DAYS)
        manifests = self.list_manifests(profile_id)
        verified = [m for m in manifests if m.verified_at]
        newest_verified_rev = max((m.revision for m in verified), default=None)

        to_prune: list[CheckpointManifest] = []
        for m in manifests:
            if m.revision == newest_verified_rev:
                continue  # the always-kept restore point
            if _parse(m.created_at) < cutoff:
                to_prune.append(m)

        if not to_prune:
            return DeletionOutcome(
                profile_id=profile_id,
                revisions_deleted=[],
                tombstone={
                    "deleted_at": _iso(now),
                    "requested_by_actor": "retention_policy",
                    "profile_id": profile_id,
                    "revisions": [],
                    "kept_newest_verified_revision": newest_verified_rev,
                    "outcome": "complete",
                },
                outcome="complete",
            )
        result = self._delete_revisions(profile_id, to_prune, "retention_policy", engine_image_ref)
        result.tombstone["kept_newest_verified_revision"] = newest_verified_rev
        result.tombstone["retention_days"] = RETENTION_DAYS
        return result


# ── module helpers ───────────────────────────────────────────────────────
def _uuid() -> str:
    import uuid

    return str(uuid.uuid4())


def _major(chromium_version: str) -> int:
    try:
        return int(chromium_version.split(".", 1)[0])
    except (ValueError, IndexError) as exc:
        raise CheckpointError(
            f"could not parse chromium major from {chromium_version!r}",
            code="chromium_downgrade_refused",
        ) from exc


def _key_of(object_ref: str) -> str:
    # s3://bucket/key -> key
    rest = object_ref[len("s3://") :]
    return rest.partition("/")[2]


def _profile_probe(extract_dir: Path) -> None:
    cookies = extract_dir / "Default" / "Cookies"
    if cookies.exists():
        try:
            result = check_local_sqlite_integrity(cookies)
        except sqlite3.Error as exc:
            raise VerificationError(
                f"Default/Cookies quick_check failed: {exc}", code="profile_probe_failed"
            ) from exc
        if result != "ok":
            raise VerificationError(
                f"Default/Cookies quick_check not ok: {result}", code="profile_probe_failed"
            )
    local_state = extract_dir / "Local State"
    if local_state.exists():
        try:
            json.loads(local_state.read_text())
        except (ValueError, OSError) as exc:
            raise VerificationError(
                f"Local State is not valid JSON: {exc}", code="profile_probe_failed"
            ) from exc


def _parse(iso: str) -> datetime:
    return datetime.fromisoformat(iso.replace("Z", "+00:00"))


def _newest_created(manifests: list[CheckpointManifest]) -> str | None:
    if not manifests:
        return None
    return max(manifests, key=lambda m: m.revision).created_at


def _assert_empty(dest_dir: Path) -> None:
    if dest_dir.exists() and any(dest_dir.iterdir()):
        # A partial write leaked into the mount — scream and clean it, never leave a
        # half-restored profile that reads as healthy.
        logger.error(
            "[checkpoint] restore failed for all candidates but %s is non-empty; "
            "clearing it so no partial/blank profile is presented as healthy.",
            dest_dir,
        )
        for child in dest_dir.iterdir():
            if child.is_dir():
                shutil.rmtree(child, ignore_errors=True)
            else:
                child.unlink(missing_ok=True)
