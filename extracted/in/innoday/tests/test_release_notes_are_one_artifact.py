"""A release's notes and a release-scoped summary are one thing, in one place.

They were two stores of the same prose. `Release.summary` was written at tag
time; a `Summary` row was written by the narrator. Whichever door somebody came
through, they saw the other one's absence -- `releases summarize v1.11.0` showed
notes that `summary --release v1.11.0` reported as "nothing written yet", and a
team reading both could not tell it was one system.

The `Summary` row is canonical: it is the one with items, a fingerprint, an
author and a history. `Release.summary` is a mirror, kept because the release
card and the release API read it. So there are two rules, and they close the loop
in both directions:

* saving a release-scoped summary writes the mirror, and
* reading one with no row yet falls back to the mirror.
"""

from __future__ import annotations

from datetime import datetime, timezone
from uuid import uuid4

import pytest
from sqlmodel import Session, select

from src.domain.organization import Organization
from src.domain.project import Project
from src.domain.release import Release, ReleaseStatus
from src.services.summary_service import mirror_release_notes, release_spec
from tests.db_helpers import build_test_engine

NOTES = "- **New property report** — available end to end.\n  BPAI-334 · shipped"


@pytest.fixture
def world():
    engine = build_test_engine()
    with Session(engine) as session:
        org = Organization(id=str(uuid4()), name="BP", alias=f"b{str(uuid4())[:5]}")
        session.add(org)
        project = Project(
            id=str(uuid4()),
            organization_id=org.id,
            alias="BPAI",
            name="Bright Power AI",
            description="d",
        )
        session.add(project)
        release = Release(
            id=str(uuid4()),
            organization_id=org.id,
            project_id=project.id,
            version="v1.11.0",
            status=ReleaseStatus.RELEASED,
            released_at=datetime(2026, 8, 25, tzinfo=timezone.utc),
        )
        session.add(release)
        session.commit()
        yield session, org, project, release


def _mirror(session, org, project, spec, body=NOTES):
    return mirror_release_notes(
        session,
        organization_id=org.id,
        project_id=project.id,
        window_spec=spec,
        body_markdown=body,
    )


class TestSavingASummaryWritesTheNotes:
    def test_the_release_row_gets_the_prose(self, world):
        session, org, project, release = world
        assert _mirror(session, org, project, release_spec("v1.11.0")) == "v1.11.0"
        session.commit()
        assert session.get(Release, release.id).summary == NOTES

    def test_a_windowed_summary_touches_no_release(self, world):
        """A three-day stand-up is not any release's notes."""
        session, org, project, release = world
        assert _mirror(session, org, project, "3d") is None
        assert release.summary is None

    def test_an_unknown_version_is_not_an_error(self, world):
        """A summary is worth storing even when the mirror cannot be written."""
        session, org, project, _ = world
        assert _mirror(session, org, project, release_spec("v9.9.9")) is None

    def test_empty_prose_does_not_erase_existing_notes(self, world):
        """A regeneration that produced nothing must not clear what stands."""
        session, org, project, release = world
        _mirror(session, org, project, release_spec("v1.11.0"))
        session.commit()
        assert (
            _mirror(session, org, project, release_spec("v1.11.0"), body=None) is None
        )
        assert session.get(Release, release.id).summary == NOTES

    def test_re_saving_replaces_rather_than_appends(self, world):
        session, org, project, release = world
        _mirror(session, org, project, release_spec("v1.11.0"))
        _mirror(session, org, project, release_spec("v1.11.0"), body="- rewritten")
        session.commit()
        assert session.get(Release, release.id).summary == "- rewritten"

    def test_another_projects_release_of_the_same_name_is_untouched(self, world):
        """Versions are unique per project, not per organization."""
        session, org, project, release = world
        other = Project(
            id=str(uuid4()),
            organization_id=org.id,
            alias="BPCL",
            name="BP Cloud",
            description="d",
        )
        session.add(other)
        session.add(
            Release(
                id=str(uuid4()),
                organization_id=org.id,
                project_id=other.id,
                version="v1.11.0",
                status=ReleaseStatus.RELEASED,
                released_at=datetime(2026, 8, 25, tzinfo=timezone.utc),
            )
        )
        session.commit()

        _mirror(session, org, project, release_spec("v1.11.0"))
        session.commit()

        theirs = session.exec(
            select(Release).where(Release.project_id == other.id)
        ).first()
        assert theirs.summary is None
        assert session.get(Release, release.id).summary == NOTES


class TestTheMirrorGateNormalises:
    """`Release:v1.11.0` is a release spec to everything except a raw startswith.

    `persist` canonicalises the spec internally and every other reader goes
    through `is_release_spec`, which strips and lowercases -- so a caller who
    sent a capitalised spec had their summary stored as a release summary while
    the mirror silently declined, and the release card went on saying nothing had
    been written.
    """

    @pytest.mark.parametrize(
        "spec",
        ["release:v1.11.0", "Release:v1.11.0", "RELEASE:v1.11.0", " release:v1.11.0 "],
    )
    def test_every_spelling_mirrors(self, world, spec):
        session, org, project, release = world
        assert _mirror(session, org, project, spec) == "v1.11.0"
        session.commit()
        assert session.get(Release, release.id).summary == NOTES

    def test_a_duration_still_does_not(self, world):
        session, org, project, release = world
        assert _mirror(session, org, project, "3d") is None
        assert release.summary is None
