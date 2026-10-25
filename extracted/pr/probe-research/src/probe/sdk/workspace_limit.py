"""This computer's workspace limit: a client-side limiter on what Probe reads.

NOT AUTH. No token, scope, credential or role changes. The computer stores
"limit to workspace W" beside its filing pin (``contexts.<ctx>.workspace``, see
`probe.sdk.config`) and sends it on every API request it makes; the API narrows
that request's READS to W in one place. It only ever narrows, never widens, and
anyone on the computer can change it (`probe workspace limit`, the desktop app).

    contexts.<ctx>.workspace = {"id": W, "project": ..., "limit": true,
                                "team_items": "show" | "hide", "name": ..., "slug": ...}

Whole team is ``limit`` false or absent; ``id`` stays the filing pin either way.

The wire (fixed with the server lane):

    X-Probe-Workspace-Limit: <W uuid>            only when limited
    X-Probe-Workspace-Limit-Team-Items: show|hide (absent reads as show)
    X-Probe-Workspace-Limit-Applied: <W uuid>    the API's echo, on every answer it limited

`PROBE_WORKSPACE_LIMIT=<uuid|slug>` (+ `PROBE_WORKSPACE_LIMIT_TEAM_ITEMS`) limits one
process -- a job on another machine has no config -- and `PROBE_WORKSPACE_LIMIT=team`
forces no limit. A slug costs one `GET /v1/workspaces` WITHOUT the limit (cached per
process).

These headers sit BESIDE `probe.client_headers`, not in it: that module's headers are
telemetry, never identity or authorization; this one is neither too, but it changes
what the server answers, so it gets its own rules here. Account plumbing (sign-in,
`/v1/me` key checks, logout, device state) builds its own `Settings` and never carries
it: a stale limit must never stop a person signing out or fixing it.

FAIL CLOSED. Nothing here falls back to the whole team: a limit this process cannot
turn into a uuid raises (`WorkspaceLimitUnknown`, `InvalidWorkspaceLimit`) instead of
being dropped, and a hosted MCP that cannot read a forwarded value forwards a value
the API refuses.
"""

from __future__ import annotations

import contextvars
import os
import re
import threading
import uuid
from collections.abc import Callable, Iterator, Mapping
from contextlib import contextmanager
from dataclasses import dataclass

from probe._compat import StrEnum

from . import errors

LIMIT_HEADER = "X-Probe-Workspace-Limit"
TEAM_ITEMS_HEADER = "X-Probe-Workspace-Limit-Team-Items"
#: The API's echo: present on every response of a request it limited, 404s included.
APPLIED_HEADER = "X-Probe-Workspace-Limit-Applied"

LIMIT_ENV = "PROBE_WORKSPACE_LIMIT"
TEAM_ITEMS_ENV = "PROBE_WORKSPACE_LIMIT_TEAM_ITEMS"
#: `PROBE_WORKSPACE_LIMIT=team`: this process sees the whole team, whatever the config says.
TEAM_WORD = "team"

#: `contexts.<ctx>.workspace` keys the limit owns (beside the pin's `id` and `project`).
LIMIT_KEY = "limit"
TEAM_ITEMS_KEY = "team_items"
NAME_KEY = "name"
SLUG_KEY = "slug"
LIMIT_KEYS = (LIMIT_KEY, TEAM_ITEMS_KEY, NAME_KEY, SLUG_KEY)

#: What `probe workspace limit` points a person at.
COMMAND = "probe workspace limit"
TEAM_COMMAND = "probe workspace limit --team"

#: A forwarded value the hosted MCP could not read: sent on as this, which the API
#: refuses (400 `invalid_workspace_limit`) -- never dropped, which would widen.
UNREADABLE_FORWARD = "unreadable"
#: A header value from a caller, at most (a uuid is 36; `id:` + slug forms are short).
_FORWARD_MAX = 200
_FORWARD_RE = re.compile(r"^[A-Za-z0-9._:-]{1,200}$")


class TeamItems(StrEnum):
    """Team-wide items under a limit: the team note, the "All workspaces" summary and
    connector/GitHub docs in search. The shared folder and datasets always show."""

    SHOW = "show"
    HIDE = "hide"


