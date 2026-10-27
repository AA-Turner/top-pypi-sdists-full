"""Login vault client: Chronos ``/api/login-vault``. The accounts (list, read,
create, edit, bake, archive, restore), plus the settings a run reads beside its
account: an app's default account (by clone), an app's sign-in hint (by
``login_key``) and the proxy exits with their bans.

Chronos keeps every login SETTING in its own tables, and those are the truth;
1Password keeps the SECRETS (password, TOTP seed, security answers, and the
username and phone they go with), which an account read brings along (login
ADR 0005). Every caller sends the Plato key it already has in ``X-API-Key``;
only keys of the vault org get in. Chronos tells two kinds apart:

* **a personal key** (a person's own key): list, read, create, edit any item,
  bake, archive and restore. A change is recorded as ``user:<email>``.
* **an org-wide key** (the org's key, held by scripts, handlers and the runs
  they start): list, read, create, archive and restore any item, and edit only
  items a run or an org key made; no bake. A change is recorded as
  ``run:<session_id>`` when the call names its session in
  ``X-Chronos-Session-Id``, else ``org-key:<digest>``.

A run carries the key it was launched with. A run a person launched holds that
person's key, so its changes are recorded as ``user:<email>`` and its session id
is ignored. Only a run that holds an org-wide key (a handler or script launch)
is recorded as ``run:<session_id>``. Chronos checks only that the sent session
exists in the vault org, so ``run:<session_id>`` is the caller's claim, not proof.

:meth:`LoginVault.for_person` is a laptop or console client (``PLATO_API_KEY``).
:meth:`LoginVault.for_run` is a run's client: the run's Plato key plus its
session id (``SESSION_ID``, or the world's own id), sent on every call.

Chronos serves one 1Password vault, :data:`CHRONOS_VAULT_NAME` (``login``). A
caller configured for another vault cannot use the login vault at all
(:func:`serves_vault`); the worlds refuse such a config.

Errors never quote a secret: a body the vault would refuse raises
:class:`InvalidVaultFields` (field names only), a 2xx reply that is not the
route's JSON raises :class:`VaultBadReply`, and a ``422`` keeps only each
error's location and message (FastAPI echoes the offending ``input``).

There is no delete route for anyone. A dead account (say the vendor closed it)
is ARCHIVED instead (:meth:`LoginVault.archive`, any key of the vault org):
Chronos records when, by whom and why, the list hides it unless asked
(``include_archived``), a read still shows it, and Chronos refuses an open, a
bake, an edit or a create of its name with a 409 until it is restored.
A run must not use it either: :func:`credential_resolver` raises
:class:`AccountArchived` (``<key>/<acct> is archived: <reason>``) for an archived
read, and :func:`archived_error` gives that text for any read or summary.

No fallback: everything Chronos serves is read only through Chronos, and an
error answer raises. A Chronos without these routes answers ``404 Not Found``
(GET) or ``405`` (POST/PATCH, the frontend mount); both raise
:class:`VaultRouteMissing`, which is never read as "no such account". A ``404``
for a missing ACCOUNT is different: :meth:`get_account` returns ``None`` for
it, and the other calls raise :class:`NotFoundError`. A run still reads the
items Chronos does not serve (:func:`is_1password_item`) with its own 1Password
token, and nothing else: :func:`credential_resolver` keeps every other
reference away from 1Password.
"""

from __future__ import annotations

import os
import re
from collections.abc import Awaitable, Callable, Mapping
from enum import StrEnum
from types import ModuleType
from typing import Any, TypeVar

import httpx
from pydantic import BaseModel, SecretStr, ValidationError
from pydantic_core import to_jsonable_python

from plato.chronos.api.login_vault import (
    archive_login_vault_account,
    bake_login_vault_account,
    create_login_vault_account,
    get_login_vault_account,
    get_login_vault_app,
    get_login_vault_default,
    get_login_vault_grant,
    get_login_vault_grant_token,
    list_login_vault_accounts,
    list_login_vault_exits,
    restore_login_vault_account,
    update_login_vault_account,
)
from plato.chronos.errors import APIError, NotFoundError, raise_for_status
from plato.chronos.models import (
    LoginVaultAccount,
    LoginVaultAccountCreate,
    LoginVaultAccountList,
    LoginVaultAccountSummary,
    LoginVaultAccountUpdate,
    LoginVaultAppHint,
    LoginVaultArchiveRequest,
    LoginVaultBakeRequest,
    LoginVaultBakeResponse,
    LoginVaultDefault,
    LoginVaultExitList,
    LoginVaultGrant,
    LoginVaultGrantToken,
)

