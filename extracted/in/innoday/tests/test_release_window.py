"""The window a release covers is derived, not typed.

`innoday releases content` required the start date as an argument. A date
nineteen days early -- typed by hand, from memory, against a release that
shipped on the 12th -- produced a report claiming 93 merged pull requests
instead of 34, twenty-one tickets wrongly flagged as shipped outside a release,
and two pull requests attributed to a ticket they did not belong to.

Nothing caught it. Every number was internally consistent and confidently wrong,
and `blastoff --dry-run` printed the right ones from the same data at the same
moment, because it derives the boundary instead of accepting one.

So the platform computes it. A caller may still override, and the payload says
which kind of answer it is.
"""

from __future__ import annotations

from datetime import datetime, timezone
from uuid import uuid4

import pytest
from sqlmodel import Session

from src.domain.organization import Organization
from src.domain.project import Project
from src.domain.release import Release, ReleaseStatus
from src.services.release_content import resolve_window
from tests.db_helpers import build_test_engine

SHIPPED_AT = datetime(2026, 8, 12, tzinfo=timezone.utc)


@pytest.fixture
def world():
    engine = build_test_engine()
    with Session(engine) as session:
        org = Organization(id=str(uuid4()), name="Acme", alias=f"a{str(uuid4())[:5]}")
        session.add(org)
        project = Project(
            id=str(uuid4()),
            organization_id=org.id,
            alias="BPAI",
            name="Bright Power",
            description="d",
        )
        session.add(project)
        session.commit()
        yield session, org, project


def _release(session, org, project, version, status, released_at=None):
    r = Release(
        organization_id=org.id,
        project_id=project.id,
        version=version,
        status=status,
        released_at=released_at,
    )
    session.add(r)
    session.commit()
    return r


def _resolve(session, org, project, **kwargs):
    return resolve_window(
        session, organization_id=org.id, project_id=project.id, **kwargs
    )


class TestItComesFromTheLastShippedRelease:
    def test_the_boundary_is_the_previous_release_date(self, world):
        session, org, project = world
        _release(session, org, project, "v1.10.0", ReleaseStatus.RELEASED, SHIPPED_AT)
        _release(session, org, project, "v1.11.0", ReleaseStatus.IN_PROGRESS)

        window = _resolve(session, org, project)
        assert window.since == SHIPPED_AT
        assert window.previous_version == "v1.10.0"
        assert window.source == "derived"
        assert window.warning is None

    def test_the_label_names_the_release_and_the_date(self, world):
        """It is printed on the report, so it has to describe the real boundary."""
        session, org, project = world
        _release(session, org, project, "v1.10.0", ReleaseStatus.RELEASED, SHIPPED_AT)
        assert _resolve(session, org, project).label == "since v1.10.0 (2026-08-12)"

    def test_an_unreleased_row_is_not_a_boundary(self, world):
        """A planned or in-flight release has shipped nothing to measure from.

        Using `next_release` here would pick exactly such a row, whose
        `released_at` is `None` by definition -- an unbounded window dressed up
        as a derived one.
        """
        session, org, project = world
        _release(session, org, project, "v1.10.0", ReleaseStatus.RELEASED, SHIPPED_AT)
        _release(session, org, project, "v1.12.0", ReleaseStatus.PLANNED)
        _release(session, org, project, "v1.11.0", ReleaseStatus.IN_PROGRESS)

        assert _resolve(session, org, project).previous_version == "v1.10.0"

    def test_it_ranks_by_semver_not_by_date(self, world):
        """Several repos publish one cross-repo version minutes apart, so the
        highest version is a steadier answer than the latest stamp."""
        session, org, project = world
        _release(session, org, project, "v1.10.0", ReleaseStatus.RELEASED, SHIPPED_AT)
        _release(
            session,
            org,
            project,
            "v1.9.0",
            ReleaseStatus.RELEASED,
            datetime(2026, 8, 20, tzinfo=timezone.utc),
        )
        assert _resolve(session, org, project).previous_version == "v1.10.0"


