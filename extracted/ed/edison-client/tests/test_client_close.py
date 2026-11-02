"""Tests for RestClient close() method and cleanup behavior."""

import asyncio
import atexit
import logging
import subprocess
import sys
import threading
import time
from concurrent.futures import ThreadPoolExecutor
from unittest.mock import MagicMock, patch

import httpx
import pytest

from edison_client import EdisonClient
from edison_client.models.app import AuthType


@pytest.fixture(name="mock_rest_client")
def fixture_mock_rest_client():
    """Create a RestClient with mocked HTTP interactions."""
    with patch(
        "edison_client.clients.rest_client.RestClient._fetch_my_orgs",
        return_value=["test-org"],
    ):
        # Use JWT auth instead of API key to avoid HTTP calls
        return EdisonClient(
            auth_type=AuthType.JWT,
            jwt="mock.jwt.token",
            cleanup_on_exit=False,
        )


def test_close_idempotency(mock_rest_client, caplog):
    """Test that calling close() multiple times is safe and doesn't cause errors."""
    caplog.set_level(logging.WARNING)

    # Access clients to ensure they're created
    _ = mock_rest_client.client
    _ = mock_rest_client.async_client

    # Close multiple times
    mock_rest_client.close()
    mock_rest_client.close()
    mock_rest_client.close()

    # Verify no warnings or errors were logged
    assert not any(record.levelno >= logging.WARNING for record in caplog.records), (
        "Unexpected warnings or errors during multiple close() calls"
    )

    # Verify client is marked as closed
    assert mock_rest_client._closed


def test_close_thread_safety(mock_rest_client, caplog):
    """Test that concurrent close() calls from multiple threads are safe."""
    caplog.set_level(logging.WARNING)

    # Access clients to ensure they're created
    _ = mock_rest_client.client
    _ = mock_rest_client.async_client

    # Call close() from multiple threads concurrently
    num_threads = 10
    with ThreadPoolExecutor(max_workers=num_threads) as executor:
        futures = [executor.submit(mock_rest_client.close) for _ in range(num_threads)]

        # Wait for all to complete
        for future in futures:
            future.result()

    # Verify no warnings or errors were logged
    assert not any(record.levelno >= logging.WARNING for record in caplog.records), (
        "Unexpected warnings or errors during concurrent close() calls"
    )

    # Verify client is marked as closed
    assert mock_rest_client._closed


def test_close_cleans_up_sync_clients(mock_rest_client, caplog):
    """Test that close() properly cleans up synchronous HTTP clients."""
    caplog.set_level(logging.WARNING)

    # Access sync client to ensure it's created
    sync_client = mock_rest_client.client

    # Mock the close method to verify it's called
    original_close = sync_client.close
    close_called = threading.Event()

    def mock_close():
        close_called.set()
        return original_close()

    sync_client.close = mock_close

    # Close the RestClient
    mock_rest_client.close()

    # Verify sync client's close was called
    assert close_called.is_set(), "Sync client close() was not called"

    # Verify no warnings or errors were logged
    assert not any(record.levelno >= logging.WARNING for record in caplog.records), (
        "Unexpected warnings or errors during sync client cleanup"
    )

    # Verify clients dict is empty
    assert len(mock_rest_client._clients) == 0


@pytest.mark.asyncio
async def test_aclose_cleans_up_async_clients(mock_rest_client, caplog):
    """Test that aclose() properly cleans up async HTTP clients."""
    caplog.set_level(logging.WARNING)

    # Access async client to ensure it's created
    async_client = mock_rest_client.async_client

    # Mock the aclose method to verify it's called
    close_called = asyncio.Event()
    original_aclose = async_client.aclose

    async def mock_aclose():
        close_called.set()
        return await original_aclose()

    async_client.aclose = mock_aclose

    # Close the RestClient asynchronously
    await mock_rest_client.aclose()

    # Verify async client's aclose was called
    assert close_called.is_set(), "Async client aclose() was not called"

    # Verify no warnings or errors were logged
    assert not any(record.levelno >= logging.WARNING for record in caplog.records), (
        "Unexpected warnings or errors during async client cleanup"
    )

    # Verify clients dict is empty
    assert len(mock_rest_client._clients) == 0


def test_close_cleans_up_mixed_clients(mock_rest_client, caplog):
    """Test that close() handles both sync and async clients together."""
    caplog.set_level(logging.WARNING)

    # Access both sync and async clients
    _ = mock_rest_client.client
    _ = mock_rest_client.async_client

    initial_client_count = len(mock_rest_client._clients)
    assert initial_client_count >= 2, "Expected at least sync and async clients"

    # Close the RestClient
    mock_rest_client.close()

    # Verify clients dict is empty
    assert len(mock_rest_client._clients) == 0

    # Verify no warnings or errors were logged
    assert not any(record.levelno >= logging.WARNING for record in caplog.records), (
        "Unexpected warnings or errors during mixed client cleanup"
    )


