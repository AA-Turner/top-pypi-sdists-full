"""A hotfix is a release you can plan tickets into before you cut it.

A hotfix is a release that moves the **Z** in ``vX.Y.Z`` instead of the Y. Until
this existed, such a version had no record until the moment of cutting -- the
release engine computed it by scanning GitHub tags and posted a `released` row --
so there was nothing to drag a ticket onto and every hotfix shipped with no
tickets and an empty changelog.

Making the version openable in advance is one line of work. Making it *survive*
is the rest, and that is what these tests hold down: the pipeline rules were all
written for a single queue of forward minors, and each of them, meeting a patch
row for the first time, does something destructive.

* ``reconcile_statuses`` puts the lowest open version in progress, and a patch of
  the last released line is lower than either forward minor -- so ``v1.9.1``
  would take over from ``v1.10.0`` simply by existing.
* ``ensure_pipeline`` archives anything open beyond two, so opening a hotfix
  would silently destroy the planned minor above it -- not at the moment anyone
  asked for it, but hours later on a background repository sync.
* ``_advance_release_pipeline`` fires on any release becoming RELEASED, and its
  backlog promotion reads slot 1 rather than what shipped -- so a one-line fix
  going out on ``v1.9.1`` would drag the whole of ``v1.10.0``'s backlog into
  todo.

Refs havilandsoftware/innoday#759 (P2), havilandsoftware/innoday-blastoff#31.
"""

from unittest.mock import patch
from uuid import uuid4

import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, select

from src.api.app import app
from src.database import get_session
from src.domain.organization import Organization
from src.domain.project import Project
from src.domain.release import Release, ReleaseStatus
from src.domain.ticket import Ticket, TicketStatus
from src.domain.user import User, UserRole
from src.services.release_planning import (
    ensure_pipeline,
    hotfix_releases,
    is_hotfix,
    next_release,
    outstanding_releases,
    reconcile_statuses,
    release_being_cut,
)
from src.services.ticket_release import resolve_ticket_release
from tests.auth_helpers import bearer_for
from tests.db_helpers import build_test_engine


def _r(version: str, status: ReleaseStatus = ReleaseStatus.PLANNED) -> Release:
    return Release(
        organization_id="org", project_id="proj", version=version, status=status
    )


def _shape(releases):
    """Every row's status, keyed by version -- the whole picture, not a sample.

    Asserting the complete shape rather than the one row a test is about is the
    point: the failures this file exists to prevent are all collateral damage to
    a *different* row than the one being changed.
    """
    return {release.version: release.status for release in releases}


def _settled(releases):
    """Apply ``ensure_pipeline``, creating the rows it asks for, and report the
    shape that results. Mirrors what the sync and the release router both do with
    its return value."""
    for version, status in ensure_pipeline(releases):
        releases.append(_r(version, status))
    return _shape(releases)


# --------------------------------------------------------------------------- #
# What counts as a hotfix
# --------------------------------------------------------------------------- #


def test_the_track_is_patches_of_the_highest_released_line():
    """v1.9.0 shipped, so v1.9.1 is a hotfix of it. v1.10.0 is not -- it moves
    the Y, which is the pipeline's own job."""
    releases = [
        _r("v1.9.0", ReleaseStatus.RELEASED),
        _r("v1.9.1"),
        _r("v1.10.0", ReleaseStatus.IN_PROGRESS),
        _r("v1.11.0"),
    ]
    assert [r.version for r in hotfix_releases(releases)] == ["v1.9.1"]


def test_several_patches_on_the_line_are_all_on_the_track_lowest_first():
    releases = [
        _r("v1.9.0", ReleaseStatus.RELEASED),
        _r("v1.9.2"),
        _r("v1.9.1"),
    ]
    assert [r.version for r in hotfix_releases(releases)] == ["v1.9.1", "v1.9.2"]