__all__ = [
    "ARCHIVE_REASON_MAX_LENGTH",
    "CHRONOS_VAULT_NAME",
    "SESSION_HEADER",
    "SESSION_ID_ENV_VAR",
    "VAULT_FIELDS",
    "AccountArchived",
    "AsyncLoginVault",
    "GrantKind",
    "InvalidVaultFields",
    "LoginVault",
    "VaultBadReply",
    "VaultRouteMissing",
    "archive_reason",
    "archived_error",
    "credential_resolver",
    "is_1password_item",
    "is_route_missing",
    "normalize_key",
    "serves_vault",
]

# A run names its Chronos session in this header, so a change made with an
# org-wide key is recorded as ``run:<session_id>`` (Chronos checks the session
# exists in the vault org). A personal key's changes are the person's anyway.
SESSION_HEADER = "X-Chronos-Session-Id"
# Where a run finds its own session id (the world runner sets it on boot).
SESSION_ID_ENV_VAR = "SESSION_ID"
# The 1Password vault the Chronos login vault serves (Chronos's
# ``login_vault_name``). A config on any other vault cannot use the login vault.
CHRONOS_VAULT_NAME = "login"

_DEFAULT_CHRONOS_URL = "https://chronos.plato.so"


# The writable fields of an account (create and edit take the same set).
VAULT_FIELDS = (
    "username",
    "password",
    "totp_seed",
    "phone",
    "security_qa",
    "login_url",
    "browser_mode",
    "login_hint",
    # Picks the mail-code inbox (plato.vault.mail_route). Unset, Chronos answers
    # the username when that is an address.
    "login_email",
    "proxy_exit",
    "auto_refresh",
    # How many live sessions (opens, bakes, runs) may use the account at once:
    # 1..50; 1 is the default.
    "max_sessions",
)

_NON_SLUG = re.compile(r"[^a-z0-9]+")

# The reason an archive records: one line (runs of whitespace become one space)
# of 1..this many characters, Chronos's rule.
ARCHIVE_REASON_MAX_LENGTH = 200


def serves_vault(vault: str | None) -> bool:
    """True when ``vault`` (a config's ``op_vault``; empty = the default) is the
    1Password vault Chronos serves. A config on another vault (``login-test``)
    must never get the prod ``login`` account that happens to share its name."""
    return ((vault or CHRONOS_VAULT_NAME).strip().lower()) == CHRONOS_VAULT_NAME


def normalize_key(value: str | None) -> str:
    """``login_key``/``account`` the way Chronos, the console and the worlds store
    them: lower case, every run outside ``[a-z0-9]`` becomes ``_``, no leading or
    trailing ``_`` (``X-Ads`` -> ``x_ads``). Also makes the value path-safe."""
    return _NON_SLUG.sub("_", (value or "").strip().lower()).strip("_")


class VaultRouteMissing(APIError):
    """This Chronos has no login vault (the routes are not deployed there): an
    error like any other, never read as "no such account"."""

    def __init__(self, status_code: int, message: str | None = None, body: dict[str, Any] | None = None):
        super().__init__(
            status_code,
            message or f"this Chronos has no /api/login-vault routes ({status_code})",
            body,
        )


class VaultBadReply(APIError):
    """Chronos answered 2xx with a body that is not the route's JSON (not JSON at
    all, e.g. a proxy's HTML page, or another shape). The body is never quoted: a
    read's body holds secrets. A write that got this answer may have landed."""


class AccountArchived(ValueError):
    """The account is archived (dead: say the vendor closed it), so nothing may
    use it until it is restored. The message is :func:`archived_error`'s
    ``<login_key>/<account> is archived: <reason>``; never a secret."""


def _text(value: Any) -> str | None:
    value = getattr(value, "value", value)  # an enum -> its string
    text = str(value).strip() if value is not None else ""
    return text or None


