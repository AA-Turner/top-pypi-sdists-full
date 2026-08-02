"""Auth0 Management API (read-only) — mint a ``client_credentials`` token.

The dedicated ``pysae-tooling-auth0-ro`` M2M client (scopes strictly ``read:*``
on the Management API) lives on the prod Auth0 tenant ``pysae.eu.auth0.com``.
Its credentials are stored in the AWS Secrets Manager secret
:data:`SECRET_ID` (region eu-west-3, keys ``client-id`` / ``client-secret``).
A ``client_credentials`` grant against the tenant mints a read-only Management
API token — the ``GET /api/v2/*`` endpoints work, writes are denied by scope.
"""

import httpx

DOMAIN = "pysae.eu.auth0.com"
AUDIENCE = "https://pysae.eu.auth0.com/api/v2/"
TOKEN_ENDPOINT = f"https://{DOMAIN}/oauth/token"
SECRET_ID = "pysae/tooling/auth0-readonly"

_HTTP_TIMEOUT = 30.0


class Auth0MgmtError(RuntimeError):
    """Raised when the Auth0 ``client_credentials`` exchange fails."""


def fetch_mgmt_token(client_id: str, client_secret: str) -> dict[str, object]:
    """Mint a read-only Management API token via ``client_credentials``.

    Returns the raw Auth0 token response (``access_token``, ``token_type``,
    ``expires_in``, ``scope``). Raises :class:`Auth0MgmtError` on any non-200.
    """
    with httpx.Client(timeout=_HTTP_TIMEOUT) as client:
        resp = client.post(
            TOKEN_ENDPOINT,
            data={
                "grant_type": "client_credentials",
                "client_id": client_id,
                "client_secret": client_secret,
                "audience": AUDIENCE,
            },
        )
    payload = resp.json() if resp.content else {}
    if resp.status_code != 200:
        raise Auth0MgmtError(_describe(payload, resp.status_code))
    return payload if isinstance(payload, dict) else {}


def _describe(payload: object, status: int) -> str:
    if isinstance(payload, dict) and payload.get("error"):
        desc = payload.get("error_description") or ""
        return f"Auth0 {payload['error']}: {desc}".strip()
    return f"Auth0 token endpoint returned HTTP {status}"
