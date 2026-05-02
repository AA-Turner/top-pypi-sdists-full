from unittest.mock import patch

import httpx
import pytest

import scale_gp_beta.lib.tracing.trace_queue_manager as tqm
from scale_gp_beta import SGPClient
from scale_gp_beta.lib.tracing.trace_queue_manager import TraceQueueManager


@pytest.fixture
def mock_transport() -> httpx.MockTransport:
    def handler(_request: httpx.Request):
        return httpx.Response(200, json={"ok": True})

    return httpx.MockTransport(handler)


@pytest.fixture
def real_sgp_client(mock_transport: httpx.MockTransport) -> SGPClient:
    """
    Creates a REAL SGPClient instance but with a mocked transport layer
    to prevent actual network calls.
    """
    return SGPClient(
        api_key="dummy_key",
        account_id="dummy_account_id",
        http_client=httpx.Client(transport=mock_transport),
    )


class TestRegisterClient:
    # Following 3 tests are to ensure that our monkey patch on SGPClient _prepare_request remains valid.
    # They should fail if Stainless changes some internals.
    def test_prepare_request_is_patched(self, real_sgp_client: SGPClient):
        """
        Verifies that our custom wrapper successfully replaces the '_prepare_request' method on the client instance.
        """
        original_method = real_sgp_client._prepare_request
        TraceQueueManager(worker_enabled=False, client=real_sgp_client)
        patched_method = real_sgp_client._prepare_request

        assert patched_method is not original_method
        assert patched_method.__name__ == "custom_prepare_request"

    def test_patch_calls_original_method(self, real_sgp_client: SGPClient):
        """
        Verifies that our custom wrapper correctly calls the original
        `_prepare_request` method, ensuring the chain of execution is not broken. Note that the original is default empty.
        But the user may have added something themselves.
        """
        manager = TraceQueueManager(worker_enabled=False)

        with patch.object(real_sgp_client, '_prepare_request', wraps=real_sgp_client._prepare_request) as mock_original:
            manager.register_client(real_sgp_client)

            real_sgp_client.spans.search()

            mock_original.assert_called_once()
            call_args = mock_original.call_args[0]
            assert len(call_args) == 1
            assert isinstance(call_args[0], httpx.Request)

    def test_patching_contract_against_real_client(self, real_sgp_client: SGPClient):
        """
        It ensures that our patching logic is compatible with the real client's
        method signature and request lifecycle. If Stainless changes the internal
        API, this test should fail.
        """
        TraceQueueManager(worker_enabled=False, client=real_sgp_client)

        try:
            # If `_prepare_request`'s signature changes, this line will raise an error.
            response = real_sgp_client.spans.search()
            assert response is not None
        except TypeError as e:
            pytest.fail(
                f"Contract broken! The signature of `_prepare_request` may have changed. Error: {e}"
            )
        except Exception as e:
            pytest.fail(f"An unexpected error occurred during the patched request: {e}")


class TestInit:
    @pytest.fixture(autouse=True)
    def reset_global_manager(self):
        """Reset the singleton before and after each test."""
        tqm._global_tracing_queue_manager = None
        yield
        tqm._global_tracing_queue_manager = None

    def _make_client(self, mock_transport: httpx.MockTransport, account_id: str) -> SGPClient:
        return SGPClient(
            api_key="dummy_key",
            account_id=account_id,
            http_client=httpx.Client(transport=mock_transport),
        )

    def test_second_init_with_new_client_updates_client(self, mock_transport: httpx.MockTransport):
        """
        Regression test for multi-tenant credential leakage (DUC / SGP-Multitenant-Prod).

        When init() is called a second time with a different client, the singleton's
        client must be updated so spans are created and patched under the correct tenant.
        Previously, the early-return on line 186 silently dropped the new client,
        causing subsequent span PATCHes to 404 because the span was created under
        the first tenant's credentials.
        """
        client_a = self._make_client(mock_transport, "tenant-a")
        client_b = self._make_client(mock_transport, "tenant-b")

        tqm.init(client=client_a)
        assert tqm._global_tracing_queue_manager is not None
        assert tqm._global_tracing_queue_manager.client is client_a

        tqm.init(client=client_b)
        assert tqm._global_tracing_queue_manager.client is client_b, (
            "init() with a new client should update the singleton's client via register_client()"
        )

    def test_second_init_without_client_does_not_clear_existing_client(self, mock_transport: httpx.MockTransport):
        """Calling init() a second time with no client should leave the existing client intact."""
        client_a = self._make_client(mock_transport, "tenant-a")

        tqm.init(client=client_a)
        tqm.init(client=None)

        manager = tqm._global_tracing_queue_manager
        assert manager is not None
        assert manager.client is client_a
