"""`plato vault open`: a real signed-in browser on one of our app accounts.

The command launches the login world in open mode (``hold_minutes``) through
Chronos with the caller's OWN Plato key, so it needs no password or proxy
tool. The world loads the account's latest saved login, signs in for real
only when the agent finds it signed out, posts the browser link (noVNC, or the
Browserbase Live View) to the session page, and holds the browser open.

This module holds the parts with rules in them, each testable on its own:

* :func:`pick_account` - ``-a``, else the app's DEFAULT account; never an
  archived one (:func:`archived_refusal`);
* :func:`find_live_sessions` / :func:`refuse_if_busy` - at most the account's
  ``max_sessions`` live opens, bakes and runs at a time, and for ``--save`` no
  live bake or other saving open (the Chronos open route's rules);
* :func:`seed_modes` / :func:`resolve_seed` - which saved login to load first;
* :func:`login_settings` - what the open launches: the vault org's
  ``login-agent`` experiment in Chronos, a launch template (no coded copy);
* :func:`build_open_launch` - the launch payload: the template filled
  (:func:`fill_template`), this open's keys on top (secret-free: ``${...}`` only);
* :func:`close_tags` / :func:`wait_for_end` - ``plato vault close``;
* :class:`OpenClient` - the few raw Chronos calls (read as plain JSON, so a new
  status value on the server cannot break a status read).
"""

from __future__ import annotations

import asyncio
import json
import re
import time
from collections.abc import AsyncIterator, Callable, Iterable, Mapping, Sequence
from dataclasses import dataclass
from datetime import UTC, datetime
from typing import Any

import httpx
from pydantic import BaseModel, ConfigDict, PositiveInt, TypeAdapter, ValidationError

from plato.chronos import login_snapshot
from plato.chronos.api.workspace_repos import list_workspace_branches, list_workspace_files
from plato.chronos.errors import APIError, NotFoundError, raise_for_status
from plato.chronos.login_vault import normalize_key
from plato.cli.vault.backends import default_for, is_archived
from plato.cli.vault.client import GateRefused, NotFound, VaultConsoleError

# The same ceiling the login world validates (hold.MAX_HOLD_MINUTES).
MAX_MINUTES = 240
DEFAULT_MINUTES = 60

# A sign-in with an emailed code can take ~10 minutes on top of VM boot.
LINK_WAIT_SECONDS = 25 * 60
LINK_POLL_SECONDS = 10.0

# The config field only an open-mode login world has (an older world ignores an
# unknown field and would run a real bake instead).
OPEN_MODE_FIELD = "hold_minutes"
# What a sign-in launches: the vault org's Chronos experiment of this name, read
# by id. Its latest version is a whole launch (world, VM, agent, Browserbase keys)
# with ${LOGIN_*} placeholders, plus the sign-in budget. No coded copy.
LOGIN_EXPERIMENT = "login-agent"
LOGIN_EXPERIMENT_ID = "f8e7985b-61b2-4b51-b96d-3f9d81ec00fa"
# Chronos's get_experiment_file (not in the generated SDK).
LOGIN_EXPERIMENT_PATH = f"/api/experiments/files/{LOGIN_EXPERIMENT_ID}"
# The template's own placeholders, filled per launch. Every other ${...} is a
# secret that Chronos fills at launch.
_TEMPLATE_PARAM = re.compile(r"\$\{(LOGIN_KEY|LOGIN_ACCOUNT|LOGIN_URL|LOGIN_VAULT)\}")
# Keys a launch sets only in some cases: an experiment holding one is refused. The
# facts and 1Password fields may be in it: every launch overwrites them.
LAUNCH_OWNED_KEYS = frozenset(
    "proxy_exit state cdp_browser copy_session_to_cdp_browser copy_verify_url cdp_browser_context_id"
    " hold_minutes hold_save opened_by agent_types_password min_warmpool_timeout login_hint second_factor"
    " seed_snapshot_url".split()
)
# The template's Browserbase keys, kept only for a Browserbase browser.
BROWSERBASE_KEYS = frozenset(
    {"cdp_browser_api_base", "cdp_browser_api_key", "cdp_browser_project_id", "cdp_browser_session_timeout"}
)
# The vault an open reads, and the token placeholder Chronos vouches for.
OP_VAULT = "login"
OP_TOKEN = "${OP_SERVICE_ACCOUNT_TOKEN}"

# The label the world gives the link on the session page (hold.py / world.py).
LINK_LABEL_PREFIX = "Signed-in browser"
OPEN_TAG = "vault_open"
# `plato vault close` puts this tag on an open session; the world's hold checks
# for it (login_world.hold.CLOSE_TAG) and ends the session cleanly. A cancel
# (`plato chronos stop`) destroys the world VM at once instead: nothing in the
# world runs, so a Browserbase browser stays up, signed in, to its own timeout.
CLOSE_TAG = "vault_close"
# The hold checks every 30 s; then the world releases, tags and completes.
CLOSE_WAIT_SECONDS = 150.0
CLOSE_POLL_SECONDS = 5.0

# In lifecycle order: the list is read one status at a time, and a session
# that moves on meanwhile (pending -> queued -> starting -> running) is then
# met again in a later request, never skipped.
LIVE_STATUSES = ("pending", "queued", "starting", "running")
# Chronos's largest /api/sessions page, and how many pages of one status the
# busy check reads before it gives up (loudly, never with a partial list).
SESSION_PAGE = 200
MAX_SESSION_PAGES = 50
# Rows each page re-reads from the one before (see OpenClient._all_pages).
PAGE_OVERLAP = 50
# How many bakes of one mode a VM browser looks through for one whose commit
# holds the tarball (the Chronos open route's MAX_BAKES_LOOKED_AT).
MAX_BAKES_LOOKED_AT = 10
# Chronos's own terminal set (core_contracts TERMINAL_STATUSES: a review that
# is still starting or running has not ended), plus older spellings.
TERMINAL_STATUSES = frozenset(
    {
        "completed",
        "failed",
        "cancelled",
        "canceled",
        "stopped",
        "timeout",
        "error",
        "needs_human_annotation",
        "review_completed",
    }
)

