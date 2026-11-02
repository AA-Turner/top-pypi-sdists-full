"""
Content-hash deduplication for cld_files.

The dedup contract is strict-intent: callers MUST declare their intent
when writing a file, and the server enforces the consequences. There is
no "upsert" semantic. The three intents are:

  * ``create``           -- "I am uploading a brand-new file. I expect
                            no existing copy."
                            If a duplicate exists: raises
                            :class:`DuplicateFileError`. The caller (UI)
                            is expected to surface the conflict to the
                            user and re-submit with a different intent.

  * ``alias_existing``   -- "I might be uploading something that exists.
                            If it does, return the existing row. Do not
                            create a duplicate row."
                            Returns the existing row when duplicate is
                            found; falls through to create when not.

  * ``force_new_copy``   -- "I want a deliberate parallel copy of this
                            content with its own id."
                            Requires a non-empty reason. Creates a new
                            cld_files row whose ``duplicate_of_file_id``
                            points back at the canonical row.

Scoping: dedup is keyed by both organization and owner when
``organization_id`` is set, and by owner otherwise. Cross-member
organization dedup is intentionally deferred until alias access semantics
exist; an upload must never return another member's unreadable private row.

This module is the single seam through which every file write must
flow. It owns the SHA-256 computation, the dedup lookup, and the
intent-vs-reality conflict logic.
"""

from __future__ import annotations

from matrx_orm import db_constraint, db_sqlstate

import enum
import hashlib
import logging
from dataclasses import dataclass
from typing import Any, Literal

logger = logging.getLogger(__name__)


SHA256_BUFSIZE = 1024 * 1024  # 1 MiB streaming buffer for large files


class UploadIntent(str, enum.Enum):
    CREATE = "create"
    ALIAS_EXISTING = "alias_existing"
    FORCE_NEW_COPY = "force_new_copy"


VALID_INTENTS = frozenset({i.value for i in UploadIntent})


@dataclass(frozen=True)
class DedupLookupResult:
    """Outcome of a pre-write checksum lookup against cld_files."""

    checksum: str
    existing: dict[str, Any] | None  # the canonical cld_files row, if any
    scope: Literal["org", "owner", "none"]

    @property
    def has_duplicate(self) -> bool:
        return self.existing is not None


# ── Exceptions ──────────────────────────────────────────────────────────


class DedupError(Exception):
    """Base class for dedup-policy violations."""

    status_code: int = 409
    error_code: str = "dedup_error"

    def to_dict(self) -> dict[str, Any]:
        return {
            "error": self.error_code,
            "status_code": self.status_code,
            "message": str(self),
        }


class DuplicateFileError(DedupError):
    """Raised when intent='create' encounters an existing copy."""

    status_code = 409
    error_code = "duplicate_file"

    def __init__(
        self,
        *,
        checksum: str,
        existing_file_id: str,
        existing_path: str | None,
        existing_created_at: str | None,
        scope: str,
    ) -> None:
        self.checksum = checksum
        self.existing_file_id = existing_file_id
        self.existing_path = existing_path
        self.existing_created_at = existing_created_at
        self.scope = scope
        message = (
            f"A file with this content already exists "
            f"(file_id={existing_file_id}"
            + (f", path={existing_path}" if existing_path else "")
            + f", scope={scope}). "
            "Use intent='alias_existing' to reuse it, or "
            "intent='force_new_copy' with a reason to create a parallel copy."
        )
        super().__init__(message)

    def to_dict(self) -> dict[str, Any]:
        return {
            **super().to_dict(),
            "existing_file_id": self.existing_file_id,
            "existing_path": self.existing_path,
            "existing_created_at": self.existing_created_at,
            "scope": self.scope,
            "checksum": self.checksum,
            "allowed_intents": ["alias_existing", "force_new_copy"],
        }


class FilePathConflictError(DedupError):
    """Raised when a strict create targets an already-occupied logical path."""

    status_code = 409
    error_code = "file_path_conflict"

    def __init__(self, *, file_path: str) -> None:
        self.file_path = file_path
        super().__init__(
            f"A file already exists at path {file_path!r}. "
            "Strict upload intents never overwrite; choose a new path."
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            **super().to_dict(),
            "file_path": self.file_path,
        }


