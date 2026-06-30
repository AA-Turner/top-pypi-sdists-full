import pytest

from mistralai.workflows.core.config.config import WorkerVersioningConfig


class TestWorkerVersioningConfigModes:
    def test_controller_mode_config(self, monkeypatch: pytest.MonkeyPatch) -> None:
        """Controller-provided variables should enable versioning and disable auto-registration."""
        for var in (
            "WORKER_AUTO_REGISTER_AS_CURRENT",
            "DEPLOYMENT_NAME",
            "BUILD_ID",
        ):
            monkeypatch.delenv(var, raising=False)

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

        monkeypatch.delenv("TEMPORAL_DEPLOYMENT_NAME", raising=False)
        monkeypatch.delenv("TEMPORAL_WORKER_BUILD_ID", raising=False)

    def test_controller_mode_ignores_deployment_name_env(self, monkeypatch: pytest.MonkeyPatch) -> None:
        """Controller mode uses TEMPORAL_DEPLOYMENT_NAME regardless of DEPLOYMENT_NAME."""
        for var in (
            "WORKER_AUTO_REGISTER_AS_CURRENT",
            "BUILD_ID",
        ):
            monkeypatch.delenv(var, raising=False)

        monkeypatch.setenv("DEPLOYMENT_NAME", "shared-payment-processor")
        monkeypatch.setenv(
            "TEMPORAL_DEPLOYMENT_NAME", "workflow-workers/shared-worker-workflows-workers-payment-processor"
        )
        monkeypatch.setenv("TEMPORAL_WORKER_BUILD_ID", "build-1234")

        cfg = WorkerVersioningConfig()
        assert cfg.deployment_name == "workflow-workers/shared-worker-workflows-workers-payment-processor"

        monkeypatch.delenv("DEPLOYMENT_NAME", raising=False)
        monkeypatch.delenv("TEMPORAL_DEPLOYMENT_NAME", raising=False)
        monkeypatch.delenv("TEMPORAL_WORKER_BUILD_ID", raising=False)

    def test_controller_mode_overrides_explicit_auto_register(self, monkeypatch: pytest.MonkeyPatch) -> None:
        """Controller mode forces auto_register=False even when explicitly set to True."""
        for var in (
            "WORKER_AUTO_REGISTER_AS_CURRENT",
            "DEPLOYMENT_NAME",
            "BUILD_ID",
        ):
            monkeypatch.delenv(var, raising=False)

        monkeypatch.setenv("WORKER_AUTO_REGISTER_AS_CURRENT", "true")
        monkeypatch.setenv(
            "TEMPORAL_DEPLOYMENT_NAME", "workflow-workers/shared-worker-workflows-workers-payment-processor"
        )
        monkeypatch.setenv("TEMPORAL_WORKER_BUILD_ID", "build-1234")

        cfg = WorkerVersioningConfig()
        assert cfg.enabled is True
        assert cfg.auto_register_as_current is False

        monkeypatch.delenv("WORKER_AUTO_REGISTER_AS_CURRENT", raising=False)
        monkeypatch.delenv("TEMPORAL_DEPLOYMENT_NAME", raising=False)
        monkeypatch.delenv("TEMPORAL_WORKER_BUILD_ID", raising=False)

    def test_manual_mode_defaults(self, monkeypatch: pytest.MonkeyPatch) -> None:
        """Manual mode should infer deployment name and enable auto-registration."""
        for var in (
            "WORKER_AUTO_REGISTER_AS_CURRENT",
            "DEPLOYMENT_NAME",
            "BUILD_ID",
            "TEMPORAL_DEPLOYMENT_NAME",
            "TEMPORAL_WORKER_BUILD_ID",
        ):
            monkeypatch.delenv(var, raising=False)

        monkeypatch.setenv("DEPLOYMENT_NAME", "manual-worker")
        monkeypatch.setenv("BUILD_ID", "v9.9.9")

        cfg = WorkerVersioningConfig()
        assert cfg.enabled is True
        assert cfg.deployment_name == "manual-worker"
        assert cfg.build_id == "v9.9.9"
        assert cfg.auto_register_as_current is True
        monkeypatch.delenv("DEPLOYMENT_NAME", raising=False)
        monkeypatch.delenv("BUILD_ID", raising=False)

    def test_manual_mode_disable_auto_register(self, monkeypatch: pytest.MonkeyPatch) -> None:
        """Manual mode with auto-register flag set to false should keep versioning enabled."""
        for var in (
            "WORKER_AUTO_REGISTER_AS_CURRENT",
            "DEPLOYMENT_NAME",
            "BUILD_ID",
            "TEMPORAL_DEPLOYMENT_NAME",
            "TEMPORAL_WORKER_BUILD_ID",
        ):
            monkeypatch.delenv(var, raising=False)

        monkeypatch.setenv("WORKER_AUTO_REGISTER_AS_CURRENT", "false")
        monkeypatch.setenv("DEPLOYMENT_NAME", "manual-worker")
        monkeypatch.setenv("BUILD_ID", "v9.9.9")

        cfg = WorkerVersioningConfig()
        assert cfg.enabled is True
        assert cfg.auto_register_as_current is False
        assert cfg.deployment_name == "manual-worker"
        assert cfg.build_id == "v9.9.9"

        for var in ("WORKER_AUTO_REGISTER_AS_CURRENT", "DEPLOYMENT_NAME", "BUILD_ID"):
            monkeypatch.delenv(var, raising=False)
