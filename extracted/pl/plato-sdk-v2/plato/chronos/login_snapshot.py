"""Resolve the latest good login snapshot for a ``(login_key, account)`` pair.

A mirror of the exploration world's ``exploration_world/login_snapshot.py`` (the
canonical copy, #2330) for callers outside the worlds: ``plato vault open`` seeds
a login world with the ref this returns. The two cannot import each other -- a
world installs its pinned SDK from PyPI, so it cannot use a module newer than that
pin, and the SDK cannot depend on a world -- so everything below this docstring is
kept identical to the canonical file by
``tests/unit/chronos/test_login_snapshot_parity.py``. Change both together.

The contract (login world ADR 0001/0002, amended 2026-09-25): the login world
commits each successful bake to the workspace repo ``login/{login_key}/snapshot``
and tags its session ``login_key:<k>``, ``account:<a>``,
``login_outcome:success``, ``mode:<vm|cdp_browser>``. The resolver reads that
repo's branches (one row per session that touched it, with the session's tags and
newest ref) and picks the newest successful bake of this account in a mode the
caller can restore.
"""

from __future__ import annotations

import logging
import re
from dataclasses import dataclass
from datetime import datetime, timezone

import httpx

from plato.chronos.api.workspace_repos import (
    list_workspace_branches,
    list_workspace_refs,
    list_workspace_repos,
)
from plato.chronos.errors import APIError

_log = logging.getLogger(__name__)
_SLUG_RE = re.compile(r"[^a-z0-9]+")
# The label the login world gives its own snapshot commit (``login-{outcome}``;
# only a successful bake commits the snapshot workspace). The runtime's
# ``step.N`` checkpoint re-commits the same files a second later.
OWN_COMMIT_STEP = "login-success"


def _slug(value: str | None) -> str:
    """Match the login world's ``slugify`` so a key baked under one spelling
    resolves under another (``Google Calendar`` -> ``google_calendar``)."""
    if not value:
        return ""
    return _SLUG_RE.sub("_", value.strip().lower()).strip("_")


def snapshot_repo_name(login_key: str) -> str:
    """The workspace repo the login world commits snapshots to for ``login_key``."""
    return f"login/{_slug(login_key)}/snapshot"


@dataclass
class ResolvedSnapshot:
    """A pointer to a committed login snapshot, enough to restore it."""

    session_id: str
    repo_name: str
    step_name: str
    created_at: datetime | None = None

    @property
    def config_ref(self) -> str:
        """The ``state.workspaces`` ref string a resume config uses:
        ``<session_id>:<step_name>``."""
        return f"{self.session_id}:{self.step_name}"


def _norm_tag(tag) -> str:
    """Chronos stores tags as an ltree: ``key:value`` reads back as ``key.value`` and
    ``-`` as ``_``. Compare in that shape so either spelling matches."""
    return str(tag).strip().lower().replace(":", ".").replace("-", "_")


def _has_tag(tags, wanted: str) -> bool:
    want = _norm_tag(wanted)
    return any(_norm_tag(t) == want for t in (tags or []))


def is_cdp_bake(tags) -> bool:
    """Whether a login session baked a vendor Context (cdp_browser) rather than a
    Chrome tarball. Reads the ``mode:`` tag the login world stamps on itself, and
    falls back to a bare ``cdp_browser`` tag for bakes launched before it did."""
    norm = {_norm_tag(t) for t in (tags or [])}
    return "mode.cdp_browser" in norm or "cdp_browser" in norm


def _filter_by_mode(sessions, cdp_browser: bool | None):
    """Keep only bakes whose artifact this run can restore. The two modes commit
    DIFFERENT artifacts to the same repo — a Context id vs a tarball — so "newest
    successful bake" alone hands a cdp run a tarball it cannot use (or a VM run a
    Context), and it then re-bakes or stops. None = no filtering (legacy callers)."""
    if cdp_browser is None:
        return list(sessions)
    want = bool(cdp_browser)
    return [s for s in sessions if is_cdp_bake(getattr(s, "tags", None)) == want]


def _aware(ts) -> datetime:
    """Sort key for API timestamps: a missing/odd value sorts oldest; a naive one
    is UTC (Chronos omits the offset on some paths)."""
    if not isinstance(ts, datetime):
        return datetime.min.replace(tzinfo=timezone.utc)
    return ts if ts.tzinfo else ts.replace(tzinfo=timezone.utc)


def _pick_snapshot_ref(sessions, repo_name: str) -> ResolvedSnapshot | None:
    """Pure selection over FULL sessions (the ones that embed ``workspace_refs``):
    the newest session (by ``created_at``) that holds an ``output`` ref to
    ``repo_name`` -> its :class:`ResolvedSnapshot`, else None. Used to read the ref
    off a child bake this run just launched (``login_refresh``); the ledger lookup
    below does not need it. Defends against unordered API results by sorting."""

    def _created(session) -> datetime:
        return _aware(getattr(session, "created_at", None))

    for session in sorted(sessions, key=_created, reverse=True):
        for ref in getattr(session, "workspace_refs", None) or []:
            if ref.repo_name == repo_name and (ref.direction or "output") == "output":
                return ResolvedSnapshot(
                    session_id=session.public_id,
                    repo_name=repo_name,
                    step_name=ref.step_name,
                    created_at=getattr(session, "created_at", None),
                )
    return None


