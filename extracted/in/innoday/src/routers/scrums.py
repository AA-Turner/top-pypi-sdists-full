"""
Scrums API Router

A scrum is one timed walk of a project's board -- the *meeting*, not a report of
it. It is opened when the walk starts, written to once per ticket as the walk
proceeds, and closed at wrap-up.

**The per-visit write is the design, not an implementation detail.** A walk that
is interrupted half way through is ordinary, so the endpoint that records a stop
takes exactly one stop and is called as that stop ends. Collecting the visits
client-side and posting them at the finish would mean every abandoned run left no
trace at all -- which is precisely the run whose record is worth having.

Prose belongs to `Summary` (see `src/routers/summaries.py`); this router links to
summaries but never writes one. `initial_summary_id` is stamped at start from
whatever scrum summary already exists for today.

`updated_summary_id` is whatever the caller regenerated after the walk, and it
**must be sent on the closing PATCH** -- the one that also sets `ended_at`.
Closing is once (`scrum_service.apply_wrap_up`), so a second PATCH answers 409
and there is no call left to add it in afterwards. The order is therefore:
finish the walk, regenerate the summary, then close with both fields together.
The `/ui` page regenerates nothing, so scrums it records leave the column NULL.

**The writes themselves are in `src/services/scrum_service.py`**, not here. The
workflow page records a scrum too, over ``/ui`` with a session cookie, because a
browser cannot authenticate against ``/api/v1`` -- so the rules about who may
close a run and what a wrap-up field may contain have to hold for two routers.
This module is the HTTP shape of them: it resolves the org, calls the service,
and maps its refusals onto status codes.
"""

import logging
from datetime import datetime
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from pydantic import BaseModel, ConfigDict, Field
from sqlmodel import Session, select

from src.database import get_session
from src.domain.organization import Organization
from src.domain.scrum import Scrum, ScrumTicketVisit
from src.domain.user import User
from src.middleware.rbac import (
    get_current_user,
    require_org_role,
)
from src.routers.projects import resolve_project
from src.services import scrum_service

logger = logging.getLogger(__name__)

router = APIRouter(tags=["scrums"])


# ---------------------------------------------------------------------------
# Request / Response models
# ---------------------------------------------------------------------------


class ScrumStart(BaseModel):
    started_at: Optional[str] = Field(
        None,
        description=(
            "ISO timestamp the walk began. Omit and the server stamps now -- "
            "which is the normal case; this exists for a client replaying a "
            "run it recorded while offline."
        ),
    )


#: Both request models below are **strict and unconstrained**, and that is one
#: decision rather than two.
#:
#: *Unconstrained*, because `scrum_service` already refuses every value these
#: models used to refuse -- and refuses it for the ``/ui`` routes too, which have
#: no model in front of them. A ``ge=0`` here on top of `_checked_int` there is a
#: second authority on the same question, and the second authority is the one
#: that drifts: the constraints and the service's limits have to be kept equal by
#: hand, and nothing notices when they stop being.
#:
#: *Strict*, because dropping the constraints alone would leave the worse half of
#: the drift in place. Lax pydantic **coerces**, so ``seconds: true`` arrived at
#: the service as ``1`` and was stored as a stop that took one second, while the
#: byte-identical body on ``/ui`` was refused -- `_checked_int` rejects ``bool``
#: in as many words. The same went for ``"5"`` and ``5.0``. Strict mode hands the
#: value over as it was sent, so both surfaces now answer the same question with
#: the same code.
#:
#: The two still word their refusals differently -- pydantic's error list against
#: `_scrum_error`'s ``{"error", "field"}`` -- and that is inherent: one is read by
#: an SDK, the other by page JavaScript that puts the message beside the box.
_STRICT = ConfigDict(strict=True)


class VisitCreate(BaseModel):
    model_config = _STRICT

    ticket_id: int = Field(..., description="`ticket.id` -- an integer, not a UUID.")
    position: int = Field(..., description="0-based order this ticket was reached in.")
    seconds: int = Field(..., description="Time spent on this ticket.")
    status_at_visit: str = Field(
        ...,
        description=(
            "The ticket's status when it was reached. A free string on purpose: "
            "it is a historical observation, so retiring a status later must not "
            "rewrite what was true at the time. Length is checked by "
            "`scrum_service.STATUS_TEXT_MAX`."
        ),
    )
    comment: Optional[str] = None
    moved_to: Optional[str] = Field(
        None, description="The status it was moved to, if it moved."
    )


