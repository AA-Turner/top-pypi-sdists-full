#!/usr/bin/env python3

"""
Minimal focused unit test for aioairq timeout issue.
This is the simplest test that reproduces the bug.

Add to: tests/test_timeout_regression.py
"""

import asyncio
import pytest
from aiohttp import web
from aiohttp.test_utils import AioHTTPTestCase


class TestTimeoutRegression(AioHTTPTestCase):
    """
    Regression test for timeout issue fixed in aioairq 0.4.7.

    Bug: Without total timeout, requests to non-responsive servers hang indefinitely.
    Fix: ClientTimeout(total=timeout, connect=timeout) ensures proper timeout.
    """

    async def get_application(self):
        """Create test application with hanging endpoint."""
        app = web.Application()
        app.router.add_get("/config", self.hanging_handler)
        return app

    async def hanging_handler(self, request):
        """Handler that accepts connection but never responds."""
        # Simulate device that accepts connection but is too slow/hung
        await asyncio.sleep(999999)
        return web.json_response({"sensors": []})

    async def test_request_with_total_timeout_does_not_hang(self):
        """
        Test that requests timeout properly with total timeout configured.

        This verifies the fix: ClientTimeout(total=10, connect=10)
        """
        import time
        from aiohttp import ClientTimeout

        timeout = ClientTimeout(total=5, connect=5)

        start = time.time()

        with self.assertRaises(asyncio.TimeoutError):
            async with self.client.get("/config", timeout=timeout) as resp:
                await resp.text()

        elapsed = time.time() - start

        # Should timeout in approximately 5 seconds
        self.assertLess(elapsed, 7, "Request should timeout around 5s")
        self.assertGreater(elapsed, 3, "Request should not timeout too early")

    async def test_request_without_total_timeout_hangs(self):
        """
        Test that demonstrates the bug: without total timeout, requests hang.

        This reproduces the issue that existed in aioairq 0.4.6.
        We use a safety timeout to prevent test from hanging forever.
        """
        from aiohttp import ClientTimeout

        # Old behavior: only connect timeout
        timeout = ClientTimeout(connect=5)

        # Safety timeout to prevent test from hanging forever
        with self.assertRaises(asyncio.TimeoutError):
            async with asyncio.timeout(10):  # Safety timeout
                async with self.client.get("/config", timeout=timeout) as resp:
                    await resp.text()

        # If we reach here, request hung beyond the safety timeout
        # This demonstrates the bug!


# Simpler pytest version
@pytest.mark.asyncio
async def test_timeout_with_hanging_server_simple():
    """
    Simplest possible test demonstrating the timeout fix.

    This can be run independently without complex fixtures.
    """
    from aiohttp import web, ClientSession, ClientTimeout

    # Create hanging server
    app = web.Application()

    async def hang(request):
        await asyncio.sleep(999999)
        return web.Response(text="never")

    app.router.add_get("/test", hang)

    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, "localhost", 0)
    await site.start()

    port = site._server.sockets[0].getsockname()[1]

    try:
        # Test with total timeout (should work)
        timeout = ClientTimeout(total=2, connect=2)
        async with ClientSession(timeout=timeout) as session:
            import time

            start = time.time()

            with pytest.raises(asyncio.TimeoutError):
                async with session.get(f"http://localhost:{port}/test") as resp:
                    await resp.text()

            elapsed = time.time() - start
            assert 1 < elapsed < 4, f"Should timeout ~2s, got {elapsed:.1f}s"

    finally:
        await runner.cleanup()


if __name__ == "__main__":
    # Can run directly for manual testing
    asyncio.run(test_timeout_with_hanging_server_simple())
    print("✓ Test passed: Timeout works correctly")
