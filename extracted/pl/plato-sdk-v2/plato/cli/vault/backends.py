"""The two places `plato vault` can reach the login vault, behind one interface.

* :class:`ChronosBackend` - the Chronos login vault (``/api/login-vault``), with
  the caller's Plato key (and, inside a run, its session id). The default.
* :class:`ConsoleBackend` - the login console (``/api/logins``), the path used
  before the vault moved into Chronos. Only on ``--via console``: a Chronos
  error (:class:`ChronosVaultMissing` included) is reported, never retried here.

Both return the same normalized, SECRET-FREE shapes (``row`` for ``list``,
``view`` for ``show``/``create``/``edit``): every value that can be a credential
is reduced to a presence boolean before it leaves this module.
"""

from __future__ import annotations

from collections.abc import Iterator
from contextlib import contextmanager
from typing import Any

import httpx

from plato.chronos.errors import APIError
from plato.chronos.login_vault import (
    InvalidVaultFields,
    LoginVault,
    VaultBadReply,
    VaultRouteMissing,
    normalize_key,
)
from plato.cli.vault.client import (
    BakeOutcomeUnknown,
    ConsoleUnreachable,
    CreateOutcomeUnknown,
    GateRefused,
    NotFound,
    PartialCreate,
    VaultConsoleClient,
    VaultConsoleError,
)


class ChronosVaultMissing(VaultConsoleError):
    """Chronos has no ``/api/login-vault`` route for the call (an older Chronos).
    Reported as an error: there is no fallback."""


# Credential presence, Chronos summary flag -> CLI key.
_CHRONOS_CREDS = {
    "password": "has_password",
    "totp": "has_totp",
    "phone": "has_phone",
    "security_qa": "has_security_qa",
}
# The archive (a dead account nothing may use until it is restored):
# ``archived_at`` is the flag, the other two say who and why.
ARCHIVE_FIELDS = ("archived_at", "archived_by", "archived_reason")
_CHRONOS_FIELDS = (
    "login_url",
    "browser_mode",
    "auto_refresh",
    "proxy_exit",
    "created_by",
    "updated_by",
    "last_bake_session_id",
    "last_bake_at",
    *ARCHIVE_FIELDS,
)
_CHRONOS_VIEW_FIELDS = (*_CHRONOS_FIELDS, "login_hint", "item_updated_at")


def _plain(value: Any) -> Any:
    """An enum / datetime from the SDK model as JSON-friendly text."""
    if value is None or isinstance(value, (bool, int, float, str)):
        return value
    enum_value = getattr(value, "value", None)
    if enum_value is not None:
        return enum_value
    iso = getattr(value, "isoformat", None)
    return iso() if callable(iso) else str(value)


def _add_default_for(out: dict, summary: Any) -> None:
    """Which clones this account is the default login for (Chronos's app
    defaults). Left out when the reply has no list, so :func:`default_for` reads
    "the source does not say"."""
    value = getattr(summary, "default_for", None)
    if isinstance(value, list):
        out["default_for"] = [str(v) for v in value]


def default_for(row: dict) -> list[str] | None:
    """The clone names a row's account is the default login for, or None when the
    source does not say. Chronos sends ``default_for`` on its list and read; the
    console sends it on ``show`` and ``is_default`` (default for its own login_key)
    on ``list``."""
    value = row.get("default_for")
    if isinstance(value, list):
        return [normalize_key(str(v)) for v in value if str(v).strip()]
    flag = row.get("is_default")
    if isinstance(flag, bool):
        return [normalize_key(str(row.get("login_key") or ""))] if flag else []
    return None


def is_archived(row: dict) -> bool:
    """Whether a list row or a ``show`` view is an archived account: Chronos
    sends ``archived_at``, the console ``archived``."""
    return bool(row.get("archived_at")) or row.get("archived") is True


def max_sessions(summary: Any) -> int:
    """How many live sessions may use the account at once. The vault's rule:
    an item without the field (or a reply without it) is 1."""
    value = getattr(summary, "max_sessions", None)
    return value if isinstance(value, int) and not isinstance(value, bool) and value >= 1 else 1