def archived_error(account: Any) -> str | None:
    """``<login_key>/<account> is archived: <reason>`` when ``account`` (a read,
    a list summary, or anything with those attributes) is archived; None when it
    is not. ``archived_at`` is the flag. An SDK model without the field still
    carries it from the reply (the models allow extra fields)."""
    if _text(getattr(account, "archived_at", None)) is None:
        return None
    reason = _text(getattr(account, "archived_reason", None)) or "no reason given"
    return f"{getattr(account, 'login_key', '')}/{getattr(account, 'account', '')} is archived: {reason}"


def archive_reason(reason: str | None) -> str:
    """The reason as Chronos stores it: one line (runs of whitespace, newlines
    included, become one space), 1..:data:`ARCHIVE_REASON_MAX_LENGTH` characters.
    ``ValueError`` for an empty or too long one, checked before any request."""
    text = " ".join((reason or "").split())
    if not text:
        raise ValueError("an archive needs a reason")
    if len(text) > ARCHIVE_REASON_MAX_LENGTH:
        raise ValueError(f"the archive reason is {len(text)} characters; at most {ARCHIVE_REASON_MAX_LENGTH}")
    return text


class InvalidVaultFields(ValueError):
    """A create/edit body the vault would refuse (too long, wrong type). Names the
    fields only: pydantic's own message quotes the value, and these are secrets."""


def _error_paths(error: ValidationError) -> str:
    """The failing field paths of a validation error, never its input. An
    unexpected key is caller text (it could be a pasted secret), so its path
    stops at the parent."""
    paths = set()
    for err in error.errors():
        loc = [str(p) for p in err.get("loc", ())]
        if err.get("type") == "extra_forbidden":
            loc = [*loc[:-1], "<unexpected key>"]
        paths.add(".".join(loc) or "<body>")
    return ", ".join(sorted(paths))


_M = TypeVar("_M", bound=BaseModel)


def _validated(model: type[_M], data: Mapping[str, Any]) -> _M:
    """``model.model_validate(data)`` for a request body, raising
    :class:`InvalidVaultFields` (names only) instead of pydantic's message."""
    try:
        return model.model_validate(data)
    except ValidationError as e:
        raise InvalidVaultFields(f"invalid login vault field(s): {_error_paths(e)}") from None


def _parse(model: type[_M], response: httpx.Response) -> _M:
    """A 2xx reply as ``model``; :class:`VaultBadReply` when it is not."""
    status = response.status_code
    try:
        data = response.json()
    except ValueError:
        kind = response.headers.get("content-type", "").split(";")[0].strip() or "no content type"
        raise VaultBadReply(status, f"Chronos answered {status} with a body that is not JSON ({kind})") from None
    try:
        return model.model_validate(data)
    except ValidationError as e:
        raise VaultBadReply(
            status, f"Chronos answered {status} with a body that is not a {model.__name__} ({_error_paths(e)})"
        ) from None


def _safe_detail(detail: Any) -> Any:
    """A FastAPI ``422`` detail without the offending ``input`` (or ``ctx``): each
    error keeps its location and message. Any other detail is returned as is."""
    if not isinstance(detail, list):
        return detail
    safe = []
    for err in detail:
        if isinstance(err, dict):
            safe.append({k: err[k] for k in ("type", "loc", "msg") if k in err})
    return safe


def _detail_text(detail: list[dict[str, Any]]) -> str:
    parts = []
    for err in detail:
        loc = ".".join(str(p) for p in err.get("loc") or () if p != "body")
        msg = str(err.get("msg") or err.get("type") or "invalid")
        parts.append(f"{loc}: {msg}" if loc else msg)
    return "; ".join(parts) or "invalid request"


def is_route_missing(error: BaseException) -> bool:
    """True when ``error`` says the vault ROUTE is missing, not an account.

    FastAPI answers an unknown GET path with ``404 {"detail": "Not Found"}``; the
    vault's own 404 names the item. An unknown POST/PATCH under ``/api/`` hits the
    frontend's static mount, which answers ``405``. The vault itself never sends a
    405 for a route this client calls (only for DELETE, which it never sends)."""
    if isinstance(error, VaultRouteMissing):
        return True
    if not isinstance(error, APIError):
        return False
    if error.status_code == 405:
        return True
    return error.status_code == 404 and (error.message or "").strip() == "Not Found"