class Source(StrEnum):
    """Where a limit came from."""

    CONFIG = "config"
    ENV = "env"


def _bare(ref: object) -> str:
    text = str(ref or "").strip()
    return text[3:] if text.startswith("id:") else text


def as_uuid(ref: object) -> str | None:
    """`ref` (bare or `id:<uuid>`) as a canonical uuid, else None."""
    try:
        return str(uuid.UUID(_bare(ref)))
    except (ValueError, AttributeError, TypeError):
        return None


@dataclass(frozen=True)
class WorkspaceLimit:
    """One resolved limit. `ref` is a uuid from the config, or what the environment
    named (a uuid or a slug); `team_items` is kept as found and checked when sent."""

    ref: str
    team_items: str = TeamItems.SHOW.value
    name: str | None = None
    slug: str | None = None
    source: Source = Source.CONFIG

    @property
    def id(self) -> str | None:
        """The workspace's uuid when this limit names one directly."""
        return as_uuid(self.ref)

    @property
    def hides_team_items(self) -> bool:
        return str(self.team_items).strip().lower() == TeamItems.HIDE.value

    @property
    def label(self) -> str:
        """How a person reads it: the name, else the slug, else the id."""
        return self.name or self.slug or self.id or self.ref or "an unnamed workspace"

    def as_json(self) -> dict:
        """`probe status --json`'s `account.workspace_limit` and `probe workspace limit
        --json`'s `workspace_limit`: `{"id", "name", "slug", "team_items"}`."""
        slug = self.slug
        if slug is None and self.id is None and self.ref:
            # An environment slug not looked up yet (status reads no network).
            slug = self.ref[5:] if self.ref.startswith("slug:") else self.ref
        return {"id": self.id, "name": self.name, "slug": slug, "team_items": self.team_items}

    def checked_team_items(self) -> str:
        """`show` or `hide`, else InvalidWorkspaceLimit naming where the value came from."""
        value = str(self.team_items or TeamItems.SHOW.value).strip().lower()
        if value in (TeamItems.SHOW.value, TeamItems.HIDE.value):
            return value
        where = f"{TEAM_ITEMS_ENV}={self.team_items!r}" if self.source is Source.ENV else (
            f"this computer's workspace limit has team_items={self.team_items!r}"
        )
        raise errors.InvalidWorkspaceLimit(
            f"{where}, which is not show or hide. Run `{COMMAND} <workspace> --team-items show` "
            f"(or hide), or `{TEAM_COMMAND}`.",
            status=None,
            detail={"code": errors.INVALID_WORKSPACE_LIMIT},
        )


def stored(context: Mapping | None) -> WorkspaceLimit | None:
    """The limit a context dict stores, or None for the whole team."""
    anchor = (context or {}).get("workspace") if isinstance(context, Mapping) else None
    if not isinstance(anchor, Mapping) or anchor.get(LIMIT_KEY) is not True:
        return None
    name = anchor.get(NAME_KEY)
    slug = anchor.get(SLUG_KEY)
    return WorkspaceLimit(
        ref=_bare(anchor.get("id")),
        team_items=str(anchor.get(TEAM_ITEMS_KEY) or TeamItems.SHOW.value),
        name=name if isinstance(name, str) and name else None,
        slug=slug if isinstance(slug, str) and slug else None,
        source=Source.CONFIG,
    )


def resolve_limit(context: Mapping | None, environ: Mapping[str, str] | None = None) -> WorkspaceLimit | None:
    """The limit in effect: `PROBE_WORKSPACE_LIMIT` first (`team` = none), else the
    context's. `PROBE_WORKSPACE_LIMIT_TEAM_ITEMS` overrides the team-items choice of
    either. Reads no network."""
    env = os.environ if environ is None else environ
    raw = (env.get(LIMIT_ENV) or "").strip()
    items = (env.get(TEAM_ITEMS_ENV) or "").strip()
    if raw.lower() == TEAM_WORD:
        return None
    if raw:
        here = stored(context)
        same = here is not None and here.id is not None and here.id == as_uuid(raw)
        return WorkspaceLimit(
            ref=raw,
            team_items=items or TeamItems.SHOW.value,
            # The config's labels when the env names the same workspace.
            name=here.name if same else None,
            slug=here.slug if same else None,
            source=Source.ENV,
        )
    limit = stored(context)
    if limit is not None and items:
        return WorkspaceLimit(
            ref=limit.ref, team_items=items, name=limit.name, slug=limit.slug, source=Source.ENV
        )
    return limit