_LOGIN_WORLD = "plato-world-login"


# --------------------------------------------------------------------------- #
# which account
# --------------------------------------------------------------------------- #


def _archived_date(value: Any) -> str | None:
    """``YYYY-MM-DD`` of an ``archived_at`` (ISO text, or a datetime), as the
    Chronos 409 prints it; None when there is no date to read."""
    if isinstance(value, datetime):
        return value.strftime("%Y-%m-%d")
    text = str(value or "").strip()
    if not text:
        return None
    try:
        return datetime.fromisoformat(text.replace("Z", "+00:00")).strftime("%Y-%m-%d")
    except ValueError:
        return text[:10]


def archived_refusal(row: Mapping[str, Any], *, default_of: str | None = None) -> str | None:
    """The Chronos open route's 409 for an archived account (with
    ``default_of``, its refusal for an archived default account), plus how to
    restore it; None when the row is not archived.

    ``default_of``: the app whose default account it is, when the caller named
    no account. The console's catalog flag (``archived`` with no date) reads
    the same, without the date."""
    if not is_archived(dict(row)):
        return None
    lk = normalize_key(str(row.get("login_key") or ""))
    ac = normalize_key(str(row.get("account") or ""))
    date = _archived_date(row.get("archived_at"))
    refusal = (
        f"{lk}/{ac} was archived{f' on {date}' if date else ''} by {row.get('archived_by') or 'someone'}: "
        f"{row.get('archived_reason') or 'no reason given'}; restore it first"
    )
    if default_of:
        refusal = f"The default account of {default_of} is archived: {refusal}"
    return f"{refusal} (`plato vault restore {lk} -a {ac}`, only if the account works again)"


def pick_account(rows: list[dict], login_key: str, account: str | None) -> tuple[dict, str]:
    """``(row, why)`` for the account to open.

    ``-a`` wins. Without it: the account whose ``default_for`` holds the
    login_key; else, when the source does not report defaults and the app has
    exactly one account, that one. Anything else is refused with the accounts
    listed, never guessed: opening the wrong account signs in as someone else.

    ``rows`` must hold the archived accounts too (``include_archived``): the
    account picked is refused (:class:`GateRefused`, the Chronos 409) when it
    is archived, and an archived default is named, never passed over for
    another account."""
    lk = normalize_key(login_key)
    mine = [r for r in rows if normalize_key(str(r.get("login_key") or "")) == lk]
    if not mine:
        raise NotFound(f"no accounts for login_key {lk!r} (see `plato vault list`)")
    names = ", ".join(sorted(str(r.get("account")) + (" (archived)" if is_archived(r) else "") for r in mine))
    row, why, default_of = _pick(mine, lk, account, names)
    if (refusal := archived_refusal({**row, "login_key": lk}, default_of=default_of)) is not None:
        raise GateRefused(refusal)
    return row, why


def _pick(mine: list[dict], lk: str, account: str | None, names: str) -> tuple[dict, str, str | None]:
    """:func:`pick_account`'s choice, archived or not: ``(row, why, default_of)``."""
    if account:
        ac = normalize_key(account)
        for row in mine:
            if normalize_key(str(row.get("account") or "")) == ac:
                return row, "given with -a", None
        raise NotFound(f"no account {ac!r} under {lk} (accounts: {names})")
    defaults = [r for r in mine if lk in (default_for(r) or [])]
    if len(defaults) == 1:
        return defaults[0], f"the default account for {lk}", lk
    if len(defaults) > 1:
        raise VaultConsoleError(f"{lk} has more than one default account ({names}); pass -a")
    known = any(default_for(r) is not None for r in mine)
    if not known and len(mine) == 1:
        return mine[0], f"the only account under {lk}", None
    why = "no account is marked default" if known else "this vault does not report default accounts"
    raise VaultConsoleError(f"{why} for {lk}; pass -a (accounts: {names})")


# --------------------------------------------------------------------------- #
# at most max_sessions per account
# --------------------------------------------------------------------------- #
#
# The same rule as the Chronos open route's, so the CLI refuses what the server
# would.


@dataclass(frozen=True)
class LiveSession:
    session_id: str
    kind: str  # "open" | "bake" | "run"
    status: str
    # A run whose ``accounts`` cannot be read: it may use any account, so it
    # counts as a run of this one (fail closed).
    unreadable: bool = False
    # An open with save (its world config's ``hold_save``): it rewrites the
    # saved login when it ends, as a bake does.
    saving: bool = False


class RunLogin(BaseModel):
    """A login a run's world config names: a ``login`` block, or an entry of
    its ``accounts`` (exploration ADR-0011). Either field may be left out."""

    login_key: str | None = None
    account: str | None = None


_RUN_ACCOUNTS: TypeAdapter[list[RunLogin]] = TypeAdapter(list[RunLogin])

# Clone name -> the ``(login_key, account)`` the login vault's defaults name for
# it (the accounts' ``default_for``, read the other way round).
CloneDefaults = Mapping[str, Sequence[tuple[str, str]]]


def clone_defaults(rows: Iterable[dict]) -> dict[str, list[tuple[str, str]]]:
    """:data:`CloneDefaults` from vault rows (``list``), by their ``default_for``."""
    found: dict[str, list[tuple[str, str]]] = {}
    for row in rows:
        key = (normalize_key(str(row.get("login_key") or "")), normalize_key(str(row.get("account") or "")))
        for clone in default_for(row) or []:
            found.setdefault(clone, []).append(key)
    return found