class InvalidIntentError(DedupError):
    """Raised when the caller supplies an unknown intent."""

    status_code = 400
    error_code = "invalid_intent"


class MissingReasonError(DedupError):
    """Raised when intent='force_new_copy' is requested with no reason."""

    status_code = 400
    error_code = "reason_required"


# ── Checksum computation ────────────────────────────────────────────────


def compute_checksum(content: bytes | bytearray | memoryview) -> str:
    """Compute the SHA-256 of a content payload.

    Returns the lowercase hex digest. Matches the format already stored
    in ``cld_files.checksum`` for existing rows so dedup lookups line up.
    """
    if isinstance(content, (bytearray, memoryview)):
        content = bytes(content)
    if not isinstance(content, bytes):
        raise TypeError(
            f"compute_checksum requires bytes; got {type(content).__name__}"
        )
    h = hashlib.sha256()
    # Single-shot is fine here; the streaming variant below is for files
    # too large to fit in memory.
    h.update(content)
    return h.hexdigest()


def compute_checksum_stream(reader: Any) -> str:
    """Compute SHA-256 over a streaming reader (any object with .read(n)).

    Used for large uploads where the full bytes shouldn't be buffered
    just to hash them. The reader is consumed; the caller is responsible
    for resetting / re-reading the source if the bytes are still needed.
    """
    h = hashlib.sha256()
    while True:
        chunk = reader.read(SHA256_BUFSIZE)
        if not chunk:
            break
        if isinstance(chunk, str):
            chunk = chunk.encode("utf-8")
        h.update(chunk)
    return h.hexdigest()


# ── Intent validation ──────────────────────────────────────────────────


def coerce_intent(value: str | UploadIntent | None) -> UploadIntent:
    """Parse an intent string. Raise ``InvalidIntentError`` on unknown."""
    if value is None:
        raise InvalidIntentError(
            "intent is required; expected one of "
            f"{sorted(VALID_INTENTS)}"
        )
    if isinstance(value, UploadIntent):
        return value
    if not isinstance(value, str):
        raise InvalidIntentError(
            f"intent must be a string; got {type(value).__name__}"
        )
    if value not in VALID_INTENTS:
        raise InvalidIntentError(
            f"unknown intent '{value}'; expected one of "
            f"{sorted(VALID_INTENTS)}"
        )
    return UploadIntent(value)


def validate_force_new_copy_reason(reason: str | None) -> str:
    """Ensure ``force_new_copy`` callers provide a real reason."""
    if not reason or not reason.strip():
        raise MissingReasonError(
            "intent='force_new_copy' requires a non-empty 'reason' "
            "describing why a parallel copy is being created."
        )
    cleaned = reason.strip()
    if len(cleaned) < 4:
        raise MissingReasonError(
            "reason for force_new_copy must be at least 4 characters."
        )
    return cleaned


# ── Lookup helper ──────────────────────────────────────────────────────


async def lookup_existing_async(
    db: Any,
    *,
    checksum: str,
    owner_id: str | None,
    organization_id: str | None,
) -> DedupLookupResult:
    """Find an existing canonical cld_files row for this checksum.

    Org scope wins if ``organization_id`` is provided. Returns a
    :class:`DedupLookupResult` describing what was found (if anything).
    """
    if not checksum:
        return DedupLookupResult(checksum=checksum, existing=None, scope="none")

    existing = await db.get_file_by_checksum_async(
        checksum,
        owner_id=owner_id,
        organization_id=organization_id,
    )
    if existing is None:
        return DedupLookupResult(checksum=checksum, existing=None, scope="none")

    # "org" is the historical wire label; lookup identity is owner+org.
    scope = "org" if organization_id else "owner"
    return DedupLookupResult(checksum=checksum, existing=existing, scope=scope)


# ── Convergence: a content write that collides with another canonical ──
#
# ``cld_files_dedup_canonical`` is UNIQUE (organization_id, created_by,
# checksum) over live canonical roots. A content write whose bytes another
# live root of the same (organization, owner) already holds violates it.
# Refusing would lose the save, so the row keeps its id, path and own object
# and becomes that canonical's ALIAS (``duplicate_of_file_id``). An alias whose
# bytes later change is no longer equivalent: its link is cleared explicitly
# in the same UPDATE, which makes it a root again — so a collision with a third
# file re-converges right here. This is the ONE path for every content writer:
# managed_write[_async], replace_file_async, track_write[_async] and
# VersionManager.restore_version[_async]. Never catch the 23505 anywhere else.


