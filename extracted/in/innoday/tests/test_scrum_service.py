"""`src/services/scrum_service.py` at the service level.

**Why this file exists.** Until now the service was covered only *through* its
two routers -- `tests/test_scrums_router.py` for ``/api/v1`` and the workflow
page tests for ``/ui``. That was tolerable while every rule it held was a shape
check both surfaces exercised on the way past. It stops being tolerable the
moment a rule is asymmetric: the day-and-kind identity of a scrum, and the
re-close asymmetry between a team scrum and a personal update, are decisions
only one surface reaches today, so a router test would certify half of each.

The rules pinned here:

* **kind isolation** -- an open team scrum is not handed to somebody opening a
  personal update, and the reverse. Nothing about that is visible from either
  router's happy path; it shows up as picks landing on a meeting's row.
* **one *update* row per (project, runner, day)** -- re-entry resumes rather than
  starting a second record. Asserted as a ``count(*)``, because "the same id came
  back" and "there is only one row" are different claims and only the second is the
  guarantee.
* **a scrum is not constrained that way, deliberately** -- a team may hold two
  stand-ups in a day, so the unique index is partial and the second meeting gets
  its own row. That capability is easy to lose to a tidier-looking key, so it is
  pinned at both levels.
* **the DB actually enforces exactly that split** -- two Postgres-only tests, one
  for the refusal and one for the permission, because the index ships in a
  migration and the SQLite suite never runs the chain.
* **an update may be re-closed; a scrum may not** -- and a re-close has to
  *change* the record, not merely be accepted.
* **whose row it is** -- `require_runner`'s refusal is unchanged by any of this.
"""

from datetime import date, datetime
from uuid import uuid4

import pytest
from sqlalchemy import func, text
from sqlmodel import Session as SQLSession
from sqlmodel import select

from src.domain.organization import (
    Organization,
    OrganizationMembership,
    OrganizationRole,
)
from src.domain.project import Project
from src.domain.scrum import (
    UPDATE_DAY_INDEX,
    Scrum,
    ScrumKind,
    ScrumTicketVisit,
)
from src.domain.ticket import Ticket, TicketStatus
from src.domain.user import User
from src.services import scrum_service

# A frozen instant, deliberately. Every "which day is this on?" assertion below
# is about a boundary, and a boundary computed from `now()` is a test that means
# something different depending on the hour the suite runs at -- including
# passing every time except between 23:00 and midnight UTC.
DAY = date(2026, 8, 17)
MORNING = "2026-08-17T09:00:00Z"
LATE = "2026-08-17T23:30:00Z"
JUST_AFTER = "2026-08-18T00:30:00Z"


@pytest.fixture
def world(db_engine):
    """One org, one project, two members -- the smallest board two people share."""
    with SQLSession(db_engine) as session:
        org = Organization(id=str(uuid4()), name="Haviland", alias="hs")
        alice = User(id=str(uuid4()), email="alice@example.com", full_name="Alice A")
        bob = User(id=str(uuid4()), email="bob@example.com", full_name="Bob B")
        session.add_all([org, alice, bob])
        session.commit()
        for person in (alice, bob):
            session.add(
                OrganizationMembership(
                    id=str(uuid4()),
                    organization_id=org.id,
                    user_id=person.id,
                    role=OrganizationRole.MEMBER,
                    is_active=True,
                )
            )
        project = Project(
            id=str(uuid4()),
            organization_id=org.id,
            alias="PF",
            name="PixelFuel",
            description="d",
        )
        session.add(project)
        session.commit()
        session.refresh(org)
        session.refresh(project)
        session.refresh(alice)
        session.refresh(bob)
        yield {
            "engine": db_engine,
            "org": org,
            "project": project,
            "alice": alice,
            "bob": bob,
        }


