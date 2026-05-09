"""Capsule SDK client — programmatic access to your apps.

Usage::

    import cpsl

    client = cpsl.Client()
    apps = client.list_apps()
    r = client.chat("diet-coach", "I had eggs for breakfast")
    print(r.text)
"""

from __future__ import annotations

import json
import os
import urllib.request
import urllib.error
from dataclasses import dataclass
from typing import Any, Iterator, Optional

from .config import ConfigContext, get_config_context


@dataclass
class ChatResponse:
    """Response from a synchronous chat call."""

    text: str
    session_id: str
    request_id: str
    raw: dict[str, Any]

    def __str__(self) -> str:
        return self.text


@dataclass
class StreamChunk:
    """A single chunk from a streaming chat response."""

    event: str
    data: dict[str, Any]

    @property
    def text(self) -> str:
        return self.data.get("text", "")

    @property
    def done(self) -> bool:
        return self.event == "done" or self.data.get("done", False)


def _http_base(ctx: Optional[ConfigContext]) -> str:
    """Derive the HTTP API base URL from config.

    Checks CAPSULE_HTTP_URL first, then derives from the gRPC config.
    In local dev the HTTP port is gRPC port + 1; in prod they share 443.
    """
    if url := os.environ.get("CAPSULE_HTTP_URL"):
        return url.rstrip("/")
    if not ctx:
        return "https://api.capsule.new"
    host = ctx.gateway_host or "gateway.capsule.new"
    grpc_port = ctx.gateway_port or 443
    if grpc_port == 443:
        if host == "gateway.capsule.new":
            return "https://api.capsule.new"
        return f"https://{host}"
    return f"http://{host}:{grpc_port + 1}"


