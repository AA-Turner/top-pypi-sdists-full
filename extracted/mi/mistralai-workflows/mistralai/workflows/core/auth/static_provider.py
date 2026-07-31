from mistralai.workflows.core.auth.provider import TokenWithMaxAge


class StaticTokenProvider:
    """Returns a fixed token, wrapping the legacy ``MISTRAL_API_KEY`` value."""

    def __init__(self, token: str) -> None:
        self._token = token

    def get_token(self) -> str:
        return self._token

    def get_token_with_max_age(self) -> TokenWithMaxAge:
        return TokenWithMaxAge(self._token, float("inf"))
