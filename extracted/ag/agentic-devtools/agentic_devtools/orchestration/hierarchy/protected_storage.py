"""Protected (encrypted-at-rest) local storage for hierarchy snapshots and traces.

Implements AES-256-GCM authenticated encryption at rest for retained
snapshot/trace content (FR-011, FR-012), using Python's ``cryptography``
library. Every frame carries a fresh cryptographically-random 96-bit nonce
(``os.urandom(12)``), a per-workflow salt, and an explicit version tag.
Frames are appended as NDJSON lines so append-only semantics are preserved
while the underlying bytes are always authenticated-encrypted.

Transport boundary (SC-017): protected storage is **local-filesystem-only**.
No snapshot or trace payload ever crosses a process/host boundary through
this module; the constructor rejects any non-local, non-absolute, or
URI-scheme storage path.

Key material is derived from an externally provisioned master key (never
stored alongside the encrypted data) combined with a random per-workflow
salt. The master key is resolved, in priority order, from:

1. the system keyring (service ``"agentic-devtools"``, key
   ``"hierarchy-master-key"``);
2. the ``AGDT_HIERARCHY_MASTER_KEY`` environment variable;
3. an operator-configured secret file.

Authorization (FR-011, FR-012, SC-017): every read/write path enforces the
configuration-declared operator/service allowlist by deriving the caller's
identity from a trusted, non-caller-supplied source — never from a
caller-supplied argument.
"""

from __future__ import annotations

import base64
import hashlib
import json
import os
import re
import sys
from collections.abc import Callable, Iterator
from dataclasses import dataclass
from pathlib import Path
from typing import IO, TYPE_CHECKING, cast

from agentic_devtools.file_locking import locked_file

if TYPE_CHECKING:
    from .trace import TraceEvent

_FRAME_VERSION = 1
_NONCE_LEN = 12  # 96 bits, per FR-011/FR-012
_KEY_LEN = 32  # AES-256
_MIN_MASTER_KEY_LEN = 32
_AUTHORIZED_PRINCIPALS_ENV = "AGDT_HIERARCHY_AUTHORIZED_PRINCIPALS"

# Matches a URI scheme prefix (e.g. "https:", "s3:", "gcs:") at the start of a
# path string. Requires at least two letters before the colon so a Windows
# drive letter ("C:\\...") is never misclassified as a remote URI scheme.
# Checked against the raw string *before* any "://" substring test because
# ``pathlib.Path`` collapses repeated slashes (e.g. ``Path("https://x")`` ->
# ``"https:/x"``), which would otherwise silently defeat a naive "://" check.
_URI_SCHEME_RE = re.compile(r"^[A-Za-z]{2,}[A-Za-z0-9+.-]*:")


def _frame_aad(version: int, salt: bytes) -> bytes:
    """Return deterministic AES-GCM associated data for a frame.

    Binding the frame's version and salt as associated data (AAD) means
    any post-write modification to those header fields causes AES-GCM
    authentication to fail, preventing silent version/salt substitution.
    """
    return version.to_bytes(4, byteorder="big") + salt


class ProtectedStorageError(RuntimeError):
    """Base class for protected-storage provisioning and integrity errors."""


class MasterKeyUnavailableError(ProtectedStorageError):
    """Raised when no master key source can supply key material."""


class CryptographicCapabilityUnavailableError(ProtectedStorageError):
    """Raised when the required AES-GCM primitive cannot be imported/used."""


class NonceReuseError(ProtectedStorageError):
    """Raised when a nonce is reused within the same derived key (never permitted)."""


class RemoteStorageRejectedError(ProtectedStorageError, ValueError):
    """Raised when a non-local storage path is supplied (SC-017 transport boundary)."""


class UnauthorizedAccessError(ProtectedStorageError):
    """Raised when the derived caller identity is not in the configured allowlist."""


def _get_aesgcm():
    try:
        from cryptography.hazmat.primitives.ciphers.aead import AESGCM
    except ImportError as exc:  # pragma: no cover - environment dependent
        msg = "cryptography's AESGCM primitive is unavailable; protected storage cannot be provisioned"
        raise CryptographicCapabilityUnavailableError(msg) from exc
    return AESGCM