@dataclass(frozen=True)
class SessionFields:
    """What the busy check reads of a session's world config, each value as text.

    ``login_key``, ``account``, ``clone_name``, ``hold_minutes``, ``hold_save``
    and ``auto_login`` are the world config's; ``login`` is the top-level
    ``login`` block, ``config_login`` the world config's, ``accounts`` its
    multi-account entries."""

    package: str | None
    tags: list[str]
    login_key: str | None
    account: str | None
    clone_name: str | None
    hold_minutes: str | None
    hold_save: str | None
    auto_login: str | None
    login: RunLogin
    config_login: RunLogin
    accounts: list[RunLogin]

    @property
    def auto_login_on(self) -> bool:
        return (self.auto_login or "").strip().lower() == "true"

    @property
    def saves(self) -> bool:
        """An open that keeps the browser's end state (``plato vault open --save``)."""
        return (self.hold_save or "").strip().lower() == "true"


def _at(data: Any, *path: str) -> Any:
    for key in path:
        if not isinstance(data, dict):
            return None
        data = data.get(key)
    return data


def _text(value: Any) -> str | None:
    """A config value as Chronos reads it in SQL (JSON ``->>``): text, or None."""
    if value is None or isinstance(value, str):
        return value
    return json.dumps(value)


def _block(value: Any) -> RunLogin:
    return RunLogin(login_key=_text(_at(value, "login_key")), account=_text(_at(value, "account")))


def session_fields(session: dict) -> SessionFields | None:
    """The busy check's view of a session; None when its ``accounts`` is not a
    list of logins (it cannot be read)."""
    wc = session.get("world_config")
    try:
        accounts = _RUN_ACCOUNTS.validate_python(_at(wc, "config", "accounts") or [])
    except ValidationError:
        return None
    return SessionFields(
        package=_text(_at(wc, "package")),
        tags=[str(t) for t in session.get("tags") or []],
        login_key=_text(_at(wc, "config", "login_key")),
        account=_text(_at(wc, "config", "account")),
        clone_name=_text(_at(wc, "config", "clone_name")),
        hold_minutes=_text(_at(wc, "config", "hold_minutes")),
        hold_save=_text(_at(wc, "config", "hold_save")),
        auto_login=_text(_at(wc, "config", "auto_login")),
        login=_block(_at(wc, "login")),
        config_login=_block(_at(wc, "config", "login")),
        accounts=accounts,
    )


def needs_defaults(sessions: Iterable[dict]) -> bool:
    """Whether any session signs in with its clone's default (``auto_login``),
    so the check needs :func:`clone_defaults`."""
    return any((fields := session_fields(s)) is not None and fields.auto_login_on for s in sessions)


def _tag_value(tags: Iterable[Any], field: str) -> str | None:
    """A structured tag's value. Chronos stores ``login_key:x`` as ``login_key.x``."""
    for tag in tags or []:
        text = str(tag)
        for sep in (".", ":"):
            if text.startswith(f"{field}{sep}"):
                return text[len(field) + 1 :]
    return None


def _has_tag(tags: Iterable[Any], wanted: str) -> bool:
    return any(str(t).strip().lower() == wanted for t in tags or [])


def _hold_minutes(value: str | None) -> int:
    try:
        return int(value or 0)
    except ValueError:
        return 0


def run_logins(fields: SessionFields, defaults: CloneDefaults) -> set[tuple[str, str]]:
    """Every ``(login_key, account)`` a run signs in as, as the exploration world
    resolves them.

    The primary login is the world config's ``login`` block, else its first
    ``accounts`` entry. With ``auto_login`` on, the clone's default login
    (``defaults``) fills what that leaves out; written fields win. Every
    ``accounts`` entry without a login_key takes the primary's. The top-level
    ``login`` block counts as written."""
    if fields.config_login != RunLogin() or not fields.accounts:
        primary = fields.config_login
    else:
        primary = fields.accounts[0]
    filled = defaults.get(normalize_key(fields.clone_name), []) if fields.auto_login_on else []
    primaries = [(primary.login_key or lk, primary.account or ac) for lk, ac in filled] or [
        (primary.login_key, primary.account)
    ]
    logins = {(fields.login.login_key, fields.login.account), *primaries}
    for entry in fields.accounts:
        logins.update((entry.login_key or lk, entry.account) for lk, _ in primaries)
    return {(normalize_key(lk), normalize_key(ac)) for lk, ac in logins}


def session_use(
    fields: SessionFields, login_key: str, account: str, defaults: CloneDefaults | None = None
) -> str | None:
    """Whether a session uses ``login_key/account`` (normalized), and as what;
    None if not. A login-world session is an ``open`` (tagged ``vault_open``,
    or ``hold_minutes`` > 0) or a ``bake``; any other session whose
    ``login_key:``/``account:`` tags or logins (:func:`run_logins`) name the
    account is a ``run``."""
    tag_lk, tag_ac = _tag_value(fields.tags, "login_key"), _tag_value(fields.tags, "account")
    if (fields.package or "").startswith(_LOGIN_WORLD):
        key = tag_lk or fields.login_key or fields.clone_name or ""
        acct = tag_ac or fields.account or ""
        if normalize_key(key) != login_key or normalize_key(acct) != account:
            return None
        opened = _has_tag(fields.tags, OPEN_TAG) or _hold_minutes(fields.hold_minutes) > 0
        return "open" if opened else "bake"
    if (login_key, account) in run_logins(fields, defaults or {}):
        return "run"
    if tag_lk and tag_ac and normalize_key(tag_lk) == login_key and normalize_key(tag_ac) == account:
        return "run"
    return None


