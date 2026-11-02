"""Where a user's refresh token lives between Python processes.

Only the refresh token needs real persistence: the access token is
short-lived and cheap to refetch, and is cached alongside it only so a warm
process avoids a refresh it doesn't need. ``default_store`` prefers the OS
keychain — through ``/usr/bin/security`` on macOS, ``keyring`` elsewhere — and
falls back to a permissioned file when no real keyring backend is importable
(common on headless Linux).
"""

from __future__ import annotations

import contextlib
import json
import os
import stat
import subprocess
import sys
from pathlib import Path
from typing import Any, Protocol, runtime_checkable

from databaas_utils.errors import ConfigurationError


def config_dir() -> Path:
    """Where profiles live: ``$DATABAAS_CONFIG_DIR`` or ``~/.config/databaas``."""
    override = os.environ.get("DATABAAS_CONFIG_DIR")
    if override:
        return Path(override)
    return Path.home() / ".config" / "databaas"


def cache_dir() -> Path:
    """Where cached sessions live: ``$DATABAAS_CACHE_DIR`` or ``~/.cache/databaas``."""
    override = os.environ.get("DATABAAS_CACHE_DIR")
    if override:
        return Path(override)
    return Path.home() / ".cache" / "databaas"


@runtime_checkable
class TokenStore(Protocol):
    """Anything that can hold one JSON-able blob per key."""

    def load(self, key: str) -> dict[str, Any] | None:
        """The blob stored under ``key``, or ``None``."""
        ...

    def save(self, key: str, data: dict[str, Any]) -> None:
        """Store ``data`` under ``key``, replacing any existing blob."""
        ...

    def delete(self, key: str) -> None:
        """Forget ``key``. A no-op if nothing is stored."""
        ...


def _safe_filename(key: str) -> str:
    return key.replace("/", "_").replace(os.sep, "_")


class FileStore:
    """A 0600 JSON file per key. The fallback when no keyring backend works.

    Args:
        directory: Where to write; ``<cache_dir>/tokens`` by default.
    """

    def __init__(self, directory: Path | None = None) -> None:
        self._dir = directory or (cache_dir() / "tokens")

    def _path(self, key: str) -> Path:
        return self._dir / f"{_safe_filename(key)}.json"

    def load(self, key: str) -> dict[str, Any] | None:
        """The blob stored under ``key``; ``None`` if absent or unreadable."""
        path = self._path(key)
        if not path.exists():
            return None
        try:
            return dict(json.loads(path.read_text()))
        except (json.JSONDecodeError, OSError):
            return None

    def save(self, key: str, data: dict[str, Any]) -> None:
        """Write ``data`` to a file readable only by the current user."""
        self._dir.mkdir(parents=True, exist_ok=True)
        path = self._path(key)
        path.write_text(json.dumps(data))
        path.chmod(stat.S_IRUSR | stat.S_IWUSR)

    def delete(self, key: str) -> None:
        """Remove the file for ``key`` if it exists."""
        self._path(key).unlink(missing_ok=True)


