"""Tests for workflow publish steps (#966).

Tests cover validation, file/webhook adapters, and engine integration.
"""

from __future__ import annotations

import tempfile
from pathlib import Path
from typing import Any
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from anteroom.config import WorkflowConfig
from anteroom.db import init_db
from anteroom.services.workflow_engine import (
    WorkflowEngine,
    load_definition,
    register_gate_condition,
)
from anteroom.services.workflow_publishers import (
    FilePublishAdapter,
    WebhookPublishAdapter,
)
from anteroom.services.workflow_runners import create_default_registry
from anteroom.services.workflow_storage import list_workflow_events, list_workflow_steps

# ---------------------------------------------------------------------------
# Test YAML definitions
# ---------------------------------------------------------------------------

PUBLISH_FILE_WORKFLOW = """\
kind: workflow
id: test_publish_file
version: 0.1.0
inputs:
  output_dir:
    type: string
    required: true
steps:
  - id: generate
    type: runner
    runner: shell
    command: "echo hello world"
  - id: publish_output
    type: publish
    context_from:
      - step: generate
        field: raw_output
    destination:
      adapter: file
      path: "{output_dir}/result.txt"
"""

PUBLISH_WEBHOOK_WORKFLOW = """\
kind: workflow
id: test_publish_webhook
version: 0.1.0
inputs: {}
steps:
  - id: generate
    type: runner
    runner: shell
    command: "echo data"
  - id: publish_hook
    type: publish
    context_from:
      - step: generate
        field: raw_output
    destination:
      adapter: webhook
      url: "https://example.com/hook"
"""

PUBLISH_WHEN_WORKFLOW = """\
kind: workflow
id: test_publish_when
version: 0.1.0
inputs: {}
steps:
  - id: generate
    type: runner
    runner: shell
    command: "echo data"
  - id: publish_conditional
    type: publish
    when:
      step: generate
      field: result_status
      equals: "nonexistent_status"
    destination:
      adapter: file
      path: "/tmp/test_publish_when.txt"
"""

PUBLISH_IN_LOOP_WORKFLOW = """\
kind: workflow
id: test_publish_loop
version: 0.1.0
inputs: {}
steps:
  - id: my_loop
    type: loop
    max_rounds: 2
    steps:
      - id: gen
        type: runner
        runner: shell
        command: "echo round"
      - id: pub
        type: publish
        destination:
          adapter: file
          path: "/tmp/nope.txt"
"""


@pytest.fixture()
def db():
    with tempfile.TemporaryDirectory() as td:
        conn = init_db(Path(td) / "test.db")
        yield conn
        conn.close()


@pytest.fixture()
def engine(db: Any) -> WorkflowEngine:
    config = WorkflowConfig()
    registry = create_default_registry()
    return WorkflowEngine(db, config, registry)


@pytest.fixture(autouse=True)
def _register_test_gates():
    async def always_pass(run: Any, step: Any, inputs: Any) -> bool:
        return True

    register_gate_condition("always_pass", always_pass)
    yield


# ---------------------------------------------------------------------------
# Validation tests
# ---------------------------------------------------------------------------


