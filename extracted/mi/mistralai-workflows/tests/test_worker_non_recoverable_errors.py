from http import HTTPStatus
from unittest.mock import AsyncMock, patch

import pytest

from mistralai.workflows.core.config.config import config
from mistralai.workflows.core.worker import _run_worker
from mistralai.workflows.exceptions import _TERMINAL_CODES, WorkflowsException


@pytest.fixture(autouse=True)
def valid_config():
    original = config.worker.deployment_name
    config.worker.deployment_name = "test-deployment"
    yield
    config.worker.deployment_name = original


def _raise_in_worker(exc: Exception):
    """Patch create_temporal_client to raise exc inside _run_worker's try block."""
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
        exc = WorkflowsException(message="Invalid API key", status=HTTPStatus.UNAUTHORIZED, code="unauthorized")
        with _raise_in_worker(exc):
            with patch("mistralai.workflows.core.worker.logger") as mock_logger:
                with pytest.raises(SystemExit):
                    await _run_worker([])
        mock_logger.error.assert_called_once()
        call_kwargs = mock_logger.error.call_args
        assert "Authentication failed" in call_kwargs[0][0]
        assert call_kwargs[1]["http_status"] == 401

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
