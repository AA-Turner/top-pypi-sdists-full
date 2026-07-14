"""HTTP client for the workflow submission service.

:class:`WorkflowServiceClient` is a small synchronous (httpx) wrapper suitable for
use from the ``plato workflow`` CLI and from orchestrator agent VMs. Endpoint and
token resolution follows the order: explicit args -> ``$WORKFLOW_SERVICE_URL`` /
``$WORKFLOW_SERVICE_TOKEN`` -> the ``.workflow-endpoint.json`` discovery file on
the results mount.

This module lives in ``plato.utils`` (not ``plato.workflows``) so the ``plato``
CLI's import chain never executes ``plato/workflows/__init__.py``: agent VMs get
the SDK installed ``--no-deps`` over base images whose baked dependency set
predates this feature, and the workflows package pulls in ``jsonschema``/world-side
modules that are absent there. Keep this module's imports stdlib + httpx only.
"""

from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any

import httpx

DEFAULT_ENDPOINT_FILE = "/workflow-results/.workflow-endpoint.json"


class WorkflowServiceError(RuntimeError):
    """Raised when the workflow service returns a non-success HTTP status.

    Carries the HTTP ``status_code`` and the decoded JSON ``payload`` (when the
    body was JSON) so callers can surface compile errors (line numbers/excerpts)
    and 409 conflicts cleanly.
    """

    def __init__(self, status_code: int, payload: Any, message: str | None = None) -> None:
        self.status_code = status_code
        self.payload = payload
        detail = message
        if detail is None:
            if isinstance(payload, dict) and payload.get("error"):
                detail = str(payload["error"])
            else:
                detail = str(payload)
        super().__init__(f"HTTP {status_code}: {detail}")


def resolve_endpoint(url: str | None = None, token: str | None = None) -> tuple[str, str | None]:
    """Resolve the service base URL and token.

    Precedence for each of URL and token independently: explicit arg ->
    environment variable -> discovery file. Raises ``ValueError`` if no URL can
    be resolved.
    """
    file_url: str | None = None
    file_token: str | None = None
    endpoint_file = Path(os.getenv("WORKFLOW_ENDPOINT_FILE", DEFAULT_ENDPOINT_FILE))
    if endpoint_file.exists():
        try:
            data = json.loads(endpoint_file.read_text())
        except (json.JSONDecodeError, OSError):
            data = {}
        if isinstance(data, dict):
            file_url = data.get("url")
            file_token = data.get("token")

    resolved_url = url or os.getenv("WORKFLOW_SERVICE_URL") or file_url
    resolved_token = token or os.getenv("WORKFLOW_SERVICE_TOKEN") or file_token
    if not resolved_url:
        raise ValueError(
            f"workflow service URL not found; pass --url, set $WORKFLOW_SERVICE_URL, or provide {endpoint_file}"
        )
    return resolved_url.rstrip("/"), resolved_token


class WorkflowServiceClient:
    """Synchronous client for the workflow submission service."""

    def __init__(self, base_url: str, token: str | None = None, *, timeout: float = 30.0) -> None:
        self.base_url = base_url.rstrip("/")
        self.token = token
        headers = {"Authorization": f"Bearer {token}"} if token else {}
        # retries=5 retries CONNECT failures only (never a sent request), with
        # exponential backoff — agent->world mesh connects flake under cluster
        # load, and a bare ConnectTimeout traceback strands the orchestrator.
        transport = httpx.HTTPTransport(retries=5)
        self._http = httpx.Client(base_url=self.base_url, headers=headers, timeout=timeout, transport=transport)

    # ------------------------------------------------------------------ helpers

    @classmethod
    def from_env(
        cls, url: str | None = None, token: str | None = None, *, timeout: float = 30.0
    ) -> WorkflowServiceClient:
        """Construct a client using :func:`resolve_endpoint`."""
        resolved_url, resolved_token = resolve_endpoint(url, token)
        return cls(resolved_url, resolved_token, timeout=timeout)

    def _decode(self, response: httpx.Response) -> Any:
        try:
            return response.json()
        except (json.JSONDecodeError, ValueError):
            return response.text

    def _handle(self, response: httpx.Response, *, ok_202: bool = False) -> Any:
        if response.status_code < 400:
            return self._decode(response)
        if ok_202 and response.status_code == 202:
            return self._decode(response)
        raise WorkflowServiceError(response.status_code, self._decode(response))

    # ------------------------------------------------------------------ verbs

    def submit(
        self,
        script: str,
        *,
        args: Any = None,
        name: str | None = None,
        budget_usd: float | None = None,
        workflow_id: str | None = None,
    ) -> dict[str, Any]:
        """Submit a workflow script. Raises :class:`WorkflowServiceError` on 422/409."""
        body: dict[str, Any] = {"script": script}
        if args is not None:
            body["args"] = args
        if name is not None:
            body["name"] = name
        if budget_usd is not None:
            body["budget_usd"] = budget_usd
        if workflow_id is not None:
            body["workflow_id"] = workflow_id
        response = self._http.post("/workflows", json=body)
        return self._handle(response)

    def status(self, workflow_id: str) -> dict[str, Any]:
        response = self._http.get(f"/workflows/{workflow_id}")
        return self._handle(response)

    def result(self, workflow_id: str) -> dict[str, Any]:
        """Fetch the result. While running/queued the body carries ``{"status": ...}``."""
        response = self._http.get(f"/workflows/{workflow_id}/result")
        return self._handle(response, ok_202=True)

    def events(self, workflow_id: str, after_seq: int = -1) -> dict[str, Any]:
        """Page journal events with ``seq > after_seq`` (``-1`` = from the beginning)."""
        response = self._http.get(f"/workflows/{workflow_id}/events", params={"after_seq": after_seq})
        return self._handle(response)

    def cancel(self, workflow_id: str) -> dict[str, Any]:
        response = self._http.post(f"/workflows/{workflow_id}/cancel")
        return self._handle(response)

    def healthz(self) -> dict[str, Any]:
        response = self._http.get("/healthz")
        return self._handle(response)

    def close(self) -> None:
        self._http.close()

    def __enter__(self) -> WorkflowServiceClient:
        return self

    def __exit__(self, *exc: object) -> None:
        self.close()