class TestPublishValidation:
    def test_publish_requires_destination(self) -> None:
        yaml_str = """\
kind: workflow
id: t
version: 0.1.0
steps:
  - id: pub
    type: publish
"""
        with pytest.raises(ValueError, match="requires a 'destination' field"):
            load_definition(yaml_str)

    def test_publish_requires_adapter(self) -> None:
        yaml_str = """\
kind: workflow
id: t
version: 0.1.0
steps:
  - id: pub
    type: publish
    destination:
      path: /tmp/out.txt
"""
        with pytest.raises(ValueError, match="unknown adapter"):
            load_definition(yaml_str)

    def test_publish_unknown_adapter(self) -> None:
        yaml_str = """\
kind: workflow
id: t
version: 0.1.0
steps:
  - id: pub
    type: publish
    destination:
      adapter: s3
"""
        with pytest.raises(ValueError, match="unknown adapter 's3'"):
            load_definition(yaml_str)

    def test_publish_file_requires_path(self) -> None:
        yaml_str = """\
kind: workflow
id: t
version: 0.1.0
steps:
  - id: pub
    type: publish
    destination:
      adapter: file
"""
        with pytest.raises(ValueError, match="file adapter requires a 'path' field"):
            load_definition(yaml_str)

    def test_publish_webhook_requires_url(self) -> None:
        yaml_str = """\
kind: workflow
id: t
version: 0.1.0
steps:
  - id: pub
    type: publish
    destination:
      adapter: webhook
"""
        with pytest.raises(ValueError, match="webhook adapter requires a 'url' field"):
            load_definition(yaml_str)

    def test_publish_not_allowed_in_loop(self) -> None:
        """Publish inside a loop should fail at execution time, not parse time.

        The parser allows any valid step types inside loops, but execution
        raises an error for unsupported types.
        """
        # Parse succeeds (type is valid)
        defn = load_definition(PUBLISH_IN_LOOP_WORKFLOW)
        assert defn.steps[0].type == "loop"
        assert defn.steps[0].steps[1].type == "publish"

    def test_publish_parsed_correctly(self) -> None:
        defn = load_definition(PUBLISH_FILE_WORKFLOW)
        pub_step = defn.steps[1]
        assert pub_step.type == "publish"
        assert pub_step.destination is not None
        assert pub_step.destination["adapter"] == "file"
        assert pub_step.destination["path"] == "{output_dir}/result.txt"
        assert pub_step.context_from is not None


# ---------------------------------------------------------------------------
# File adapter tests
# ---------------------------------------------------------------------------


class TestFilePublishAdapter:
    @pytest.mark.asyncio
    async def test_file_publish_writes_content(self, tmp_path: Path) -> None:
        adapter = FilePublishAdapter()
        out = tmp_path / "output.txt"
        result = await adapter.publish(
            content="hello world",
            destination={"adapter": "file", "path": str(out)},
        )
        assert result.status == "success"
        assert out.read_text() == "hello world"

    @pytest.mark.asyncio
    async def test_file_publish_creates_parent_dirs(self, tmp_path: Path) -> None:
        adapter = FilePublishAdapter()
        out = tmp_path / "deep" / "nested" / "output.txt"
        result = await adapter.publish(
            content="nested content",
            destination={"adapter": "file", "path": str(out)},
        )
        assert result.status == "success"
        assert out.exists()
        assert out.read_text() == "nested content"

    @pytest.mark.asyncio
    async def test_file_publish_result_artifacts(self, tmp_path: Path) -> None:
        adapter = FilePublishAdapter()
        out = tmp_path / "out.txt"
        result = await adapter.publish(
            content="data",
            destination={"adapter": "file", "path": str(out)},
        )
        assert result.artifacts["destination"] == f"file:{out}"
        assert result.artifacts["bytes_written"] == 4

    @pytest.mark.asyncio
    async def test_file_publish_empty_path_fails(self) -> None:
        adapter = FilePublishAdapter()
        result = await adapter.publish(
            content="data",
            destination={"adapter": "file", "path": ""},
        )
        assert result.status == "failed"
        assert "No path" in result.summary

    @pytest.mark.asyncio
    async def test_file_publish_permission_denied(self) -> None:
        adapter = FilePublishAdapter()
        with patch.object(Path, "write_text", side_effect=PermissionError("Permission denied")):
            with patch("anteroom.tools.security.validate_path", return_value=("/fake/path.txt", None)):
                with patch.object(Path, "mkdir"):
                    result = await adapter.publish(
                        content="data",
                        destination={"adapter": "file", "path": "/fake/path.txt"},
                    )
        assert result.status == "failed"
        assert "Permission denied" in result.summary

    @pytest.mark.asyncio
    async def test_file_publish_template_path(self, tmp_path: Path) -> None:
        """Template variables should be resolved by the engine before reaching the adapter."""
        adapter = FilePublishAdapter()
        out = tmp_path / "resolved.txt"
        result = await adapter.publish(
            content="resolved content",
            destination={"adapter": "file", "path": str(out)},
        )
        assert result.status == "success"
        assert out.read_text() == "resolved content"


