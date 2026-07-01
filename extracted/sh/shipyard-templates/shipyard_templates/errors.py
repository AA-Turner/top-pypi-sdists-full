from .exit_code_exception import ExitCodeException
from typing import Union

EXIT_CODE_INVALID_CREDENTIAL = 180
EXIT_CODE_BAD_API_REQUEST = 181
EXIT_CODE_ACCESS_DENIED = 182
EXIT_CODE_NOT_FOUND = 183
EXIT_CODE_INTERNAL_SERVER_ERROR = 184
EXIT_CODE_UNKNOWN_ERROR = 249


class InvalidCredentialError(ExitCodeException):
    def __init__(self, message):
        super().__init__(message, exit_code=EXIT_CODE_INVALID_CREDENTIAL)


class BadRequestError(ExitCodeException):
    def __init__(self, message):
        super().__init__(message, exit_code=EXIT_CODE_BAD_API_REQUEST)


class AccessDeniedError(ExitCodeException):
    def __init__(self, message):
        super().__init__(message, exit_code=EXIT_CODE_ACCESS_DENIED)


class NotFoundError(ExitCodeException):
    def __init__(self, message):
        super().__init__(message, exit_code=EXIT_CODE_NOT_FOUND)


class InternalServerError(ExitCodeException):
    def __init__(self, message):
        super().__init__(message, exit_code=EXIT_CODE_INTERNAL_SERVER_ERROR)


def handle_errors(error_message: str, error_code: Union[int, str]):
    """Helper function to raise the appropriate error based on the HTTP status code

    Args:
        error_message: The message returned by the server
        error_code: The HTTP status code

    Raises:
        InvalidCredentialError:
        BadRequestError:
        AccessDeniedError:
        NotFoundError:
        InternalServerError:
        ExitCodeException:
    """
    if error_code == 401:
        raise InvalidCredentialError(
            f"Invalid credentials. Response from the server: {error_message}"
        )
    elif error_code == 400:
        raise BadRequestError(f"Bad request. Response from the server: {error_message}")
    elif error_code == 403:
        raise AccessDeniedError(
            f"Access denied. Response from the server: {error_message}"
        )
    elif error_code == 404:
        raise NotFoundError(
            f"Resource not found. Response from the server: {error_message}"
        )
    elif error_code == 500:
        raise InternalServerError(
            f"Internal server error. Response from the server: {error_message}"
        )
    else:
        raise ExitCodeException(
            f"An unexpected error occurred: {error_message}",
            exit_code=EXIT_CODE_UNKNOWN_ERROR,
        )