def _raise(response: httpx.Response) -> None:
    """``raise_for_status`` with the route-missing case typed, and a ``422``'s
    echoed input dropped from the error's message and body."""
    try:
        raise_for_status(response)
    except APIError as e:
        if is_route_missing(e):
            raise VaultRouteMissing(e.status_code, body=e.body) from e
        detail = e.body.get("detail") if isinstance(e.body, dict) else None
        if isinstance(detail, list):
            safe = _safe_detail(detail)
            e.body = {**e.body, "detail": safe}
            e.message = _detail_text(safe)
            e.args = (e.message,)
        raise


def _send(client: httpx.Client, request_args: dict[str, Any]) -> httpx.Response:
    response = client.request(**request_args)
    _raise(response)
    return response


async def _asend(client: httpx.AsyncClient, request_args: dict[str, Any]) -> httpx.Response:
    response = await client.request(**request_args)
    _raise(response)
    return response


def _fields(fields: Mapping[str, Any]) -> dict[str, Any]:
    """Only the vault's writable fields; an unknown name is a caller bug, refused
    here rather than by a 422 after a network round trip."""
    unknown = sorted(set(fields) - set(VAULT_FIELDS))
    if unknown:
        raise ValueError(f"unknown login vault field(s): {', '.join(unknown)}")
    return {k: v for k, v in fields.items() if v is not None}


def _clear(value: Any) -> Any:
    if isinstance(value, SecretStr):
        return value.get_secret_value()
    if isinstance(value, dict):
        return {k: _clear(v) for k, v in value.items()}
    if isinstance(value, list):
        return [_clear(v) for v in value]
    return value


def _with_body(args: dict[str, Any], body: BaseModel) -> dict[str, Any]:
    """The generated request args with ``body`` sent as is. The generated builders
    dump with ``mode="json"``, which writes a ``SecretStr`` (the password, TOTP seed,
    phone and security answers are ``format: password`` in the spec) as
    ``**********``: the vault would store the mask."""
    args["json"] = to_jsonable_python(_clear(body.model_dump(exclude_none=True)))
    return args


def _create_body(login_key: str, account: str, fields: Mapping[str, Any]) -> LoginVaultAccountCreate:
    return _validated(
        LoginVaultAccountCreate,
        {"login_key": normalize_key(login_key), "account": normalize_key(account), **_fields(fields)},
    )


def _update_body(fields: Mapping[str, Any]) -> LoginVaultAccountUpdate:
    return _validated(LoginVaultAccountUpdate, _fields(fields))


def _keys(login_key: str, account: str) -> tuple[str, str]:
    lk, ac = normalize_key(login_key), normalize_key(account)
    if not lk or not ac:
        raise ValueError("login_key and account must not be empty")
    return lk, ac


def _list_args(login_key: str | None, include_archived: bool, api_key: str) -> dict[str, Any]:
    # ``include_archived`` only when asked: a Chronos from before the archive
    # answers the same list either way.
    return list_login_vault_accounts._build_request_args(
        login_key=normalize_key(login_key) or None,
        include_archived=True if include_archived else None,
        x_api_key=api_key,
    )


def _archive_args(login_key: str, account: str, reason: str, api_key: str) -> dict[str, Any]:
    lk, ac = _keys(login_key, account)
    body = _validated(LoginVaultArchiveRequest, {"reason": archive_reason(reason)})
    return archive_login_vault_account._build_request_args(login_key=lk, account=ac, body=body, x_api_key=api_key)


def _slug(value: str | None, what: str) -> str:
    slug = normalize_key(value)
    if not slug:
        raise ValueError(f"{what} must not be empty")
    return slug


def _default_args(clone: str, api_key: str) -> dict[str, Any]:
    return get_login_vault_default._build_request_args(clone=_slug(clone, "clone"), x_api_key=api_key)


def _app_args(login_key: str, api_key: str) -> dict[str, Any]:
    return get_login_vault_app._build_request_args(login_key=_slug(login_key, "login_key"), x_api_key=api_key)


class GrantKind(StrEnum):
    """Which app grant of an account: ``api`` (the vendor's REST API) or ``hosted_mcp`` (its hosted MCP server)."""

    api = "api"
    hosted_mcp = "hosted_mcp"


