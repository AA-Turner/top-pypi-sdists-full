"""Tests for JiraProvider idempotent reruns."""

from __future__ import annotations

from unittest.mock import MagicMock

from agentic_devtools.adapters.jira_provider import JiraProvider
from agentic_devtools.adapters.orchestration_key import embed_orchestration_key, generate_orchestration_key
from tests.unit.adapters.jira_provider._fixtures import _make_mock_session, _make_response


class TestJiraIdempotentRerunFlow:
    """Verify idempotent re-run creates 0 duplicates for Jira provider."""

    def test_jira_rerun_finds_existing(self):
        orch_key = generate_orchestration_key("create_issue", "epic.features[0]")
        session = _make_mock_session()

        def mock_request(method, url, **kwargs):
            resp = MagicMock()
            resp.status_code = 200
            resp.text = "{}"
            resp.raise_for_status = MagicMock()
            if "/search" in url:
                resp.json.return_value = {"issues": [{"key": "PROJ-99", "id": "10099"}]}
            else:
                resp.json.return_value = {}
            return resp

        session.request.side_effect = mock_request
        provider = JiraProvider(project_key="PROJ", base_url="https://jira.example.com", session=session)
        body = embed_orchestration_key("Body", orch_key)

        result = provider.create_issue("Title", body, "task", dry_run=False)
        assert result.status == "existing"
        assert result.identifier == "PROJ-99"

    def test_idempotency_key_recovers_from_fresh_provider_instance(self):
        """A fresh provider instance (empty in-memory cache) must still find a
        previously created issue when the same ``idempotency_key`` is passed,
        because ``create_issue`` embeds the key into the description at
        creation time and a later run's remote search can match on it."""
        orch_key = generate_orchestration_key("create_issue", "tree-1", "e1")

        creating_session = _make_mock_session()
        creating_session.request.return_value = _make_response(201, {"key": "PROJ-1", "id": "10001"})
        first_provider = JiraProvider(project_key="PROJ", base_url="https://jira.example.com", session=creating_session)
        created = first_provider.create_issue("Epic", "Body", "epic", idempotency_key=orch_key, dry_run=False)
        assert created.status == "created"
        embedded_body = creating_session.request.call_args.kwargs["json"]["fields"]["description"]
        assert f"agdt-orch-key:{orch_key}" in embedded_body

        def mock_request(method, url, **kwargs):
            resp = MagicMock()
            resp.status_code = 200
            resp.text = "{}"
            resp.raise_for_status = MagicMock()
            if "/search" in url:
                resp.json.return_value = {"issues": [{"key": "PROJ-1", "id": "10001"}]}
            else:
                resp.json.return_value = {}
            return resp

        recovery_session = _make_mock_session()
        recovery_session.request.side_effect = mock_request
        fresh_provider = JiraProvider(project_key="PROJ", base_url="https://jira.example.com", session=recovery_session)

        recovered = fresh_provider.create_issue("Epic", "Body", "epic", idempotency_key=orch_key, dry_run=False)
        assert recovered.status == "existing"
        assert recovered.identifier == "PROJ-1"
        # Only the JQL search was issued â€” no duplicate POST /issue was made.
        assert all("/search" in call.args[1] for call in recovery_session.request.call_args_list)
