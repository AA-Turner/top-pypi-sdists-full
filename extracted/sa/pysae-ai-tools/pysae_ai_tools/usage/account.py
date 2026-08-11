"""Identity of the active Claude account, and per-account state directories.

The usage subsystem persists several state files (usage cache, lock, primer state and
log, notification dedup levels, spend history, unblock override). A user juggling two
Claude plans needs those metrics kept apart, one plan never bleeding into the other.

The OAuth access token in ``~/.claude/.credentials.json`` rotates, so it cannot key an
account. The identity lives in ``~/.claude.json`` under ``oauthAccount`` (``accountUuid`` /
``emailAddress`` / ``organizationName``) and survives token rotation.

Each account owns a directory ``<data>/assistants/claude/accounts/<key>/`` (XDG data dir)
where ``key`` is the ``accountUuid`` alone. Only the uuid is stable: Claude Code rewrites
``oauthAccount`` field by field during a ``/login``, so ``organizationName`` and
``emailAddress`` are briefly absent, or mismatched (the previous org next to the new email).
Mixing them into the key made the *same* account resolve to different directories from one
hook invocation to the next — splitting its state and, worst of all, hiding the unblock
override so a lifted block silently came back. The org/email only survive as a display label
in ``account.json``. :func:`ensure_dir` writes that label the first time a directory appears.

State files are written under the *active* account's directory; a non-active account can only
be *read* (no token to fetch with), via :func:`resolve`.
"""

import json
import os
import re
from dataclasses import dataclass
from pathlib import Path

from ..config import assistant_data_dir

BASE_DIR = assistant_data_dir("claude")
ACCOUNTS_DIR = BASE_DIR / "accounts"
SETTINGS_PATH = Path.home() / ".claude.json"

# Optional override, read only by the CLI read paths (`usage show/history --account`), never
# by the write paths — hooks/statusline/primer always target the real active account.
ACCOUNT_ENV = "PYSAE_AI_TOOLS_ACCOUNT"

DEFAULT_KEY = "default"
META_FILE = "account.json"

_SANITIZE_RE = re.compile(r"[^0-9A-Za-z._-]+")


@dataclass
class Account:
    """A Claude account identity. ``key`` is the on-disk directory name."""

    key: str
    uuid: str | None
    email: str | None
    org_name: str | None
    org_type: str | None

    @property
    def label(self) -> str:
        """Human-readable name for display, most specific first."""
        return self.email or self.org_name or self.uuid or "compte par défaut"


def _sanitize(value: str) -> str:
    return _SANITIZE_RE.sub("-", value).strip("-").lower()


def _compose_key(uuid: str) -> str:
    """On-disk key for an account: its ``accountUuid``, the only field stable across a login.

    Sanitized because a real uuid (``[0-9a-f-]``) passes through untouched, but a malformed
    ``accountUuid`` must never inject a path separator into the key (path traversal).
    """
    return _sanitize(uuid) or DEFAULT_KEY


def _read_settings() -> dict[str, object]:
    """Read ``~/.claude.json`` as UTF-8 JSON; empty dict on any failure.

    ``errors="replace"`` and the broad ``ValueError`` catch matter because this runs at import
    time (the path constants resolve through here): a stray non-UTF-8 byte would otherwise raise
    ``UnicodeDecodeError`` and crash the import of the whole usage subsystem, not just one call."""
    try:
        data = json.loads(SETTINGS_PATH.read_text(encoding="utf-8", errors="replace"))
    except (OSError, ValueError):
        return {}
    return data if isinstance(data, dict) else {}


def _str_or_none(value: object) -> str | None:
    return value if isinstance(value, str) and value else None


def _account_from_oauth(oauth: dict[str, object]) -> Account | None:
    uuid = _str_or_none(oauth.get("accountUuid"))
    if uuid is None:
        return None
    email = _str_or_none(oauth.get("emailAddress"))
    org_name = _str_or_none(oauth.get("organizationName"))
    org_type = _str_or_none(oauth.get("organizationType"))
    return Account(key=_compose_key(uuid), uuid=uuid, email=email, org_name=org_name, org_type=org_type)


def current_account() -> Account | None:
    """The active Claude account from ``~/.claude.json`` (``oauthAccount``).

    Returns None when no OAuth account is recorded (API-key mode, or a Claude Code old
    enough not to persist it) — callers then fall back to the ``default`` state directory.
    """
    oauth = _read_settings().get("oauthAccount")
    if not isinstance(oauth, dict):
        return None
    return _account_from_oauth(oauth)


