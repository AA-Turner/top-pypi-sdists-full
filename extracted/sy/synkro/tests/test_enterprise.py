"""Tests for synkro.enterprise SDK."""

import json
from unittest.mock import MagicMock, patch

import httpx
import pytest

from synkro.enterprise import (
    AsyncSynkro,
    Synkro,
    SynkroAPIError,
    SynkroAuthError,
    SynkroError,
    SynkroNotFoundError,
    SynkroRateLimitError,
)
from synkro.enterprise._http import _raise_for_status
from synkro.enterprise.types import (
    DatasetCreateResult,
    LangSmithConnection,
    Policy,
    PolicyCreateResult,
    Project,
    ProjectStatus,
)

# ── Fixtures ──────────────────────────────────────────────


def _mock_response(status_code: int = 200, json_data=None, headers=None):
    """Create a mock httpx.Response."""
    resp = MagicMock(spec=httpx.Response)
    resp.status_code = status_code
    resp.is_success = 200 <= status_code < 300
    resp.text = json.dumps(json_data) if json_data else ""
    resp.json.return_value = json_data or {}
    resp.headers = headers or {}
    return resp


def _make_client():
    """Create a Synkro client with a mocked transport."""
    client = Synkro(api_key="sk-test-123", base_url="http://localhost:3000")
    return client


# ── Error Mapping Tests ──────────────────────────────────


class TestErrorMapping:
    def test_401_raises_auth_error(self):
        resp = _mock_response(401)
        with pytest.raises(SynkroAuthError, match="Invalid or expired API key"):
            _raise_for_status(resp)

    def test_404_raises_not_found(self):
        resp = _mock_response(404)
        with pytest.raises(SynkroNotFoundError, match="Resource not found"):
            _raise_for_status(resp)

    def test_429_raises_rate_limit(self):
        resp = _mock_response(429, headers={"Retry-After": "30"})
        with pytest.raises(SynkroRateLimitError, match="Rate limit exceeded") as exc_info:
            _raise_for_status(resp)
        assert exc_info.value.retry_after == "30"

    def test_500_raises_api_error(self):
        resp = _mock_response(500, json_data={"error": "Internal server error"})
        with pytest.raises(SynkroAPIError, match="500: Internal server error") as exc_info:
            _raise_for_status(resp)
        assert exc_info.value.status_code == 500

    def test_400_raises_api_error_with_detail(self):
        resp = _mock_response(400, json_data={"error": "Bad request: missing name"})
        with pytest.raises(SynkroAPIError, match="Bad request: missing name") as exc_info:
            _raise_for_status(resp)
        assert exc_info.value.status_code == 400

    def test_200_does_not_raise(self):
        resp = _mock_response(200)
        _raise_for_status(resp)  # Should not raise


# ── Client Tests ─────────────────────────────────────────


class TestClientInit:
    def test_default_base_url(self):
        client = Synkro(api_key="sk-test")
        assert client._http._client.base_url == httpx.URL("https://api.synkro.sh")
        client.close()

    def test_custom_base_url(self):
        client = Synkro(api_key="sk-test", base_url="http://localhost:3000")
        assert client._http._client.base_url == httpx.URL("http://localhost:3000")
        client.close()

    def test_headers_set(self):
        client = Synkro(api_key="sk-test-key")
        headers = client._http._client.headers
        assert headers["x-api-key"] == "sk-test-key"
        assert headers["content-type"] == "application/json"
        assert "synkro-python/" in headers["user-agent"]
        client.close()

    def test_context_manager(self):
        with Synkro(api_key="sk-test") as client:
            assert client.projects is not None
            assert client.policies is not None
            assert client.integrations is not None

    def test_has_all_resources(self):
        client = Synkro(api_key="sk-test")
        assert hasattr(client, "projects")
        assert hasattr(client, "policies")
        assert hasattr(client, "integrations")
        client.close()

    def test_async_client_init(self):
        client = AsyncSynkro(api_key="sk-test")
        assert hasattr(client, "projects")
        assert hasattr(client, "policies")
        assert hasattr(client, "integrations")


