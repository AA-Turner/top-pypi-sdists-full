"""Where `plato vault app` keeps an account's app credentials, behind one interface.

Phase 1 is :class:`LocalFileStore`: one JSON file per account (mode 600, directories 700, atomic replace).

``lock`` is what keeps a single-use refresh token single-use: every refresh
re-reads the record under it, so two processes never send the same refresh token.
"""

from __future__ import annotations

import errno
import fcntl
import json
import os
import tempfile
import time
from collections.abc import Iterator
from contextlib import AbstractContextManager, contextmanager
from pathlib import Path
from typing import Protocol

from pydantic import ValidationError

from plato.chronos.login_vault import normalize_key
from plato.cli.vault.app_models import AppCredentials
from plato.cli.vault.client import VaultConsoleError

STORE_DIR_ENV_VAR = "PLATO_VAULT_APPS_DIR"
DEFAULT_STORE_DIR = Path.home() / ".plato-creds" / "vault-apps"
LOCK_TIMEOUT_S = 60.0


class StoreError(VaultConsoleError):
    """The store could not be read, written or locked. Its text never quotes a value."""


class LockTimeout(StoreError):
    """Another process held the account's lock too long (a refresh that hangs?)."""

    exit_code = 3


class AppStore(Protocol):
    def load(self, login_key: str, account: str) -> AppCredentials | None: ...

    def save(self, creds: AppCredentials) -> None: ...

    def lock(self, login_key: str, account: str) -> AbstractContextManager[None]: ...

    def where(self, login_key: str, account: str) -> str: ...


def _slugs(login_key: str, account: str) -> tuple[str, str]:
    lk, ac = normalize_key(login_key), normalize_key(account)
    if not lk or not ac:
        raise StoreError("login_key and account must hold at least one letter or digit")
    return lk, ac


class LocalFileStore:
    """The phase-1 store: files on this machine only."""

    def __init__(self, root: Path | None = None) -> None:
        env = os.environ.get(STORE_DIR_ENV_VAR)
        self.root = root or (Path(env) if env else DEFAULT_STORE_DIR)

    def _path(self, login_key: str, account: str) -> Path:
        lk, ac = _slugs(login_key, account)
        return self.root / lk / f"{ac}.json"

    def where(self, login_key: str, account: str) -> str:
        return str(self._path(login_key, account))

    def _ensure_dir(self, path: Path) -> None:
        """Make the root and the login_key directory, 700 whatever the umask says."""
        try:
            self.root.parent.mkdir(parents=True, exist_ok=True)
            for d in (self.root, path.parent):
                d.mkdir(mode=0o700, exist_ok=True)
                os.chmod(d, 0o700)
        except OSError as e:
            raise StoreError(f"cannot make {path.parent}: {_why(e)}") from None

    def load(self, login_key: str, account: str) -> AppCredentials | None:
        path = self._path(login_key, account)
        try:
            raw = path.read_text()
        except FileNotFoundError:
            return None
        except OSError as e:
            raise StoreError(f"cannot read {path}: {e.strerror}") from None
        try:
            return AppCredentials.model_validate(json.loads(raw))
        except (ValueError, ValidationError):
            # Never chain the error: pydantic and json quote the input, which holds the secrets.
            raise StoreError(f"{path} is not a valid app record; fix or remove it by hand") from None

    def save(self, creds: AppCredentials) -> None:
        """An atomic replace of the record (see :func:`atomic_write`)."""
        path = self._path(creds.login_key, creds.account)
        self._ensure_dir(path)
        atomic_write(path, json.dumps(creds.model_dump(mode="json", context={"reveal": True}), indent=1))

    @contextmanager
    def lock(self, login_key: str, account: str, timeout_s: float = LOCK_TIMEOUT_S) -> Iterator[None]:
        """An exclusive ``flock`` on ``<account>.lock`` next to the record. ``flock``
        (not ``lockf``) so two threads of one process also exclude each other."""
        path = self._path(login_key, account).with_suffix(".lock")
        self._ensure_dir(path)
        try:
            fd = os.open(path, os.O_RDWR | os.O_CREAT, 0o600)
        except OSError as e:
            raise StoreError(f"cannot open {path}: {_why(e)}") from None
        try:
            deadline = time.monotonic() + timeout_s
            while True:
                try:
                    fcntl.flock(fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
                    break
                except OSError as e:
                    if e.errno not in (errno.EAGAIN, errno.EACCES):
                        raise StoreError(f"cannot lock {path}: {e.strerror}") from None
                    if time.monotonic() >= deadline:
                        raise LockTimeout(
                            f"{path} stayed locked for {timeout_s:.0f} s: another refresh of this account is "
                            "running. Wait for it, then try again"
                        ) from None
                    time.sleep(0.05)
            try:
                yield
            finally:
                fcntl.flock(fd, fcntl.LOCK_UN)
        finally:
            os.close(fd)


def _why(error: OSError) -> str:
    return error.strerror or type(error).__name__


def atomic_write(path: Path, text: str) -> None:
    """Write ``text`` to a 600 temp file in ``path``'s directory, fsync, then rename it
    over ``path``: a reader sees the old file or the new one, never half of one.

    On any failure, also Ctrl-C, the temp file (it holds the secrets) is deleted.
    Only an ``OSError`` becomes a :class:`StoreError`; other errors raise as they are."""
    try:
        fd, tmp = tempfile.mkstemp(prefix=f".{path.name}.", suffix=".tmp", dir=path.parent)
    except OSError as e:
        raise StoreError(f"cannot write {path}: {_why(e)}") from None
    try:
        try:
            f = os.fdopen(fd, "w")
        except BaseException:
            os.close(fd)
            raise
        with f:
            os.fchmod(f.fileno(), 0o600)
            f.write(text)
            f.flush()
            os.fsync(f.fileno())
        os.replace(tmp, path)
    except BaseException as e:
        try:
            os.unlink(tmp)
        except OSError:
            pass
        if isinstance(e, OSError):
            raise StoreError(f"cannot write {path}: {_why(e)}") from None
        raise
    # The replace is done, so the new file is in place. The directory fsync only
    # makes the rename durable sooner: a failure here is not a failed write.
    try:
        dir_fd = os.open(path.parent, os.O_RDONLY)
        try:
            os.fsync(dir_fd)
        finally:
            os.close(dir_fd)
    except OSError:
        pass


def default_store() -> AppStore:
    """The store the CLI uses. Tests patch this (or set ``PLATO_VAULT_APPS_DIR``)."""
    return LocalFileStore()
