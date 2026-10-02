"""
requests-async: Simple async HTTP client with requests-like interface
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Basic usage:
    import requests_async
    
    response = await requests_async.get('https://httpbin.org/get')
    print(response.json())

:copyright: (c) 2024 by requests-async contributors.
:license: MIT, see LICENSE for more details.
"""

__version__ = "0.2.4"
__author__ = "requests-async contributors"

from .client import (
    AsyncSession,
    get, post, put, delete, patch, head, options, request
)

# Expose httpx types for convenience
from httpx import Response, HTTPError, RequestError, TimeoutException

__all__ = [
    'AsyncSession',
    'get', 'post', 'put', 'delete', 'patch', 'head', 'options', 'request',
    'Response', 'HTTPError', 'RequestError', 'TimeoutException'
]