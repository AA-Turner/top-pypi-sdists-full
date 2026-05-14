from __future__ import annotations

import json as jsonlib
from typing import Any
from urllib.parse import urlencode, urlsplit, urlunsplit

from .clients.capsule import PipedreamProxyRequest
from .integration import IntegrationLike, integration_type as normalize_integration_type


class PipedreamProxyResponse:
    """Small requests-compatible response wrapper for Pipedream proxy calls."""

    def __init__(self, *, status_code: int, headers: dict[str, str] | None, body: bytes):
        self.status_code = int(status_code)
        self.headers = dict(headers or {})
        self.content = bytes(body or b"")

    @property
    def ok(self) -> bool:
        return 200 <= self.status_code < 400

    @property
    def text(self) -> str:
        return self.content.decode("utf-8", errors="replace")

    @property
    def reason(self) -> str:
        return self.headers.get("Reason") or self.headers.get("Status") or ""

    def json(self) -> Any:
        return jsonlib.loads(self.text)

    def raise_for_status(self) -> None:
        if self.ok:
            return
        message = f"{self.status_code} Error for proxied Pipedream request"
        if self.text:
            message = f"{message}: {self.text}"
        try:
            import requests

            raise requests.HTTPError(message, response=self)
        except ImportError:
            raise RuntimeError(message)


class PipedreamProxySession:
    """requests.Session-shaped transport backed by Capsule's Pipedream proxy."""

    def __init__(
        self,
        *,
        stub: Any,
        app_id: str,
        user_email: str,
        owner_id: str,
        integration: IntegrationLike,
        env: str = "",
    ) -> None:
        self._stub = stub
        self._app_id = app_id
        self._user_email = user_email
        self._owner_id = owner_id
        self._env = env
        self._integration_type = normalize_integration_type(integration)
        self.headers: dict[str, str] = {}

    def request(
        self,
        method: str,
        url: str,
        *,
        params: Any = None,
        headers: dict[str, str] | None = None,
        data: Any = None,
        json: Any = None,
        timeout: float | tuple[float, float] | None = None,
        **kwargs: Any,
    ) -> PipedreamProxyResponse:
        if kwargs.get("files") is not None:
            raise NotImplementedError("PipedreamProxySession does not support files")
        del timeout

        body, body_headers = _encode_body(data=data, json=json)
        merged_headers = dict(self.headers)
        merged_headers.update(body_headers)
        if headers:
            merged_headers.update(headers)

        req = PipedreamProxyRequest(
            app_id=self._app_id,
            user_email=self._user_email,
            owner_id=self._owner_id,
            env=self._env,
            integration_type=self._integration_type,
            method=str(method).upper(),
            url=_merge_params(url, params),
            headers=merged_headers,
            body=body,
        )
        resp = self._stub.pipedream_proxy(req)
        return PipedreamProxyResponse(
            status_code=resp.status_code,
            headers=dict(resp.headers),
            body=resp.body,
        )

    def get(self, url: str, **kwargs: Any) -> PipedreamProxyResponse:
        return self.request("GET", url, **kwargs)

    def post(self, url: str, **kwargs: Any) -> PipedreamProxyResponse:
        return self.request("POST", url, **kwargs)

    def put(self, url: str, **kwargs: Any) -> PipedreamProxyResponse:
        return self.request("PUT", url, **kwargs)

    def patch(self, url: str, **kwargs: Any) -> PipedreamProxyResponse:
        return self.request("PATCH", url, **kwargs)

    def delete(self, url: str, **kwargs: Any) -> PipedreamProxyResponse:
        return self.request("DELETE", url, **kwargs)

    def head(self, url: str, **kwargs: Any) -> PipedreamProxyResponse:
        return self.request("HEAD", url, **kwargs)

    def options(self, url: str, **kwargs: Any) -> PipedreamProxyResponse:
        return self.request("OPTIONS", url, **kwargs)


def _merge_params(url: str, params: Any) -> str:
    if not params:
        return url
    if isinstance(params, bytes):
        encoded = params.decode("utf-8")
    elif isinstance(params, str):
        encoded = params
    else:
        encoded = urlencode(params, doseq=True)
    parts = urlsplit(url)
    query = f"{parts.query}&{encoded}" if parts.query else encoded
    return urlunsplit((parts.scheme, parts.netloc, parts.path, query, parts.fragment))


def _encode_body(*, data: Any, json: Any) -> tuple[bytes, dict[str, str]]:
    if json is not None:
        return (
            jsonlib.dumps(json, separators=(",", ":")).encode("utf-8"),
            {"Content-Type": "application/json"},
        )
    if data is None:
        return b"", {}
    if isinstance(data, bytes):
        return data, {}
    if isinstance(data, bytearray):
        return bytes(data), {}
    if isinstance(data, str):
        return data.encode("utf-8"), {}
    if isinstance(data, dict) or isinstance(data, list) or isinstance(data, tuple):
        return (
            urlencode(data, doseq=True).encode("utf-8"),
            {"Content-Type": "application/x-www-form-urlencoded"},
        )
    if hasattr(data, "read"):
        value = data.read()
        if isinstance(value, str):
            return value.encode("utf-8"), {}
        return bytes(value), {}
    return bytes(data), {}