def is_dedup_unique_violation(exc: BaseException) -> bool:
    """True if ``exc`` is a Postgres 23505 on ``cld_files_dedup_canonical``.

    Any other violation (e.g. the ``owner_id, file_path`` key) is a real error
    and must propagate.
    """
    # The SQLSTATE and the constraint name, never the error's words.
    return db_sqlstate(exc) == "23505" and db_constraint(exc) == "cld_files_dedup_canonical"


def _stale_alias_link(current: dict[str, Any], updates: dict[str, Any]) -> tuple[str, ...]:
    """The columns to NULL: an alias whose checksum changes loses its link."""
    checksum = updates.get("checksum")
    if current.get("duplicate_of_file_id") and checksum and checksum != current.get("checksum"):
        return ("duplicate_of_file_id",)
    return ()


def _log_converged(file_id: object, canonical_id: str) -> None:
    logger.info(
        "file %s now holds bytes identical to canonical %s; kept as its dedup alias",
        file_id,
        canonical_id,
    )


async def _canonical_for_collision_async(
    db: Any,
    exc: BaseException,
    checksum: str | None,
    *,
    owner_id: str | None,
    organization_id: str | None,
    self_id: object = None,
) -> str | None:
    if not checksum or not is_dedup_unique_violation(exc):
        return None
    found = await lookup_existing_async(
        db, checksum=checksum, owner_id=owner_id, organization_id=organization_id
    )
    if found.existing is None or str(found.existing["id"]) == str(self_id):
        return None
    return str(found.existing["id"])


def _canonical_for_collision(
    db: Any,
    exc: BaseException,
    checksum: str | None,
    *,
    owner_id: str | None,
    organization_id: str | None,
    self_id: object = None,
) -> str | None:
    if not checksum or not is_dedup_unique_violation(exc):
        return None
    existing = db.get_file_by_checksum(
        checksum, owner_id=owner_id, organization_id=organization_id
    )
    if existing is None or str(existing["id"]) == str(self_id):
        return None
    return str(existing["id"])


def _write_scope(db: Any):
    """A (nested -> SAVEPOINT) transaction on the file store's database; a no-op scope
    when ``db`` does not name one (test doubles)."""
    import contextlib

    name_fn = getattr(db, "_db_name", None)
    name = name_fn() if callable(name_fn) else None
    if not isinstance(name, str) or not name:
        return contextlib.nullcontext()
    from matrx_orm import transaction

    return transaction(database=name)


async def update_file_converging_async(
    db: Any,
    file_id: str,
    updates: dict[str, Any],
    *,
    current: dict[str, Any],
    owner_id: str | None,
    organization_id: str | None,
) -> dict[str, Any]:
    """UPDATE a row's content, converging on the dedup canonical.

    ``current`` is the row as read before this write. Returns the column
    values actually written (a cleared link appears as ``None``).
    """
    clear = _stale_alias_link(current, updates)
    try:
        # SAVEPOINT around the probing UPDATE. Inside the caller's transaction
        # (replace_file_async) a 23505 on cld_files_dedup_canonical aborts the
        # whole transaction; the checksum-canonical lookup below then died with
        # InFailedSQLTransactionError (feedback 7fb72866). The nested
        # transaction rolls back to the savepoint, so the lookup and the
        # converging UPDATE run on a healthy transaction. Outside any
        # transaction this is simply a short transaction around the one UPDATE.
        async with _write_scope(db):
            if clear:
                await db.update_file_async(file_id, updates, clear_columns=clear)
            else:
                await db.update_file_async(file_id, updates)
        return {**updates, **dict.fromkeys(clear)}
    except Exception as update_exc:
        canonical_id = await _canonical_for_collision_async(
            db,
            update_exc,
            updates.get("checksum"),
            owner_id=owner_id,
            organization_id=organization_id,
            self_id=file_id,
        )
        if canonical_id is None:
            raise
        converged = {**updates, "duplicate_of_file_id": canonical_id}
        _log_converged(file_id, canonical_id)
        await db.update_file_async(file_id, converged)
        return converged


