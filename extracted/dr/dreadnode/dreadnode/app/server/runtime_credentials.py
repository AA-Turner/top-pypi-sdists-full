"""Resolve the bearer credential a runtime server accepts.

The current platform provisions one immutable credential in
``DREADNODE_RUNTIME_TOKEN``. For N-1 rollback, a newly provisioned runtime also
materializes that value at ``DREADNODE_RUNTIME_TOKEN_FILE``: the previous
platform release can rotate the file during its legacy reconnect flow after a
rollback. The current platform never writes the file after startup.

When the file is configured it becomes authoritative as soon as it contains a
credential. A retired environment value is never resurrected if the file later
becomes unavailable. Credential replacement is detected synchronously on auth
checks, and listeners are notified so token-bound WebSockets and tickets can be
revoked.
"""

import os
import secrets
import stat
import threading
import typing as t
from pathlib import Path

from loguru import logger

from dreadnode.app.env import read_env_with_deprecation

__all__ = [
    "RuntimeCredentialMaterializationError",
    "RuntimeCredentialSource",
    "get_credential_source",
    "materialize_runtime_token_file",
    "read_runtime_token",
    "reset_credential_source",
]

_TOKEN_FILE_ENV = "DREADNODE_RUNTIME_TOKEN_FILE"  # noqa: S105 - env name, not a secret


class _CredentialUnavailableError(Exception):
    """The configured file cannot be read without risking stale fallback."""


class RuntimeCredentialMaterializationError(RuntimeError):
    """A configured rollback credential file could not be established safely."""


def _read_env_token() -> str | None:
    """Read the provisioned environment credential with legacy fallback."""
    return read_env_with_deprecation(
        "DREADNODE_RUNTIME_TOKEN",
        "SANDBOX_AUTH_TOKEN",
    )


def read_runtime_token() -> str | None:
    """Return the credential for subprocess and worker callbacks.

    A missing file is a pre-materialization state and falls back to the
    provisioned environment value. Any other file read failure fails closed:
    the environment may contain a credential that an N-1 reconnect retired.
    """
    path_value = os.environ.get(_TOKEN_FILE_ENV)
    if not path_value:
        return _read_env_token()

    try:
        return Path(path_value).read_text(encoding="utf-8").strip() or None
    except FileNotFoundError:
        return _read_env_token()
    except OSError as exc:
        logger.warning("Failed to read runtime credential file {}: {}", path_value, exc)
        return None


def _atomic_write(path: Path, content: str) -> None:
    """Atomically write a credential file with owner-only permissions."""
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(
        f"{path.name}.{os.getpid()}.{secrets.token_hex(8)}.tmp",
    )
    descriptor: int | None = None
    try:
        descriptor = os.open(
            temporary,
            os.O_WRONLY | os.O_CREAT | os.O_EXCL,
            0o600,
        )
        with os.fdopen(descriptor, "w", encoding="utf-8") as handle:
            descriptor = None
            handle.write(content)
            handle.flush()
            os.fsync(handle.fileno())
        temporary.replace(path)
    finally:
        if descriptor is not None:
            os.close(descriptor)
        try:
            temporary.unlink(missing_ok=True)
        except OSError:
            logger.warning("Failed to clean up temporary runtime credential file {}", temporary)


def materialize_runtime_token_file() -> Path | None:
    """Establish and verify the configured N-1 reconnect token file.

    Returns ``None`` when no file is configured. With a configured path, returns
    that path only after verifying a nonempty credential and exact ``0600``
    permissions. Any failure raises :class:`RuntimeCredentialMaterializationError`
    so server startup cannot continue in an env-only state that N-1 would later
    consider non-rotatable.

    Existing content always wins so a restart cannot overwrite a credential
    already rotated by the previous platform release. An unreadable existing
    file is therefore a hard failure, never a reason to restore the environment
    credential over it.
    """
    path_value = os.environ.get(_TOKEN_FILE_ENV)
    if not path_value:
        return None

    path = Path(path_value)
    try:
        exists = path.exists()
    except OSError as exc:
        raise RuntimeCredentialMaterializationError(
            f"Failed to inspect configured runtime credential file {path_value}: {exc}",
        ) from exc

    if exists:
        try:
            existing = path.read_text(encoding="utf-8").strip()
        except OSError as exc:
            raise RuntimeCredentialMaterializationError(
                f"Configured runtime credential file is unreadable: {path_value}: {exc}",
            ) from exc
        if not existing:
            token = _read_env_token()
            if token is None or not token.strip():
                raise RuntimeCredentialMaterializationError(
                    f"Configured runtime credential file is empty and no credential is available: "
                    f"{path_value}",
                )
            try:
                _atomic_write(path, token.strip())
            except OSError as exc:
                raise RuntimeCredentialMaterializationError(
                    f"Failed to populate configured runtime credential file {path_value}: {exc}",
                ) from exc
    else:
        token = _read_env_token()
        if token is None or not token.strip():
            raise RuntimeCredentialMaterializationError(
                f"Cannot create configured runtime credential file without a credential: "
                f"{path_value}",
            )
        try:
            _atomic_write(path, token.strip())
        except OSError as exc:
            raise RuntimeCredentialMaterializationError(
                f"Failed to create configured runtime credential file {path_value}: {exc}",
            ) from exc

    try:
        path.chmod(0o600)
        actual = path.read_text(encoding="utf-8").strip()
        mode = stat.S_IMODE(path.stat().st_mode)
    except OSError as exc:
        raise RuntimeCredentialMaterializationError(
            f"Failed to verify configured runtime credential file {path_value}: {exc}",
        ) from exc

    if not actual:
        raise RuntimeCredentialMaterializationError(
            f"Configured runtime credential file failed readback verification: {path_value}",
        )
    # The final file is authoritative. N-1 may observe and atomically rotate a
    # pre-existing or newly-created file before this readback; any final
    # nonempty owner-only value is therefore a valid established credential.
    if mode != 0o600:
        raise RuntimeCredentialMaterializationError(
            f"Configured runtime credential file must have mode 0600, got {mode:04o}: {path_value}",
        )
    return path