def _grant_args(route: ModuleType, login_key: str, account: str, kind: GrantKind, api_key: str) -> dict[str, Any]:
    lk, ac = _keys(login_key, account)
    return route._build_request_args(login_key=lk, account=ac, kind=GrantKind(kind).value, x_api_key=api_key)


def _base_url(base_url: str | None) -> str:
    return (base_url or os.environ.get("CHRONOS_URL") or _DEFAULT_CHRONOS_URL).rstrip("/")


# The account item's credential fields: 1Password field label -> the attribute
# the Chronos read returns it in (see :func:`credential_resolver`). ``login-email``
# is a Chronos setting, not an item field: a ref to it reads the account's login email.
_OP_CREDENTIAL_FIELDS = {
    "username": "username",
    "password": "password",
    "totp-seed": "totp_seed",
    "phone": "phone",
    "login-email": "login_email",
}

# The 1Password items Chronos does not serve, which a run still reads with its
# own token: the ``mail-<account>`` inboxes, the ``sms-<x>`` phone numbers,
# ``textverified``, the ``proxy-<provider>`` items and ``browserbase``.
_1PASSWORD_ITEMS = frozenset({"textverified", "browserbase"})
_1PASSWORD_PREFIXES = ("mail-", "sms-", "proxy-")
# Settings items Chronos owns now; their 1Password copies are frozen and stale.
_SETTINGS_ITEMS = frozenset({"login-defaults", "login-hints", "proxy-bans", "proxy-ban-notes"})


def is_1password_item(title: str | None) -> bool:
    """Whether a run reads the 1Password item ``title`` with its own token: an
    item Chronos does not serve (a mail inbox, an SMS number, TextVerified, a
    proxy provider, Browserbase). An account item (``<login_key>-<account>``) and
    the settings items (``login-defaults``, ``login-hints``, ``proxy-bans``,
    ``proxy-ban-notes``) are False: they are read only through Chronos."""
    name = (title or "").strip().lower()
    if name in _SETTINGS_ITEMS:
        return False
    return name in _1PASSWORD_ITEMS or name.startswith(_1PASSWORD_PREFIXES)


OpResolver = Callable[[str], Awaitable[str | None]]


def credential_resolver(
    account: LoginVaultAccount | Any | None,
    *,
    fallback: OpResolver | None = None,
) -> OpResolver:
    """An ``op://`` resolver (``async (ref) -> str | None``) for worlds that read
    credentials by 1Password reference:

    * the account item's own credentials
      (``op://login/<login_key>-<account>/{username,password,totp-seed,phone}``,
      and ``login-email``)
      come from ``account``, the Chronos read of that item, and from nowhere
      else: a field the read has empty is empty;
    * a reference to an item that stays in 1Password (:func:`is_1password_item`:
      ``mail-*``, ``sms-*``, ``textverified``, ``proxy-*``, ``browserbase``) goes
      to ``fallback``, the run's own 1Password resolver;
    * every other reference answers None: Chronos serves it (another account's
      item, the per-app defaults and hints, the exit bans), so a run never reads
      it from 1Password.

    ``account`` None (Chronos has no such account) answers only the 1Password
    items. Raises :class:`AccountArchived` when ``account`` is archived: a run
    must not sign in as a dead account (``<login_key>/<account> is archived:
    <reason>``)."""
    item = f"{account.login_key}-{account.account}".lower() if account is not None else None
    refusal = archived_error(account) if account is not None else None
    if refusal is not None:
        raise AccountArchived(refusal)

    async def resolve(ref: str) -> str | None:
        parts = ref[len("op://") :].split("/") if ref.startswith("op://") else []
        if len(parts) < 3:
            return None
        title = parts[1]
        if (
            item is not None
            and len(parts) == 3
            and parts[0].lower() == CHRONOS_VAULT_NAME
            and title.lower() == item
            and parts[2] in _OP_CREDENTIAL_FIELDS
        ):
            value = getattr(account, _OP_CREDENTIAL_FIELDS[parts[2]], None)
            return value if isinstance(value, str) and value else None
        if fallback is not None and is_1password_item(title):
            return await fallback(ref)
        return None

    return resolve


