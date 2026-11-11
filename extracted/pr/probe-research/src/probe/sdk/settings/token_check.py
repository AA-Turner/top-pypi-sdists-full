"""Does the API take a token now: one `GET /v1/me` with it (`probe mcp token set`, the wizard, the Codex move)."""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass

from probe.foundation.compat.compat import StrEnum


class TokenVerdict(StrEnum):
    OK = "ok"
    REJECTED = "rejected"  # a definitive 401 or 403
    UNREACHABLE = "unreachable"  # anything else: a blip, a 5xx, a non-2xx answer, a timeout


@dataclass(frozen=True)
class TokenCheck:
    verdict: TokenVerdict
    #: The `/v1/me` answer when OK, else None.
    identity: dict | None = None


def check_token(token: str, base_url: str, *, surface: str | None = None,
                client_headers: Mapping[str, str] | None = None, timeout: float | None = None,
                max_retries: int | None = None) -> TokenCheck:
    """Ask the API who `token` is. OK only for a 2xx answer. Raises what else the request raised."""
    from probe import errors
    from probe.sdk.delivery.transport.transport import Transport
    from probe.sdk.settings.settings import resolve

    options: dict = {"client_headers": client_headers}
    if surface is not None:
        options["surface"] = surface
    if timeout is not None:
        options["timeout"] = timeout
    if max_retries is not None:
        options["max_retries"] = max_retries
    try:
        with Transport(resolve(base_url=base_url, token=token), **options) as transport:
            response = transport.request("GET", "/v1/me", idempotent=True)
            if not 200 <= response.status_code < 300:
                return TokenCheck(TokenVerdict.UNREACHABLE)
            return TokenCheck(TokenVerdict.OK, response.json() if response.content else {})
    except (errors.AuthError, errors.ScopeError):
        return TokenCheck(TokenVerdict.REJECTED)
    except (errors.TransportError, errors.ServerError):
        return TokenCheck(TokenVerdict.UNREACHABLE)