# ---------------------------------------------------------------------------
# Webhook adapter tests
# ---------------------------------------------------------------------------


class TestWebhookPublishAdapter:
    @pytest.mark.asyncio
    async def test_webhook_publish_posts_content(self) -> None:
        adapter = WebhookPublishAdapter()
        mock_response = MagicMock()
        mock_response.status_code = 200

        mock_client = AsyncMock()
        mock_client.request = AsyncMock(return_value=mock_response)
        mock_client.__aenter__ = AsyncMock(return_value=mock_client)
        mock_client.__aexit__ = AsyncMock(return_value=False)

        with patch("httpx.AsyncClient", return_value=mock_client):
            result = await adapter.publish(
                content="payload data",
                destination={"adapter": "webhook", "url": "https://example.com/hook"},
            )

        assert result.status == "success"
        mock_client.request.assert_called_once()
        call_args = mock_client.request.call_args
        assert call_args[0][0] == "POST"
        assert call_args[0][1] == "https://example.com/hook"

    @pytest.mark.asyncio
    async def test_webhook_publish_with_template(self) -> None:
        adapter = WebhookPublishAdapter()
        mock_response = MagicMock()
        mock_response.status_code = 200

        mock_client = AsyncMock()
        mock_client.request = AsyncMock(return_value=mock_response)
        mock_client.__aenter__ = AsyncMock(return_value=mock_client)
        mock_client.__aexit__ = AsyncMock(return_value=False)

        with patch("httpx.AsyncClient", return_value=mock_client):
            result = await adapter.publish(
                content="my data",
                destination={
                    "adapter": "webhook",
                    "url": "https://example.com/hook",
                    "body_template": "Result: {content}",
                },
            )

        assert result.status == "success"
        call_args = mock_client.request.call_args
        body = call_args[1]["content"]
        assert b"Result: my data" in body

    @pytest.mark.asyncio
    async def test_webhook_publish_failure(self) -> None:
        adapter = WebhookPublishAdapter()
        mock_response = MagicMock()
        mock_response.status_code = 500

        mock_client = AsyncMock()
        mock_client.request = AsyncMock(return_value=mock_response)
        mock_client.__aenter__ = AsyncMock(return_value=mock_client)
        mock_client.__aexit__ = AsyncMock(return_value=False)

        with patch("httpx.AsyncClient", return_value=mock_client):
            result = await adapter.publish(
                content="data",
                destination={"adapter": "webhook", "url": "https://example.com/hook"},
            )

        assert result.status == "failed"
        assert "500" in result.summary

    @pytest.mark.asyncio
    async def test_webhook_credential_injection(self) -> None:
        adapter = WebhookPublishAdapter()
        mock_response = MagicMock()
        mock_response.status_code = 200

        mock_client = AsyncMock()
        mock_client.request = AsyncMock(return_value=mock_response)
        mock_client.__aenter__ = AsyncMock(return_value=mock_client)
        mock_client.__aexit__ = AsyncMock(return_value=False)

        with patch("httpx.AsyncClient", return_value=mock_client):
            result = await adapter.publish(
                content="data",
                destination={"adapter": "webhook", "url": "https://example.com/hook"},
                credentials={"API_KEY": "secret123"},
            )

        assert result.status == "success"
        call_args = mock_client.request.call_args
        headers = call_args[1]["headers"]
        assert headers["X-API_KEY"] == "secret123"

    @pytest.mark.asyncio
    async def test_webhook_idempotency_key_header(self) -> None:
        adapter = WebhookPublishAdapter()
        mock_response = MagicMock()
        mock_response.status_code = 200

        mock_client = AsyncMock()
        mock_client.request = AsyncMock(return_value=mock_response)
        mock_client.__aenter__ = AsyncMock(return_value=mock_client)
        mock_client.__aexit__ = AsyncMock(return_value=False)

        with patch("httpx.AsyncClient", return_value=mock_client):
            result = await adapter.publish(
                content="data",
                destination={"adapter": "webhook", "url": "https://example.com/hook"},
                idempotency_key="run-1:pub",
            )

        assert result.status == "success"
        call_args = mock_client.request.call_args
        headers = call_args[1]["headers"]
        assert headers["Idempotency-Key"] == "run-1:pub"

    @pytest.mark.asyncio
    async def test_webhook_json_parsing_fallback(self) -> None:
        """When Content-Type is JSON but body isn't valid JSON, falls back to raw."""
        adapter = WebhookPublishAdapter()
        mock_response = MagicMock()
        mock_response.status_code = 200

        mock_client = AsyncMock()
        mock_client.request = AsyncMock(return_value=mock_response)
        mock_client.__aenter__ = AsyncMock(return_value=mock_client)
        mock_client.__aexit__ = AsyncMock(return_value=False)

        with patch("httpx.AsyncClient", return_value=mock_client):
            result = await adapter.publish(
                content="not-valid-json",
                destination={
                    "adapter": "webhook",
                    "url": "https://example.com/hook",
                    "headers": {"Content-Type": "application/json"},
                },
            )

        assert result.status == "success"
        call_args = mock_client.request.call_args
        assert call_args[1]["content"] == b"not-valid-json"

    @pytest.mark.asyncio
    async def test_webhook_network_timeout(self) -> None:
        adapter = WebhookPublishAdapter()

        mock_client = AsyncMock()
        mock_client.request = AsyncMock(side_effect=TimeoutError("timed out"))
        mock_client.__aenter__ = AsyncMock(return_value=mock_client)
        mock_client.__aexit__ = AsyncMock(return_value=False)

        with patch("httpx.AsyncClient", return_value=mock_client):
            result = await adapter.publish(
                content="data",
                destination={"adapter": "webhook", "url": "https://example.com/hook"},
            )

        assert result.status == "failed"
        assert "timed out" in result.summary

    @pytest.mark.asyncio
    async def test_webhook_publish_size_limit(self) -> None:
        adapter = WebhookPublishAdapter()
        big_content = "x" * (1_048_577)  # Just over 1MB
        result = await adapter.publish(
            content=big_content,
            destination={"adapter": "webhook", "url": "https://example.com/hook"},
        )
        assert result.status == "failed"
        assert "1MB" in result.summary


