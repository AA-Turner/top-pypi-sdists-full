"""HTTP utilities for CodeMie SDK."""

from typing import (
    TypeVar,
    Type,
    Any,
    Callable,
    get_origin,
    get_args,
)
import requests
import logging
from functools import wraps

T = TypeVar("T")

TokenSource = str | Callable[[], str]

logger = logging.getLogger(__name__)


def log_request(func):
    """Decorator to log request details"""

    @wraps(func)
    def wrapper(self, *args, **kwargs):
        http_method = func.__name__.upper()
        endpoint = kwargs.get("endpoint", args[0] if args else None)
        logger.debug(f"Making {http_method} request to {self._base_url}{endpoint}")

        try:
            result = func(self, *args, **kwargs)
            logger.info(f"Successfully processed {http_method} request to {endpoint}")
            return result
        except Exception as e:
            logger.error(f"Error during {http_method} request to {endpoint}: {str(e)}")
            raise

    return wrapper


class ApiRequestHandler:
    """Handles HTTP requests with consistent error handling and response parsing."""

    def __init__(
        self,
        base_url: str,
        token: str | Callable[[], str],
        verify_ssl: bool = True,
    ):
        """Initialize the API request handler.

        Args:
            base_url: Base URL for the API
            token: Authentication token string or callable that returns one
            verify_ssl: Whether to verify SSL certificates
        """
        self._base_url = base_url.rstrip("/")
        self._token = token
        self._verify_ssl = verify_ssl
        self._is_localhost = self._is_localhost_domain(base_url)

    @staticmethod
    def _is_localhost_domain(domain: str) -> bool:
        """Check if the domain is a localhost variant."""
        domain_lower = domain.lower()
        localhost_patterns = [
            "localhost",
            "127.0.0.1",
            "0.0.0.0",
            "192.168",
        ]
        return any(pattern in domain_lower for pattern in localhost_patterns)

    def _get_headers(
        self, exclude_content_type: bool = False, include_auth: bool = True
    ) -> dict:
        """Gets request headers with auth token.

        Args:
            exclude_content_type: Whether to exclude Content-Type header (for multipart requests)
            include_auth: Whether to include the Authorization header
        """
        headers = {}
        if not exclude_content_type:
            headers["Content-Type"] = "application/json"

        if include_auth:
            if self._is_localhost and not self._token:
                headers["Authorization"] = "dev-codemie-user"
            else:
                token_value = self._token() if callable(self._token) else self._token
                headers["Authorization"] = f"Bearer {token_value}"
        return headers

    def _parse_response(
        self,
        response: requests.Response,
        response_model: Type[T],
        wrap_response: bool = True,
    ) -> T:
        """Parse response data into model, handling both single models and lists.

        Args:
            response: Response from requests
            response_model: Type to parse into (can be a single model or list[model])
            wrap_response: Whether response is wrapped in 'data' field

        Returns:
            Parsed response object or list of objects
        """
        try:
            # Handle empty responses (e.g., 204 No Content for DELETE operations)
            if not response.content or response.status_code == 204:
                logger.debug(f"Empty response with status {response.status_code}")
                if response_model is dict:
                    return {}
                return None

            response_data = response.json()
            logger.debug(f"Received response with status {response.status_code}")
            logger.debug(f"Response datasource_type: {type(response_data)}")

            # Handle data wrapper for dict responses only
            if wrap_response and isinstance(response_data, dict):
                response_data = response_data.get("data", response_data)

            # If response_model is dict, return raw data
            if response_model is dict:
                return response_data

            # Handle List types
            origin = get_origin(response_model)
            if origin is list:
                # Get the model class from list[Model]
                model_class = get_args(response_model)[0]
                if not isinstance(response_data, list):
                    response_data = [response_data]

                # If list[dict], return raw data without validation
                if model_class is dict:
                    return response_data

                return [model_class.model_validate(item) for item in response_data]
            else:
                # Handle single model
                return response_model.model_validate(response_data)

        except ValueError as e:
            logger.error(f"Failed to parse response: {str(e)}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error parsing response: {str(e)}")
            raise

    @log_request
    def get(
        self,
        endpoint: str,
        response_model: Type[T],
        params: dict[str, Any] | None = None,
        wrap_response: bool = True,
    ) -> T:
        """Makes a GET request and parses the response.

        Args:
            endpoint: API endpoint path
            response_model: Pydantic model class or list[Model] for response
            params: Query parameters
            wrap_response: Whether response is wrapped in 'data' field

        Returns:
            Parsed response object or list of objects, or raw Response if response_model is requests.Response
        """
        if params:
            logger.debug(f"Request params: {params}")
        response = requests.get(
            url=f"{self._base_url}{endpoint}",
            headers=self._get_headers(),
            params=params,
            verify=self._verify_ssl,
        )
        response.raise_for_status()

        if response_model is None or response_model is requests.Response:
            return response

        return self._parse_response(response, response_model, wrap_response)

    @log_request
    def post(
        self,
        endpoint: str,
        response_model: Type[T],
        json_data: dict[str, Any] | None = None,
        params: dict[str, Any] | None = None,
        stream: bool = False,
        wrap_response: bool = True,
        raise_on_error: bool = True,
        extra_headers: dict[str, str] | None = None,
        include_auth: bool = True,
    ) -> T:
        """Makes a POST request and parses the response.

        Args:
            endpoint: API endpoint path
            response_model: Pydantic model class or list[Model] for response
            json_data: JSON request body
            params: Query parameters
            stream: Whether to return streaming response
            wrap_response: Whether response is wrapped in 'data' field
            raise_on_error: Whether to raise exception on HTTP error status codes
            extra_headers: Optional additional HTTP headers to include (e.g., X-* for MCP propagation)
            include_auth: Whether to include the Authorization header
        """
        if json_data:
            logger.debug(f"Request body: {json_data}")

        headers = self._get_headers(include_auth=include_auth)
        if extra_headers:
            headers.update(extra_headers)

        response = requests.post(
            url=f"{self._base_url}{endpoint}",
            headers=headers,
            json=json_data,
            params=params,
            verify=self._verify_ssl,
            stream=stream,
        )
        if raise_on_error:
            response.raise_for_status()

        if stream:
            return response

        if response_model is None or response_model is requests.Response:
            return response

        return self._parse_response(response, response_model, wrap_response)

    @log_request
    def post_multipart(
        self,
        endpoint: str,
        response_model: Type[T],
        params: dict[str, Any] | None = None,
        data: dict[str, Any] | None = None,
        files: list | None = None,
        wrap_response: bool = True,
    ) -> T:
        """Makes a POST multipart/form-data request and parses the response.

        Args:
            endpoint: API endpoint path
            response_model: Pydantic model class or list[Model] for response
            params: Url parameters
            data: Data to be sent as multipart/form-data
            files: List of file tuples for upload
            wrap_response: Whether response is wrapped in 'data' field

        Returns:
            Parsed response object or list of objects
        """

        response = requests.post(
            url=f"{self._base_url}{endpoint}",
            headers=self._get_headers(
                exclude_content_type=True
            ),  # Let requests set multipart content-type
            params=params,
            data=data,
            files=files,
            verify=self._verify_ssl,
        )
        response.raise_for_status()

        return self._parse_response(response, response_model, wrap_response)

    @log_request
    def put_multipart(
        self,
        endpoint: str,
        response_model: Type[T],
        params: dict[str, Any] | None = None,
        files: list | None = None,
        wrap_response: bool = True,
    ) -> T:
        """Makes a PUT multipart/form-data request and parses the response.

        Args:
            endpoint: API endpoint path
            response_model: Pydantic model class or list[Model] for response
            params: Url parameters
            files: List of file tuples for upload
            wrap_response: Whether response is wrapped in 'data' field

        Returns:
            Parsed response object or list of objects
        """
        response = requests.put(
            url=f"{self._base_url}{endpoint}",
            headers=self._get_headers(
                exclude_content_type=True
            ),  # Let requests set multipart content-type
            params=params,
            files=files,
            verify=self._verify_ssl,
        )
        response.raise_for_status()

        return self._parse_response(response, response_model, wrap_response)

    @log_request
    def put(
        self,
        endpoint: str,
        response_model: Type[T],
        json_data: dict[str, Any],
        params: dict[str, Any] | None = None,
        wrap_response: bool = True,
        extra_headers: dict[str, str] | None = None,
    ) -> T:
        """Makes a PUT request and parses the response.

        Args:
            endpoint: API endpoint path
            response_model: Pydantic model class or list[Model] for response
            json_data: JSON request body
            params: Query parameters
            wrap_response: Whether response is wrapped in 'data' field
            extra_headers: Optional additional HTTP headers to include (e.g., X-* for MCP propagation)

        Returns:
            Parsed response object or list of objects
        """
        logger.debug(f"Request body: {json_data}")
        headers = self._get_headers()
        if extra_headers:
            headers.update(extra_headers)
        response = requests.put(
            url=f"{self._base_url}{endpoint}",
            headers=headers,
            json=json_data,
            params=params,
            verify=self._verify_ssl,
        )
        response.raise_for_status()
        return self._parse_response(response, response_model, wrap_response)

    @log_request
    def patch(
        self,
        endpoint: str,
        response_model: Type[T],
        json_data: dict[str, Any],
        params: dict[str, Any] | None = None,
        wrap_response: bool = True,
    ) -> T:
        """Makes a PATCH request and parses the response.

        Args:
            endpoint: API endpoint path
            response_model: Pydantic model class or list[Model] for response
            json_data: JSON request body
            params: Optional query parameters (e.g., filters, pagination)
            wrap_response: Whether response is wrapped in 'data' field

        Returns:
            Parsed response object or list of objects
        """
        logger.debug(f"Request body: {json_data}")
        response = requests.patch(
            url=f"{self._base_url}{endpoint}",
            headers=self._get_headers(),
            json=json_data,
            params=params,
            verify=self._verify_ssl,
        )
        response.raise_for_status()
        return self._parse_response(response, response_model, wrap_response)

    @log_request
    def delete(
        self,
        endpoint: str,
        response_model: Type[T],
        params: dict[str, Any] | None = None,
        json_data: dict[str, Any] | None = None,
        wrap_response: bool = True,
    ) -> T:
        """Makes a DELETE request and parses the response.

        Args:
            endpoint: API endpoint path
            response_model: Pydantic model class or list[Model] for response
            params: Query parameters (for passing multiple user_id params for bulk delete)
            json_data: JSON request body (some endpoints, e.g. /v1/feedback, require
                a body on DELETE rather than query params)
            wrap_response: Whether response is wrapped in 'data' field

        Returns:
            Parsed response object or list of objects
        """
        response = requests.delete(
            url=f"{self._base_url}{endpoint}",
            headers=self._get_headers(),
            params=params,
            json=json_data,
            verify=self._verify_ssl,
        )
        response.raise_for_status()

        return self._parse_response(response, response_model, wrap_response)
