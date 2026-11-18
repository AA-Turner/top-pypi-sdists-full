"""ProjectDetailsMixin, Client's methods: what a project or experiment page shows beside its row -- the data it
uses and makes, its README, the workspaces it sits in, its subtree, its synced Google Docs, where its metric points
live, and its visuals (twins: app/projects/api, app/files/catalog, app/integrations)."""

from __future__ import annotations

from typing import Any

from ......generated.models import (
    GoogleDocList,
    ProjectPointsStoreOut,
    ProjectReadmeOut,
    ProjectSubtreeOut,
    ProjectWorkspacesOut,
    WorkspaceVisualsOut,
)


class ProjectDetailsMixin:
    """Part of Client: its methods run with `self` the Client; compose() folds them into Client."""

    def get_project_data(self, project_id: str) -> dict:
        """``GET /v1/projects/{id}/data``: the datasets and checkpoints a project's runs use and make."""
        return self.transport.get(f"/v1/projects/{project_id}/data")

    def get_experiment_data(self, experiment_id: str, *, project_id: str | None = None) -> dict:
        """``GET /v1/projects/{P}/experiments/{E}/data``: the datasets and checkpoints an experiment's runs use."""
        return self._on_experiment(
            lambda p, e: self.transport.get(f"/v1/projects/{p}/experiments/{e}/data"), experiment_id, project_id
        )

    def get_project_readme(self, project_id: str) -> dict:
        """``GET /v1/projects/{id}/readme``: the README of the repo a project points at (`markdown` + source)."""
        return self.transport.get(f"/v1/projects/{project_id}/readme")

    def get_experiment_readme(self, experiment_id: str, *, project_id: str | None = None) -> dict:
        """``GET /v1/projects/{P}/experiments/{E}/readme``: the README of the repo an experiment points at."""
        return self._on_experiment(
            lambda p, e: self.transport.get(f"/v1/projects/{p}/experiments/{e}/readme"), experiment_id, project_id
        )

    def list_project_workspaces(self, project_id: str) -> dict:
        """``GET /v1/projects/{id}/workspaces``: the workspaces a project is in."""
        return self.transport.get(f"/v1/projects/{project_id}/workspaces")

    def get_project_subtree(self, project_id: str) -> dict:
        """``GET /v1/projects/{id}/subtree``: every project and experiment filed under a project, in one read."""
        return self.transport.get(f"/v1/projects/{project_id}/subtree")

    def list_project_google_docs(self, project_id: str) -> dict:
        """``GET /v1/projects/{id}/google-docs``: the Google Docs synced into a project, and how each sync stands."""
        return self.transport.get(f"/v1/projects/{project_id}/google-docs")

    def get_project_points_store(self, project_id: str) -> dict:
        """``GET /v1/projects/{id}/points-store``: where a project's metric points live (`postgres` | `clickhouse`)."""
        return self.transport.get(f"/v1/projects/{project_id}/points-store")

    def list_project_visuals(
        self, project_id: str, *, scope: str | None = None, cursor: str | None = None, limit: int | None = None
    ) -> dict:
        """``GET /v1/projects/{id}/workspace/visuals``: the images and charts filed in a project, a page at a time."""
        filters: dict[str, Any] = {
            key: value for key, value in {"scope": scope, "cursor": cursor, "limit": limit}.items() if value is not None
        }
        return self.transport.get(f"/v1/projects/{project_id}/workspace/visuals", params=filters or None)


class ProjectDetailsReads:
    """`client.projects`' typed detail reads; `ProjectsResource` takes them in."""

    __slots__ = ()

    def get_readme(self, project_id: str) -> ProjectReadmeOut:
        """`Client.get_project_readme` as a `ProjectReadmeOut`."""
        return self._to_model(ProjectReadmeOut, self._client.get_project_readme(project_id))

    def list_workspaces(self, project_id: str) -> ProjectWorkspacesOut:
        """`Client.list_project_workspaces` as a `ProjectWorkspacesOut`."""
        return self._to_model(ProjectWorkspacesOut, self._client.list_project_workspaces(project_id))

    def get_subtree(self, project_id: str) -> ProjectSubtreeOut:
        """`Client.get_project_subtree` as a `ProjectSubtreeOut`."""
        return self._to_model(ProjectSubtreeOut, self._client.get_project_subtree(project_id))

    def list_google_docs(self, project_id: str) -> GoogleDocList:
        """`Client.list_project_google_docs` as a `GoogleDocList`."""
        return self._to_model(GoogleDocList, self._client.list_project_google_docs(project_id))

    def get_points_store(self, project_id: str) -> ProjectPointsStoreOut:
        """`Client.get_project_points_store` as a `ProjectPointsStoreOut`."""
        return self._to_model(ProjectPointsStoreOut, self._client.get_project_points_store(project_id))

    def list_visuals(
        self, project_id: str, *, scope: str | None = None, cursor: str | None = None, limit: int | None = None
    ) -> WorkspaceVisualsOut:
        """`Client.list_project_visuals` as a `WorkspaceVisualsOut`."""
        return self._to_model(WorkspaceVisualsOut, self._client.list_project_visuals(
            project_id, scope=scope, cursor=cursor, limit=limit))