# ── Projects Resource Tests ──────────────────────────────


class TestProjects:
    def test_list(self):
        client = _make_client()
        mock_data = [
            {"id": "p1", "slug": "proj_abc", "name": "Test", "is_active": True},
            {"id": "p2", "slug": "proj_def", "name": "Test 2", "is_active": False},
        ]
        with patch.object(client._http, "get", return_value=mock_data):
            projects = client.projects.list()
        assert len(projects) == 2
        assert isinstance(projects[0], Project)
        assert projects[0].id == "p1"
        assert projects[0].slug == "proj_abc"
        assert projects[1].is_active is False
        client.close()

    def test_get(self):
        client = _make_client()
        mock_data = {
            "id": "p1",
            "slug": "proj_abc",
            "name": "Test",
            "is_active": True,
            "gateway_url": "https://gateway.synkro.sh/v1/p/proj_abc",
        }
        with patch.object(client._http, "get", return_value=mock_data) as mock_get:
            project = client.projects.get("p1")
        assert isinstance(project, Project)
        assert project.gateway_url == "https://gateway.synkro.sh/v1/p/proj_abc"
        mock_get.assert_called_once_with("/api/projects/p1")
        client.close()

    def test_create(self):
        client = _make_client()
        mock_data = {"id": "p1", "slug": "proj_abc", "name": "My Project", "is_active": True}
        with patch.object(client._http, "post", return_value=mock_data) as mock_post:
            project = client.projects.create(name="My Project", provider="openai")
        assert isinstance(project, Project)
        assert project.name == "My Project"
        mock_post.assert_called_once_with(
            "/api/projects", json={"name": "My Project", "provider": "openai"}
        )
        client.close()

    def test_create_defaults(self):
        client = _make_client()
        mock_data = {"id": "p1", "slug": "proj_abc", "name": "Default Project", "is_active": True}
        with patch.object(client._http, "post", return_value=mock_data) as mock_post:
            client.projects.create()
        mock_post.assert_called_once_with("/api/projects", json={"name": "Default Project"})
        client.close()

    def test_update(self):
        client = _make_client()
        with patch.object(client._http, "patch", return_value={}) as mock_patch:
            client.projects.update("p1", name="New Name", is_active=False)
        mock_patch.assert_called_once_with(
            "/api/projects/p1", json={"name": "New Name", "is_active": False}
        )
        client.close()

    def test_update_langsmith_project(self):
        client = _make_client()
        with patch.object(client._http, "patch", return_value={}) as mock_patch:
            client.projects.update("p1", langsmith_project="my-ls-proj")
        mock_patch.assert_called_once_with(
            "/api/projects/p1", json={"langsmith_project": "my-ls-proj"}
        )
        client.close()

    def test_update_partial(self):
        client = _make_client()
        with patch.object(client._http, "patch", return_value={}) as mock_patch:
            client.projects.update("p1", name="Only Name")
        mock_patch.assert_called_once_with("/api/projects/p1", json={"name": "Only Name"})
        client.close()

    def test_delete(self):
        client = _make_client()
        with patch.object(client._http, "delete", return_value={}) as mock_delete:
            client.projects.delete("p1")
        mock_delete.assert_called_once_with("/api/projects/p1")
        client.close()

    def test_status(self):
        client = _make_client()
        mock_data = {
            "project_id": "p1",
            "slug": "proj_abc",
            "name": "Test",
            "is_active": True,
            "has_api_key": True,
            "has_policy": True,
            "rule_count": 12,
            "is_ready": True,
            "violations_total": 45,
            "violations_24h": 3,
        }
        with patch.object(client._http, "get", return_value=mock_data):
            status = client.projects.status("p1")
        assert isinstance(status, ProjectStatus)
        assert status.is_ready is True
        assert status.rule_count == 12
        assert status.violations_24h == 3
        client.close()

    def test_rotate_slug(self):
        client = _make_client()
        with patch.object(client._http, "post", return_value={"slug": "proj_newslug"}) as mock:
            new_slug = client.projects.rotate_slug("p1")
        assert new_slug == "proj_newslug"
        mock.assert_called_once_with("/api/projects/p1/rotate-slug")
        client.close()


