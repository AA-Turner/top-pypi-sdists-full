"""
Proxy tests for requests-async (optional)
These tests require a working proxy server
"""

import pytest
import requests_async


# Proxy configuration - update these if you have access to test proxies
TEST_HTTP_PROXY = None  # "http://user:pass@proxy:port"  
TEST_SOCKS5_PROXY = None  # "socks5://user:pass@proxy:port"


@pytest.mark.skipif(TEST_HTTP_PROXY is None, reason="No HTTP proxy configured")
@pytest.mark.asyncio
async def test_http_proxy():
    """Test HTTP proxy functionality"""
    async with requests_async.AsyncSession(proxies=TEST_HTTP_PROXY) as session:
        response = await session.get('http://httpbin.org/ip')
        assert response.status_code == 200
        # Proxy should change the IP address
        data = response.json()
        assert 'origin' in data


@pytest.mark.skipif(TEST_SOCKS5_PROXY is None, reason="No SOCKS5 proxy configured") 
@pytest.mark.asyncio
async def test_socks5_proxy():
    """Test SOCKS5 proxy functionality"""
    async with requests_async.AsyncSession(proxies=TEST_SOCKS5_PROXY) as session:
        response = await session.get('http://httpbin.org/ip')
        assert response.status_code == 200
        data = response.json()
        assert 'origin' in data


@pytest.mark.asyncio
async def test_proxy_dict_format():
    """Test proxy configuration with dict format"""
    # This test just verifies the proxy parameter is accepted
    # without actually using a proxy
    proxies = {"http://": "http://proxy:8080", "https://": "https://proxy:8080"}
    
    # Should not raise an error during initialization
    async with requests_async.AsyncSession(proxies=proxies) as session:
        assert session._client_kwargs.get('proxy') is not None