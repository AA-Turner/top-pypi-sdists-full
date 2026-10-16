from http import HTTPStatus
from unittest.mock import AsyncMock, patch

import pytest
from pydantic import SecretStr

from mistralai.workflows.core.config.config import config
from mistralai.workflows.core.worker import _run_worker, run_worker
from mistralai.workflows.exceptions import _TERMINAL_CODES, ErrorCode, WorkflowsException


@pytest.fixture(autouse=True)
def valid_config(restore_config_sections):
    worker = config.worker
    original = worker.deployment_name
    worker.deployment_name = "test-deployment"
    yield
    worker.deployment_name = original


def _raise_in_worker(exc: Exception):
    """Patch create_temporal_client to raise exc inside _run_worker's error reporting."""
    return patch(
        "mistralai.workflows.core.worker.create_temporal_client",
        new=AsyncMock(side_effect=exc),
    )


class TestNonRecoverableErrors:
    @pytest.mark.asyncio
    async def test_unauthorized_exits_with_code_1(self):
        exc = WorkflowsException(message="Invalid API key", status=HTTPStatus.UNAUTHORIZED, code="unauthorized")
        with _raise_in_worker(exc):
            with pytest.raises(SystemExit) as exc_info:
                await _run_worker([])
        assert exc_info.value.code == 1

    @pytest.mark.asyncio
    async def test_unauthorized_suppresses_chained_cause(self):
        exc = WorkflowsException(message="Invalid API key", status=HTTPStatus.UNAUTHORIZED, code="unauthorized")
        with _raise_in_worker(exc):
            with pytest.raises(SystemExit) as exc_info:
                await _run_worker([])
        assert exc_info.value.__cause__ is None

    @pytest.mark.asyncio
    async def test_unauthorized_logs_structured_error(self):
        exc = WorkflowsException(
            message="Invalid API key",
            status=HTTPStatus.UNAUTHORIZED,
            code="unauthorized",
            logging_properties={"temporal_connection_error": "upstream rejected credentials"},
        )
        with _raise_in_worker(exc):
            with patch("mistralai.workflows.core.worker.logger") as mock_logger:
                with pytest.raises(SystemExit):
                    await _run_worker([])
        mock_logger.error.assert_called_once()
        call_kwargs = mock_logger.error.call_args
        assert "Authentication failed" in call_kwargs[0][0]
        assert call_kwargs[1]["http_status"] == 401
        assert call_kwargs[1]["temporal_connection_error"] == "upstream rejected credentials"

    @pytest.mark.asyncio
    async def test_temporal_unauthorized_names_explicit_temporal_api_key(self):
        exc = WorkflowsException(
            message="Invalid API key",
            status=HTTPStatus.UNAUTHORIZED,
            code=ErrorCode.TEMPORAL_CONNECTION_ERROR,
        )
        with (
            patch.object(config.temporal, "api_key", SecretStr("temporal-key")),
            patch.object(config.common, "mistral_sa_token_path", None),
            patch("mistralai.workflows.core.worker.logger") as mock_logger,
            _raise_in_worker(exc),
            pytest.raises(SystemExit),
        ):
            await _run_worker([])

        assert "TEMPORAL_API_KEY" in mock_logger.error.call_args.args[0]

    @pytest.mark.asyncio
    async def test_temporal_unauthorized_names_mistral_api_key_when_used_as_fallback(self):
        exc = WorkflowsException(
            message="Invalid API key",
            status=HTTPStatus.UNAUTHORIZED,
            code=ErrorCode.TEMPORAL_CONNECTION_ERROR,
        )
        with (
            patch.object(config.temporal, "api_key", None),
            patch.object(config.common, "mistral_sa_token_path", None),
            patch.object(config.common, "mistral_api_key", SecretStr("mistral-key")),
            patch("mistralai.workflows.core.worker.logger") as mock_logger,
            _raise_in_worker(exc),
            pytest.raises(SystemExit),
        ):
            await _run_worker([])

        assert "MISTRAL_API_KEY" in mock_logger.error.call_args.args[0]

    @pytest.mark.asyncio
    async def test_config_discovery_unauthorized_names_mistral_api_key(self):
        exc = WorkflowsException(
            message="Invalid API key",
            status=HTTPStatus.UNAUTHORIZED,
            code=ErrorCode.WORKER_RUNTIME_CONFIG_ERROR,
        )
        with (
            patch.object(config.temporal, "api_key", SecretStr("temporal-key")),
            patch.object(config.common, "mistral_sa_token_path", None),
            patch.object(config.common, "mistral_api_key", SecretStr("mistral-key")),
            patch(
                "mistralai.workflows.core.worker.config_discovery.apply_worker_runtime_config",
                new=AsyncMock(side_effect=exc),
            ),
            patch("mistralai.workflows.core.worker.logger") as mock_logger,
            pytest.raises(SystemExit) as exc_info,
        ):
            await run_worker([], enable_config_discovery=True)

        assert exc_info.value.code == 1
        assert "MISTRAL_API_KEY" in mock_logger.error.call_args.args[0]

    @pytest.mark.asyncio
    async def test_detached_config_discovery_unauthorized_reaches_the_caller(self):
        exc = WorkflowsException(
            message="Invalid API key",
            status=HTTPStatus.UNAUTHORIZED,
            code=ErrorCode.WORKER_RUNTIME_CONFIG_ERROR,
        )
        with (
            patch.object(config.temporal, "api_key", SecretStr("temporal-key")),
            patch.object(config.common, "mistral_sa_token_path", None),
            patch.object(config.common, "mistral_api_key", SecretStr("mistral-key")),
            patch(
                "mistralai.workflows.core.worker.config_discovery.apply_worker_runtime_config",
                new=AsyncMock(side_effect=exc),
            ),
            patch("mistralai.workflows.core.worker.logger") as mock_logger,
            pytest.raises(WorkflowsException) as exc_info,
        ):
            await run_worker([], detach=True, enable_config_discovery=True)

        assert exc_info.value is exc
        mock_logger.error.assert_called_once()
        assert "MISTRAL_API_KEY" in mock_logger.error.call_args.args[0]

    @pytest.mark.asyncio
    async def test_unexpected_config_discovery_error_is_not_reported_as_a_stopped_worker(self):
        with (
            patch(
                "mistralai.workflows.core.worker.config_discovery.apply_worker_runtime_config",
                new=AsyncMock(side_effect=ValueError("Unable to determine port from URL: temporal.example.com")),
            ),
            patch("mistralai.workflows.core.worker.logger") as mock_logger,
            pytest.raises(ValueError),
        ):
            await run_worker([], detach=True, enable_config_discovery=True)

        mock_logger.error.assert_called_once()
        assert mock_logger.error.call_args.args[0] == "Worker config discovery failed"

    @pytest.mark.asyncio
    async def test_detached_worker_preserves_workflows_exception(self):
        exc = WorkflowsException(message="Invalid API key", status=HTTPStatus.UNAUTHORIZED, code="unauthorized")
        with _raise_in_worker(exc):
            with pytest.raises(WorkflowsException) as exc_info:
                await _run_worker([], exit_on_terminal_error=False)

        assert exc_info.value is exc

    @pytest.mark.asyncio
    async def test_wf_1104_exits_with_code_1(self):
        exc = WorkflowsException(
            message="Failed to register workflow specs",
            status=HTTPStatus.FORBIDDEN,
            code="WF_1104",
        )
        with _raise_in_worker(exc):
            with pytest.raises(SystemExit) as exc_info:
                await _run_worker([])
        assert exc_info.value.code == 1

    @pytest.mark.asyncio
    async def test_wf_1104_suppresses_chained_cause(self):
        exc = WorkflowsException(
            message="Failed to register workflow specs",
            status=HTTPStatus.FORBIDDEN,
            code="WF_1104",
        )
        with _raise_in_worker(exc):
            with pytest.raises(SystemExit) as exc_info:
                await _run_worker([])
        assert exc_info.value.__cause__ is None

    @pytest.mark.asyncio
    async def test_wf_1104_logs_human_readable_label(self):
        exc = WorkflowsException(
            message="Failed to register workflow specs",
            status=HTTPStatus.FORBIDDEN,
            code="WF_1104",
        )
        with _raise_in_worker(exc):
            with patch("mistralai.workflows.core.worker.logger") as mock_logger:
                with pytest.raises(SystemExit):
                    await _run_worker([])
        mock_logger.error.assert_called_once()
        call_kwargs = mock_logger.error.call_args
        assert call_kwargs[0][0] == _TERMINAL_CODES["WF_1104"]

    @pytest.mark.asyncio
    async def test_unknown_workflows_exception_reraises(self):
        exc = WorkflowsException(
            message="Something unexpected",
            status=HTTPStatus.TOO_MANY_REQUESTS,
            code="WF_9999",
        )
        with _raise_in_worker(exc):
            with pytest.raises(WorkflowsException):
                await _run_worker([])

    @pytest.mark.asyncio
    async def test_401_takes_priority_over_dict_lookup(self):
        # An exception with 401 status must not fall through to dict lookup.
        exc = WorkflowsException(
            message="Unauthorized",
            status=HTTPStatus.UNAUTHORIZED,
            code="WF_1104",  # even if code happens to be in the dict
        )
        with _raise_in_worker(exc):
            with patch("mistralai.workflows.core.worker.logger") as mock_logger:
                with pytest.raises(SystemExit):
                    await _run_worker([])
        # Must log the auth message, not the WF_1104 label
        call_kwargs = mock_logger.error.call_args
        assert "Authentication failed" in call_kwargs[0][0]
        assert _TERMINAL_CODES["WF_1104"] not in call_kwargs[0][0]
