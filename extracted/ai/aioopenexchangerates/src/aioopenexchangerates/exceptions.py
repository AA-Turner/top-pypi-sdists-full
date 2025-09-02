"""Provide exceptions for the Open Exchange Rates API."""


class OpenExchangeRatesError(Exception):
    """Represent an error for the Open Exchange Rates API."""


class OpenExchangeRatesClientError(OpenExchangeRatesError):
    """Represent a client error."""


class OpenExchangeRatesAuthError(OpenExchangeRatesClientError):
    """Represent an authentication error."""


class OpenExchangeRatesRateLimitError(OpenExchangeRatesClientError):
    """Represent a rate limit error."""
