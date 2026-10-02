# Copyright 2023 Agnostiq Inc.


import contextlib

import requests
from rich.console import Console

from covalent_cloud.shared.classes.settings import settings

"""Covalent Cloud SDK Exception module."""


class CovalentSDKError(Exception):
    """Covalent Cloud SDK Base Exception class.

    Attributes:
        message (str): Explanation of the error.
        code (str): String enum representing error analogous to error code.
    """

    def __init__(self, message: str = "Generic Error", code: str = "error/generic") -> None:
        """
        Initializes a new instance of the CovalentSDKError class.

        Args:
            message (str): Explanation of the error.
            code (str): String enum representing error analogous to error code.

        """
        self.message = message
        self.code = code
        super().__init__(f"[{code}] {message}")

    @staticmethod
    def print_error(e: Exception, level: str = "warning") -> None:
        """Print a CovalentSDKError.

        Args:
            e: The CovalentSDKError to print.
            level: The level of the message to print.  Defaults to "warning".

        """
        message = str(e)

        # if it is an error raised by APIClient (requests lib under the hood) parse out error message and display
        if isinstance(e, requests.HTTPError):
            error_response = e.response
            with contextlib.suppress(Exception):
                message = error_response.json().get("detail", message)

        console = Console()
        if level == "warning":
            console.print(f"[bold yellow1]WARNING: {message}[bold yellow1]")
        elif level == "error":
            console.print(f"[bold red1]ERROR: {message}[bold red1]")

    def rich_print(self, level: str = "warning") -> None:
        CovalentSDKError.print_error(self, level)


class CovalentAPIKeyError(CovalentSDKError):
    """Covalent Cloud SDK API Key Error class."""

    def __init__(self, message, code) -> None:
        super().__init__(message, code)


class CovalentGenericAPIError(CovalentSDKError):
    """Covalent Cloud Server Generic API Error class."""

    def __init__(self, error) -> None:
        try:
            error_message = error.response.json()["detail"]
            error_code = error.response.json()["code"]
        except:
            error_message = "Unknown Error"
            error_code = "error/unknown"

        super().__init__(error_message, error_code)


class InsufficientMemoryError(CovalentSDKError):
    """Error raised when the assigned executor's memory is insufficient for reliable service operation."""

    def __init__(self, memory) -> None:
        message = f"The assigned executor's memory ({memory} GB) is insufficient for reliable service operation. Assign an executor with more than {settings.function_serve.min_executor_memory_gb} GB of memory to avoid this error (a minimum of {settings.function_serve.recommended_executor_memory_gb} GB is recommended)."
        code = "error/insufficient_memory"
        super().__init__(message, code)


class CovalentCloudError(CovalentSDKError):
    """Base exception for Covalent Cloud SDK."""

    pass


class ResourceNotFoundError(CovalentCloudError):
    """Resource does not exist or user lacks access."""

    def __init__(self, message: str = "Resource not found"):
        super().__init__(message, "resource/not_found")


class AuthenticationError(CovalentCloudError):
    """Authentication failed."""

    def __init__(self, message: str = "Authentication failed"):
        super().__init__(message, "auth/failed")


class ValidationError(CovalentCloudError):
    """Invalid parameters provided."""

    def __init__(self, message: str = "Invalid parameters"):
        super().__init__(message, "validation/error")


def handle_error(e):
    """Handle a Covalent Cloud SDK Error.

    Args:
        e: The Covalent Cloud SDK Error to handle.

    """
    if isinstance(e, CovalentSDKError):
        e.rich_print(level="error")
    else:
        CovalentSDKError.rich_print(e, level="error")

    raise e