def chronos_row(summary: Any) -> dict:
    """A Chronos summary (or account) as a list row. No secret can be in it: the
    summary has none, and an account's secrets are never read here."""
    row = {
        "login_key": summary.login_key,
        "account": summary.account,
        "username": summary.username,
        "creds": {k: bool(getattr(summary, flag, False)) for k, flag in _CHRONOS_CREDS.items()},
    }
    row.update({k: _plain(getattr(summary, k, None)) for k in _CHRONOS_FIELDS})
    row["max_sessions"] = max_sessions(summary)
    _add_default_for(row, summary)
    return row


def chronos_view(account: Any) -> dict:
    """``show``'s projection of a Chronos account: non-secret fields plus presence."""
    view = {
        "login_key": account.login_key,
        "account": account.account,
        "username": account.username,
        "creds": {
            "username": bool(account.username),
            **{k: bool(getattr(account, flag, False)) for k, flag in _CHRONOS_CREDS.items()},
        },
    }
    view.update({k: _plain(getattr(account, k, None)) for k in _CHRONOS_VIEW_FIELDS})
    view["max_sessions"] = max_sessions(account)
    _add_default_for(view, account)
    # What makes an account bakeable through Chronos: a login URL on the item.
    view["bakeable"] = bool(account.login_url)
    return view


@contextmanager
def chronos_errors(base_url: str, *, unknown: type[ConsoleUnreachable] | None = None) -> Iterator[None]:
    """SDK errors -> the CLI's typed errors (and so its documented exit codes).
    None of these messages quotes a request or reply body: both can hold secrets."""
    try:
        yield
    except VaultRouteMissing as e:
        raise ChronosVaultMissing(str(e)) from e
    except InvalidVaultFields as e:
        # The request was refused before it was sent; the message names fields only.
        raise VaultConsoleError(str(e)) from None
    except VaultBadReply as e:
        # A 2xx that is not the route's JSON (a proxy or load balancer page): the
        # request was sent, so a create or bake MAY have landed.
        raise (unknown or ConsoleUnreachable)(f"{e} (at {base_url})") from None
    except APIError as e:
        detail = e.message
        if e.status_code == 401:
            raise VaultConsoleError(f"401 from Chronos: {detail} - check PLATO_API_KEY") from e
        if e.status_code == 403:
            raise GateRefused(
                f"403 refused by Chronos: {detail} (only keys of the vault org get in; an org-wide "
                "key cannot bake, and may edit only items a run or an org-wide key created; "
                "--via console uses the login console instead)"
            ) from e
        if e.status_code == 404:
            raise NotFound(detail) from e
        if e.status_code == 409:
            raise GateRefused(f"409 refused by Chronos: {detail}") from e
        if e.status_code >= 500:
            raise ConsoleUnreachable(f"{e.status_code} from Chronos: {detail}") from e
        raise VaultConsoleError(f"{e.status_code} from Chronos: {detail}") from e
    except httpx.HTTPError as e:
        sent = not isinstance(e, (httpx.ConnectError, httpx.ConnectTimeout))
        if unknown is not None and sent:
            raise unknown(f"no answer from Chronos at {base_url}: {e}") from e
        raise ConsoleUnreachable(f"cannot reach Chronos at {base_url}: {e}") from e