def test_a_patch_on_an_older_line_is_not_on_the_track():
    """The project has already shipped v1.10.0, so v1.9.1 is a release out of
    chronology -- there is no hotfix to cut there. Documented in
    ``hotfix_releases``: it stays subject to the ordinary below-the-high-water
    rule, which is what it was subject to before this track existed."""
    releases = [
        _r("v1.9.0", ReleaseStatus.RELEASED),
        _r("v1.10.0", ReleaseStatus.RELEASED),
        _r("v1.9.1"),
    ]
    assert hotfix_releases(releases) == []


def test_a_project_with_nothing_released_has_no_line_to_patch():
    releases = [_r("v0.1.0", ReleaseStatus.IN_PROGRESS), _r("v0.1.1")]
    assert hotfix_releases(releases) == []


def test_a_project_on_no_versioning_line_at_all_has_no_track():
    """`rancher-FINAL` is not a version and cannot be patched."""
    assert hotfix_releases([_r("rancher-FINAL", ReleaseStatus.RELEASED)]) == []


@pytest.mark.parametrize(
    "version,expected",
    [
        ("v1.9.1", True),
        ("v1.9.2", True),
        ("v1.9.0", False),  # Opens a line rather than patching one.
        ("v1.10.0", False),
        ("v2.0.1", False),  # No v2.0.0 on record: not fixing anything.
        ("rancher-FINAL", False),
    ],
)
def test_is_hotfix_asks_whether_the_line_below_already_shipped(version, expected):
    """The question ``hotfix_releases`` asks, but about a version that has since
    been released -- at which point it is the high-water mark itself."""
    history = [
        _r("v1.9.0", ReleaseStatus.RELEASED),
        _r("v1.9.1", ReleaseStatus.RELEASED),
        _r("v1.9.2", ReleaseStatus.RELEASED),
        _r("v1.10.0", ReleaseStatus.RELEASED),
    ]
    assert is_hotfix(version, history) is expected


# --------------------------------------------------------------------------- #
# reconcile_statuses stops collapsing the track
# --------------------------------------------------------------------------- #


def test_a_hotfix_does_not_take_over_as_the_version_in_progress():
    """The bug this rule change exists for. v1.9.1 is the lowest thing ahead of
    the high-water mark, so the "you ship in order" rule made it slot 1 and
    demoted the minor the project was actually cutting."""
    releases = [
        _r("v1.9.0", ReleaseStatus.RELEASED),
        _r("v1.9.1"),
        _r("v1.10.0", ReleaseStatus.IN_PROGRESS),
        _r("v1.11.0"),
    ]
    reconcile_statuses(releases)
    assert _shape(releases) == {
        "v1.9.0": ReleaseStatus.RELEASED,
        "v1.9.1": ReleaseStatus.PLANNED,
        "v1.10.0": ReleaseStatus.IN_PROGRESS,
        "v1.11.0": ReleaseStatus.PLANNED,
    }


def test_a_hotfix_row_is_never_in_progress():
    """IN_PROGRESS names one thing on a project: the version blastoff cuts next.
    A hotfix is asked for by name, not reached by working down the queue, so the
    track is pinned PLANNED and the minor keeps the slot."""
    releases = [
        _r("v1.9.0", ReleaseStatus.RELEASED),
        _r("v1.9.1", ReleaseStatus.IN_PROGRESS),
        _r("v1.10.0", ReleaseStatus.IN_PROGRESS),
    ]
    changed = reconcile_statuses(releases)
    assert changed == 1
    assert _shape(releases)["v1.9.1"] == ReleaseStatus.PLANNED
    assert _shape(releases)["v1.10.0"] == ReleaseStatus.IN_PROGRESS


def test_a_hotfix_is_not_closed_out_as_history():
    """It is above the high-water mark, so rule 1 must not reach it either."""
    releases = [_r("v1.9.0", ReleaseStatus.RELEASED), _r("v1.9.1")]
    reconcile_statuses(releases)
    assert _shape(releases)["v1.9.1"] == ReleaseStatus.PLANNED


