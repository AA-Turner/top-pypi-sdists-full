from unittest.mock import AsyncMock, MagicMock, patch

from temporalio.service import RPCError, RPCStatusCode

from mistralai.workflows.core.worker import (
    _auto_register_as_current_version,
    _is_deployment_controller_managed_error,
)

# The exact rejection the server returns when the Temporal Worker Controller already
# owns the deployment (see Sentry VIBE-AGENTS-43).
_MANAGER_IDENTITY_MESSAGE = (
    "ManagerIdentity 'shared-worker/workflow-workers' is set and does not match user identity ''; "
    "to proceed, set your own identity as the ManagerIdentity, remove the ManagerIdentity, "
    "or wait for the other client to do so"
)


def _rpc_error(message: str, status: RPCStatusCode) -> RPCError:
    return RPCError(message, status, b"")


def _client_raising(side_effect: object) -> AsyncMock:
    client = AsyncMock()
    client.workflow_service.set_worker_deployment_current_version = AsyncMock(side_effect=side_effect)
    return client


class TestIsDeploymentControllerManagedError:
    def test_true_for_manager_identity_failed_precondition(self) -> None:
        exc = _rpc_error(_MANAGER_IDENTITY_MESSAGE, RPCStatusCode.FAILED_PRECONDITION)
        assert _is_deployment_controller_managed_error(exc) is True

    def test_false_for_failed_precondition_without_manager_identity(self) -> None:
        exc = _rpc_error("worker deployment not ready", RPCStatusCode.FAILED_PRECONDITION)
        assert _is_deployment_controller_managed_error(exc) is False

    def test_false_for_manager_identity_with_other_status(self) -> None:
        exc = _rpc_error(_MANAGER_IDENTITY_MESSAGE, RPCStatusCode.NOT_FOUND)
        assert _is_deployment_controller_managed_error(exc) is False

    def test_false_for_non_rpc_error(self) -> None:
        assert _is_deployment_controller_managed_error(RuntimeError("boom")) is False


class TestAutoRegisterAsCurrentVersion:
    async def test_controller_managed_bails_without_retry_or_error(self) -> None:
        """A controller-owned deployment must stop after the first rejection, not retry 48 times."""
        exc = _rpc_error(_MANAGER_IDENTITY_MESSAGE, RPCStatusCode.FAILED_PRECONDITION)
        client = _client_raising(exc)
        mock_logger = MagicMock()

        with (
            patch("asyncio.sleep", new=AsyncMock()),
            patch("mistralai.workflows.core.worker.logger", new=mock_logger),
        ):
            await _auto_register_as_current_version(
                temporal_client=client,
                namespace="default",
                deployment_name="dep",
                build_id="build-1",
            )

        assert client.workflow_service.set_worker_deployment_current_version.call_count == 1
        assert mock_logger.error.call_count == 0
        mock_logger.info.assert_called_once()

    async def test_transient_error_then_success_still_retries(self) -> None:
        """A genuinely transient error must still be retried until the deployment is available."""
        transient = _rpc_error("worker deployment not found", RPCStatusCode.NOT_FOUND)
        client = _client_raising([transient, None])
        mock_logger = MagicMock()

        with (
            patch("asyncio.sleep", new=AsyncMock()),
            patch("mistralai.workflows.core.worker.logger", new=mock_logger),
        ):
            await _auto_register_as_current_version(
                temporal_client=client,
                namespace="default",
                deployment_name="dep",
                build_id="build-1",
            )

        assert client.workflow_service.set_worker_deployment_current_version.call_count == 2
        assert mock_logger.error.call_count == 0
        mock_logger.info.assert_called_once()