class ChronosBackend:
    """The Chronos login vault, with the caller's Plato key. ``session_id`` (a run's
    own Chronos session) is sent along, so a change made with an org-wide key is
    recorded as that run's (a personal key's change is always the person's)."""

    name = "chronos"

    def __init__(
        self, api_key: str, base_url: str, *, session_id: str | None = None, vault_factory: Any = LoginVault
    ) -> None:
        self.base_url = base_url.rstrip("/")
        self._vault = vault_factory(api_key=api_key, base_url=self.base_url, session_id=session_id)

    def close(self) -> None:
        close = getattr(self._vault, "close", None)
        if callable(close):
            close()

    def list_accounts(
        self, login_key: str | None = None, include_archived: bool = False
    ) -> tuple[list[dict], str | None]:
        """The rows, and ``vault_error`` when the list may be incomplete
        (Chronos could not list 1Password, so items made by hand there may be
        missing). Chronos leaves archived accounts out unless asked for them."""
        with chronos_errors(self.base_url):
            listing = self._vault.list_accounts(login_key, include_archived=include_archived)
        return [chronos_row(s) for s in listing.accounts], listing.vault_error

    def show(self, login_key: str, account: str) -> dict:
        with chronos_errors(self.base_url):
            found = self._vault.get_account(login_key, account)
        if found is None:
            raise NotFound(f"no vault item for {normalize_key(login_key)}/{normalize_key(account)}")
        return chronos_view(found)

    def create(self, login_key: str, account: str, fields: dict) -> dict:
        with chronos_errors(self.base_url, unknown=CreateOutcomeUnknown):
            created = self._vault.create_account(login_key, account, **fields)
        return {"view": chronos_view(created), "partial": False}

    def edit(self, login_key: str, account: str, fields: dict) -> dict:
        # One PATCH: every field lands or none does.
        with chronos_errors(self.base_url):
            saved = self._vault.update_account(login_key, account, **fields)
        return {"view": chronos_view(saved), "applied": sorted(fields)}

    def bake(self, login_key: str, account: str, browser_mode: str | None) -> dict:
        with chronos_errors(self.base_url, unknown=BakeOutcomeUnknown):
            launched = self._vault.bake(login_key, account, browser_mode=browser_mode)
        return {
            "session_id": launched.session_id,
            "browser_mode": _plain(launched.browser_mode),
            "world_package": launched.world_package,
        }

    def status(self, login_key: str, account: str) -> dict:
        view = self.show(login_key, account)
        return {"session_id": view.get("last_bake_session_id"), "last_bake_at": view.get("last_bake_at")}

    def archive(self, login_key: str, account: str, reason: str) -> dict:
        """Archive the account (any key of the vault org, for any account)."""
        with chronos_errors(self.base_url):
            summary = self._vault.archive(login_key, account, reason)
        return chronos_row(summary)

    def restore(self, login_key: str, account: str) -> dict:
        with chronos_errors(self.base_url):
            summary = self._vault.restore(login_key, account)
        return chronos_row(summary)


# --------------------------------------------------------------------------- #
# console (--via console)
# --------------------------------------------------------------------------- #

# Only these console fields are ever rendered. The console record also carries
# credential-shaped values (a reveal route feeds the same page), so an allowlist
# means no code path here can print one by accident. Presence flags only.
CONSOLE_DETAIL_FIELDS = (
    "login_key",
    "account",
    "email",
    "method",
    "method_kinds",
    "migrated",
    "archived",
    *ARCHIVE_FIELDS,
    "live",
    "bakeable",
    "browser_mode",
    "auto_refresh",
    "login_hint",
    "bake_session_id",
    "default_for",
    "login_url",
    "op_item_url",
)
SNAPSHOT_FIELDS = ("status", "age_days", "created_at", "ref", "kind", "mode", "proxy_exit", "context_id", "via_vm")
_PROXY_FIELDS = ("name", "note", "error", "label")
# The vault's own field names (op_client._FIELDS) - what `cred_presence` is keyed
# by. Always these four keys, so a driver can read `creds["password"]` whatever
# the console had in hand; the flat has_* flags are all it sends when 1Password
# is unconfigured or hiccups (build_detail emits `cred_presence` as `{}` there).
_CRED_FIELDS = ("username", "password", "totp", "phone")
_CRED_FLAT = {"username": "has_user", "password": "has_pass", "totp": "has_totp"}
# The list route's per-account fields: the vault-backed config and
# the BOUND exit (`proxy`). `bakeable` is computed by build_detail only, so it
# stays a `show` fact: reading it here rendered "no" for every account.
# `is_default`: the app defaults name this account for its own login_key.
_CONSOLE_ROW_FIELDS = (
    "account",
    "migrated",
    "archived",
    *ARCHIVE_FIELDS,
    "live",
    "browser_mode",
    "auto_refresh",
    "login_url",
    "is_default",
)


def pick(record: Any, fields: tuple[str, ...]) -> dict:
    """The allowlisted subset of a console record. A key the console did not send
    stays absent, never a null: a driver would read "no mode" or "not bakeable"
    from a value the console never stated."""
    if not isinstance(record, dict):
        return {}
    return {k: record[k] for k in fields if k in record}


