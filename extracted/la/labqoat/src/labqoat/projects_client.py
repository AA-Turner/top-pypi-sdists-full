"""Typed management of the projects that own runs, datasets, dashboards and one memory."""

from labqoat._generated.project import Project
from labqoat._generated.project_attributes import ProjectAttributes
from labqoat._generated.project_budget import ProjectBudget
from labqoat._generated.project_budget_limits import ProjectBudgetLimits
from labqoat._generated.project_list import ProjectList
from labqoat._generated.project_move import ProjectMove
from labqoat._generated.project_move_result import ProjectMoveResult
from labqoat.base_client import BaseClient
from labqoat.errors.api_error import ApiError


class ProjectsClient(BaseClient):
    """Address projects by name; the client's own selected project only scopes ``ProjectMove.apps``."""

    def list(self, archived: bool = False) -> ProjectList:
        """List the active projects of the client's environment with what each owns, or the archived ones instead."""
        path = "/api/v1/projects?archived=true" if archived else "/api/v1/projects"
        return self.decode(self.send("GET", path), path, ProjectList.from_dict)

    def get(self, name: str) -> Project:
        """Read one project with its objectives and apps; a project nothing was written to does not exist yet."""
        path = f"/api/v1/projects/{self.encode_ref(name)}"
        return self.decode(self.send("GET", path), path, Project.from_dict)

    def put(self, name: str, attributes: ProjectAttributes | None = None) -> Project:
        """Create the project when missing and apply the given attributes; repeating the call is safe."""
        path = f"/api/v1/projects/{self.encode_ref(name)}"
        response = self.send_json("PUT", path, (attributes or ProjectAttributes()).to_dict())
        return self.decode(response, path, Project.from_dict)

    def budget(self, name: str) -> ProjectBudget:
        """Read what the project spent against its money and time budgets, with hints to spend more or less."""
        path = f"/api/v1/projects/{self.encode_ref(name)}/budget"
        return self.decode(self.send("GET", path), path, ProjectBudget.from_dict)

    def put_budget(self, name: str, limits: ProjectBudgetLimits | None = None) -> ProjectBudget:
        """Create the project when missing and replace its whole budget; no limits removes the budget."""
        path = f"/api/v1/projects/{self.encode_ref(name)}/budget"
        response = self.send_json("PUT", path, (limits or ProjectBudgetLimits()).to_dict())
        return self.decode(response, path, ProjectBudget.from_dict)

    def delete(self, name: str) -> None:
        """Remove a project that no longer owns runs, datasets or dashboards."""
        path = f"/api/v1/projects/{self.encode_ref(name)}"
        response = self.send("DELETE", path)
        if response.status_code != 204 or response.content:
            raise ApiError("Expected an empty deletion response.", status=response.status_code)

    def archive(self, name: str) -> Project:
        """Hide a project from listings and navigation and cancel its active runs; what it owns stays readable."""
        path = f"/api/v1/projects/{self.encode_ref(name)}/archive"
        return self.decode(self.send("POST", path), path, Project.from_dict)

    def unarchive(self, name: str) -> Project:
        """Return an archived project to listings and navigation."""
        path = f"/api/v1/projects/{self.encode_ref(name)}/unarchive"
        return self.decode(self.send("POST", path), path, Project.from_dict)

    def move(self, name: str, selection: ProjectMove) -> ProjectMoveResult:
        """Move existing runs, apps, dashboards and datasets into the named project, creating it when missing."""
        path = f"/api/v1/projects/{self.encode_ref(name)}/moves"
        return self.decode(self.send_json("POST", path, selection.to_dict()), path, ProjectMoveResult.from_dict)
