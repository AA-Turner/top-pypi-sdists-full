from typing import Optional

from qwak.clients.project.client import ProjectsManagementClient


def execute(
    project_name: str,
    project_description: str,
    jfrog_project_key: Optional[str] = None,
):
    projects_management = ProjectsManagementClient()
    return projects_management.create_project(
        project_name, project_description, jfrog_project_key
    )