def _open(session, world, *, kind, user=None, started_at=None):
    """Open a record. ``started_at`` defaults to **omitted**, which matters.

    An explicit ``started_at`` means "this is a replay of a run I recorded
    offline", and for a team scrum that deliberately bypasses the resume lookup --
    it asserts *which* run this is. So a test about scrum idempotency must leave it
    out or it is testing the replay path instead. The update tests pass one because
    an update always keys on its day, replay or not, and a frozen day is what lets
    them assert a boundary without reading the clock.
    """
    return scrum_service.open_scrum(
        session,
        organization_id=world["org"].id,
        project_id=world["project"].id,
        run_by_user_id=(user or world["alice"]).id,
        kind=kind,
        started_at=started_at,
    )


def _count(session, world, kind, day=None):
    """How many of one kind Alice has on this project. ``day`` narrows it to one.

    Left off for the scrum cases: they are about "how many meetings", and nothing
    keys a scrum by day, so filtering on today's date would be a filter the
    behaviour under test does not have.
    """
    conditions = [
        Scrum.project_id == world["project"].id,
        Scrum.run_by_user_id == world["alice"].id,
        Scrum.kind == kind,
    ]
    if day is not None:
        conditions.append(Scrum.day == day)
    return int(
        session.exec(select(func.count()).select_from(Scrum).where(*conditions)).one()
    )


def _make_ticket(session, world, summary):
    ticket = Ticket(
        summary=summary,
        organization_id=world["org"].id,
        project_id=world["project"].id,
        status=TicketStatus.DONE,
    )
    session.add(ticket)
    session.commit()
    session.refresh(ticket)
    return ticket.id


def _visit_ids(session, scrum):
    return [
        v.ticket_id
        for v in session.exec(
            select(ScrumTicketVisit)
            .where(ScrumTicketVisit.scrum_id == scrum.id)
            .order_by(ScrumTicketVisit.position)
        ).all()
    ]


def test_a_personal_update_is_never_handed_the_team_scrums_row(world):
    """**The strongest argument for the discriminator, and it is silent.**

    `open_scrum` used to be idempotent on ``(org, project, user, ended_at IS
    NULL)`` -- nothing about a kind. So somebody who had walked half a stand-up
    and then opened their own daily update got *the meeting's row* back, and
    every pick they made was written onto the minutes of the scrum. No error, no
    second row, nothing on screen to notice.

    Both directions, because the failure is symmetric: an open update must not
    be handed to somebody starting the team walk either.
    """
    with SQLSession(world["engine"]) as session:
        scrum = _open(session, world, kind=ScrumKind.SCRUM.value)
        update = _open(session, world, kind=ScrumKind.UPDATE.value)
        assert update.id != scrum.id, (
            "the personal update was written onto the team scrum's row"
        )
        assert update.kind == ScrumKind.UPDATE.value
        assert scrum.kind == ScrumKind.SCRUM.value

        # And re-asking for each one gets its own back, not the other.
        assert _open(session, world, kind=ScrumKind.SCRUM.value).id == scrum.id
        assert _open(session, world, kind=ScrumKind.UPDATE.value).id == update.id


def test_re_entering_an_update_resumes_the_day_rather_than_starting_a_second(world):
    """Requirement 6: one record per person per project per day.

    A submitted update has ``ended_at`` set, and the old idempotency keyed on
    ``ended_at IS NULL`` -- so re-entry to correct a pick opened a **second**
    row, and the day then had two answers to "what did Alice say?".

    Both halves are asserted. "The same id came back" would still be true if a
    second row existed and the query happened to order this one first, so the
    guarantee is the ``count(*)``.
    """
    with SQLSession(world["engine"]) as session:
        first = _open(session, world, kind=ScrumKind.UPDATE.value, started_at=MORNING)
        scrum_service.apply_wrap_up(
            session, scrum=first, sent={"ended_at": "2026-08-17T09:05:00Z"}
        )
        again = _open(session, world, kind=ScrumKind.UPDATE.value, started_at=MORNING)
        assert again.id == first.id
        assert _count(session, world, ScrumKind.UPDATE.value, DAY) == 1


