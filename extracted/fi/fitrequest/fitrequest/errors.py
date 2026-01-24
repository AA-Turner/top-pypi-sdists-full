from dataclasses import dataclass
from typing import Any

# https://docs.gunicorn.org/en/stable/settings.html#limit-request-line
LIMIT_REQUEST_LINE = 4094


@dataclass
class FitRequestConfigurationError(ValueError):
    """Base fitrequest configuration error."""


@dataclass
class FitRequestRuntimeError(RuntimeError):
    """Base fitrequest runtime error."""


@dataclass
class HTTPStatusError(FitRequestRuntimeError):
    """Pickable version of httpx.HTTPStatusError"""

    status_code: int
    content: bytes
    details: str | None = None


@dataclass
class UnrecognizedParametersError(FitRequestConfigurationError):
    """
    Unrecognized parameters: the following are neither arguments of the current generated method
    nor valid httpx.request arguments
    """

    method_name: str
    unrecognized_arguments: set[str]


@dataclass
class UrlRequestTooLongError(FitRequestRuntimeError):
    """Triggered when the length of the requested URL exceeds the maximum allowed limit."""

    url: str
    url_size: int
    url_size_limit: int = LIMIT_REQUEST_LINE


@dataclass
class InvalidMethodDecoratorError(FitRequestConfigurationError):
    """
    Exception raised when the specified method decorator is either not a valid callable
    or cannot be retrieved from the global environment using the given name.
    """

    provided_decorator: str


@dataclass
class InvalidParamsTypeError(FitRequestConfigurationError):
    """
    Exception raised when the specified parameters have an incorrect type.
    """

    provided_params: Any


@dataclass
class InvalidResponseTypeError(FitRequestConfigurationError):
    """
    Exception raised when the specified response model have an incorrect type.
    """

    provided_model: Any


@dataclass
class UnexpectedLiteralTypeError(FitRequestRuntimeError):
    """
    This exception is raised when an unexpected type is provided instead of a Literal type.
    During CLI generation, Literal types are converted to Enums to ensure compatibility with the typer library.
    """

    bad_type: type


class UnexpectedNoneBaseURLError(FitRequestConfigurationError):
    """Raised when neither MethodConfig nor MethodConfigGroup specifies the base_url attribute."""


class FitDecoratorInvalidUsageError(FitRequestConfigurationError):
    """
    Raised when the @fit decorator is applied to methods that do not belong to a class inheriting from FitRequest.
    """


class MultipleAuthenticationError(FitRequestConfigurationError):
    """
    Raised when more than one authentication method is detected.
    The user should provide only a single valid authentication method for the request.
    """


class HttpVerbNotProvidedError(FitRequestConfigurationError):
    """
    This exception is raised to indicate that a required HTTP verb has not been specified in the
    MethodConfigFamily configuration. The user should ensure that an appropriate HTTP verb
    (such as GET, POST, PUT, PATCH, DELETE) is provided.
    """


@dataclass
class ReservedNamesError(FitRequestConfigurationError):
    """
    This exception is thrown when a reserved name is used as an argument in the generated method.
    """

    reserved_fitrequest_names: set[str]
    reserved_httpx_names: set[str]
    bad_names: set[str]


@dataclass
class MissingRequiredArgumentError(FitRequestRuntimeError):
    """
    This exception is thrown when a required argument (declared using the Pydantic class ``Field``) is missing.
    """

    name: str


@dataclass
class InfinitePaginationError(FitRequestRuntimeError):
    """
    Triggered when the current page has already been requested during the pagination loop,
    resulting in the client being trapped in an infinite loop.
    """

    url_stack: list[str]
