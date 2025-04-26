from typing import List

from anyscale._private.sdk.base_sdk import BaseSDK
from anyscale.client.openapi_client import (
    CreateUserProjectCollaborator,
    CreateUserProjectCollaboratorValue,
)
from anyscale.project.models import CreateProjectCollaborator


class PrivateProjectSDK(BaseSDK):
    def add_collaborators(
        self, cloud: str, project: str, collaborators: List[CreateProjectCollaborator]
    ) -> None:
        cloud_id = self.client.get_cloud_id(cloud_name=cloud, compute_config_id=None)
        project_id = self.client.get_project_id(parent_cloud_id=cloud_id, name=project)

        self.client.add_project_collaborators(
            project_id=project_id,
            collaborators=[
                CreateUserProjectCollaborator(
                    value=CreateUserProjectCollaboratorValue(email=collaborator.email),
                    permission_level=collaborator.permission_level.lower(),
                )
                for collaborator in collaborators
            ],
        )