def test_a_second_stand_up_in_one_day_is_a_second_meeting(world):
    """**A team may hold two scrums in a day, and this is what keeps that possible.**

    A dropped call restarted, a session split across a break, two halves of a team
    in different timezones -- all ordinary, all a *second meeting* with minutes of
    its own. The unique index is partial (``WHERE kind = 'update'``) precisely so
    this stays recordable: an earlier draft put ``kind`` inside a whole-table key,
    which reads tidier and silently made the second stand-up impossible.

    "Scrums stay final" is a different rule and is enforced elsewhere --
    `apply_wrap_up` refuses a second *close*, which is the test below. Finality of
    the record is not the same claim as one-meeting-per-day, and conflating them is
    how the capability got lost the first time.
    """
    with SQLSession(world["engine"]) as session:
        morning = _open(session, world, kind=ScrumKind.SCRUM.value)
        scrum_service.apply_wrap_up(
            session, scrum=morning, sent={"ended_at": "2026-08-17T09:20:00Z"}
        )
        afternoon = _open(session, world, kind=ScrumKind.SCRUM.value)
        assert afternoon.id != morning.id, (
            "the afternoon's stand-up was written onto the morning's record"
        )
        assert afternoon.ended_at is None
        assert _count(session, world, ScrumKind.SCRUM.value) == 2

        # And the un-ended one is still what a retry or a cancel-and-restart gets,
        # so the second meeting has the same idempotency the first did.
        assert _open(session, world, kind=ScrumKind.SCRUM.value).id == afternoon.id
        assert _count(session, world, ScrumKind.SCRUM.value) == 2


def test_an_update_may_be_re_closed_and_the_second_close_actually_changes_it(world):
    """Your daily form is yours to correct until the day ends. A meeting's minutes are not.

    The acceptance is not enough on its own: `apply_wrap_up` returning without
    raising while writing nothing would satisfy a test that only looked at the
    exception. So the second close carries a different value and the value is
    read back.
    """
    with SQLSession(world["engine"]) as session:
        update = _open(session, world, kind=ScrumKind.UPDATE.value, started_at=MORNING)
        scrum_service.apply_wrap_up(
            session,
            scrum=update,
            sent={"ended_at": "2026-08-17T09:05:00Z", "notes_markdown": "first pass"},
        )
        again = scrum_service.apply_wrap_up(
            session,
            scrum=update,
            sent={"ended_at": "2026-08-17T09:40:00Z", "notes_markdown": "corrected"},
        )
        assert again.notes_markdown == "corrected"
        assert again.ended_at == datetime(2026, 8, 17, 9, 40, 0)


def test_a_team_scrum_still_refuses_a_second_close(world):
    """The asymmetry is the point, so the other half is pinned too."""
    with SQLSession(world["engine"]) as session:
        scrum = _open(session, world, kind=ScrumKind.SCRUM.value)
        scrum_service.apply_wrap_up(
            session, scrum=scrum, sent={"ended_at": "2026-08-17T09:05:00Z"}
        )
        with pytest.raises(scrum_service.ScrumAlreadyClosed):
            scrum_service.apply_wrap_up(
                session, scrum=scrum, sent={"notes_markdown": "sneaking this in"}
            )


def test_a_teammates_record_is_still_not_yours_to_write(world):
    """`require_runner`'s refusal is untouched by any of this.

    Requirement 5 is per *project*: a scrum somebody else ran still ticks the
    picker. Requirement 6 is per *person*: it does not make their row editable.
    Conflating the two is how "resume today's record" becomes "silently edit the
    minutes of a meeting somebody else ran", which the service refuses to be.
    """
    with SQLSession(world["engine"]) as session:
        theirs = _open(session, world, kind=ScrumKind.SCRUM.value, user=world["bob"])
        with pytest.raises(scrum_service.ScrumNotYours):
            scrum_service.require_runner(theirs, world["alice"].id)
        # And Alice opening her own update on the same project is a different row.
        mine = _open(session, world, kind=ScrumKind.UPDATE.value)
        assert mine.id != theirs.id


