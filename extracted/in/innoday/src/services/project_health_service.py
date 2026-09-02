"""One composite answer to "is this project actually working?".

Before this, that question took four calls and the caller assembled the verdict:
``GET /health`` for the database (globally, not per project), ``GET
.../boards`` for what is registered, ``GET .../boards/{id}/sync-history`` for
whether the last sync worked, and a **dry-run sync** -- asynchronous, ~50s, with
a poll loop -- for whether the board is reachable at all. Three of those four
read only InnoDay's own database, so the composite they produced could say
"healthy" about a board whose credential had expired months earlier.

The live half reuses ``BaseBoardAdapter.validate_connection()``, which already
exists on every adapter and is already exercised on every sync (each adapter's
``initialize()`` calls it). Nothing new had to be written per board type, and
nothing here duplicates the credential chain: ``resolve_board_token`` +
``build_board_adapter`` are the same two calls sync and ticket-creation make.
"""

import asyncio
import logging
import time
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional, Tuple

from sqlalchemy import text
from sqlmodel import Session, select

from src.adapters import BaseBoardAdapter, BoardCredentialError
from src.domain import BoardRegistration, BoardSyncHistory
from src.domain.organization import Organization
from src.domain.repository import GitHubSyncHistory
from src.services.board_adapter_factory import build_board_adapter, resolve_board_token
from src.utils.time_windows import as_utc

logger = logging.getLogger(__name__)

#: Per-board deadline for the live check. Probing on by default means one hung
#: board must not hold the whole report open.
_PROBE_TIMEOUT_SECONDS = 10.0

#: Deadline for resolving a credential and building an adapter. This phase looks
#: local but is not: an OAuth Jira board mints a fresh access token over the
#: network inside ``build_board_adapter``, so it needs its own bound.
_ADAPTER_BUILD_TIMEOUT_SECONDS = 10.0

#: Ceiling on the whole probe phase, per-board deadlines notwithstanding. The
#: serial credential phase is additive, so N boards could otherwise sum to
#: N x _ADAPTER_BUILD_TIMEOUT_SECONDS before a single network check began.
_TOTAL_PROBE_BUDGET_SECONDS = 25.0

#: Cap on simultaneous board connections. A project with a dozen boards should
#: not open a dozen sockets at once on a request that is meant to be cheap.
_MAX_CONCURRENT_PROBES = 4


def _database_connected(session: Session) -> Tuple[bool, Optional[int]]:
    """A real round trip, and how long it took.

    Deliberately not `True` with a comment saying we must be connected because
    the handler is running -- that is what `/platform/health` used to do, and a
    check that cannot fail reads exactly like one that passed.

    The timing costs nothing (the query was already being run) and it is what
    makes the database a row like any other rather than one with a blank where
    every other dependency has a number.
    """
    started = time.monotonic()
    try:
        session.exec(text("SELECT 1"))
        return True, int((time.monotonic() - started) * 1000)
    except Exception:
        logger.warning("project health: database check failed", exc_info=True)
        return False, None


def _last_repo_sync(session: Session, project_id: str) -> Optional[datetime]:
    """When this project's repositories were last discovered from GitHub.

    `GitHubSyncHistory` is the only honest source. `Repository.last_synced_at`
    and the registration's `last_sync_at` sit right beside it and are never
    written -- the model's own comment records a reader that trusted them and
    reported "connected, never synced" for every organisation.

    Completed rows only. The table is terminal-state by design, so a `failed`
    row is a real attempt that wrote nothing, and counting it as freshness is
    the same mistake as counting a board's `--dry-run`.
    """
    row = session.exec(
        select(GitHubSyncHistory)
        .where(
            GitHubSyncHistory.project_id == project_id,
            GitHubSyncHistory.status == "completed",
        )
        .order_by(GitHubSyncHistory.started_at.desc())  # type: ignore[union-attr]
        .limit(1)
    ).first()
    return as_utc(row.started_at) if row else None


def _last_real_sync(session: Session, board_id: str) -> Optional[BoardSyncHistory]:
    """The last sync that actually wrote something.

    ``dry_run`` rows are excluded, for the reason the model's own comment gives:
    a preview records a row indistinguishable from a real sync, and reading one
    as evidence of freshness is a bug this codebase has already had. A board
    whose only recent run was a `--dry-run` is **not** fresh.
    """
    return session.exec(
        select(BoardSyncHistory)
        .where(
            BoardSyncHistory.board_registration_id == board_id,
            BoardSyncHistory.dry_run.is_(False),  # type: ignore[union-attr]
        )
        .order_by(BoardSyncHistory.started_at.desc())  # type: ignore[union-attr]
        .limit(1)
    ).first()