def test_a_patch_on_an_older_line_is_still_treated_as_history():
    """The documented answer to "what if someone opens a patch on a line the
    project has moved past". Unchanged behaviour: below the high-water mark is
    history someone forgot to close, whatever digit moved."""
    releases = [
        _r("v1.9.0", ReleaseStatus.RELEASED),
        _r("v1.10.0", ReleaseStatus.RELEASED),
        _r("v1.9.1"),
    ]
    reconcile_statuses(releases)
    assert _shape(releases)["v1.9.1"] == ReleaseStatus.RELEASED


def test_reconcile_is_idempotent_with_a_hotfix_open():
    releases = [
        _r("v1.9.0", ReleaseStatus.RELEASED),
        _r("v1.9.1"),
        _r("v1.10.0", ReleaseStatus.IN_PROGRESS),
        _r("v1.11.0"),
    ]
    reconcile_statuses(releases)
    assert reconcile_statuses(releases) == 0


def test_the_next_release_is_still_the_minor_while_a_hotfix_is_open():
    releases = [
        _r("v1.9.0", ReleaseStatus.RELEASED),
        _r("v1.9.1"),
        _r("v1.10.0", ReleaseStatus.IN_PROGRESS),
    ]
    reconcile_statuses(releases)
    assert next_release(releases).version == "v1.10.0"
    assert release_being_cut(releases).version == "v1.10.0"


# --------------------------------------------------------------------------- #
# The two forward slots are undisturbed
# --------------------------------------------------------------------------- #


def test_opening_a_hotfix_does_not_archive_the_planned_minor():
    """The destructive one. Three rows are open, the cap is two, and the row
    ``ensure_pipeline`` would have archived for being third is the minor a whole
    release of tickets is planned into."""
    releases = [
        _r("v1.9.0", ReleaseStatus.RELEASED),
        _r("v1.9.1"),
        _r("v1.10.0", ReleaseStatus.IN_PROGRESS),
        _r("v1.11.0"),
    ]
    assert _settled(releases) == {
        "v1.9.0": ReleaseStatus.RELEASED,
        "v1.9.1": ReleaseStatus.PLANNED,
        "v1.10.0": ReleaseStatus.IN_PROGRESS,
        "v1.11.0": ReleaseStatus.PLANNED,
    }


def test_a_hotfix_does_not_count_as_a_slot():
    """With only a hotfix open, the project still has no minor in flight and both
    slots must be opened above the line it shipped -- not one, and not off the
    patch."""
    releases = [_r("v1.9.0", ReleaseStatus.RELEASED), _r("v1.9.1")]
    assert _settled(releases) == {
        "v1.9.0": ReleaseStatus.RELEASED,
        "v1.9.1": ReleaseStatus.PLANNED,
        "v1.10.0": ReleaseStatus.IN_PROGRESS,
        "v1.11.0": ReleaseStatus.PLANNED,
    }


def test_two_hotfixes_at_once_still_leave_the_slots_alone():
    releases = [
        _r("v1.9.0", ReleaseStatus.RELEASED),
        _r("v1.9.1"),
        _r("v1.9.2"),
        _r("v1.10.0", ReleaseStatus.IN_PROGRESS),
        _r("v1.11.0"),
    ]
    assert _settled(releases) == {
        "v1.9.0": ReleaseStatus.RELEASED,
        "v1.9.1": ReleaseStatus.PLANNED,
        "v1.9.2": ReleaseStatus.PLANNED,
        "v1.10.0": ReleaseStatus.IN_PROGRESS,
        "v1.11.0": ReleaseStatus.PLANNED,
    }


def test_ensure_pipeline_is_idempotent_with_a_hotfix_open():
    releases = [
        _r("v1.9.0", ReleaseStatus.RELEASED),
        _r("v1.9.1"),
        _r("v1.10.0", ReleaseStatus.IN_PROGRESS),
        _r("v1.11.0"),
    ]
    _settled(releases)
    assert ensure_pipeline(releases) == []