class _VaultBase:
    def __init__(
        self,
        *,
        api_key: str,
        base_url: str | None = None,
        timeout: float = 30.0,
        session_id: str | None = None,
    ) -> None:
        if not api_key:
            raise ValueError("a login vault client needs a Plato key")
        self._api_key = api_key
        self._base_url = _base_url(base_url)
        self._timeout = timeout
        self._session_id = (session_id or "").strip() or None

    @property
    def base_url(self) -> str:
        return self._base_url

    @property
    def session_id(self) -> str | None:
        """The Chronos session this client speaks for (sent as ``X-Chronos-Session-Id``)."""
        return self._session_id

    def _with_session(self, args: dict[str, Any]) -> dict[str, Any]:
        """The generated request args plus the run's session header, when it has one."""
        if self._session_id:
            args["headers"] = {**args.get("headers", {}), SESSION_HEADER: self._session_id}
        return args

    @staticmethod
    def _run_identity(
        api_key: str | None, session_id: str | None, environ: Mapping[str, str] | None
    ) -> tuple[str, str | None]:
        env = os.environ if environ is None else environ
        key = (api_key or env.get("PLATO_API_KEY", "")).strip()
        sid = (session_id or env.get(SESSION_ID_ENV_VAR, "")).strip() or None
        return key, sid