# ── Policies Resource Tests ──────────────────────────────


class TestPolicies:
    def test_list(self):
        client = _make_client()
        mock_data = [
            {
                "id": "pol_1",
                "name": "Expense Policy",
                "policy_text": "All expenses...",
                "rules": [{"id": "R001"}],
                "rule_count": 1,
                "is_active": True,
            }
        ]
        with patch.object(client._http, "get", return_value=mock_data):
            policies = client.policies.list("p1")
        assert len(policies) == 1
        assert isinstance(policies[0], Policy)
        assert policies[0].id == "pol_1"
        client.close()

    def test_create(self):
        client = _make_client()
        mock_data = {
            "ok": True,
            "policy_id": "pol_1",
            "rules": [{"id": "R001"}, {"id": "R002"}],
            "rule_count": 2,
            "model": "gpt-4o",
            "timing_ms": 1500,
        }
        with patch.object(client._http, "post", return_value=mock_data) as mock_post:
            result = client.policies.create("p1", text="All expenses require receipts", name="v1")
        assert isinstance(result, PolicyCreateResult)
        assert result.ok is True
        assert result.rule_count == 2
        assert result.timing_ms == 1500
        assert result.status == "ready"
        mock_post.assert_called_once_with(
            "/api/projects/p1/policies",
            json={
                "policy_text": "All expenses require receipts",
                "name": "v1",
            },
        )
        client.close()

    def test_create_polls_on_202(self):
        client = _make_client()
        post_data = {
            "ok": True,
            "policy_id": "pol_1",
            "status": "extracting",
            "event_id": "evt_abc123",
        }
        fetched_policies = [
            {
                "id": "pol_1",
                "name": "v1",
                "policy_text": "All expenses...",
                "rules": [{"id": "R001"}, {"id": "R002"}],
                "rule_count": 2,
            }
        ]
        inngest_resp = MagicMock(spec=httpx.Response)
        inngest_resp.is_success = True
        inngest_resp.json.return_value = {"data": [{"status": "Completed"}]}

        with (
            patch.object(client._http, "post", return_value=post_data),
            patch.object(client._http, "get", return_value=fetched_policies),
            patch("synkro.enterprise.resources.policies.httpx.get", return_value=inngest_resp),
            patch("synkro.enterprise.resources.policies.time.sleep"),
        ):
            result = client.policies.create("p1", text="All expenses require receipts")
        assert isinstance(result, PolicyCreateResult)
        assert result.status == "ready"
        assert result.rule_count == 2
        assert result.rules == [{"id": "R001"}, {"id": "R002"}]
        client.close()

    def test_create_poll_failure_raises(self):
        client = _make_client()
        post_data = {
            "ok": True,
            "policy_id": "pol_1",
            "status": "extracting",
            "event_id": "evt_abc123",
        }
        inngest_resp = MagicMock(spec=httpx.Response)
        inngest_resp.is_success = True
        inngest_resp.json.return_value = {"data": [{"status": "Failed"}]}

        with (
            patch.object(client._http, "post", return_value=post_data),
            patch("synkro.enterprise.resources.policies.httpx.get", return_value=inngest_resp),
            patch("synkro.enterprise.resources.policies.time.sleep"),
            pytest.raises(SynkroError, match="extraction failed"),
        ):
            client.policies.create("p1", text="All expenses require receipts")
        client.close()

    def test_update(self):
        client = _make_client()
        with patch.object(client._http, "patch", return_value={}) as mock_patch:
            client.policies.update(
                "p1",
                "pol_1",
                name="v2",
                rule_updates=[{"rule_id": "R001", "mode": "blocking"}],
            )
        mock_patch.assert_called_once_with(
            "/api/projects/p1/policies",
            json={
                "policy_id": "pol_1",
                "name": "v2",
                "rule_updates": [{"rule_id": "R001", "mode": "blocking"}],
            },
        )
        client.close()

    def test_deactivate(self):
        client = _make_client()
        with patch.object(client._http, "delete", return_value={}) as mock_delete:
            client.policies.deactivate("p1", "pol_1")
        mock_delete.assert_called_once_with(
            "/api/projects/p1/policies", params={"policy_id": "pol_1"}
        )
        client.close()


