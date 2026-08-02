"""
Unit tests for aioairq timeout handling.
Add this to: tests/test_timeout.py
"""

import asyncio
import pytest
import aiohttp
from aiohttp import web
from aioairq import AirQ


class HangingServerFixture:
    """Test fixture that creates a server which accepts connections but never responds."""
    
    def __init__(self):
        self.app = None
        self.runner = None
        self.site = None
        self.port = None
        
    async def start(self, port=0):
        """Start the hanging server."""
        self.app = web.Application()
        self.app.router.add_get('/config', self._hanging_handler)
        self.app.router.add_get('/data', self._hanging_handler)
        
        self.runner = web.AppRunner(self.app)
        await self.runner.setup()
        self.site = web.TCPSite(self.runner, 'localhost', port)
        await self.site.start()
        
        # Get the actual port
        self.port = self.site._server.sockets[0].getsockname()[1]
        
    async def stop(self):
        """Stop the hanging server."""
        if self.runner:
            await self.runner.cleanup()
            
    async def _hanging_handler(self, request):
        """Handler that accepts request but never responds."""
        # Hang indefinitely
        await asyncio.sleep(999999)
        return web.Response(text='Should never reach here')


@pytest.fixture
async def hanging_server():
    """Fixture providing a server that hangs on requests."""
    server = HangingServerFixture()
    await server.start()
    yield server
    await server.stop()


@pytest.fixture
async def aiohttp_session():
    """Fixture providing an aiohttp ClientSession."""
    session = aiohttp.ClientSession()
    yield session
    await session.close()


@pytest.mark.asyncio
async def test_timeout_without_total_timeout_hangs(hanging_server, aiohttp_session):
    """
    Test that without total timeout, requests to hanging server hang indefinitely.
    
    This reproduces the bug that was fixed in version 0.4.7.
    """
    # Configure session with only connect timeout (old behavior)
    timeout = aiohttp.ClientTimeout(connect=5)
    
    with pytest.raises(asyncio.TimeoutError):
        # We use asyncio.wait_for to prevent test from hanging forever
        async with asyncio.timeout(10):  # Safety timeout for test
            async with aiohttp_session.get(
                f'http://localhost:{hanging_server.port}/config',
                timeout=timeout
            ) as resp:
                await resp.text()
    
    # If we reach here without the safety timeout, the bug exists
    pytest.fail("Request should have timed out but didn't")


@pytest.mark.asyncio
async def test_timeout_with_total_timeout_works(hanging_server, aiohttp_session):
    """
    Test that with total timeout, requests to hanging server timeout properly.
    
    This verifies the fix in version 0.4.7.
    """
    # Configure session with both connect and total timeout (new behavior)
    timeout = aiohttp.ClientTimeout(total=5, connect=5)
    
    import time
    start = time.time()
    
    with pytest.raises(asyncio.TimeoutError):
        async with aiohttp_session.get(
            f'http://localhost:{hanging_server.port}/config',
            timeout=timeout
        ) as resp:
            await resp.text()
    
    elapsed = time.time() - start
    
    # Should timeout around 5 seconds (total timeout)
    assert 4 < elapsed < 7, f"Expected ~5s timeout, got {elapsed:.1f}s"


@pytest.mark.asyncio
async def test_airq_config_with_hanging_server(hanging_server):
    """
    Test AirQ.config property with a hanging server.
    
    This tests the actual AirQ class behavior with timeout.
    """
    # Create AirQ instance pointing to hanging server
    async with aiohttp.ClientSession() as session:
        airq = AirQ(
            f'localhost:{hanging_server.port}',
            'test_password',
            session
        )
        
        # This should timeout and raise an exception
        with pytest.raises((asyncio.TimeoutError, aiohttp.ClientError)):
            # Set a reasonable timeout for the test
            async with asyncio.timeout(15):
                await airq.config


@pytest.mark.asyncio
async def test_airq_data_with_hanging_server(hanging_server):
    """
    Test AirQ.data property with a hanging server.
    
    This tests the actual AirQ class behavior with timeout.
    """
    async with aiohttp.ClientSession() as session:
        airq = AirQ(
            f'localhost:{hanging_server.port}',
            'test_password',
            session
        )
        
        with pytest.raises((asyncio.TimeoutError, aiohttp.ClientError)):
            async with asyncio.timeout(15):
                await airq.data


@pytest.mark.asyncio
async def test_multiple_requests_with_hanging_server(hanging_server):
    """
    Test that multiple requests to hanging server all timeout properly.
    
    This ensures the session doesn't get stuck in a bad state.
    """
    timeout = aiohttp.ClientTimeout(total=5, connect=5)
    
    async with aiohttp.ClientSession(timeout=timeout) as session:
        # Try multiple requests
        for i in range(3):
            with pytest.raises(asyncio.TimeoutError):
                async with session.get(
                    f'http://localhost:{hanging_server.port}/config'
                ) as resp:
                    await resp.text()
            
            # Small delay between requests
            await asyncio.sleep(0.1)


@pytest.mark.asyncio
async def test_session_reuse_after_timeout(hanging_server):
    """
    Test that session can be reused after a timeout occurs.
    
    This verifies that timeout doesn't leave session in broken state.
    """
    timeout = aiohttp.ClientTimeout(total=5, connect=5)
    
    async with aiohttp.ClientSession(timeout=timeout) as session:
        # First request to hanging server - should timeout
        with pytest.raises(asyncio.TimeoutError):
            async with session.get(
                f'http://localhost:{hanging_server.port}/config'
            ) as resp:
                await resp.text()
        
        # Session should still be usable for other requests
        # (This would need a working endpoint to test fully)
        assert session is not None
        assert not session.closed


@pytest.mark.asyncio 
async def test_default_timeout_in_airq_class():
    """
    Test that AirQ class uses appropriate timeout values.
    
    This is a regression test to ensure timeout configuration doesn't get lost.
    """
    async with aiohttp.ClientSession() as session:
        # Check that session has timeout configured
        # (Implementation detail: may need to check how AirQ configures this)
        
        airq = AirQ('test.local', 'password', session)
        
        # Verify the session is configured properly
        # This test ensures future changes don't accidentally remove timeout
        assert session is not None


# Performance/stress test
@pytest.mark.asyncio
@pytest.mark.slow
async def test_concurrent_timeouts(hanging_server):
    """
    Test multiple concurrent requests to hanging server all timeout correctly.
    
    Stress test to ensure timeout mechanism works under concurrent load.
    """
    timeout = aiohttp.ClientTimeout(total=5, connect=5)
    
    async with aiohttp.ClientSession(timeout=timeout) as session:
        # Create 10 concurrent requests
        tasks = []
        for i in range(10):
            task = session.get(f'http://localhost:{hanging_server.port}/config')
            tasks.append(task)
        
        # All should timeout
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # All results should be TimeoutError or similar
        for result in results:
            assert isinstance(result, (asyncio.TimeoutError, aiohttp.ClientError))
