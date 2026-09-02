"""
Tests for the GitHub credential lifecycle endpoints under
`/organizations/{org_id}/integrations/github/`.

Covers PF-150: `connect` used to return `organization: null` (a bare string or
None) instead of a populated organization object.

Also covers #572: `connect` validates the token against the live GitHub API and
then never stamped `last_validated_at` (0 of 4 rows in dev had it), and there
was no way at all to ask whether an *already-stored* credential still works —
the only route to that was re-submitting the token through `connect`, which
needs the asker to still hold it.
"""

import logging
from contextlib import contextmanager
from unittest.mock import patch
from uuid import uuid4

import httpx
import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, select

from src.api.app import app
from src.database import get_session
from src.domain.org_credential import OrgCredential
from src.domain.organization import (
    Organization,
    OrganizationMembership,
    OrganizationRole,
)
from src.domain.user import User, UserRole
from src.services.org_credential_service import (
    GITHUB_INTEGRATION,
    VaultUnavailableError,
)
from tests.auth_helpers import bearer_for
from tests.db_helpers import build_test_engine

STORED_TOKEN = "ghp_stored_token_must_never_be_echoed"


@pytest.fixture
def db_engine():
    engine = build_test_engine()
    return engine


@pytest.fixture
def db_session(db_engine):
    with Session(db_engine) as session:
        yield session


@pytest.fixture
def client(db_engine, db_session):
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
    o = Organization(id=str(uuid4()), name="Test Org")
    db_session.add(o)
    db_session.commit()
    db_session.refresh(o)
    return o


@pytest.fixture
def user(db_session):
    u = User(
        id=str(uuid4()),
        email="dev@example.com",
        full_name="Dev User",
        role=UserRole.ADMIN,
        is_platform_member=True,
    )
    db_session.add(u)
    db_session.commit()
    db_session.refresh(u)
    return u


@pytest.fixture
def auth_headers(user, db_session):
    return bearer_for(db_session, user.id)


class TestGitHubConnect:
    def test_connect_github_returns_non_null_organization(
        self, client, org, auth_headers
    ):
        resp = client.post(
            f"/api/v1/organizations/{org.id}/integrations/github/connect",
            json={
                "service": "github",
                "config": {"organization": "some-org"},
                "test_connection": False,
            },
            headers=auth_headers,
        )
        assert resp.status_code == 201
        data = resp.json()
        assert data["organization"] is not None
        assert isinstance(data["organization"], dict)
        assert data["organization"]["id"] is not None
        assert data["organization"]["alias"] is not None
        assert data["organization"]["github_org"] == "some-org"

    def test_connect_github_missing_org_name_returns_400(
        self, client, org, auth_headers
    ):
        resp = client.post(
            f"/api/v1/organizations/{org.id}/integrations/github/connect",
            json={
                "service": "github",
                "config": {},
                "test_connection": False,
            },
            headers=auth_headers,
        )
        assert resp.status_code == 400

    def test_connect_github_organization_matches_caller_org(
        self, client, org, auth_headers
    ):
        resp = client.post(
            f"/api/v1/organizations/{org.id}/integrations/github/connect",
            json={
                "service": "github",
                "config": {"organization": "some-org"},
                "test_connection": False,
            },
            headers=auth_headers,
        )
        assert resp.status_code == 201
        data = resp.json()
        assert data["organization"]["id"] == org.id
        assert data["organization"]["alias"] == org.alias