def test_two_patches_in_a_row():
    """v1.9.1 ships; v1.9.2 is opened on the same line. The track moves up with
    the high-water mark and the minors never notice either of them."""
    releases = [
        _r("v1.9.0", ReleaseStatus.RELEASED),
        _r("v1.9.1", ReleaseStatus.RELEASED),
        _r("v1.9.2"),
        _r("v1.10.0", ReleaseStatus.IN_PROGRESS),
        _r("v1.11.0"),
    ]
    assert [r.version for r in hotfix_releases(releases)] == ["v1.9.2"]
    assert _settled(releases) == {
        "v1.9.0": ReleaseStatus.RELEASED,
        "v1.9.1": ReleaseStatus.RELEASED,
        "v1.9.2": ReleaseStatus.PLANNED,
        "v1.10.0": ReleaseStatus.IN_PROGRESS,
        "v1.11.0": ReleaseStatus.PLANNED,
    }


def test_with_nothing_released_a_patch_is_an_ordinary_forward_version():
    """The documented answer to "a patch on a project that has never shipped".
    There is no line to fix, so v0.1.1 is not a hotfix and gets no exemption --
    it competes for the two slots like any other version, and v0.2.0 is archived
    for being third. Nothing has shipped, so the version to open is simply the
    one you intend to cut."""
    releases = [
        _r("v0.1.0", ReleaseStatus.IN_PROGRESS),
        _r("v0.1.1"),
        _r("v0.2.0"),
    ]
    assert _settled(releases) == {
        "v0.1.0": ReleaseStatus.IN_PROGRESS,
        "v0.1.1": ReleaseStatus.PLANNED,
        "v0.2.0": ReleaseStatus.ARCHIVED,
    }


def test_a_project_with_no_hotfix_is_exactly_as_it_was():
    """The rule change is additive. A project with no patch row anywhere must
    settle to the shape it settled to before this file existed."""
    releases = [_r("v1.9.0", ReleaseStatus.RELEASED)]
    assert _settled(releases) == {
        "v1.9.0": ReleaseStatus.RELEASED,
        "v1.10.0": ReleaseStatus.IN_PROGRESS,
        "v1.11.0": ReleaseStatus.PLANNED,
    }


# --------------------------------------------------------------------------- #
# Tickets plan into a hotfix exactly as into a minor
# --------------------------------------------------------------------------- #


def test_a_hotfix_is_offered_by_the_picker():
    """The ticket-to-release join is a version-string match with no notion of
    which digit moved, so this needed nothing new -- but it is the whole point of
    the feature, so it is pinned."""
    releases = [
        _r("v1.9.0", ReleaseStatus.RELEASED),
        _r("v1.9.1"),
        _r("v1.10.0", ReleaseStatus.IN_PROGRESS),
        _r("v1.11.0"),
    ]
    reconcile_statuses(releases)
    assert [r.version for r in outstanding_releases(releases)] == [
        "v1.10.0",
        "v1.9.1",
        "v1.11.0",
    ]


# --------------------------------------------------------------------------- #
# Through the API
# --------------------------------------------------------------------------- #


@pytest.fixture
def db_engine():
    engine = build_test_engine()
    yield engine
    engine.dispose()


@pytest.fixture
def db_session(db_engine):
    with Session(db_engine) as session:
        yield session


@pytest.fixture
def client(db_engine):
    def override_get_session():
        with Session(db_engine) as session:
            yield session

    app.dependency_overrides[get_session] = override_get_session
    with patch("src.api.app._assert_schema_at_head"):
        with TestClient(app) as c:
            yield c
    app.dependency_overrides.clear()


@pytest.fixture
def org(db_session):
    o = Organization(id=str(uuid4()), name="Hotfix Org")
    db_session.add(o)
    db_session.commit()
    db_session.refresh(o)
    return o


