"""Auto-generated stub for module: rpc."""
from typing import Any, Callable, Dict, Optional, Tuple

from .token_auth import AuthToken, RefreshToken
from .utils import log_errors

# Constants
logger: Any

# Classes
class RPC:
    # RPC class for handling backend API requests with token-based authentication.

    def __init__(self: Any, access_key: Optional[str] = None, secret_key: Optional[str] = None, project_id: Optional[str] = None, base_url: Optional[str] = None, max_workers: int = 5) -> None:
        """
        Initialize the RPC client with optional project ID and base URL.
        
                Args:
                    access_key: API access key (or set MATRICE_ACCESS_KEY_ID env var)
                    secret_key: API secret key (or set MATRICE_SECRET_ACCESS_KEY env var)
                    project_id: Optional project ID to include in requests
                    base_url: Optional custom base URL (or set MATRICE_BASE_URL env var)
                    max_workers: Maximum number of workers for background request queue (default: 5)
        """
        ...

    def add_project_id(self: Any, url: str) -> str:
        """
        Add project ID to the URL if present and not already included.
        """
        ...

    async def async_send_request(self: Any, method: str = '', path: str = '', headers: Optional[Any] = None, payload: Optional[Any] = None, files: Optional[Any] = None, data: Optional[Any] = None, timeout: int = 120, raise_exception: bool = True, base_url: Optional[str] = None, max_retries: int = 0, retry_delay: float = 1.0, exponential_backoff: bool = True, default_return_value: Optional[Dict[str, Any]] = None, **kwargs: Any) -> Dict[str, Any]:
        """
        Send an async HTTP request to the specified endpoint with retry support.
        
                Args:
                    method: HTTP method (GET, POST, PUT, DELETE, etc.)
                    path: API endpoint path (also accepts 'endpoint' as alias)
                    headers: Optional request headers
                    payload: Optional JSON payload
                    files: Optional files to upload
                    data: Optional raw data
                    timeout: Request timeout in seconds (default: 60)
                    raise_exception: Whether to raise exceptions on error (default: True)
                    base_url: Optional custom base URL
                    max_retries: Maximum number of retry attempts on failure (default: 0)
                    retry_delay: Initial delay between retries in seconds (default: 1.0)
                    exponential_backoff: Whether to use exponential backoff for retries (default: True)
                    default_return_value: Value to return on failure when raise_exception=False
        
                Returns:
                    Response data dict
        """
        ...

    def clear_completed_background_requests(self: Any) -> int:
        """
        Clear completed background requests from the queue.
        
                Returns:
                    Number of completed requests that were cleared
        """
        ...

    def delete(self: Any, path: str = '', payload: Optional[Any] = None, headers: Optional[Any] = None, timeout: int = 120, raise_exception: bool = True, base_url: Optional[str] = None, max_retries: int = 0, retry_delay: float = 1.0, exponential_backoff: bool = True, default_return_value: Optional[Any] = None, background: bool = False, on_complete: Optional[Callable[[Any], None]] = None, **kwargs: Any) -> Optional[Any]:
        """
        Send a DELETE request to the specified endpoint.
        """
        ...

    async def delete_async(self: Any, path: str = '', payload: Optional[Any] = None, headers: Optional[Any] = None, timeout: int = 120, raise_exception: bool = True, base_url: Optional[str] = None, max_retries: int = 0, retry_delay: float = 1.0, exponential_backoff: bool = True, default_return_value: Optional[Any] = None, **kwargs: Any) -> Any:
        """
        Send an async DELETE request to the specified endpoint.
        """
        ...

    def get(self: Any, path: str = '', params: Optional[Any] = None, timeout: int = 120, raise_exception: bool = True, base_url: Optional[str] = None, max_retries: int = 0, retry_delay: float = 1.0, exponential_backoff: bool = True, default_return_value: Optional[Any] = None, background: bool = False, on_complete: Optional[Callable[[Any], None]] = None, **kwargs: Any) -> Optional[Any]:
        """
        Send a GET request to the specified endpoint.
        """
        ...

    async def get_async(self: Any, path: str = '', params: Optional[Any] = None, timeout: int = 120, raise_exception: bool = True, base_url: Optional[str] = None, max_retries: int = 0, retry_delay: float = 1.0, exponential_backoff: bool = True, default_return_value: Optional[Any] = None, **kwargs: Any) -> Any:
        """
        Send an async GET request to the specified endpoint.
        """
        ...

    def get_background_request_count(self: Any) -> Tuple[int, int]:
        """
        Get the count of pending and completed background requests.
        
                Returns:
                    Tuple of (pending_count, completed_count)
        """
        ...

    def post(self: Any, path: str = '', payload: Optional[Any] = None, headers: Optional[Any] = None, files: Optional[Any] = None, data: Optional[Any] = None, timeout: int = 120, raise_exception: bool = True, base_url: Optional[str] = None, max_retries: int = 0, retry_delay: float = 1.0, exponential_backoff: bool = True, default_return_value: Optional[Any] = None, background: bool = False, on_complete: Optional[Callable[[Any], None]] = None, **kwargs: Any) -> Optional[Any]:
        """
        Send a POST request to the specified endpoint.
        """
        ...

    async def post_async(self: Any, path: str = '', payload: Optional[Any] = None, headers: Optional[Any] = None, files: Optional[Any] = None, data: Optional[Any] = None, timeout: int = 120, raise_exception: bool = True, base_url: Optional[str] = None, max_retries: int = 0, retry_delay: float = 1.0, exponential_backoff: bool = True, default_return_value: Optional[Any] = None, **kwargs: Any) -> Any:
        """
        Send an async POST request to the specified endpoint.
        """
        ...

    def put(self: Any, path: str = '', payload: Optional[Any] = None, headers: Optional[Any] = None, timeout: int = 120, raise_exception: bool = True, base_url: Optional[str] = None, max_retries: int = 0, retry_delay: float = 1.0, exponential_backoff: bool = True, default_return_value: Optional[Any] = None, background: bool = False, on_complete: Optional[Callable[[Any], None]] = None, **kwargs: Any) -> Optional[Any]:
        """
        Send a PUT request to the specified endpoint.
        """
        ...

    async def put_async(self: Any, path: str = '', payload: Optional[Any] = None, headers: Optional[Any] = None, timeout: int = 120, raise_exception: bool = True, base_url: Optional[str] = None, max_retries: int = 0, retry_delay: float = 1.0, exponential_backoff: bool = True, default_return_value: Optional[Any] = None, **kwargs: Any) -> Any:
        """
        Send an async PUT request to the specified endpoint.
        """
        ...

    def refresh_token(self: Any) -> None:
        """
        Refresh authentication token with automatic fallback to full re-auth.
        
                Uses a cascading approach:
                1. Check if AuthToken is expired/expiring soon (5 min buffer)
                2. Try normal AuthToken refresh via RefreshToken
                3. If that fails, fall back to complete re-authentication from credentials
        
                Thread-safe: Uses _token_lock to prevent concurrent refresh attempts.
                Never raises exceptions - logs errors and attempts recovery silently.
        """
        ...

    def send_request(self: Any, method: str = '', path: str = '', headers: Optional[Dict[str, str]] = None, payload: Optional[Dict[str, Any]] = None, files: Optional[Dict[str, Any]] = None, data: Optional[Any] = None, timeout: int = 120, raise_exception: bool = True, base_url: Optional[str] = None, max_retries: int = 0, retry_delay: float = 1.0, exponential_backoff: bool = True, default_return_value: Optional[Any] = None, background: bool = False, on_complete: Optional[Callable[[Dict[str, Any]], None]] = None, **kwargs: Any) -> Optional[Dict[str, Any]]:
        """
        Send an HTTP request to the specified endpoint with retry and background execution support.
        
                Args:
                    method: HTTP method (GET, POST, PUT, DELETE, etc.)
                    path: API endpoint path (also accepts 'endpoint' as alias)
                    headers: Optional request headers
                    payload: Optional JSON payload
                    files: Optional files to upload
                    data: Optional raw data
                    timeout: Request timeout in seconds (default: 60)
                    raise_exception: Whether to raise exceptions on error (default: True)
                    base_url: Optional custom base URL
                    max_retries: Maximum number of retry attempts on failure (default: 0)
                    retry_delay: Initial delay between retries in seconds (default: 1.0)
                    exponential_backoff: Whether to use exponential backoff for retries (default: True)
                    default_return_value: Value to return on failure when raise_exception=False
                    background: Execute request in background without blocking (default: False)
                    on_complete: Optional callback function to call with the result when background=True
        
                Returns:
                    Response data dict, or None if background=True
        """
        ...

    def shutdown(self: Any, wait: bool = True, timeout: Optional[float] = None) -> None:
        """
        Shutdown the RPC client and cleanup resources.
        
                Args:
                    wait: Whether to wait for all background requests to complete before shutdown
                    timeout: Optional timeout in seconds when waiting for requests (only used if wait=True)
        """
        ...

    def wait_for_background_requests(self: Any, timeout: Optional[float] = None) -> int:
        """
        Wait for all background requests to complete.
        
                Args:
                    timeout: Optional timeout in seconds to wait for all requests to complete.
                            If None, waits indefinitely.
        
                Returns:
                    Number of requests that completed successfully
        """
        ...