class ScrumFinish(BaseModel):
    model_config = _STRICT

    ended_at: Optional[str] = Field(
        None, description="ISO timestamp; naive UTC stored."
    )
    total_seconds: Optional[int] = Field(
        None,
        description=(
            "The page's own clock. Sent rather than derived, because "
            "`ended_at - started_at` also counts the tab sitting open."
        ),
    )
    transcript_url: Optional[str] = Field(
        None,
        description=(
            "http/https link to the recording. A value with no scheme is "
            "completed to https rather than refused -- it is typed by hand. "
            "Length is checked by `scrum_service.TRANSCRIPT_URL_MAX`, after the "
            "scheme is completed."
        ),
    )
    updated_summary_id: Optional[str] = Field(
        None,
        description=(
            "The summary regenerated after the walk. Send it on **this** call: "
            "the same PATCH closes the scrum, and a closed scrum refuses "
            "further writes, so there is no later call to add it in."
        ),
    )
    lingering_count: Optional[int] = None
    notes_markdown: Optional[str] = None


class VisitResponse(BaseModel):
    id: str
    scrum_id: str
    ticket_id: int
    position: int
    seconds: int
    status_at_visit: str
    comment: Optional[str] = None
    moved_to: Optional[str] = None
    created_at: datetime


class ScrumResponse(BaseModel):
    id: str
    organization_id: str
    project_id: str
    run_by_user_id: str
    started_at: datetime
    ended_at: Optional[datetime] = None
    total_seconds: Optional[int] = None
    initial_summary_id: Optional[str] = None
    updated_summary_id: Optional[str] = None
    transcript_url: Optional[str] = None
    lingering_count: Optional[int] = None
    notes_markdown: Optional[str] = None
    visit_count: int = 0


class ScrumDetail(ScrumResponse):
    visits: List[VisitResponse] = []


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _http(error: scrum_service.ScrumError) -> HTTPException:
    """The service's refusal, as the HTTP answer it deserves.

    The table itself is `scrum_service.HTTP_STATUS_FOR`, not a copy here. This
    router and the ``/ui`` write routes each kept an identical one, which is the
    same two-surfaces-one-rule problem the service was created for: a new
    refusal added to one table is a 400 on the other, and nothing says so.
    """
    return HTTPException(
        status_code=scrum_service.http_status(error), detail=str(error)
    )


def _to_response(scrum: Scrum, session: Session) -> ScrumResponse:
    return ScrumResponse(
        id=scrum.id,
        organization_id=scrum.organization_id,
        project_id=scrum.project_id,
        run_by_user_id=scrum.run_by_user_id,
        started_at=scrum.started_at,
        ended_at=scrum.ended_at,
        total_seconds=scrum.total_seconds,
        initial_summary_id=scrum.initial_summary_id,
        updated_summary_id=scrum.updated_summary_id,
        transcript_url=scrum.transcript_url,
        lingering_count=scrum.lingering_count,
        notes_markdown=scrum.notes_markdown,
        visit_count=scrum_service.visit_count(session, scrum.id),
    )


def _to_visit_response(visit: ScrumTicketVisit) -> VisitResponse:
    return VisitResponse(
        id=visit.id,
        scrum_id=visit.scrum_id,
        ticket_id=visit.ticket_id,
        position=visit.position,
        seconds=visit.seconds,
        status_at_visit=visit.status_at_visit,
        comment=visit.comment,
        moved_to=visit.moved_to,
        created_at=visit.created_at,
    )


# ---------------------------------------------------------------------------
# Endpoints
# ---------------------------------------------------------------------------
#
# All five are gated at plain membership (`require_org_role()`), not DEVELOPER.
# A scrum record is a record of a meeting its participants attended, and a MEMBER
# can already write the tickets the walk moves -- gating the minutes higher than
# the work they describe would only produce runs that go unrecorded.


@router.post(
    "/api/v1/organizations/{org_id}/projects/{project_id}/scrums",
    response_model=ScrumResponse,
    status_code=status.HTTP_201_CREATED,
)
async def start_scrum(
    org_id: str,
    project_id: str,
    body: Optional[ScrumStart] = None,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
    org: Organization = Depends(require_org_role()),
):
    """Open a scrum. Stamps who ran it and when, and links today's summary.

    `{project_id}` accepts a UUID, an alias or a name, like every other
    project-scoped route -- `resolve_project` owns that, including the refusal to
    guess between two projects sharing a name.
    """
    project = resolve_project(project_id, org.id, session)

    try:
        scrum = scrum_service.open_scrum(
            session,
            organization_id=org.id,
            project_id=project.id,
            run_by_user_id=current_user.id,
            started_at=body.started_at if body else None,
        )
    except scrum_service.ScrumError as exc:
        raise _http(exc)
    return _to_response(scrum, session)