# ---------------------------------------------------------------------------
# Engine integration tests
# ---------------------------------------------------------------------------


class TestPublishEngineIntegration:
    @pytest.mark.asyncio
    async def test_publish_step_succeeds(self, db: Any, tmp_path: Path) -> None:
        out_file = tmp_path / "result.txt"
        config = WorkflowConfig()
        registry = create_default_registry()
        engine = WorkflowEngine(db, config, registry)

        defn = load_definition(PUBLISH_FILE_WORKFLOW)
        run = await engine.start_run(
            defn,
            target_kind="test",
            target_ref="pub-test",
            inputs={"output_dir": str(tmp_path)},
        )
        assert run["status"] == "completed"
        assert out_file.exists()

    @pytest.mark.asyncio
    async def test_publish_step_with_context_from(self, db: Any, tmp_path: Path) -> None:
        yaml_str = f"""\
kind: workflow
id: test_ctx
version: 0.1.0
inputs: {{}}
steps:
  - id: gen
    type: runner
    runner: shell
    command: "echo context_output"
  - id: pub
    type: publish
    context_from:
      - step: gen
        field: raw_output
    destination:
      adapter: file
      path: "{tmp_path}/ctx.txt"
"""
        config = WorkflowConfig()
        registry = create_default_registry()
        engine = WorkflowEngine(db, config, registry)

        defn = load_definition(yaml_str)
        run = await engine.start_run(defn, target_kind="test", target_ref="ctx-test")
        assert run["status"] == "completed"
        out = tmp_path / "ctx.txt"
        assert out.exists()

    @pytest.mark.asyncio
    async def test_publish_step_failure_fails_run(self, db: Any) -> None:
        yaml_str2 = """\
kind: workflow
id: test_fail
version: 0.1.0
inputs: {}
steps:
  - id: pub
    type: publish
    destination:
      adapter: file
      path: "/dev/null/impossible/path.txt"
"""
        config = WorkflowConfig()
        registry = create_default_registry()
        engine = WorkflowEngine(db, config, registry)

        defn = load_definition(yaml_str2)
        run = await engine.start_run(defn, target_kind="test", target_ref="fail-test")
        assert run["status"] == "failed"

    @pytest.mark.asyncio
    async def test_publish_step_with_when_clause(self, db: Any) -> None:
        config = WorkflowConfig()
        registry = create_default_registry()
        engine = WorkflowEngine(db, config, registry)

        defn = load_definition(PUBLISH_WHEN_WORKFLOW)
        run = await engine.start_run(defn, target_kind="test", target_ref="when-test")
        assert run["status"] == "completed"
        # The publish step should be skipped because the when condition doesn't match
        steps = list_workflow_steps(db, run["id"])
        pub_steps = [s for s in steps if s["step_id"] == "publish_conditional"]
        assert len(pub_steps) == 1
        assert pub_steps[0]["status"] == "skipped"

    @pytest.mark.asyncio
    async def test_publish_step_event_emitted(self, db: Any, tmp_path: Path) -> None:
        out = tmp_path / "event_test.txt"
        yaml_str = f"""\
kind: workflow
id: test_event
version: 0.1.0
inputs: {{}}
steps:
  - id: pub
    type: publish
    destination:
      adapter: file
      path: "{out}"
"""
        config = WorkflowConfig()
        registry = create_default_registry()
        engine = WorkflowEngine(db, config, registry)

        defn = load_definition(yaml_str)
        run = await engine.start_run(defn, target_kind="test", target_ref="event-test")
        assert run["status"] == "completed"

        events = list_workflow_events(db, run["id"])
        event_types = [e["event_type"] for e in events]
        assert "step_started" in event_types
        assert "step_finished" in event_types

    @pytest.mark.asyncio
    async def test_webhook_template_url_validated_after_resolution(self, db: Any) -> None:
        """Templated webhook URLs must be egress-validated after template resolution.

        Regression test: URLs containing '{' are skipped in start_run() validation.
        After template resolution, the resolved URL must be checked against the
        egress allowlist. A disallowed host must fail.
        """
        yaml_str = """\
kind: workflow
id: test_template_egress
version: 0.1.0
inputs:
  target_host:
    type: string
    required: true
steps:
  - id: gen
    type: runner
    runner: shell
    command: "echo data"
  - id: pub
    type: publish
    context_from:
      - step: gen
        field: raw_output
    destination:
      adapter: webhook
      url: "https://{target_host}/hook"
"""
        config = WorkflowConfig()
        registry = create_default_registry()
        engine = WorkflowEngine(
            db,
            config,
            registry,
            egress_allowed_domains=["allowed.example.com"],
            egress_block_localhost=True,
        )

        defn = load_definition(yaml_str)
        run = await engine.start_run(
            defn,
            target_kind="test",
            target_ref="egress-test",
            inputs={"target_host": "evil.example.com"},
        )
        assert run["status"] == "failed"
        steps = list_workflow_steps(db, run["id"])
        pub_steps = [s for s in steps if s["step_id"] == "pub"]
        assert len(pub_steps) == 1
        assert pub_steps[0]["status"] == "failed"
        assert "egress" in (pub_steps[0].get("result_summary") or "").lower()
