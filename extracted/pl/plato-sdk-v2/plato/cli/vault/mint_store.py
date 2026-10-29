"""Where `plato vault mint token` keeps a grant: the Chronos login vault, never this machine and
never an org secret.

The grant goes in with ``PUT .../grants/{kind}`` (it lands ``paused``) and is set ``active``, so
Chronos refreshes it on demand from then on (a token read, or a launch that resolves it). The
routes are plato's ``chronos/api/login_vault_grants.py``. Reads go through the generated SDK
routes; it has no write route, so the writes are requests here.
Writes need a person's own Plato key. No error text quotes a request or a reply body.
"""

from __future__ import annotations

from datetime import datetime
from typing import TypeVar, cast
from urllib.parse import quote

import httpx
from pydantic import BaseModel, ConfigDict, SecretStr, ValidationError

from plato.chronos.api.login_vault import get_login_vault_grant, get_login_vault_grant_token
from plato.chronos.errors import APIError, NotFoundError
from plato.cli.vault.client import VaultConsoleError
from plato.cli.vault.mint_models import OAuthSpec, OAuthTokens

STORE_TIMEOUT_S = 30.0
M = TypeVar("M", bound=BaseModel)


class StoreRefused(VaultConsoleError):
    """Chronos refused a grant write or read. Exit 6."""

    exit_code = 6


class GrantState(BaseModel):
    """The fields of a grant reply this command reads (``LoginVaultGrant``, no secret)."""

    model_config = ConfigDict(extra="ignore")

    state: str
    generation: int
    scopes: list[str] = []
    has_refresh_token: bool = False
    expires_at: datetime | None = None


class GrantToken(BaseModel):
    model_config = ConfigDict(extra="ignore")

    access_token: SecretStr
    expires_at: datetime | None = None
    generation: int
    refreshed: bool = False


class TokenReadFailed(StoreRefused):
    """The token read answered an error: no grant (404), not active and expired or a refresh
    that never ended (409), or the vendor refused the refresh (502)."""

    def __init__(self, message: str, status: int) -> None:
        super().__init__(message)
        self.status = status


def _json(response: httpx.Response) -> object:
    try:
        return response.json()
    except ValueError:
        return None


def _detail(body: object) -> str:
    """A refusal's ``detail`` when it is a string (FastAPI's 409s and 403s); a 422's detail can
    echo the body, so only its locations."""
    if not isinstance(body, dict):
        return ""
    detail = cast("dict[str, object]", body).get("detail")
    if isinstance(detail, str):
        return detail
    if not isinstance(detail, list):
        return ""
    locs: list[str] = []
    for item in cast("list[object]", detail):
        loc = cast("dict[str, object]", item).get("loc") if isinstance(item, dict) else None
        if isinstance(loc, list):
            locs.append(".".join(str(p) for p in cast("list[object]", loc)))
    return "; ".join(locs)


class GrantStore:
    def __init__(self, base_url: str, api_key: str, http: httpx.Client | None = None) -> None:
        self._base = base_url.rstrip("/")
        self._http = http or httpx.Client(base_url=self._base, timeout=STORE_TIMEOUT_S)
        self._key = api_key
        self._headers = {"X-API-Key": api_key, "Accept": "application/json"}

    def close(self) -> None:
        self._http.close()

    def __enter__(self) -> GrantStore:
        return self

    def __exit__(self, *exc: object) -> None:
        self.close()

    def _path(self, login_key: str, account: str, kind: str) -> str:
        return f"/api/login-vault/accounts/{quote(login_key, safe='')}/{quote(account, safe='')}/grants/{kind}"

    def _send(self, method: str, path: str, what: str, body: object | None = None) -> httpx.Response:
        try:
            return self._http.request(method, f"{self._base}{path}", json=body, headers=self._headers)
        except httpx.HTTPError as e:
            raise StoreRefused(f"{what}: Chronos did not answer ({type(e).__name__})") from None

    def _call(self, method: str, path: str, what: str, body: object | None = None) -> httpx.Response:
        response = self._send(method, path, what, body)
        if response.status_code >= 400:
            raise StoreRefused(f"{what}: HTTP {response.status_code} {_detail(_json(response))}".rstrip())
        return response

    def grant(self, login_key: str, account: str, kind: str) -> GrantState | None:
        what = "the grant read"
        try:
            got = get_login_vault_grant.sync(
                self._http, quote(login_key, safe=""), quote(account, safe=""), kind, x_api_key=self._key
            )
            return GrantState.model_validate(got.model_dump(mode="json"))
        except NotFoundError:
            return None
        except APIError as e:
            raise StoreRefused(f"{what}: HTTP {e.status_code} {_detail(e.body)}".rstrip()) from None
        except httpx.HTTPError as e:
            raise StoreRefused(f"{what}: Chronos did not answer ({type(e).__name__})") from None
        except ValueError:
            raise StoreRefused(f"{what}: Chronos answered with an unreadable body") from None

    def token(self, login_key: str, account: str, kind: str) -> GrantToken:
        """The access token; Chronos refreshes an active grant first when it is due."""
        what = "the grant token read"
        try:
            got = get_login_vault_grant_token.sync(
                self._http, quote(login_key, safe=""), quote(account, safe=""), kind, x_api_key=self._key
            )
            return GrantToken.model_validate(got.model_dump(exclude_none=True))
        except APIError as e:
            raise TokenReadFailed(f"{what}: HTTP {e.status_code} {_detail(e.body)}".rstrip(), e.status_code) from None
        except httpx.HTTPError as e:
            raise StoreRefused(f"{what}: Chronos did not answer ({type(e).__name__})") from None
        except ValueError:
            raise StoreRefused(f"{what}: Chronos answered with an unreadable body") from None

    def set_state(self, login_key: str, account: str, kind: str, state: str, generation: int) -> GrantState:
        path = f"{self._path(login_key, account, kind)}/state"
        body = {"state": state, "generation": generation}
        return _model(GrantState, self._call("POST", path, f"the grant state {state}", body), "the grant state")

    def import_grant(
        self,
        login_key: str,
        account: str,
        kind: str,
        spec: OAuthSpec,
        client_id: str,
        client_secret: SecretStr | None,
        redirect_uri: str,
        tokens: OAuthTokens,
        user_id: str | None,
        consent_email: str | None,
    ) -> GrantState:
        if tokens.refresh_token is None:
            raise StoreRefused("the vendor gave no refresh token, and a login-vault grant needs one")
        body = {
            "client_id": client_id,
            "client_auth": spec.client_auth.value,
            "token_url": spec.token_url,
            "resource": spec.resource,
            "redirect_uri": redirect_uri,
            "scopes": spec.scopes,
            "client_secret": client_secret.get_secret_value() if client_secret is not None else None,
            "refresh_token": tokens.refresh_token.get_secret_value(),
            "access_token": tokens.access_token.get_secret_value(),
            "expires_at": tokens.expires_at.isoformat() if tokens.expires_at else None,
            "user_id": user_id,
            "consent_email": consent_email,
        }
        response = self._call("PUT", self._path(login_key, account, kind), "the grant import", body)
        del body
        return _model(GrantState, response, "the grant import")


def _model(model: type[M], response: httpx.Response, what: str) -> M:
    try:
        return model.model_validate(response.json())
    except (ValueError, ValidationError):
        raise StoreRefused(f"{what}: Chronos answered HTTP {response.status_code} with an unreadable body") from None