@router.post(
    "/api/v1/organizations/{org_id}/scrums/{scrum_id}/visits",
    response_model=VisitResponse,
    status_code=status.HTTP_201_CREATED,
)
async def record_visit(
    org_id: str,
    scrum_id: str,
    body: VisitCreate,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
    org: Organization = Depends(require_org_role()),
):
    """Record one stop on the walk. One call per ticket, as the stop ends.

    Deliberately not a bulk endpoint -- see the module docstring. Only the person
    who opened the scrum may add to it: membership says what may be written, not
    whose row it may be written to.
    """
    try:
        scrum = scrum_service.writable_scrum(session, scrum_id, org.id, current_user.id)
        visit = scrum_service.record_visit(
            session,
            scrum=scrum,
            ticket_id=body.ticket_id,
            position=body.position,
            seconds=body.seconds,
            status_at_visit=body.status_at_visit,
            comment=body.comment,
            moved_to=body.moved_to,
        )
    except scrum_service.ScrumError as exc:
        raise _http(exc)
    return _to_visit_response(visit)


@router.patch(
    "/api/v1/organizations/{org_id}/scrums/{scrum_id}",
    response_model=ScrumResponse,
)
async def finish_scrum(
    org_id: str,
    scrum_id: str,
    body: ScrumFinish,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
    org: Organization = Depends(require_org_role()),
):
    """Close a scrum: end time, clock, transcript, regenerated summary, notes.

    Only fields the caller actually sent are written (`exclude_unset`), so a
    wrap-up that fills in the notes cannot blank the transcript URL it did not
    mention.

    422 for a malformed ``ended_at`` or ``transcript_url``, 403 for someone who
    did not run the walk, 409 once it is closed -- all decided by
    `scrum_service.apply_wrap_up`, which the ``/ui`` page shares.
    """
    try:
        scrum = scrum_service.writable_scrum(session, scrum_id, org.id, current_user.id)
        scrum = scrum_service.apply_wrap_up(
            session, scrum=scrum, sent=body.model_dump(exclude_unset=True)
        )
    except scrum_service.ScrumError as exc:
        raise _http(exc)
    return _to_response(scrum, session)


@router.get(
    "/api/v1/organizations/{org_id}/projects/{project_id}/scrums",
    response_model=List[ScrumResponse],
)
async def list_scrums(
    org_id: str,
    project_id: str,
    limit: int = Query(50, ge=1, le=200),
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
    org: Organization = Depends(require_org_role()),
):
    """This project's scrums, most recent first."""
    project = resolve_project(project_id, org.id, session)

    scrums = session.exec(
        select(Scrum)
        .where(Scrum.project_id == project.id)
        .order_by(Scrum.started_at.desc())  # type: ignore[attr-defined]
        .limit(limit)
    ).all()
    return [_to_response(s, session) for s in scrums]


@router.get(
    "/api/v1/organizations/{org_id}/scrums/{scrum_id}",
    response_model=ScrumDetail,
)
async def get_scrum(
    org_id: str,
    scrum_id: str,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
    org: Organization = Depends(require_org_role()),
):
    """One scrum with its visits nested, in the order the walk took them."""
    try:
        scrum = scrum_service.resolve_scrum(session, scrum_id, org.id)
    except scrum_service.ScrumError as exc:
        raise _http(exc)

    visits = session.exec(
        select(ScrumTicketVisit)
        .where(
            ScrumTicketVisit.scrum_id == scrum.id,
            # **A withdrawn pick is not part of the record**, here as much as on
            # the page. Its row survives only to remember whether the board ever
            # got that ticket's comment (`ScrumTicketVisit.withdrawn_at`).
            #
            # This filter was the one that got missed. `withdrawn_at` was added
            # for `/ui`, and the three readers enumerated with it were the three
            # in the files that change was already touching -- this router was
            # not one of them, so it kept serving withdrawn picks *and* their
            # comment text while `visit_count` in the same payload excluded
            # them. A response that contradicts itself is worse than either
            # answer alone, and `VisitResponse` carries no `withdrawn_at`, so a
            # consumer could not have filtered it either.
            #
            # The general lesson, recorded because it is the hazard of any new
            # lifecycle state: the readers to update are found by grepping every
            # consumer of the model, not by reading the diff.
            ScrumTicketVisit.withdrawn_at.is_(None),  # type: ignore[union-attr]
        )
        # `position`, then `created_at`: position is what the walk meant, and the
        # tie-break keeps two stops that were sent the same position stable
        # rather than ordered arbitrarily by the planner.
        .order_by(ScrumTicketVisit.position, ScrumTicketVisit.created_at)  # type: ignore[arg-type]
    ).all()

    base = _to_response(scrum, session)
    return ScrumDetail(
        **base.model_dump(),
        visits=[_to_visit_response(v) for v in visits],
    )