@pytest.fixture
def project(db_session, org):
    p = Project(
        id=str(uuid4()),
        organization_id=org.id,
        alias=f"H{str(uuid4())[:6]}".upper(),
        name="Hotfix Project",
        description="A project with a line to patch",
    )
    db_session.add(p)
    db_session.commit()
    db_session.refresh(p)
    return p


@pytest.fixture
def user(db_session, org):
    u = User(
        id=str(uuid4()),
        email="hotfix@example.com",
        full_name="Hotfix User",
        role=UserRole.MEMBER,
        is_platform_member=True,
    )
    db_session.add(u)
    db_session.commit()
    db_session.refresh(u)
    return u


@pytest.fixture
def auth_headers(user, db_session):
    return bearer_for(db_session, user.id)


@pytest.fixture
def shipped_line(db_session, org, project):
    """v1.9.0 released, v1.10.0 being cut, v1.11.0 being filled -- the state a
    real project is in when somebody needs a hotfix."""
    rows = [
        Release(
            id=str(uuid4()),
            organization_id=org.id,
            project_id=project.id,
            version="v1.9.0",
            status=ReleaseStatus.RELEASED,
        ),
        Release(
            id=str(uuid4()),
            organization_id=org.id,
            project_id=project.id,
            version="v1.10.0",
            status=ReleaseStatus.IN_PROGRESS,
        ),
        Release(
            id=str(uuid4()),
            organization_id=org.id,
            project_id=project.id,
            version="v1.11.0",
            status=ReleaseStatus.PLANNED,
        ),
    ]
    for row in rows:
        db_session.add(row)
    db_session.commit()
    return {row.version: row.id for row in rows}


def _pipeline(db_engine, project_id):
    """Read the whole release shape back from a session of its own -- the request
    ran in a different one, so the test session's identity map would report the
    rows as they were before the handler touched them."""
    with Session(db_engine) as fresh:
        rows = fresh.exec(select(Release).where(Release.project_id == project_id)).all()
        return {r.version: r.status for r in rows}


def test_opening_a_hotfix_is_accepted_and_disturbs_nothing(
    client, org, project, db_engine, auth_headers, shipped_line
):
    """`innoday releases create v1.9.1` on a project that shipped v1.9.0."""
    resp = client.post(
        f"/api/v1/organizations/{org.id}/releases",
        json={"project_id": project.id, "version": "v1.9.1"},
        headers=auth_headers,
    )
    assert resp.status_code in (200, 201)
    assert resp.json()["status"] == "planned"

    assert _pipeline(db_engine, project.id) == {
        "v1.9.0": ReleaseStatus.RELEASED,
        "v1.9.1": ReleaseStatus.PLANNED,
        "v1.10.0": ReleaseStatus.IN_PROGRESS,
        "v1.11.0": ReleaseStatus.PLANNED,
    }


def test_a_ticket_plans_into_a_hotfix(
    client, org, project, db_session, auth_headers, shipped_line
):
    db_session.add(
        Release(
            id=str(uuid4()),
            organization_id=org.id,
            project_id=project.id,
            version="v1.9.1",
            status=ReleaseStatus.PLANNED,
        )
    )
    db_session.commit()

    assert (
        resolve_ticket_release(
            db_session,
            organization_id=org.id,
            project_id=project.id,
            value="v1.9.1",
        )
        == "v1.9.1"
    )


def test_shipping_a_hotfix_does_not_rotate_the_minor_pipeline(
    client, org, project, db_session, db_engine, auth_headers, shipped_line
):
    """v1.10.0 stays in flight and v1.11.0 stays planned. Nothing is promoted and
    no fourth version is opened -- the pipeline was never cutting v1.9.1."""
    hotfix = Release(
        id=str(uuid4()),
        organization_id=org.id,
        project_id=project.id,
        version="v1.9.1",
        status=ReleaseStatus.PLANNED,
    )
    db_session.add(hotfix)
    db_session.commit()

    resp = client.patch(
        f"/api/v1/organizations/{org.id}/releases/{hotfix.id}",
        json={"status": "released"},
        headers=auth_headers,
    )
    assert resp.status_code == 200

    assert _pipeline(db_engine, project.id) == {
        "v1.9.0": ReleaseStatus.RELEASED,
        "v1.9.1": ReleaseStatus.RELEASED,
        "v1.10.0": ReleaseStatus.IN_PROGRESS,
        "v1.11.0": ReleaseStatus.PLANNED,
    }


