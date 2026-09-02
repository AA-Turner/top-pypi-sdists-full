"""An alias in the URL must reach the handler as the UUID it resolves to.

`resolve_organization`/`resolve_project` accept a UUID, an alias or a name, so
every org-scoped route reads as alias-tolerant. It was not: the guard resolved
the entity for *authorization* and returned it, while the handler's own `org_id`
/ `project_id` argument stayed bound to the raw path -- and 105 handlers filtered
with that raw value against a UUID column.

The proven case, measured against the deployed API:

    GET /organizations/hs/releases   ->  HTTP 200, []      (PF has three)

Not an error. A confident, wrong, empty answer. Where the ref feeds a lookup
rather than a filter, the same cause shows up as a spurious 404 instead.

**These tests go through `TestClient` on purpose.** The fix mutates
`request.scope["path_params"]` from inside a dependency, which works only because
FastAPI solves sub-dependencies before it binds the handler's path parameters --
real behaviour, but not a documented guarantee. A unit test calling the guard
directly would pass whatever FastAPI did. Driving a live route is the only check
that fails if that order ever changes.
"""

from unittest.mock import patch
from uuid import uuid4

import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, select

from src.api.app import app
from src.database import get_session
from src.domain.organization import (
    Organization,
    OrganizationMembership,
    OrganizationRole,
)
from src.domain.project import Project
from src.domain.release import Release
from src.domain.ticket import Ticket
from src.domain.user import User, UserRole
from tests.auth_helpers import bearer_for
from tests.db_helpers import build_test_engine


@pytest.fixture
def db_engine():
    return build_test_engine()


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
    o = Organization(id=str(uuid4()), name="Haviland Software", alias="hs")
    db_session.add(o)
    db_session.commit()
    db_session.refresh(o)
    return o


@pytest.fixture
def project(db_session, org):
    p = Project(
        id=str(uuid4()),
        name="Innoday",
        alias="PF",
        description="Release management and orchestration.",
        organization_id=org.id,
    )
    db_session.add(p)
    db_session.commit()
    db_session.refresh(p)
    return p


@pytest.fixture
def user(db_session):
    u = User(
        id=str(uuid4()),
        email="karl@example.com",
        full_name="Karl Haviland",
        role=UserRole.MEMBER,
        is_platform_member=True,
    )
    db_session.add(u)
    db_session.commit()
    db_session.refresh(u)
    return u


@pytest.fixture
def auth(user, db_session):
    return bearer_for(db_session, user.id)


@pytest.fixture
def release(db_session, org, project):
    r = Release(
        id=str(uuid4()),
        organization_id=org.id,
        project_id=project.id,
        version="v1.0.0",
    )
    db_session.add(r)
    db_session.commit()
    db_session.refresh(r)
    return r


class TestTheOrgAliasReachesTheHandlerResolved:
    """`list_releases` filters `Release.organization_id == org_id` with the raw
    param, so this route is the one the bug was found on."""

    def test_an_alias_returns_the_same_rows_as_the_uuid(
        self, client, auth, org, release
    ):
        by_uuid = client.get(f"/api/v1/organizations/{org.id}/releases", headers=auth)
        by_alias = client.get("/api/v1/organizations/hs/releases", headers=auth)

        assert by_uuid.status_code == 200
        assert by_alias.status_code == 200
        assert len(by_uuid.json()) == 1
        # The regression: this used to be `[]`.
        assert by_alias.json() == by_uuid.json()

    def test_an_unknown_alias_still_404s(self, client, auth):
        """Normalising must not turn a bad org into a permissive one."""
        r = client.get("/api/v1/organizations/nosuchorg/releases", headers=auth)
        assert r.status_code == 404


class TestTheProjectAliasReachesTheHandlerResolved:
    # A `test_a_project_alias_filters_correctly` stood here passing `project.id`.
    # It was named for an alias, exercised none, and asserted a strict subset of
    # `test_a_query_parameter_alias_filters_correctly` below, which compares the
    # alias against the UUID.

    def test_a_project_alias_in_the_path_resolves(
        self, client, auth, org, project, db_session
    ):
        """`get_project_tickets` looked the project up with the raw ref, so an
        alias 404'd where the UUID worked."""
        by_uuid = client.get(
            f"/api/v1/organizations/{org.id}/projects/{project.id}/tickets",
            headers=auth,
        )
        by_alias = client.get(
            "/api/v1/organizations/hs/projects/PF/tickets", headers=auth
        )

        assert by_uuid.status_code == 200
        assert by_alias.status_code == by_uuid.status_code
        assert by_alias.json() == by_uuid.json()

    def test_an_unknown_project_still_404s(self, client, auth, org):
        r = client.get("/api/v1/organizations/hs/projects/NOSUCH/tickets", headers=auth)
        assert r.status_code == 404