def resolve_master_key(*, secret_file: Path | None = None) -> bytes:
    """Resolve the externally provisioned master key material.

    Tries, in order: the system keyring, the ``AGDT_HIERARCHY_MASTER_KEY``
    environment variable, and an operator-configured secret file. Raises
    ``MasterKeyUnavailableError`` when none of these sources supply key
    material — the derivation secret is never stored in the workflow state
    directory.
    """
    try:
        import keyring  # type: ignore[import-not-found]

        secret = keyring.get_password("agentic-devtools", "hierarchy-master-key")
        if secret:
            return secret.encode("utf-8")
    except Exception:  # noqa: BLE001 - keyring backend unavailable/misconfigured
        pass

    env_val = os.environ.get("AGDT_HIERARCHY_MASTER_KEY", "")
    if env_val:
        return env_val.encode("utf-8")

    if secret_file is not None and secret_file.is_file():
        content = secret_file.read_text(encoding="utf-8").strip()
        if content:
            return content.encode("utf-8")

    msg = (
        "No hierarchy master key is available from the system keyring, "
        "AGDT_HIERARCHY_MASTER_KEY, or an operator-configured secret file"
    )
    raise MasterKeyUnavailableError(msg)


def resolve_authorized_principals(*, config_file: Path | None = None) -> frozenset[str]:
    """Resolve the independently configured operator/service allowlist."""
    raw = os.environ.get(_AUTHORIZED_PRINCIPALS_ENV, "")
    if raw:
        principals = frozenset(part.strip() for part in raw.split(",") if part.strip())
    else:
        path = config_file or (Path.home() / ".agdt" / "hierarchy-authorized-principals")
        try:
            principals = frozenset(
                line.strip()
                for line in path.read_text(encoding="utf-8").splitlines()
                if line.strip() and not line.lstrip().startswith("#")
            )
        except FileNotFoundError:
            principals = frozenset()
    if not principals:
        raise ValueError(f"{_AUTHORIZED_PRINCIPALS_ENV} or an operator-configured allowlist file is required")
    return principals


def derive_workflow_key(master_key: bytes, salt: bytes) -> bytes:
    """Derive a unique 256-bit data key for one workflow from the master key and a random salt."""
    if not isinstance(master_key, bytes) or len(master_key) < _MIN_MASTER_KEY_LEN:
        raise ValueError(f"master_key must be at least {_MIN_MASTER_KEY_LEN} bytes")
    try:
        from cryptography.hazmat.primitives import hashes
        from cryptography.hazmat.primitives.kdf.hkdf import HKDF
    except ImportError as exc:  # pragma: no cover - environment dependent
        msg = "cryptography's HKDF primitive is unavailable; protected storage cannot be provisioned"
        raise CryptographicCapabilityUnavailableError(msg) from exc
    return HKDF(algorithm=hashes.SHA256(), length=_KEY_LEN, salt=salt, info=b"agdt-hierarchy-protected-storage").derive(
        master_key
    )


def _is_local_absolute_path(path: Path) -> bool:
    text = str(path)
    if _URI_SCHEME_RE.match(text):
        return False
    return path.is_absolute()


def _first_existing_symlink(path: Path) -> Path | None:
    for candidate in (path, *path.parents):
        if candidate.is_symlink():
            return candidate
    return None


def _assert_no_symlink_components(path: Path) -> None:
    symlink = _first_existing_symlink(path)
    if symlink is None:
        return
    msg = f"Protected storage path contains a symlinked component: {symlink}"
    raise RemoteStorageRejectedError(msg)


@dataclass(frozen=True)
class EncryptedFrame:
    """One AES-256-GCM authenticated frame appended to protected storage."""

    version: int
    salt: str
    nonce: str
    ciphertext: str
    tag: str

    def to_dict(self) -> dict[str, object]:
        return {
            "version": self.version,
            "salt": self.salt,
            "nonce": self.nonce,
            "ciphertext": self.ciphertext,
            "tag": self.tag,
        }