def console_snapshot(record: Any) -> dict:
    """The console's snapshot projection. With no snapshot the console still fills
    `kind`, `mode` and `via_vm` with defaults ("vm", "chrome", False); those are not
    facts about anything, so they are dropped to None and `status` alone says "none".
    Only an explicit "none" does this: a record with no status keeps its fields."""
    view = pick(record, SNAPSHOT_FIELDS)
    if view.get("status") == "none":
        view = {k: None for k in SNAPSHOT_FIELDS} | {"status": "none"}
    return view


def _console_creds(detail: dict) -> dict[str, bool]:
    """Credential PRESENCE only, coerced to booleans so no value can leak."""
    presence = detail.get("cred_presence")
    if isinstance(presence, dict) and presence:
        return {k: bool(presence.get(k)) for k in _CRED_FIELDS}
    return {k: bool(detail.get(_CRED_FLAT[k])) if k in _CRED_FLAT else False for k in _CRED_FIELDS}


def console_view(detail: dict) -> dict:
    """The safe projection of the console's ``build_detail``."""
    view = pick(detail, CONSOLE_DETAIL_FIELDS)
    view["creds"] = _console_creds(detail)
    view["snapshot"] = console_snapshot(detail.get("snapshot"))
    proxy = pick(detail.get("proxy"), _PROXY_FIELDS)
    view["proxy"] = proxy
    if "name" in proxy:
        view["proxy_exit"] = proxy["name"]
    lineage = detail.get("lineage")
    view["lineage_count"] = len(lineage) if isinstance(lineage, list) else 0
    return view


def console_row(login_key: Any, account: dict) -> dict:
    row = {"login_key": login_key, **pick(account, _CONSOLE_ROW_FIELDS)}
    if "proxy" in account:
        # The BOUND exit, not `snapshot.proxy_exit` (the exit the last bake left from).
        row["proxy_exit"] = account.get("proxy")
    if "bake_session_id" in account:
        row["last_bake_session_id"] = account.get("bake_session_id")
    row["snapshot"] = console_snapshot(account.get("snapshot"))
    return row


def _same_key(group: Any, login_key: str) -> bool:
    """Match a group's login_key. The console lowercases keys, the operator may not."""
    return str((group or {}).get("login_key") or "").lower() == login_key.lower()


# Create/edit field -> the console's credentials-route name.
_CONSOLE_CRED_NAMES = {"username": "username", "password": "password", "totp_seed": "totp", "phone": "phone"}


