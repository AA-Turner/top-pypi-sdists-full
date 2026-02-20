"""Projects resource — CRUD operations for Synkro projects."""

from __future__ import annotations

from typing import TYPE_CHECKING

from synkro.enterprise.types import Project, ProjectStatus

if TYPE_CHECKING:
    from synkro.enterprise._http import AsyncBaseHTTPClient, BaseHTTPClient


class Projects:
    """Sync project operations."""

    def __init__(self, http: BaseHTTPClient):
        self._http = http

    def list(self) -> list[Project]:
        """GET /api/projects"""
        data = self._http.get("/api/projects")
        return [Project(**p) for p in data]

    def create(self, *, name: str = "Default Project", provider: str | None = None) -> Project:
        """POST /api/projects"""
        body: dict = {"name": name}
        if provider is not None:
            body["provider"] = provider
        data = self._http.post("/api/projects", json=body)
        return Project(**data)

    def get(self, project_id: str) -> Project:
        """GET /api/projects/{project_id}"""
        data = self._http.get(f"/api/projects/{project_id}")
        return Project(**data)

    def update(
        self,
        project_id: str,
        *,
        name: str | None = None,
        provider: str | None = None,
        langsmith_project: str | None = None,
        is_active: bool | None = None,
    ) -> None:
        """PATCH /api/projects/{project_id}"""
        body: dict = {}
        if name is not None:
            body["name"] = name
        if provider is not None:
            body["provider"] = provider
        if langsmith_project is not None:
            body["langsmith_project"] = langsmith_project
        if is_active is not None:
            body["is_active"] = is_active
        self._http.patch(f"/api/projects/{project_id}", json=body)

    def delete(self, project_id: str) -> None:
        """DELETE /api/projects/{project_id}"""
        self._http.delete(f"/api/projects/{project_id}")

    def status(self, project_id: str) -> ProjectStatus:
        """GET /api/projects/{project_id}/status"""
        data = self._http.get(f"/api/projects/{project_id}/status")
        return ProjectStatus(**data)

    def rotate_slug(self, project_id: str) -> str:
        """POST /api/projects/{project_id}/rotate-slug — returns the new slug."""
        data = self._http.post(f"/api/projects/{project_id}/rotate-slug")
        return data["slug"]


class AsyncProjects:
    """Async project operations."""

    def __init__(self, http: AsyncBaseHTTPClient):
        self._http = http

    async def list(self) -> list[Project]:
        """GET /api/projects"""
        data = await self._http.get("/api/projects")
        return [Project(**p) for p in data]

    async def create(
        self, *, name: str = "Default Project", provider: str | None = None
    ) -> Project:
        """POST /api/projects"""
        body: dict = {"name": name}
        if provider is not None:
            body["provider"] = provider
        data = await self._http.post("/api/projects", json=body)
        return Project(**data)

    async def get(self, project_id: str) -> Project:
        """GET /api/projects/{project_id}"""
        data = await self._http.get(f"/api/projects/{project_id}")
        return Project(**data)

    async def update(
        self,
        project_id: str,
        *,
        name: str | None = None,
        provider: str | None = None,
        langsmith_project: str | None = None,
        is_active: bool | None = None,
    ) -> None:
        """PATCH /api/projects/{project_id}"""
        body: dict = {}
        if name is not None:
            body["name"] = name
        if provider is not None:
            body["provider"] = provider
        if langsmith_project is not None:
            body["langsmith_project"] = langsmith_project
        if is_active is not None:
            body["is_active"] = is_active
        await self._http.patch(f"/api/projects/{project_id}", json=body)

    async def delete(self, project_id: str) -> None:
        """DELETE /api/projects/{project_id}"""
        await self._http.delete(f"/api/projects/{project_id}")

    async def status(self, project_id: str) -> ProjectStatus:
        """GET /api/projects/{project_id}/status"""
        data = await self._http.get(f"/api/projects/{project_id}/status")
        return ProjectStatus(**data)

    async def rotate_slug(self, project_id: str) -> str:
        """POST /api/projects/{project_id}/rotate-slug — returns the new slug."""
        data = await self._http.post(f"/api/projects/{project_id}/rotate-slug")
        return data["slug"]