class KeyringStore:
    """Backed by the OS keychain through the ``keyring`` package.

    Covers macOS Keychain, Windows Credential Manager and Secret Service.
    Needs the ``login`` extra.
    """

    _SERVICE = "databaas-utils"

    def _hint(self, key: str) -> str:
        profile = key.split("@", 1)[0]
        return (
            "On macOS this happens when another Python installation created the "
            f"entry: run `databaas logout --profile {profile}` from that "
            f"installation, or delete the {self._SERVICE!r} entry for {key!r} in "
            "Keychain Access, then log in again. Logging in under another "
            "--profile, or with DATABAAS_TOKEN_STORE=file, avoids the entry."
        )

    def load(self, key: str) -> dict[str, Any] | None:
        """The blob stored under ``key``; ``None`` if absent or unreadable."""
        import keyring

        raw = keyring.get_password(self._SERVICE, key)
        if raw is None:
            return None
        try:
            return dict(json.loads(raw))
        except json.JSONDecodeError:
            return None

    def save(self, key: str, data: dict[str, Any]) -> None:
        """Store ``data`` in the OS keychain.

        Raises:
            ConfigurationError: If the keychain refuses, for instance because
                another program owns the existing entry.
        """
        import keyring
        from keyring.errors import KeyringError

        try:
            keyring.set_password(self._SERVICE, key, json.dumps(data))
        except KeyringError as exc:
            raise ConfigurationError(
                f"could not save the login for {key!r} in the OS keychain "
                f"({exc}). {self._hint(key)}"
            ) from exc

    def delete(self, key: str) -> None:
        """Remove ``key`` from the keychain if present.

        Raises:
            ConfigurationError: If the entry exists but the keychain refuses to
                remove it.
        """
        import keyring
        from keyring.errors import PasswordDeleteError

        try:
            keyring.delete_password(self._SERVICE, key)
        except PasswordDeleteError as exc:
            # keyring raises this for a missing entry too; only a refusal is an error.
            if keyring.get_password(self._SERVICE, key) is not None:
                raise ConfigurationError(
                    f"could not remove the login for {key!r} from the OS keychain "
                    f"({exc}). {self._hint(key)}"
                ) from exc


class MacKeychainStore:
    """The refresh token in the macOS Keychain, the rest in a 0600 file.

    macOS ties a Keychain entry to the binary that created it, and only that
    binary may replace or remove it. Through ``keyring`` that binary is the
    Python interpreter, so a uv Python upgrade or another virtualenv could no
    longer save the rotated refresh token (``-25244``). Going through Apple's
    ``/usr/bin/security`` keeps the owner the same for every interpreter.

    ``security -i`` reads the secret from stdin, keeping it out of the process
    list, but caps a command at about 4 KB; that fits a refresh token but not
    a full bundle with an access token, so the access token is cached in a
    file instead.

    Args:
        cache: Holds everything but the refresh token; ``<cache_dir>/sessions``
            by default.
    """

    _SERVICE = "databaas-refresh-token"
    # Where KeyringStore kept the whole bundle before 0.5.2.
    _LEGACY_SERVICE = KeyringStore._SERVICE
    _SECURITY = "/usr/bin/security"
    _NOT_FOUND = 44
    _MAX_COMMAND = 4000

    def __init__(self, cache: FileStore | None = None) -> None:
        self._cache = cache or FileStore(cache_dir() / "sessions")

    def _run(
        self, args: list[str], stdin: str | None = None
    ) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [self._SECURITY, *args],
            input=stdin,
            capture_output=True,
            text=True,
            check=False,
        )

    @staticmethod
    def _check_key(key: str) -> None:
        if any(c in key for c in '"\\\n'):
            raise ConfigurationError(
                f"cannot keep the login for {key!r} in the macOS Keychain: the "
                "profile name contains a quote, backslash or newline. Use another "
                "--profile, or DATABAAS_TOKEN_STORE=file."
            )

    def load(self, key: str) -> dict[str, Any] | None:
        """The cached session for ``key`` with its refresh token; ``None`` if absent.

        Raises:
            ConfigurationError: If the Keychain refuses the read.
        """
        data = self._cache.load(key) or {}
        result = self._run(
            ["find-generic-password", "-s", self._SERVICE, "-a", key, "-w"]
        )
        if result.returncode == 0:
            data["refresh_token"] = result.stdout.rstrip("\n")
        elif result.returncode != self._NOT_FOUND:
            raise ConfigurationError(
                f"could not read the login for {key!r} from the macOS Keychain "
                f"({result.stderr.strip()})"
            )
        return data or None

    def save(self, key: str, data: dict[str, Any]) -> None:
        """Store the refresh token in the Keychain and the rest in the cache file.

        Raises:
            ConfigurationError: If the Keychain refuses, or the refresh token is
                too long to pass to ``security``.
        """
        self._check_key(key)
        rest = {k: v for k, v in data.items() if k != "refresh_token"}
        refresh_token = data.get("refresh_token")
        if refresh_token:
            command = (
                f'add-generic-password -U -s "{self._SERVICE}" -a "{key}" '
                f'-X "{str(refresh_token).encode().hex()}"\n'
            )
            if len(command) > self._MAX_COMMAND:
                raise ConfigurationError(
                    f"the refresh token for {key!r} is too long for the macOS "
                    "Keychain helper. Log in with DATABAAS_TOKEN_STORE=file."
                )
            result = self._run(["-i"], stdin=command)
            if result.returncode != 0:
                raise ConfigurationError(
                    f"could not save the login for {key!r} in the macOS Keychain "
                    f"({result.stderr.strip()})"
                )
        else:
            self._delete_secret(key)
        self._cache.save(key, rest)

    def delete(self, key: str) -> None:
        """Remove ``key`` from the Keychain and the cache. A no-op if absent.

        Also tries to remove a pre-0.5.2 ``databaas-utils`` entry for ``key``;
        that only succeeds from the interpreter that created it, so check
        :meth:`has_legacy_entry` afterwards.

        Raises:
            ConfigurationError: If the Keychain refuses to remove the entry.
        """
        self._delete_secret(key)
        self._cache.delete(key)
        if self.has_legacy_entry(key):
            with contextlib.suppress(Exception):
                import keyring

                keyring.delete_password(self._LEGACY_SERVICE, key)

    def has_legacy_entry(self, key: str) -> bool:
        """Whether a pre-0.5.2 ``databaas-utils`` Keychain entry exists for ``key``.

        Reads attributes only, so the Keychain never asks for access.
        """
        result = self._run(
            ["find-generic-password", "-s", self._LEGACY_SERVICE, "-a", key]
        )
        return result.returncode == 0

    def _delete_secret(self, key: str) -> None:
        result = self._run(["delete-generic-password", "-s", self._SERVICE, "-a", key])
        if result.returncode not in (0, self._NOT_FOUND):
            raise ConfigurationError(
                f"could not remove the login for {key!r} from the macOS Keychain "
                f"({result.stderr.strip()})"
            )


