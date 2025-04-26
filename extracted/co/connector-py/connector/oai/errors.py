import logging
import traceback
from abc import abstractmethod
from collections.abc import Callable
from typing import Any

from connector.generated import Error, ErrorCode, ErrorResponse

logger = logging.getLogger("integration-connectors.sdk")


class ConnectorError(Exception):
    """
    Base exception class for Lumos connectors.
    Preferred way to raise exceptions inside the conenctors.
    `raise ConnectorError(message, error_code)`

    message: str (Custom error message)
    error_code: ErrorCode (The actual error code, eg. "internal_error")
    app_error_code: str | None (The application-specific error code, eg. "my_app.internal_error" or Zoom error 300)
    """

    def __init__(
        self,
        *,
        message: str,
        error_code: ErrorCode,
        app_error_code: str | None = None,
    ):
        self.error_code = error_code
        self.app_error_code = app_error_code
        self.message = message


class ExceptionHandler:
    """
    Abstract class for handling exceptions. You can subclass this to create your own exception handler.
    """

    def __init__(self):
        pass

    @staticmethod
    @abstractmethod
    def handle(
        e: Exception,
        original_func: Any,
        response: ErrorResponse,
        error_code: ErrorCode | None = None,
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
    def handle(
        e: Exception,
        original_func: Any,
        response: ErrorResponse,
        error_code: ErrorCode | None = None,
    ) -> ErrorResponse:
        logger.debug(e, exc_info=True)
        status_code: int | None = None

        # HTTPX HTTP Status code / message
        if hasattr(e, "response") and hasattr(e.response, "status_code"):  # type: ignore
            status_code = e.response.status_code  # type: ignore
        # GraphQL error code
        if hasattr(e, "code"):
            status_code = e.code  # type: ignore

        # Attempt to extract error message from response
        response_message = None
        try:
            error_data = e.response.json()  # type: ignore
            if error_data and not (isinstance(error_data, dict | list) and len(error_data) == 0):
                if hasattr(e, "response") and hasattr(e.response, "url"):  # type: ignore
                    response_message = (
                        f"[{status_code}][{str(e.response.url).split('?')[0]}] {str(error_data)}"  # type: ignore
                    )
                else:
                    response_message = f"[{status_code}] {str(error_data)}"
        except Exception:
            if hasattr(e, "response") and hasattr(e.response, "text"):  # type: ignore
                if hasattr(e.response, "url") and hasattr(e.response, "status_code"):  # type: ignore
                    response_message = (
                        f"[{e.response.status_code}][{str(e.response.url).split('?')[0]}] {e.response.text}"  # type: ignore
                        if e.response.text  # type: ignore
                        else None
                    )
                else:
                    response_message = e.response.text or None  # type: ignore
            else:
                response_message = str(e.message) if hasattr(e, "message") else str(e)  # type: ignore

        # Populating some base info
        if "response_message" in locals() and response_message:
            response.error.message = response_message
        else:
            response.error.message = e.message if hasattr(e, "message") else str(e)  # type: ignore

        response.error.status_code = status_code
        # TODO: add line number
        response.error.raised_in = f"{original_func.__module__}:{original_func.__name__}"
        response.error.raised_by = f"{e.__class__.__name__}"

        # ConnectorError has an error_code param
        if isinstance(e, ConnectorError):
            response.error.error_code = e.error_code
            response.error.app_error_code = e.app_error_code if e.app_error_code else None
        else:
            traceback.print_exception(e)
            response.error.error_code = ErrorCode.UNEXPECTED_ERROR

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
        error_code: ErrorCode | None = None,
    ) -> ErrorResponse:
        match response.error.status_code:
            case 400:
                response.error.error_code = ErrorCode.BAD_REQUEST
            case 401:
                response.error.error_code = ErrorCode.UNAUTHORIZED
            case 403:
                response.error.error_code = ErrorCode.PERMISSION_DENIED
            case 404:
                response.error.error_code = ErrorCode.NOT_FOUND
            case 429:
                response.error.error_code = ErrorCode.RATE_LIMIT
            case _:
                response.error.error_code = ErrorCode.API_ERROR

        return response


ErrorMap = list[tuple[type[Exception], type[ExceptionHandler], ErrorCode | None]]


def handle_exception(
    exception_classes: ErrorMap, error: Exception, func: Callable[[Any], Any], app_id: str
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
        error=Error(message=str(error), error_code=ErrorCode.UNEXPECTED_ERROR, app_id=app_id),
    )

    resp = DefaultHandler.handle(
        error,
        func,
        resp,
        None,
    )

    if not isinstance(error, ConnectorError):
        for exception_class, handler, code in exception_classes:
            if isinstance(error, exception_class) and handler:
                resp = handler.handle(error, func, resp, code)

    logger.error(f"{resp.error.app_id}/{resp.error.error_code}: {resp.error.message}")
    return resp
