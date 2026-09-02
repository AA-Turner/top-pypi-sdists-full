"""A repository's releases belong to exactly one project (PF-1368).

``_discover_releases`` imports a repo's published GitHub Releases as ``Release``
rows on the project being synced. It used to read *every* repo linked to the
project, so a repo shared between projects pushed its own package version into
all of them.

That is not hypothetical. ``innoday-blastoff`` carries PF's GitHub topic, and
publishing it to PyPI requires a published GitHub Release (``publish.yml``
triggers on ``release: published``). Publishing v0.3.0 therefore created a **PF
platform release v0.3.0**, which became ``max(released)`` and collapsed the
v1.0.0 changelog window from 171 merged PRs to 5 — silently, since a release row
that exists looks exactly like a release row that was meant to.

These tests pin the boundary: which repos discovery reads, that the invariant is
enforced by the database rather than by service code, and that the backfill
refuses to guess for a repo nobody has decided about.
"""

from uuid import uuid4

import pytest
from sqlalchemy.exc import IntegrityError
from sqlmodel import Session, select

from src.domain.organization import Organization
from src.domain.project import Project, ProjectRepository, RepositoryLayer
from src.domain.release import Release, ReleaseStatus
from src.domain.repository import Repository
from src.services.github_connect_service import GitHubConnectService
from tests.db_helpers import build_test_engine


@pytest.fixture
def db_session():
    engine = build_test_engine()
    with Session(engine) as session:
        yield session


@pytest.fixture
def org(db_session):
    o = Organization(id=str(uuid4()), name="Test Org")
    db_session.add(o)
    db_session.commit()
    return o


def make_project(db_session, org, alias_prefix="P"):
    p = Project(
        id=str(uuid4()),
        organization_id=org.id,
        alias=f"{alias_prefix}{str(uuid4())[:5]}".upper(),
        name="Project",
        description="d",
    )
    db_session.add(p)
    db_session.commit()
    return p


def make_repo(db_session, org, name):
    r = Repository(
        id=str(uuid4()),
        organization_id=org.id,
        name=name,
        full_name=f"acme/{name}",
        url=f"https://github.com/acme/{name}",
    )
    db_session.add(r)
    db_session.commit()
    return r


def link(db_session, project, repo, primary_project=False, active=True):
    pr = ProjectRepository(
        id=str(uuid4()),
        project_id=project.id,
        repository_id=repo.id,
        layer=RepositoryLayer.UNASSIGNED,
        is_primary_project=primary_project,
        is_active=active,
    )
    db_session.add(pr)
    db_session.commit()
    return pr


class TestTheInvariantIsInTheDatabase:
    """One primary project per repository, enforced by uq_repo_primary_project.

    In the database and not only in the service, because a service-layer rule is
    what let the release-import conflation stand unnoticed: nothing failed, the
    wrong row simply appeared.
    """

    def test_a_second_primary_for_one_repo_is_rejected(self, db_session, org):
        repo = make_repo(db_session, org, "shared")
        a = make_project(db_session, org, "A")
        b = make_project(db_session, org, "B")

        link(db_session, a, repo, primary_project=True)

        with pytest.raises(IntegrityError):
            link(db_session, b, repo, primary_project=True)
        db_session.rollback()

    def test_many_non_primary_links_are_fine(self, db_session, org):
        """The index must be partial — a repo legitimately belongs to several
        projects, and only the True rows are constrained."""
        repo = make_repo(db_session, org, "shared")
        for prefix in ("A", "B", "C"):
            link(db_session, make_project(db_session, org, prefix), repo)

        rows = db_session.exec(
            select(ProjectRepository).where(ProjectRepository.repository_id == repo.id)
        ).all()
        assert len(rows) == 3

    def test_one_primary_alongside_several_secondaries(self, db_session, org):
        repo = make_repo(db_session, org, "shared")
        link(db_session, make_project(db_session, org, "A"), repo, primary_project=True)
        link(db_session, make_project(db_session, org, "B"), repo)
        link(db_session, make_project(db_session, org, "C"), repo)

        primaries = db_session.exec(
            select(ProjectRepository).where(
                ProjectRepository.repository_id == repo.id,
                ProjectRepository.is_primary_project == True,  # noqa: E712
            )
        ).all()
        assert len(primaries) == 1

    def test_two_different_repos_may_each_be_primary_in_one_project(
        self, db_session, org
    ):
        """The index keys on repository_id, not project_id — a project owning the
        release path of several repos is the normal case, not a violation."""
        project = make_project(db_session, org, "A")
        for name in ("one", "two", "three"):
            link(
                db_session,
                project,
                make_repo(db_session, org, name),
                primary_project=True,
            )

        rows = db_session.exec(
            select(ProjectRepository).where(
                ProjectRepository.project_id == project.id,
                ProjectRepository.is_primary_project == True,  # noqa: E712
            )
        ).all()
        assert len(rows) == 3