def default_store() -> TokenStore:
    """The OS keychain when one is available, else ``FileStore``.

    On macOS that is ``MacKeychainStore``; elsewhere ``KeyringStore``.
    ``keyring`` degrades to ``keyrings.alt.file.PlaintextKeyring`` or
    ``keyring.backends.fail.Keyring`` when no OS backend is importable; neither
    is worth preferring over a permissioned file, so both fall through to
    ``FileStore``. ``DATABAAS_TOKEN_STORE=file|keyring`` forces a choice.
    """
    forced = os.environ.get("DATABAAS_TOKEN_STORE")
    if forced == "file":
        return FileStore()
    if sys.platform == "darwin" and Path(MacKeychainStore._SECURITY).exists():
        return MacKeychainStore()
    if forced == "keyring":
        return KeyringStore()
    try:
        import keyring
        from keyring.backends.fail import Keyring as FailKeyring

        backend = keyring.get_keyring()
        module = type(backend).__module__
        if isinstance(backend, FailKeyring) or "keyrings.alt" in module:
            return FileStore()
        return KeyringStore()
    except ImportError:
        return FileStore()


def store_lock(key: str) -> Any:
    """A cross-process lock guarding refresh-token rotation for ``key``.

    Zitadel rotates the refresh token on every use, so two processes refreshing
    the same stored token at once would each save a rotated token and
    invalidate the other's — this lock serialises "load, maybe refresh, save"
    across processes, not just threads.
    """
    from filelock import FileLock

    lock_dir = cache_dir() / "locks"
    lock_dir.mkdir(parents=True, exist_ok=True)
    return FileLock(str(lock_dir / f"{_safe_filename(key)}.lock"))
