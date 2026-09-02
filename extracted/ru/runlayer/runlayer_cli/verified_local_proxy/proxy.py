"""Verified Local MCP Proxy - Core proxy logic."""

from __future__ import annotations

import os
import threading
import time
from collections.abc import Awaitable, Callable

import anyio
import structlog
from fastmcp.client.transports import SSETransport, StreamableHttpTransport
from fastmcp.server.proxy import FastMCPProxy, ProxyClient

from runlayer_cli.middleware import RunlayerMiddleware

from runlayer_cli.verified_local_proxy.config import VerificationConfig
from runlayer_cli.verified_local_proxy.exceptions import (
    TargetNotRunningError,
    VerificationError,
)
from runlayer_cli.verified_local_proxy.verification import get_verifier

logger = structlog.get_logger(__name__)

# Global flag to signal re-verification threads to stop
_stop_reverification = threading.Event()

# Heartbeat tracking for watchdog
_heartbeat_time: float = 0.0
_heartbeat_lock = threading.Lock()

# Grace period for verification to complete (accounts for subprocess timeouts + overhead)
_VERIFICATION_TIMEOUT_SECONDS = 120


def _update_heartbeat() -> None:
    """Update the heartbeat timestamp after successful verification."""
    global _heartbeat_time
    with _heartbeat_lock:
        _heartbeat_time = time.monotonic()


def _get_heartbeat() -> float:
    """Get the current heartbeat timestamp."""
    with _heartbeat_lock:
        return _heartbeat_time


def _get_transport(
    config: VerificationConfig,
    identity_forward_headers: dict[str, str] | None = None,
) -> SSETransport | StreamableHttpTransport:
    """Get the appropriate transport for the target URL.

    ``identity_forward_headers`` is held by reference — the refresh loop
    mutates it in place, same as the ordinary local path in ``main.run``.
    """
    url = config.target_url
    headers = identity_forward_headers
    # Use SSE transport if the path contains /sse
    if "/sse" in config.target_path.lower():
        return SSETransport(url, headers=headers)
    else:
        return StreamableHttpTransport(url, headers=headers)


def verify_target(
    config: VerificationConfig, max_retries: int = 3, retry_delay: float = 2.0
) -> None:
    """
    Verify the target process is running and has valid signature.

    Args:
        config: Verification configuration
        max_retries: Maximum number of retries to find the process
        retry_delay: Delay in seconds between retries

    Raises:
        TargetNotRunningError: If target process not found after retries
        VerificationError: If signature verification fails
    """
    verifier = get_verifier()
    port = config.target_port

    # Try to find the process with retries
    process_info = None
    for attempt in range(max_retries):
        logger.debug(
            f"Looking for process on port {port} (attempt {attempt + 1}/{max_retries})..."
        )
        process_info = verifier.find_process_on_port(port)

        if process_info:
            logger.debug(
                f"Found process: {process_info.name} (PID: {process_info.pid}) at {process_info.binary_path}"
            )
            break

        if attempt < max_retries - 1:
            logger.debug(f"Process not found, retrying in {retry_delay}s...")
            time.sleep(retry_delay)

    if not process_info:
        raise TargetNotRunningError(
            f"No process found listening on port {port} after {max_retries} attempts. "
            f"Please ensure {config.display_name} is running."
        )

    # Verify signature
    logger.debug(f"Verifying signature for {process_info.binary_path}...")
    verifier.verify_signature(process_info, config)
    logger.info(f"Signature verified for {config.display_name}")


def wait_for_target(config: VerificationConfig, poll_interval: float = 5.0) -> None:
    """
    Wait for the target process to start and verify its signature.

    This function polls until the target is found and verified, or until
    the timeout is reached (if configured).

    Args:
        config: Verification configuration
        poll_interval: Seconds between poll attempts

    Raises:
        TargetNotRunningError: If timeout is reached without finding target
        VerificationError: If found target has invalid signature
    """
    timeout = config.wait_timeout_seconds
    start_time = time.monotonic()

    logger.debug(f"Waiting for {config.display_name} to start...")
    if timeout:
        logger.debug(f"Timeout: {timeout}s")

    attempt = 0
    while True:
        attempt += 1

        # Check timeout
        if timeout:
            elapsed = time.monotonic() - start_time
            if elapsed >= timeout:
                raise TargetNotRunningError(
                    f"Timeout ({timeout}s) waiting for {config.display_name} to start"
                )

        try:
            # Try to verify (single attempt)
            verify_target(config, max_retries=1, retry_delay=0)
            return  # Success!
        except TargetNotRunningError:
            # Not running yet, keep waiting
            if attempt % 12 == 1:  # Log every ~60s (12 * 5s)
                logger.debug(f"Still waiting for {config.display_name}...")
            time.sleep(poll_interval)
        except VerificationError:
            # Found but invalid signature - this is a real error
            raise