def test_the_day_comes_from_started_at_and_the_boundary_is_utc_midnight(world):
    """Late in the evening is still today; half an hour later is not.

    ``day`` is stamped server-side from ``started_at``, which is naive UTC --
    never from ``created_at``, which `TimestampMixin` makes *aware*, and never
    from a client-supplied local date, which lets a tab in UTC+13 tick
    tomorrow's box.

    Both instants are explicit rather than derived from `datetime.utcnow`: a
    boundary test that reads the clock passes or fails depending on the hour.
    """
    with SQLSession(world["engine"]) as session:
        late = _open(session, world, kind=ScrumKind.UPDATE.value, started_at=LATE)
        assert late.day == date(2026, 8, 17)

        after = _open(
            session,
            world,
            kind=ScrumKind.UPDATE.value,
            started_at=JUST_AFTER,
        )
        assert after.day == date(2026, 8, 18)
        # Thirty minutes apart and two different days, so two different records.
        assert after.id != late.id


def test_replacing_picks_validates_the_whole_set_before_writing_any_of_it(world):
    """A malformed fifth pick must not leave the first four recorded.

    The call's entire contract is "this is the answer" -- a partial application of
    it is the one outcome that cannot be right, because the caller is then told the
    write failed while the record holds some of it. So every pick is checked before
    the first is written, and the refusal names the field like every other one here.
    """
    with SQLSession(world["engine"]) as session:
        update = _open(session, world, kind=ScrumKind.UPDATE.value, started_at=MORNING)
        good = _make_ticket(session, world, "real one")

        with pytest.raises(scrum_service.ScrumInvalid):
            scrum_service.replace_picks(
                session,
                scrum=update,
                sent=[
                    {"ticket_id": good, "status_at_visit": "done"},
                    {"ticket_id": good, "status_at_visit": "done"},  # the same box
                ],
            )
        assert _visit_ids(session, update) == []

        with pytest.raises(scrum_service.ScrumNotFound):
            scrum_service.replace_picks(
                session,
                scrum=update,
                sent=[
                    {"ticket_id": good, "status_at_visit": "done"},
                    {"ticket_id": 987654, "status_at_visit": "done"},
                ],
            )
        assert _visit_ids(session, update) == [], (
            "a refused set left part of itself behind"
        )


def test_a_team_scrums_visits_may_not_be_replaced_as_a_set(world):
    """The per-stop write is what makes an interrupted meeting leave a trace.

    Replacing a scrum's visits wholesale would delete the first half of a walk
    because somebody retried the second, so this is refused at the service rather
    than left to each caller to remember.
    """
    with SQLSession(world["engine"]) as session:
        scrum = _open(session, world, kind=ScrumKind.SCRUM.value)
        ticket = _make_ticket(session, world, "a stop")
        with pytest.raises(scrum_service.ScrumInvalid):
            scrum_service.replace_picks(
                session,
                scrum=scrum,
                sent=[{"ticket_id": ticket, "status_at_visit": "in review"}],
            )


def test_an_unknown_kind_is_refused_rather_than_stored(world):
    """The kind is a discriminator, so an unrecognised one is not a new category.

    Both surfaces reach this: the ``/ui`` route forwards whatever JSON it was
    given, and a value the service accepted would create a partition of the
    table nothing reads and nothing ticks.
    """
    with SQLSession(world["engine"]) as session:
        with pytest.raises(scrum_service.ScrumInvalid):
            _open(session, world, kind="standup")
        with pytest.raises(scrum_service.ScrumInvalid):
            _open(session, world, kind=None)