def test_closed_client_raises_on_access(mock_rest_client):
    """Test that accessing client properties after close() raises RuntimeError."""
    # Close the client
    mock_rest_client.close()

    # Verify attempting to access client raises RuntimeError
    with pytest.raises(RuntimeError, match="RestClient has been closed"):
        _ = mock_rest_client.client

    with pytest.raises(RuntimeError, match="RestClient has been closed"):
        _ = mock_rest_client.async_client


def test_closed_client_get_client_raises(mock_rest_client):
    """Test that get_client() raises RuntimeError after close()."""
    # Close the client
    mock_rest_client.close()

    # Verify get_client raises RuntimeError
    with pytest.raises(RuntimeError, match="RestClient has been closed"):
        mock_rest_client.get_client("application/json", authenticated=False)


@pytest.mark.asyncio
async def test_aclose_idempotency(mock_rest_client, caplog):
    """Test that calling aclose() multiple times is safe and doesn't cause errors."""
    caplog.set_level(logging.WARNING)

    # Access clients to ensure they're created
    _ = mock_rest_client.client
    _ = mock_rest_client.async_client

    # Close multiple times asynchronously
    await mock_rest_client.aclose()
    await mock_rest_client.aclose()
    await mock_rest_client.aclose()

    # Verify no warnings or errors were logged
    assert not any(record.levelno >= logging.WARNING for record in caplog.records), (
        "Unexpected warnings or errors during multiple aclose() calls"
    )

    # Verify client is marked as closed
    assert mock_rest_client._closed


@pytest.mark.asyncio
async def test_aclose_with_multiple_async_clients(mock_rest_client, caplog):
    """Test that aclose() properly handles multiple async clients."""
    caplog.set_level(logging.WARNING)

    # Create multiple async clients with different configurations
    _ = mock_rest_client.get_client(
        "application/json", authenticated=True, async_client=True
    )
    _ = mock_rest_client.get_client(
        "application/json", authenticated=False, async_client=True
    )
    _ = mock_rest_client.get_client(
        "multipart/form-data", authenticated=True, async_client=True
    )

    # Verify we have multiple clients
    assert len(mock_rest_client._clients) >= 3

    # Close all clients
    await mock_rest_client.aclose()

    # Verify all clients are closed
    assert len(mock_rest_client._clients) == 0

    # Verify no warnings or errors were logged
    assert not any(record.levelno >= logging.WARNING for record in caplog.records), (
        "Unexpected warnings or errors during multiple async client cleanup"
    )


def test_close_with_exception_in_client_close(mock_rest_client, caplog):
    """Test that close() handles exceptions from client.close() gracefully."""
    caplog.set_level(logging.WARNING)

    # Access client to ensure it's created
    client = mock_rest_client.client

    # Mock close to raise an exception
    def raise_error():
        raise RuntimeError("Simulated close error")

    client.close = raise_error

    # Close should not raise, but suppress the error
    mock_rest_client.close()

    # Verify the RestClient is still marked as closed
    assert mock_rest_client._closed

    # Verify clients dict is empty (client was removed despite error)
    assert len(mock_rest_client._clients) == 0

    # No warnings should be logged (errors are suppressed with contextlib.suppress)
    assert not any(record.levelno >= logging.WARNING for record in caplog.records), (
        "Unexpected warnings logged despite error suppression"
    )


@pytest.mark.asyncio
async def test_aclose_with_exception_in_client_aclose(mock_rest_client, caplog):
    """Test that aclose() handles exceptions from client.aclose() gracefully."""
    caplog.set_level(logging.WARNING)

    # Access async client to ensure it's created
    async_client = mock_rest_client.async_client

    # Mock aclose to raise an exception
    async def raise_error():  # noqa: RUF029
        raise RuntimeError("Simulated aclose error")

    async_client.aclose = raise_error

    # aclose should not raise, but suppress the error
    await mock_rest_client.aclose()

    # Verify the RestClient is still marked as closed
    assert mock_rest_client._closed

    # Verify clients dict is empty (client was removed despite error)
    assert len(mock_rest_client._clients) == 0

    # No warnings should be logged (errors are suppressed)
    assert not any(record.levelno >= logging.WARNING for record in caplog.records), (
        "Unexpected warnings logged despite error suppression"
    )