class TestWhenItCannotBeDerived:
    def test_no_previous_release_is_unbounded_and_says_so(self, world):
        """A first release legitimately has nothing behind it."""
        session, org, project = world
        window = _resolve(session, org, project)
        assert window.since is None
        assert window.source == "derived"
        assert "no previous release" in window.label
        assert window.warning is None

    def test_a_released_row_with_no_date_warns(self, world):
        """The same failure, arriving from the data instead of a keyboard.

        Treating a missing date as "since the beginning of time" is how a
        release comes to report the whole history as its contents. It stays
        unbounded -- there is nothing else it could be -- but it is never quiet
        about it.
        """
        session, org, project = world
        _release(session, org, project, "v1.10.0", ReleaseStatus.RELEASED, None)

        window = _resolve(session, org, project)
        assert window.since is None
        assert window.previous_version == "v1.10.0"
        assert window.warning is not None
        assert "no release date" in window.warning


class TestOverrideStaysPossible:
    def test_a_supplied_boundary_wins(self, world):
        session, org, project = world
        _release(session, org, project, "v1.10.0", ReleaseStatus.RELEASED, SHIPPED_AT)
        asked = datetime(2026, 7, 24, tzinfo=timezone.utc)

        window = _resolve(session, org, project, since=asked)
        assert window.since == asked

    def test_a_supplied_boundary_is_marked_as_such(self, world):
        """The distinction the payload exists to carry.

        A boundary the platform computed from its own release records is a
        different kind of claim from one somebody passed in, and the reader of a
        release report should be able to tell them apart.
        """
        session, org, project = world
        _release(session, org, project, "v1.10.0", ReleaseStatus.RELEASED, SHIPPED_AT)
        supplied = _resolve(
            session, org, project, since=datetime(2026, 7, 24, tzinfo=timezone.utc)
        )
        derived = _resolve(session, org, project)
        assert supplied.source == "supplied"
        assert derived.source == "derived"

    def test_the_payload_shape_is_serialisable(self, world):
        session, org, project = world
        _release(session, org, project, "v1.10.0", ReleaseStatus.RELEASED, SHIPPED_AT)
        block = _resolve(session, org, project).as_dict()
        assert set(block) == {
            "since",
            "until",
            "previous_version",
            "label",
            "source",
        }
        assert block["since"].startswith("2026-08-12")


class TestTheBoundaryCanBeComparedToGitHub:
    """A naive boundary is a crash, not a wrong answer, and it is easy to ship.

    `released_at` is a plain `DateTime` in both dialects, so it round-trips
    without a timezone. GitHub's `merged_at` is parsed as aware. Comparing the
    two raises `TypeError: can't compare offset-naive and offset-aware
    datetimes` part-way through assembling a release -- and the supplied path
    never hits it, because an ISO string is parsed aware, so the bug hides until
    the derived path runs.
    """

    def test_a_derived_boundary_is_timezone_aware(self, world):
        session, org, project = world
        _release(session, org, project, "v1.10.0", ReleaseStatus.RELEASED, SHIPPED_AT)
        assert _resolve(session, org, project).since.tzinfo is not None

    def test_it_can_be_compared_with_a_github_timestamp(self, world):
        from src.utils.time_windows import parse_iso_utc

        session, org, project = world
        _release(session, org, project, "v1.10.0", ReleaseStatus.RELEASED, SHIPPED_AT)
        since = _resolve(session, org, project).since
        merged_at = parse_iso_utc("2026-08-20T00:00:00Z")
        assert merged_at >= since