# ── Integrations Resource Tests ──────────────────────────


class TestIntegrations:
    def test_langsmith_status(self):
        client = _make_client()
        mock_data = {"connected": True, "id": "ls_1", "project_count": 3}
        with patch.object(client._http, "get", return_value=mock_data):
            conn = client.integrations.langsmith_status()
        assert isinstance(conn, LangSmithConnection)
        assert conn.connected is True
        assert conn.project_count == 3
        client.close()

    def test_connect_langsmith(self):
        client = _make_client()
        mock_data = {"connected": True, "id": "ls_1", "status": "active"}
        with patch.object(client._http, "post", return_value=mock_data) as mock_post:
            conn = client.integrations.connect_langsmith(api_key="lsv2_xxx")
        assert conn.connected is True
        mock_post.assert_called_once_with(
            "/api/integrations/langsmith",
            json={"api_key": "lsv2_xxx", "base_url": "https://api.smith.langchain.com"},
        )
        client.close()

    def test_disconnect_langsmith(self):
        client = _make_client()
        with patch.object(client._http, "delete", return_value={}) as mock_delete:
            client.integrations.disconnect_langsmith()
        mock_delete.assert_called_once_with("/api/integrations/langsmith")
        client.close()

    def test_langsmith_projects(self):
        client = _make_client()
        mock_data = [{"name": "proj-a"}, {"name": "proj-b"}]
        with patch.object(client._http, "get", return_value=mock_data):
            projects = client.integrations.langsmith_projects()
        assert len(projects) == 2
        client.close()

    def test_langsmith_toggle(self):
        client = _make_client()
        with patch.object(client._http, "post", return_value={}) as mock_post:
            client.integrations.langsmith_toggle("p1", enabled=True, langsmith_project="my-proj")
        mock_post.assert_called_once_with(
            "/api/integrations/langsmith/toggle",
            json={"project_id": "p1", "enabled": True, "langsmith_project": "my-proj"},
        )
        client.close()

    def test_langsmith_create_dataset(self):
        client = _make_client()
        mock_data = {"dataset_id": "ds_1", "example_count": 5}
        with patch.object(client._http, "post", return_value=mock_data) as mock_post:
            result = client.integrations.langsmith_create_dataset(
                name="test-ds", description="Test dataset"
            )
        assert isinstance(result, DatasetCreateResult)
        assert result.dataset_id == "ds_1"
        assert result.example_count == 5
        mock_post.assert_called_once_with(
            "/api/integrations/langsmith/datasets",
            json={"name": "test-ds", "description": "Test dataset"},
        )
        client.close()


# ── Type Tests ───────────────────────────────────────────


class TestTypes:
    def test_project_optional_fields(self):
        p = Project(id="p1", slug="s", name="n")
        assert p.provider is None
        assert p.is_active is True
        assert p.gateway_url is None
        assert p.created_at is None

    def test_policy_defaults(self):
        p = Policy(id="pol_1", name="n", policy_text="t")
        assert p.rules == []
        assert p.rule_count == 0
        assert p.is_active is True

    def test_langsmith_connection_defaults(self):
        c = LangSmithConnection(connected=False)
        assert c.project_count == 0
        assert c.id is None

    def test_policy_create_result_optional(self):
        r = PolicyCreateResult(ok=True, policy_id="pol_1")
        assert r.status == "ready"
        assert r.event_id is None
        assert r.rules == []
        assert r.model is None
        assert r.timing_ms is None


# ── Gateway Tests ────────────────────────────────────────


