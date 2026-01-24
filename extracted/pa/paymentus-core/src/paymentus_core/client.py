"""
Core HTTP client for Paymentus API
"""
import json
from typing import Any, Dict, Optional, Union

import requests
from pydantic import BaseModel, Field

from .exceptions import APIError, NetworkError, RateLimitError, ServerError


class ClientConfig(BaseModel):
    """Configuration for HTTP client"""
    base_url: str
    timeout: int = 30
    headers: Dict[str, str] = Field(default_factory=dict)
    verify_ssl: bool = True
    max_retries: int = 3
    retry_status_codes: list = Field(default_factory=lambda: [429, 500, 502, 503, 504])


class Response:
    """API response wrapper"""
    def __init__(
        self,
        status_code: int,
        headers: Dict[str, str],
        body: Any,
        request_id: Optional[str] = None
    ):
        self.status_code = status_code
        self.headers = headers
        self.body = body
        self.request_id = request_id or headers.get("X-Request-Id")
        
    @property
    def is_success(self) -> bool:
        """Check if response indicates success"""
        return 200 <= self.status_code < 300

    @property
    def is_redirect(self) -> bool:
        """Check if response is a redirect"""
        return 300 <= self.status_code < 400
        
    @property
    def is_client_error(self) -> bool:
        """Check if response indicates client error"""
        return 400 <= self.status_code < 500
        
    @property
    def is_server_error(self) -> bool:
        """Check if response indicates server error"""
        return self.status_code >= 500


class Client:
    """HTTP client for Paymentus API"""
    def __init__(self, config: ClientConfig):
        """Initialize with client configuration"""
        self.config = config
        self.session = self._setup_session()
        
    def _setup_session(self) -> requests.Session:
        """Setup requests session with retries and default headers"""
        session = requests.Session()
        
        # Setup retry adapter if max_retries > 0
        if self.config.max_retries > 0:
            retry_adapter = requests.adapters.HTTPAdapter(
                max_retries=requests.adapters.Retry(
                    total=self.config.max_retries,
                    backoff_factor=0.3,
                    status_forcelist=self.config.retry_status_codes,
                    allowed_methods=["GET", "POST", "PUT", "DELETE", "HEAD", "OPTIONS"]
                )
            )
            session.mount("http://", retry_adapter)
            session.mount("https://", retry_adapter)
        
        # Set default headers
        for key, value in self.config.headers.items():
            session.headers[key] = value
            
        # Always send JSON
        session.headers["Content-Type"] = "application/json"
        session.headers["Accept"] = "application/json"
        
        return session

    def get(
        self,
        path: str,
        params: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None
    ) -> Response:
        """Send HTTP GET request"""
        return self._request("GET", path, params=params, headers=headers)

    def post(
        self,
        path: str,
        data: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None
    ) -> Response:
        """Send HTTP POST request"""
        return self._request("POST", path, data=data, headers=headers)

    def put(
        self,
        path: str,
        data: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None
    ) -> Response:
        """Send HTTP PUT request"""
        return self._request("PUT", path, data=data, headers=headers)

    def delete(
        self,
        path: str,
        data: Optional[Dict[str, Any]] = None, 
        headers: Optional[Dict[str, str]] = None
    ) -> Response:
        """Send HTTP DELETE request"""
        return self._request("DELETE", path, data=data, headers=headers)

    def _request(
        self,
        method: str,
        path: str,
        params: Optional[Dict[str, Any]] = None,
        data: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None
    ) -> Response:
        """Make a HTTP request and handle response/errors"""
        full_url = f"{self.config.base_url.rstrip('/')}/{path.lstrip('/')}"
        request_headers = headers or {}
        
        try:
            response = self.session.request(
                method=method,
                url=full_url,
                params=params,
                json=data,
                headers=request_headers,
                timeout=self.config.timeout,
                verify=self.config.verify_ssl
            )
            
            # Parse response body
            body = None
            if response.content:
                try:
                    body = response.json()
                except json.JSONDecodeError:
                    body = response.content.decode("utf-8")
                    
            response_obj = Response(
                status_code=response.status_code,
                headers=dict(response.headers),
                body=body,
                request_id=response.headers.get("X-Request-Id")
            )
            
            # Check for API errors
            self._check_for_errors(response_obj)
            
            return response_obj
            
        except requests.exceptions.RequestException as e:
            # Handle network errors
            raise NetworkError(
                message=f"Network error: {str(e)}",
                details={"original_exception": str(e)}
            ) from e

    def _check_for_errors(self, response: Response) -> None:
        """Check response for errors and raise appropriate exceptions"""
        if response.is_success:
            return
            
        message = "Unknown error"
        code = None
        details = {}
        
        # Try to extract error details from response body
        if isinstance(response.body, dict):
            message = response.body.get("message", message)
            code = response.body.get("code", code)
            details = response.body.get("details", details)
        
        # Include request ID if available
        if response.request_id:
            details["request_id"] = response.request_id
            
        # Raise appropriate exception based on status code
        if response.status_code == 429:
            raise RateLimitError(
                message=message or "Rate limit exceeded",
                code=code,
                details=details
            )
        elif response.status_code >= 500:
            raise ServerError(
                message=message or "Internal server error",
                code=code,
                details=details
            )
        else:
            raise APIError(
                message=message or "API error",
                code=code,
                details=details
            ) 