# -- turning a ref into a uuid ------------------------------------------------

#: (base_url, account, ref) -> uuid, for this process's life: the slug an environment
#: named. `account` is the credential's fingerprint: two teams on one API can both
#: have an `eng` workspace, and a switched login must never reuse the other's uuid.
_RESOLVED: dict[tuple[str, str, str], str] = {}
_RESOLVED_LOCK = threading.Lock()


def account_key(bearer: str | None) -> str:
    """A credential's cache identity: a short hash, never the secret itself."""
    import hashlib

    return hashlib.sha256((bearer or "").encode("utf-8")).hexdigest()[:16] if bearer else ""


def _match(rows: object, ref: str) -> str | None:
    bare = ref[5:] if ref.startswith("slug:") else _bare(ref)
    for row in rows if isinstance(rows, list) else []:
        if isinstance(row, Mapping) and row.get("slug") == bare and row.get("id"):
            return str(row["id"])
    return None


def resolve_id(
    limit: WorkspaceLimit,
    *,
    base_url: str,
    list_workspaces: Callable[[], object],
    account: str = "",
) -> str:
    """The limit's workspace uuid. A uuid is used as is; a slug (environment only) is
    looked up once per process with `list_workspaces`, which the caller makes WITHOUT
    the limit header. Raises rather than returning nothing: fail closed."""
    ident = limit.id
    if ident is not None:
        return ident
    ref = (limit.ref or "").strip()
    if not ref:
        raise errors.WorkspaceLimitUnknown(
            f"this computer's workspace limit names no workspace. Run `{COMMAND} <workspace>` "
            f"or `{TEAM_COMMAND}`.",
            status=None,
            detail={"code": errors.WORKSPACE_LIMIT_UNKNOWN},
        )
    key = (str(base_url or "").rstrip("/"), account, ref)
    with _RESOLVED_LOCK:
        hit = _RESOLVED.get(key)
    if hit is not None:
        return hit
    found = _match(list_workspaces(), ref)
    if found is None:
        what = f"{LIMIT_ENV}={ref!r}" if limit.source is Source.ENV else f"this computer's workspace limit {ref!r}"
        raise errors.WorkspaceLimitUnknown(
            f"{what} is not a workspace on this team (see `probe workspace list`). Set it to a "
            f"workspace id or slug, or `{LIMIT_ENV}=team` for the whole team.",
            status=None,
            detail={"code": errors.WORKSPACE_LIMIT_UNKNOWN},
        )
    with _RESOLVED_LOCK:
        _RESOLVED[key] = found
    return found


def request_headers(limit: WorkspaceLimit | None, workspace_id: str | None) -> dict[str, str]:
    """The two request headers for a limit already resolved to `workspace_id`."""
    if limit is None or not workspace_id:
        return {}
    return {LIMIT_HEADER: workspace_id, TEAM_ITEMS_HEADER: limit.checked_team_items()}


def fail_closed_headers(limit: WorkspaceLimit | None) -> dict[str, str]:
    """The headers for a limit this process could not turn into a uuid (a slug it
    could not look up): the value as found when it is header-safe, else
    `UNREADABLE_FORWARD`. The API refuses either (400 `invalid_workspace_limit`), so
    a surface that must emit SOMETHING (an MCP headers helper) fails closed."""
    if limit is None:
        return {}
    ref = (limit.ref or "").strip()
    value = ref if _FORWARD_RE.fullmatch(ref) else UNREADABLE_FORWARD
    items = str(limit.team_items or TeamItems.SHOW.value).strip().lower()
    if items not in (TeamItems.SHOW.value, TeamItems.HIDE.value):
        items = UNREADABLE_FORWARD
    return {LIMIT_HEADER: value, TEAM_ITEMS_HEADER: items}