class TestRefsThatArriveOutsideThePath:
    """`normalize_path_refs` rewrites path parameters. A query parameter and a
    body field are neither, so they need `resolve_project_ref` explicitly."""

    def test_a_query_parameter_alias_filters_correctly(
        self, client, auth, org, project, release
    ):
        by_uuid = client.get(
            f"/api/v1/organizations/hs/releases?project_id={project.id}", headers=auth
        )
        by_alias = client.get(
            "/api/v1/organizations/hs/releases?project_id=PF", headers=auth
        )

        assert by_alias.status_code == 200
        assert len(by_uuid.json()) == 1
        assert by_alias.json() == by_uuid.json()

    def test_a_body_alias_is_not_written_to_the_fk(
        self, client, auth, org, project, db_session
    ):
        """The worst of the three: `create_release` puts `body.project_id`
        straight into `Release.project_id`, a **foreign key**.

        On Postgres `releases_project_id_fkey` is validated and not deferrable, so
        an alias there was refused at flush and the request answered **500** --
        not a corrupt row. What this assertion sees is the SQLite version of the
        same bug (the alias stored, every later query missing the row it just
        wrote), because `build_test_engine` leaves foreign keys off. Same missing
        call, two symptoms; see the note in `tests/db_helpers.py`.
        """
        r = client.post(
            "/api/v1/organizations/hs/releases",
            json={"version": "v2.0.0", "project_id": "PF"},
            headers=auth,
        )
        assert r.status_code == 201

        stored = db_session.exec(
            select(Release).where(Release.version == "v2.0.0")
        ).one()
        assert stored.project_id == project.id
        assert stored.project_id != "PF"

    def test_a_patch_body_alias_is_not_written_to_the_fk(
        self, client, auth, org, project, release, db_session
    ):
        """`create_release` resolved its body ref; `update_release`, 300 lines
        below in the same file, did not -- and it `setattr`s every field it was
        given onto the row. Measured on Postgres: 500, mid-release, since the
        PATCH that marks a release shipped is also what closes its tickets."""
        other = Project(
            id=str(uuid4()),
            name="Blastoff",
            alias="BO",
            description="Release engine.",
            organization_id=org.id,
        )
        db_session.add(other)
        db_session.commit()

        r = client.patch(
            f"/api/v1/organizations/hs/releases/{release.id}",
            json={"project_id": "BO"},
            headers=auth,
        )
        assert r.status_code == 200

        db_session.expire_all()
        assert db_session.get(Release, release.id).project_id == other.id

    def test_a_patch_that_never_mentions_the_project_is_still_accepted(
        self, client, auth, org, project, release
    ):
        """Resolution happens in the dumped fields, not on the model.

        Assigning to `body.project_id` would add it to `model_fields_set`, so a
        PATCH of anything else would acquire a `project_id: None` and be refused
        by the "cannot be cleared" check.
        """
        r = client.patch(
            f"/api/v1/organizations/hs/releases/{release.id}",
            json={"name": "First light"},
            headers=auth,
        )
        assert r.status_code == 200, r.text
        assert r.json()["project_id"] == project.id

    def test_a_version_lookup_by_alias_finds_the_real_release(
        self, client, auth, org, project, release
    ):
        """This one did not answer wrongly by omission -- it **invented a
        record**: `?project_id=PF` returned `{"id": "", "status":
        "unregistered"}` while the UUID returned the real release."""
        by_uuid = client.get(
            f"/api/v1/organizations/hs/releases/by-version/{release.version}",
            params={"project_id": project.id},
            headers=auth,
        )
        by_alias = client.get(
            f"/api/v1/organizations/hs/releases/by-version/{release.version}",
            params={"project_id": "PF"},
            headers=auth,
        )

        assert by_uuid.status_code == 200
        assert by_alias.status_code == 200
        assert by_alias.json()["id"] == release.id
        assert by_alias.json() == by_uuid.json()

    def test_an_unresolvable_ref_is_never_reported_as_unregistered(
        self, client, auth, org, project, release
    ):
        """The synthetic "unregistered" release stays -- `innoday releases show`
        reads it to tell a board-sourced version from an unknown one -- but a ref
        that names no project must not be able to reach it. Otherwise a typo comes
        back as a release, which is worse than the empty list this file exists to
        remove."""
        r = client.get(
            f"/api/v1/organizations/hs/releases/by-version/{release.version}",
            params={"project_id": "NOSUCH"},
            headers=auth,
        )
        assert r.status_code == 404
        assert "unregistered" not in r.text

    def test_the_current_release_is_readable_by_alias(
        self, client, auth, org, project, release
    ):
        """A 404 here reads as "nothing shipped", and this route exists so that a
        summary can be generated by reading it and nothing else."""
        by_uuid = client.get(
            "/api/v1/organizations/hs/releases/current/tickets",
            params={"project_id": project.id},
            headers=auth,
        )
        by_alias = client.get(
            "/api/v1/organizations/hs/releases/current/tickets",
            params={"project_id": "PF"},
            headers=auth,
        )

        assert by_uuid.status_code == 200
        assert by_alias.json() == by_uuid.json()

    def test_a_missing_current_release_names_the_ref_that_was_sent(
        self, client, auth, org, project
    ):
        """The 404 interpolates `project_id`, which is now a resolved UUID -- so
        the message must carry what the caller typed, not an identifier they have
        never seen."""
        r = client.get(
            "/api/v1/organizations/hs/releases/current/tickets",
            params={"project_id": "PF"},
            headers=auth,
        )
        assert r.status_code == 404
        assert "Project PF has no current release" in r.json()["detail"]

    def test_a_board_query_alias_filters_correctly(self, client, auth, org, project):
        r = client.get("/api/v1/organizations/hs/boards?project_id=PF", headers=auth)
        assert r.status_code == 200