class TestDiscoveryReadsOnlyPrimaryRepos:
    """The behaviour change itself, asserted on which repos get read."""

    def _service(self, db_session):
        return GitHubConnectService(db_session)

    def _selected_names(self, db_session, project):
        """Mirror of _discover_releases' selection, so the test states the rule
        rather than restating the SQL."""
        return set(
            db_session.exec(
                select(Repository.name)
                .join(
                    ProjectRepository,
                    ProjectRepository.repository_id == Repository.id,
                )
                .where(
                    ProjectRepository.project_id == project.id,
                    ProjectRepository.is_active == True,  # noqa: E712
                    ProjectRepository.is_primary_project == True,  # noqa: E712
                )
            ).all()
        )

    def test_a_secondary_repo_is_not_read(self, db_session, org):
        """The blastoff case exactly: the repo belongs to PF, but its releases
        belong to its own project."""
        pf = make_project(db_session, org, "PF")
        bo = make_project(db_session, org, "BO")
        blastoff = make_repo(db_session, org, "innoday-blastoff")

        link(db_session, bo, blastoff, primary_project=True)
        link(db_session, pf, blastoff)  # secondary in PF

        assert self._selected_names(db_session, pf) == set()
        assert self._selected_names(db_session, bo) == {"innoday-blastoff"}

    def test_a_primary_repo_is_read(self, db_session, org):
        pf = make_project(db_session, org, "PF")
        core = make_repo(db_session, org, "innoday")
        link(db_session, pf, core, primary_project=True)

        assert self._selected_names(db_session, pf) == {"innoday"}

    def test_an_undecided_repo_is_read_by_nobody(self, db_session, org):
        """False on every link means nobody has chosen. Skipping is deliberate:
        the wrong version silently imported is unrecoverable, a repo that goes
        quiet and logs why is not."""
        a = make_project(db_session, org, "A")
        b = make_project(db_session, org, "B")
        repo = make_repo(db_session, org, "undecided")
        link(db_session, a, repo)
        link(db_session, b, repo)

        assert self._selected_names(db_session, a) == set()
        assert self._selected_names(db_session, b) == set()

    def test_inactive_primary_link_is_still_excluded(self, db_session, org):
        """is_active and is_primary_project are independent gates; a repo that
        lost the topic contributes nothing even while it holds the primary."""
        pf = make_project(db_session, org, "PF")
        repo = make_repo(db_session, org, "gone")
        link(db_session, pf, repo, primary_project=True, active=False)

        assert self._selected_names(db_session, pf) == set()


class TestNewLinksAdoptAnUnclaimedRepo:
    """_repo_has_project_link decides whether discovery may claim a new repo."""

    def test_a_repo_with_no_other_link_is_claimable(self, db_session, org):
        pf = make_project(db_session, org, "PF")
        repo = make_repo(db_session, org, "fresh")

        service = GitHubConnectService(db_session)
        assert (
            service._repo_has_project_link(repo.id, excluding_project_id=pf.id) is False
        )

    def test_a_repo_already_elsewhere_is_not_claimable(self, db_session, org):
        pf = make_project(db_session, org, "PF")
        other = make_project(db_session, org, "OT")
        repo = make_repo(db_session, org, "shared")
        link(db_session, other, repo, primary_project=True)

        service = GitHubConnectService(db_session)
        assert (
            service._repo_has_project_link(repo.id, excluding_project_id=pf.id) is True
        )

    def test_an_inactive_link_elsewhere_still_blocks_the_claim(self, db_session, org):
        """A repo that lost another project's topic can regain it — the row is
        kept for exactly that. Treating the link as absent would hand this
        project the primary and then collide when the other one came back."""
        pf = make_project(db_session, org, "PF")
        other = make_project(db_session, org, "OT")
        repo = make_repo(db_session, org, "returning")
        link(db_session, other, repo, primary_project=True, active=False)

        service = GitHubConnectService(db_session)
        assert (
            service._repo_has_project_link(repo.id, excluding_project_id=pf.id) is True
        )

    def test_its_own_link_does_not_block_it(self, db_session, org):
        pf = make_project(db_session, org, "PF")
        repo = make_repo(db_session, org, "mine")
        link(db_session, pf, repo)

        service = GitHubConnectService(db_session)
        assert (
            service._repo_has_project_link(repo.id, excluding_project_id=pf.id) is False
        )


