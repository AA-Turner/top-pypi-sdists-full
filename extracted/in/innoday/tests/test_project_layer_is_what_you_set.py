"""A layer set on a project's link is the layer that project sees.

`repos set-layer bps-ui-demo --layer design` reported success and `repos list`
went on printing `ui`. Both were telling the truth about different columns:
the command writes `project_repositories.layer`, the listing read
`repositories.layer`. A command that appears to do nothing is worse than one
that fails -- the natural next step is to run it again, or to conclude the
feature is broken.
"""

from uuid import uuid4

import pytest
from sqlmodel import Session

from src.domain.organization import Organization
from src.domain.project import Project, ProjectRepository, RepositoryLayer
from src.domain.repository import Repository
from src.routers.repositories import _layer_value
from tests.db_helpers import build_test_engine


@pytest.fixture
def db_session():
    engine = build_test_engine()
    with Session(engine) as session:
        yield session


@pytest.fixture
def world(db_session):
    org = Organization(id=str(uuid4()), name="Acme", alias=f"a{str(uuid4())[:5]}")
    db_session.add(org)
    project = Project(
        id=str(uuid4()),
        organization_id=org.id,
        alias=f"P{str(uuid4())[:5]}".upper(),
        name="Project",
        description="d",
    )
    repo = Repository(
        id=str(uuid4()),
        organization_id=org.id,
        name="bps-ui-demo",
        full_name="acme/bps-ui-demo",
        url="https://github.com/acme/bps-ui-demo",
        layer="ui",
    )
    db_session.add_all([project, repo])
    db_session.commit()
    return db_session, org, project, repo


def _link(session, project, repo, layer):
    session.add(
        ProjectRepository(
            id=str(uuid4()),
            project_id=project.id,
            repository_id=repo.id,
            layer=layer,
        )
    )
    session.commit()


class TestTheLinkLayerWins:
    def test_a_project_classification_overrides_the_org_wide_one(self, world):
        session, org, project, repo = world
        _link(session, project, repo, RepositoryLayer.DESIGN)
        assert _layer_value(RepositoryLayer.DESIGN) == "design"
        assert repo.layer == "ui", "the org-wide value is deliberately untouched"

    def test_unassigned_does_not_overwrite_a_real_value(self, world):
        """ "Nobody classified this here" is not an answer.

        Falling through to the repository's own layer is right; replacing `ui`
        with the placeholder would lose information the listing already had.
        """
        assert _layer_value(RepositoryLayer.UNASSIGNED) is None
        assert _layer_value(None) is None

    def test_every_real_layer_reports_its_lowercase_value(self):
        """The API and CLI speak values; Postgres stores names. Pin the side
        this function is on, because getting it wrong 422s the caller."""
        for layer in RepositoryLayer:
            if layer is RepositoryLayer.UNASSIGNED:
                continue
            assert _layer_value(layer) == layer.value
            assert _layer_value(layer).islower()


class TestTheRouteReturnsIt:
    """The helper being right is not the same as the listing using it.

    A first version of these tests only exercised `_layer_value`, and deleting
    the override from the route left every one of them green -- the exact shape
    of test that cannot fail.
    """

    @pytest.mark.asyncio
    async def test_the_listing_shows_the_project_layer(self, world):
        session, org, project, repo = world
        _link(session, project, repo, RepositoryLayer.DESIGN)

        from src.routers.repositories import list_project_repositories

        rows = await list_project_repositories(
            organization_id=org.id,
            project_id=project.id,
            session=session,
            current_user=None,
            layer=None,
            _org=org,
        )
        assert [(r.name, r.layer) for r in rows] == [("bps-ui-demo", "design")]

    @pytest.mark.asyncio
    async def test_an_unclassified_link_falls_back_to_the_repository(self, world):
        session, org, project, repo = world
        _link(session, project, repo, RepositoryLayer.UNASSIGNED)

        from src.routers.repositories import list_project_repositories

        rows = await list_project_repositories(
            organization_id=org.id,
            project_id=project.id,
            session=session,
            current_user=None,
            layer=None,
            _org=org,
        )
        assert rows[0].layer == "ui"
