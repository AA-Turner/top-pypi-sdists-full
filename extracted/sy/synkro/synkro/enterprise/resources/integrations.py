"""Integrations resource — LangSmith and other external service connections."""

from __future__ import annotations

from typing import TYPE_CHECKING

from synkro.enterprise.types import DatasetCreateResult, LangSmithConnection

if TYPE_CHECKING:
    from synkro.enterprise._http import AsyncBaseHTTPClient, BaseHTTPClient


class Integrations:
    """Sync integration operations."""

    def __init__(self, http: BaseHTTPClient):
        self._http = http

    def langsmith_status(self) -> LangSmithConnection:
        """GET /api/integrations/langsmith"""
        data = self._http.get("/api/integrations/langsmith")
        return LangSmithConnection(**data)

    def connect_langsmith(
        self,
        *,
        api_key: str,
        base_url: str = "https://api.smith.langchain.com",
    ) -> LangSmithConnection:
        """POST /api/integrations/langsmith"""
        data = self._http.post(
            "/api/integrations/langsmith",
            json={"api_key": api_key, "base_url": base_url},
        )
        return LangSmithConnection(**data)

    def disconnect_langsmith(self) -> None:
        """DELETE /api/integrations/langsmith"""
        self._http.delete("/api/integrations/langsmith")

    def langsmith_projects(self) -> list[dict]:
        """GET /api/integrations/langsmith/projects"""
        return self._http.get("/api/integrations/langsmith/projects")

    def langsmith_toggle(
        self,
        project_id: str,
        *,
        enabled: bool,
        langsmith_project: str | None = None,
    ) -> None:
        """POST /api/integrations/langsmith/toggle"""
        body: dict = {"project_id": project_id, "enabled": enabled}
        if langsmith_project is not None:
            body["langsmith_project"] = langsmith_project
        self._http.post("/api/integrations/langsmith/toggle", json=body)

    def langsmith_create_dataset(
        self,
        *,
        name: str,
        traces: list[dict] | None = None,
        description: str | None = None,
    ) -> DatasetCreateResult:
        """POST /api/integrations/langsmith/datasets"""
        body: dict = {"name": name}
        if traces is not None:
            body["traces"] = traces
        if description is not None:
            body["description"] = description
        data = self._http.post("/api/integrations/langsmith/datasets", json=body)
        return DatasetCreateResult(**data)


class AsyncIntegrations:
    """Async integration operations."""

    def __init__(self, http: AsyncBaseHTTPClient):
        self._http = http

    async def langsmith_status(self) -> LangSmithConnection:
        """GET /api/integrations/langsmith"""
        data = await self._http.get("/api/integrations/langsmith")
        return LangSmithConnection(**data)

    async def connect_langsmith(
        self,
        *,
        api_key: str,
        base_url: str = "https://api.smith.langchain.com",
    ) -> LangSmithConnection:
        """POST /api/integrations/langsmith"""
        data = await self._http.post(
            "/api/integrations/langsmith",
            json={"api_key": api_key, "base_url": base_url},
        )
        return LangSmithConnection(**data)

    async def disconnect_langsmith(self) -> None:
        """DELETE /api/integrations/langsmith"""
        await self._http.delete("/api/integrations/langsmith")

    async def langsmith_projects(self) -> list[dict]:
        """GET /api/integrations/langsmith/projects"""
        return await self._http.get("/api/integrations/langsmith/projects")

    async def langsmith_toggle(
        self,
        project_id: str,
        *,
        enabled: bool,
        langsmith_project: str | None = None,
    ) -> None:
        """POST /api/integrations/langsmith/toggle"""
        body: dict = {"project_id": project_id, "enabled": enabled}
        if langsmith_project is not None:
            body["langsmith_project"] = langsmith_project
        await self._http.post("/api/integrations/langsmith/toggle", json=body)

    async def langsmith_create_dataset(
        self,
        *,
        name: str,
        traces: list[dict] | None = None,
        description: str | None = None,
    ) -> DatasetCreateResult:
        """POST /api/integrations/langsmith/datasets"""
        body: dict = {"name": name}
        if traces is not None:
            body["traces"] = traces
        if description is not None:
            body["description"] = description
        data = await self._http.post("/api/integrations/langsmith/datasets", json=body)
        return DatasetCreateResult(**data)