async def _build_probe(
    session: Session, registration: BoardRegistration, org: Optional[Organization]
) -> Tuple[Optional[BaseBoardAdapter], Optional[Dict[str, Any]]]:
    """Resolve the credential and build the adapter. **Serial, on purpose.**

    Everything here touches ``session`` -- ``resolve_board_token`` reads Vault
    through it, and an OAuth Jira board mints a fresh token through it inside
    ``build_board_adapter``. A SQLModel ``Session`` cannot be shared across
    concurrent coroutines: gather these and one board can be suspended
    mid-transaction while another issues a query on the same session. So this
    phase runs one board at a time, and only the network call in
    ``_validate`` -- which touches no session -- is parallelised.

    Returns ``(adapter, None)`` or ``(None, report)`` where ``report`` already
    carries a three-valued verdict.
    """
    try:
        token = resolve_board_token(session, registration, org)
    except BoardCredentialError as e:
        return None, {
            "reachable": None,
            "latency_ms": None,
            "detail": f"no credential stored: {e}",
        }
    except Exception as e:  # noqa: BLE001 - a broken credential must not 500 the report
        return None, {
            "reachable": None,
            "latency_ms": None,
            "detail": f"credential could not be read: {e}",
        }

    try:
        adapter = await asyncio.wait_for(
            build_board_adapter(registration, token, session),
            timeout=_ADAPTER_BUILD_TIMEOUT_SECONDS,
        )
    except asyncio.TimeoutError:
        return None, {
            "reachable": None,
            "latency_ms": None,
            "detail": (
                f"credential/adapter setup exceeded "
                f"{_ADAPTER_BUILD_TIMEOUT_SECONDS:.0f}s"
            ),
        }
    except Exception as e:  # noqa: BLE001
        # We never got as far as asking the board, so nothing was proved.
        return None, {
            "reachable": None,
            "latency_ms": None,
            "detail": f"adapter could not be built: {e}",
        }

    return adapter, None


async def _validate(adapter: BaseBoardAdapter) -> Dict[str, Any]:
    """Ask the board, under a deadline, and time it.

    The deadline exists because probing is unconditional. One board behind a
    hung proxy would otherwise hold the whole report open for as long as its
    HTTP client allowed, turning a health check into the outage it is meant to
    describe.

    **A timeout is `False`, not `None`.** The distinction this file keeps is
    "we asked and got nothing" versus "we could not ask": no credential means
    nothing was proved, but a board that will not answer inside the budget is
    not reachable, and saying so is the useful answer.
    """
    started = time.monotonic()
    try:
        ok = await asyncio.wait_for(
            adapter.validate_connection(), timeout=_PROBE_TIMEOUT_SECONDS
        )
    except asyncio.TimeoutError:
        return {
            "reachable": False,
            "latency_ms": int((time.monotonic() - started) * 1000),
            "detail": f"no answer within {_PROBE_TIMEOUT_SECONDS:.0f}s",
        }
    except Exception as e:  # noqa: BLE001
        # A refused credential is a verdict, not an outage of this endpoint.
        return {
            "reachable": False,
            "latency_ms": int((time.monotonic() - started) * 1000),
            "detail": str(e),
        }

    return {
        "reachable": bool(ok),
        "latency_ms": int((time.monotonic() - started) * 1000),
        "detail": "ok" if ok else "board rejected the connection",
    }


