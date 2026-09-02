"""Changing which versions a project's two forward slots hold.

``release_planning`` decides the *shape* of the pipeline and is deliberately
pure -- every function there takes a list of releases and touches no session.
This module is the other half: the one operation that has to write, and the only
one that has to know about tickets.

**Why retargeting needs its own home rather than a ``version`` field on
``ReleaseUpdate``.** A release is joined to its tickets by a free-text match --
``ticket.release == release.version``, with no foreign key (see the ``Release``
docstring). Renaming the row alone silently detaches every ticket planned into
it -- so the release ships reporting that nothing was planned into it, and the
work is in no slot, in no pool, and in no release. The rename and the rewrite
are one operation or they are a bug, and burying that inside a generic PATCH
field is how the two get separated by someone later.
"""

import logging
from dataclasses import dataclass, field
from typing import List, Optional, Tuple

from sqlmodel import Session, select

from src.domain.release import Release
from src.domain.ticket import Ticket, TicketStatus
from src.services.release_planning import (
    BUMP_PARTS,
    next_release,
    pipeline_options,
    semver_key,
    slot_two,
)

logger = logging.getLogger(__name__)


@dataclass
class Retarget:
    """What a retarget did, or why it did nothing."""

    ok: bool
    message: str
    #: (old version, new version) for each slot that moved.
    moved: List[Tuple[str, str]] = field(default_factory=list)
    tickets_rewritten: int = 0


def _rename(session: Session, release: Release, new_version: str) -> int:
    """Move one release to a new version, taking its tickets with it.

    Returns how many tickets followed. The two writes are inseparable: see the
    module docstring.
    """
    old = release.version
    tickets = session.exec(
        select(Ticket).where(
            Ticket.project_id == release.project_id,
            Ticket.release == old,
            Ticket.deleted_at.is_(None),  # type: ignore[union-attr]
        )
    ).all()
    for ticket in tickets:
        ticket.release = new_version
        session.add(ticket)

    release.version = new_version
    release.touch()
    session.add(release)
    return len(tickets)


def promote_backlog_in(session: Session, project_id: str, version: str) -> int:
    """Make sure nothing in a release is still sitting in the backlog.

    Work in the release being **cut** is work in hand, so a BACKLOG ticket becomes
    TODO. Anything above TODO is left alone: a ticket in progress or in review is
    further along, and demoting it to satisfy a rule about the backlog would lose
    real information.

    Stated as an invariant rather than an event -- "the in-progress release has no
    backlog tickets" -- so it is idempotent and both callers can simply assert it:
    the Releases tab when someone plans a ticket in, and the release router when a
    rotation promotes a whole release into that slot. Written once here because the
    two had begun to keep separate copies of the same sentence.

    Returns how many moved. Does not commit; the caller owns the transaction.
    """
    tickets = session.exec(
        select(Ticket).where(
            Ticket.project_id == project_id,
            Ticket.release == version,
            Ticket.status == TicketStatus.BACKLOG,
            Ticket.deleted_at.is_(None),  # type: ignore[union-attr]
        )
    ).all()
    for ticket in tickets:
        ticket.status = TicketStatus.TODO
        ticket.touch()
        session.add(ticket)
    if tickets:
        logger.info(
            "release.backlog_promoted project_id=%s version=%s count=%s",
            project_id,
            version,
            len(tickets),
        )
    return len(tickets)


def retarget(session: Session, project_id: str, part: str) -> Retarget:
    """Recompute both forward slots as a ``part`` bump of the last shipped version.

    ``part`` is major, minor or patch. Slot 1 becomes that bump of the highest
    released version and slot 2 becomes a minor bump of slot 1 -- always
    recomputed from what has *shipped*, never from what the slots currently hold.
    That is what makes this a toggle rather than a ratchet: flipping to major and
    back to minor lands exactly where it started, however many times it is
    flipped, and no previous value has to be stored anywhere for "revert" to
    work.

    Refuses rather than guesses in three cases, each of which would otherwise
    fail at commit or silently do the wrong thing:

    * an unknown ``part``;
    * a project whose slots hold non-semver versions, which cannot be bumped;
    * a target version already held by some other release row, which would
      violate ``uq_release_project_version``.

    Does not commit. The caller owns the transaction, so the renames and the
    ticket rewrites land together or not at all.
    """
    if part not in BUMP_PARTS:
        return Retarget(False, f"{part!r} is not a version part.")

    releases = list(
        session.exec(
            select(Release).where(
                Release.project_id == project_id,
                Release.deleted_at.is_(None),
            )
        ).all()
    )

    slot_one = next_release(releases)
    if slot_one is None:
        return Retarget(
            False,
            "This project has no upcoming release to move. It appears once "
            "something has shipped, or on the next repository sync.",
        )

    options = {option[0]: option for option in pipeline_options(releases)}
    if part not in options:
        return Retarget(
            False,
            f"{slot_one.version} cannot be bumped -- it is not a version number.",
        )
    _, want_one, want_two = options[part]

    # Slot 2 is the lowest PLANNED row **above** slot 1 -- and that qualifier used
    # to be in this comment and not in the code, which is #577: a PLANNED row below
    # the version being cut was invisible on the page and yet was what this moved.
    # `slot_two` is now the single implementation of the sentence, shared with the
    # page that displays it. There may be none yet if a rotation half-failed;
    # retargeting slot 1 alone is still correct, and the next sync opens the slot
    # above it.
    second: Optional[Release] = slot_two(releases, slot_one)

    wanted = {slot_one.id: want_one}
    if second is not None:
        wanted[second.id] = want_two

    # Collision check across the whole project before writing anything: a
    # half-applied retarget is worse than a refused one.
    taken = {
        release.version: release for release in releases if release.id not in wanted
    }
    for version in wanted.values():
        clash = taken.get(version)
        if clash is not None:
            return Retarget(
                False,
                f"{version} already exists on this project "
                f"({clash.status.value}). Nothing was changed.",
            )

    moved = []
    rewritten = 0
    by_id = {release.id: release for release in releases}
    # Highest first, so an intermediate state never collides with the slot it is
    # about to vacate -- moving v1.9.0 -> v2.0.0 while v1.10.0 still holds its
    # old value is fine, but the reverse order can transiently duplicate.
    for release_id, version in sorted(
        wanted.items(), key=lambda item: semver_key(item[1]), reverse=True
    ):
        release = by_id[release_id]
        if release.version == version:
            continue
        was = release.version
        rewritten += _rename(session, release, version)
        moved.append((was, version))

    if not moved:
        return Retarget(True, f"Already on the {part} line. Nothing to change.")

    logger.info(
        "release.pipeline_retargeted project_id=%s part=%s moved=%s tickets=%s",
        project_id,
        part,
        moved,
        rewritten,
    )
    ticket_note = (
        f" {rewritten} ticket{'' if rewritten == 1 else 's'} moved with them."
        if rewritten
        else ""
    )
    return Retarget(
        True,
        f"Now heading for {want_one}, then {want_two}.{ticket_note}",
        moved=moved,
        tickets_rewritten=rewritten,
    )