def session_kind(session: dict, login_key: str, account: str, defaults: CloneDefaults | None = None) -> str | None:
    """Whether a live session uses ``login_key/account``, and as what: ``open``
    (a person's browser), ``bake`` (a login-world sign-in) or ``run`` (anything
    else that signs in as it: its tags, a ``login`` block, a multi-account
    ``accounts`` entry, or with ``auto_login`` the clone's default from
    ``defaults``). A session whose ``accounts`` cannot be read is a ``run``:
    it may use the account. None if not."""
    fields = session_fields(session)
    if fields is None:
        return "run"
    return session_use(fields, normalize_key(login_key), normalize_key(account), defaults)


def find_live_sessions(
    sessions: Iterable[dict], login_key: str, account: str, defaults: CloneDefaults | None = None
) -> list[LiveSession]:
    """Every live session in ``sessions`` that uses this account."""
    lk, ac = normalize_key(login_key), normalize_key(account)
    found: dict[str, LiveSession] = {}
    for session in sessions:
        sid = str(session.get("public_id") or "")
        if not sid:
            continue
        status = str(session.get("status") or "")
        fields = session_fields(session)
        if fields is None:
            found[sid] = LiveSession(sid, "run", status, unreadable=True)
        elif (kind := session_use(fields, lk, ac, defaults)) is not None:
            found[sid] = LiveSession(sid, kind, status, saving=kind == "open" and fields.saves)
    return list(found.values())


def max_sessions_of(row: Mapping[str, Any]) -> int:
    """How many live sessions may use the account at once: the row's
    ``max_sessions`` (the Chronos vault's field), else 1. The login console does
    not send it, and 1 is the vault's own default: one session at a time."""
    value = row.get("max_sessions")
    return value if isinstance(value, int) and not isinstance(value, bool) and value >= 1 else 1


def with_last_bake(live: list[LiveSession], last_bake_id: str | None, status: str | None) -> list[LiveSession]:
    """``live`` plus the account's last bake while it has not ended. A bake in a
    review status is not in ``live`` (Chronos lists live statuses only) but still
    counts, as on the Chronos open route; one already in ``live`` counts once."""
    if not last_bake_id or not status or status in TERMINAL_STATUSES:
        return live
    if any(s.session_id == last_bake_id for s in live):
        return live
    return [*live, LiveSession(last_bake_id, "bake", status)]


def count_last_bake(
    read_session: Callable[[str], dict], live: list[LiveSession], last_bake_id: str | None
) -> list[LiveSession]:
    """:func:`with_last_bake`, reading the bake's status only when it is not in
    ``live`` already. A bake Chronos does not find (gone, or another org's) does
    not count: the open route cannot see it either. An answer without a status
    fails the check: counting the bake as ended could start an open beside it."""
    if not last_bake_id or any(s.session_id == last_bake_id for s in live):
        return live
    try:
        body = read_session(last_bake_id)
    except NotFoundError:
        return live
    status = body.get("status") if isinstance(body, dict) else None
    if not isinstance(status, str) or not status:
        raise VaultConsoleError(
            f"cannot read the status of the account's last bake {last_bake_id}, "
            "so cannot check that the account is free; try again"
        )
    return with_last_bake(live, last_bake_id, status)


def refuse_if_busy(live: list[LiveSession], login_key: str, account: str, *, limit: int, save: bool = False) -> None:
    """The Chronos open route's rules, each
    message the route's 409 text plus how to act on it from the CLI:

    * an open with ``save`` rewrites the saved login, as a bake does, so it is
      refused while a bake of the account (the last bake too, while it has not
      ended) or another saving open is live, whatever ``limit`` says;
    * any open is refused while the live sessions using the account (opens,
      bakes and runs, the last bake while it has not ended) number ``limit``
      (the account's ``max_sessions``) or more."""
    lk, ac = normalize_key(login_key), normalize_key(account)
    if save and (blocking := [s for s in live if s.kind == "bake" or s.saving]):
        which = "; ".join(
            f"{'saving open' if s.saving else s.kind} session {s.session_id} ({s.status or 'live'})"
            + (", whose accounts list cannot be read" if s.unreadable else "")
            for s in blocking
        )
        raise GateRefused(
            f"{lk}/{ac} is in use: {which}. An open with save rewrites the saved login, as a bake "
            "does, so it needs the account free of bakes and other saving opens: wait for it to end, "
            "stop it, or open without save. "
            "End an open with `plato vault close <id>` and a bake with `plato chronos stop <id>`, "
            "or run `plato vault open` again without --save"
        )
    if len(live) < limit:
        return
    which = ", ".join(
        f"{s.kind} {s.session_id} ({s.status or 'live'}"
        + ("; its accounts list cannot be read, so it counts" if s.unreadable else "")
        + ")"
        for s in live
    )
    where = "over" if len(live) > limit else "at"
    raise GateRefused(
        f"{lk}/{ac} is {where} its limit ({len(live)} of {limit}): {which}. "
        "Wait for one to end or stop it, or raise the account's max_sessions. "
        "End an open with `plato vault close <id>` and anything else with `plato chronos stop <id>`; "
        f"raise the limit with `plato vault edit {lk} -a {ac} --max-sessions N`"
    )


# --------------------------------------------------------------------------- #
# which saved login
# --------------------------------------------------------------------------- #


def hosted_browser(browser_mode: str | None) -> bool:
    """Open in a Browserbase browser (Live View) rather than a VM Chrome (noVNC).
    Only a pure ``browserbase`` account: a ``browserbase_via_vm`` account signs in
    on a VM because the hosted browser cannot finish that site's sign-in, so it
    opens there."""
    return (browser_mode or "").strip().lower() == "browserbase"


def seed_modes(browser_mode: str | None) -> list[bool]:
    """The ``cdp_browser`` filters to try, in order, when looking up the saved login.

    VM Chrome needs a tarball: a ``chrome`` bake (``mode:vm``). A
    ``browserbase_via_vm`` bake commits a tarball AND a Context and is tagged
    ``mode:cdp_browser``, so a via-VM account looks there first, then at older VM
    bakes. A ``browserbase`` account needs a Context (``mode:cdp_browser``)."""
    mode = (browser_mode or "").strip().lower()
    if mode == "browserbase":
        return [True]
    if mode == "browserbase_via_vm":
        return [True, False]
    return [False]