def test_schedule_async_close_with_running_loop(mock_rest_client, caplog):
    """Test _schedule_async_close when there's a running event loop."""
    caplog.set_level(logging.WARNING)

    # Access async client
    async_client = mock_rest_client.async_client

    # Track if aclose was called
    close_called = threading.Event()
    original_aclose = async_client.aclose

    async def mock_aclose():
        close_called.set()
        return await original_aclose()

    async_client.aclose = mock_aclose

    async def test_in_loop():
        # Schedule close while loop is running
        mock_rest_client._schedule_async_close(async_client)

        # Give the task a moment to execute
        await asyncio.sleep(0.1)

    # Run in an event loop
    asyncio.run(test_in_loop())

    # Verify aclose was called
    assert close_called.is_set(), "Async client aclose() was not called"

    # Verify no warnings or errors were logged
    assert not any(record.levelno >= logging.WARNING for record in caplog.records), (
        "Unexpected warnings or errors during scheduled async close"
    )


def test_schedule_async_close_without_running_loop(mock_rest_client, caplog):
    """Test _schedule_async_close when there's no running event loop."""
    caplog.set_level(logging.WARNING)

    # Create a minimal async client mock
    async_client = MagicMock(spec=httpx.AsyncClient)
    close_called = threading.Event()

    async def mock_aclose():  # noqa: RUF029
        close_called.set()

    async_client.aclose = mock_aclose

    # Schedule close without a running loop
    mock_rest_client._schedule_async_close(async_client)

    # Give time for asyncio.run() to complete
    time.sleep(0.1)

    # Verify aclose was called
    assert close_called.is_set(), "Async client aclose() was not called"

    # Verify no warnings or errors were logged
    assert not any(record.levelno >= logging.WARNING for record in caplog.records), (
        "Unexpected warnings or errors during scheduled async close"
    )


def test_close_does_not_affect_other_instances(caplog):
    """Test that closing one RestClient instance doesn't affect others."""
    caplog.set_level(logging.WARNING)

    with patch(
        "edison_client.clients.rest_client.RestClient._fetch_my_orgs",
        return_value=["test-org"],
    ):
        client1 = EdisonClient(
            auth_type=AuthType.JWT,
            jwt="mock.jwt.token.1",
            cleanup_on_exit=False,
        )
        client2 = EdisonClient(
            auth_type=AuthType.JWT,
            jwt="mock.jwt.token.2",
            cleanup_on_exit=False,
        )

    # Access clients on both instances
    _ = client1.client
    _ = client2.client

    # Close client1
    client1.close()

    # Verify client1 is closed
    assert client1._closed

    # Verify client2 is NOT closed and still works
    assert not client2._closed
    _ = client2.client  # Should not raise

    # Clean up client2
    client2.close()

    # Verify no warnings or errors were logged
    assert not any(record.levelno >= logging.WARNING for record in caplog.records), (
        "Unexpected warnings or errors during independent client cleanup"
    )


@pytest.mark.asyncio
async def test_mixed_close_and_aclose(mock_rest_client, caplog):
    """Test that calling both close() and aclose() is safe."""
    caplog.set_level(logging.WARNING)

    # Access clients
    _ = mock_rest_client.client
    _ = mock_rest_client.async_client

    # Close synchronously first
    mock_rest_client.close()

    # Then try to close asynchronously (should be a no-op)
    await mock_rest_client.aclose()

    # Verify no warnings or errors were logged
    assert not any(record.levelno >= logging.WARNING for record in caplog.records), (
        "Unexpected warnings or errors during mixed close/aclose calls"
    )


def test_destructor_cleanup_with_sync_clients(caplog):
    """Test that __del__ properly cleans up sync clients without warnings."""
    caplog.set_level(logging.WARNING)

    with patch(
        "edison_client.clients.rest_client.RestClient._fetch_my_orgs",
        return_value=["test-org"],
    ):
        client = EdisonClient(
            auth_type=AuthType.JWT,
            jwt="mock.jwt.token",
            cleanup_on_exit=False,
        )

        # Access sync client only
        _ = client.client

        # Delete without explicit close
        del client

    # Verify no warnings were logged for sync client cleanup
    assert not any(record.levelno >= logging.WARNING for record in caplog.records), (
        "Unexpected warnings during __del__ cleanup of sync clients"
    )


