"""
Tests for repository listing and ?refresh=true state transitions
(archived_at, deleted_at tracking).
"""

from unittest.mock import AsyncMock, MagicMock, patch
from uuid import uuid4

import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session

from src.api.app import app
from src.database import get_session
from src.domain.organization import Organization
from src.domain.repository import Repository
from src.domain.user import User, UserRole
from tests.auth_helpers import bearer_for
from tests.db_helpers import build_test_engine


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


class TestListRepositoriesBasic:
    def test_list_returns_empty_for_new_org(self, client, org, auth_headers):
        resp = client.get(
            f"/api/v1/organizations/{org.id}/repositories",
            headers=auth_headers,
        )
        assert resp.status_code == 200
        assert resp.json() == []

    def test_list_returns_registered_repos(self, client, org, db_session, auth_headers):
        repo = Repository(
            id="gh-1",
            organization_id=org.id,
            name="my-repo",
            full_name="testorg/my-repo",
            url="https://github.com/testorg/my-repo",
            layer="api",
        )
        db_session.add(repo)
        db_session.commit()

        resp = client.get(
            f"/api/v1/organizations/{org.id}/repositories",
            headers=auth_headers,
        )
        assert resp.status_code == 200
        data = resp.json()
        assert len(data) == 1
        assert data[0]["name"] == "my-repo"


class TestRepositoryRefresh:
    def _make_github_repo(self, repo_id, name, archived=False):
        return {
            "id": repo_id,
            "name": name,
            "full_name": f"testorg/{name}",
            "html_url": f"https://github.com/testorg/{name}",
            "description": None,
            "language": "Python",
            "stargazers_count": 0,
            "forks_count": 0,
            "open_issues_count": 0,
            "private": False,
            "archived": archived,
            "topics": [],
            "created_at": "2024-01-01T00:00:00Z",
            "updated_at": "2024-01-01T00:00:00Z",
        }

    def test_refresh_without_credentials_returns_422(self, client, org, auth_headers):
        with patch(
            "src.routers.repositories.get_github_credentials", return_value=None
        ):
            resp = client.get(
                f"/api/v1/organizations/{org.id}/repositories?refresh=true",
                headers=auth_headers,
            )
        assert resp.status_code == 422

    def test_refresh_marks_archived_repo(
        self, client, org, db_engine, db_session, auth_headers
    ):
        existing = Repository(
            id="gh-10",
            organization_id=org.id,
            name="active-repo",
            full_name="testorg/active-repo",
            url="https://github.com/testorg/active-repo",
            archived=False,
            archived_at=None,
        )
        db_session.add(existing)
        db_session.commit()

        remote = [self._make_github_repo("gh-10", "active-repo", archived=True)]

        with patch(
            "src.routers.repositories.get_github_credentials",
            return_value={"token": "gho_test", "github_org": "testorg"},
        ):
            with patch("src.api.github_api.GitHubAPI") as mock_gh_class:
                mock_gh = AsyncMock()
                mock_gh.get_all_organization_repositories = AsyncMock(
                    return_value=remote
                )
                mock_gh.parse_repository_data = MagicMock(
                    side_effect=lambda r: {
                        "id": r["id"],
                        "name": r["name"],
                        "full_name": r["full_name"],
                        "url": r["html_url"],
                        "archived": r["archived"],
                        "language": r.get("language"),
                        "stars": r.get("stargazers_count", 0),
                        "forks": r.get("forks_count", 0),
                        "open_issues_count": r.get("open_issues_count", 0),
                        "is_private": r.get("private", False),
                    }
                )
                mock_gh_class.return_value = mock_gh

                resp = client.get(
                    f"/api/v1/organizations/{org.id}/repositories?refresh=true",
                    headers=auth_headers,
                )

        assert resp.status_code == 200

        with Session(db_engine) as s:
            updated = s.get(Repository, "gh-10")
            assert updated.archived is True
            assert updated.archived_at is not None

    def test_refresh_marks_missing_repo_as_deleted(
        self, client, org, db_engine, db_session, auth_headers
    ):
        existing = Repository(
            id="gh-20",
            organization_id=org.id,
            name="old-repo",
            full_name="testorg/old-repo",
            url="https://github.com/testorg/old-repo",
            deleted=False,
        )
        db_session.add(existing)
        db_session.commit()

        # GitHub returns zero repos — old-repo is gone
        remote = []

        with patch(
            "src.routers.repositories.get_github_credentials",
            return_value={"token": "gho_test", "github_org": "testorg"},
        ):
            with patch("src.api.github_api.GitHubAPI") as mock_gh_class:
                mock_gh = AsyncMock()
                mock_gh.get_all_organization_repositories = AsyncMock(
                    return_value=remote
                )
                mock_gh.parse_repository_data = MagicMock(return_value={})
                mock_gh_class.return_value = mock_gh

                resp = client.get(
                    f"/api/v1/organizations/{org.id}/repositories?refresh=true",
                    headers=auth_headers,
                )

        assert resp.status_code == 200

        with Session(db_engine) as s:
            deleted_repo = s.get(Repository, "gh-20")
            assert deleted_repo.deleted is True
            assert deleted_repo.deleted_at is not None
