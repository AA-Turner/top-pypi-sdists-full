import asyncio
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from unittest.mock import AsyncMock, MagicMock
from v2.nacos.common.client_config_builder import ClientConfigBuilder
from v2.nacos.ai.remote.ai_http_client_proxy import AiHttpClientProxy
from v2.nacos.common.constants import Constants

async def main():
    client_config = (ClientConfigBuilder()
                     .server_address('localhost:8848')
                     .build())
    
    # 构造最小化 proxy 对象
    proxy = AiHttpClientProxy.__new__(AiHttpClientProxy)
    proxy.client_config = client_config
    proxy.app_name = 'test-app'
    proxy.namespace_id = ''

    # Mock nacos_server_connector.inject_security_info
    mock_connector = MagicMock()
    mock_connector.inject_security_info = AsyncMock(return_value=None)
    proxy.nacos_server_connector = mock_connector

    headers = await proxy._build_headers()
    
    assert 'Client-Version' in headers, "Missing Client-Version header"
    assert 'User-Agent' in headers, "Missing User-Agent header"
    assert headers['Client-Version'] == Constants.CLIENT_VERSION, f"Client-Version mismatch: {headers['Client-Version']}"
    assert headers['User-Agent'] == Constants.CLIENT_VERSION, f"User-Agent mismatch: {headers['User-Agent']}"
    assert 'Nacos-Python-Client:v3.2.0' in headers['Client-Version'], f"Version not 3.2.0: {headers['Client-Version']}"
    
    print(f"✅ Client-Version: {headers['Client-Version']}")
    print(f"✅ User-Agent: {headers['User-Agent']}")
    print("✅ HTTP version headers verified!")

asyncio.run(main())