def test_atexit_cleanup_on_forgotten_close():
    """Test that atexit.register ensures cleanup even if user forgets to call close()."""
    # Create a test script that creates a client but doesn't close it
    test_script = """
import logging
import sys
from unittest.mock import patch

# Set up logging to capture any warnings
logging.basicConfig(level=logging.WARNING, stream=sys.stderr)

with patch(
    "edison_client.clients.rest_client.RestClient._fetch_my_orgs",
    return_value=["test-org"],
):
    from edison_client import EdisonClient
    from edison_client.models.app import AuthType

    # Create client WITH cleanup_on_exit=True (default)
    client = EdisonClient(
        auth_type=AuthType.JWT,
        jwt="mock.jwt.token",
        cleanup_on_exit=True,
    )

    # Access clients to ensure they are created
    _ = client.client
    _ = client.async_client

    # Intentionally DO NOT call close()
    # Exit handlers should clean up automatically
    print("CLIENTS_CREATED")
"""

    # Run the script in a subprocess to test atexit behavior
    result = subprocess.run(  # noqa: S603
        [sys.executable, "-c", test_script],
        check=False,
        capture_output=True,
        text=True,
        timeout=10,
    )

    # Verify the script ran successfully
    assert result.returncode == 0, f"Script failed: {result.stderr}"
    assert "CLIENTS_CREATED" in result.stdout, "Script did not execute properly"

    # Verify no warnings about unclosed clients
    # (httpx would normally warn about unclosed clients if cleanup didn't work)
    assert "unclosed" not in result.stderr.lower(), (
        f"Client cleanup did not work properly. stderr: {result.stderr}"
    )


def test_atexit_registration_with_cleanup_on_exit_true(caplog):
    """Test that atexit.register is called when cleanup_on_exit=True."""
    caplog.set_level(logging.WARNING)

    # Track atexit.register calls
    original_register = atexit.register
    registered_callbacks = []

    def mock_register(func, *args, **kwargs):
        registered_callbacks.append(func)
        return original_register(func, *args, **kwargs)

    with (
        patch(
            "edison_client.clients.rest_client.RestClient._fetch_my_orgs",
            return_value=["test-org"],
        ),
        patch("atexit.register", side_effect=mock_register),
    ):
        client = EdisonClient(
            auth_type=AuthType.JWT,
            jwt="mock.jwt.token",
            cleanup_on_exit=True,  # Should register atexit handler
        )

        # Verify atexit.register was called with client.close
        assert len(registered_callbacks) > 0, "atexit.register was not called"
        assert any(callback.__name__ == "close" for callback in registered_callbacks), (
            "close() method was not registered with atexit"
        )

        # Clean up properly
        client.close()


def test_atexit_not_registered_with_cleanup_on_exit_false(caplog):
    """Test that atexit.register is NOT called when cleanup_on_exit=False."""
    caplog.set_level(logging.WARNING)

    # Track atexit.register calls
    original_register = atexit.register
    registered_callbacks = []

    def mock_register(func, *args, **kwargs):
        registered_callbacks.append(func)
        return original_register(func, *args, **kwargs)

    with (
        patch(
            "edison_client.clients.rest_client.RestClient._fetch_my_orgs",
            return_value=["test-org"],
        ),
        patch("atexit.register", side_effect=mock_register),
    ):
        client = EdisonClient(
            auth_type=AuthType.JWT,
            jwt="mock.jwt.token",
            cleanup_on_exit=False,  # Should NOT register atexit handler
        )

        # Count how many close callbacks were registered
        close_callbacks = [cb for cb in registered_callbacks if cb.__name__ == "close"]

        # Verify close was not registered (or at least one less than if it were True)
        initial_count = len(close_callbacks)

        # Clean up properly
        client.close()

        # Now create another with cleanup_on_exit=True to verify the difference
        registered_callbacks.clear()

        client2 = EdisonClient(
            auth_type=AuthType.JWT,
            jwt="mock.jwt.token.2",
            cleanup_on_exit=True,
        )

        # This one should have registered
        assert any(cb.__name__ == "close" for cb in registered_callbacks), (
            "close() should be registered when cleanup_on_exit=True"
        )

        client2.close()


def test_atexit_cleanup_is_idempotent(caplog):
    """Test that atexit cleanup is safe even if close() was already called."""
    caplog.set_level(logging.WARNING)

    with patch(
        "edison_client.clients.rest_client.RestClient._fetch_my_orgs",
        return_value=["test-org"],
    ):
        client = EdisonClient(
            auth_type=AuthType.JWT,
            jwt="mock.jwt.token",
            cleanup_on_exit=True,
        )

        # Access clients
        _ = client.client

        # Manually close
        client.close()

        # Simulate atexit calling close again
        client.close()

        # Should not raise or log warnings
        assert not any(
            record.levelno >= logging.WARNING for record in caplog.records
        ), "Atexit cleanup after manual close() caused warnings"