# --------------------------------------------------------------------------- #
# The database's own guarantee
# --------------------------------------------------------------------------- #


@pytest.fixture
def pg_world(pg_engine):
    """An org, a user and a project on Postgres, with names nothing else will reuse.

    Unique per run: this database persists between runs and `organizations.alias` /
    `users.email` are uniquely indexed, so fixed values pass once and then fail
    forever on a duplicate key -- which is how a regression test stops testing
    anything.
    """
    tag = uuid4().hex[:8]
    with SQLSession(pg_engine) as session:
        org = Organization(id=str(uuid4()), name=f"Dup {tag}", alias=f"dup{tag}")
        user = User(id=str(uuid4()), email=f"dup-{tag}@example.com", full_name="D")
        session.add_all([org, user])
        session.commit()
        project = Project(
            id=str(uuid4()),
            organization_id=org.id,
            alias=f"D{tag[:6]}".upper(),
            name=f"Dup project {tag}",
            description="d",
        )
        session.add(project)
        session.commit()
        yield {"engine": pg_engine, "org": org, "user": user, "project": project}


#: Two rows for one (project, runner, day) differing only in `kind`. Raw SQL rather
#: than the service on purpose: going through `open_scrum` would test `open_scrum`,
#: which the tests above already do. What is under test here is the index.
_INSERT_SCRUM = text(
    "INSERT INTO scrums (id, created_at, updated_at, organization_id, "
    "project_id, run_by_user_id, started_at, kind, day) VALUES "
    "(:id, now(), now(), :org, :project, :user, :started, :kind, :day)"
)


def _row_args(pg_world, kind):
    return {
        "org": pg_world["org"].id,
        "project": pg_world["project"].id,
        "user": pg_world["user"].id,
        "started": datetime(2026, 8, 17, 9, 0, 0),
        "kind": kind,
        "day": DAY,
    }


def test_the_index_refuses_two_updates_on_one_day(pg_world):
    """**Postgres-only, and it has to be.**

    The SQLite suite builds its schema from ``SQLModel.metadata.create_all`` and
    never runs alembic, so the index this asserts ships in a migration that suite
    cannot see. The service's own lookup is what callers meet; this is what holds
    when two requests race it, which is the case no amount of read-then-write in
    Python can close -- and it is exactly the case the page produces, since it
    retries the open after any rejection.
    """
    with SQLSession(pg_world["engine"]) as session:
        args = _row_args(pg_world, ScrumKind.UPDATE.value)
        session.exec(_INSERT_SCRUM, params={**args, "id": str(uuid4())})
        session.commit()

        with pytest.raises(Exception) as caught:
            session.exec(_INSERT_SCRUM, params={**args, "id": str(uuid4())})
            session.commit()
        assert UPDATE_DAY_INDEX in str(caught.value)
        session.rollback()