@dataclass(frozen=True)
class SeedRef:
    session_id: str
    step_name: str

    @property
    def config_ref(self) -> str:
        return f"{self.session_id}:{self.step_name}"


TARBALL = "snapshot.tar.gz"


def has_tarball(listing: Any) -> bool:
    """Whether a workspace file listing (``WorkspaceFilesResponse``) holds the
    VM browser's tarball."""
    return any(
        str(getattr(entry, "relpath", "")).rsplit("/", 1)[-1] == TARBALL
        for directory in getattr(listing, "directories", None) or []
        for entry in getattr(directory, "entries", None) or []
    )


async def _tarball_in(chronos: Any, snap: login_snapshot.ResolvedSnapshot) -> bool | None:
    """Whether the bake's commit holds a tarball; None when Chronos cannot list
    it (a network error or an error status: the bake is then kept, and at worst
    the agent signs in for real). Any other error is a bug and is raised."""
    try:
        listing = await list_workspace_files.asyncio(chronos._client, snap.session_id, snap.step_name, snap.repo_name)
    except (httpx.HTTPError, APIError):
        return None
    return has_tarball(listing)


def _created(snap: Any) -> datetime:
    ts = getattr(snap, "created_at", None)
    if not isinstance(ts, datetime):
        return datetime.min.replace(tzinfo=UTC)
    return ts if ts.tzinfo else ts.replace(tzinfo=UTC)


async def saved_logins(
    chronos: Any, login_key: str, account: str, *, cdp_browser: bool, limit: int = MAX_BAKES_LOOKED_AT
) -> AsyncIterator[login_snapshot.ResolvedSnapshot]:
    """This account's successful bakes in one mode, newest first, at most ``limit``.

    The resolver's rule (``login_snapshot._pick_branch`` and its own-commit ref),
    taken again from what is left, so the first one is what
    ``resolve_latest_snapshot`` returns. Lazy: each bake costs one read of its
    refs, so only the bakes a caller looks at are read."""
    repo_name = login_snapshot.snapshot_repo_name(login_key)
    repo_id = await login_snapshot._snapshot_repo_id(chronos._client, repo_name)
    if not repo_id:
        return
    rows = list((await list_workspace_branches.asyncio(chronos._client, repo_id)).branches or [])
    for _ in range(limit):
        row = login_snapshot._pick_branch(rows, login_key=login_key, account=account, cdp_browser=cdp_browser)
        if row is None:
            return
        rows = [r for r in rows if r is not row]
        own = await login_snapshot._own_commit(chronos._client, row.session_public_id, repo_name)
        yield login_snapshot.ResolvedSnapshot(
            session_id=row.session_public_id,
            repo_name=repo_name,
            step_name=own.step_name if own else row.last_step,
            created_at=getattr(own, "created_at", None) or getattr(row, "updated_at", None),
        )


async def _resolve(
    chronos_url: str, api_key: str, login_key: str, account: str, modes: list[bool], *, needs_tarball: bool
) -> SeedRef | None:
    from plato.chronos.sdk import AsyncChronos

    found = []
    async with AsyncChronos(base_url=chronos_url, api_key=api_key) as chronos:
        for cdp in modes:
            async for snap in saved_logins(chronos, login_key, account, cdp_browser=cdp):
                # A VM browser loads only a tarball: a pure-Browserbase bake of a
                # via-VM account holds a Context alone, so look further back
                # (as the Chronos open route does).
                if needs_tarball and await _tarball_in(chronos, snap) is False:
                    continue
                found.append(snap)
                break
    if not found:
        return None
    best = max(found, key=_created)
    return SeedRef(best.session_id, best.step_name)


def resolve_seed(
    chronos_url: str, api_key: str, login_key: str, account: str, browser_mode: str | None
) -> SeedRef | None:
    """The newest successful bake of this account the browser can load, or None
    (never baked: the world signs in for real). Uses the exploration world's
    resolver (``plato.chronos.login_snapshot``), so a person gets the login the
    runs get. A VM browser takes the newest bake that holds a tarball, in either
    mode a via-VM account bakes in, looking back up to
    :data:`MAX_BAKES_LOOKED_AT` bakes per mode."""
    return asyncio.run(
        _resolve(
            chronos_url,
            api_key,
            normalize_key(login_key),
            normalize_key(account),
            seed_modes(browser_mode),
            needs_tarball=not hosted_browser(browser_mode),
        )
    )


# --------------------------------------------------------------------------- #
# the launch
# --------------------------------------------------------------------------- #


def _ltree_tag(tag: str) -> str:
    """The SDK launch's tag normalization (``plato.chronos.sdk._normalize_tag``)."""
    return tag.replace("-", "_").replace(":", ".").replace(" ", "_")


def snapshot_repo(login_key: str) -> str:
    return f"login/{normalize_key(login_key)}/snapshot"


def vm_timeout(minutes: int, sign_in_budget_seconds: int) -> int:
    """The VMs' platform lifetime (seconds): the hold plus the sign-in budget.
    The world's own timer ends the hold; this is the backstop when the world
    wedges, so a signed-in browser is never up for the default 12-22 hours."""
    return int(minutes) * 60 + sign_in_budget_seconds