class ProtectedStorage:
    """Append-only, AES-256-GCM-encrypted local storage for one workflow.

    Args:
        storage_path: An absolute local filesystem path (never a URI).
        master_key: The externally provisioned master key. When omitted,
            ``resolve_master_key`` is used.
        salt: A random per-workflow salt. When omitted, a fresh salt is
            generated and reused for the lifetime of this instance.
        authorized_principals: Non-empty trusted operator/service allowlist
            authorized to read or mutate this storage.
        access_trace_path: Optional protected-trace path where blocked access
            attempts are recorded as encrypted events.
    """

    def __init__(
        self,
        storage_path: Path,
        *,
        master_key: bytes | None = None,
        salt: bytes | None = None,
        authorized_principals: frozenset[str] | None = None,
        access_trace_path: Path | None = None,
        asserted_identity: str | None = None,
    ) -> None:
        if not isinstance(storage_path, Path) or not _is_local_absolute_path(storage_path):
            msg = f"Protected storage requires an absolute local filesystem path, got: {storage_path!r}"
            raise RemoteStorageRejectedError(msg)
        _assert_no_symlink_components(storage_path)
        self._path = storage_path
        self._master_key = master_key if master_key is not None else resolve_master_key()
        if len(self._master_key) < _MIN_MASTER_KEY_LEN:
            raise ValueError(f"master_key must be at least {_MIN_MASTER_KEY_LEN} bytes")
        self._path.parent.mkdir(parents=True, exist_ok=True)
        # Salt is resolved lazily: a caller-supplied salt is trusted immediately;
        # a persisted salt from an existing file is loaded eagerly.  If neither
        # is available the salt is deferred (None) and selected under the
        # inter-process lock on the first append to prevent concurrent instances
        # from each generating a different random salt.
        if salt is not None:
            if len(salt) != 16:
                msg = f"salt must be exactly 16 bytes, got {len(salt)}"
                raise ValueError(msg)
            persisted = self._load_persisted_salt()
            if persisted is not None and persisted != salt:
                raise ValueError("caller-supplied salt does not match the salt already persisted in the storage file")
            self._salt: bytes | None = salt
        else:
            self._salt = self._load_persisted_salt()
        # Key derivation is also deferred when the salt is not yet known.
        self._key: bytes | None = derive_workflow_key(self._master_key, self._salt) if self._salt is not None else None
        if not authorized_principals:
            raise ValueError("authorized_principals must be a non-empty allowlist")
        if any(not isinstance(principal, str) or not principal.strip() for principal in authorized_principals):
            raise ValueError("authorized_principals must contain only non-empty principal names")
        self._authorized_principals = frozenset(authorized_principals)
        self._access_trace_path = access_trace_path
        # Deliberately ignored: authorization must never trust a caller claim.
        _ = asserted_identity
        self._used_nonces: set[bytes] = set()
        if self._path.exists():
            self._load_used_nonces()

    @property
    def path(self) -> Path:
        return self._path

    def _load_used_nonces(self) -> None:
        _assert_no_symlink_components(self._path)
        for frame in _iter_frames(self._path, skip_invalid=True):
            try:
                self._used_nonces.add(base64.b64decode(frame.nonce, validate=True))
            except (ValueError, TypeError):
                # A corrupt/truncated frame's nonce field is unusable; skip it
                # rather than let it block loading nonces from earlier,
                # well-formed frames.
                continue

    def _load_persisted_salt(self) -> bytes | None:
        """Recover the workflow salt from the first valid persisted frame."""
        _assert_no_symlink_components(self._path)
        for frame in _iter_frames(self._path, skip_invalid=True):
            try:
                salt = base64.b64decode(frame.salt, validate=True)
            except (ValueError, TypeError):
                continue
            if len(salt) == 16:
                return salt
        return None

    @staticmethod
    def _read_salt_from_handle(file_handle: IO[str]) -> bytes | None:
        """Read the persisted salt from an already-locked/open file handle."""
        file_handle.seek(0)
        for line in file_handle:
            stripped = line.strip()
            if not stripped:
                continue
            try:
                data = json.loads(stripped)
                salt = base64.b64decode(data["salt"], validate=True)
                if len(salt) == 16:
                    return salt
            except Exception:  # noqa: BLE001
                continue
        return None

    @staticmethod
    def _truncate_invalid_final_frame(file_handle: IO[str]) -> None:
        """Truncate an invalid final non-blank frame so future appends stay recoverable."""
        file_handle.seek(0)
        last_nonblank_start: int | None = None
        last_nonblank_line: str | None = None
        while True:
            position = file_handle.tell()
            line = file_handle.readline()
            if line == "":
                break
            stripped = line.strip()
            if stripped:
                last_nonblank_start = position
                last_nonblank_line = stripped
        if last_nonblank_start is None or last_nonblank_line is None:
            file_handle.seek(0, os.SEEK_END)
            return
        try:
            data = json.loads(last_nonblank_line)
        except json.JSONDecodeError:
            file_handle.seek(last_nonblank_start)
            file_handle.truncate()
            file_handle.seek(0, os.SEEK_END)
            return
        try:
            EncryptedFrame(
                version=data["version"],
                salt=data["salt"],
                nonce=data["nonce"],
                ciphertext=data["ciphertext"],
                tag=data["tag"],
            )
        except (KeyError, TypeError) as exc:
            msg = (
                f"Malformed protected-storage final frame at {last_nonblank_start}: record may have been tampered with"
            )
            raise ProtectedStorageError(msg) from exc
        file_handle.seek(0, os.SEEK_END)

    def _check_authorized(self, operation: str) -> None:
        try:
            authorize(
                operation=operation,
                allowlist=self._authorized_principals,
            )
        except UnauthorizedAccessError as exc:
            self._record_unauthorized_access(operation)
            raise exc

    def _record_unauthorized_access(self, operation: str) -> None:
        if self._access_trace_path is None:
            return
        try:
            from .trace import TraceEvent, TraceEventType

            audit_storage = ProtectedStorage(
                self._access_trace_path,
                master_key=self._master_key,
                authorized_principals=self._authorized_principals,
            )
            audit_storage._append_audit_trace_event(
                TraceEvent(
                    event_type=TraceEventType.SCOPE_VIOLATION,
                    agent_scope="orchestrator",
                    event_detail={
                        "agent_id": "protected-storage",
                        "attempted_path": str(self._path),
                        "enforcement": "blocked",
                        "reason": "unauthorized_access",
                        "operation": operation,
                    },
                )
            )
        except Exception:  # noqa: BLE001 - an audit failure must not bypass authorization
            pass

    @staticmethod
    def _read_last_frame_from_handle(file_handle: IO[str]) -> EncryptedFrame | None:
        file_handle.seek(0)
        last_nonblank: str | None = None
        for line in file_handle:
            stripped = line.strip()
            if stripped:
                last_nonblank = stripped
        if last_nonblank is None:
            return None
        data = json.loads(last_nonblank)
        return EncryptedFrame(
            version=data["version"],
            salt=data["salt"],
            nonce=data["nonce"],
            ciphertext=data["ciphertext"],
            tag=data["tag"],
        )

    def append(
        self,
        plaintext: bytes,
        *,
        nonce: bytes | None = None,
        before_append: Callable[[bytes | None], bytes | None] | None = None,
    ) -> None:
        """Encrypt and append ``plaintext`` as one authenticated frame.

        Args:
            plaintext: The exact bytes to protect.
            nonce: Normally omitted (a fresh ``os.urandom(12)`` nonce is
                generated). Callers MUST NOT reuse a nonce within the same
                derived key; doing so raises ``NonceReuseError``.
        """
        self._check_authorized("append")
        self._append_internal(plaintext, nonce=nonce, before_append=before_append)

    def _append_internal(
        self,
        plaintext: bytes,
        *,
        nonce: bytes | None = None,
        before_append: Callable[[bytes | None], bytes | None] | None = None,
    ) -> None:
        aesgcm_cls = _get_aesgcm()
        frame_nonce = nonce if nonce is not None else os.urandom(_NONCE_LEN)
        if len(frame_nonce) != _NONCE_LEN:
            msg = f"Nonce must be {_NONCE_LEN} bytes (96 bits), got {len(frame_nonce)}"
            raise ProtectedStorageError(msg)
        _assert_no_symlink_components(self._path)
        with locked_file(self._path, mode="a+", encoding="utf-8") as handle:
            # Finalize salt selection under the inter-process lock to prevent two
            # freshly constructed instances from each using a different random salt.
            file_handle_rw = cast(IO[str], handle)
            persisted = self._read_salt_from_handle(file_handle_rw)
            if persisted is not None:
                if self._salt is not None and self._salt != persisted:
                    raise ValueError(
                        "caller-supplied salt does not match the salt already persisted in the storage file"
                    )
                self._salt = persisted
            elif self._salt is None:
                self._salt = os.urandom(16)
            self._key = derive_workflow_key(self._master_key, self._salt)
            self._truncate_invalid_final_frame(file_handle_rw)
            assert self._key is not None  # noqa: S101 — invariant enforced above
            aesgcm = aesgcm_cls(self._key)
            if before_append is not None:
                last_plaintext: bytes | None = None
                last_frame = self._read_last_frame_from_handle(file_handle_rw)
                if last_frame is not None:
                    try:
                        frame_salt = base64.b64decode(last_frame.salt)
                    except Exception as exc:  # noqa: BLE001
                        msg = f"Malformed protected-storage frame salt in {self._path}"
                        raise ProtectedStorageError(msg) from exc
                    if frame_salt != self._salt:
                        msg = (
                            "protected storage contains a frame with a salt that does not match "
                            "the workflow's persisted salt"
                        )
                        raise ProtectedStorageError(msg)
                    try:
                        nonce_last = base64.b64decode(last_frame.nonce)
                        ciphertext_last = base64.b64decode(last_frame.ciphertext)
                        tag_last = base64.b64decode(last_frame.tag)
                        aad_last = _frame_aad(last_frame.version, frame_salt)
                        last_plaintext = aesgcm.decrypt(
                            nonce_last,
                            ciphertext_last + tag_last,
                            associated_data=aad_last,
                        )
                    except Exception as exc:  # noqa: BLE001
                        msg = (
                            f"AES-GCM authentication failed for frame in {self._path}: "
                            "record may have been tampered with"
                        )
                        raise ProtectedStorageError(msg) from exc
                replacement_plaintext = before_append(last_plaintext)
                if replacement_plaintext is not None:
                    plaintext = replacement_plaintext
            if frame_nonce in self._used_nonces or frame_nonce in _read_nonces_without_lock(self._path):
                msg = "Nonce reuse detected for this derived key; a fresh cryptographically-random nonce is required"
                raise NonceReuseError(msg)
            aad = _frame_aad(_FRAME_VERSION, self._salt)
            combined = aesgcm.encrypt(frame_nonce, plaintext, associated_data=aad)
            ciphertext, tag = combined[:-16], combined[-16:]
            frame = EncryptedFrame(
                version=_FRAME_VERSION,
                salt=base64.b64encode(self._salt).decode("ascii"),
                nonce=base64.b64encode(frame_nonce).decode("ascii"),
                ciphertext=base64.b64encode(ciphertext).decode("ascii"),
                tag=base64.b64encode(tag).decode("ascii"),
            )
            file_handle = cast(IO[str], handle)
            file_handle.write(json.dumps(frame.to_dict(), sort_keys=True) + "\n")
        try:
            _assert_no_symlink_components(self._path)
            os.chmod(self._path, 0o600)
        except OSError:  # pragma: no cover - platform dependent
            pass
        self._used_nonces.add(frame_nonce)

    def _append_audit_trace_event(self, event: TraceEvent) -> None:
        """Append one encrypted audit trace event without re-entering authorization."""
        from .trace import (
            _effective_timestamp_for_append,
            _last_event_timestamp,
            _serialize_event_with_timestamp,
            serialize_event,
        )

        line = serialize_event(event)

        def _validate_last_timestamp(last_plaintext: bytes | None) -> bytes | None:
            if last_plaintext is None:
                return None
            last_ts = _last_event_timestamp(last_plaintext.decode("utf-8"))
            event_timestamp = event.timestamp
            effective_timestamp = _effective_timestamp_for_append(event, last_ts)
            if effective_timestamp != event_timestamp:
                return (_serialize_event_with_timestamp(event, effective_timestamp) + "\n").encode("utf-8")
            return None

        self._append_internal((line + "\n").encode("utf-8"), before_append=_validate_last_timestamp)

    def read_all(self) -> list[bytes]:
        """Decrypt and return every valid frame's plaintext, in append order.

        A malformed/truncated final line does not prevent earlier, well-formed
        frames from being read. Parseable frames that fail authentication are
        treated as integrity errors, even when they are the final frame.
        """
        self._check_authorized("read_all")
        aesgcm_cls = _get_aesgcm()
        _assert_no_symlink_components(self._path)

        if not self._path.exists():
            return []

        # If no key was derived yet (deferred salt path), derive it now from the
        # first valid frame in the file.  read_all never writes, so there is no
        # race; the file already exists here.
        key = self._key
        if key is None:
            persisted = self._load_persisted_salt()
            if persisted is None:
                if any(frame is not None for _, frame in _iter_frames_with_positions(self._path)):
                    msg = (
                        f"Protected storage at {self._path} contains frame data but no valid "
                        "persisted salt; protected data may be corrupted"
                    )
                    raise ProtectedStorageError(msg)
                return []
            self._salt = persisted
            self._key = derive_workflow_key(self._master_key, persisted)
            key = self._key
        aesgcm = aesgcm_cls(key)
        results: list[bytes] = []
        for position, frame in _iter_frames_with_positions(self._path):
            if frame is None:
                continue
            try:
                nonce = base64.b64decode(frame.nonce)
                ciphertext = base64.b64decode(frame.ciphertext)
                tag = base64.b64decode(frame.tag)
                frame_salt = base64.b64decode(frame.salt)
                aad = _frame_aad(frame.version, frame_salt)
                plaintext = aesgcm.decrypt(nonce, ciphertext + tag, associated_data=aad)
            except Exception as exc:  # noqa: BLE001
                msg = (
                    f"AES-GCM authentication failed for frame {position}"
                    f" (path={self._path}): record may have been tampered with"
                )
                raise ProtectedStorageError(msg) from exc
            results.append(plaintext)
        return results

    def write_snapshot(self, plaintext: bytes) -> str:
        """Persist snapshot bytes and return the matching content-addressed reference."""
        self.append(plaintext)
        return f"sha256:{hashlib.sha256(plaintext).hexdigest()}"

    def delete(self) -> bool:
        """Delete retained data after enforcing the configured allowlist."""
        self._check_authorized("delete")
        _assert_no_symlink_components(self._path)
        try:
            self._path.unlink()
        except FileNotFoundError:
            return False
        self._used_nonces.clear()
        return True


