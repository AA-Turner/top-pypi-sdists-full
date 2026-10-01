"""Keep a project's releases and its board's releases in step, both ways.

The rules live here once; each board adapter only translates (see the release
methods on `BaseBoardAdapter`). The rules:

1. Releases pair by the board's own id once known, else by version string --
   the same key `Ticket.release` carries.
2. **InnoDay owns the release setup.** A *managed* release is one InnoDay holds
   for the project (planned, in progress or released). An open one is created
   on the board if missing -- including when the board deleted it -- and the
   board's name and stage are put back to InnoDay's on every sync. A release
   InnoDay explicitly withdraws is moved to the board's canceled stage.
3. Anything else the board holds is an *extra* release: never created, changed
   or deleted here, and it never changes a ticket's InnoDay release.
4. **Ticket membership in managed releases syncs both ways**, by three-way
   merge against the snapshot taken at the last sync (`board_ticket_keys`):
   - added or moved on the board since the snapshot → InnoDay follows;
   - removed on the board since the snapshot → InnoDay's release is cleared;
   - otherwise InnoDay's placement is pushed to the board (attach/detach).
   A release with no snapshot has never been synced: nothing is assumed
   removed, the board's membership wins any disagreement, and InnoDay-only
   placements are attached on the board (the union).
   A ticket sits in one release: InnoDay's single `Ticket.release`, so a board
   that lists it in two is brought down to one.
   **Shipped releases are history.** A RELEASED release is paired and staged,
   but never created on the board after the fact, and its tickets no longer
   move -- Linear rolls open issues forward on completion and archives old
   ones, and neither is InnoDay un-shipping them.
5. A board with no release line (a board type without releases, a Linear plan
   without Releases, no or several pipelines) is not an error: releases are
   managed in InnoDay only. A single failed board write is reported, never
   fatal; the snapshot records what the board really holds, so the next sync
   retries it.
"""

import logging
from typing import Any, Dict, List, Optional, Set

from sqlmodel import Session, col, select

from src.adapters.base_adapter import (
    BaseBoardAdapter,
    BoardCapabilityError,
    BoardRelease,
)
from src.domain.board import BoardRegistration, BoardType
from src.domain.organization import Organization
from src.domain.release import Release, ReleaseStatus
from src.domain.ticket import Ticket

logger = logging.getLogger(__name__)

MANAGED_STATUSES = (
    ReleaseStatus.PLANNED,
    ReleaseStatus.IN_PROGRESS,
    ReleaseStatus.RELEASED,
)

#: InnoDay status -> board-neutral stage.
STAGE_FOR = {
    ReleaseStatus.PLANNED: "planned",
    ReleaseStatus.IN_PROGRESS: "started",
    ReleaseStatus.RELEASED: "completed",
}
CANCELED = "canceled"

INNODAY_ONLY = "releases managed in InnoDay only"


#: Statuses whose ticket membership still moves. A shipped release is history:
#: its tickets stay as they shipped, whatever the board does afterwards (Linear
#: rolls open issues forward on completion, and archives old issues).
OPEN_STATUSES = (ReleaseStatus.PLANNED, ReleaseStatus.IN_PROGRESS)


def _is_managed(release: Release) -> bool:
    return release.deleted_at is None and release.status in MANAGED_STATUSES


def _version_key(version: str) -> str:
    v = version.strip()
    return v[1:] if len(v) > 1 and v[0] in "vV" and v[1].isdigit() else v


def _same_version(a: str, b: str) -> bool:
    """`v1.5.0` and `1.5.0` are one version -- teams name releases either way.

    Only a `v` before a digit is dropped, so `vNext` and `Venus` stay distinct.
    """
    return _version_key(a) == _version_key(b)


def managed_versions(session: Session, project_id: str) -> List[str]:
    """The versions InnoDay holds for this project, i.e. the managed releases."""
    rows = session.exec(
        select(Release.version).where(
            Release.project_id == project_id,
            Release.deleted_at.is_(None),  # type: ignore[union-attr]
            col(Release.status).in_(MANAGED_STATUSES),
        )
    ).all()
    return list(rows)


class _Run:
    """Counters and warnings for one reconcile, returned as the sync result."""

    def __init__(self) -> None:
        self.counts = {
            "releases_created": 0,
            "releases_updated": 0,
            "releases_canceled": 0,
            "tickets_attached": 0,
            "tickets_cleared": 0,
            "board_attached": 0,
            "board_detached": 0,
        }
        self.errors: List[str] = []

    async def attempt(self, what: str, call) -> bool:
        try:
            await call
            return True
        except Exception as e:  # noqa: BLE001 -- reported, retried next sync
            logger.warning("Release sync: %s failed: %s", what, e)
            self.errors.append(f"{what}: {e}")
            return False


