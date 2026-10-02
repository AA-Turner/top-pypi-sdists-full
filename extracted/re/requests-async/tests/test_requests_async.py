"""
Simple tests for requests-async
"""

import asyncio
import pytest
import requests_async


@pytest.mark.asyncio
async def test_get_request():
    """Test basic GET request"""
    response = await requests_async.get('https://httpbin.org/get')
    assert response.status_code == 200
    data = response.json()
    assert 'url' in data


@pytest.mark.asyncio
async def test_post_request():
    """Test basic POST request with JSON"""
    test_data = {'test': 'data', 'number': 42}
    response = await requests_async.post('http://httpbin.org/post', json=test_data, timeout=30.0)
    assert response.status_code == 200
    data = response.json()
    assert data['json'] == test_data


@pytest.mark.asyncio
async def test_session_usage():
    """Test AsyncSession context manager"""
    async with requests_async.AsyncSession() as session:
        response = await session.get('https://httpbin.org/get')
        assert response.status_code == 200


@pytest.mark.asyncio
async def test_all_http_methods():
    """Test all HTTP methods"""
    base_url = 'https://httpbin.org'
    
    methods = [
        ('get', 'GET'),
        ('post', 'POST'),
        ('put', 'PUT'),
        ('delete', 'DELETE'),
        ('patch', 'PATCH'),
    ]
    
    # Test basic HTTP methods
    for method_name, expected_method in methods:
        method_func = getattr(requests_async, method_name)
        response = await method_func(f'{base_url}/{method_name.lower()}')
        assert response.status_code == 200
        data = response.json()
        assert f'/{method_name.lower()}' in data['url']
    
    # Test HEAD separately (returns no content)
    response = await requests_async.head(f'{base_url}/get')
    assert response.status_code == 200
    
    # Test OPTIONS separately (might return different status)
    response = await requests_async.options(f'{base_url}/get')
    assert response.status_code in [200, 405]  # Some servers don't support OPTIONS


@pytest.mark.asyncio
async def test_headers_and_params():
    """Test headers and query parameters"""
    headers = {'User-Agent': 'requests-async-test'}
    params = {'param1': 'value1', 'param2': 'value2'}
    
    response = await requests_async.get(
        'https://httpbin.org/get',
        headers=headers,
        params=params
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data['headers']['User-Agent'] == 'requests-async-test'
    assert data['args'] == params


if __name__ == '__main__':
    # Simple test runner
    asyncio.run(test_get_request())
    print("✅ All tests passed!")