def _iter_frames_with_positions(path: Path) -> Iterator[tuple[int, EncryptedFrame | None]]:
    """Yield frames with physical line positions, tolerating only a final invalid line."""
    if not path.exists():
        return
    with locked_file(path, mode="r", exclusive=False, encoding="utf-8") as handle:
        file_handle = cast(IO[str], handle)
        lines = file_handle.readlines()
    nonblank_positions = [index for index, line in enumerate(lines) if line.strip()]
    last_position = nonblank_positions[-1] if nonblank_positions else -1
    for position, line in enumerate(lines):
        stripped = line.strip()
        if not stripped:
            continue
        try:
            data = json.loads(stripped)
            yield (
                position,
                EncryptedFrame(
                    version=data["version"],
                    salt=data["salt"],
                    nonce=data["nonce"],
                    ciphertext=data["ciphertext"],
                    tag=data["tag"],
                ),
            )
        except json.JSONDecodeError as exc:
            if position == last_position:
                yield position, None
                continue
            msg = f"Malformed protected-storage frame at line {position}: record may have been tampered with"
            raise ProtectedStorageError(msg) from exc
        except (KeyError, TypeError) as exc:
            msg = f"Malformed protected-storage frame at line {position}: record may have been tampered with"
            raise ProtectedStorageError(msg) from exc