class Client:
    """Programmatic client for Capsule apps.

    Authenticates using the workspace token from ``capsule login``.
    If ``token`` is not provided, reads from ``~/.capsule/config.ini``.
    """

    def __init__(
        self,
        token: Optional[str] = None,
        gateway_url: Optional[str] = None,
    ):
        ctx = get_config_context()
        if token:
            self._token = token
        elif ctx and ctx.token:
            self._token = ctx.token
        else:
            raise RuntimeError("No credentials. Run 'capsule login' or pass token=.")

        self._base = gateway_url.rstrip("/") if gateway_url else _http_base(ctx)
        self._ctx = ctx
        self._app_cache: dict[str, str] = {}

    def _headers(self) -> dict[str, str]:
        return {
            "Authorization": f"Bearer {self._token}",
            "Content-Type": "application/json",
        }

    def _request(self, method: str, path: str, body: dict | None = None) -> dict:
        url = f"{self._base}/api/v1{path}"
        data = json.dumps(body).encode() if body else None
        req = urllib.request.Request(url, data=data, headers=self._headers(), method=method)
        try:
            with urllib.request.urlopen(req, timeout=120) as resp:
                return json.loads(resp.read())
        except urllib.error.HTTPError as e:
            msg = e.read().decode() if e.fp else str(e)
            raise RuntimeError(f"HTTP {e.code}: {msg}") from e

    def _post(self, path: str, body: dict) -> dict:
        data = json.dumps(body).encode()
        req = urllib.request.Request(
            f"{self._base}{path}",
            data=data,
            headers=self._headers(),
            method="POST",
        )
        try:
            with urllib.request.urlopen(req, timeout=120) as resp:
                return json.loads(resp.read())
        except urllib.error.HTTPError as e:
            msg = e.read().decode() if e.fp else str(e)
            raise RuntimeError(f"HTTP {e.code}: {msg}") from e

    def _api_get(self, path: str) -> dict:
        return self._request("GET", path)

    def _api_post(self, path: str, body: dict) -> dict:
        return self._request("POST", path, body)

    def _api_delete(self, path: str, body: dict | None = None) -> dict:
        return self._request("DELETE", path, body)

    def reset_onboarding(self, app: str) -> dict:
        """Reset onboarding for the authenticated user of an app."""
        app_id = self._resolve_app_id(app)
        return self._api_delete(f"/app/{app_id}/onboarding/complete", {"reset": True})

    def _get_stream(self, url: str) -> Iterator[StreamChunk]:
        req = urllib.request.Request(url, headers=self._headers())
        with urllib.request.urlopen(req, timeout=120) as resp:
            event = ""
            for raw_line in resp:
                line = raw_line.decode().rstrip("\n")
                if line.startswith("event:"):
                    event = line[6:].strip()
                elif line.startswith("data:"):
                    try:
                        data = json.loads(line[5:].strip())
                    except json.JSONDecodeError:
                        data = {}
                    chunk = StreamChunk(event=event, data=data)
                    yield chunk
                    if chunk.done:
                        return

    def _grpc_client(self):
        from .channel import ServiceClient
        return ServiceClient(self._ctx)

    def list_apps(self) -> list[dict[str, Any]]:
        """List all apps owned by the authenticated workspace."""
        with self._grpc_client() as c:
            from .clients.capsule import ListAppsRequest
            res = c.capsule.list_apps(ListAppsRequest())
            if not res.ok:
                raise RuntimeError(f"list_apps failed: {res.err_msg}")
            return [
                {"id": a.id, "name": a.name, "hostname": a.hostname}
                for a in res.apps
            ]

    def get_app(self, name_or_id: str) -> dict[str, Any]:
        """Get details for a single app by name or ID."""
        app_id = self._resolve_app_id(name_or_id)
        return self._api_get(f"/apps/{app_id}")

    def create_checkout(self, app: str, return_url: str = "") -> str:
        """Create a checkout URL for an app. Returns the Stripe checkout URL."""
        app_id = self._resolve_app_id(app)
        app_data = self._api_get(f"/apps/{app_id}")
        app_info = app_data.get("app", app_data)
        if int(app_info.get("price_in_cents", 0) or 0) <= 0:
            raise RuntimeError("App is free; checkout is only available for paid apps.")
        body: dict[str, Any] = {}
        if return_url:
            body["return_url"] = return_url
        data = self._api_post(f"/checkout/{app_id}", body)
        url = data.get("checkout_url", "")
        if not url:
            raise RuntimeError("No checkout URL returned")
        return url

    def list_payments(self, app: str) -> list[dict[str, Any]]:
        """List payments for an app."""
        app_id = self._resolve_app_id(app)
        return self._api_get(f"/apps/{app_id}/payments")

    def get_earnings(self, app: str) -> dict[str, Any]:
        """Get earnings summary for an app (revenue, fees, developer share)."""
        app_id = self._resolve_app_id(app)
        return self._api_get(f"/apps/{app_id}/earnings")

    def _resolve_app_id(self, name_or_id: str) -> str:
        """Resolve an app name to its UUID, caching results."""
        if len(name_or_id) == 36 and "-" in name_or_id:
            return name_or_id
        if name_or_id in self._app_cache:
            return self._app_cache[name_or_id]
        for app in self.list_apps():
            self._app_cache[app["name"]] = app["id"]
        if name_or_id in self._app_cache:
            return self._app_cache[name_or_id]
        raise ValueError(f"App not found: {name_or_id}")

    def chat(
        self,
        app: str,
        text: str,
        session_id: Optional[str] = None,
    ) -> ChatResponse:
        """Send a message and get a complete response (synchronous)."""
        app_id = self._resolve_app_id(app)
        body: dict[str, Any] = {"text": text}
        if session_id:
            body["session_id"] = session_id
        raw = self._post(f"/api/v1/app/{app_id}/chat", body)
        replies = raw.get("replies", [])
        return ChatResponse(
            text=replies[0]["text"] if replies else "",
            session_id=raw.get("session_id", ""),
            request_id=raw.get("request_id", ""),
            raw=raw,
        )

    def stream(
        self,
        app: str,
        text: str,
        session_id: Optional[str] = None,
    ) -> Iterator[StreamChunk]:
        """Send a message and stream the response via SSE."""
        app_id = self._resolve_app_id(app)
        params = f"text={urllib.request.quote(text)}"
        if session_id:
            params += f"&session_id={urllib.request.quote(session_id)}"
        url = f"{self._base}/api/v1/app/{app_id}/stream?{params}"
        return self._get_stream(url)
