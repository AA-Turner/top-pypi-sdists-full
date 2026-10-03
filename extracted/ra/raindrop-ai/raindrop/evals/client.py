"""Credential-safe Query SDK transport. Evals fail explicitly rather than silently passing."""

from __future__ import annotations

import asyncio
import os
import time
from typing import Any
from urllib.parse import urlsplit

import httpx

DEFAULT_QUERY_URL = "https://query.raindrop.ai"
DEFAULT_REPLAY_INGEST_URL = "https://backend.raindrop.ai/api/replays/ingest/"


class EvalAPIError(RuntimeError):
    def __init__(self, status: int, method: str, path: str, message: str) -> None:
        self.status = status
        super().__init__(f"Raindrop {method} {path}: {status} {message}")


class EvalDatasetPublishConflictError(EvalAPIError):
    pass


class EvalPublishError(EvalAPIError):
    pass


def credential_endpoint(value: str) -> str:
    url = urlsplit(value)
    if not url.hostname or (
        url.scheme != "https"
        and not (
            url.scheme == "http" and url.hostname in ("localhost", "127.0.0.1", "::1")
        )
    ):
        raise ValueError("Raindrop endpoints require HTTPS, except on loopback hosts")
    if url.username or url.password or url.query or url.fragment:
        raise ValueError(
            "Raindrop endpoints cannot contain credentials, a query, or a fragment"
        )
    return value.rstrip("/")


def replay_ingest_endpoint(value: str, trusted_url: str | None = None) -> str:
    value = credential_endpoint(value)
    if trusted_url is None and value == "https://app.raindrop.ai/api/replays/ingest":
        value = DEFAULT_REPLAY_INGEST_URL.rstrip("/")
    if value != credential_endpoint(trusted_url or DEFAULT_REPLAY_INGEST_URL):
        raise ValueError(
            "Replay ingest URL does not match the trusted replay_ingest_url"
        )
    return value + "/v1/traces"


class EvalClient:
    """Query SDK client, separate from the application's telemetry write key."""

    def __init__(
        self,
        api_key: str | None = None,
        *,
        project_id: str | None = None,
        query_url: str = DEFAULT_QUERY_URL,
        replay_ingest_url: str | None = None,
        app_git: bool | dict[str, Any] = True,
    ) -> None:
        from raindrop.app_git import prepare_app_git

        self.app_git_snapshot, self.app_git_plan, _ = prepare_app_git(app_git)
        self.api_key = api_key or os.getenv("RAINDROP_QUERY_API_KEY", "")
        if not self.api_key.strip():
            raise ValueError(
                "Evals require a Query SDK API key (RAINDROP_QUERY_API_KEY)"
            )
        self.project_id = (
            project_id
            if project_id is not None
            else os.getenv("RAINDROP_PROJECT_ID", "default")
        )
        self.query_url = credential_endpoint(query_url)
        self.replay_ingest_url = (
            credential_endpoint(replay_ingest_url) if replay_ingest_url else None
        )

    async def git_fields(self) -> dict[str, Any]:
        from raindrop.app_git import discover_local_git

        if self.app_git_plan is not None:
            discovered = await asyncio.to_thread(discover_local_git, self.app_git_plan)
            if discovered is not None:
                self.app_git_snapshot = discovered
            self.app_git_plan = None
        fields = self.app_git_snapshot.properties
        sha = fields.get("raindrop.app.commit_sha")
        return {
            "commit_sha": sha,
            "commit_dirty": fields.get("raindrop.app.commit_dirty") if sha else None,
            "commit_branch": fields.get("raindrop.app.branch"),
        }

    async def request(
        self,
        method: str,
        path: str,
        *,
        body: Any = None,
        query_url: str | None = None,
        retries: int = 0,
        deadline: float | None = None,
        absolute_url: str | None = None,
        replay_id: str | None = None,
    ) -> Any:
        """Send an authenticated request to an application-configured endpoint.

        URL overrides are trusted configuration, not dataset or user input; they
        receive this client's Query API key. Server-provided replay ingest URLs
        must first pass replay_ingest_endpoint's trusted endpoint check.
        """
        url = (
            credential_endpoint(absolute_url)
            if absolute_url
            else credential_endpoint(query_url or self.query_url) + path
        )
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }
        if self.project_id is not None:
            headers["X-Raindrop-Project-Id"] = self.project_id
        if replay_id:
            headers["X-Raindrop-Replay-Id"] = replay_id
        # Instrumentation must not turn Query API requests into child model traces.
        from opentelemetry.context import attach, detach, set_value
        from opentelemetry.instrumentation.utils import _SUPPRESS_INSTRUMENTATION_KEY

        token = attach(set_value(_SUPPRESS_INSTRUMENTATION_KEY, True))
        try:
            async with httpx.AsyncClient(
                follow_redirects=False, trust_env=False
            ) as session:
                for attempt in range(retries + 1):
                    budget = (
                        30.0
                        if deadline is None
                        else min(30.0, max(0.001, deadline - time.monotonic()))
                    )
                    try:
                        response = await session.request(
                            method, url, headers=headers, json=body, timeout=budget
                        )
                    except httpx.TransportError:
                        if attempt == retries or (
                            deadline is not None and time.monotonic() >= deadline
                        ):
                            raise
                        await asyncio.sleep(min(0.1 * 2**attempt, budget))
                        continue
                    if response.is_success:
                        try:
                            return response.json()
                        except ValueError as error:
                            raise RuntimeError(
                                f"Raindrop {method} {path} returned invalid JSON"
                            ) from error
                    if attempt < retries and (
                        response.status_code in (408, 429)
                        or response.status_code >= 500
                    ):
                        try:
                            delay = min(
                                30.0, max(0, float(response.headers["retry-after"]))
                            )
                        except (KeyError, ValueError):
                            delay = 0.1 * 2**attempt
                        if deadline is not None:
                            delay = min(delay, max(0, deadline - time.monotonic()))
                            if time.monotonic() >= deadline:
                                raise EvalAPIError(
                                    response.status_code,
                                    method,
                                    path,
                                    "Polling deadline exceeded",
                                )
                        await asyncio.sleep(delay)
                        continue
                    error_cls = (
                        EvalDatasetPublishConflictError
                        if response.status_code == 409
                        and path.startswith("/v1/eval-datasets/")
                        else EvalAPIError
                    )
                    # Redact credentials even if an upstream error echoes its request headers.
                    raise error_cls(
                        response.status_code,
                        method,
                        path,
                        response.text.replace(self.api_key, "[redacted]"),
                    )
        finally:
            detach(token)