def test_a_lost_race_resolves_to_the_winning_row_rather_than_a_500(
    pg_world, monkeypatch
):
    """**The concurrency case the index was added for, seen from the caller's side.**

    `_existing_scrum` is a read and the insert after it is a write, so two requests
    that arrive together both find nothing and both insert. That is not a thought
    experiment here: the page retries the open after any rejection and re-opens on
    cancel, so a dropped response followed by a retry produces exactly this.

    An `IntegrityError` is not a `ScrumError`, so neither router's ``except`` sees
    it -- the loser used to get a bare 500 about a record that exists and is
    theirs. Now the loser re-reads and returns the row that won, which is what
    turns the constraint from "converts a duplicate into a 500" into "converts a
    duplicate into the right row".

    **The interleave is forced rather than raced.** Two real sessions would not
    reproduce it: under READ COMMITTED the loser's own lookup inside `open_scrum`
    happens *after* the winner commits, sees the row and returns it without ever
    reaching the insert -- so the test would pass while exercising none of the code
    it is about. Threads would be flaky and would fail the same way on any machine
    that happened to serialise them. So the winning row is inserted up front and
    the *first* lookup is made to answer "nothing", which is exactly the state a
    lost race leaves the loser in: a read that was true when it ran and is not by
    the time the write lands.

    Postgres-only, because the index it depends on ships in a migration and the
    SQLite suite never runs the chain.
    """
    engine = pg_world["engine"]
    args = _row_args(pg_world, ScrumKind.UPDATE.value)
    winner_id = str(uuid4())
    with SQLSession(engine) as winner:
        winner.exec(_INSERT_SCRUM, params={**args, "id": winner_id})
        winner.commit()

    real = scrum_service._existing_scrum
    calls = {"n": 0}

    def stale_first(*a, **kw):
        calls["n"] += 1
        return None if calls["n"] == 1 else real(*a, **kw)

    monkeypatch.setattr(scrum_service, "_existing_scrum", stale_first)

    with SQLSession(engine) as loser:
        resumed = scrum_service.open_scrum(
            loser,
            organization_id=pg_world["org"].id,
            project_id=pg_world["project"].id,
            run_by_user_id=pg_world["user"].id,
            kind=ScrumKind.UPDATE.value,
            started_at=MORNING,
        )

    # The insert really was attempted and really did violate the index -- if the
    # first lookup had found the row there would be no second call.
    assert calls["n"] == 2, "the IntegrityError path was not reached"
    assert resumed.id == winner_id

    # And no second row survived the rollback.
    with SQLSession(engine) as session:
        rows = session.exec(
            select(Scrum).where(
                Scrum.project_id == pg_world["project"].id,
                Scrum.run_by_user_id == pg_world["user"].id,
                Scrum.kind == ScrumKind.UPDATE.value,
                Scrum.day == DAY,
            )
        ).all()
        assert len(rows) == 1


def test_the_index_allows_two_scrums_on_one_day(pg_world):
    """**The other half of the partial predicate, and the half worth pinning hardest.**

    `WHERE kind = 'update'` is easy to lose: dropping it, or folding `kind` into the
    key, leaves a schema that still passes the test above while silently making a
    second stand-up unrecordable. Nothing else would fail — `open_scrum` would hand
    the closed row back, the walk would append its visits to the wrong meeting, and
    the wrap-up's 409 reads to the page as success.

    So the index's permissiveness is asserted directly against the database, not
    inferred from the service being willing to try.
    """
    with SQLSession(pg_world["engine"]) as session:
        args = _row_args(pg_world, ScrumKind.SCRUM.value)
        session.exec(_INSERT_SCRUM, params={**args, "id": str(uuid4())})
        session.exec(_INSERT_SCRUM, params={**args, "id": str(uuid4())})
        session.commit()

        assert (
            int(
                session.exec(
                    select(func.count())
                    .select_from(Scrum)
                    .where(
                        Scrum.project_id == pg_world["project"].id,
                        Scrum.kind == ScrumKind.SCRUM.value,
                        Scrum.day == DAY,
                    )
                ).one()
            )
            == 2
        ), "the index is constraining scrums, so a second meeting cannot be recorded"


