import time
from pathlib import Path
from typing import NamedTuple

import jwt

from mistralai.workflows.core.auth.provider import TokenWithMaxAge
from mistralai.workflows.exceptions import WorkflowError

# Re-read the file once the cached token is within this many seconds of expiry.
_DEFAULT_REFRESH_MARGIN_SECONDS = 30.0


class _CachedToken(NamedTuple):
    token: str
    exp: float


def _decode_jwt_exp(token: str) -> float:
    """Return a JWT's ``exp`` (epoch seconds), raising ``WorkflowError`` if the token isn't a JWT with an ``exp``."""
    try:
        payload = jwt.decode(token, options={"verify_signature": False})
        return float(payload["exp"])
    except (jwt.InvalidTokenError, KeyError, TypeError, ValueError) as exc:
        raise WorkflowError("Service-account token is not a JWT with an 'exp' claim") from exc


class FileTokenProvider:
    """Reads a JWT from a file, caching it until it nears expiry so rotation is picked up.

    Intended for Kubernetes service-account tokens, which are always JWTs. Read failures raise
    retryable WorkflowErrors so a transient missing/empty file (e.g. a remount during rotation)
    recovers instead of killing the worker.
    """

    def __init__(
        self,
        token_path: str | Path,
        refresh_margin_seconds: float = _DEFAULT_REFRESH_MARGIN_SECONDS,
    ) -> None:
        self._token_path = Path(token_path)
        self._refresh_margin_seconds = refresh_margin_seconds
        self._cached: _CachedToken | None = None

    def get_token(self) -> str:
        return self._current().token

    def get_token_with_max_age(self) -> TokenWithMaxAge:
        """Return the current token and the max seconds a caching consumer may reuse it.

        This is the token's time-to-expiry minus the refresh margin, floored at zero.
        """
        cached = self._current()
        return TokenWithMaxAge(cached.token, max(cached.exp - time.time() - self._refresh_margin_seconds, 0.0))

    def _current(self) -> _CachedToken:
        cached = self._cached
        if cached is not None and time.time() < cached.exp - self._refresh_margin_seconds:
            return cached
        token = self._read_token()
        self._cached = _CachedToken(token, _decode_jwt_exp(token))
        return self._cached

    def _read_token(self) -> str:
        try:
            token = self._token_path.read_text().strip()
        except OSError as exc:
            raise WorkflowError(
                f"Failed to read service-account token from {self._token_path}",
            ) from exc
        if not token:
            raise WorkflowError(
                f"Service-account token file is empty: {self._token_path}",
            )
        return token
