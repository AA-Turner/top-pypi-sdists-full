"""Publish adapters for workflow output steps (#966).

Each adapter delivers content to a specific destination type.
V1 ships with file (local filesystem) and webhook (HTTP POST).
"""

from __future__ import annotations

import logging
from pathlib import Path
from typing import Any, Protocol

logger = logging.getLogger(__name__)


class PublishAdapter(Protocol):
    async def publish(
        self,
        content: str,
        destination: dict[str, Any],
        credentials: dict[str, str] | None = None,
        idempotency_key: str | None = None,
    ) -> Any: ...


class FilePublishAdapter:
    async def publish(
        self,
        content: str,
        destination: dict[str, Any],
        credentials: dict[str, str] | None = None,
        idempotency_key: str | None = None,
    ) -> Any:
        from .workflow_runners import RunnerResult

        path_str = destination.get("path", "")
        if not path_str:
            return RunnerResult(status="failed", summary="No path specified", duration_ms=0)

        # Path security: block sensitive system paths
        from ..tools.security import validate_path

        resolved, error = validate_path(path_str, str(Path.cwd()))
        if error:
            return RunnerResult(status="failed", summary=f"Path blocked: {error}", duration_ms=0)

        path = Path(resolved)
        try:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content, encoding="utf-8")
            bytes_written = len(content.encode("utf-8"))
            return RunnerResult(
                status="success",
                summary=f"Published to {path_str}",
                artifacts={"destination": f"file:{path_str}", "bytes_written": bytes_written},
                duration_ms=0,
            )
        except Exception as exc:
            return RunnerResult(status="failed", summary=f"File write failed: {exc}", duration_ms=0)


class WebhookPublishAdapter:
    async def publish(
        self,
        content: str,
        destination: dict[str, Any],
        credentials: dict[str, str] | None = None,
        idempotency_key: str | None = None,
    ) -> Any:
        from .workflow_runners import RunnerResult

        url = destination.get("url", "")
        if not url:
            return RunnerResult(status="failed", summary="No URL specified", duration_ms=0)

        method = destination.get("method", "POST").upper()
        headers = dict(destination.get("headers", {}))

        if credentials:
            for key, val in credentials.items():
                headers[f"X-{key}"] = val

        if idempotency_key:
            headers["Idempotency-Key"] = idempotency_key

        body_template = destination.get("body_template")
        if body_template:
            body = body_template.replace("{content}", content)
        else:
            body = content

        if len(body.encode("utf-8")) > 1_048_576:
            return RunnerResult(status="failed", summary="Payload exceeds 1MB limit", duration_ms=0)

        try:
            import httpx

            async with httpx.AsyncClient(timeout=30.0) as client:
                if headers.get("Content-Type", "").startswith("application/json"):
                    import json

                    try:
                        json_body = json.loads(body)
                        resp = await client.request(method, url, json=json_body, headers=headers)
                    except json.JSONDecodeError:
                        resp = await client.request(method, url, content=body.encode(), headers=headers)
                else:
                    resp = await client.request(method, url, content=body.encode(), headers=headers)

                if resp.status_code >= 400:
                    return RunnerResult(
                        status="failed",
                        summary=f"HTTP {resp.status_code} from {url}",
                        artifacts={"destination": f"webhook:{url}", "status_code": resp.status_code},
                        duration_ms=0,
                    )
                return RunnerResult(
                    status="success",
                    summary=f"Published to {url} (HTTP {resp.status_code})",
                    artifacts={"destination": f"webhook:{url}", "status_code": resp.status_code},
                    duration_ms=0,
                )
        except Exception as exc:
            return RunnerResult(status="failed", summary=f"Webhook failed: {exc}", duration_ms=0)


class PublisherRegistry:
    def __init__(self) -> None:
        self._adapters: dict[str, PublishAdapter] = {}

    def register(self, name: str, adapter: PublishAdapter) -> None:
        self._adapters[name] = adapter

    def get(self, name: str) -> PublishAdapter | None:
        return self._adapters.get(name)


def create_default_publisher_registry() -> PublisherRegistry:
    registry = PublisherRegistry()
    registry.register("file", FilePublishAdapter())
    registry.register("webhook", WebhookPublishAdapter())
    return registry
