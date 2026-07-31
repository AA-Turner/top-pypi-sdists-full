from typing import NamedTuple, Protocol


class TokenWithMaxAge(NamedTuple):
    """A token and the max seconds a caching consumer may reuse it before re-fetching.

    ``max_age`` is ``inf`` when the credential never rotates (e.g. a static key).
    """

    token: str
    max_age: float


class TokenProvider(Protocol):
    """Supplies the bearer token used to authenticate the SDK against Mistral services."""

    def get_token(self) -> str: ...

    def get_token_with_max_age(self) -> TokenWithMaxAge:
        """Return the current token and how long a caching consumer may reuse it before re-fetching.

        Used by long-lived push-based consumers.
        """
        ...
