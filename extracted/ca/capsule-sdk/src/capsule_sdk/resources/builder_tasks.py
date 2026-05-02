from __future__ import annotations

from typing import Literal

from capsule_sdk._http import HttpClient
from capsule_sdk.models.builder_tasks import BuilderTasksResponse


class BuilderTasks:
    def __init__(self, http: HttpClient, *, tenant_id: str) -> None:
        self._http = http
        self._tenant_id = tenant_id

    def poll(self, kind: Literal["new", "refresh"]) -> BuilderTasksResponse:
        path = f"/api/v1/tenant/{self._tenant_id}/builder-tasks"
        data = self._http.get(path, params={"kind": kind})
        return BuilderTasksResponse.model_validate(data)