async def reconcile_from_board(
    session: Session,
    registration: BoardRegistration,
    adapter: BaseBoardAdapter,
    project_id: str,
    innoday_wins: Optional[Set[str]] = None,
) -> Dict[str, Any]:
    """Bring the board's release line and InnoDay's into agreement.

    `innoday_wins` names board ticket keys whose InnoDay release was *just*
    written by a person: for those, InnoDay's answer is pushed even if the
    board also changed since the last sync -- the newer intent wins.

    Changes are added to `session`; committing is the caller's. Never raises for
    a board with no release line.
    """
    innoday_wins = innoday_wins or set()
    try:
        board_releases = await adapter.list_releases()
    except BoardCapabilityError as e:
        logger.info("Release sync off for board %s: %s", registration.id, e)
        return {"status": "innoday_only", "message": INNODAY_ONLY, "reason": str(e)}

    run = _Run()
    releases = session.exec(
        select(Release).where(Release.project_id == project_id)
    ).all()

    # 1. Pair InnoDay releases with board releases: board id first, then version.
    by_id = {r.external_id: r for r in board_releases}
    unpaired = {r.external_id: r for r in board_releases}
    paired: Dict[str, BoardRelease] = {}  # keyed by our Release.id
    # Two passes, so a version match can never take a board release that
    # another InnoDay release already owns by id.
    for release in releases:
        board = by_id.get(release.board_release_id or "")
        if board is not None and board.external_id in unpaired:
            paired[release.id] = unpaired.pop(board.external_id)
    for release in releases:
        if release.id in paired or not _is_managed(release):
            continue
        board = next(
            (b for b in unpaired.values() if _same_version(b.version, release.version)),
            None,
        )
        if board is not None:
            paired[release.id] = unpaired.pop(board.external_id)

    managed = [r for r in releases if _is_managed(r)]

    # 2. Release setup: InnoDay's is the answer.
    for release in managed:
        want = STAGE_FOR[release.status]
        board = paired.get(release.id)
        if board is None:
            if release.status not in OPEN_STATUSES:
                # Shipped before the board was paired: history is not
                # exported, so connecting a board does not spray old versions.
                continue
            if release.board_release_id:
                logger.info(
                    "Board release for %s is gone; recreating it", release.version
                )
            try:
                board = await adapter.create_release(release.version, want)
            except Exception as e:  # noqa: BLE001 -- reported, retried next sync
                run.errors.append(f"create {release.version}: {e}")
                continue
            paired[release.id] = board
            release.board_release_id = board.external_id
            # A new board release holds nothing, so nothing was removed there.
            release.board_ticket_keys = None
            session.add(release)
            run.counts["releases_created"] += 1
            continue

        if release.board_release_id != board.external_id:
            release.board_release_id = board.external_id
            session.add(release)
        if board.archived:
            continue  # archived on the board: the same release, left as it is
        if release.status not in OPEN_STATUSES and release.board_ticket_keys is None:
            # Shipped before InnoDay ever synced it open: history is paired,
            # not rewritten -- completing an old Linear release would also
            # trigger Linear's rollover of its open issues.
            continue
        changes: Dict[str, Any] = {}
        if not _same_version(board.version, release.version):
            changes["version"] = release.version
        if board.stage and board.stage != want:
            changes["stage"] = want
        if changes and await run.attempt(
            f"update {release.version}",
            adapter.update_release(board.external_id, **changes),
        ):
            run.counts["releases_updated"] += 1

    for release in releases:
        board = paired.get(release.id)
        # Only an explicit withdrawal cancels on the board. InnoDay's own
        # housekeeping archives releases (a third open version, a non-semver
        # name) and that is not a statement about the board; and a release
        # that completed stays completed.
        if (
            board is None
            or release.deleted_at is None
            or board.archived
            or board.stage in (CANCELED, "completed")
        ):
            continue
        if await run.attempt(
            f"cancel {release.version}",
            adapter.update_release(board.external_id, stage=CANCELED),
        ):
            run.counts["releases_canceled"] += 1

    # 3. Ticket membership, three-way against each release's snapshot. Only
    #    open releases take part; a ticket in a shipped one is left alone.
    live = [
        r
        for r in managed
        if r.id in paired and r.status in OPEN_STATUSES and not paired[r.id].archived
    ]
    versions = {r.version for r in live}
    frozen = {r.version for r in managed} - versions
    board_keys: Dict[str, Set[str]] = {
        r.version: set(paired[r.id].ticket_external_ids) for r in live
    }
    snapshot: Dict[str, Optional[Set[str]]] = {
        r.version: (
            set(r.board_ticket_keys) if r.board_ticket_keys is not None else None
        )
        for r in live
    }
    stage_of = {r.version: paired[r.id].stage for r in live}
    board_id_of = {r.version: paired[r.id].external_id for r in live}

    keys = set().union(*board_keys.values()) if board_keys else set()
    keys |= {k for s in snapshot.values() if s for k in s}
    tickets = session.exec(
        select(Ticket).where(
            Ticket.board_registration_id == registration.id,
            Ticket.project_id == project_id,
            Ticket.deleted_at.is_(None),  # type: ignore[union-attr]
            col(Ticket.external_ticket_id).is_not(None),
        )
    ).all()
    tickets = [
        t
        for t in tickets
        if (t.external_ticket_id in keys or t.release in versions)
        and t.release not in frozen
    ]

    for ticket in tickets:
        key = ticket.external_ticket_id
        on_board = {v for v in versions if key in board_keys[v]}
        placed = ticket.release if ticket.release in versions else None

        added = {
            v
            for v in on_board
            if (snapshot[v] is not None and key not in snapshot[v])
            or snapshot[v] is None
        }
        removed = {
            v
            for v in versions
            if snapshot[v] and key in snapshot[v] and v not in on_board
        }
        if key in innoday_wins:
            pass  # a person just set this in InnoDay; push it as it stands
        elif added and placed not in on_board:
            # Includes the first run (no snapshot): what the board holds wins
            # over an InnoDay value nobody chose -- before this sync existed,
            # those came from stale semver labels.
            ticket.release = _pick(added, stage_of)
            session.add(ticket)
            run.counts["tickets_attached"] += 1
        elif placed in removed:
            ticket.release = None
            session.add(ticket)
            run.counts["tickets_cleared"] += 1

        # Push InnoDay's (possibly just updated) placement to the board.
        desired = {ticket.release} if ticket.release in versions else set()
        for v in sorted(on_board - desired):
            if await run.attempt(
                f"detach {key} from {v}",
                adapter.remove_ticket_from_release(board_id_of[v], key),
            ):
                board_keys[v].discard(key)
                run.counts["board_detached"] += 1
        for v in sorted(desired - on_board):
            if await run.attempt(
                f"attach {key} to {v}",
                adapter.add_ticket_to_release(board_id_of[v], key),
            ):
                board_keys[v].add(key)
                run.counts["board_attached"] += 1

    # 4. The snapshot is what the board holds now, including any failed pushes,
    #    so the next sync sees "board unchanged" and retries InnoDay's answer.
    for release in live:
        release.board_ticket_keys = sorted(board_keys[release.version])
        session.add(release)

    return {
        "status": "synced" if not run.errors else "partial",
        "matched_releases": sorted(versions),
        "extra_releases": sorted(b.version for b in unpaired.values()),
        **run.counts,
        "errors": run.errors,
    }