class TestGitHubConnectWithToken:
    """
    BUG 1 fix: passing a real token (config.token) must validate against
    GitHub and actually store credentials (in Vault `org_credentials` -- it was
    CredentialProvider when this was written), not just
    create a GitHubOrgRegistration row with nothing to authenticate with.
    """

    def test_connect_with_token_stores_credentials(self, client, org, auth_headers):
        with (
            patch(
                "src.api.github_api.GitHubAPI.validate_token",
                return_value={"login": "octocat"},
            ),
            patch(
                "src.api.github_api.GitHubAPI.validate_organization_access",
                return_value=True,
            ),
            patch(
                "src.api.github_api.GitHubAPI.get_all_organization_repositories",
                return_value=[{"id": "1"}, {"id": "2"}],
            ),
            patch(
                "src.services.github_connect_service.set_github_credentials"
            ) as mock_set_creds,
            patch(
                "src.services.github_connect_service.get_github_credentials"
            ) as mock_get_creds,
        ):
            # Not yet connected on the pre-check; the post-write read-back must
            # return a token or connect() fails loudly by design.
            mock_get_creds.side_effect = [None, {"token": "ghp_faketoken"}]

            resp = client.post(
                f"/api/v1/organizations/{org.id}/integrations/github/connect",
                json={
                    "service": "github",
                    "config": {"organization": "some-org", "token": "ghp_faketoken"},
                    "test_connection": True,
                },
                headers=auth_headers,
            )

        assert resp.status_code == 201
        data = resp.json()
        assert data["organization"]["github_org"] == "some-org"
        assert data["total_repos_discovered"] == 2
        # The token goes to Supabase Vault, not the local keyring.
        mock_set_creds.assert_called_once()
        kwargs = mock_set_creds.call_args.kwargs
        assert kwargs["token"] == "ghp_faketoken"
        assert kwargs["github_org"] == "some-org"

    def test_connect_with_invalid_token_returns_400(self, client, org, auth_headers):
        with patch(
            "src.api.github_api.GitHubAPI.validate_token",
            side_effect=Exception("Bad credentials"),
        ):
            resp = client.post(
                f"/api/v1/organizations/{org.id}/integrations/github/connect",
                json={
                    "service": "github",
                    "config": {"organization": "some-org", "token": "bad-token"},
                    "test_connection": True,
                },
                headers=auth_headers,
            )
        assert resp.status_code == 400

    def test_reconnect_different_org_without_force_returns_400(
        self, client, org, auth_headers
    ):
        with (
            patch(
                "src.api.github_api.GitHubAPI.validate_token",
                return_value={"login": "octocat"},
            ),
            patch(
                "src.api.github_api.GitHubAPI.validate_organization_access",
                return_value=True,
            ),
            patch(
                "src.api.github_api.GitHubAPI.get_all_organization_repositories",
                return_value=[],
            ),
            patch("src.services.github_connect_service.set_github_credentials"),
            patch(
                "src.services.github_connect_service.get_github_credentials"
            ) as mock_get_creds,
        ):
            # First connect to "org-a": nothing stored on the pre-check, then the
            # post-write read-back must succeed.
            mock_get_creds.side_effect = [None, {"token": "tok"}]
            resp1 = client.post(
                f"/api/v1/organizations/{org.id}/integrations/github/connect",
                json={
                    "service": "github",
                    "config": {"organization": "org-a", "token": "tok"},
                },
                headers=auth_headers,
            )
            assert resp1.status_code == 201

            # Second connect to "org-b" without force -- should be rejected
            mock_get_creds.side_effect = None
            mock_get_creds.return_value = {"token": "tok", "github_org": "org-a"}
            resp2 = client.post(
                f"/api/v1/organizations/{org.id}/integrations/github/connect",
                json={
                    "service": "github",
                    "config": {"organization": "org-b", "token": "tok"},
                },
                headers=auth_headers,
            )

        assert resp2.status_code == 400


# =============================================================================
# #572 -- last_validated_at, and validating an already-stored credential
# =============================================================================


@pytest.fixture
def stored_credential(db_session, org):
    """An org_credentials row with `last_validated_at` unset.

    A real row, not a mock: the stamp is an ORM UPDATE on an ordinary table, so
    asserting on the persisted column is what makes these tests behavioural
    rather than "was a function called". The row is created directly because
    `set_org_credential` is a Postgres function SQLite does not have — the
    payload itself is irrelevant here, only the audit columns are.
    """
    row = OrgCredential(
        id=str(uuid4()),
        organization_id=org.id,
        integration_type=GITHUB_INTEGRATION,
        vault_secret_id=str(uuid4()),
    )
    db_session.add(row)
    db_session.commit()
    db_session.refresh(row)
    assert row.last_validated_at is None
    return row


