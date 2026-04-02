# clients/rest/client.py
import json as json_lib
import logging
from datetime import datetime
from enum import Enum
from typing import Any, Dict, Optional, Union
from urllib.parse import urljoin

import backoff
import requests

from seshat.general.exceptions import (
    RestClientException,
    BadRequestError,
    UnauthorizedError,
    ForbiddenError,
    NotFoundError,
    ServerError,
)


class HttpMethod(str, Enum):
    GET = "GET"
    POST = "POST"
    PUT = "PUT"
    DELETE = "DELETE"
    PATCH = "PATCH"


def _should_retry(exc: Exception) -> bool:
    """Determine if request should be retried based on exception"""
    # Retry on connection errors and 5xx responses
    if isinstance(exc, requests.ConnectionError):
        return True
    if isinstance(exc, ServerError):
        return True
    if isinstance(exc, requests.Timeout):
        return True
    return False


class RestClient:
    """Reusable REST client with error handling, retries and logging"""

    def __init__(
        self,
        base_url: str,
        timeout: int = 30,
        max_retries: int = 3,
        retry_delay: int = 1,
        headers: Optional[Dict[str, str]] = None,
        logger: Optional[logging.Logger] = None,
        verbose: bool = False,
    ):
        """
        Initialize REST client

        Args:
            base_url: Base URL for all requests
            timeout: Request timeout in seconds
            max_retries: Maximum number of retries for failed requests
            retry_delay: Delay between retries in seconds
            headers: Default headers to include in all requests
            logger: Custom logger instance
        """
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self.max_retries = max_retries
        self.retry_delay = retry_delay
        self.headers = headers or {}
        self.session = requests.Session()
        self.logger = logger or logging.getLogger(__name__)
        self.verbose = verbose

    def _build_url(self, endpoint: str) -> str:
        """Build full URL from endpoint"""
        return urljoin(f"{self.base_url}/", endpoint.lstrip("/"))

    def _log_request(
        self,
        method: str,
        url: str,
        params: Optional[Dict] = None,
        headers: Optional[Dict] = None,
        json: Optional[Dict] = None,
        data: Optional[Any] = None,
    ) -> str:
        """Log request details and return request ID"""
        request_id = datetime.now().strftime("%Y%m%d_%H%M%S_%f")

        # Create sanitized headers (remove sensitive info)
        safe_headers = headers.copy() if headers else {}
        if "Authorization" in safe_headers:
            safe_headers["Authorization"] = "REDACTED"

        request_data = {
            "request_id": request_id,
            "method": method,
            "url": url,
            "params": params,
            "headers": safe_headers,
        }

        if json:
            request_data["json"] = json
        if data:
            request_data["data"] = data if isinstance(data, str) else "<binary_data>"

        self.logger.info(
            f"REQUEST [{request_id}]: {method} {url}",
            extra={"request_data": request_data},
        )
        return request_id

    def _log_response(
        self,
        request_id: str,
        status_code: int,
        elapsed: float,
        headers: Dict,
        body: Any,
    ):
        """Log response details"""
        response_data = {
            "request_id": request_id,
            "status_code": status_code,
            "elapsed_ms": int(elapsed * 1000),
            "headers": dict(headers),
        }

        # Try to include response body in logs, with size limit
        try:
            if isinstance(body, (dict, list)):
                response_data["body"] = body
            elif isinstance(body, str):
                response_data["body"] = (
                    body[:1000] + "..." if len(body) > 1000 else body
                )
            else:
                response_data["body"] = "<binary_data>"
        except Exception as e:
            response_data["body"] = "<unserializable_data>"
            response_data["body_error"] = str(e)

        self.logger.info(
            f"RESPONSE [{request_id}]: {status_code} ({response_data['elapsed_ms']}ms)",
            extra={"response_data": response_data},
        )

    @staticmethod
    def _handle_error(status_code: int, message: str):
        """Map HTTP errors to exceptions"""
        error_map = {
            400: BadRequestError,
            401: UnauthorizedError,
            403: ForbiddenError,
            404: NotFoundError,
        }

        if status_code in error_map:
            raise error_map[status_code](message)
        elif status_code >= 500:
            raise ServerError(message)
        else:
            raise RestClientException(f"HTTP {status_code}: {message}")

    def _create_backoff_decorator(self):
        return backoff.on_exception(
            backoff.expo,
            (requests.RequestException, RestClientException),
            max_tries=self.max_retries,
            giveup=lambda e: not _should_retry(e),
            base=self.retry_delay,
        )

    def request(
        self,
        method: Union[str, HttpMethod],
        endpoint: str,
        params: Optional[Dict[str, Any]] = None,
        json: Optional[Dict[str, Any]] = None,
        data: Optional[Any] = None,
        headers: Optional[Dict[str, str]] = None,
        timeout: Optional[int] = None,
    ) -> Any:
        """
        Make HTTP request

        Args:
            method: HTTP method
            endpoint: API endpoint (will be joined with base_url)
            params: Query parameters
            json: JSON body
            data: Raw body data
            headers: Additional headers
            timeout: Request timeout override

        Returns:
            Response data (parsed from JSON)

        Raises:
            RestClientException: Base class for all client exceptions
            BadRequestError: 400 response
            UnauthorizedError: 401 response
            ForbiddenError: 403 response
            NotFoundError: 404 response
            ServerError: 5xx response
        """
        # Merge headers
        request_headers = self.headers.copy()
        if headers:
            request_headers.update(headers)

        url = self._build_url(endpoint)

        @self._create_backoff_decorator()
        def _execute_request():
            request_id = self._log_request(
                method=method if isinstance(method, str) else method.value,
                url=url,
                params=params,
                headers=request_headers,
                json=json,
                data=data,
            )

            try:
                response = self.session.request(
                    method=method if isinstance(method, str) else method.value,
                    url=url,
                    params=params,
                    json=json,
                    data=data,
                    headers=request_headers,
                    timeout=timeout or self.timeout,
                )

                try:
                    response_data = response.json()
                except (ValueError, json_lib.JSONDecodeError):
                    response_data = response.text

                self._log_response(
                    request_id=request_id,
                    status_code=response.status_code,
                    elapsed=response.elapsed.total_seconds(),
                    headers=dict(response.headers),
                    body=response_data,
                )

                if response.status_code >= 400:
                    error_message = (
                        response_data.get("error", {}).get("message", "Unknown error")
                        if isinstance(response_data, dict)
                        else str(response_data)
                    )
                    self._handle_error(response.status_code, error_message)

                return response_data

            except requests.RequestException as e:
                if self.verbose:
                    self.logger.error(
                        f"REQUEST FAILED [{request_id}]: {str(e)}",
                        extra={"error": str(e)},
                        exc_info=True,
                    )
                else:
                    self.logger.error(
                        f"REQUEST FAILED [{request_id}]: {str(e)}",
                    )
                raise RestClientException(f"Request failed: {str(e)}")

        return _execute_request()

    def get(self, endpoint: str, **kwargs) -> Any:
        return self.request(HttpMethod.GET, endpoint, **kwargs)

    def post(self, endpoint: str, **kwargs) -> Any:
        return self.request(HttpMethod.POST, endpoint, **kwargs)

    def put(self, endpoint: str, **kwargs) -> Any:
        return self.request(HttpMethod.PUT, endpoint, **kwargs)

    def delete(self, endpoint: str, **kwargs) -> Any:
        return self.request(HttpMethod.DELETE, endpoint, **kwargs)

    def patch(self, endpoint: str, **kwargs) -> Any:
        return self.request(HttpMethod.PATCH, endpoint, **kwargs)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.session.close()