def check_world_schema(schema: Any, world_package: str) -> None:
    """Refuse a login world without open mode. RunConfig ignores an unknown
    field, so an older world would run an ordinary bake: a real sign-in and a
    new snapshot, and no browser for anyone."""
    config_schema = getattr(schema, "config_schema", None)
    if hasattr(config_schema, "model_dump"):
        config_schema = config_schema.model_dump()
    properties = config_schema.get("properties") if isinstance(config_schema, dict) else None
    if OPEN_MODE_FIELD not in (properties or {}):
        version = getattr(schema, "version", None) or "?"
        raise VaultConsoleError(
            f"{world_package} (version {version}) has no open mode yet. Wait for the login "
            "world release, or pass --world-package with a version that has it"
        )


# The login-agent fields an open reads (Chronos's LoginVaultLoginSettings checks the rest).
class LoginAgent(BaseModel):
    # Another key (runtime, image, ...) is refused, not dropped, as Chronos refuses it.
    model_config = ConfigDict(extra="forbid")

    package: str
    agent_name: str | None = None  # None or "": the package's default agent
    config: dict[str, Any]


class LoginVm(BaseModel):
    cpus: PositiveInt
    memory: PositiveInt
    disk: PositiveInt
    timeout: PositiveInt | None = None  # a bake's; an open sets its own


class LoginRuntime(BaseModel):
    vm: LoginVm


class LoginWorldConfig(BaseModel, extra="allow"):
    agent: LoginAgent


class LoginWorld(BaseModel):
    package: str
    runtime: LoginRuntime
    config: LoginWorldConfig


class LoginOpen(BaseModel):
    sign_in_budget_seconds: PositiveInt


class LoginSelfHeal(BaseModel):
    vm_timeout: PositiveInt


class LoginMetadata(BaseModel):
    open: LoginOpen
    self_heal: LoginSelfHeal


class LoginSettings(BaseModel):
    version: int  # every open is tagged login_agent:v<N>
    source: str
    world: LoginWorld
    metadata: LoginMetadata

    def filled(self, **params: str) -> LoginSettings:
        """These settings with the template's ``${LOGIN_*}`` filled (:func:`fill_template`)."""
        return self.model_validate(fill_template(self.model_dump(mode="json"), params))

    def describe(self) -> str:
        agent = self.world.config.agent
        model, turns = agent.config.get("model_name"), agent.config.get("max_turns")
        name = agent.agent_name or "default agent"
        return f"{name} on {agent.package}, {model}, {turns} turns ({self.source or 'Chronos'})"


def fill_template(value: Any, params: Mapping[str, str]) -> Any:
    """``value`` with ``${LOGIN_KEY}``, ``${LOGIN_ACCOUNT}``, ``${LOGIN_URL}`` and
    ``${LOGIN_VAULT}`` replaced from ``params`` in every string, at any depth.
    Nothing else changes: the secrets' ``${...}`` stay for Chronos."""
    if isinstance(value, str):
        return _TEMPLATE_PARAM.sub(lambda m: params[m.group(1)], value)
    if isinstance(value, dict):
        return {k: fill_template(v, params) for k, v in value.items()}
    if isinstance(value, list):
        return [fill_template(v, params) for v in value]
    return value


def no_login_settings(reason: str) -> VaultConsoleError:
    """The refusal when Chronos gives no usable login settings."""
    return VaultConsoleError(
        f"Chronos gave no login settings ({reason}). An open launches what the vault org's "
        f"{LOGIN_EXPERIMENT} experiment says, read with your Plato key, which must be in that org"
    )


def login_settings(file: Any) -> LoginSettings:
    """The latest version of the login-agent experiment (``file``: Chronos's
    reply). Refusals name fields, never values."""
    if not isinstance(file, dict) or file.get("name") != LOGIN_EXPERIMENT:
        raise no_login_settings(f"experiment {LOGIN_EXPERIMENT_ID} is not named {LOGIN_EXPERIMENT}")
    version = file.get("latest_version")
    if not isinstance(version, dict) or not isinstance(version.get("config_json"), dict):
        raise no_login_settings(f"the {LOGIN_EXPERIMENT} experiment has no version with a config")
    number = version.get("version_number")
    try:
        settings = LoginSettings.model_validate(
            {**version["config_json"], "version": number, "source": f"experiment:{LOGIN_EXPERIMENT}:v{number}"}
        )
    except ValidationError as e:
        where = ".".join(str(p) for p in e.errors()[0]["loc"])
        raise no_login_settings(f"the {LOGIN_EXPERIMENT} experiment has no usable {where}") from None
    if settings.world.package.rsplit(":", 1)[0] != _LOGIN_WORLD:
        raise no_login_settings(f"the {LOGIN_EXPERIMENT} experiment has no usable world.package")
    if owned := sorted(LAUNCH_OWNED_KEYS & settings.world.config.model_dump().keys()):
        raise no_login_settings(
            f"the {LOGIN_EXPERIMENT} experiment sets what each launch sets itself: {', '.join(owned)}"
        )
    return settings