class TestTicketBodiesTakeAnAlias:
    """`{"project_id": "PF"}` answered *"Project not found in this
    organization"* -- for a project the caller is a member of, while CLAUDE.md
    told people an alias works wherever a UUID does."""

    def test_a_create_stores_the_uuid(self, client, auth, org, project, db_session):
        with patch("src.routers.tickets.can_create_ticket", return_value=True):
            r = client.post(
                "/api/v1/organizations/hs/tickets",
                json={
                    "summary": "Resolve the ref",
                    "project_id": "PF",
                    "push_to_board": False,
                },
                headers=auth,
            )
        assert r.status_code == 200, r.text
        assert r.json()["project_id"] == project.id

    def test_a_move_by_alias_lands_on_the_project(
        self, client, auth, org, project, db_session
    ):
        destination = Project(
            id=str(uuid4()),
            name="Blastoff",
            alias="BO",
            description="Release engine.",
            organization_id=org.id,
        )
        ticket = Ticket(
            summary="Move me",
            organization_id=org.id,
            project_id=project.id,
        )
        db_session.add(destination)
        db_session.add(ticket)
        db_session.commit()
        db_session.refresh(ticket)

        r = client.put(
            f"/api/v1/organizations/hs/tickets/{ticket.id}",
            json={"project_id": "BO"},
            headers=auth,
        )
        assert r.status_code == 200, r.text
        assert r.json()["project_id"] == destination.id


