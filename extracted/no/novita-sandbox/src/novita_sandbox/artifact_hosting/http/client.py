"""HTTP client wrapper with retry logic for Artifact Hosting SDK V2."""

import logging
import time
from typing import Any, Callable, Dict, Iterator, Optional, TypeVar

import httpx

from novita_sandbox.artifact_hosting.exceptions import (
    CancellationError,
    DeploymentError,
    DeploymentNotFoundError,
    ProjectNotFoundError,
    QuotaExceededError,
    RollbackError,
)

logger = logging.getLogger("novita_sandbox.artifact_hosting.http")

T = TypeVar("T")


class HTTPClient:
    """HTTP client wrapper with retry logic and error handling.
    
    Provides a unified interface for making HTTP requests to the
    Artifact Hosting API with:
    - Automatic retry with exponential backoff for transient errors
    - Error response mapping to SDK exceptions
    - Request/response logging
    - SSE stream support for log streaming
    
    Args:
        base_url: Base URL for API requests.
        api_key: API key for authentication.
        timeout: Request timeout in seconds (default: 30.0).
        max_retries: Maximum retry attempts for transient errors (default: 3).
    """
    
    def __init__(
        self,
        base_url: str,
        api_key: str,
        timeout: float = 30.0,
        max_retries: int = 3,
    ):
        self.base_url = base_url.rstrip("/")
        self.api_key = api_key
        self.timeout = timeout
        self.max_retries = max_retries
        self._client: Optional[httpx.Client] = None
    
    @property
    def client(self) -> httpx.Client:
        """Get or create HTTP client (lazy initialization)."""
        if self._client is None:
            self._client = httpx.Client(
                base_url=self.base_url,
                timeout=self.timeout,
                headers={
                    "X-API-Key": self.api_key,
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json",
                },
                event_hooks={
                    "request": [self._log_request],
                    "response": [self._log_response],
                },
            )
            logger.debug(f"HTTP client initialized: base_url={self.base_url}")
        return self._client
    
    def _log_request(self, request: httpx.Request) -> None:
        """Log HTTP request details."""
        logger.debug(f"HTTP Request: {request.method} {request.url}")
        if request.content and len(request.content) < 2000:
            try:
                body = request.content.decode("utf-8")
                logger.debug(f"  Request body: {body}")
            except Exception:
                logger.debug(f"  Request body: <binary, {len(request.content)} bytes>")
    
    def _log_response(self, response: httpx.Response) -> None:
        """Log HTTP response details."""
        response.read()
        logger.debug(
            f"HTTP Response: {response.status_code} {response.reason_phrase} "
            f"({response.elapsed.total_seconds():.2f}s)"
        )
        if response.headers.get("content-type", "").startswith("application/json"):
            try:
                if len(response.content) < 2000:
                    logger.debug(f"  Response body: {response.text}")
            except Exception:
                pass
    
    def _retry_with_backoff(
        self,
        func: Callable[[], T],
        initial_delay: float = 1.0,
        max_delay: float = 10.0,
    ) -> T:
        """Execute a function with exponential backoff retry logic.
        
        Only retries on transient network errors:
        - httpx.ConnectTimeout
        - httpx.ReadTimeout
        - httpx.NetworkError
        
        Args:
            func: Function to execute.
            initial_delay: Initial delay before first retry.
            max_delay: Maximum delay between retries.
        
        Returns:
            Result of the function call.
        
        Raises:
            Exception: Any exception raised by the function after all retries.
        """
        delay = initial_delay
        last_exception: Optional[Exception] = None
        
        for attempt in range(self.max_retries + 1):
            try:
                return func()
            except (httpx.ConnectTimeout, httpx.ReadTimeout, httpx.NetworkError) as e:
                last_exception = e
                
                if attempt >= self.max_retries:
                    raise
                
                logger.warning(
                    f"Request failed (attempt {attempt + 1}/{self.max_retries + 1}): {e}. "
                    f"Retrying in {min(delay, max_delay):.1f}s..."
                )
                time.sleep(min(delay, max_delay))
                delay *= 2
            except Exception:
                raise
        
        if last_exception:
            raise last_exception
        
        raise RuntimeError("Retry logic failed unexpectedly")
    
    def _check_response(self, response: httpx.Response, context: str = "") -> None:
        """Check HTTP response and raise appropriate exceptions.
        
        Args:
            response: httpx Response object.
            context: Optional context string for error messages.
        
        Raises:
            ProjectNotFoundError: If project not found (404).
            DeploymentNotFoundError: If deployment not found (404).
            QuotaExceededError: If quota exceeded (429).
            CancellationError: If cancellation failed.
            RollbackError: If rollback failed.
            DeploymentError: For other errors.
        """
        if response.is_success:
            return
        
        # Parse error response
        try:
            error_data = response.json()
            error_code = error_data.get("error", {}).get("code", "")
            error_message = error_data.get("error", {}).get("message", response.text)
        except Exception:
            error_code = ""
            error_message = response.text
        
        # Add context to message
        if context:
            error_message = f"{context}: {error_message}"
        
        # Map status codes to exceptions
        if response.status_code == 404:
            if "project" in error_message.lower():
                raise ProjectNotFoundError(error_message, code=error_code)
            elif "deployment" in error_message.lower():
                raise DeploymentNotFoundError(error_message, code=error_code)
            else:
                raise DeploymentError(error_message, code=error_code)
        elif response.status_code == 409:
            # Conflict - could be cancellation or rollback failure
            if "cancel" in context.lower():
                raise CancellationError(error_message, code=error_code)
            elif "rollback" in context.lower():
                raise RollbackError(error_message, code=error_code)
            else:
                raise DeploymentError(error_message, code=error_code)
        elif response.status_code == 429:
            raise QuotaExceededError(error_message, code=error_code)
        else:
            raise DeploymentError(error_message, code=error_code)
    
    def get(
        self,
        path: str,
        params: Optional[Dict[str, Any]] = None,
        context: str = "",
    ) -> Dict[str, Any]:
        """Make a GET request.
        
        Args:
            path: URL path (relative to base_url).
            params: Query parameters.
            context: Context string for error messages.
        
        Returns:
            Parsed JSON response.
        """
        def _request() -> httpx.Response:
            return self.client.get(path, params=params)
        
        response = self._retry_with_backoff(_request)
        self._check_response(response, context)
        result: Dict[str, Any] = response.json()
        return result
    
    def post(
        self,
        path: str,
        json: Optional[Dict[str, Any]] = None,
        context: str = "",
    ) -> Dict[str, Any]:
        """Make a POST request.
        
        Args:
            path: URL path (relative to base_url).
            json: JSON body.
            context: Context string for error messages.
        
        Returns:
            Parsed JSON response.
        """
        def _request() -> httpx.Response:
            return self.client.post(path, json=json)
        
        response = self._retry_with_backoff(_request)
        self._check_response(response, context)
        result: Dict[str, Any] = response.json()
        return result
    
    def put(
        self,
        path: str,
        json: Optional[Dict[str, Any]] = None,
        context: str = "",
    ) -> Dict[str, Any]:
        """Make a PUT request.
        
        Args:
            path: URL path (relative to base_url).
            json: JSON body.
            context: Context string for error messages.
        
        Returns:
            Parsed JSON response.
        """
        def _request() -> httpx.Response:
            return self.client.put(path, json=json)
        
        response = self._retry_with_backoff(_request)
        self._check_response(response, context)
        result: Dict[str, Any] = response.json()
        return result
    
    def patch(
        self,
        path: str,
        json: Optional[Dict[str, Any]] = None,
        context: str = "",
    ) -> Dict[str, Any]:
        """Make a PATCH request.
        
        Args:
            path: URL path (relative to base_url).
            json: JSON body.
            context: Context string for error messages.
        
        Returns:
            Parsed JSON response.
        """
        def _request() -> httpx.Response:
            return self.client.patch(path, json=json)
        
        response = self._retry_with_backoff(_request)
        self._check_response(response, context)
        result: Dict[str, Any] = response.json()
        return result
    
    def delete(
        self,
        path: str,
        params: Optional[Dict[str, Any]] = None,
        context: str = "",
    ) -> Optional[Dict[str, Any]]:
        """Make a DELETE request.
        
        Args:
            path: URL path (relative to base_url).
            params: Query parameters.
            context: Context string for error messages.
        
        Returns:
            Parsed JSON response or None if no content.
        """
        def _request() -> httpx.Response:
            return self.client.delete(path, params=params)
        
        response = self._retry_with_backoff(_request)
        self._check_response(response, context)
        
        if response.status_code == 204 or not response.content:
            return None
        result: Dict[str, Any] = response.json()
        return result
    
    def stream_sse(
        self,
        path: str,
        params: Optional[Dict[str, Any]] = None,
    ) -> Iterator[str]:
        """Stream Server-Sent Events from an endpoint.
        
        Args:
            path: URL path (relative to base_url).
            params: Query parameters.
        
        Yields:
            SSE event data strings.
        """
        for _, data in self.stream_sse_events(path, params=params):
            if data:
                yield data
    
    def stream_sse_events(
        self,
        path: str,
        params: Optional[Dict[str, Any]] = None,
    ) -> Iterator[tuple[str, str]]:
        """Stream Server-Sent Events from an endpoint with event types.
        
        Args:
            path: URL path (relative to base_url).
            params: Query parameters.
        
        Yields:
            Tuple of (event_type, data) for each SSE event.
            event_type defaults to "message" if not specified.
        """
        with self.client.stream("GET", path, params=params) as response:
            self._check_response(response)
            
            buffer = ""
            for chunk in response.iter_text():
                buffer += chunk
                while "\n\n" in buffer:
                    event_block, buffer = buffer.split("\n\n", 1)
                    # Parse SSE event
                    event_type = "message"
                    data = ""
                    for line in event_block.split("\n"):
                        if line.startswith("event: "):
                            event_type = line[7:].strip()
                        elif line.startswith("data: "):
                            if data:
                                data += "\n" + line[6:]
                            else:
                                data = line[6:]
                        elif line.startswith(":"):
                            # Comment line, skip
                            continue
                    yield event_type, data
    
    def close(self) -> None:
        """Close the HTTP client and release resources."""
        if self._client is not None:
            self._client.close()
            self._client = None
    
    def __enter__(self) -> "HTTPClient":
        """Context manager entry."""
        return self
    
    def __exit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        """Context manager exit."""
        self.close()
