from unittest.mock import patch

import pytest

from mistralai.workflows.core.config.config import AppConfig, config
from mistralai.workflows.core.worker import _run_worker
from mistralai.workflows.exceptions import WorkflowsException


@pytest.fixture(autouse=True)
def restore_config():
    original_task_queue = config.temporal.task_queue
    original_deployment_name = config.worker.deployment_name
    yield
    config.temporal.task_queue = original_task_queue
    config.worker.deployment_name = original_deployment_name


class TestGetEffectiveTaskQueue:
    def _cfg(self, deployment_name: str | None, task_queue: str) -> AppConfig:
        cfg = config.model_copy(deep=True)
        cfg.worker.deployment_name = deployment_name
        cfg.temporal.task_queue = task_queue
        return cfg

    def test_no_deployment_name_returns_task_queue(self) -> None:
        assert self._cfg(None, "my-queue").get_effective_task_queue() == "my-queue"

    def test_no_deployment_name_default_queue_returns_default(self) -> None:
        assert self._cfg(None, "default").get_effective_task_queue() == "default"

    def test_deployment_name_with_default_task_queue_returns_deployment_name(self) -> None:
        assert self._cfg("alice", "default").get_effective_task_queue() == "alice"

    def test_deployment_name_matching_task_queue_returns_deployment_name(self) -> None:
        assert self._cfg("alice", "alice").get_effective_task_queue() == "alice"

    def test_conflict_without_raise_flag_returns_deployment_name(self) -> None:
        assert self._cfg("alice", "bob").get_effective_task_queue(raise_on_conflict=False) == "alice"

    def test_adding_conflicting_deployment_name_to_existing_task_queue_raises(self) -> None:
        with pytest.raises(WorkflowsException, match="TEMPORAL_TASK_QUEUE.*conflicts.*DEPLOYMENT_NAME"):
            self._cfg(deployment_name="bob", task_queue="alice").get_effective_task_queue(raise_on_conflict=True)

    def test_adding_conflicting_task_queue_to_existing_deployment_name_raises(self) -> None:
        with pytest.raises(WorkflowsException, match="TEMPORAL_TASK_QUEUE.*conflicts.*DEPLOYMENT_NAME"):
            self._cfg(deployment_name="alice", task_queue="bob").get_effective_task_queue(raise_on_conflict=True)

    def test_adding_matching_deployment_name_to_existing_task_queue_is_not_a_conflict(self) -> None:
        result = self._cfg(deployment_name="alice", task_queue="alice").get_effective_task_queue(raise_on_conflict=True)
        assert result == "alice"

    def test_adding_task_queue_default_with_deployment_name_is_not_a_conflict(self) -> None:
        result = self._cfg(deployment_name="alice", task_queue="default").get_effective_task_queue(
            raise_on_conflict=True
        )
        assert result == "alice"


class TestWorkerStartupRequiresDeploymentName:
    def _cfg(self, deployment_name: str | None, task_queue: str = "default") -> AppConfig:
        cfg = config.model_copy(deep=True)
        cfg.worker.deployment_name = deployment_name
        cfg.temporal.task_queue = task_queue
        return cfg

    def test_deployment_name_none_with_default_queue_raises(self) -> None:
        with pytest.raises(ValueError, match="DEPLOYMENT_NAME is required"):
            self._cfg(None, "default").validate_for_worker_startup()

    def test_deployment_name_explicitly_set_to_default_string_warns(self) -> None:
        with patch("mistralai.workflows.core.config.config.logger") as mock_logger:
            self._cfg("default").validate_for_worker_startup()
        mock_logger.warning.assert_called_once()
        assert "default" in mock_logger.warning.call_args[0][0]

    def test_deployment_name_set_to_non_default_does_not_warn(self) -> None:
        with patch("mistralai.workflows.core.config.config.logger") as mock_logger:
            self._cfg("invoice-parser").validate_for_worker_startup()
        mock_logger.warning.assert_not_called()

    @pytest.mark.asyncio
    async def test_run_worker_fails_fast_when_neither_set(self) -> None:
        cfg = self._cfg(None)
        config.worker.deployment_name = cfg.worker.deployment_name
        config.temporal.task_queue = cfg.temporal.task_queue
        with pytest.raises(ValueError, match="DEPLOYMENT_NAME is required"):
            await _run_worker([])