class TestOtherBodiesThatCarryAProjectRef:
    def test_an_identity_claim_stores_the_uuid(
        self, client, auth, org, project, user, db_session
    ):
        """`user_identity.project_id` is a validated FK too, so an alias here was
        a 500 on Postgres rather than a wrong row."""
        # A real membership row, not the platform-member bypass: this route
        # refuses to map a handle to someone resolution would not match anyway.
        db_session.add(
            OrganizationMembership(
                id=str(uuid4()),
                user_id=user.id,
                organization_id=org.id,
                role=OrganizationRole.ADMIN,
                is_active=True,
            )
        )
        db_session.commit()

        r = client.post(
            "/api/v1/organizations/hs/identities",
            json={
                "user": user.email,
                "platform": "linear",
                "handle": "Karl Haviland",
                "project_id": "PF",
            },
            headers=auth,
        )
        assert r.status_code == 201, r.text
        assert r.json()["project_id"] == project.id

    def test_a_board_registration_gets_past_the_project_check(
        self, client, auth, org, project
    ):
        """`board register` is the first call a new project makes, and an alias
        stopped at *"Project 'PF' not found"*. Board access is stubbed out: what
        is under test is that the ref resolves, so the route reaches the board at
        all -- reported here as the board being unreachable, not the project."""
        with patch("src.routers.boards.validate_board_access", return_value=False):
            r = client.post(
                "/api/v1/organizations/hs/boards",
                json={
                    "board_url": "https://trello.com/b/abc123",
                    "board_name": "Delivery",
                    "board_type": "trello",
                    "project_id": "PF",
                },
                headers={**auth, "X-Integration-Token": "tok"},
            )

        assert r.status_code != 404, r.text
        assert "Project" not in r.text


class TestNormalizationIsCaseInsensitiveAndIdempotent:
    def test_a_lowercase_project_alias_resolves(self, client, auth, org, project):
        """`resolve_project` upper-cases both sides; the normaliser must not
        narrow that."""
        r = client.get("/api/v1/organizations/hs/projects/pf/tickets", headers=auth)
        assert r.status_code == 200

    def test_a_uuid_passes_through_unchanged(self, client, auth, org, project):
        r = client.get(
            f"/api/v1/organizations/{org.id}/projects/{project.id}/tickets",
            headers=auth,
        )
        assert r.status_code == 200


class TestTheNormalizerItself:
    """Unit-level checks of the parts a route cannot easily exercise."""

    def test_both_org_param_spellings_are_rewritten(self, db_session, org):
        """Routers use `org_id` and `organization_id` interchangeably."""
        from src.middleware.rbac import normalize_path_refs

        request = _fake_request({"organization_id": "hs", "org_id": "hs"})
        normalize_path_refs(request, org, db_session)

        assert request.scope["path_params"]["organization_id"] == org.id
        assert request.scope["path_params"]["org_id"] == org.id

    def test_a_route_with_no_project_param_is_untouched(self, db_session, org):
        from src.middleware.rbac import normalize_path_refs

        request = _fake_request({"org_id": "hs", "board_id": "abc"})
        normalize_path_refs(request, org, db_session)

        assert request.scope["path_params"]["board_id"] == "abc"

    def test_a_project_uuid_costs_no_lookup(self, db_session, org, project):
        """Gate on the UUID shape so the common path adds no query."""
        from src.middleware import rbac

        request = _fake_request({"org_id": "hs", "project_id": project.id})
        with patch("src.routers.projects.resolve_project") as resolver:
            rbac.normalize_path_refs(request, org, db_session)

        resolver.assert_not_called()
        assert request.scope["path_params"]["project_id"] == project.id

    def test_a_padded_uuid_leaves_as_the_bare_uuid(self, db_session, org, project):
        """The gate strips before matching; the value it keeps must be stripped too.

        It was not: the UUID branch returned early with the original, so
        `<uuid>%20` satisfied the short-circuit and then filtered a UUID column by
        `"<uuid> "` -- landing on the very `200 []` this change removes, through
        the fast path meant to be free.
        """
        from src.middleware.rbac import normalize_path_refs, resolve_project_ref

        assert resolve_project_ref(f" {project.id} ", org.id, db_session) == project.id

        request = _fake_request({"org_id": "hs", "project_id": f"{project.id} "})
        normalize_path_refs(request, org, db_session)
        assert request.scope["path_params"]["project_id"] == project.id

    def test_a_padded_alias_still_resolves(self, db_session, org, project):
        from src.middleware.rbac import resolve_project_ref

        assert resolve_project_ref(" PF ", org.id, db_session) == project.id

    def test_a_padded_uuid_query_parameter_still_filters(
        self, client, auth, org, project, release
    ):
        """End to end, since the path-param and query-param sites now share one
        gate and this is the reachable half."""
        r = client.get(
            "/api/v1/organizations/hs/releases",
            params={"project_id": f"{project.id} "},
            headers=auth,
        )
        assert r.status_code == 200
        assert len(r.json()) == 1


def _fake_request(path_params):
    class _R:
        def __init__(self, params):
            self.scope = {"path_params": params}

    return _R(dict(path_params))
