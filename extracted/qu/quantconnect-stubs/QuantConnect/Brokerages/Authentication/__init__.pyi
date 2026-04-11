from typing import overload
from enum import IntEnum
import abc
import datetime
import typing

import QuantConnect.Api
import QuantConnect.Brokerages.Authentication
import System
import System.Threading
import System.Threading.Tasks

AuthenticationHeaderValue = typing.Any
HttpResponseMessage = typing.Any

QuantConnect_Brokerages_Authentication_LeanOAuthTokenHandler_T = typing.TypeVar("QuantConnect_Brokerages_Authentication_LeanOAuthTokenHandler_T")
QuantConnect_Brokerages_Authentication_LeanTokenHandler_T = typing.TypeVar("QuantConnect_Brokerages_Authentication_LeanTokenHandler_T")
QuantConnect_Brokerages_Authentication__EventContainer_Callable = typing.TypeVar("QuantConnect_Brokerages_Authentication__EventContainer_Callable")
QuantConnect_Brokerages_Authentication__EventContainer_ReturnType = typing.TypeVar("QuantConnect_Brokerages_Authentication__EventContainer_ReturnType")


class TokenType(IntEnum):
    """Defines the supported types of access tokens used for authentication."""

    BEARER = 0
    """A Bearer token, typically used for standard HTTP Authorization headers."""

    SESSION_TOKEN = 1
    """A Session token, typically used for username/password authorization headers."""


class OAuthTokenRequest(System.Object):
    """
    Represents a Lean platform token request, including all fields required by the
    live/auth0/refresh endpoint. Optional fields are omitted from JSON when null.
    """

    @property
    def brokerage(self) -> str:
        """
        Gets the name of the brokerage associated with the access token request.
        The value is normalized to lowercase.
        """
        ...

    @brokerage.setter
    def brokerage(self, value: str) -> None:
        ...

    @property
    def account_id(self) -> str:
        """Gets the account identifier associated with the brokerage."""
        ...

    @account_id.setter
    def account_id(self, value: str) -> None:
        ...

    @property
    def refresh_token(self) -> str:
        """
        Gets the OAuth refresh token used to obtain a new access token.
        Omitted from JSON when null.
        """
        ...

    @refresh_token.setter
    def refresh_token(self, value: str) -> None:
        ...

    @property
    def deploy_id(self) -> str:
        """
        Gets the Lean deploy identifier for brokerages that require it.
        Omitted from JSON when null.
        """
        ...

    @deploy_id.setter
    def deploy_id(self, value: str) -> None:
        ...

    def __init__(self, brokerage: str, account_id: str, refresh_token: str = None, deploy_id: str = None) -> None:
        """
        Initializes a new instance of OAuthTokenRequest with all fields.
        Use named parameters to supply only the fields required by the target brokerage.
        
        :param brokerage: The brokerage name. Normalized to lowercase.
        :param account_id: The account number or identifier.
        :param refresh_token: OAuth refresh token; omitted from JSON when null.
        :param deploy_id: Lean deploy identifier; omitted from JSON when null.
        """
        ...

    def to_json(self) -> str:
        """
        Serializes the request into a compact camelCase JSON string.
        Null properties are excluded from the output.
        
        :returns: A JSON string representing the current request.
        """
        ...


class LeanOAuthTokenHandler(typing.Generic[QuantConnect_Brokerages_Authentication_LeanOAuthTokenHandler_T], QuantConnect.Brokerages.Authentication.LeanTokenHandler[QuantConnect_Brokerages_Authentication_LeanOAuthTokenHandler_T]):
    """
    Handles OAuth token retrieval and caching by interacting with the Lean platform.
    Implements retry and expiration logic for secure HTTP communication.
    """

    @property
    def max_retry_count(self) -> int:
        """
        The maximum number of retry attempts when fetching an access token.
        
        
        This codeEntityType is protected.
        """
        ...

    @max_retry_count.setter
    def max_retry_count(self, value: int) -> None:
        ...

    @property
    def retry_interval(self) -> datetime.timedelta:
        """
        The time interval to wait between retry attempts when fetching an access token.
        
        
        This codeEntityType is protected.
        """
        ...

    @retry_interval.setter
    def retry_interval(self, value: datetime.timedelta) -> None:
        ...

    @property
    def offset_before_expiration(self) -> datetime.timedelta:
        """Some padding before expiration to request a new token"""
        ...

    @offset_before_expiration.setter
    def offset_before_expiration(self, value: datetime.timedelta) -> None:
        ...

    def __init__(self, api_client: QuantConnect.Api.ApiConnection, request: QuantConnect.Brokerages.Authentication.OAuthTokenRequest, token_lifetime: datetime.timedelta) -> None:
        """
        Initializes a new instance of the LeanOAuthTokenHandler class with default token credentials type.
        
        :param api_client: The API client used to communicate with the Lean platform.
        :param request: The request model used to generate the access token.
        :param token_lifetime: The expected lifetime of a fetched token. A 1-minute safety buffer is applied before expiry.
        Must be provided explicitly — each brokerage has a different token lifetime.
        """
        ...

    def get_access_token(self, cancellation_token: System.Threading.CancellationToken) -> QuantConnect_Brokerages_Authentication_LeanOAuthTokenHandler_T:
        """
        Retrieves a valid access token from the Lean platform.
        Caches and reuses tokens until expiration to minimize unnecessary requests.
        Retries up to max_retry_count times on failure. Thread-safe via a lock.
        
        :param cancellation_token: A token used to observe cancellation requests.
        :returns: A LeanTokenCredentials instance containing the token type and access token string.
        """
        ...