async def _probe_github(
    session: Session, organization: Optional[Organization]
) -> Dict[str, Any]:
    """Is the organization's GitHub credential still good?

    GitHub is the one integration that already had a real live validator --
    ``validate_stored_github_credential``, added because an expired token was
    invisible everywhere else in the system: onboarding/resolve answered 500 and
    repository discovery answered ``[]``, and neither said "the token expired".
    Leaving it out of a project health check meant this endpoint reproduced that
    exact blind spot for the half of a project that is repos rather than boards.

    **Org-scoped, not project-scoped.** ``org_credentials`` holds one GitHub
    credential per organization, so this answers for every project in the org.
    The key is named ``github`` and the payload says ``"scope": "organization"``
    so nobody reads it as being about this project alone.

    **``github_login`` is deliberately dropped.** The sibling
    ``/integrations/{service}/validate`` route is ADMIN-only specifically because
    its response names the account the org's token belongs to; this route is
    DEVELOPER, so it reports the verdict and not the identity.

    **This writes.** On success the validator stamps ``last_validated_at``. A GET
    with an audit side effect is worth knowing about, and it is the right
    semantics -- "when did we last confirm this" is exactly what a health check
    establishes -- but it is a write on a read route.
    """
    if organization is None:
        return {"scope": "organization", "reachable": None, "detail": "no organization"}

    from src.services.github_connect_service import GitHubConnectService
    from src.services.org_credential_service import VaultUnavailableError

    started = time.monotonic()
    try:
        result = await asyncio.wait_for(
            GitHubConnectService(session).validate_stored_github_credential(
                organization.id
            ),
            timeout=_PROBE_TIMEOUT_SECONDS,
        )
    except asyncio.TimeoutError:
        return {
            "scope": "organization",
            "reachable": False,
            "latency_ms": int((time.monotonic() - started) * 1000),
            "detail": f"no answer within {_PROBE_TIMEOUT_SECONDS:.0f}s",
        }
    except VaultUnavailableError as e:
        # The store could not be read, so nothing was proved about the token.
        return {"scope": "organization", "reachable": None, "detail": f"vault: {e}"}
    except ValueError as e:
        # No credential stored, or no such org -- not a failed validation.
        return {
            "scope": "organization",
            "reachable": None,
            "detail": f"nothing to check: {e}",
        }
    except Exception as e:  # noqa: BLE001 - must not fail the report
        logger.warning("project health: github check failed", exc_info=True)
        return {"scope": "organization", "reachable": None, "detail": f"error: {e}"}

    # `valid` is itself three-valued: null means GitHub did not answer.
    valid = result.get("valid")
    return {
        "scope": "organization",
        "reachable": valid,
        "latency_ms": int((time.monotonic() - started) * 1000),
        "github_org": result.get("github_org"),
        "org_access": result.get("org_access"),
        "last_validated_at": result.get("last_validated_at"),
        "detail": result.get("error") or ("ok" if valid else "credential rejected"),
    }


async def _probe_all(
    session: Session,
    boards: List[BoardRegistration],
    organization: Optional[Organization],
    board_reports: List[Dict[str, Any]],
) -> None:
    """Probe every active board, in place, within a total budget.

    **This function does not raise.** The database verdict and the sync ages are
    useful on their own, and they are the half that cannot fail; letting a
    misbehaving third party turn the whole report into a 500 would make this
    endpoint less reliable than the four calls it replaced. Anything unexpected
    is recorded against the board it came from and the report still returns.

    Boards left unprobed when the budget runs out keep ``reachable: None`` with a
    detail saying so -- not ``False``, which would accuse a board nobody asked.
    """
    deadline = time.monotonic() + _TOTAL_PROBE_BUDGET_SECONDS

    def _remaining() -> float:
        return deadline - time.monotonic()

    # Phase 1, serial: everything that touches the session (see _build_probe).
    pending: List[Tuple[int, BaseBoardAdapter]] = []
    for index, registration in enumerate(boards):
        if not registration.is_active:
            continue
        if _remaining() <= 0:
            board_reports[index].update(
                {
                    "reachable": None,
                    "latency_ms": None,
                    "detail": (
                        f"not probed: {_TOTAL_PROBE_BUDGET_SECONDS:.0f}s budget "
                        f"spent on earlier boards"
                    ),
                }
            )
            continue
        try:
            adapter, failure = await _build_probe(session, registration, organization)
        except Exception as e:  # noqa: BLE001 - see docstring
            logger.warning(
                "project health: adapter setup failed for board %s",
                registration.id,
                exc_info=True,
            )
            board_reports[index].update(
                {"reachable": None, "latency_ms": None, "detail": f"setup error: {e}"}
            )
            continue
        if failure is not None:
            board_reports[index].update(failure)
        elif adapter is not None:
            pending.append((index, adapter))

    if not pending:
        return

    # Phase 2, concurrent: network only, so the report costs the slowest board
    # rather than the sum of all of them. Bounded, so a board-heavy project does
    # not fan out without limit.
    semaphore = asyncio.Semaphore(_MAX_CONCURRENT_PROBES)

    async def _guarded(adapter: BaseBoardAdapter) -> Dict[str, Any]:
        async with semaphore:
            return await _validate(adapter)

    try:
        results = await asyncio.wait_for(
            asyncio.gather(
                *(_guarded(adapter) for _, adapter in pending),
                return_exceptions=True,
            ),
            timeout=max(_remaining(), 0.1),
        )
    except asyncio.TimeoutError:
        for index, _ in pending:
            if board_reports[index]["reachable"] is None:
                board_reports[index].update(
                    {
                        "latency_ms": None,
                        "detail": (
                            f"not probed: {_TOTAL_PROBE_BUDGET_SECONDS:.0f}s "
                            f"total budget exhausted"
                        ),
                    }
                )
        return
    except Exception as e:  # noqa: BLE001 - see docstring
        logger.warning("project health: probe phase failed: %s", e, exc_info=True)
        return

    for (index, _), result in zip(pending, results):
        if isinstance(result, BaseException):
            board_reports[index].update(
                {
                    "reachable": False,
                    "latency_ms": None,
                    "detail": f"probe failed: {result}",
                }
            )
        else:
            board_reports[index].update(result)


