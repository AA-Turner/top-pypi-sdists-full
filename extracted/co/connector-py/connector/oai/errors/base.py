import json
import logging
from abc import ABC, abstractmethod
from collections.abc import Callable
from typing import Any, ClassVar

from connector_sdk_types.errors import (
    DEPRECATED_CODE_REDIRECTS,
    ConnectorErrorCode,
    ConnectorErrorMetadata,
    build_metadata,
)
from connector_sdk_types.generated import Error, ErrorCode, ErrorResponse
from httpx import ConnectError

logger = logging.getLogger("integration-connectors.sdk")
error_logger = logging.getLogger("integration-connectors.sdk.errors")

DNS_ERROR_TOKENS = ["name or service not known", "nodename nor servname provided"]
ILLEGAL_HEADER_MESSAGE = (
    "Illegal header constructed for API request. Please check the app configuration and try again."
)
FAILED_TO_CONNECT_MESSAGE = "Failed to connect to the API. Please verify the URL or try at a later time due to a potential temporary network issue."
FAILED_TO_PARSE_JSON_MESSAGE = "Failed to parse JSON response: {error_text}"
HTML_ERROR_MESSAGE = "Upstream HTML error response."
MAX_TEXT_ERROR_MESSAGE_LENGTH = 800
TRUNCATED_APPENDIX = "...(truncated)"


class ConnectorError(Exception):
    """
    Base exception class for Lumos connectors.
    Preferred way to raise exceptions inside the connectors.

    Subclasses carry a class-level DEFAULT_CODE and DEFAULT_MESSAGE so that
    callers can raise them without specifying the error code explicitly:

        raise RateLimitError(message="Slack throttled the request")
        raise NotFoundError()  # uses DEFAULT_MESSAGE

    All constructor arguments are optional; omitting them falls back to the
    class-level defaults.  The original keyword-only signature is preserved for
    backwards compatibility:

        raise ConnectorError(message="…", error_code=SDKErrorCode.NOT_FOUND)
        raise SomeError(metadata=ConnectorErrorMetadata(retryable=True))
    """

    DEFAULT_CODE: ClassVar[ConnectorErrorCode] = ConnectorErrorCode.INTERNAL_ERROR
    DEFAULT_MESSAGE: ClassVar[str] = "An unexpected error occurred"
    DEFAULT_HINT: ClassVar[str | None] = None

    def __init__(
        self,
        *,
        message: str | None = None,
        error_code: ErrorCode | ConnectorErrorCode | None = None,
        app_error_code: str | None = None,
        hint: str | None = None,
        retryable: bool | None = None,
        throttled: bool | None = None,
        refreshable: bool | None = None,
    ):
        # standard fields
        self.error_code: ErrorCode | ConnectorErrorCode = (
            error_code if error_code is not None else self.DEFAULT_CODE
        )
        self.app_error_code = app_error_code
        self.message = message if message is not None else self.DEFAULT_MESSAGE

        # metadata overrides
        self.hint = hint if hint is not None else self.DEFAULT_HINT
        self.retryable = retryable
        self.throttled = throttled
        self.refreshable = refreshable

        super().__init__(self.message)

    def __str__(self) -> str:
        return self.message

    def _resolve_code(self) -> ConnectorErrorCode:
        """Resolve to a ``ConnectorErrorCode``, redirecting deprecated ``ErrorCode`` values."""
        if isinstance(self.error_code, ConnectorErrorCode):
            return self.error_code
        redirected = DEPRECATED_CODE_REDIRECTS.get(self.error_code.value)
        return redirected if redirected is not None else ConnectorErrorCode.INTERNAL_ERROR

    def get_error_metadata(self) -> ConnectorErrorMetadata:
        """
        Return enrichment metadata derived from this exception.
        Can be overriden by supplying metadata overrides when raising the exception.
        """
        return build_metadata(
            self._resolve_code(),
            hint=self.hint,
            retryable=self.retryable,
            throttled=self.throttled,
            refreshable=self.refreshable,
        )


class ExceptionHandler(ABC):
    """
    Abstract class for handling exceptions. You can subclass this to create your own exception handler.
    """

    @staticmethod
    @abstractmethod
    def handle(
        e: Exception,
        original_func: Any,
        response: ErrorResponse,
        error_code: ErrorCode | ConnectorErrorCode | None = None,
    ) -> ErrorResponse:
        """
        Handle an exception. (ErrorHandler signature typing)

        e: Exception (An exception that was raised)
        original_func: FunctionType (The original method that was called, eg. validate_credentials)
        response: ErrorResp (The output of the connector call)
        error_code: str | None (The application-specific error code, eg. "my_app.internal_error")
        """
        return response