class ConsoleBackend:
    """The login console (``/api/logins``): the path before the Chronos vault."""

    name = "console"

    def __init__(self, base_url: str, *, client_factory: Any = VaultConsoleClient) -> None:
        self.base_url = base_url.rstrip("/")
        self._client = client_factory(self.base_url)

    def close(self) -> None:
        close = getattr(self._client, "close", None)
        if callable(close):
            close()

    def list_accounts(
        self, login_key: str | None = None, include_archived: bool = False
    ) -> tuple[list[dict], str | None]:
        """The rows, and the console's ``vault_error`` (its last Chronos list
        may be incomplete)."""
        inventory = self._client.list_logins(include_archived=include_archived)
        groups = [g for g in inventory.get("groups", []) if not login_key or _same_key(g, login_key)]
        rows = [console_row(g.get("login_key"), a) for g in groups for a in g.get("accounts", [])]
        return rows, inventory.get("vault_error")

    def show(self, login_key: str, account: str) -> dict:
        return console_view(self._client.get_login_detail(login_key, account))

    def create(self, login_key: str, account: str, fields: dict) -> dict:
        if "max_sessions" in fields:
            raise VaultConsoleError("the login console cannot set max sessions; that needs the Chronos login vault")
        body: dict[str, Any] = {"login_key": login_key, "account": account}
        for key, name in _CONSOLE_CRED_NAMES.items():
            if fields.get(key):
                body[name] = fields[key]
        if fields.get("security_qa"):
            body["security_qa"] = fields["security_qa"]
        if fields.get("login_url"):
            body["target_url"] = fields["login_url"]
        result = self._client.create_login(body)
        created = result.get("created") if isinstance(result, dict) else None
        if not isinstance(created, dict):
            # Never quote the payload: an unexpected shape could echo anything.
            raise ConsoleUnreachable(
                f"{self.base_url}/api/logins answered without a create report; "
                f"run `plato vault show {login_key} --account {account}` to see what landed"
            )
        # The console commits its catalog row first and reports a failed vault
        # write as "error: <Type>" in that write's slot.
        failed = [k for k in ("op_item", "login_url") if isinstance(created.get(k), str)]
        # The fields the console create route has no slot for go through the edit routes.
        rest = {k: fields[k] for k in ("browser_mode", "login_hint", "proxy_exit", "auto_refresh") if k in fields}
        applied: list[str] = []
        if rest and not failed:
            applied = self._edit_routes(login_key, account, rest)
        return {
            "view": {
                "login_key": result.get("login_key", login_key),
                "account": result.get("account", account),
                "created": {k: created.get(k) for k in ("catalog", "op_item", "login_url")},
                "applied": applied,
            },
            "partial": bool(failed),
            "failed": failed,
        }

    def edit(self, login_key: str, account: str, fields: dict) -> dict:
        """Several console routes, so several writes: ``applied`` names each one
        AFTER it lands, and a failure part-way reports what is already in."""
        if fields.get("browser_mode") == "":
            raise VaultConsoleError("the login console cannot clear a browser mode; that needs the Chronos vault")
        if "max_sessions" in fields:
            # Checked before any write, so nothing else lands half-way.
            raise VaultConsoleError("the login console cannot set max sessions; that needs the Chronos login vault")
        applied = self._edit_routes(login_key, account, fields)
        return {"view": None, "applied": applied}

    def _edit_routes(self, login_key: str, account: str, fields: dict) -> list[str]:
        applied: list[str] = []
        try:
            creds = {name: fields[key] for key, name in _CONSOLE_CRED_NAMES.items() if key in fields}
            if "security_qa" in fields:
                creds["security_qa"] = fields["security_qa"]
            if "login_url" in fields:
                creds["login_url"] = fields["login_url"]
            if creds:
                self._client.update_credentials(login_key, account, creds)
                applied += sorted(k for k in fields if k in (*_CONSOLE_CRED_NAMES, "security_qa", "login_url"))
            if fields.get("browser_mode"):
                self._client.update_bake_config(login_key, account, browser_mode=fields["browser_mode"])
                applied.append("browser_mode")
            if "login_hint" in fields:
                self._client.set_login_hint(login_key, account, fields["login_hint"] or "")
                applied.append("login_hint")
            if "proxy_exit" in fields:
                self._client.bind_proxy(login_key, account, fields["proxy_exit"] or "")
                applied.append("proxy_exit")
            if fields.get("auto_refresh") is not None:
                self._client.set_auto_refresh(login_key, account, bool(fields["auto_refresh"]))
                applied.append("auto_refresh")
        except VaultConsoleError as e:
            e.applied = applied
            raise
        return applied

    def bake(self, login_key: str, account: str, browser_mode: str | None) -> dict:
        result = self._client.bake_login(login_key, account, browser_mode=browser_mode)
        return {"session_id": str(result.get("session_id") or "") or None, "browser_mode": browser_mode}

    def status(self, login_key: str, account: str) -> dict:
        return self._client.get_bake_live(login_key, account)

    def archive(self, login_key: str, account: str, reason: str) -> dict:
        """The console's Archive: through Chronos when it serves the vault, else
        the item's archive fields written with the console's own token."""
        return _console_archive_row(login_key, account, self._client.archive_login(login_key, account, reason))

    def restore(self, login_key: str, account: str) -> dict:
        return _console_archive_row(login_key, account, self._client.restore_login(login_key, account))


def _console_archive_row(login_key: str, account: str, result: Any) -> dict:
    """The console's archive/restore answer as a list row (allowlisted)."""
    row = {"login_key": login_key, "account": account}
    if isinstance(result, dict):
        row.update(pick(result, ("archived", *ARCHIVE_FIELDS)))
    return row


__all__ = [
    "ARCHIVE_FIELDS",
    "SNAPSHOT_FIELDS",
    "ChronosBackend",
    "ChronosVaultMissing",
    "ConsoleBackend",
    "PartialCreate",
    "chronos_errors",
    "chronos_row",
    "chronos_view",
    "console_row",
    "console_snapshot",
    "console_view",
    "default_for",
    "is_archived",
    "max_sessions",
    "pick",
]