async def get_project_health(
    session: Session,
    organization: Optional[Organization],
    project_id: str,
    probe: bool = True,
) -> Dict[str, Any]:
    """Assemble the report, contacting every active board.

    **``probe`` defaults on, and that is the whole point.** It shipped defaulting
    *off*, which meant the default answer to "is this project working?" was
    assembled entirely from InnoDay's own database -- the exact shape of
    non-answer this endpoint was written to replace, and one under which a board
    whose credential expired months ago reads as healthy. If a board is active
    and has a credential, it gets asked.

    ``probe=False`` remains available for the cases where the outbound calls are
    genuinely unwanted: a tight loop, a caller that only needs sync ages, or a
    board known to be hanging. It is an escape hatch, not the default posture.
    """
    database_connected, database_latency_ms = _database_connected(session)

    boards = session.exec(
        select(BoardRegistration).where(
            BoardRegistration.project_id == project_id,
            BoardRegistration.organization_id
            == (organization.id if organization else None),
            # A soft-deleted registration is gone as far as anyone is concerned.
            # Omitting this filter made the report resurrect boards that had been
            # deleted months earlier: BPAI's Jira `ITPT Board` was deleted on
            # 2026-08-08 and still appeared here, which `board list` -- which does
            # filter -- correctly hid. It read as an un-cleaned-up registration
            # somebody needed to act on, when the cleanup had already happened.
            BoardRegistration.deleted_at.is_(None),  # type: ignore[union-attr]
        )
    ).all()

    now = datetime.now(timezone.utc)
    board_reports: List[Dict[str, Any]] = []

    for registration in boards:
        last = _last_real_sync(session, registration.id)
        started = as_utc(last.started_at) if last else None

        board_reports.append(
            {
                "id": registration.id,
                "name": registration.board_name,
                "board_type": (
                    registration.board_type.value
                    if hasattr(registration.board_type, "value")
                    else str(registration.board_type)
                ),
                "is_active": bool(registration.is_active),
                "last_sync_at": started.isoformat() if started else None,
                # Reported as a number, never as a verdict. "Stale" is a policy
                # the caller owns -- a board synced hourly and one synced weekly
                # are both correct, and an endpoint cannot know which this is.
                "last_sync_age_seconds": (
                    int((now - started).total_seconds()) if started else None
                ),
                "last_sync_status": (
                    last.sync_status.value
                    if last and hasattr(last.sync_status, "value")
                    else (str(last.sync_status) if last else None)
                ),
                "reachable": None,
                "latency_ms": None,
                "detail": (
                    "not probed: registration is inactive"
                    if not registration.is_active
                    else ("not probed" if not probe else "probing")
                ),
            }
        )

    github: Dict[str, Any] = {
        "scope": "organization",
        "reachable": None,
        "detail": "not probed",
    }

    if probe:
        await _probe_all(session, boards, organization, board_reports)
        github = await _probe_github(session, organization)

    if not database_connected:
        status = "unhealthy"
    elif any(b["reachable"] is False for b in board_reports):
        status = "degraded"
    elif github.get("reachable") is False:
        # An expired GitHub token degrades the project for the same reason a
        # refused board does: half its work -- repos, issues, releases -- stops
        # resolving, silently and without an error that names the cause.
        status = "degraded"
    else:
        # An inactive registration is a **state, not a fault**, and must not
        # degrade the project. Deactivating a board is how you retire one --
        # BPAI still carries its old Jira `ITPT Board` from before it moved to
        # Linear -- and `board delete` is a soft delete, so the row stays
        # forever. Degrading on it made BPAI permanently yellow with no action
        # available to make it green, which is the shape of alarm every operator
        # learns to ignore. It is reported in `is_active` for anyone who wants
        # to act on it; it is not a problem with the project.
        status = "healthy"

    # **The GitHub row is a dependency like any other, so it carries the same
    # two numbers.** `latency_ms` was already measured by the probe and simply
    # never surfaced; the sync age had no source until now, so the row rendered
    # two dashes that read as "not applicable" when they meant "not looked up".
    repo_sync = _last_repo_sync(session, project_id)
    github = dict(github)
    github["last_sync_at"] = repo_sync.isoformat() if repo_sync else None
    github["last_sync_age_seconds"] = (
        int((now - repo_sync).total_seconds()) if repo_sync else None
    )

    return {
        "status": status,
        "database": "connected" if database_connected else "disconnected",
        "database_latency_ms": database_latency_ms,
        "project_id": project_id,
        "boards": board_reports,
        "github": github,
    }
