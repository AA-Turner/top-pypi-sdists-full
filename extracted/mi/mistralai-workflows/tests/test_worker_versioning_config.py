from pathlib import Path

import pytest

from mistralai.workflows import WorkerConfig, WorkerVersioningConfig, WorkflowsConfig
from mistralai.workflows.core.config.config import resolve_worker_config


@pytest.fixture(autouse=True)
def isolate_environment(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    monkeypatch.chdir(tmp_path)
    for var in (
        "WORKER_AUTO_REGISTER_AS_CURRENT",
        "AUTO_REGISTER_AS_CURRENT",
        "DEPLOYMENT_NAME",
        "BUILD_ID",
        "TEMPORAL_DEPLOYMENT_NAME",
        "TEMPORAL_WORKER_BUILD_ID",
    ):
        monkeypatch.delenv(var, raising=False)


class TestWorkerVersioningConfigModes:
    def test_controller_mode_config(self, monkeypatch: pytest.MonkeyPatch) -> None:
        """Controller-provided variables should enable versioning and disable auto-registration."""
        monkeypatch.setenv(
            "TEMPORAL_DEPLOYMENT_NAME", "workflow-workers/shared-worker-workflows-workers-payment-processor"
        )
        monkeypatch.setenv("TEMPORAL_WORKER_BUILD_ID", "build-1234")

        cfg = WorkerVersioningConfig()
        assert cfg.enabled is True
        # deployment_name comes from TEMPORAL_DEPLOYMENT_NAME, not DEPLOYMENT_NAME
        assert cfg.deployment_name == "workflow-workers/shared-worker-workflows-workers-payment-processor"
        assert cfg.build_id == "build-1234"
        assert cfg.auto_register_as_current is False

    def test_controller_mode_ignores_deployment_name_env(self, monkeypatch: pytest.MonkeyPatch) -> None:
        """Controller mode uses TEMPORAL_DEPLOYMENT_NAME regardless of DEPLOYMENT_NAME."""
        monkeypatch.setenv("DEPLOYMENT_NAME", "shared-payment-processor")
        monkeypatch.setenv(
            "TEMPORAL_DEPLOYMENT_NAME", "workflow-workers/shared-worker-workflows-workers-payment-processor"
        )
        monkeypatch.setenv("TEMPORAL_WORKER_BUILD_ID", "build-1234")

        cfg = WorkerVersioningConfig()
        assert cfg.deployment_name == "workflow-workers/shared-worker-workflows-workers-payment-processor"

    @pytest.mark.parametrize("source", ["environment", "code"])
    def test_controller_mode_overrides_explicit_auto_register(
        self, monkeypatch: pytest.MonkeyPatch, source: str
    ) -> None:
        """Controller mode forces auto_register=False even when explicitly set to True."""
        monkeypatch.setenv(
            "TEMPORAL_DEPLOYMENT_NAME", "workflow-workers/shared-worker-workflows-workers-payment-processor"
        )
        monkeypatch.setenv("TEMPORAL_WORKER_BUILD_ID", "build-1234")
        if source == "environment":
            monkeypatch.setenv("WORKER_AUTO_REGISTER_AS_CURRENT", "true")
            cfg = WorkerVersioningConfig()
        else:
            cfg = WorkerVersioningConfig(auto_register_as_current=True)

        assert cfg.enabled is True
        assert cfg.auto_register_as_current is False

    def test_manual_mode_defaults(self, monkeypatch: pytest.MonkeyPatch) -> None:
        """Manual mode should infer deployment name and enable auto-registration."""
        monkeypatch.setenv("DEPLOYMENT_NAME", "manual-worker")
        monkeypatch.setenv("BUILD_ID", "v9.9.9")

        cfg = WorkerVersioningConfig()
        assert cfg.enabled is True
        assert cfg.deployment_name == "manual-worker"
        assert cfg.build_id == "v9.9.9"
        assert cfg.auto_register_as_current is True

    def test_manual_mode_disable_auto_register(self, monkeypatch: pytest.MonkeyPatch) -> None:
        """Manual mode with auto-register flag set to false should keep versioning enabled."""
        monkeypatch.setenv("WORKER_AUTO_REGISTER_AS_CURRENT", "false")
        monkeypatch.setenv("DEPLOYMENT_NAME", "manual-worker")
        monkeypatch.setenv("BUILD_ID", "v9.9.9")

        cfg = WorkerVersioningConfig()
        assert cfg.enabled is True
        assert cfg.auto_register_as_current is False
        assert cfg.deployment_name == "manual-worker"
        assert cfg.build_id == "v9.9.9"


class TestWorkerVersioningConfigPrecedence:
    @pytest.mark.parametrize("source", ["environment", "dotenv"])
    @pytest.mark.parametrize("keyword", ["auto_register_as_current", "WORKER_AUTO_REGISTER_AS_CURRENT"])
    @pytest.mark.parametrize(("explicit", "inherited"), [(False, "true"), (True, "false")])
    def test_explicit_value_beats_inherited_value(
        self,
        monkeypatch: pytest.MonkeyPatch,
        tmp_path: Path,
        source: str,
        keyword: str,
        explicit: bool,
        inherited: str,
    ) -> None:
        env_file = tmp_path / ".env"
        if source == "environment":
            monkeypatch.setenv("WORKER_AUTO_REGISTER_AS_CURRENT", inherited)
        else:
            env_file.write_text(f"WORKER_AUTO_REGISTER_AS_CURRENT={inherited}\n")

        cfg = WorkerVersioningConfig(
            _env_file=env_file, deployment_name="manual-worker", BUILD_ID="v2", **{keyword: explicit}
        )

        assert cfg.enabled is True
        assert cfg.auto_register_as_current is explicit

    def test_field_name_is_not_an_environment_variable(self, monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
        monkeypatch.setenv("AUTO_REGISTER_AS_CURRENT", "false")
        (tmp_path / ".env").write_text("auto_register_as_current=false\n")

        cfg = WorkerVersioningConfig(_env_file=tmp_path / ".env", deployment_name="manual-worker", BUILD_ID="v2")

        assert cfg.auto_register_as_current is True

    @pytest.mark.parametrize("use_model", [False, True])
    def test_worker_resolution_preserves_explicit_value(self, monkeypatch: pytest.MonkeyPatch, use_model: bool) -> None:
        monkeypatch.setenv("WORKER_AUTO_REGISTER_AS_CURRENT", "true")
        versioning = {"deployment_name": "manual-worker", "BUILD_ID": "v2", "auto_register_as_current": False}
        worker = (
            WorkerConfig(versioning=WorkerVersioningConfig(**versioning)) if use_model else {"versioning": versioning}
        )
        config = WorkflowsConfig(worker=worker)

        resolved = resolve_worker_config(config)

        assert config.worker.versioning.auto_register_as_current is False
        assert resolved.worker.versioning.enabled is True
        assert resolved.worker.versioning.auto_register_as_current is False
