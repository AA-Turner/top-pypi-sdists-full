"""
The gateway client for `seq secret` — the ONLY network surface A3 owns.

Three calls, all authenticated with the caller's own SDK API key (`Authorization: Bearer <SEQUENCES_API_KEY>`):
  POST   /v1/secrets           write/rotate a named bundle   (201 = stored)
  GET    /v1/secrets           list the caller's secrets      (metadata only, never values)
  DELETE /v1/secrets/{name}    delete a named secret

WHY a dedicated client and not `sequence_ai._core.transport.Transport`: that transport puts the raw
response body onto every exception (`body=r.text`). For the WRITE call, a gateway
4xx/5xx may echo the request body — which carries the plaintext env values — so passing `r.text` through
would leak a secret into an exception message / traceback. This client instead hands `raise_for` the exact
plaintext values it just sent, which masks them in every field of the answer and drops its raw text before
the one mapping builds the exception; it never stores or logs a response body. That is the mechanical form
of goal 15/17: no secret value on any SDK-side channel, including the failure path.




"""
from __future__ import annotations

import os
from collections.abc import Iterable
from typing import Any, TYPE_CHECKING

import httpx
import pydantic
from sequence_base.contract import SecretCreateRequest, SecretInfo

from seq._account import auth_headers, credential
from seq.errors import raise_for, unreachable
from sequence_ai._core.mock_gate import is_mock
from sequence_ai._core.names import segment
from sequence_ai.errors import InternalError

if TYPE_CHECKING:
    from seq._mock import MockSecretsBackend





DEFAULT_BASE_URL = "https://api.generalsequences.com"



_TIMEOUT_S = 30.0


def _redact(text: str, values: Iterable[str]) -> str:
    """Replace every plaintext secret value (and nothing else) with `***`.

    Applied to any gateway error text before it leaves this module, so a response that echoes the request
    body cannot surface a value. Longest-first so a value that is a substring of another is masked whole.
    """
    out = text
    for v in sorted((v for v in values if v), key=len, reverse=True):
        out = out.replace(v, "***")
    return out


def _api_key(api_key: str | None, base_url: str | None = None) -> Any:
    """The caller's SDK API key: explicit arg, else SEQUENCES_API_KEY, else their `seq login` sign-in
    (seq/_account.py). Missing → fail closed BEFORE any request, so nothing is ever attempted unauthenticated."""
    return credential(api_key, base_url)


class SecretsClient:
    """The `seq secret` backend selector: one facade, three verbs (`create`/`list`/`delete`).

    The real gateway over httpx, authenticated with the caller's SDK API key. The base URL `mock` selects the SDK's
    own test fixture instead (seq/_mock.py, in no package a user installs: mock_gate.is_mock tells anyone else it is
    not for users). CLI code talks only to this facade and never knows which it hit.
    """

    def __init__(self, api_key: str | None = None, base_url: str | None = None) -> None:
        base = base_url or os.environ.get("SEQUENCES_BASE_URL") or DEFAULT_BASE_URL
        self._backend: _GatewayBackend | MockSecretsBackend
        if is_mock(base):
            from seq._mock import MockSecretsBackend

            self._backend = MockSecretsBackend(base, api_key)
        else:
            self._backend = _GatewayBackend(api_key, base)

    def create(self, req: SecretCreateRequest) -> None:
        self._backend.create(req)

    def list(self) -> list[SecretInfo]:
        return self._backend.list()

    def delete(self, name: str, force: bool = False) -> None:
        self._backend.delete(name, force=force)


class _GatewayBackend:
    """A thin, one-shot client over the gateway's `/v1/secrets` surface. Carries the API key; never a value
    beyond the moment it POSTs one."""

    def __init__(self, api_key: str | None = None, base_url: str | None = None) -> None:
        self._key = _api_key(api_key, base_url)
        self._base = (base_url or os.environ.get("SEQUENCES_BASE_URL") or DEFAULT_BASE_URL).rstrip("/")

    def _client(self) -> httpx.Client:

        from seq._http import RetryReads

        return httpx.Client(
            base_url=self._base,
            timeout=_TIMEOUT_S,

            headers={**auth_headers(self._key), "Content-Type": "application/json"},
            transport=RetryReads(),
        )


    def create(self, req: SecretCreateRequest) -> None:
        """POST /v1/secrets. 2xx (canonically 201) = stored. On any non-2xx, fail closed and raise with the
        gateway's message REDACTED of the values just sent — nothing is treated as stored.

        Re-setting an existing name is a plain re-POST (rotation): the gateway replaces the bundle; A3 does
        not delete-then-create and does not merge.
        """
        values = list(req.env.values())
        try:
            with self._client() as c:

                r = c.post("/v1/secrets", json=req.model_dump())
        except httpx.TransportError as exc:


            raise unreachable(self._base, _redact(str(exc), values)) from None
        raise_for(r, redact=values)


    def list(self) -> list[SecretInfo]:
        """GET /v1/secrets → the caller's secrets as metadata (name + env_keys + timestamps), NEVER values.
        Zero secrets is an empty list, not an error."""
        try:
            with self._client() as c:
                r = c.get("/v1/secrets")
        except httpx.TransportError as exc:
            raise unreachable(self._base, exc) from None
        raise_for(r)
        body = r.json()


        items = body.get("secrets", body) if isinstance(body, dict) else body




        try:
            return [SecretInfo.model_validate(x) for x in items]
        except pydantic.ValidationError:
            raise InternalError("gateway returned a malformed /v1/secrets response") from None


    def delete(self, name: str, force: bool = False) -> None:
        """DELETE /v1/secrets/{name}. A name you have none of is NotFound. While a live deployment binds it the
        gateway answers 409 (code secret_in_use, the deployments in the error's details) unless force=true — raise_for
        surfaces that message (names + the --force way out) to the user."""
        try:
            with self._client() as c:
                r = c.delete(f"/v1/secrets/{segment(name)}", params={"force": "true"} if force else None)
        except httpx.TransportError as exc:
            raise unreachable(self._base, exc) from None
        raise_for(r)