def build_open_launch(
    *,
    login_key: str,
    account: str,
    login_url: str,
    browser_mode: str | None,
    proxy_exit: str | None,
    minutes: int,
    save: bool,
    opened_by: str,
    seed: SeedRef | None,
    settings: LoginSettings,
    world_package: str | None = None,
) -> dict[str, Any]:
    """The ``/api/jobs/launch`` body. Secret-free: credentials stay in 1Password
    and every key is a ``${...}`` placeholder Chronos fills from the org's
    secrets. The exit goes by NAME; the world resolves and ban-checks it.
    It starts from ``settings`` (the template, filled for this account); this
    open's keys go on top and always win. ``world_package`` (a dev build, say)
    replaces their package."""
    if not 1 <= minutes <= MAX_MINUTES:
        raise VaultConsoleError(f"--minutes must be 1..{MAX_MINUTES}")
    lk, ac = normalize_key(login_key), normalize_key(account)
    bb = hosted_browser(browser_mode)
    settings = settings.filled(LOGIN_KEY=lk, LOGIN_ACCOUNT=ac, LOGIN_URL=login_url, LOGIN_VAULT=OP_VAULT)
    lifetime = vm_timeout(minutes, settings.metadata.open.sign_in_budget_seconds)
    agent = settings.world.config.agent
    config: dict[str, Any] = {
        # A VM browser gets none of the template's Browserbase keys (no Browserbase secret needed).
        **{k: v for k, v in settings.world.config.model_dump(mode="json").items() if bb or k not in BROWSERBASE_KEYS},
        # This open's keys win over the template's, the 1Password fields too.
        "clone_name": lk,
        "login_key": lk,
        "account": ac,
        "target_url": login_url,
        "op_service_account_token": OP_TOKEN,
        "op_vault": OP_VAULT,
        "hold_minutes": minutes,
        "hold_save": save,
        "opened_by": opened_by,
        # Pinned either way, so the world's vault fill never switches the mode.
        "cdp_browser": bb,
        # The password is TYPED blind, never printed into the agent's trace: the
        # person who opened the browser can read the session.
        "agent_types_password": False,
        # The agent VM's lifetime too (the warm-pool floor is 12 h otherwise).
        "min_warmpool_timeout": lifetime,
        "agent": {
            "package": agent.package,
            **({"agent_name": agent.agent_name} if agent.agent_name else {}),
            "runtime": {"type": "vm", "vm": {"timeout": lifetime}},
            # No chrome_start_url: the world opens where it LOOKS for a
            # signed-in browser (the app's home when the login page hides it).
            "config": {k: v for k, v in agent.config.items() if k != "chrome_start_url"},
        },
    }
    if proxy_exit:
        config["proxy_exit"] = proxy_exit
    if seed is not None:
        # Restored into the world's own snapshot workspace before it starts.
        config["state"] = {"workspaces": {snapshot_repo(lk): seed.config_ref}}
    tags = [lk, ac, OPEN_TAG, f"login_key:{lk}", f"account:{ac}", f"login_agent:v{settings.version}"]
    if opened_by:
        tags.append(f"opened_by:{normalize_key(opened_by)}")
    return {
        # Chronos keeps tags as an ltree (``login_key.x``); the SDK's launch sends
        # them in that shape, and so does this.
        "tags": [_ltree_tag(t) for t in tags],
        "world": {
            "package": world_package or settings.world.package,
            "runtime": {"type": "vm", "vm": {**settings.world.runtime.vm.model_dump(), "timeout": lifetime}},
            "config": config,
        },
    }


# --------------------------------------------------------------------------- #
# Chronos
# --------------------------------------------------------------------------- #


def _session_rows(body: Any, which: str) -> list[dict]:
    """The rows of one /api/sessions page. A page without a ``sessions`` list,
    or a row without a ``public_id``, is refused: read as empty or skipped, a
    live session would go uncounted and the account look free. A row's status
    is not checked (Chronos may add new ones)."""
    found = body.get("sessions") if isinstance(body, dict) else None
    if not isinstance(found, list):
        raise VaultConsoleError(
            f"Chronos answered the {which} sessions list without a 'sessions' list; cannot check that the account is free"
        )
    for row in found:
        if not isinstance(row, dict) or not isinstance(row.get("public_id"), str) or not row["public_id"]:
            raise VaultConsoleError(
                f"Chronos listed a {which} session without a public_id; cannot check that the account is free"
            )
    return found


class OpenClient:
    """The raw Chronos calls `open` makes, with the caller's own key."""

    def __init__(self, base_url: str, api_key: str, *, transport: httpx.BaseTransport | None = None) -> None:
        self.base_url = base_url.rstrip("/")
        self._client = httpx.Client(
            base_url=self.base_url,
            headers={"X-API-Key": api_key},
            timeout=60.0,
            transport=transport,
        )

    def close(self) -> None:
        self._client.close()

    def _get(self, path: str, **params: Any) -> Any:
        response = self._client.get(path, params=params or None)
        raise_for_status(response)
        return response.json()

    def me(self) -> str:
        """The caller's email, or "" when Chronos will not say."""
        try:
            return str((self._get("/api/auth/me") or {}).get("email") or "")
        except (APIError, httpx.HTTPError, ValueError):
            # Refused, unreachable, or a body that is not JSON: only the audit
            # tag and the messages lose the name. Anything else is a bug.
            return ""

    def login_settings(self) -> LoginSettings:
        """The vault org's login-agent experiment, by id: experiments are
        org-scoped, so the caller's key must be in that org."""
        try:
            file = self._get(LOGIN_EXPERIMENT_PATH)
        except APIError as e:
            if e.status_code not in (403, 404):
                raise  # chronos_errors names it
            raise no_login_settings(
                f"your key cannot see the vault org's {LOGIN_EXPERIMENT} experiment ({e.status_code})"
            ) from None
        except ValueError:  # the body is not JSON
            raise no_login_settings(f"the {LOGIN_EXPERIMENT} experiment reply is not JSON") from None
        return login_settings(file)

    def live_sessions(self) -> list[dict]:
        """Every queued/starting/running/pending session (child sessions and
        archived ones too), every page: the Chronos open route checks them all.
        Chronos takes one status per request, lists archived sessions only on
        their own (``archived_only``; archiving does not stop a session), and
        returns at most :data:`SESSION_PAGE` rows a page."""
        merged: dict[str, dict] = {}
        for status in LIVE_STATUSES:
            for archived in (False, True):
                for row in self._all_pages(status, archived):
                    merged[row["public_id"]] = row
        return list(merged.values())

    def _all_pages(self, status: str, archived: bool) -> list[dict]:
        """Every page of one status. Chronos pages by offset over a list that
        changes meanwhile: a session that ends moves the rest forward, so each
        page starts :data:`PAGE_OVERLAP` rows before the last one ended. A page
        that shares none of those rows means the list moved further than that
        between two requests, and a row may have been skipped: refused, never
        a partial list."""
        rows: list[dict] = []
        overlap = max(0, min(PAGE_OVERLAP, SESSION_PAGE - 1))
        offset, tail = 0, set()
        for _ in range(MAX_SESSION_PAGES):
            body = self._get(
                "/api/sessions",
                status=status,
                limit=SESSION_PAGE,
                offset=offset,
                top_level_only="false",
                archived_only=str(archived).lower(),
                # Children come as rows of their own (top_level_only=false).
                include_children="false",
            )
            found = _session_rows(body, f"{'archived ' if archived else ''}{status}")
            ids = [row["public_id"] for row in found]
            if tail and tail.isdisjoint(ids):
                raise VaultConsoleError(
                    f"the {'archived ' if archived else ''}{status} sessions changed while they were "
                    "read, so one may have been missed; try again"
                )
            rows.extend(found)
            if len(found) < SESSION_PAGE:
                return rows
            tail = set(ids[len(ids) - overlap :]) if overlap else set()
            offset += SESSION_PAGE - overlap
        # Never a partial list: a session past it could use the account.
        raise VaultConsoleError(
            f"more than {offset + overlap} {'archived ' if archived else ''}{status} sessions; "
            "cannot check that the account is free"
        )

    def world_schema(self, world_package: str) -> Any:
        """The registry's schema of ``world_package`` (``name[:version]``)."""
        from plato.chronos.api.registry import (
            get_world_schema_api_registry_worlds__package_name__schema_get as get_schema,
        )

        name, _, version = world_package.partition(":")
        pinned = version not in ("", "latest")
        return get_schema.sync(
            self._client, package_name=name, version=version if pinned else None, allow_prerelease=pinned
        )

    def launch(self, body: dict[str, Any]) -> str:
        response = self._client.post("/api/jobs/launch", json=body, timeout=150.0)
        raise_for_status(response)
        return str((response.json() or {}).get("session_id") or "")

    def session(self, session_id: str) -> dict:
        return self._get(f"/api/sessions/{session_id}") or {}

    def set_tags(self, session_id: str, tags: list[str]) -> None:
        """Replace the session's tags (Chronos stores them in ltree form)."""
        response = self._client.patch(f"/api/sessions/{session_id}/tags", json={"tags": tags})
        raise_for_status(response)