class LoginVault(_VaultBase):
    """Synchronous client (the CLI)."""

    def __init__(
        self,
        *,
        api_key: str,
        base_url: str | None = None,
        timeout: float = 30.0,
        transport: httpx.BaseTransport | None = None,
        session_id: str | None = None,
    ) -> None:
        super().__init__(api_key=api_key, base_url=base_url, timeout=timeout, session_id=session_id)
        self._client = httpx.Client(base_url=self._base_url, timeout=timeout, transport=transport)

    @classmethod
    def for_person(cls, api_key: str | None = None, base_url: str | None = None, timeout: float = 30.0) -> LoginVault:
        """A person's client: ``api_key`` or ``PLATO_API_KEY``."""
        return cls(api_key=api_key or os.environ.get("PLATO_API_KEY", ""), base_url=base_url, timeout=timeout)

    @classmethod
    def for_run(
        cls,
        base_url: str | None = None,
        *,
        api_key: str | None = None,
        session_id: str | None = None,
        environ: Mapping[str, str] | None = None,
        timeout: float = 30.0,
    ) -> LoginVault | None:
        """A run's client: the Plato key the run has (``api_key``, else
        ``PLATO_API_KEY``) and its session id (``session_id``, else ``SESSION_ID``).
        None when the run has no Plato key."""
        key, sid = cls._run_identity(api_key, session_id, environ)
        return cls(api_key=key, base_url=base_url, timeout=timeout, session_id=sid) if key else None

    def close(self) -> None:
        self._client.close()

    def _call(self, args: dict[str, Any]) -> httpx.Response:
        return _send(self._client, self._with_session(args))

    def __enter__(self) -> LoginVault:
        return self

    def __exit__(self, *exc: object) -> None:
        self.close()

    def list_accounts(self, login_key: str | None = None, include_archived: bool = False) -> LoginVaultAccountList:
        """Every account (non-secret summaries). Archived accounts are left out
        unless ``include_archived``."""
        args = _list_args(login_key, include_archived, self._api_key)
        return _parse(LoginVaultAccountList, self._call(args))

    def get_account(self, login_key: str, account: str) -> LoginVaultAccount | None:
        """One account WITH its secrets (Chronos reads them from 1Password); None
        when there is no such account."""
        lk, ac = _keys(login_key, account)
        args = get_login_vault_account._build_request_args(login_key=lk, account=ac, x_api_key=self._api_key)
        try:
            return _parse(LoginVaultAccount, self._call(args))
        except NotFoundError:
            return None

    def create_account(self, login_key: str, account: str, **fields: Any) -> LoginVaultAccount:
        """A new item (409 when the title exists). ``fields``: see :data:`VAULT_FIELDS`."""
        body = _create_body(login_key, account, fields)
        args = _with_body(create_login_vault_account._build_request_args(body=body, x_api_key=self._api_key), body)
        return _parse(LoginVaultAccount, self._call(args))

    def update_account(self, login_key: str, account: str, **fields: Any) -> LoginVaultAccount:
        """Change some fields: omitted/None = leave, ``""`` = clear, a value = set;
        ``security_qa=[]`` clears all questions."""
        lk, ac = _keys(login_key, account)
        body = _update_body(fields)
        args = _with_body(
            update_login_vault_account._build_request_args(
                login_key=lk, account=ac, body=body, x_api_key=self._api_key
            ),
            body,
        )
        return _parse(LoginVaultAccount, self._call(args))

    def bake(self, login_key: str, account: str, browser_mode: str | None = None) -> LoginVaultBakeResponse:
        """Launch a login-world bake (a REAL, paid session). ``browser_mode``
        overrides the item's mode for this one bake."""
        lk, ac = _keys(login_key, account)
        args = bake_login_vault_account._build_request_args(
            login_key=lk,
            account=ac,
            body=_validated(LoginVaultBakeRequest, {"browser_mode": browser_mode}),
            x_api_key=self._api_key,
        )
        return _parse(LoginVaultBakeResponse, self._call(args))

    def archive(self, login_key: str, account: str, reason: str) -> LoginVaultAccountSummary:
        """Archive a dead account (any key of the vault org): the list hides it and
        nothing may use it until :meth:`restore`. Archiving an archived account
        changes nothing (the first reason stands). Answers the account without
        its secrets."""
        args = _archive_args(login_key, account, reason, self._api_key)
        return _parse(LoginVaultAccountSummary, self._call(args))

    def restore(self, login_key: str, account: str) -> LoginVaultAccountSummary:
        """Clear the archive (any key of the vault org). A no-op for an account
        that is not archived. Answers the account without its secrets."""
        lk, ac = _keys(login_key, account)
        args = restore_login_vault_account._build_request_args(login_key=lk, account=ac, x_api_key=self._api_key)
        return _parse(LoginVaultAccountSummary, self._call(args))

    def get_default(self, clone: str) -> LoginVaultDefault:
        """The account ``clone`` signs in as by default (``auto_login``):
        ``login_key`` and ``account`` are None when the clone has no default."""
        return _parse(LoginVaultDefault, self._call(_default_args(clone, self._api_key)))

    def get_app_hint(self, login_key: str) -> LoginVaultAppHint:
        """The sign-in flow every account of the app shares; ``login_hint`` is
        None when none is recorded. A bake joins it with the account's own."""
        return _parse(LoginVaultAppHint, self._call(_app_args(login_key, self._api_key)))

    def list_exits(self) -> LoginVaultExitList:
        """Every proxy exit with its bans (read fresh; ``login_key`` ``*`` = every
        app) and the accounts bound to it. No provider credentials."""
        args = list_login_vault_exits._build_request_args(x_api_key=self._api_key)
        return _parse(LoginVaultExitList, self._call(args))

    def get_grant(self, login_key: str, account: str, kind: GrantKind) -> LoginVaultGrant | None:
        """The account's ``kind`` app grant without secrets:
        its state, generation and expiry. None when there is no such grant."""
        args = _grant_args(get_login_vault_grant, login_key, account, kind, self._api_key)
        try:
            return _parse(LoginVaultGrant, self._call(args))
        except NotFoundError:
            return None

    def get_grant_token(self, login_key: str, account: str, kind: GrantKind) -> LoginVaultGrantToken:
        """The grant's access token (never the refresh token). Chronos refreshes an
        active grant first when it has little time left. Raises ``APIError``: 404 no
        grant or token, 409 not active and expired, 502 the vendor refused the refresh."""
        args = _grant_args(get_login_vault_grant_token, login_key, account, kind, self._api_key)
        return _parse(LoginVaultGrantToken, self._call(args))