class TestGateway:
    def _make_gw_client(self, gateway_url="https://gateway.synkro.sh/v1/projects/my-slug"):
        return Synkro(
            api_key="sk-test-123",
            gateway_url=gateway_url,
            base_url="http://localhost:3000",
        )

    def test_gateway_returns_dict(self):
        client = self._make_gw_client()
        mock_openai = MagicMock()
        mock_async_openai = MagicMock()
        with patch.dict(
            "sys.modules",
            {"openai": MagicMock(OpenAI=mock_openai, AsyncOpenAI=mock_async_openai)},
        ):
            result = client.gateway(api_key="provider-key-123", provider="google")
        assert "client" in result
        assert "async_client" in result
        assert result["api_key"] == "provider-key-123"
        client.close()

    def test_gateway_with_provider_and_user_id(self):
        client = self._make_gw_client()
        mock_openai = MagicMock()
        mock_async_openai = MagicMock()
        with patch.dict(
            "sys.modules",
            {"openai": MagicMock(OpenAI=mock_openai, AsyncOpenAI=mock_async_openai)},
        ):
            client.gateway(
                api_key="provider-key-123",
                user_id="user-42",
                provider="google",
            )
        # Verify OpenAI clients were created with correct headers
        sync_call = mock_openai.call_args
        assert sync_call.kwargs["base_url"] == "https://gateway.synkro.sh/v1/projects/my-slug"
        assert sync_call.kwargs["api_key"] == "provider-key-123"
        assert sync_call.kwargs["default_headers"]["x-synkro-api-key"] == "sk-test-123"
        assert sync_call.kwargs["default_headers"]["x-synkro-provider"] == "google"
        assert sync_call.kwargs["default_headers"]["x-synkro-user-id"] == "user-42"
        client.close()

    def test_gateway_minimal(self):
        client = self._make_gw_client()
        mock_openai = MagicMock()
        mock_async_openai = MagicMock()
        with patch.dict(
            "sys.modules",
            {"openai": MagicMock(OpenAI=mock_openai, AsyncOpenAI=mock_async_openai)},
        ):
            result = client.gateway(api_key="sk-xxx")
        sync_call = mock_openai.call_args
        assert sync_call.kwargs["default_headers"] == {"x-synkro-api-key": "sk-test-123"}
        assert result["api_key"] == "sk-xxx"
        client.close()

    def test_gateway_no_url_raises(self):
        client = _make_client()  # no gateway_url
        with pytest.raises(ValueError, match="No gateway_url configured"):
            client.gateway(api_key="sk-xxx")
        client.close()

    def test_gateway_import_error(self):
        client = self._make_gw_client()
        with patch.dict("sys.modules", {"openai": None}):
            with pytest.raises(ImportError, match="openai is required"):
                client.gateway(api_key="sk-xxx")
        client.close()


class TestCreateHeaders:
    def test_all_fields(self):
        from synkro.enterprise import createHeaders

        headers = createHeaders(api_key="sk-abc", provider="openai", user_id="u1")
        assert headers == {
            "x-synkro-api-key": "sk-abc",
            "x-synkro-provider": "openai",
            "x-synkro-user-id": "u1",
        }

    def test_minimal(self):
        from synkro.enterprise import createHeaders

        headers = createHeaders(api_key="sk-abc")
        assert headers == {"x-synkro-api-key": "sk-abc"}


# ── Error Class Tests ────────────────────────────────────


class TestErrors:
    def test_synkro_error_is_exception(self):
        with pytest.raises(Exception):
            raise SynkroAuthError("test")

    def test_rate_limit_retry_after(self):
        err = SynkroRateLimitError("limited", retry_after="60")
        assert err.retry_after == "60"
        assert str(err) == "limited"

    def test_api_error_status_code(self):
        err = SynkroAPIError("bad", status_code=422)
        assert err.status_code == 422

    def test_not_found_is_api_error(self):
        err = SynkroNotFoundError("gone")
        assert isinstance(err, SynkroAPIError)
        assert err.status_code == 404