class RuntimeCredentialSource:
    """Thread-safe resolver for the runtime server's active credential.

    The optional retirement callback runs after the internal lock is released.
    It should remain cheap and non-blocking because an authentication request
    observes and reports the replacement synchronously.
    """

    def __init__(
        self,
        *,
        on_retire: "t.Callable[[str], None] | None" = None,
    ) -> None:
        self._on_retire = on_retire
        self._lock = threading.RLock()
        self._current: str | None = None
        # Once a real file credential is observed, the environment credential
        # is necessarily only a stale provisioning artifact.
        self._file_backed = False

    def set_on_retire(self, on_retire: "t.Callable[[str], None] | None") -> None:
        """Install or clear the callback invoked for a retired credential."""
        with self._lock:
            self._on_retire = on_retire

    def _read_credential(self) -> str | None:
        path_value = os.environ.get(_TOKEN_FILE_ENV)
        if not path_value:
            return _read_env_token()

        try:
            value = Path(path_value).read_text(encoding="utf-8").strip()
        except FileNotFoundError:
            if self._file_backed:
                raise _CredentialUnavailableError(f"{path_value} vanished") from None
            return _read_env_token()
        except OSError as exc:
            raise _CredentialUnavailableError(f"{path_value}: {exc}") from exc

        if value:
            self._file_backed = True
        return value or None

    def _refresh(self) -> str | None:
        """Refresh current state and return the credential just retired."""
        try:
            resolved = self._read_credential()
        except _CredentialUnavailableError as exc:
            logger.warning("Runtime credential file unavailable; keeping current value: {}", exc)
            return None

        # A replacement always writes a complete, non-empty credential. Retain
        # the last known value across an empty/partial write so auth never opens
        # and active clients are not spuriously retired.
        if resolved is None:
            return None
        if self._current is not None and secrets.compare_digest(resolved, self._current):
            return None

        retired = self._current
        self._current = resolved
        return retired

    def _fire_retire(self, retired: str | None) -> None:
        if retired is None:
            return
        callback = self._on_retire
        if callback is None:
            return
        try:
            callback(retired)
        except Exception:
            logger.exception("Runtime credential retirement callback failed")

    def enabled(self) -> bool:
        """Return whether runtime authentication is configured.

        A configured path keeps authentication enabled. If its last observed
        value becomes temporarily unreadable, that value remains active; if no
        value was ever observed, nothing is accepted. Neither case fails open.

        This check deliberately performs no file I/O. Callers that present a
        credential follow it with :meth:`is_active`, which refreshes once from
        the authoritative source. Keeping configuration detection separate
        avoids reading the rollback-only file twice for every authentication.
        """
        with self._lock:
            return (
                self._current is not None
                or bool(os.environ.get(_TOKEN_FILE_ENV))
                or _read_env_token() is not None
            )

    def is_active(self, presented: str) -> bool:
        """Return whether ``presented`` is the current credential.

        Every check reconciles with the file. A rotated-out value therefore
        cannot authorize a fresh REST request, WebSocket, or ticket even if no
        other request has observed the replacement yet.
        """
        with self._lock:
            retired = self._refresh()
            active = self._current is not None and secrets.compare_digest(
                presented,
                self._current,
            )
        self._fire_retire(retired)
        return active


_source_lock = threading.Lock()
_source: RuntimeCredentialSource | None = None


def get_credential_source() -> RuntimeCredentialSource:
    """Return the process-wide credential source."""
    global _source  # noqa: PLW0603
    with _source_lock:
        if _source is None:
            _source = RuntimeCredentialSource()
        return _source


def reset_credential_source(**kwargs: t.Any) -> RuntimeCredentialSource:
    """Replace the process-wide credential source for tests."""
    global _source  # noqa: PLW0603
    with _source_lock:
        _source = RuntimeCredentialSource(**kwargs)
        return _source