def _iter_frames(path: Path, *, skip_invalid: bool) -> Iterator[EncryptedFrame]:
    if not path.exists():
        return
    with locked_file(path, mode="r", exclusive=False, encoding="utf-8") as handle:
        file_handle = cast(IO[str], handle)
        for line in file_handle:
            stripped = line.strip()
            if not stripped:
                continue
            try:
                data = json.loads(stripped)
                yield EncryptedFrame(
                    version=data["version"],
                    salt=data["salt"],
                    nonce=data["nonce"],
                    ciphertext=data["ciphertext"],
                    tag=data["tag"],
                )
            except Exception:  # noqa: BLE001
                if skip_invalid:
                    continue
                raise


def _read_nonces_without_lock(path: Path) -> set[bytes]:
    """Read persisted nonces while the caller holds the storage file lock."""
    if not path.exists():
        return set()
    _assert_no_symlink_components(path)
    nonces: set[bytes] = set()
    with path.open(encoding="utf-8") as handle:
        for line in handle:
            try:
                data = json.loads(line)
                nonce = base64.b64decode(data["nonce"], validate=True)
            except (KeyError, TypeError, ValueError, json.JSONDecodeError):
                continue
            if len(nonce) == _NONCE_LEN:
                nonces.add(nonce)
    return nonces