def _pick(candidates: Set[str], stage_of: Dict[str, str]) -> str:
    """One version for a ticket the board added to several managed releases.

    An open release (not completed or canceled) wins, since that is where the
    work is going; ties break on the version string so the answer never
    depends on the order the board happened to return releases in.
    """
    closed = {"completed", CANCELED}
    return min(candidates, key=lambda v: (stage_of.get(v) in closed, v))


#: Board types whose adapter has a release line. Others are skipped before any
#: credential or connection work -- they would only answer "InnoDay only".
RELEASE_BOARD_TYPES = {BoardType.LINEAR}


async def sync_project_releases(
    session: Session,
    project_id: str,
    innoday_wins: Optional[Set[str]] = None,
) -> Optional[dict]:
    """Run the release reconcile for a project's board, right after an InnoDay write.

    Called by the release and ticket routes once their own change is committed,
    so InnoDay's answer reaches the board without waiting for the next board
    sync. Best-effort and self-contained: it never raises, a project without a
    live board is a no-op, and anything it could not do the next board sync
    does. Returns the reconcile summary, or None when nothing ran.

    **Never the first reconcile.** Until board sync has paired this project's
    releases, pairing and back-filling a whole board belongs in that
    background job, not inside somebody's PATCH.
    """
    # Imported here: the factory imports adapters that import this package's
    # neighbours, and a module-level import would be a cycle.
    from src.services.board_adapter_factory import (
        build_board_adapter,
        resolve_board_token,
    )

    registration = session.exec(
        select(BoardRegistration).where(
            BoardRegistration.project_id == project_id,
            BoardRegistration.deleted_at.is_(None),  # type: ignore[union-attr]
            BoardRegistration.is_active == True,  # noqa: E712
        )
    ).first()
    if registration is None or registration.board_type not in RELEASE_BOARD_TYPES:
        return None
    paired_before = session.exec(
        select(Release.id).where(
            Release.project_id == project_id,
            col(Release.board_release_id).is_not(None),
        )
    ).first()
    if paired_before is None:
        return None
    try:
        # One SAVEPOINT for everything that touches the database: on Postgres
        # a failed statement would otherwise poison the caller's session.
        with session.begin_nested():
            org = session.get(Organization, registration.organization_id)
            token = resolve_board_token(session, registration, org)
            adapter = await build_board_adapter(registration, token, session)
            await adapter.initialize(token)
            result = await reconcile_from_board(
                session, registration, adapter, project_id, innoday_wins
            )
        session.commit()
        return result
    except Exception as e:  # noqa: BLE001 -- never fails the InnoDay write
        logger.warning("Release push for project %s failed: %s", project_id, e)
        return {"status": "error", "message": str(e)}