class DefaultHandler(ExceptionHandler):
    """
    Default exception handler that handles the basic HTTPX/GQL extraction (etc.) and chains onto the global handler.
    These are operations that are always done on the raised error.
    """

    @staticmethod
    def _extract_status_code(e: Exception) -> int | None:
        status_code: int | None = None
        if hasattr(e, "response") and hasattr(e.response, "status_code"):  # type: ignore
            status_code = e.response.status_code  # type: ignore
        if hasattr(e, "code"):
            status_code = e.code  # type: ignore
        if not isinstance(status_code, int):
            status_code = None
        return status_code

    @staticmethod
    def _message_from_json_response(response: Any, status_code: int | None) -> str | None:
        try:
            error_data = response.json()
        except Exception:
            return None

        if not error_data:
            return None
        if isinstance(error_data, dict | list) and len(error_data) == 0:
            return None

        url = getattr(response, "url", None)
        if url is not None:
            return f"[{status_code}][{str(url).split('?')[0]}] {error_data}"
        return f"[{status_code}] {error_data}"

    @staticmethod
    def _normalize_text_message(text: str) -> str:
        """Collaspe whitespace/newlines to keep logs compact"""
        return " ".join(text.split())

    @staticmethod
    def _omit_query_params(url: str) -> str:
        """Remove sensitive query params from the URL"""
        return url.split("?")[0]

    @staticmethod
    def _is_html_response(text: str, content_type: str | None) -> bool:
        """Check if a response text is a HTML response"""
        normalized_content_type = (content_type or "").lower()
        if "text/html" in normalized_content_type:
            return True
        stripped_text = text.lstrip().lower()
        return stripped_text.startswith("<!doctype") or stripped_text.startswith("<html")

    @staticmethod
    def _message_from_text_response(response: Any) -> str | None:
        """
        Extract an error message from a `response.text` attribute.

        Parses the URL, status code and text.
        Omits HTML responses and truncates long text responses (>800 chars).
        """
        text = getattr(response, "text", None)
        if not text:
            return None

        url = getattr(response, "url", None)
        if url is not None:
            url = DefaultHandler._omit_query_params(str(url))

        resp_status = getattr(response, "status_code", None)

        content_type = None
        headers = getattr(response, "headers", None)
        if headers is not None:
            content_type = headers.get("content-type", None)

        if DefaultHandler._is_html_response(text, content_type):
            if url is not None and resp_status is not None:
                return f"[{resp_status}][{url}] {HTML_ERROR_MESSAGE}"
            return HTML_ERROR_MESSAGE

        normalized_text = DefaultHandler._normalize_text_message(text)
        if len(normalized_text) > MAX_TEXT_ERROR_MESSAGE_LENGTH:
            normalized_text = normalized_text[:MAX_TEXT_ERROR_MESSAGE_LENGTH] + TRUNCATED_APPENDIX

        if url is not None and resp_status is not None:
            return f"[{resp_status}][{url}] {normalized_text}"
        return normalized_text

    @staticmethod
    def _extract_error_message(e: Exception, status_code: int | None) -> str | None:
        response = getattr(e, "response", None)
        if response is None:
            return getattr(e, "message", str(e))

        json_message = DefaultHandler._message_from_json_response(response, status_code)
        if json_message is not None:
            return json_message

        text_message = DefaultHandler._message_from_text_response(response)
        if text_message is not None:
            return text_message

        return None

    @staticmethod
    def _fallback_error_message(e: Exception) -> str:
        return f"{e.__class__.__name__}: (no message)"

    @staticmethod
    def _populate_base_error_info(
        response: ErrorResponse,
        e: Exception,
        original_func: Any,
        status_code: int | None,
        message: str | None,
    ) -> None:
        exception_message = getattr(e, "message", None)

        if message:
            response.error.message = message
        elif exception_message is not None:
            response.error.message = exception_message
        else:
            response.error.message = str(e)

        normalized = (
            response.error.message.strip() if isinstance(response.error.message, str) else ""
        )
        response.error.message = (
            DefaultHandler._fallback_error_message(e) if not normalized else normalized
        )
        response.error.status_code = status_code
        response.error.raised_in = f"{original_func.__module__}:{original_func.__name__}"
        response.error.raised_by = f"{e.__class__.__name__}"

    @staticmethod
    def _handle_connector_error(response: ErrorResponse, e: ConnectorError) -> None:
        code = e.error_code
        if isinstance(code, ConnectorErrorCode):
            response.error.error_code = code
        else:
            # Normalise deprecated ErrorCode values and redirect to appropriate replacement
            response.error.error_code = DEPRECATED_CODE_REDIRECTS.get(
                code.value
            ) or ConnectorErrorCode(code.value)
        response.error.app_error_code = e.app_error_code if e.app_error_code else None

    @staticmethod
    def _handle_special_cases(response: ErrorResponse, e: Exception) -> None:
        response.error.error_code = ConnectorErrorCode.INTERNAL_ERROR
        error_text = str(e)

        if "illegal header" in error_text.lower():
            response.error.message = ILLEGAL_HEADER_MESSAGE
            response.error.error_code = ConnectorErrorCode.BAD_REQUEST

        if isinstance(e, ConnectError) or any(
            token in error_text.lower() for token in DNS_ERROR_TOKENS
        ):
            response.error.message = FAILED_TO_CONNECT_MESSAGE
            response.error.error_code = ConnectorErrorCode.CONNECTION_TIMEOUT

        if isinstance(e, json.JSONDecodeError):
            response.error.error_code = ConnectorErrorCode.INVALID_RESPONSE
            if not response.error.message or response.error.message == error_text:
                response.error.message = FAILED_TO_PARSE_JSON_MESSAGE.format(error_text=error_text)

    @staticmethod
    def handle(
        e: Exception,
        original_func: Any,
        response: ErrorResponse,
        error_code: ErrorCode | ConnectorErrorCode | None = None,
    ) -> ErrorResponse:
        logger.debug(e, exc_info=True)

        status_code = DefaultHandler._extract_status_code(e)
        response_message = DefaultHandler._extract_error_message(e, status_code)
        DefaultHandler._populate_base_error_info(
            response, e, original_func, status_code, response_message
        )

        if isinstance(e, ConnectorError):
            DefaultHandler._handle_connector_error(response, e)
        else:
            DefaultHandler._handle_special_cases(response, e)

        return response