def close_tags(session: dict) -> list[str] | None:
    """The tags to write so the world ends the hold: the session's own, plus
    :data:`CLOSE_TAG`; None when it already has the tag (a second close writes
    nothing: Chronos only REPLACES tags, so every write can race the world's own
    final tags). Refuses a session that is not a ``plato vault open`` one: a
    bake or a run has no hold to end, and the tag would mean nothing to it."""
    tags = [str(t) for t in session.get("tags") or []]
    if not _has_tag(tags, OPEN_TAG):
        raise VaultConsoleError(
            "not a `plato vault open` session (no vault_open tag); end other sessions with `plato chronos stop`"
        )
    return None if _has_tag(tags, CLOSE_TAG) else [*tags, CLOSE_TAG]


def transient(exc: BaseException) -> bool:
    """A session read worth retrying in a wait: the network failed, or Chronos
    is briefly down (5xx, 429). Anything else (a 401/404, a reply that is not
    the session) would fail the same way every time, so the wait raises it."""
    if isinstance(exc, httpx.TransportError):
        return True
    return isinstance(exc, APIError) and (exc.status_code >= 500 or exc.status_code == 429)


def link_of(session: dict) -> str | None:
    """The browser link the world put on the session page, if it has yet."""
    for entry in session.get("preview_urls") or []:
        if isinstance(entry, dict) and str(entry.get("label") or "").startswith(LINK_LABEL_PREFIX):
            return str(entry.get("url") or "") or None
    return None


@dataclass(frozen=True)
class LinkWait:
    link: str | None
    status: str
    reason: str | None = None


def wait_for_link(
    get_session: Callable[[], dict],
    *,
    timeout: float = LINK_WAIT_SECONDS,
    poll: float = LINK_POLL_SECONDS,
    sleep: Callable[[float], None] | None = None,
    clock: Callable[[], float] | None = None,
    on_poll: Callable[[str], None] | None = None,
) -> LinkWait:
    """Poll the session until its link appears, it ends, or ``timeout``. A read
    that fails for a :func:`transient` reason is retried; any other is raised."""
    sleep = sleep or time.sleep
    clock = clock or time.monotonic
    deadline = clock() + timeout
    status = ""
    while True:
        try:
            session = get_session()
        except Exception as exc:
            if not transient(exc):
                raise
            session = {}  # one failed read is not the end of the wait
        status = str(session.get("status") or status or "").lower()
        link = link_of(session)
        if link:
            return LinkWait(link, status)
        if status in TERMINAL_STATUSES:
            return LinkWait(None, status, session.get("status_reason"))
        if on_poll:
            on_poll(status)
        if clock() >= deadline:
            return LinkWait(None, status, "timed out waiting for the link")
        sleep(poll)


def wait_for_end(
    get_session: Callable[[], dict],
    *,
    timeout: float = CLOSE_WAIT_SECONDS,
    poll: float = CLOSE_POLL_SECONDS,
    sleep: Callable[[float], None] | None = None,
    clock: Callable[[], float] | None = None,
) -> str:
    """Poll until the session ends; its last status (terminal, or not yet). A
    read that fails for a :func:`transient` reason is retried; any other is raised."""
    sleep = sleep or time.sleep
    clock = clock or time.monotonic
    deadline = clock() + timeout
    status = ""
    while True:
        try:
            status = str(get_session().get("status") or status or "").lower()
        except Exception as exc:
            if not transient(exc):
                raise
        if status in TERMINAL_STATUSES or clock() >= deadline:
            return status
        sleep(poll)
