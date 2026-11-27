import importlib
import json
import logging
import os
import subprocess
import sys
from pathlib import Path
from typing import Any
from unittest.mock import AsyncMock, patch

import pytest
from pydantic import ValidationError
from pydantic_settings.exceptions import SettingsError
from structlog.testing import capture_logs

from mistralai.workflows import AgentConfig, WorkerConfig, WorkflowsConfig, run_worker
from mistralai.workflows.core.config.config import config as legacy_config
from mistralai.workflows.core.config.config import get_config_from_env, resolve_worker_config


@pytest.mark.asyncio
async def test_run_worker_accepts_explicit_config_without_worker_environment(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.delenv("DEPLOYMENT_NAME", raising=False)
    explicit_config = WorkflowsConfig(
        worker=WorkerConfig(
            deployment_name="code-deployment",
            enable_config_discovery=False,
            server_url="https://code.example",
        )
    )

    async def assert_runtime_config(_workflows, resolved_config, **_kwargs) -> None:
        assert legacy_config is not resolved_config
        assert legacy_config.worker.server_url == "https://code.example"

    with patch(
        "mistralai.workflows.core.worker._run_worker",
        new_callable=AsyncMock,
        side_effect=assert_runtime_config,
    ) as worker:
        with pytest.warns(UserWarning, match="Disabling automatic config discovery"):
            await run_worker([], config=explicit_config)

    worker.assert_awaited_once()
    resolved_config = worker.await_args.args[1]
    assert resolved_config is not explicit_config
    assert resolved_config.worker.deployment_name == "code-deployment"


def test_environment_is_resolved_when_config_is_constructed(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("SERVER_URL", "https://first.example")
    first = WorkflowsConfig()
    monkeypatch.setenv("SERVER_URL", "https://second.example")
    second = WorkflowsConfig()

    assert first.worker.server_url == "https://first.example"
    assert second.worker.server_url == "https://second.example"


def test_environment_only_worker_config_is_resolved_for_each_startup(monkeypatch: pytest.MonkeyPatch) -> None:
    config_module = importlib.import_module("mistralai.workflows.core.config.config")
    lazy_config = config_module._lazy_config
    previously_loaded_config = lazy_config.get_if_loaded()
    object.__setattr__(lazy_config, "_value", None)
    try:
        monkeypatch.setenv("SERVER_URL", "https://first.example")
        first = resolve_worker_config(None)
        monkeypatch.setenv("SERVER_URL", "https://second.example")
        second = resolve_worker_config(None)
    finally:
        object.__setattr__(lazy_config, "_value", previously_loaded_config)

    assert first.worker.server_url == "https://first.example"
    assert second.worker.server_url == "https://second.example"
    assert first is not second


def test_partial_explicit_config_keeps_environment_values(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("SERVER_URL", "https://environment.example")

    config = resolve_worker_config(WorkflowsConfig(worker=WorkerConfig(deployment_name="code-deployment")))

    assert config.worker.deployment_name == "code-deployment"
    assert config.worker.server_url == "https://environment.example"


@pytest.fixture(params=["environment", "dotenv", "secrets"])
def inherited_setting(monkeypatch: pytest.MonkeyPatch, tmp_path: Path, request: pytest.FixtureRequest):
    """Set one setting from the environment, a dotenv file or a secrets file, and return the matching kwargs."""
    dotenv = tmp_path / ".env"
    secrets = tmp_path / "secrets"
    secrets.mkdir()

    def set_value(name: str, value: dict[str, Any]) -> dict[str, Any]:
        data = json.dumps(value)
        monkeypatch.delenv(name, raising=False)
        if request.param == "environment":
            monkeypatch.setenv(name, data)
        elif request.param == "dotenv":
            dotenv.write_text(f"{name}='{data}'\n")
        else:
            (secrets / name).write_text(data)
        return {"_env_file": dotenv, "_secrets_dir": secrets}

    return set_value


def _dropped_header_warnings(logs: list[dict[str, Any]]) -> dict[str, list[str]]:
    return {
        entry["field"]: entry["discarded_headers"]
        for entry in logs
        if entry["event"] == "Headers set in code replace inherited headers; these inherited headers are not sent"
    }


@pytest.mark.parametrize("field_name", ["mistral_api_headers", "mistral_api_header_files"])
class TestExplicitWorkerHeaders:
    @pytest.mark.parametrize("headers", [{}, None, {"X-Shared": "code", "X-Code": "code"}])
    def test_explicit_headers_replace_inherited_mapping(
        self, inherited_setting, field_name: str, headers: dict[str, str] | None
    ) -> None:
        settings = inherited_setting(field_name.upper(), {"X-Inherited": "inherited", "X-Shared": "inherited"})

        assert getattr(WorkerConfig(**{field_name: headers}, **settings), field_name) == headers

    @pytest.mark.parametrize("headers", [{}, {"X-Code": "code"}])
    def test_nested_override_replaces_worker_setting(self, inherited_setting, field_name: str, headers) -> None:
        settings = inherited_setting("WORKER", {field_name: {"X-Parent": "parent"}, "graph": {"upload_graph": False}})

        config = WorkflowsConfig(worker={field_name: headers, "graph": {"graph_summarise_enabled": False}}, **settings)

        assert getattr(config.worker, field_name) == headers
        assert config.worker.graph.upload_graph is False
        assert config.worker.graph.graph_summarise_enabled is False

    def test_omitted_nested_headers_keep_merging(self, monkeypatch, inherited_setting, field_name: str) -> None:
        settings = inherited_setting("WORKER", {field_name: {"X-Parent": "parent", "X-Shared": "parent"}})
        monkeypatch.setenv(field_name.upper(), '{"X-Direct":"direct","X-Shared":"direct"}')

        config = WorkflowsConfig(worker={"deployment_name": "code-deployment"}, **settings)

        assert getattr(config.worker, field_name) == {"X-Direct": "direct", "X-Shared": "parent", "X-Parent": "parent"}

    def test_explicit_header_field_leaves_the_other_field_inherited(self, monkeypatch, field_name: str) -> None:
        monkeypatch.setenv("MISTRAL_API_HEADERS", '{"X-Static":"static"}')
        monkeypatch.setenv("MISTRAL_API_HEADER_FILES", '{"X-File":"file"}')
        other_field, other_value = (
            ("mistral_api_header_files", {"X-File": "file"})
            if field_name == "mistral_api_headers"
            else ("mistral_api_headers", {"X-Static": "static"})
        )

        worker = WorkerConfig(**{field_name: {}}, _env_file=None)

        assert getattr(worker, field_name) == {}
        assert getattr(worker, other_field) == other_value

    def test_explicit_headers_remain_a_serializable_mutable_dict(self, monkeypatch, field_name: str) -> None:
        monkeypatch.setenv(field_name.upper(), '{"X-Direct":"direct"}')
        headers = {"X-Code": "code"}
        config = WorkflowsConfig(worker={field_name: headers})

        resolved_headers = getattr(config.worker, field_name)
        assert type(resolved_headers) is dict
        resolved_headers["X-Added"] = "added"
        assert headers == {"X-Code": "code"}
        assert json.loads(config.worker.model_dump_json())[field_name] == resolved_headers

    @pytest.mark.parametrize("headers", [{"X-Kept": "code"}, None])
    def test_dropped_inherited_headers_are_logged_by_name(
        self, inherited_setting, field_name: str, headers: dict[str, str] | None
    ) -> None:
        settings = inherited_setting(field_name.upper(), {"Authorization": "secret-token", "X-Kept": "inherited"})

        with capture_logs() as logs:
            WorkerConfig(**{field_name: headers}, **settings)

        expected = ["Authorization"] if headers else ["Authorization", "X-Kept"]
        assert _dropped_header_warnings(logs) == {field_name: expected}
        assert "secret-token" not in repr(logs)

    def test_headers_dropped_through_workflows_config_are_logged(self, monkeypatch, field_name: str) -> None:
        monkeypatch.setenv(field_name.upper(), '{"Authorization":"secret-token"}')

        with capture_logs() as logs:
            WorkflowsConfig(worker={field_name: {}}, _env_file=None)

        assert _dropped_header_warnings(logs) == {field_name: ["Authorization"]}

    def test_headers_dropped_from_worker_setting_are_logged(self, monkeypatch, field_name: str) -> None:
        monkeypatch.delenv(field_name.upper(), raising=False)
        monkeypatch.setenv("WORKER", json.dumps({field_name: {"X-Worker": "inherited"}}))

        with capture_logs() as logs:
            WorkflowsConfig(worker={field_name: {"X-Code": "code"}}, _env_file=None)

        assert _dropped_header_warnings(logs) == {field_name: ["X-Worker"]}

    def test_nothing_is_logged_when_no_inherited_header_is_dropped(self, monkeypatch, field_name: str) -> None:
        monkeypatch.setenv(field_name.upper(), '{"X-Kept":"inherited"}')

        with capture_logs() as logs:
            WorkerConfig(**{field_name: {"X-Kept": "code"}}, _env_file=None)
            WorkerConfig(_env_file=None)

        assert _dropped_header_warnings(logs) == {}


def test_explicit_deployment_name_warns_when_it_differs_from_environment(
    monkeypatch: pytest.MonkeyPatch,
    caplog: pytest.LogCaptureFixture,
) -> None:
    monkeypatch.setenv("DEPLOYMENT_NAME", "environment-deployment")
    explicit = WorkflowsConfig(worker=WorkerConfig(deployment_name="code-deployment"))

    with caplog.at_level(logging.WARNING, logger="mistralai.workflows.core.config.config"):
        resolved = resolve_worker_config(explicit)

    assert resolved.worker.deployment_name == "code-deployment"
    assert "Explicit worker deployment name overrides DEPLOYMENT_NAME" in caplog.text
    assert "code-deployment" in caplog.text
    assert "environment-deployment" in caplog.text


def test_deployment_name_warning_ignores_invalid_unrelated_environment(
    monkeypatch: pytest.MonkeyPatch,
    caplog: pytest.LogCaptureFixture,
) -> None:
    explicit = WorkflowsConfig(
        worker=WorkerConfig(
            deployment_name="code-deployment",
            agent=AgentConfig(),
        )
    )
    monkeypatch.setenv("DEPLOYMENT_NAME", "environment-deployment")
    monkeypatch.setenv("BLOB_STORAGE_CONFIGS", "not-json")

    with pytest.raises(SettingsError, match="blob_storage_configs"):
        get_config_from_env()

    with caplog.at_level(logging.WARNING, logger="mistralai.workflows.core.config.config"):
        resolved = resolve_worker_config(explicit)

    assert resolved.worker.deployment_name == "code-deployment"
    assert "Explicit worker deployment name overrides DEPLOYMENT_NAME" in caplog.text
    assert "code-deployment" in caplog.text
    assert "environment-deployment" in caplog.text


def test_empty_explicit_config_uses_sdk_defaults(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("DEPLOYMENT_NAME", raising=False)

    config = WorkflowsConfig()

    assert config.worker.deployment_name is None
    assert config.worker.retry_policy_max_attempts == 3
    assert config.temporal.namespace == "mistral-workflows"
    assert config.http.timeout == 60.0


def test_explicit_worker_config_does_not_mutate_standard_otel_environment(monkeypatch: pytest.MonkeyPatch) -> None:
    host_environment = {
        "OTEL_EXPORTER_OTLP_CERTIFICATE": "/host/ca.pem",
        "OTEL_EXPORTER_OTLP_CLIENT_CERTIFICATE": "/host/client.pem",
        "OTEL_EXPORTER_OTLP_CLIENT_KEY": "/host/client.key",
        "OTEL_EXPORTER_OTLP_HEADERS": "Authorization=Bearer host-token",
    }
    for name, value in host_environment.items():
        monkeypatch.setenv(name, value)

    resolve_worker_config(
        WorkflowsConfig(
            common={
                "ca_bundle": "/worker/ca.pem",
                "mtls_client_cert_path": "/worker/client.pem",
                "mtls_client_key_path": "/worker/client.key",
                "mistral_api_key": "worker-token",
            }
        )
    )
    resolve_worker_config(WorkflowsConfig())

    assert {name: os.environ[name] for name in host_environment} == host_environment


def test_run_worker_resolves_environment_at_invocation_time() -> None:
    script = """
import asyncio
import os
from unittest.mock import AsyncMock, patch

from mistralai.workflows import run_worker

os.environ["DEPLOYMENT_NAME"] = "late-deployment"

async def main():
    with patch("mistralai.workflows.core.worker._run_worker", new_callable=AsyncMock) as worker:
        await run_worker([], enable_config_discovery=False)
    assert worker.await_args.args[1].worker.deployment_name == "late-deployment"

asyncio.run(main())
"""

    result = subprocess.run(
        [sys.executable, "-c", script],
        capture_output=True,
        check=False,
        env=os.environ.copy(),
        text=True,
    )

    assert result.returncode == 0, result.stderr


class TestBareEnvironmentVariables:
    """Bare variables other software exports must not crash or configure the SDK."""

    @pytest.fixture(autouse=True)
    def _isolated_environment(self, monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
        config_module = sys.modules["mistralai.workflows.core.config.config"]
        monkeypatch.setattr(config_module, "_ignored_foreign_env_vars", set())
        monkeypatch.chdir(tmp_path)
        nested = {"agent", "graph", "versioning", "deployment_location", "worker", "common", "temporal", "http"}
        nested.update({"blob_storage_configs", "temporal_payload_encryption", "temporal_payload_offloading"})
        nested.update({"temporal_payload_compression", "activity_attributes_offloading"})
        for name in [name for name in os.environ if name.lower().split("__")[0] in nested]:
            monkeypatch.delenv(name)

    @staticmethod
    def _ignored(logs: list[dict[str, Any]]) -> list[str]:
        return [log["env_variable"] for log in logs if "not a JSON object" in log["event"]]

    @pytest.mark.parametrize("variable", ["AGENT", "GRAPH", "VERSIONING", "DEPLOYMENT_LOCATION", "WORKER"])
    def test_non_json_value_for_a_nested_model_is_ignored_with_a_warning(
        self, monkeypatch: pytest.MonkeyPatch, variable: str
    ) -> None:
        monkeypatch.setenv(variable, "claude-code")

        with capture_logs() as logs:
            get_config_from_env()

        assert self._ignored(logs) == [variable]

    @pytest.mark.parametrize("value", ["claude-code", "", "   ", "null", "[1]", "123"])
    def test_any_value_that_is_not_a_json_object_is_ignored(self, monkeypatch: pytest.MonkeyPatch, value: str) -> None:
        monkeypatch.setenv("AGENT", value)

        with capture_logs() as logs:
            get_config_from_env()

        assert self._ignored(logs) == ["AGENT"]

    def test_the_variable_name_is_matched_case_insensitively(self, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.setenv("agent", "claude-code")

        with capture_logs() as logs:
            get_config_from_env()

        assert self._ignored(logs) == ["AGENT"]

    def test_the_warning_is_logged_once_per_process(self, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.setenv("AGENT", "claude-code")

        with capture_logs() as logs:
            get_config_from_env()
            get_config_from_env()

        assert self._ignored(logs) == ["AGENT"]

    @pytest.mark.parametrize("source", ["environment", "dotenv"])
    def test_nested_variables_still_apply_next_to_an_ignored_one(
        self, monkeypatch: pytest.MonkeyPatch, tmp_path: Path, source: str
    ) -> None:
        if source == "environment":
            monkeypatch.setenv("AGENT", "claude-code")
            monkeypatch.setenv("AGENT__MISTRAL_CLIENT_TIMEOUT_MS", "5")
        else:
            (tmp_path / ".env.test").write_text("AGENT=claude-code\nAGENT__MISTRAL_CLIENT_TIMEOUT_MS=5\n")

        with capture_logs() as logs:
            config = get_config_from_env()

        assert config.worker.agent.mistral_client_timeout_ms == 5
        assert self._ignored(logs) == ["AGENT"]

    def test_json_value_still_configures(self, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.setenv("AGENT", '{"mistral_client_timeout_ms": 7}')

        assert get_config_from_env().worker.agent.mistral_client_timeout_ms == 7

    def test_malformed_json_object_still_fails(self, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.setenv("AGENT", '{"mistral_client_timeout_ms": 7')

        with pytest.raises(SettingsError, match="agent"):
            get_config_from_env()

    @pytest.mark.parametrize(
        ("variable", "error", "field"),
        [
            ("BLOB_STORAGE_CONFIGS", SettingsError, "blob_storage_configs"),
            ("BLOB_STORAGE_CONFIGS__traces", ValidationError, "blob_storage_configs"),
            ("TEMPORAL_PAYLOAD_ENCRYPTION", ValidationError, "temporal_payload_encryption"),
        ],
    )
    def test_non_json_value_for_other_fields_still_fails(
        self, monkeypatch: pytest.MonkeyPatch, variable: str, error: type[Exception], field: str
    ) -> None:
        monkeypatch.setenv(variable, "off")

        with pytest.raises(error, match=field):
            get_config_from_env()

    def test_bare_encryption_names_do_not_fill_the_nested_config(self, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.setenv("TEMPORAL_PAYLOAD_ENCRYPTION__MODE", "full")
        monkeypatch.setenv("MODE", "partial")
        monkeypatch.setenv("MAIN_KEY", "bare-main")
        monkeypatch.setenv("SECONDARY_KEY", "bare-secondary")

        encryption = get_config_from_env().worker.temporal_payload_encryption

        assert encryption is not None
        assert encryption.mode == "full"
        assert encryption.main_key is None
        assert encryption.secondary_key is None

    @pytest.mark.parametrize(
        ("nested", "bare", "read"),
        [
            (
                {"BLOB_STORAGE_CONFIGS__DOCS__STORAGE_PROVIDER": "s3"},
                {"BUCKET_NAME": "bare", "ENDPOINT_URL": "http://bare", "AWS_ACCESS_KEY_ID": "bare"},
                lambda worker: worker.blob_storage_configs["docs"].model_dump(exclude_defaults=True),
            ),
            (
                {"TEMPORAL_PAYLOAD_OFFLOADING__STORAGE_CONFIG__STORAGE_PROVIDER": "s3"},
                {"BUCKET_NAME": "bare", "MIN_SIZE_BYTES": "7"},
                lambda worker: worker.temporal_payload_offloading.model_dump(exclude_defaults=True),
            ),
            (
                {"TEMPORAL_PAYLOAD_COMPRESSION__MIN_SIZE_BYTES": "4096"},
                {"ALGORITHM_CONFIG": '{"algorithm": "zstd", "level": 9}'},
                lambda worker: worker.temporal_payload_compression.model_dump(exclude_defaults=True),
            ),
        ],
    )
    def test_bare_names_do_not_fill_other_payload_configs(
        self, monkeypatch: pytest.MonkeyPatch, nested: dict[str, str], bare: dict[str, str], read: Any
    ) -> None:
        for name, value in {**nested, **bare}.items():
            monkeypatch.setenv(name, value)

        with_bare = read(get_config_from_env().worker)
        for name in bare:
            monkeypatch.delenv(name)

        assert with_bare == read(get_config_from_env().worker)

    def test_nested_encryption_names_still_apply(self, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.setenv("TEMPORAL_PAYLOAD_ENCRYPTION__MODE", "partial")
        monkeypatch.setenv("TEMPORAL_PAYLOAD_ENCRYPTION__MAIN_KEY", "nested-main")
        monkeypatch.setenv("TEMPORAL_PAYLOAD_ENCRYPTION__SECONDARY_KEY", "nested-secondary")

        encryption = get_config_from_env().worker.temporal_payload_encryption

        assert encryption is not None
        assert encryption.main_key is not None and encryption.main_key.get_secret_value() == "nested-main"
        assert encryption.secondary_key is not None
        assert encryption.secondary_key.get_secret_value() == "nested-secondary"

    def test_mistyped_nested_encryption_name_still_fails(self, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.setenv("TEMPORAL_PAYLOAD_ENCRYPTION__MODE", "full")
        monkeypatch.setenv("TEMPORAL_PAYLOAD_ENCRYPTION__MAIN_KYE", "nested-main")

        with pytest.raises(ValidationError, match="main_kye"):
            get_config_from_env()