def update_file_converging(
    db: Any,
    file_id: str,
    updates: dict[str, Any],
    *,
    current: dict[str, Any],
    owner_id: str | None,
    organization_id: str | None,
) -> dict[str, Any]:
    """Sync twin of :func:`update_file_converging_async`."""
    clear = _stale_alias_link(current, updates)
    try:
        if clear:
            db.update_file(file_id, updates, clear_columns=clear)
        else:
            db.update_file(file_id, updates)
        return {**updates, **dict.fromkeys(clear)}
    except Exception as update_exc:
        canonical_id = _canonical_for_collision(
            db,
            update_exc,
            updates.get("checksum"),
            owner_id=owner_id,
            organization_id=organization_id,
            self_id=file_id,
        )
        if canonical_id is None:
            raise
        converged = {**updates, "duplicate_of_file_id": canonical_id}
        _log_converged(file_id, canonical_id)
        db.update_file(file_id, converged)
        return converged


async def insert_file_converging_async(
    db: Any,
    payload: dict[str, Any],
    *,
    owner_id: str,
    organization_id: str | None,
) -> dict[str, Any]:
    """INSERT a path row; bytes another canonical holds keep the path as its alias."""
    try:
        return await db.upsert_file_async(payload)
    except Exception as insert_exc:
        canonical_id = await _canonical_for_collision_async(
            db,
            insert_exc,
            payload.get("checksum"),
            owner_id=owner_id,
            organization_id=organization_id,
        )
        if canonical_id is None:
            raise
        _log_converged(payload.get("file_path"), canonical_id)
        return await db.upsert_file_async({**payload, "duplicate_of_file_id": canonical_id})


def insert_file_converging(
    db: Any,
    payload: dict[str, Any],
    *,
    owner_id: str,
    organization_id: str | None,
) -> dict[str, Any]:
    """Sync twin of :func:`insert_file_converging_async`."""
    try:
        return db.upsert_file(payload)
    except Exception as insert_exc:
        canonical_id = _canonical_for_collision(
            db,
            insert_exc,
            payload.get("checksum"),
            owner_id=owner_id,
            organization_id=organization_id,
        )
        if canonical_id is None:
            raise
        _log_converged(payload.get("file_path"), canonical_id)
        return db.upsert_file({**payload, "duplicate_of_file_id": canonical_id})


# ── Policy resolution ──────────────────────────────────────────────────


@dataclass(frozen=True)
class DedupDecision:
    """The action a write path should take after consulting the policy.

    One of:
      - ``write_new`` (intent=create, no dupe): caller performs a normal write.
      - ``return_existing`` (intent=alias_existing, dupe found):
        caller skips the write entirely and returns the existing row.
      - ``write_alias`` (intent=force_new_copy, dupe found):
        caller performs a normal write but stamps
        ``duplicate_of_file_id = canonical.id`` on the new row.
      - ``write_new`` (intent=alias_existing or force_new_copy, no dupe):
        same as a plain create.
    """

    action: Literal["write_new", "return_existing", "write_alias"]
    intent: UploadIntent
    lookup: DedupLookupResult
    reason: str | None = None  # only for force_new_copy

    @property
    def canonical_file_id(self) -> str | None:
        if self.lookup.existing is None:
            return None
        return str(self.lookup.existing.get("id"))