def _pick_branch(branches, *, login_key: str, account: str | None, cdp_browser: bool | None):
    """Pure selection (unit-testable) over the rows Chronos returns for the snapshot
    repo's branches: one per session that ever committed to the repo, with that
    session's ``tags``, its newest ref's ``last_step`` and that ref's ``updated_at``.

    Only the tags separate a bake of THIS login from a reader — a failed bake never
    commits the snapshot workspace, but a bake SEEDED from an earlier snapshot and
    an exploration run that restored one both appear here through their *input*
    ref (with the seed's step name). ``login_outcome:success`` drops the readers;
    ``login_key:<this key>`` drops a successful bake of ANOTHER login that was
    seeded from this repo (its row would otherwise win with the seed's old ref).
    Then narrow to the account (any account when None) and to the mode this run
    can restore, and take the newest by ``updated_at``. Sorts explicitly: Chronos
    orders these rows by session id, not by time.
    """
    key_tag = f"login_key:{_slug(login_key)}"
    rows = [
        b
        for b in (branches or [])
        if getattr(b, "session_public_id", None)
        and _has_tag(getattr(b, "tags", None), "login_outcome:success")
        and _has_tag(b.tags, key_tag)
    ]
    if account_slug := _slug(account):
        rows = [b for b in rows if _has_tag(b.tags, f"account:{account_slug}")]
    rows = _filter_by_mode(rows, cdp_browser)
    rows.sort(key=lambda b: _aware(getattr(b, "updated_at", None)), reverse=True)
    return rows[0] if rows else None


async def _snapshot_repo_id(client, repo_name: str) -> str | None:
    """The public id of ``repo_name`` in this org, or None when no bake has ever
    created it. Reads the org's repo list on purpose: the ``resolve`` endpoint
    would CREATE an empty repo for a key that was never baked."""
    resp = await list_workspace_repos.asyncio(client)
    for repo in resp.repos or []:
        if repo.name == repo_name:
            return repo.repo_id
    return None


async def resolve_latest_snapshot(
    chronos,
    login_key: str,
    account: str | None = None,
    *,
    cdp_browser: bool | None = None,
) -> ResolvedSnapshot | None:
    """Return the newest successful login bake for ``(login_key, account)``, or None.

    ``chronos`` is an ``AsyncChronos``. Three read-only calls, no session fetch:
    the org's repo list (name -> id for ``login/{login_key}/snapshot``; None when
    the repo does not exist yet, i.e. nothing was ever baked), that repo's
    branches (then :func:`_pick_branch`), and the winning session's workspace
    refs, so the ref handed out is the bake's own ``login-success`` commit
    (:func:`own_commit_ref`). If that last read fails on the wire, the row's
    ``last_step`` — the runtime's ``step.N`` re-commit of the same files — is
    used instead, with a warning.

    ``cdp_browser`` narrows to bakes of THIS run's mode (see :func:`_filter_by_mode`);
    None keeps every successful bake, which is right only for a caller that can
    restore either artifact. Child bakes (in-world auto_refresh) are plain rows
    here — there is no top-level/child distinction to get wrong.
    """
    repo_name = snapshot_repo_name(login_key)
    repo_id = await _snapshot_repo_id(chronos._client, repo_name)
    if not repo_id:
        return None
    resp = await list_workspace_branches.asyncio(chronos._client, repo_id)
    row = _pick_branch(
        resp.branches or [],
        login_key=login_key,
        account=account,
        cdp_browser=cdp_browser,
    )
    if row is None:
        return None
    own = await _own_commit(chronos._client, row.session_public_id, repo_name)
    return ResolvedSnapshot(
        session_id=row.session_public_id,
        repo_name=repo_name,
        step_name=own.step_name if own else row.last_step,
        created_at=(getattr(own, "created_at", None) or getattr(row, "updated_at", None)),
    )


def own_commit_ref(refs, repo_name: str):
    """The bake's OWN snapshot commit among a session's workspace refs: the
    ``output`` ref to ``repo_name`` labelled :data:`OWN_COMMIT_STEP`, else the
    oldest ``output`` ref there (the world commits before the runtime does),
    else None. Never an ``input`` ref — a seeded bake carries its seed's
    ``login-success`` as an input ref, and that is someone else's snapshot."""
    outputs = [
        r
        for r in (refs or [])
        if getattr(r, "repo_name", None) == repo_name and (getattr(r, "direction", None) or "output") == "output"
    ]
    for r in outputs:
        if r.step_name == OWN_COMMIT_STEP:
            return r
    outputs.sort(key=lambda r: _aware(getattr(r, "created_at", None)))
    return outputs[0] if outputs else None


async def _own_commit(client, session_id: str, repo_name: str):
    """One extra read for the WINNING row only: its session's refs, so the ref we
    hand out is the world's ``login-success`` commit rather than the runtime's
    ``step.N`` re-commit (same files either way).

    Only a transport / Chronos API failure falls back (None -> the caller uses the
    row's ``last_step``, which is a known-good ref to the same files), and it is
    logged as a warning: a flaky read should not start a leg signed out over a
    label. Anything else raises."""
    try:
        resp = await list_workspace_refs.asyncio(client, session_public_id=session_id)
    except (httpx.HTTPError, APIError) as exc:
        _log.warning(
            "login snapshot: could not read refs of %s (%s); using its newest ref",
            session_id[:8],
            exc,
        )
        return None
    return own_commit_ref(resp.refs or [], repo_name)
