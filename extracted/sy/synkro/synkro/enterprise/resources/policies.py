"""Policies resource — CRUD operations for project policies."""

from __future__ import annotations

import os
import time
from typing import TYPE_CHECKING

import httpx

from synkro.enterprise.errors import SynkroError
from synkro.enterprise.types import Policy, PolicyCreateResult

if TYPE_CHECKING:
    from synkro.enterprise._http import AsyncBaseHTTPClient, BaseHTTPClient

_POLL_INTERVAL = 2.0
_POLL_TIMEOUT = 120.0


def _inngest_url() -> str:
    return os.environ.get("INNGEST_URL", "http://localhost:8288")


def _poll_extraction_sync(event_id: str) -> None:
    """Block until Inngest extraction run completes."""
    url = f"{_inngest_url()}/v1/events/{event_id}/runs"
    deadline = time.monotonic() + _POLL_TIMEOUT

    while time.monotonic() < deadline:
        resp = httpx.get(url, timeout=10.0)
        if resp.is_success:
            runs = resp.json().get("data", [])
            if runs:
                status = runs[0].get("status")
                if status == "Completed":
                    return
                if status == "Failed":
                    raise SynkroError("Policy extraction failed")
        time.sleep(_POLL_INTERVAL)

    raise SynkroError(f"Policy extraction timed out after {_POLL_TIMEOUT}s")


async def _poll_extraction_async(event_id: str) -> None:
    """Block until Inngest extraction run completes (async)."""
    import asyncio

    url = f"{_inngest_url()}/v1/events/{event_id}/runs"
    deadline = time.monotonic() + _POLL_TIMEOUT

    async with httpx.AsyncClient(timeout=10.0) as client:
        while time.monotonic() < deadline:
            resp = await client.get(url)
            if resp.is_success:
                runs = resp.json().get("data", [])
                if runs:
                    status = runs[0].get("status")
                    if status == "Completed":
                        return
                    if status == "Failed":
                        raise SynkroError("Policy extraction failed")
            await asyncio.sleep(_POLL_INTERVAL)

    raise SynkroError(f"Policy extraction timed out after {_POLL_TIMEOUT}s")


def _build_result(policy_id: str, policies: list[dict]) -> PolicyCreateResult:
    """Find the extracted policy and build a result."""
    policy = next((p for p in policies if p.get("id") == policy_id), None)
    if policy is None:
        raise SynkroError(f"Policy {policy_id} not found after extraction")
    return PolicyCreateResult(
        ok=True,
        policy_id=policy_id,
        status="ready",
        rules=policy.get("rules", []),
        rule_count=policy.get("rule_count", 0),
    )


class Policies:
    """Sync policy operations."""

    def __init__(self, http: BaseHTTPClient):
        self._http = http

    def list(self, project_id: str) -> list[Policy]:
        """GET /api/projects/{project_id}/policies"""
        data = self._http.get(f"/api/projects/{project_id}/policies")
        return [Policy(**p) for p in data]

    def create(
        self,
        project_id: str,
        *,
        text: str,
        name: str | None = None,
        score_threshold: float | None = None,
        model: str | None = None,
    ) -> PolicyCreateResult:
        """POST /api/projects/{project_id}/policies

        Blocks until rule extraction completes. If the server returns 202
        (async extraction), polls Inngest until the run finishes, then
        fetches the fully populated policy.
        """
        body: dict = {"policy_text": text}
        if name is not None:
            body["name"] = name
        if score_threshold is not None:
            body["score_threshold"] = score_threshold
        if model is not None:
            body["model"] = model
        data = self._http.post(f"/api/projects/{project_id}/policies", json=body)

        if data.get("status") == "extracting" and data.get("event_id"):
            _poll_extraction_sync(data["event_id"])
            policies = self._http.get(f"/api/projects/{project_id}/policies")
            return _build_result(data["policy_id"], policies)

        return PolicyCreateResult(**data)

    def update(
        self,
        project_id: str,
        policy_id: str,
        *,
        name: str | None = None,
        text: str | None = None,
        rule_updates: list[dict] | None = None,
        score_threshold: float | None = None,
        is_active: bool | None = None,
    ) -> None:
        """PATCH /api/projects/{project_id}/policies"""
        body: dict = {"policy_id": policy_id}
        if name is not None:
            body["name"] = name
        if text is not None:
            body["policy_text"] = text
        if rule_updates is not None:
            body["rule_updates"] = rule_updates
        if score_threshold is not None:
            body["score_threshold"] = score_threshold
        if is_active is not None:
            body["is_active"] = is_active
        self._http.patch(f"/api/projects/{project_id}/policies", json=body)

    def deactivate(self, project_id: str, policy_id: str) -> None:
        """DELETE /api/projects/{project_id}/policies?policy_id={policy_id}"""
        self._http.delete(f"/api/projects/{project_id}/policies", params={"policy_id": policy_id})


class AsyncPolicies:
    """Async policy operations."""

    def __init__(self, http: AsyncBaseHTTPClient):
        self._http = http

    async def list(self, project_id: str) -> list[Policy]:
        """GET /api/projects/{project_id}/policies"""
        data = await self._http.get(f"/api/projects/{project_id}/policies")
        return [Policy(**p) for p in data]

    async def create(
        self,
        project_id: str,
        *,
        text: str,
        name: str | None = None,
        score_threshold: float | None = None,
        model: str | None = None,
    ) -> PolicyCreateResult:
        """POST /api/projects/{project_id}/policies

        Blocks until rule extraction completes. If the server returns 202
        (async extraction), polls Inngest until the run finishes, then
        fetches the fully populated policy.
        """
        body: dict = {"policy_text": text}
        if name is not None:
            body["name"] = name
        if score_threshold is not None:
            body["score_threshold"] = score_threshold
        if model is not None:
            body["model"] = model
        data = await self._http.post(f"/api/projects/{project_id}/policies", json=body)

        if data.get("status") == "extracting" and data.get("event_id"):
            await _poll_extraction_async(data["event_id"])
            policies = await self._http.get(f"/api/projects/{project_id}/policies")
            return _build_result(data["policy_id"], policies)

        return PolicyCreateResult(**data)

    async def update(
        self,
        project_id: str,
        policy_id: str,
        *,
        name: str | None = None,
        text: str | None = None,
        rule_updates: list[dict] | None = None,
        score_threshold: float | None = None,
        is_active: bool | None = None,
    ) -> None:
        """PATCH /api/projects/{project_id}/policies"""
        body: dict = {"policy_id": policy_id}
        if name is not None:
            body["name"] = name
        if text is not None:
            body["policy_text"] = text
        if rule_updates is not None:
            body["rule_updates"] = rule_updates
        if score_threshold is not None:
            body["score_threshold"] = score_threshold
        if is_active is not None:
            body["is_active"] = is_active
        await self._http.patch(f"/api/projects/{project_id}/policies", json=body)

    async def deactivate(self, project_id: str, policy_id: str) -> None:
        """DELETE /api/projects/{project_id}/policies?policy_id={policy_id}"""
        await self._http.delete(
            f"/api/projects/{project_id}/policies", params={"policy_id": policy_id}
        )