@pytest.fixture
def member_headers(db_session, org):
    """Bearer for a plain MEMBER of `org` — no platform bypass.

    `is_platform_member=True` (which the `user` fixture sets) synthesises an
    ADMIN membership in `verify_org_membership`, so a role guard cannot be
    tested with it.
    """
    member = User(
        id=str(uuid4()),
        email=f"member-{uuid4().hex[:8]}@example.com",
        full_name="Plain Member",
        role=UserRole.MEMBER,
        is_platform_member=False,
    )
    db_session.add(member)
    db_session.add(
        OrganizationMembership(
            id=str(uuid4()),
            user_id=member.id,
            organization_id=org.id,
            role=OrganizationRole.MEMBER,
            is_active=True,
        )
    )
    db_session.commit()
    return bearer_for(db_session, member.id)


def _reread(db_session, row_id):
    db_session.expire_all()
    return db_session.exec(
        select(OrgCredential).where(OrgCredential.id == row_id)
    ).first()


@contextmanager
def _github_connect_ok():
    """The live-GitHub calls `connect` makes, all succeeding.

    A context manager rather than a tuple of unstarted patchers: the tuple form
    handed back three, and call sites that only wanted two bound the third to
    `_` and never entered it — so the test read as though repo discovery were
    patched while the real outbound call was one refactor away from firing.
    """
    with (
        patch(
            "src.api.github_api.GitHubAPI.validate_token",
            return_value={"login": "octocat"},
        ),
        patch(
            "src.api.github_api.GitHubAPI.validate_organization_access",
            return_value=True,
        ),
        patch(
            "src.api.github_api.GitHubAPI.get_all_organization_repositories",
            return_value=[],
        ),
    ):
        yield


@contextmanager
def _validate_probes(token=None, org_access=None, creds=None):
    """Everything the validate route touches outside its own database.

    `token` and `org_access` are `patch` keyword arguments for the two
    *diagnostic* probes (`{"return_value": ...}` or `{"side_effect": ...}`), so
    "GitHub answered 429" and "GitHub never answered" are expressible in the
    same shape — which is the distinction this endpoint has to get right.

    The probes are what validation uses, deliberately, and not the boolean
    `validate_organization_access` that `connect` uses: a bool cannot carry
    "GitHub did not answer".
    """
    with (
        patch(
            "src.api.github_api.GitHubAPI.probe_token",
            **(token or {"return_value": (200, {"login": "octocat"})}),
        ),
        patch(
            "src.api.github_api.GitHubAPI.organization_access_status",
            **(org_access or {"return_value": 200}),
        ),
        patch(
            "src.services.github_connect_service.get_github_credentials",
            **(
                creds
                or {"return_value": {"token": STORED_TOKEN, "github_org": "some-org"}}
            ),
        ),
    ):
        yield


class TestConnectStampsLastValidatedAt:
    """`connect` validates against the live API; that must be recorded."""

    def test_connect_stamps_last_validated_at(
        self, client, org, auth_headers, db_session, stored_credential
    ):
        with (
            _github_connect_ok(),
            patch("src.services.github_connect_service.set_github_credentials"),
            patch(
                "src.services.github_connect_service.get_github_credentials"
            ) as mock_get_creds,
        ):
            # Nothing stored on the pre-check; every later read is the post-write
            # read-back, which must return a token or connect() fails by design.
            # A function rather than `side_effect=[None, {...}]`: a list makes a
            # third call anywhere in connect_github_organization a StopIteration
            # instead of a meaningful failure, so the test would be pinned to a
            # call count it does not care about.
            reads = {"n": 0}

            def _stored_credential(*_args, **_kwargs):
                reads["n"] += 1
                return None if reads["n"] == 1 else {"token": STORED_TOKEN}

            mock_get_creds.side_effect = _stored_credential
            resp = client.post(
                f"/api/v1/organizations/{org.id}/integrations/github/connect",
                json={
                    "service": "github",
                    "config": {"organization": "some-org", "token": STORED_TOKEN},
                },
                headers=auth_headers,
            )

        assert resp.status_code == 201
        assert _reread(db_session, stored_credential.id).last_validated_at is not None

    def test_connect_does_not_stamp_when_github_rejects_the_token(
        self, client, org, auth_headers, db_session, stored_credential
    ):
        """The column means "someone proved this works", so a 400 must not set it."""
        with patch(
            "src.api.github_api.GitHubAPI.validate_token",
            side_effect=Exception("Bad credentials"),
        ):
            resp = client.post(
                f"/api/v1/organizations/{org.id}/integrations/github/connect",
                json={
                    "service": "github",
                    "config": {"organization": "some-org", "token": "bad-token"},
                },
                headers=auth_headers,
            )

        assert resp.status_code == 400
        assert _reread(db_session, stored_credential.id).last_validated_at is None


