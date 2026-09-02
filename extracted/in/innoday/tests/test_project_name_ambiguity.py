"""`resolve_project` refuses an ambiguous name instead of picking one.

`projects.id` is a primary key and `uq_project_org_alias` covers
`(organization_id, alias)`. **`projects.name` has no constraint at all**, so two
projects in one org may share a name — and the resolver's third branch was a
plain `.first()` on an unordered query. With two projects called "Platform" the
answer was whichever row Postgres happened to return, and nothing anywhere
recorded that a choice had been made.

Twenty-nine call sites read `resolve_project`. A silent arbitrary pick means a
ticket created against, a board registered for, or a summary written about the
wrong project.

No duplicate names existed when this was written — measured: zero duplicates,
and zero names colliding with another project's alias. This disarms the trap
before it arms itself, which is also why the tests below have to *construct* the
collision rather than find one.
"""

from __future__ import annotations

from uuid import uuid4

import pytest
from fastapi import HTTPException
from sqlmodel import Session

from src.domain.organization import Organization
from src.domain.project import Project
from src.routers.projects import resolve_project
from tests.db_helpers import build_test_engine


@pytest.fixture
def session():
    with Session(build_test_engine()) as s:
        yield s


@pytest.fixture
def org(session):
    o = Organization(id=str(uuid4()), name="Org", alias=f"o{uuid4().hex[:8]}")
    session.add(o)
    session.commit()
    return o


def _project(session, org, *, alias: str, name: str) -> Project:
    p = Project(
        id=str(uuid4()),
        organization_id=org.id,
        alias=alias,
        name=name,
        description="",
    )
    session.add(p)
    session.commit()
    return p


class TestUniqueLookupsStillWin:
    """Id and alias are constrained, so they resolve without ceremony."""

    def test_by_id(self, session, org):
        p = _project(session, org, alias="ALPHA", name="Alpha")
        assert resolve_project(p.id, org.id, session).id == p.id

    def test_by_alias_case_insensitively(self, session, org):
        p = _project(session, org, alias="ALPHA", name="Alpha")
        assert resolve_project("alpha", org.id, session).id == p.id

    def test_by_name_when_it_is_unambiguous(self, session, org):
        """The convenience is kept — only the ambiguous case changes."""
        p = _project(session, org, alias="ALPHA", name="Team Alpha")
        assert resolve_project("team alpha", org.id, session).id == p.id

    def test_an_alias_beats_another_project_s_name(self, session, org):
        """Order is the guarantee: the constrained match wins.

        Otherwise naming one project after another's alias would let the
        unconstrained branch answer first.
        """
        aliased = _project(session, org, alias="PLATFORM", name="Alpha")
        _project(session, org, alias="BETA", name="Platform")
        assert resolve_project("PLATFORM", org.id, session).id == aliased.id


class TestAmbiguousName:
    def test_two_projects_sharing_a_name_raise_409(self, session, org):
        _project(session, org, alias="ONE", name="Platform")
        _project(session, org, alias="TWO", name="Platform")

        with pytest.raises(HTTPException) as exc:
            resolve_project("Platform", org.id, session)

        assert exc.value.status_code == 409

    def test_the_error_names_the_aliases_to_disambiguate_with(self, session, org):
        """A refusal the caller cannot act on is barely better than a wrong answer."""
        _project(session, org, alias="ONE", name="Platform")
        _project(session, org, alias="TWO", name="Platform")

        with pytest.raises(HTTPException) as exc:
            resolve_project("platform", org.id, session)

        detail = exc.value.detail
        assert "ONE" in detail and "TWO" in detail
        assert "alias" in detail.lower()

    def test_a_duplicate_name_in_another_org_is_not_ambiguity(self, session, org):
        """Scoping comes first: another tenant's project is not a candidate."""
        other = Organization(id=str(uuid4()), name="Other", alias=f"x{uuid4().hex[:8]}")
        session.add(other)
        session.commit()
        mine = _project(session, org, alias="ONE", name="Platform")
        _project(session, other, alias="TWO", name="Platform")

        assert resolve_project("Platform", org.id, session).id == mine.id

    def test_the_refusal_is_reproducible(self, session, org):
        """Same input, same message — the candidate list is ordered.

        An unordered listing would name the aliases in a different order each
        time, which makes the error look like two different errors.
        """
        _project(session, org, alias="ZULU", name="Platform")
        _project(session, org, alias="ALPHA", name="Platform")

        details = []
        for _ in range(3):
            with pytest.raises(HTTPException) as exc:
                resolve_project("Platform", org.id, session)
            details.append(exc.value.detail)

        assert len(set(details)) == 1, details
        assert details[0].index("ALPHA") < details[0].index("ZULU")


def test_a_missing_project_is_still_a_404(session, org):
    with pytest.raises(HTTPException) as exc:
        resolve_project("nothing-like-this", org.id, session)
    assert exc.value.status_code == 404