class HTTPHandler(ExceptionHandler):
    """
    Default exception handler for simple HTTP exceptions.
    If you want to handle more complicated exceptions, you can create your own instead.
    """

    @staticmethod
    def handle(
        e: Exception,
        original_func: Any,
        response: ErrorResponse,
        error_code: ErrorCode | ConnectorErrorCode | None = None,
    ) -> ErrorResponse:
        match response.error.status_code:
            case 400 | 413 | 415 | 422:
                response.error.error_code = ConnectorErrorCode.BAD_REQUEST
            case 401:
                response.error.error_code = ConnectorErrorCode.UNAUTHORIZED
            case 403:
                response.error.error_code = ConnectorErrorCode.PERMISSION_DENIED
            case 404:
                response.error.error_code = ConnectorErrorCode.NOT_FOUND
            case 405 | 406 | 501:
                response.error.error_code = ConnectorErrorCode.UNSUPPORTED_OPERATION
            case 408:
                response.error.error_code = ConnectorErrorCode.REQUEST_TIMEOUT
            case 409:
                response.error.error_code = ConnectorErrorCode.CONFLICT
            case 429:
                response.error.error_code = ConnectorErrorCode.RATE_LIMIT
            case 503:
                response.error.error_code = ConnectorErrorCode.SERVICE_ERROR
            case 500 | 502 | 504:
                response.error.error_code = ConnectorErrorCode.BAD_GATEWAY
            case _:
                response.error.error_code = ConnectorErrorCode.INVALID_RESPONSE
        return response


ErrorMap = list[
    tuple[type[Exception], type[ExceptionHandler], ErrorCode | ConnectorErrorCode | None]
]


def handle_exception(
    error: Exception, exception_classes: ErrorMap, capability: Callable[[Any], Any], app_id: str
) -> ErrorResponse:
    """
    Decorator that adds error handling to a method. Uses the default Lumos error handler if no exception handler is provided.

    Example:
    ```python
    @exception_handler(
        (httpx.HTTPStatusError, ExceptionHandler, "error.code"),
    )
    async def verify_credentials(self, args: ValidateCredentialsArgs) -> ValidateCredentialsResp:
        pass
    ```

    Args:
        exception_classes (tuple): Tuple of exception classes to be handled. Map of exception class to handler function.

    Returns
    -------
        function: Decorated function.
    """

    resp = ErrorResponse(
        is_error=True,
        error=Error(
            message=str(error), error_code=ConnectorErrorCode.INTERNAL_ERROR, app_id=app_id
        ),
    )

    resp = DefaultHandler.handle(
        error,
        capability,
        resp,
        None,
    )

    if not isinstance(error, ConnectorError):
        for exception_class, handler, code in exception_classes:
            if isinstance(error, exception_class) and handler:
                resp = handler.handle(error, capability, resp, code)

    # Auto-populate metadata
    if isinstance(error, ConnectorError):
        # metadata is built based on the exception
        resp.error.error_metadata = error.get_error_metadata()
    elif isinstance(resp.error.error_code, ConnectorErrorCode):
        # metadata is built based on the error code
        resp.error.error_metadata = build_metadata(resp.error.error_code)
    else:
        # default fallback to INTERNAL_ERROR
        resp.error.error_metadata = build_metadata(ConnectorErrorCode.INTERNAL_ERROR)

    # Log the error + metadata
    error_metadata = resp.error.error_metadata
    error_logger.error(
        "%s/%s: %s | error_fault=%s error_category=%s error_retryable=%s error_throttled=%s error_refreshable=%s error_hint=%s",
        resp.error.app_id,
        resp.error.error_code.value,
        resp.error.message,
        error_metadata.fault.value,
        error_metadata.category.value,
        error_metadata.retryable,
        error_metadata.throttled,
        error_metadata.refreshable,
        error_metadata.hint or "",
        exc_info=True,
    )
    return resp