class TestValidateStoredCredential:
    """POST /integrations/{service}/validate — check what is already stored."""

    def _post(self, client, org, headers, service="github"):
        return client.post(
            f"/api/v1/organizations/{org.id}/integrations/{service}/validate",
            headers=headers,
        )

    def test_validate_reports_valid_and_stamps(
        self, client, org, auth_headers, db_session, stored_credential
    ):
        with _validate_probes():
            resp = self._post(client, org, auth_headers)

        assert resp.status_code == 200
        body = resp.json()
        assert body["valid"] is True
        assert body["github_login"] == "octocat"
        assert body["github_org"] == "some-org"
        assert body["org_access"] is True
        assert body["error"] is None
        assert body["last_validated_at"] is not None
        assert _reread(db_session, stored_credential.id).last_validated_at is not None

    @pytest.mark.parametrize(
        "probes",
        [
            pytest.param({}, id="success"),
            pytest.param({"token": {"return_value": (401, None)}}, id="rejected"),
            pytest.param({"org_access": {"return_value": 404}}, id="no-org-access"),
            pytest.param(
                {
                    "token": {
                        "side_effect": httpx.LocalProtocolError(
                            f"Illegal header value b'Bearer {STORED_TOKEN}'"
                        )
                    }
                },
                id="exception-quoting-the-request",
            ),
        ],
    )
    def test_validate_never_echoes_the_credential(
        self, client, org, auth_headers, stored_credential, caplog, probes
    ):
        """Every path, not just the happy one.

        The `exception-quoting-the-request` case is not hypothetical and is why
        this test is parametrized: a stored token with a stray newline makes
        httpx/h11 raise `LocalProtocolError: Illegal header value b'Bearer
        ghp_…'`, and the first version of this endpoint interpolated `str(e)`
        into the 200 body and the log line. The success-only version of this
        test stayed green through exactly that mutation.

        The log is asserted as well as the body: a secret in the server log is
        still a leaked secret, and it is the half a response-body assertion
        silently misses.
        """
        with caplog.at_level(logging.DEBUG), _validate_probes(**probes):
            resp = self._post(client, org, auth_headers)

        assert resp.status_code == 200
        assert STORED_TOKEN not in resp.text
        assert STORED_TOKEN not in caplog.text

    def test_validate_reports_an_expired_token_without_stamping(
        self, client, org, auth_headers, db_session, stored_credential
    ):
        """The case that cost real time: an expired token made onboarding 500 and
        repository discovery return `[]`, neither of which said "expired"."""
        with _validate_probes(token={"return_value": (401, None)}):
            resp = self._post(client, org, auth_headers)

        # 200, not 4xx: the request was fine and the question was answered.
        assert resp.status_code == 200
        body = resp.json()
        assert body["valid"] is False
        assert "rejected the stored token" in body["error"]
        assert "401" in body["error"]
        assert body["last_validated_at"] is None
        assert _reread(db_session, stored_credential.id).last_validated_at is None

    def test_validate_reports_lost_org_access_without_stamping(
        self, client, org, auth_headers, db_session, stored_credential
    ):
        with _validate_probes(org_access={"return_value": 404}):
            resp = self._post(client, org, auth_headers)

        assert resp.status_code == 200
        body = resp.json()
        assert body["valid"] is False
        assert body["org_access"] is False
        assert body["github_login"] == "octocat"
        assert "no access" in body["error"]
        assert _reread(db_session, stored_credential.id).last_validated_at is None

    @pytest.mark.parametrize(
        "probes,expect_login",
        [
            pytest.param({"token": {"return_value": (429, None)}}, None, id="on-token"),
            pytest.param(
                {"org_access": {"return_value": 429}}, "octocat", id="on-org-access"
            ),
        ],
    )
    def test_validate_reports_a_throttled_github_as_undetermined(
        self,
        client,
        org,
        auth_headers,
        db_session,
        stored_credential,
        probes,
        expect_login,
    ):
        """A 429 is not a verdict on the credential.

        Mapping every non-200 to "no access" made this endpoint answer
        `valid: false, org_access: false, "the stored token … has no access to
        organization 'x'"` because GitHub rate-limited us. A diagnostic endpoint
        giving a confident wrong answer is worse than one that says it does not
        know — an ADMIN acts on it, and the action (reissue the org's token) is
        the wrong one.
        """
        with _validate_probes(**probes):
            resp = self._post(client, org, auth_headers)

        assert resp.status_code == 200
        body = resp.json()
        assert body["valid"] is None, "429 must not be reported as a bad credential"
        assert body["org_access"] is None
        assert body["github_login"] == expect_login
        assert "did not answer" in body["error"]
        assert "429" in body["error"]
        # Nothing was proved, so nothing is stamped.
        assert body["last_validated_at"] is None
        assert _reread(db_session, stored_credential.id).last_validated_at is None

    @pytest.mark.parametrize(
        "probes",
        [
            pytest.param(
                {"token": {"side_effect": httpx.ConnectError("connection refused")}},
                id="on-token",
            ),
            pytest.param(
                {
                    "org_access": {
                        "side_effect": httpx.ConnectError("connection refused")
                    }
                },
                id="on-org-access",
            ),
        ],
    )
    def test_validate_survives_github_being_unreachable(
        self, client, org, auth_headers, db_session, stored_credential, probes
    ):
        """Both live calls are inside the same handling.

        The org-access call used to sit *outside* the `try`, so a ConnectError
        there escaped unhandled — and with no exception handlers registered on
        this app that is a bare 500 with no cause in the body, one line away
        from an identical failure that answered a graceful 200. The `on-org-access`
        case is red (a raised ConnectError, not a 200) if that call moves back
        out.
        """
        with _validate_probes(**probes):
            resp = self._post(client, org, auth_headers)

        assert resp.status_code == 200
        body = resp.json()
        assert body["valid"] is None
        assert "did not answer" in body["error"]
        assert "ConnectError" in body["error"]
        # The exception's own message is never quoted — that is what leaks the
        # credential — so the class name is all that identifies it.
        assert "connection refused" not in body["error"]
        assert _reread(db_session, stored_credential.id).last_validated_at is None

    def test_validate_returns_503_when_vault_cannot_be_read(
        self, client, org, auth_headers, stored_credential
    ):
        """Trap A, on the one route whose caller is asking to read a credential.

        `VaultUnavailableError` is the loud failure this PR adds to the reader;
        left uncaught it is an opaque 500 with the actionable text visible only
        in the server log. The message names the extension, the function and the
        grant, and holds no secret, so it belongs in the response.
        """
        with _validate_probes(
            creds={
                "side_effect": VaultUnavailableError(
                    "get_org_credential could not be called on this Postgres "
                    "database — check the supabase_vault extension"
                )
            }
        ):
            resp = self._post(client, org, auth_headers)

        assert resp.status_code == 503
        assert "supabase_vault" in resp.json()["detail"]

    def test_validate_with_nothing_stored_returns_404(
        self, client, org, auth_headers, stored_credential
    ):
        """Nothing was validated and nothing failed validation — not `valid: false`."""
        with _validate_probes(creds={"return_value": None}):
            resp = self._post(client, org, auth_headers)

        assert resp.status_code == 404
        assert "no stored GitHub credential" in resp.json()["detail"]

    def test_validate_requires_admin(
        self, client, org, member_headers, db_session, stored_credential
    ):
        """A plain MEMBER may not exercise the org's stored credential.

        Everything downstream of the guard is set up to *succeed*, deliberately.
        Without that, an unguarded route would 404 on the absent credential and
        this test would still be red for the wrong reason — the shape of the
        #593 defect, where replacing an ADMIN guard with a no-op left the suite
        green. Mutated to `Depends(lambda: None)` this returns 200 and the
        credential is stamped by someone who should not have been able to ask.
        """
        with _validate_probes():
            resp = self._post(client, org, member_headers)

        assert resp.status_code == 403
        assert "admin" in resp.json()["detail"].lower()
        # Refused means refused: no outbound check, no audit write.
        assert _reread(db_session, stored_credential.id).last_validated_at is None

    def test_validate_requires_authentication(self, client, org):
        assert self._post(client, org, {}).status_code == 401

    def test_validate_other_services_are_honest_501s(
        self, client, org, auth_headers, stored_credential
    ):
        """Scoped to github — org_credentials holds exactly one integration type."""
        resp = self._post(client, org, auth_headers, service="slack")
        assert resp.status_code == 501


