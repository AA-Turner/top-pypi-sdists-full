class DjangoEsiException(Exception):
    pass


class TokenError(DjangoEsiException):
    pass


class TokenInvalidError(TokenError):
    pass


class TokenExpiredError(TokenError):
    pass


class NotRefreshableTokenError(TokenError):
    pass


class IncompleteResponseError(DjangoEsiException):
    pass


class SSOUnavailableError(IncompleteResponseError):
    """The EVE SSO could not be reached or failed to respond, after retries.

    The token itself may be fine, so it should be kept.
    """
    pass


class SSOOAuthError(DjangoEsiException):
    """The EVE SSO rejected a request with an OAuth2 error response."""

    def __init__(self, error: str, description: str | None = None) -> None:
        self.error = error
        self.description = description
        super().__init__(error, description)

    def __str__(self) -> str:
        return f"{self.error}: {self.description}" if self.description else self.error