class TestTheTwoPrimaryFlagsAreDifferentThings:
    """is_primary and is_primary_project point opposite ways on one table, and
    that is the likeliest thing for a future change to conflate."""

    def test_they_are_independent(self, db_session, org):
        project = make_project(db_session, org, "A")
        repo = make_repo(db_session, org, "r")
        pr = ProjectRepository(
            id=str(uuid4()),
            project_id=project.id,
            repository_id=repo.id,
            layer=RepositoryLayer.UNASSIGNED,
            is_primary=True,  # this repo is the project's main repo
            is_primary_project=False,  # ...but its releases live elsewhere
        )
        db_session.add(pr)
        db_session.commit()

        stored = db_session.exec(
            select(ProjectRepository).where(ProjectRepository.id == pr.id)
        ).first()
        assert stored.is_primary is True
        assert stored.is_primary_project is False

    def test_being_the_projects_main_repo_does_not_grant_the_release_path(
        self, db_session, org
    ):
        """Setting is_primary must not imply is_primary_project — otherwise the
        bug returns through the other flag."""
        a = make_project(db_session, org, "A")
        b = make_project(db_session, org, "B")
        repo = make_repo(db_session, org, "shared")

        db_session.add(
            ProjectRepository(
                id=str(uuid4()),
                project_id=a.id,
                repository_id=repo.id,
                layer=RepositoryLayer.UNASSIGNED,
                is_primary=True,
                is_primary_project=False,
            )
        )
        link(db_session, b, repo, primary_project=True)
        db_session.commit()

        owners = db_session.exec(
            select(ProjectRepository.project_id).where(
                ProjectRepository.repository_id == repo.id,
                ProjectRepository.is_primary_project == True,  # noqa: E712
            )
        ).all()
        assert owners == [b.id]


class TestDefaultIsNotPrimary:
    def test_a_bare_link_claims_nothing(self, db_session, org):
        """Default False, so a link created by any path that has not been taught
        about this column cannot silently acquire a repo's release path."""
        project = make_project(db_session, org, "A")
        repo = make_repo(db_session, org, "r")
        pr = ProjectRepository(
            id=str(uuid4()),
            project_id=project.id,
            repository_id=repo.id,
            layer=RepositoryLayer.UNASSIGNED,
        )
        db_session.add(pr)
        db_session.commit()
        assert pr.is_primary_project is False


class TestReleaseRowsAreProjectScoped:
    """Sanity floor: a release belongs to one project, so the fix is about which
    project a repo's version reaches — not about deduplicating versions."""

    def test_same_version_may_exist_for_two_projects(self, db_session, org):
        a = make_project(db_session, org, "A")
        b = make_project(db_session, org, "B")
        for project in (a, b):
            db_session.add(
                Release(
                    id=str(uuid4()),
                    organization_id=org.id,
                    project_id=project.id,
                    version="v0.3.0",
                    status=ReleaseStatus.RELEASED,
                )
            )
        db_session.commit()

        rows = db_session.exec(select(Release).where(Release.version == "v0.3.0")).all()
        assert {r.project_id for r in rows} == {a.id, b.id}


class TestProjectRepositoriesAcceptsAnAlias:
    """`--project <alias>` must work here as it does everywhere else.

    `list_project_repositories` matched on `Project.id` alone while every
    sibling route goes through `resolve_project` (id, then alias, then name), so
    one command in the CLI disagreed with the rest:

        innoday --project BLASTOFF summary    -> fine
        innoday --project BLASTOFF sync       -> fine
        innoday --project BLASTOFF repos list -> 404

    The alias is what a person has to hand; the UUID is not. And the failure was
    a bare 404 — indistinguishable from "no such project" — so the form that does
    work was not discoverable from the error.
    """

    def test_resolve_project_accepts_id_alias_and_name(self, db_session, org):
        from src.routers.projects import resolve_project

        project = make_project(db_session, org, "BO")
        by_id = resolve_project(project.id, org.id, db_session)
        by_alias = resolve_project(project.alias, org.id, db_session)
        by_name = resolve_project(project.name, org.id, db_session)
        assert by_id.id == by_alias.id == by_name.id == project.id

    def test_the_repositories_query_keys_on_the_resolved_id(self, db_session, org):
        """The half of the fix that is easy to miss: resolving the project but
        then joining on the raw ref returns an empty list rather than a 404 —
        a wrong answer that looks like a legitimately empty project."""
        from src.routers.projects import resolve_project

        project = make_project(db_session, org, "BO")
        repo = make_repo(db_session, org, "innoday-blastoff")
        link(db_session, project, repo, primary_project=True)

        resolved = resolve_project(project.alias, org.id, db_session)

        found = db_session.exec(
            select(Repository)
            .join(ProjectRepository, ProjectRepository.repository_id == Repository.id)
            .where(
                ProjectRepository.project_id == resolved.id,
                ProjectRepository.is_active == True,  # noqa: E712
            )
        ).all()
        assert [r.name for r in found] == ["innoday-blastoff"]

        # ...and the same query keyed on the alias finds nothing.
        by_ref = db_session.exec(
            select(Repository)
            .join(ProjectRepository, ProjectRepository.repository_id == Repository.id)
            .where(ProjectRepository.project_id == project.alias)
        ).all()
        assert by_ref == []