@pytest.mark.parametrize("seam", ["resolve_board_token", "build_board_adapter"])
def test_an_aborted_transaction_still_records_why_the_push_failed(
    pg_world, monkeypatch, seam
):
    """**Postgres-only, and it is the #641 class exactly.**

    `_push` reads the database three times inside its blanket `except` — the
    organization, the board credential, and the claimed handle. On Postgres a
    failure in any of them *deactivates the transaction*: every later statement
    is refused and `COMMIT` becomes a silent `ROLLBACK`. So the recorder that
    exists to make a push failure outlive its response would itself fail, get
    swallowed by the wrapper that stops it replacing the original error, and
    leave nothing behind but a log line.

    SQLite has no such state, so the whole class is invisible to the rest of the
    suite — which is why this lives here and why it is worth the fixture.

    The response staying honest is not the property under test: it already was.
    What is asserted is the durable record, in the one failure mode where losing
    it matters most.
    """
    import asyncio

    from src.domain.board import BoardRegistration, BoardType
    from src.services import ticket_status_service

    engine = pg_world["engine"]
    with SQLSession(engine) as session:
        board = BoardRegistration(
            id=str(uuid4()),
            run_by_user_id=pg_world["user"].id,
            organization_id=pg_world["org"].id,
            project_id=pg_world["project"].id,
            board_name="B",
            board_url="https://linear.app/x/team/B",
            board_type=BoardType.LINEAR,
            board_external_id="team",
        )
        ticket = Ticket(
            summary="aborted",
            organization_id=pg_world["org"].id,
            project_id=pg_world["project"].id,
            status=TicketStatus.TODO,
            board_registration_id=board.id,
            external_ticket_id="B-1",
        )
        session.add(board)
        session.commit()
        session.add(ticket)
        session.commit()
        session.refresh(ticket)
        ticket_id = ticket.id

    scrum = None
    with SQLSession(engine) as session:
        scrum = scrum_service.open_scrum(
            session,
            organization_id=pg_world["org"].id,
            project_id=pg_world["project"].id,
            run_by_user_id=pg_world["user"].id,
            kind=ScrumKind.UPDATE.value,
            started_at="2026-08-19T09:00:00Z",
        )
        scrum_service.replace_picks(
            session,
            scrum=scrum,
            sent=[
                {
                    "ticket_id": ticket_id,
                    "status_at_visit": "todo",
                    "moved_to": TicketStatus.IN_PROGRESS.value,
                }
            ],
        )
        scrum_id = scrum.id

    def _poison(session, *args, **kwargs):
        """Fail the way a real DB error inside the push path fails.

        A bare `raise` would exercise the classification branch and nothing else;
        the point here is the *session state* a DBAPI error leaves behind.
        """
        session.exec(text("SELECT 1 / 0"))

    async def _poison_async(registration, token, session, *args, **kwargs):
        return _poison(session)

    # **Both seams, because both read the database.** `resolve_board_token` calls
    # a Vault `SECURITY DEFINER` function; `build_board_adapter` looks like pure
    # construction but its Jira OAuth branch calls `ensure_fresh_jira_token`,
    # which does its own reads. Covering only the first protected the cheaper
    # half of one hazard and left the other outside the savepoint.
    #
    # **The credential lookup has to be stubbed for the second case**, and this
    # is not a detail. This board has no stored credential, so the real
    # `resolve_board_token` raises `BoardCredentialError` first and `_push`
    # returns before `build_board_adapter` is ever called -- the parametrisation
    # would run the *same* path twice and report two passes. Caught by mutation:
    # moving the adapter build outside the savepoint changed nothing, because
    # nothing reached it.
    if seam == "resolve_board_token":
        monkeypatch.setattr(ticket_status_service, seam, _poison)
    else:
        monkeypatch.setattr(
            ticket_status_service, "resolve_board_token", lambda *a, **k: "tok"
        )
        monkeypatch.setattr(ticket_status_service, seam, _poison_async)

    with SQLSession(engine) as session:
        scrum = session.get(Scrum, scrum_id)
        actor = session.get(User, pg_world["user"].id)
        answer = asyncio.run(
            scrum_service.apply_recorded_moves(session, scrum=scrum, actor=actor)
        )

    assert answer["pushed"] is False
    assert answer["errors"]
    with SQLSession(engine) as session:
        visit = session.exec(
            select(ScrumTicketVisit).where(ScrumTicketVisit.scrum_id == scrum_id)
        ).one()
        assert visit.push_error, (
            "the aborted transaction swallowed the only durable record of the failure"
        )
    with SQLSession(engine) as session:
        assert session.get(Ticket, ticket_id).status == TicketStatus.IN_PROGRESS