# --- Authorization (T073) -------------------------------------------------


def _derive_windows_token_identity() -> str:
    """Return the current Windows process identity as a trusted SID string."""
    import ctypes
    from ctypes import wintypes

    win_dll = getattr(ctypes, "WinDLL")
    token_query = 0x0008
    token_user_class = 1

    class _SidAndAttributes(ctypes.Structure):
        _fields_ = [("Sid", wintypes.LPVOID), ("Attributes", wintypes.DWORD)]

    class _TokenUser(ctypes.Structure):
        _fields_ = [("User", _SidAndAttributes)]

    kernel32 = win_dll("kernel32", use_last_error=True)
    advapi32 = win_dll("advapi32", use_last_error=True)

    process_token = wintypes.HANDLE()
    if not advapi32.OpenProcessToken(kernel32.GetCurrentProcess(), token_query, ctypes.byref(process_token)):
        raise OSError("OpenProcessToken failed")
    try:
        required = wintypes.DWORD()
        advapi32.GetTokenInformation(process_token, token_user_class, None, 0, ctypes.byref(required))
        if required.value <= 0:
            raise OSError("GetTokenInformation returned no token-user payload")

        buffer = ctypes.create_string_buffer(required.value)
        if not advapi32.GetTokenInformation(
            process_token,
            token_user_class,
            buffer,
            required.value,
            ctypes.byref(required),
        ):
            raise OSError("GetTokenInformation failed")

        token_user = ctypes.cast(buffer, ctypes.POINTER(_TokenUser)).contents
        sid_string = wintypes.LPWSTR()
        if not advapi32.ConvertSidToStringSidW(token_user.User.Sid, ctypes.byref(sid_string)):
            raise OSError("ConvertSidToStringSidW failed")
        try:
            if not sid_string.value:
                raise OSError("ConvertSidToStringSidW returned an empty SID")
            return f"sid:{sid_string.value}"
        finally:
            kernel32.LocalFree(sid_string)
    finally:
        kernel32.CloseHandle(process_token)