def env_ref() -> str:
    """Account reference from ``PYSAE_AI_TOOLS_ACCOUNT`` (the env fallback for ``--account``)."""
    return os.environ.get(ACCOUNT_ENV, "").strip()


def account_key(account: Account | None) -> str:
    return account.key if account is not None else DEFAULT_KEY


def state_dir(account: Account | None = None) -> Path:
    """Directory holding ``account``'s state files. Pure: no mkdir, no migration.

    ``account`` None resolves the active account (or the ``default`` bucket)."""
    resolved = account if account is not None else current_account()
    return ACCOUNTS_DIR / account_key(resolved)


def active_state_dir() -> Path:
    """State directory for the active account — the base of every write path."""
    return state_dir(current_account())


def ensure_dir(directory: Path) -> None:
    """Create ``directory``, and name it the first time it appears.

    Every write path goes through here. A uuid-keyed directory says nothing about whose state
    it holds, so ``account.json`` is what lets :func:`list_accounts` name it later; writing it
    only when it is missing keeps the identity lookup off the repeated write path.
    """
    try:
        directory.mkdir(parents=True, exist_ok=True)
        if (directory / META_FILE).exists():
            return
    except OSError:
        return
    active = current_account()
    if active is not None and active.key == directory.name:
        write_account_meta(active)


def write_account_meta(account: Account) -> None:
    """Persist ``account``'s identity next to its state, so a non-active account can still be
    named and resolved later (``~/.claude.json`` only carries the logged-in one). Best-effort."""
    try:
        target = state_dir(account)
        target.mkdir(parents=True, exist_ok=True)
        (target / META_FILE).write_text(
            json.dumps(
                {
                    "uuid": account.uuid,
                    "email": account.email,
                    "org_name": account.org_name,
                    "org_type": account.org_type,
                },
                ensure_ascii=False,
            ),
            encoding="utf-8",
        )
    except OSError:
        pass


def _account_from_meta(directory: Path) -> Account | None:
    try:
        data = json.loads((directory / META_FILE).read_text(encoding="utf-8", errors="replace"))
    except (OSError, ValueError):
        return None
    if not isinstance(data, dict):
        return None
    return Account(
        key=directory.name,
        uuid=_str_or_none(data.get("uuid")),
        email=_str_or_none(data.get("email")),
        org_name=_str_or_none(data.get("org_name")),
        org_type=_str_or_none(data.get("org_type")),
    )


def list_accounts() -> list[Account]:
    """Every account with a state directory, from its persisted ``account.json``.

    A directory with no readable meta still counts: its name *is* the uuid, so it can be named
    and resolved by uuid even though nothing ever wrote a label into it.
    """
    out: list[Account] = []
    try:
        entries = sorted(p for p in ACCOUNTS_DIR.iterdir() if p.is_dir())
    except OSError:
        return out
    for directory in entries:
        account = _account_from_meta(directory)
        if account is None and directory.name != DEFAULT_KEY:
            account = Account(key=directory.name, uuid=directory.name, email=None, org_name=None, org_type=None)
        if account is not None:
            out.append(account)
    return out


def legacy_dirs_for(uuid: str) -> list[Path]:
    """Directories holding ``uuid``'s state under a pre-uuid key (``{org}-{email}-{uuid}``).

    Matched on the uuid suffix, which every legacy key ended with. Oldest first, so a merge
    replays them in the order they were written and the freshest state wins.
    """
    key = _compose_key(uuid)
    try:
        candidates = [p for p in ACCOUNTS_DIR.iterdir() if p.is_dir() and p.name != key and p.name.endswith(key)]
    except OSError:
        return []
    # `-` separated the head from the uuid: without it, `…-2<uuid>` would pass as a legacy key.
    legacy = [p for p in candidates if p.name.endswith(f"-{key}")]
    return sorted(legacy, key=_mtime)


def _mtime(path: Path) -> float:
    try:
        return path.stat().st_mtime
    except OSError:
        return 0.0


def resolve(ref: str | None) -> Account | None:
    """Resolve an account reference (key, uuid or email) to a known account, or None.

    Matches the active account and any account carrying a state directory. Case-insensitive
    on the email; the active account is considered even before its directory exists."""
    if not ref:
        return None
    needle = ref.strip().lower()
    candidates = list_accounts()
    active = current_account()
    if active is not None and all(active.key != c.key for c in candidates):
        candidates.append(active)
    for account in candidates:
        if needle in (account.key.lower(), (account.uuid or "").lower(), (account.email or "").lower()):
            return account
    return None