class TestNamingAVersionThatHasAlreadyShipped:
    """The window has to follow the version, or the answer is a different release.

    Found an hour after BPAI v1.11.0 went out. `innoday releases content
    v1.11.0` -- the exact invocation the summary skill documents for
    summarising a release other than the one in flight -- returned its ten
    tickets against a window that opened at 14:12 that afternoon, which is when
    v1.11.0 *ended*. Zero merged pull requests. Every ticket flagged as having
    no code behind it.

    Nothing about that output looked broken: ten real tickets, a stated window,
    `source: derived`. It was the same failure the derived boundary was built to
    prevent, arriving from the version argument instead of the keyboard.
    """

    def test_the_window_opens_at_the_release_behind_the_named_one(self, world):
        session, org, project = world
        _release(session, org, project, "v1.10.0", ReleaseStatus.RELEASED, SHIPPED_AT)
        _release(
            session,
            org,
            project,
            "v1.11.0",
            ReleaseStatus.RELEASED,
            datetime(2026, 8, 25, tzinfo=timezone.utc),
        )

        window = _resolve(session, org, project, version="v1.11.0")

        assert window.previous_version == "v1.10.0"
        assert window.since == SHIPPED_AT
        assert window.source == "derived"

    def test_the_window_closes_when_the_named_version_shipped(self, world):
        session, org, project = world
        shipped = datetime(2026, 8, 25, tzinfo=timezone.utc)
        _release(session, org, project, "v1.10.0", ReleaseStatus.RELEASED, SHIPPED_AT)
        _release(session, org, project, "v1.11.0", ReleaseStatus.RELEASED, shipped)

        window = _resolve(session, org, project, version="v1.11.0")

        assert window.until == shipped
        assert window.as_dict()["until"] == shipped.isoformat()

    def test_the_label_names_both_ends(self, world):
        session, org, project = world
        _release(session, org, project, "v1.10.0", ReleaseStatus.RELEASED, SHIPPED_AT)
        _release(
            session,
            org,
            project,
            "v1.11.0",
            ReleaseStatus.RELEASED,
            datetime(2026, 8, 25, tzinfo=timezone.utc),
        )

        window = _resolve(session, org, project, version="v1.11.0")

        assert window.label == "v1.10.0 → v1.11.0"

    def test_the_release_in_flight_still_has_no_closing_boundary(self, world):
        """Naming the version being cut must not change today's answer.

        It is still accumulating, so a closing bound would cut off work that
        belongs to it -- and this is the overwhelmingly common call.
        """
        session, org, project = world
        _release(session, org, project, "v1.10.0", ReleaseStatus.RELEASED, SHIPPED_AT)
        _release(session, org, project, "v1.11.0", ReleaseStatus.IN_PROGRESS)

        window = _resolve(session, org, project, version="v1.11.0")

        assert window.until is None
        assert window.since == SHIPPED_AT
        assert window.label == "since v1.10.0 (2026-08-12)"

    def test_the_first_release_ever_has_nothing_behind_it(self, world):
        """Named, shipped, and nothing before it: unbounded start, bounded end."""
        session, org, project = world
        shipped = datetime(2026, 8, 25, tzinfo=timezone.utc)
        _release(session, org, project, "v1.0.0", ReleaseStatus.RELEASED, shipped)

        window = _resolve(session, org, project, version="v1.0.0")

        assert window.since is None
        assert window.previous_version is None
        assert window.until == shipped

    def test_a_supplied_since_moves_the_start_and_leaves_the_end_alone(self, world):
        """`--since` overrides the window's *start*. That is all it says it does.

        The first version of this shipped the opposite -- an override dropped the
        closing bound too, on the reasoning that a caller's boundary is both ends
        of it. Review of #711, which reached the same fix independently, made the
        better case: the two boundaries answer different questions. Choosing
        where to begin counting is not a statement that a release which shipped
        three weeks ago should keep absorbing everything merged since.
        """
        session, org, project = world
        typed = datetime(2026, 7, 24, tzinfo=timezone.utc)
        shipped = datetime(2026, 8, 25, tzinfo=timezone.utc)
        _release(session, org, project, "v1.10.0", ReleaseStatus.RELEASED, SHIPPED_AT)
        _release(session, org, project, "v1.11.0", ReleaseStatus.RELEASED, shipped)

        window = _resolve(session, org, project, since=typed, version="v1.11.0")

        assert window.source == "supplied"
        assert window.since == typed
        assert window.until == shipped

    def test_the_version_is_matched_by_semver_not_by_spelling(self, world):
        """`1.11.0` and `v1.11.0` are one release.

        A byte-exact lookup finds neither when the caller spells it the other
        way, and "no row" is indistinguishable from "has not shipped" -- which
        leaves the window open, which is the bug.
        """
        session, org, project = world
        shipped = datetime(2026, 8, 25, tzinfo=timezone.utc)
        _release(session, org, project, "v1.10.0", ReleaseStatus.RELEASED, SHIPPED_AT)
        _release(session, org, project, "v1.11.0", ReleaseStatus.RELEASED, shipped)

        window = _resolve(session, org, project, version="1.11.0")

        assert window.until == shipped
        assert window.previous_version == "v1.10.0"