def stored_headers(context: Mapping | None = None) -> dict[str, str]:
    """The headers a STATIC copy carries -- Codex's config.toml, Kimi Code's manifest,
    which outlive any one process -- from the context FILE's limit only, never
    `PROBE_WORKSPACE_LIMIT` (one process's). {} for the whole team. Re-rendered on
    every limit change, as a token rotation re-renders the bearer."""
    if context is None:
        from .config import load_context

        context = load_context()
    return offline_headers(stored(context))


def offline_headers(limit: WorkspaceLimit | None) -> dict[str, str]:
    """A limit's headers with no network: its uuid when it names one, else the
    fail-closed form (an environment slug no one looked up). {} for none."""
    if limit is None:
        return {}
    if limit.id is None:
        return fail_closed_headers(limit)
    try:
        return request_headers(limit, limit.id)
    except errors.InvalidWorkspaceLimit:
        return fail_closed_headers(limit)


def limit_headers_of(headers: Mapping | None) -> dict[str, str]:
    """Just the limit headers of a header map (case-insensitive keys)."""
    wanted = {LIMIT_HEADER.lower(): LIMIT_HEADER, TEAM_ITEMS_HEADER.lower(): TEAM_ITEMS_HEADER}
    return {
        wanted[str(key).lower()]: str(value)
        for key, value in (headers or {}).items()
        if str(key).lower() in wanted
    }


def list_workspaces_unlimited(base_url: str, bearer: str, *, timeout: float = 10.0) -> object:
    """`GET /v1/workspaces` with a bare bearer and NO limit header, for code that has
    no `Transport` (the daemon, the service, `probe mcp headers`)."""
    import httpx

    from .tls import ssl_context

    try:
        with httpx.Client(base_url=base_url.rstrip("/"), timeout=timeout, verify=ssl_context()) as http:
            resp = http.get("/v1/workspaces", headers={"Authorization": f"Bearer {bearer}"})
    except httpx.HTTPError as exc:
        # A RosError like every other failure here, so the fail-closed callers
        # (`headers_or_fail_closed`) catch it instead of crashing offline.
        raise errors.TransportError(f"could not list workspaces to resolve the workspace limit: {exc}") from exc
    if resp.status_code >= 400:
        try:
            detail = resp.json().get("detail")
        except (ValueError, AttributeError):
            detail = resp.text
        raise errors.error_for(resp.status_code, detail)
    return resp.json()


def headers_for(
    settings,
    *,
    bearer: str | None = None,
    base_url: str | None = None,
) -> dict[str, str]:
    """This process's limit headers for `settings` (a resolved `Settings`), or {}.

    `base_url`: only when it is the deployment `settings` resolves to -- a limit is
    one team's workspace and means nothing to another deployment. `bearer` lists the
    workspaces for an environment slug (default: the settings' token, else the MCP
    token)."""
    limit = getattr(settings, "workspace_limit", None)
    if limit is None:
        return {}
    own = str(getattr(settings, "base_url", "") or "").rstrip("/")
    if base_url is not None and str(base_url).rstrip("/") != own:
        return {}
    key = bearer or getattr(settings, "token", None) or getattr(settings, "mcp_token", None) or ""
    ident = resolve_id(
        limit, base_url=own, list_workspaces=lambda: list_workspaces_unlimited(own, key), account=account_key(key)
    )
    return request_headers(limit, ident)


def headers_or_fail_closed(settings, *, bearer: str | None = None, base_url: str | None = None) -> dict[str, str]:
    """`headers_for`, for a surface that must send SOMETHING rather than raise (an
    MCP connection, a background poll): a limit it cannot name goes as
    `fail_closed_headers`, which the API refuses. Never {} while limited."""
    try:
        return headers_for(settings, bearer=bearer, base_url=base_url)
    except errors.RosError:
        return fail_closed_headers(getattr(settings, "workspace_limit", None))


def ambient_headers(base_url: str | None = None, *, bearer: str | None = None) -> dict[str, str]:
    """The current context's limit headers (`resolve()`), for a request to
    `base_url` (None: the context's own deployment; another deployment gets none).
    Fails closed (`headers_or_fail_closed`)."""
    from .config import resolve

    return headers_or_fail_closed(resolve(), bearer=bearer, base_url=base_url)


