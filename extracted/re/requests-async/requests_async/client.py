"""
Async HTTP client implementation based on httpx
"""

import httpx
from typing import Optional, Dict, Any, Union

# Re-export httpx.Response for convenience
Response = httpx.Response


class AsyncSession:
    """
    Async HTTP session with requests-like interface
    
    Example:
        async with AsyncSession() as session:
            response = await session.get('https://httpbin.org/get')
            print(response.json())
    """
    
    def __init__(self, 
                 timeout: Optional[float] = 30.0,
                 headers: Optional[Dict[str, str]] = None,
                 proxies: Optional[Union[str, Dict[str, str]]] = None,
                 **kwargs):
        """
        Initialize async session
        
        Args:
            timeout: Request timeout in seconds (default: 30.0)
            headers: Default headers for all requests
            proxies: Proxy configuration (string or dict)
                    - String: "http://proxy:port" or "socks5://proxy:port"
                    - Dict: {"http://": "http://proxy:port", "https://": "https://proxy:port"}
            **kwargs: Additional httpx.AsyncClient arguments
        """
        # Handle proxy configuration
        if proxies:
            if isinstance(proxies, str):
                # Single proxy string for all protocols
                kwargs['proxy'] = proxies
            elif isinstance(proxies, dict):
                # For requests-style proxy dict, we need to handle it properly
                # Convert requests format to httpx format
                
                # Find the appropriate proxy for HTTPS requests (preferred)
                proxy_url = None
                
                # Try different key formats that users might use
                for key in ['https', 'https://', 'http', 'http://']:
                    if key in proxies:
                        proxy_url = proxies[key]
                        break
                
                if proxy_url:
                    # Use single proxy for all protocols (most common use case)
                    kwargs['proxy'] = proxy_url
        
        self._client_kwargs = {
            'timeout': timeout,
            'headers': headers,
            **kwargs
        }
        self._client: Optional[httpx.AsyncClient] = None
    
    async def __aenter__(self):
        self._client = httpx.AsyncClient(**self._client_kwargs)
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self._client:
            await self._client.aclose()
    
    async def request(self, method: str, url: str, **kwargs) -> Response:
        """Send HTTP request"""
        if not self._client:
            raise RuntimeError("Session not initialized. Use 'async with' statement.")
        
        # Handle requests -> httpx parameter mapping
        if 'allow_redirects' in kwargs:
            kwargs['follow_redirects'] = kwargs.pop('allow_redirects')
        
        return await self._client.request(method, url, **kwargs)
    
    async def get(self, url: str, **kwargs) -> Response:
        """Send GET request"""
        return await self.request('GET', url, **kwargs)
    
    async def post(self, url: str, **kwargs) -> Response:
        """Send POST request"""
        return await self.request('POST', url, **kwargs)
    
    async def put(self, url: str, **kwargs) -> Response:
        """Send PUT request"""
        return await self.request('PUT', url, **kwargs)
    
    async def delete(self, url: str, **kwargs) -> Response:
        """Send DELETE request"""
        return await self.request('DELETE', url, **kwargs)
    
    async def patch(self, url: str, **kwargs) -> Response:
        """Send PATCH request"""
        return await self.request('PATCH', url, **kwargs)
    
    async def head(self, url: str, **kwargs) -> Response:
        """Send HEAD request"""
        return await self.request('HEAD', url, **kwargs)
    
    async def options(self, url: str, **kwargs) -> Response:
        """Send OPTIONS request"""
        return await self.request('OPTIONS', url, **kwargs)


# Global convenience functions
async def request(method: str, url: str, **kwargs) -> Response:
    """
    Send HTTP request using temporary session
    
    Example:
        response = await requests_async.request('GET', 'https://httpbin.org/get')
    """
    # Extract session parameters
    session_params = {}
    request_params = {}
    
    # Session parameters that should go to AsyncSession
    session_param_names = {'timeout', 'headers', 'proxies', 'proxy', 'verify', 'cert', 'trust_env'}
    
    for key, value in kwargs.items():
        if key in session_param_names:
            session_params[key] = value
        else:
            request_params[key] = value
    
    # Handle requests -> httpx parameter mapping for request parameters
    if 'allow_redirects' in request_params:
        request_params['follow_redirects'] = request_params.pop('allow_redirects')
    
    async with AsyncSession(**session_params) as session:
        return await session.request(method, url, **request_params)


async def get(url: str, **kwargs) -> Response:
    """
    Send GET request
    
    Example:
        response = await requests_async.get('https://httpbin.org/get')
        data = response.json()
    """
    return await request('GET', url, **kwargs)


async def post(url: str, **kwargs) -> Response:
    """
    Send POST request
    
    Example:
        response = await requests_async.post('https://httpbin.org/post', 
                                           json={'key': 'value'})
    """
    return await request('POST', url, **kwargs)


async def put(url: str, **kwargs) -> Response:
    """Send PUT request"""
    return await request('PUT', url, **kwargs)


async def delete(url: str, **kwargs) -> Response:
    """Send DELETE request"""
    return await request('DELETE', url, **kwargs)


async def patch(url: str, **kwargs) -> Response:
    """Send PATCH request"""
    return await request('PATCH', url, **kwargs)


async def head(url: str, **kwargs) -> Response:
    """Send HEAD request"""
    return await request('HEAD', url, **kwargs)


async def options(url: str, **kwargs) -> Response:
    """Send OPTIONS request"""
    return await request('OPTIONS', url, **kwargs)