def resolve_dedup_policy(
    intent: UploadIntent,
    lookup: DedupLookupResult,
    *,
    reason: str | None,
    file_path: str | None = None,
) -> DedupDecision:
    """Apply the strict-intent contract.

    Raises ``DuplicateFileError`` for intent='create' + dupe found.
    Validates the reason for force_new_copy.
    Otherwise returns a :class:`DedupDecision` the write path can act on.
    """
    if intent is UploadIntent.CREATE:
        if lookup.has_duplicate:
            existing = lookup.existing or {}
            raise DuplicateFileError(
                checksum=lookup.checksum,
                existing_file_id=str(existing.get("id")),
                existing_path=existing.get("file_path"),
                existing_created_at=str(existing.get("created_at"))
                if existing.get("created_at") else None,
                scope=lookup.scope,
            )
        return DedupDecision(action="write_new", intent=intent, lookup=lookup)

    if intent is UploadIntent.ALIAS_EXISTING:
        if lookup.has_duplicate:
            existing_path = (lookup.existing or {}).get("file_path")
            if file_path is not None and existing_path != file_path:
                # Dedupe is a storage concern; it never means "no row". The
                # bytes already live at ANOTHER path, so this placement gets a
                # row of its own linked by duplicate_of_file_id (main's ruling,
                # 2026-10-21: a.txt then b.txt with the same bytes answered
                # b.txt with a.txt's id and recorded b.txt nowhere).
                return DedupDecision(action="write_alias", intent=intent, lookup=lookup)
            return DedupDecision(
                action="return_existing", intent=intent, lookup=lookup
            )
        return DedupDecision(action="write_new", intent=intent, lookup=lookup)

    # FORCE_NEW_COPY
    validated_reason = validate_force_new_copy_reason(reason)
    if lookup.has_duplicate:
        return DedupDecision(
            action="write_alias",
            intent=intent,
            lookup=lookup,
            reason=validated_reason,
        )
    # No dupe to alias — degenerate to a normal create. We don't error
    # because the request was self-consistent (the caller said "I want a
    # new copy"); there just isn't anything to alias.
    return DedupDecision(
        action="write_new",
        intent=intent,
        lookup=lookup,
        reason=validated_reason,
    )


# ── End-to-end one-shot ─────────────────────────────────────────────────


async def resolve_async(
    db: Any,
    *,
    intent: str | UploadIntent,
    content: bytes,
    owner_id: str | None,
    organization_id: str | None,
    reason: str | None = None,
    precomputed_checksum: str | None = None,
    file_path: str | None = None,
) -> DedupDecision:
    """End-to-end: hash + lookup + policy. Returns a decision for the
    caller's write path. Most callers want this.

    Args:
        db: a ``CloudSyncDB`` (or anything with
            ``get_file_by_checksum_async``).
        intent: 'create' / 'alias_existing' / 'force_new_copy'.
        content: the raw bytes about to be written.
        owner_id / organization_id: scope for the dedup lookup.
        reason: required for 'force_new_copy'; ignored otherwise.
        precomputed_checksum: if the caller already hashed the content,
            pass it here to avoid re-hashing.

    Raises ``InvalidIntentError``, ``DuplicateFileError``, or
    ``MissingReasonError`` per the strict contract.
    """
    intent_enum = coerce_intent(intent)
    checksum = precomputed_checksum or compute_checksum(content)
    # Empty content hashes to the same constant SHA-256 for every caller,
    # forever — it carries no content to legitimately dedup against, and
    # honoring it here (even via a caller-supplied precomputed_checksum)
    # would let a blank ``upload_with_intent`` alias onto, or raise a
    # DuplicateFileError against, whatever unrelated file first happened
    # to be uploaded empty in this owner/org scope (production defect,
    # jobs-bar cold-walk-11, 2026-09-18; sync_engine.py's five write-path
    # mirrors were closed in db7eb7f09c — this is the explicit
    # upload_with_intent / alias_existing door). Empty content never has
    # a dedup checksum, so it can never match or alias anything here.
    if not content:
        checksum = None
    lookup = await lookup_existing_async(
        db,
        checksum=checksum,
        owner_id=owner_id,
        organization_id=organization_id,
    )
    return resolve_dedup_policy(intent_enum, lookup, reason=reason, file_path=file_path)


__all__ = [
    "UploadIntent",
    "VALID_INTENTS",
    "DedupLookupResult",
    "DedupDecision",
    "DedupError",
    "DuplicateFileError",
    "FilePathConflictError",
    "InvalidIntentError",
    "MissingReasonError",
    "compute_checksum",
    "compute_checksum_stream",
    "coerce_intent",
    "validate_force_new_copy_reason",
    "lookup_existing_async",
    "is_dedup_unique_violation",
    "update_file_converging",
    "update_file_converging_async",
    "insert_file_converging",
    "insert_file_converging_async",
    "resolve_dedup_policy",
    "resolve_async",
]