# -- per-request scopes ---------------------------------------------------------

#: The hosted MCP's per-request headers: the CALLER's limit, which it forwards on the
#: API calls it makes for them. Unset (None) means "use this process's own"; an EMPTY
#: mapping is a real answer -- the caller sent none -- and must never fall back to ours
#: (the same rule as `client_headers._outbound_client_headers`).
_forwarded: contextvars.ContextVar[dict[str, str] | None] = contextvars.ContextVar(
    "probe_workspace_limit_forwarded", default=None
)
#: True inside `without_limit()`: the one call that must see every workspace (a picker).
_suppressed: contextvars.ContextVar[bool] = contextvars.ContextVar("probe_workspace_limit_suppressed", default=False)


def forwarded() -> dict[str, str] | None:
    return _forwarded.get()


def suppressed() -> bool:
    return _suppressed.get()


@contextmanager
def forwarded_scope(headers: Mapping[str, str] | None) -> Iterator[None]:
    """Bind the caller's limit headers for the block (the hosted MCP, per request)."""
    token = _forwarded.set(None if headers is None else dict(headers))
    try:
        yield
    finally:
        _forwarded.reset(token)


@contextmanager
def without_limit() -> Iterator[None]:
    """Requests in the block carry no limit: the workspace list a picker shows (the
    desktop app's `workspaces`, `probe workspace limit` resolving its argument), and an
    environment slug's own lookup."""
    token = _suppressed.set(True)
    try:
        yield
    finally:
        _suppressed.reset(token)


def _decoded(value: object) -> str | None:
    if isinstance(value, bytes):
        try:
            value = value.decode("ascii")
        except UnicodeDecodeError:
            return None
    return value if isinstance(value, str) else None


def forward_from(headers: Mapping) -> dict[str, str]:
    """The limit headers of an incoming request (an ASGI header mapping, bytes or str
    keys), to forward as they came: the API validates them. A value that is not
    header-safe is forwarded as `UNREADABLE_FORWARD` (refused upstream), never dropped."""
    wanted = {LIMIT_HEADER.lower(): LIMIT_HEADER, TEAM_ITEMS_HEADER.lower(): TEAM_ITEMS_HEADER}
    out: dict[str, str] = {}
    for raw_key, raw_value in headers.items():
        key = _decoded(raw_key)
        if key is None or key.lower() not in wanted:
            continue
        value = _decoded(raw_value)
        value = value.strip() if value is not None else None
        if value is None or len(value) > _FORWARD_MAX or not _FORWARD_RE.fullmatch(value):
            value = UNREADABLE_FORWARD
        out[wanted[key.lower()]] = value
    if TEAM_ITEMS_HEADER in out and LIMIT_HEADER not in out:
        # Team items without a limit narrow nothing: pass nothing.
        out.pop(TEAM_ITEMS_HEADER)
    return out


# -- what a person reads ----------------------------------------------------------


def hidden_hint(applied: str, limit: WorkspaceLimit | None = None) -> str:
    """`(hidden by this computer's workspace limit: <W>)`, for a 404 the API answered
    under a limit (its `X-Probe-Workspace-Limit-Applied` echo)."""
    name = limit.label if limit is not None and limit.id is not None and limit.id == as_uuid(applied) else None
    return f"(hidden by this computer's workspace limit: {name or f'workspace {applied}'})"


def maybe_hidden_hint(limit: WorkspaceLimit | None) -> str:
    """For a slug lookup that found nothing while limited: it may be in another workspace."""
    if limit is None:
        return ""
    return (
        f"(this computer's workspace limit is {limit.label}: it may be in another workspace; "
        f"`{TEAM_COMMAND}` lifts the limit)"
    )


def with_hint(message: str, hint: str) -> str:
    if not hint or hint in message:
        return message
    return f"{message.rstrip()} {hint}"


def annotate_not_found(exc: BaseException, hint: str) -> BaseException:
    """Append `hint` to a RosError's message in place (its `str()`), once."""
    if not hint or not exc.args or not isinstance(exc.args[0], str):
        return exc
    exc.args = (with_hint(exc.args[0], hint), *exc.args[1:])
    return exc