def derive_caller_identity() -> str:
    """Derive the caller's identity from a trusted, non-caller-supplied source.

    On POSIX, this is the OS process owner (``os.getuid()`` resolved via
    ``pwd.getpwuid``). This value can never be influenced by a caller
    argument or a plain environment variable, which is required so that an
    asserted allowlisted principal name cannot bypass the authorization check.

    When POSIX account lookup is unavailable, the function falls back to a
    trusted numeric UID only when ``os.getuid`` exists. On Windows, where
    ``pwd`` and ``os.getuid`` are normally unavailable, it instead resolves the
    current process token SID. If no trusted identity source is available,
    identity derivation fails closed.
    """
    try:
        import pwd

        return pwd.getpwuid(os.getuid()).pw_name
    except (ImportError, KeyError, AttributeError):  # pragma: no cover - non-POSIX platform
        if hasattr(os, "getuid"):
            return f"uid:{os.getuid()}"
        if sys.platform == "win32":
            try:
                return _derive_windows_token_identity()
            except Exception as exc:  # noqa: BLE001 - normalize all Windows identity failures to fail-closed auth
                raise UnauthorizedAccessError(
                    "Unable to derive caller identity from trusted identity sources on this platform"
                ) from exc
        raise UnauthorizedAccessError("Unable to derive caller identity from trusted identity sources on this platform")


def authorize(
    *,
    operation: str,
    allowlist: frozenset[str],
    asserted_identity: str | None = None,  # noqa: ARG001 - intentionally ignored; documents the rejected bypass vector
) -> str:
    """Authorize an operation against the configuration-declared allowlist.

    Args:
        operation: A short description of the attempted operation (for
            trace/error messages only).
        allowlist: The workflow configuration's authorized-principals list.
        asserted_identity: Deliberately ignored. Any caller-supplied identity
            claim MUST NOT influence the authorization decision — the
            identity used below always comes from ``derive_caller_identity``.

    Returns:
        The derived identity, when authorized.

    Raises:
        UnauthorizedAccessError: When the derived identity is not present in
            ``allowlist``.
    """
    derived_identity = derive_caller_identity()
    if derived_identity not in allowlist:
        msg = f"Identity '{derived_identity}' is not authorized to perform '{operation}'"
        raise UnauthorizedAccessError(msg)
    return derived_identity