class AsyncLoginVault(_VaultBase):
    """Async client (worlds, the console backend)."""

    def __init__(
        self,
        *,
        api_key: str,
        base_url: str | None = None,
        timeout: float = 30.0,
        transport: httpx.AsyncBaseTransport | None = None,
        session_id: str | None = None,
    ) -> None:
        super().__init__(api_key=api_key, base_url=base_url, timeout=timeout, session_id=session_id)
        self._client = httpx.AsyncClient(base_url=self._base_url, timeout=timeout, transport=transport)

    @classmethod
    def for_person(
        cls, api_key: str | None = None, base_url: str | None = None, timeout: float = 30.0
    ) -> AsyncLoginVault:
        """A person's client: ``api_key`` or ``PLATO_API_KEY``."""
        return cls(api_key=api_key or os.environ.get("PLATO_API_KEY", ""), base_url=base_url, timeout=timeout)

    @classmethod
    def for_run(
        cls,
        base_url: str | None = None,
        *,
        api_key: str | None = None,
        session_id: str | None = None,
        environ: Mapping[str, str] | None = None,
        timeout: float = 30.0,
    ) -> AsyncLoginVault | None:
        """A run's client: the run's Plato key and session id (see :meth:`LoginVault.for_run`).
        None when the run has no Plato key."""
        key, sid = cls._run_identity(api_key, session_id, environ)
        return cls(api_key=key, base_url=base_url, timeout=timeout, session_id=sid) if key else None

    async def aclose(self) -> None:
        await self._client.aclose()

    async def _call(self, args: dict[str, Any]) -> httpx.Response:
        return await _asend(self._client, self._with_session(args))

    async def __aenter__(self) -> AsyncLoginVault:
        return self

    async def __aexit__(self, *exc: object) -> None:
        await self.aclose()

    async def list_accounts(
        self, login_key: str | None = None, include_archived: bool = False
    ) -> LoginVaultAccountList:
        args = _list_args(login_key, include_archived, self._api_key)
        return _parse(LoginVaultAccountList, await self._call(args))

    async def get_account(self, login_key: str, account: str) -> LoginVaultAccount | None:
        lk, ac = _keys(login_key, account)
        args = get_login_vault_account._build_request_args(login_key=lk, account=ac, x_api_key=self._api_key)
        try:
            return _parse(LoginVaultAccount, await self._call(args))
        except NotFoundError:
            return None

    async def create_account(self, login_key: str, account: str, **fields: Any) -> LoginVaultAccount:
        body = _create_body(login_key, account, fields)
        args = _with_body(create_login_vault_account._build_request_args(body=body, x_api_key=self._api_key), body)
        return _parse(LoginVaultAccount, await self._call(args))

    async def update_account(self, login_key: str, account: str, **fields: Any) -> LoginVaultAccount:
        lk, ac = _keys(login_key, account)
        body = _update_body(fields)
        args = _with_body(
            update_login_vault_account._build_request_args(
                login_key=lk, account=ac, body=body, x_api_key=self._api_key
            ),
            body,
        )
        return _parse(LoginVaultAccount, await self._call(args))

    async def bake(self, login_key: str, account: str, browser_mode: str | None = None) -> LoginVaultBakeResponse:
        lk, ac = _keys(login_key, account)
        args = bake_login_vault_account._build_request_args(
            login_key=lk,
            account=ac,
            body=_validated(LoginVaultBakeRequest, {"browser_mode": browser_mode}),
            x_api_key=self._api_key,
        )
        return _parse(LoginVaultBakeResponse, await self._call(args))

    async def archive(self, login_key: str, account: str, reason: str) -> LoginVaultAccountSummary:
        args = _archive_args(login_key, account, reason, self._api_key)
        return _parse(LoginVaultAccountSummary, await self._call(args))

    async def restore(self, login_key: str, account: str) -> LoginVaultAccountSummary:
        lk, ac = _keys(login_key, account)
        args = restore_login_vault_account._build_request_args(login_key=lk, account=ac, x_api_key=self._api_key)
        return _parse(LoginVaultAccountSummary, await self._call(args))

    async def get_default(self, clone: str) -> LoginVaultDefault:
        return _parse(LoginVaultDefault, await self._call(_default_args(clone, self._api_key)))

    async def get_app_hint(self, login_key: str) -> LoginVaultAppHint:
        return _parse(LoginVaultAppHint, await self._call(_app_args(login_key, self._api_key)))

    async def list_exits(self) -> LoginVaultExitList:
        args = list_login_vault_exits._build_request_args(x_api_key=self._api_key)
        return _parse(LoginVaultExitList, await self._call(args))

    async def get_grant(self, login_key: str, account: str, kind: GrantKind) -> LoginVaultGrant | None:
        args = _grant_args(get_login_vault_grant, login_key, account, kind, self._api_key)
        try:
            return _parse(LoginVaultGrant, await self._call(args))
        except NotFoundError:
            return None

    async def get_grant_token(self, login_key: str, account: str, kind: GrantKind) -> LoginVaultGrantToken:
        args = _grant_args(get_login_vault_grant_token, login_key, account, kind, self._api_key)
        return _parse(LoginVaultGrantToken, await self._call(args))