def _reverification_loop(config: VerificationConfig) -> None:
    """
    Background loop that periodically re-verifies the target process.

    This mitigates TOCTOU (time-of-check to time-of-use) attacks where
    a risky process could replace the verified process after initial check.

    If re-verification fails:
    - With retry_on_target_loss=True: Keep trying until target returns
    - With retry_on_target_loss=False: Terminate the proxy
    """
    interval = config.reverify_interval_seconds
    if interval is None:
        return

    logger.debug(f"Starting periodic re-verification every {interval}s")
    if config.retry_on_target_loss:
        logger.debug(
            "Retry on target loss: enabled (proxy will wait for target to restart)"
        )
    _update_heartbeat()  # Initial heartbeat

    target_available = True  # Track if target is currently verified

    while not _stop_reverification.wait(timeout=interval):
        try:
            logger.debug(f"Running periodic re-verification for {config.display_name}")
            verify_target(config, max_retries=1, retry_delay=0)
            logger.debug("Periodic re-verification passed")
            _update_heartbeat()

            # If we were waiting for target to return, log that it's back
            if not target_available:
                logger.info(f"{config.display_name} is back and verified!")
                target_available = True

        except TargetNotRunningError as e:
            _update_heartbeat()  # Thread is alive, just waiting

            if config.retry_on_target_loss:
                if target_available:
                    logger.warning(f"Target lost: {e}")
                    logger.debug(f"Waiting for {config.display_name} to restart...")
                    target_available = False
                # Keep looping - will retry next interval
                continue
            else:
                logger.error(f"SECURITY: Periodic re-verification FAILED: {e}")
                logger.error("Target process is gone. Terminating proxy.")
                os._exit(1)

        except VerificationError as e:
            # Signature mismatch is ALWAYS a security failure
            # Even with retry_on_target_loss, we don't accept invalid signatures
            logger.error(f"SECURITY: Signature verification FAILED: {e}")
            logger.error(
                "Target may have been replaced with risky process. Terminating proxy."
            )
            os._exit(1)

        except Exception as e:
            logger.warning(f"Unexpected error during re-verification: {e}")
            _update_heartbeat()
            continue

    logger.debug("Re-verification loop stopped")


def _watchdog_loop(interval: int) -> None:
    """
    Watchdog that monitors the reverification thread's heartbeat.

    If the reverification thread gets stuck (e.g., subprocess hangs despite timeout,
    or thread is blocked), the watchdog will terminate the process.

    This prevents attacks that try to block reverification indefinitely.
    """
    max_stale = interval + _VERIFICATION_TIMEOUT_SECONDS
    check_interval = min(interval, 30)  # Check at least every 30s

    logger.debug(f"Watchdog started: max heartbeat staleness {max_stale}s")

    while not _stop_reverification.wait(timeout=check_interval):
        heartbeat = _get_heartbeat()
        staleness = time.monotonic() - heartbeat

        if staleness > max_stale:
            logger.error(
                f"SECURITY: Watchdog timeout - reverification heartbeat stale for {staleness:.1f}s "
                f"(max allowed: {max_stale}s)"
            )
            logger.error("Reverification thread may be stuck. Terminating proxy.")
            os._exit(1)  # Hard exit - security critical

    logger.debug("Watchdog stopped")


def create_proxy(
    config: VerificationConfig,
    middleware: RunlayerMiddleware | None = None,
    identity_forward_headers: dict[str, str] | None = None,
) -> FastMCPProxy:
    """Create a FastMCPProxy to the verified target."""
    transport = _get_transport(
        config, identity_forward_headers=identity_forward_headers
    )
    proxy_client = ProxyClient(transport)

    def reuse_client_factory() -> ProxyClient:
        return proxy_client

    proxy = FastMCPProxy(
        client_factory=reuse_client_factory,
        name=f"Runlayer Verified Proxy - {config.display_name}",
    )

    if middleware is not None:
        middleware.proxy = proxy
        proxy.add_middleware(middleware)

    return proxy


def run_proxy(
    config: VerificationConfig,
    skip_verification: bool = False,
    middleware: RunlayerMiddleware | None = None,
    identity_forward_headers: dict[str, str] | None = None,
    identity_forward_refresher: Callable[[], Awaitable[None]] | None = None,
) -> None:
    """Run the verified local proxy (verify -> create proxy -> stdio).

    ``identity_forward_headers`` / ``identity_forward_refresher`` mirror
    ``main.run``; both optional so the standalone entrypoint keeps working
    without a Runlayer backend.
    """
    # Step 1: Verify signature (unless explicitly skipped)
    if skip_verification:
        logger.warning(
            "SIGNATURE VERIFICATION SKIPPED - This is dangerous and should only be used for testing!"
        )
    elif config.wait_for_target:
        # Wait mode: poll until target is available
        wait_for_target(config)
    else:
        # Normal mode: fail if target not immediately available
        verify_target(config)

    # Step 2: Start periodic re-verification + watchdog threads if configured
    reverify_thread = None
    watchdog_thread = None
    if config.reverify_interval_seconds and not skip_verification:
        _stop_reverification.clear()

        # Reverification thread - periodically re-verifies target process
        reverify_thread = threading.Thread(
            target=_reverification_loop,
            args=(config,),
            daemon=True,
            name="reverify-thread",
        )
        reverify_thread.start()

        # Watchdog thread - kills process if reverification gets stuck
        watchdog_thread = threading.Thread(
            target=_watchdog_loop,
            args=(config.reverify_interval_seconds,),
            daemon=True,
            name="watchdog-thread",
        )
        watchdog_thread.start()

    try:
        # Step 3: Create and run proxy
        proxy = create_proxy(
            config,
            middleware=middleware,
            identity_forward_headers=identity_forward_headers,
        )

        async def _run() -> None:
            async with anyio.create_task_group() as tg:
                if identity_forward_refresher is not None:
                    tg.start_soon(identity_forward_refresher)
                await proxy.run_stdio_async(show_banner=False)
                tg.cancel_scope.cancel()

        anyio.run(_run)
    finally:
        # Signal threads to stop
        _stop_reverification.set()
        if reverify_thread and reverify_thread.is_alive():
            reverify_thread.join(timeout=1.0)
        if watchdog_thread and watchdog_thread.is_alive():
            watchdog_thread.join(timeout=1.0)