class LeanTokenCredentials(QuantConnect.Api.RestResponse):
    """
    Represents credentials required for token-based authentication,
    including the access token and its type (e.g., Bearer).
    """

    @property
    def token_type(self) -> QuantConnect.Brokerages.Authentication.TokenType:
        """Gets the type of the token (e.g., Bearer)."""
        ...

    @token_type.setter
    def token_type(self, value: QuantConnect.Brokerages.Authentication.TokenType) -> None:
        ...

    @property
    def access_token(self) -> str:
        """Gets the token string used for authentication."""
        ...

    @access_token.setter
    def access_token(self, value: str) -> None:
        ...

    @overload
    def __init__(self, token_type: QuantConnect.Brokerages.Authentication.TokenType, access_token: str) -> None:
        """
        Initializes a new instance of the LeanTokenCredentials class.
        
        :param token_type: The type of the token.
        :param access_token: The token string.
        """
        ...

    @overload
    def __init__(self) -> None:
        """Initializes a new instance of the LeanTokenCredentials class."""
        ...


class LeanTokenHandler(typing.Generic[QuantConnect_Brokerages_Authentication_LeanTokenHandler_T], metaclass=abc.ABCMeta):
    """
    Provides base functionality for token-based HTTP request handling.
    Token acquisition and retry logic are delegated entirely to get_access_token,
    implemented by derived classes (e.g., LeanOAuthTokenHandler).
    """

    @property
    def authentication_failed(self) -> _EventContainer[typing.Callable[[System.Object, System.Exception], typing.Any], typing.Any]:
        """
        Raised when authentication fails after all retry attempts are exhausted.
        Subscribers can use this to trigger graceful application shutdown.
        """
        ...

    @authentication_failed.setter
    def authentication_failed(self, value: _EventContainer[typing.Callable[[System.Object, System.Exception], typing.Any], typing.Any]) -> None:
        ...

    def __init__(self, create_auth_header: typing.Callable[[QuantConnect.Brokerages.Authentication.TokenType, str], AuthenticationHeaderValue] = None, handler: typing.Any = None) -> None:
        """
        Initializes a new instance of the LeanTokenHandler{T} class.
        
        
        This codeEntityType is protected.
        
        :param create_auth_header: An optional delegate for creating an AuthenticationHeaderValue
        from the token type and access token. If not provided, a default implementation is used.
        :param handler: An optional inner HttpMessageHandler. If not provided, a default HttpClientHandler is used.
        """
        ...

    def get_access_token(self, cancellation_token: System.Threading.CancellationToken) -> QuantConnect_Brokerages_Authentication_LeanTokenHandler_T:
        """
        Retrieves a valid access token for authenticating HTTP requests.
        Must be implemented by derived classes to provide token type and value,
        with optional support for caching and refresh logic.
        
        :param cancellation_token: A cancellation token that can be used to cancel the token retrieval operation.
        :returns: A LeanTokenCredentials instance containing the token type and access token string.
        """
        ...

    def on_authentication_failed(self, exception: System.Exception) -> None:
        """
        Invokes the authentication_failed event.
        Derived classes call this when authentication fails after exhausting all retry attempts.
        
        
        This codeEntityType is protected.
        
        :param exception: The exception that caused the authentication failure.
        """
        ...

    def send(self, request: typing.Any, cancellation_token: System.Threading.CancellationToken) -> typing.Any:
        """
        Sends an HTTP request synchronously, applying token-based authentication.
        
        
        This codeEntityType is protected.
        
        :param request: The HTTP request message to send.
        :param cancellation_token: A cancellation token to cancel operation.
        :returns: The HTTP response message.
        """
        ...

    def send_async(self, request: typing.Any, cancellation_token: System.Threading.CancellationToken) -> System.Threading.Tasks.Task[HttpResponseMessage]:
        """
        Sends an HTTP request asynchronously by internally invoking the synchronous send(HttpRequestMessage, CancellationToken) method.
        This is useful for compatibility with components that require an asynchronous pipeline, even though the core logic is synchronous.
        
        
        This codeEntityType is protected.
        
        :param request: The HTTP request message to send.
        :param cancellation_token: A cancellation token to cancel the operation.
        :returns: A task representing the asynchronous operation, containing the HTTP response message.
        """
        ...


class _EventContainer(typing.Generic[QuantConnect_Brokerages_Authentication__EventContainer_Callable, QuantConnect_Brokerages_Authentication__EventContainer_ReturnType]):
    """This class is used to provide accurate autocomplete on events and cannot be imported."""

    def __call__(self, *args: typing.Any, **kwargs: typing.Any) -> QuantConnect_Brokerages_Authentication__EventContainer_ReturnType:
        """Fires the event."""
        ...

    def __iadd__(self, item: QuantConnect_Brokerages_Authentication__EventContainer_Callable) -> typing.Self:
        """Registers an event handler."""
        ...

    def __isub__(self, item: QuantConnect_Brokerages_Authentication__EventContainer_Callable) -> typing.Self:
        """Unregisters an event handler."""
        ...


