from unittest.mock import patch

import pytest

from mistralai.workflows.core.config.config import AppConfig, config
from mistralai.workflows.core.worker import _run_worker


class TestDeploymentRouting:
    @pytest.mark.parametrize("deployment_name", ["invoice-parser", "default"])
    @pytest.mark.parametrize("legacy_queue", ["default", "another-deployment"])
    def test_legacy_queue_environment_does_not_override_deployment(
        self, monkeypatch: pytest.MonkeyPatch, deployment_name: str, legacy_queue: str
    ) -> None:
        monkeypatch.setenv("DEPLOYMENT_NAME", deployment_name)
        monkeypatch.setenv("TEMPORAL_TASK_QUEUE", legacy_queue)
        cfg = AppConfig()

        cfg.validate_for_worker_startup()

        assert cfg.get_effective_task_queue() == deployment_name
        assert "task_queue" not in cfg.temporal.model_dump()
        assert "task_queue" not in type(cfg.temporal).model_fields

    def test_queue_is_not_a_configurable_field(self) -> None:
        cfg = config.model_copy(deep=True)

        with pytest.raises(ValueError, match='has no field "task_queue"'):
            setattr(cfg.temporal, "task_queue", "another-deployment")


class TestWorkerStartupRequiresDeploymentName:
    @pytest.mark.parametrize("legacy_queue", [None, "default", "invoice-parser"])
    def test_legacy_queue_does_not_supply_a_deployment(
        self, monkeypatch: pytest.MonkeyPatch, legacy_queue: str | None
    ) -> None:
        monkeypatch.delenv("DEPLOYMENT_NAME", raising=False)
        if legacy_queue is None:
            monkeypatch.delenv("TEMPORAL_TASK_QUEUE", raising=False)
        else:
            monkeypatch.setenv("TEMPORAL_TASK_QUEUE", legacy_queue)
        cfg = AppConfig()
        cfg.worker.deployment_name = None

        with pytest.raises(ValueError, match="DEPLOYMENT_NAME is required"):
            cfg.validate_for_worker_startup()

    def test_default_deployment_name_warns(self) -> None:
        cfg = config.model_copy(deep=True)
        cfg.worker.deployment_name = "default"
        with patch("mistralai.workflows.core.config.config.logger") as mock_logger:
            cfg.validate_for_worker_startup()
        mock_logger.warning.assert_called_once()
        assert "default" in mock_logger.warning.call_args[0][0]

    def test_non_default_deployment_name_does_not_warn(self) -> None:
        cfg = config.model_copy(deep=True)
        cfg.worker.deployment_name = "invoice-parser"
        with patch("mistralai.workflows.core.config.config.logger") as mock_logger:
            cfg.validate_for_worker_startup()
        mock_logger.warning.assert_not_called()

    @pytest.mark.asyncio
    async def test_run_worker_fails_before_connecting_without_deployment(self, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.setattr(config.worker, "deployment_name", None)
        with pytest.raises(ValueError, match="DEPLOYMENT_NAME is required"):
            await _run_worker([])