def test_shipping_a_hotfix_does_not_drag_the_next_minors_backlog_into_todo(
    client, org, project, db_session, db_engine, auth_headers, shipped_line
):
    """The damage a rotation would actually do. The backlog promotion reads slot
    1 rather than what shipped, so a one-line fix going out on v1.9.1 would have
    started the whole of v1.10.0."""
    deferred = Ticket(
        summary="deferred to the next minor",
        organization_id=org.id,
        project_id=project.id,
        status=TicketStatus.BACKLOG,
        release="v1.10.0",
    )
    db_session.add(deferred)
    hotfix = Release(
        id=str(uuid4()),
        organization_id=org.id,
        project_id=project.id,
        version="v1.9.1",
        status=ReleaseStatus.PLANNED,
    )
    db_session.add(hotfix)
    db_session.commit()
    ticket_id = deferred.id

    resp = client.patch(
        f"/api/v1/organizations/{org.id}/releases/{hotfix.id}",
        json={"status": "released"},
        headers=auth_headers,
    )
    assert resp.status_code == 200

    with Session(db_engine) as fresh:
        still_deferred = fresh.get(Ticket, ticket_id)
        assert still_deferred.status == TicketStatus.BACKLOG


def test_two_hotfixes_in_a_row_through_the_api(
    client, org, project, db_engine, auth_headers, shipped_line
):
    """v1.9.1 ships, then v1.9.2 is opened on the same line and ships too. The
    minors are untouched throughout and the second patch is recognised as a
    hotfix of the first."""
    for version in ("v1.9.1", "v1.9.2"):
        opened = client.post(
            f"/api/v1/organizations/{org.id}/releases",
            json={"project_id": project.id, "version": version},
            headers=auth_headers,
        )
        assert opened.status_code in (200, 201)

        shipped = client.patch(
            f"/api/v1/organizations/{org.id}/releases/{opened.json()['id']}",
            json={"status": "released"},
            headers=auth_headers,
        )
        assert shipped.status_code == 200

    assert _pipeline(db_engine, project.id) == {
        "v1.9.0": ReleaseStatus.RELEASED,
        "v1.9.1": ReleaseStatus.RELEASED,
        "v1.9.2": ReleaseStatus.RELEASED,
        "v1.10.0": ReleaseStatus.IN_PROGRESS,
        "v1.11.0": ReleaseStatus.PLANNED,
    }


def test_shipping_the_minor_still_rotates(
    client, org, project, db_session, db_engine, auth_headers, shipped_line
):
    """The exemption is narrow. With a hotfix open beside it, v1.10.0 shipping
    still promotes v1.11.0 and opens v1.12.0 -- and the hotfix row, now below the
    high-water mark, is closed out as the history it has become."""
    db_session.add(
        Release(
            id=str(uuid4()),
            organization_id=org.id,
            project_id=project.id,
            version="v1.9.1",
            status=ReleaseStatus.PLANNED,
        )
    )
    db_session.commit()

    resp = client.patch(
        f"/api/v1/organizations/{org.id}/releases/{shipped_line['v1.10.0']}",
        json={"status": "released"},
        headers=auth_headers,
    )
    assert resp.status_code == 200

    assert _pipeline(db_engine, project.id) == {
        "v1.9.0": ReleaseStatus.RELEASED,
        "v1.9.1": ReleaseStatus.RELEASED,
        "v1.10.0": ReleaseStatus.RELEASED,
        "v1.11.0": ReleaseStatus.IN_PROGRESS,
        "v1.12.0": ReleaseStatus.PLANNED,
    }
