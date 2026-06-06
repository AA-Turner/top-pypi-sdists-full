import asyncio
from unittest.mock import AsyncMock, MagicMock, patch
from uuid import uuid4

import httpx
import pytest

from mistralai.workflows.core.worker import _worker_heartbeat
from mistralai.workflows.exceptions import WorkflowsException
from mistralai.workflows.protocol.v1.workflow import (
    WorkflowRegistrationRef,
    WorkflowSpecsRegisterResponse,
)
from mistralai.workflows.worker_client.errors.sdkerror import SDKError

WF_ID = uuid4()
REG_ID = uuid4()

HEARTBEAT_NOT_AVAILABLE_MSG = "Heartbeat endpoint not available"
HEARTBEAT_FAILED_MSG = "Heartbeat failed"


def _make_ref() -> WorkflowRegistrationRef:
    return WorkflowRegistrationRef(workflow_id=WF_ID, workflow_registration_id=REG_ID)


def _make_sdk_error(status_code: int) -> SDKError:
    response = httpx.Response(status_code=status_code, request=httpx.Request("POST", "http://test"))
    return SDKError("API error", response)


def _make_worker_client(heartbeat_side_effect: list) -> AsyncMock:
    client = AsyncMock()
    client.heartbeat_async = AsyncMock(side_effect=heartbeat_side_effect)
    return client


def _make_register_response() -> WorkflowSpecsRegisterResponse:
    return WorkflowSpecsRegisterResponse(
        workflow_registration_ids=[WF_ID],
        workflow_registration_refs=[_make_ref()],
        has_conflicts=False,
    )


async def _run_heartbeat(
    worker_client: AsyncMock,
    iterations: int,
    register_mock: AsyncMock | None = None,
    logger_mock: MagicMock | None = None,
) -> AsyncMock:
    call_count = 0

    async def _counting_sleep(delay: float) -> None:
        nonlocal call_count
        call_count += 1
        if call_count > iterations:
            raise asyncio.CancelledError

    register = register_mock or AsyncMock(return_value=_make_register_response())
    logger_patch = (
        patch("mistralai.workflows.core.worker.logger", new=logger_mock)
        if logger_mock
        else patch.object(_worker_heartbeat, "__module__", _worker_heartbeat.__module__)
    )

    with (
        pytest.raises(asyncio.CancelledError),
        patch("asyncio.sleep", new=_counting_sleep),
        patch("mistralai.workflows.core.worker._register_workflow_specs", new=register),
        logger_patch,
    ):
        await _worker_heartbeat(
            worker_client=worker_client,
            workflow_definitions=[],
            workflow_registration_refs=[_make_ref()],
            interval=10,
        )

    return register


def _count_warnings(mock_logger: MagicMock, substring: str) -> int:
    return sum(1 for c in mock_logger.warning.call_args_list if substring in c.args[0])


class TestWorkerHeartbeat:
    @pytest.mark.parametrize(
        ("error", "expected_not_available", "expected_failed"),
        [
            pytest.param(_make_sdk_error(404), 1, 0, id="sdk-404"),
            pytest.param(_make_sdk_error(405), 1, 0, id="sdk-405"),
            pytest.param(_make_sdk_error(500), 0, 3, id="sdk-500"),
            pytest.param(ConnectionError("refused"), 0, 3, id="connection-error"),
        ],
    )
    async def test_warning_behavior(self, error: Exception, expected_not_available: int, expected_failed: int) -> None:
        iterations = 3
        client = _make_worker_client([error] * iterations)
        mock_logger = MagicMock()

        register = await _run_heartbeat(client, iterations=iterations, logger_mock=mock_logger)

        assert _count_warnings(mock_logger, HEARTBEAT_NOT_AVAILABLE_MSG) == expected_not_available
        assert _count_warnings(mock_logger, HEARTBEAT_FAILED_MSG) == expected_failed
        assert register.call_count == iterations

    async def test_reregistration_failure_logs_error(self) -> None:
        client = _make_worker_client([_make_sdk_error(500)])
        register_mock = AsyncMock(side_effect=RuntimeError("register failed"))
        mock_logger = MagicMock()

        await _run_heartbeat(client, iterations=1, register_mock=register_mock, logger_mock=mock_logger)

        assert mock_logger.warning.call_count == 1
        assert HEARTBEAT_FAILED_MSG in mock_logger.warning.call_args.args[0]
        assert mock_logger.error.call_count == 1
        assert "re-registration also failed" in mock_logger.error.call_args.args[0]

    async def test_heartbeat_suppresses_instrumentation(self) -> None:
        client = _make_worker_client([None])

        with patch("mistralai.workflows.core.worker.suppress_instrumentation") as suppress:
            register = await _run_heartbeat(client, iterations=1)

        suppress.assert_called_once_with()
        client.heartbeat_async.assert_awaited_once()
        register.assert_not_awaited()

    async def test_unexpected_error_raises_workflows_exception(self) -> None:
        client = AsyncMock()
        client.heartbeat_async = AsyncMock(side_effect=RuntimeError("unexpected"))
        mock_logger = MagicMock()

        async def _sleep_then_fail(delay: float) -> None:
            raise RuntimeError("event loop crash")

        with (
            pytest.raises(WorkflowsException, match="Fail to heartbeat worker"),
            patch("asyncio.sleep", new=_sleep_then_fail),
            patch("mistralai.workflows.core.worker._register_workflow_specs", new=AsyncMock()),
            patch("mistralai.workflows.core.worker.logger", new=mock_logger),
        ):
            await _worker_heartbeat(
                worker_client=client,
                workflow_definitions=[],
                workflow_registration_refs=[_make_ref()],
                interval=10,
            )

        assert mock_logger.error.call_count == 1
        assert "Error in heartbeat task" in mock_logger.error.call_args.args[0]
