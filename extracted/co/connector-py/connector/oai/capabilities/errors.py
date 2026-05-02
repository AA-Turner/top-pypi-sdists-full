from functools import cached_property

from connector_sdk_types.generated import ConnectorErrorCode, Error, ErrorResponse


class CapabilityError(Exception):
    """A base exception class for any errors which can occur relating
    to capabilities during integration runtime execution."""

    ERROR_CODE: ConnectorErrorCode = ConnectorErrorCode.INTERNAL_ERROR
    """An error code associated with this type of capability error."""

    def __init__(self, app_id: str, *, message: str) -> None:
        self._app_id = app_id
        self._message = message

    @cached_property
    def error_response(self) -> ErrorResponse:
        """The capability error response derived during capability error handling."""
        return ErrorResponse(
            is_error=True,
            error=Error(
                app_id=self._app_id,
                message=self._message,
                error_code=self.ERROR_CODE,
            ),
        )


class CapabilityNotImplementedError(CapabilityError):
    ERROR_CODE = ConnectorErrorCode.UNSUPPORTED_OPERATION


class CapabilityRequestError(CapabilityError):
    """An error which may occur during capability request handling."""

    ERROR_CODE: ConnectorErrorCode = ConnectorErrorCode.BAD_REQUEST
    """An error code associated with bad capability requests."""


class CapabilityRequestValidationError(CapabilityRequestError):
    """An error which may occurs when a capability request cannot be validated."""

    def __init__(
        self,
        app_id: str,
        *,
        message: str = "Invalid request, expected JSON input.",
    ) -> None:
        super().__init__(app_id, message=message)


class CapabilityRequestAuthenticationError(CapabilityRequestError):
    """An error which may occurs when a capability request cannot be authenticated."""

    def __init__(
        self,
        app_id: str,
        *,
        message: str = "Missing auth/credentials in request",
    ) -> None:
        super().__init__(app_id, message=message)


class CapabilityRequestSettingsError(CapabilityRequestError):
    """An error which may occurs when capability request settings are incomplete."""

    def __init__(
        self,
        app_id: str,
        *,
        message: str = "Invalid settings passed on request.",
    ) -> None:
        super().__init__(app_id, message=message)


class CapabilityExecutionError(CapabilityError):
    """An error which may occur during capability execution."""

    def __init__(self, error_response: ErrorResponse) -> None:
        # NOTE: Since this error response is derived by the capability exception
        # handler, we accept the error response directly.
        self._app_id = error_response.error.app_id
        self._message = error_response.error.message
        self._error_response = error_response

    @cached_property
    def error_response(self) -> ErrorResponse:
        """The error response derived during capability exception handling."""
        return self._error_response


class CapabilityResponseError(CapabilityError):
    """An error which may occur when the capability executes successfully, but does
    not respond with an valid response."""

    ERROR_CODE = ConnectorErrorCode.INVALID_RESPONSE

    def __init__(
        self,
        app_id: str,
        *,
        message: str = "Unxpected response from executed capability.",
    ) -> None:
        super().__init__(app_id, message=message)