class TestTheSurvivingSyncPathResolvesTheTenantCredential:
    """#554's fail-closed property, moved to the sync path that still exists.

    It has now been homeless twice. `POST /integrations/github/sync` did
    ``x_integration_token or os.environ.get("GITHUB_TOKEN", "")`` — fail **open**,
    so an org with no stored credential silently synced against whatever account
    the deployment's own token belonged to. #595 deleted that endpoint and its
    tests, leaving the property pinned only on
    `POST /github-registrations/{id}/sync`; #658 deleted *that* (it was the
    org-wide import, and repositories now arrive only by project topic) and its
    tests with it. Topic discovery is the one repository sync left, so this is
    where the property lives.

    **Deliberately not of the shape "the env var is no longer read".** That is
    satisfied by code resolving nothing at all, and by a resolver returning None on
    every backend — which is what `get_org_credential_payload` does on SQLite, where
    it swallows `OperationalError`/`ProgrammingError`. So `GITHUB_TOKEN` is set to a
    recognisable sentinel, the resolver is patched at its import location in
    `src.services.github_connect_service`, and the assertion is on the token that
    reached `GitHubAPI`. The fail-closed twin asserts GitHub was **not** called at
    all — the pair is what makes both halves load-bearing.
    """

    OPERATOR_TOKEN = "ghp_operator_must_never_be_used"
    TENANT_TOKEN = "ghp_tenant_token"

    @pytest.fixture
    def project(self, db_session, org):
        from src.domain.project import Project

        p = Project(
            id=str(uuid4()),
            organization_id=org.id,
            alias="CRED",
            name="Credential Project",
            description="d",
        )
        db_session.add(p)
        db_session.commit()
        return p

    @contextmanager
    def _github_probe(self, creds):
        """Patch the resolver and capture the token `GitHubAPI` was built with.

        `search_organization_repositories` is patched on the class rather than
        stubbed as a free function so `self` — and therefore `self.token`, assigned
        in the real `__init__` — is the object the service actually constructed.
        """
        from src.api.github_api import GitHubAPI

        tokens: list = []

        async def record(api_self, *args, **kwargs):
            tokens.append(api_self.token)
            return []

        with (
            patch(
                "src.services.github_connect_service.get_github_credentials",
                return_value=creds,
            ),
            patch.object(GitHubAPI, "search_organization_repositories", new=record),
        ):
            yield tokens

    @pytest.mark.asyncio
    async def test_the_vault_token_reaches_github_not_the_process_env_one(
        self, db_session, org, project, monkeypatch
    ):
        from src.services.github_connect_service import GitHubConnectService

        monkeypatch.setenv("GITHUB_TOKEN", self.OPERATOR_TOKEN)
        creds = {"token": self.TENANT_TOKEN, "github_org": "acme"}

        with self._github_probe(creds) as tokens:
            await GitHubConnectService(db_session).discover_project_repositories(
                organization_id=org.id, project_id=project.id, github_label="cred"
            )

        assert tokens == [self.TENANT_TOKEN]

    @pytest.mark.asyncio
    async def test_an_unconfigured_org_refuses_and_never_calls_github(
        self, db_session, org, project, monkeypatch
    ):
        """No credential is a refusal, not a sync on the operator's account."""
        from src.services.github_connect_service import GitHubConnectService

        monkeypatch.setenv("GITHUB_TOKEN", self.OPERATOR_TOKEN)

        with self._github_probe(None) as tokens:
            with pytest.raises(ValueError) as raised:
                await GitHubConnectService(db_session).discover_project_repositories(
                    organization_id=org.id, project_id=project.id, github_label="cred"
                )

        assert "No GitHub connection found" in str(raised.value)
        assert tokens == [], "GitHub must not be reached without a tenant credential"
