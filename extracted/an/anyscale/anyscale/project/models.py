from dataclasses import dataclass, field
from typing import Any, Dict, List

from anyscale._private.models import ModelBase, ModelEnum


class ProjectPermissionLevel(ModelEnum):
    OWNER = "OWNER"
    WRITE = "WRITE"
    READONLY = "READONLY"

    __docstrings__ = {
        OWNER: "Owner permission level for the project",
        WRITE: "Write permission level for the project",
        READONLY: "Readonly permission level for the project",
    }


@dataclass(frozen=True)
class CreateProjectCollaborator(ModelBase):
    """User to be added as a collaborator to a project.
    """

    __doc_py_example__ = """\
import anyscale
from anyscale.project.models import ProjectPermissionLevel, CreateProjectCollaborator
create_project_collaborator = CreateProjectCollaborator(
   # Email of the user to be added as a collaborator
    email="test@anyscale.com",
    # Permission level for the user to the project (ProjectPermissionLevel.OWNER, ProjectPermissionLevel.WRITE, ProjectPermissionLevel.READONLY)
    permission_level=ProjectPermissionLevel.READONLY,
)
"""

    def _validate_email(self, email: str):
        if not isinstance(email, str):
            raise TypeError("Email must be a string.")

    email: str = field(
        metadata={"docstring": "Email of the user to be added as a collaborator."},
    )

    def _validate_permission_level(
        self, permission_level: ProjectPermissionLevel
    ) -> ProjectPermissionLevel:
        if isinstance(permission_level, str):
            return ProjectPermissionLevel.validate(permission_level)
        elif isinstance(permission_level, ProjectPermissionLevel):
            return permission_level
        else:
            raise TypeError(
                f"'permission_level' must be a 'ProjectPermissionLevel' (it is {type(permission_level)})."
            )

    permission_level: ProjectPermissionLevel = field(  # type: ignore
        default=ProjectPermissionLevel.READONLY,  # type: ignore
        metadata={
            "docstring": "Permission level the added user should have for the project"  # type: ignore
            f"(one of: {','.join([str(m.value) for m in ProjectPermissionLevel])}",  # type: ignore
        },
    )


@dataclass(frozen=True)
class CreateProjectCollaborators(ModelBase):
    """List of users to be added as collaborators to a project.
    """

    __doc_py_example__ = """\
import anyscale
from anyscale.project.models import ProjectPermissionLevel, CreateProjectCollaborator, CreateProjectCollaborators
create_project_collaborator = CreateProjectCollaborator(
   # Email of the user to be added as a collaborator
    email="test@anyscale.com",
    # Permission level for the user to the project (ProjectPermissionLevel.OWNER, ProjectPermissionLevel.WRITE, ProjectPermissionLevel.READONLY)
    permission_level=ProjectPermissionLevel.READONLY,
)
create_project_collaborators = CreateProjectCollaborators(
    collaborators=[create_project_collaborator]
)
"""

    collaborators: List[Dict[str, Any]] = field(
        metadata={
            "docstring": "List of users to be added as collaborators to a project."
        },
    )

    def _validate_collaborators(self, collaborators: List[Dict[str, Any]]):
        if not isinstance(collaborators, list):
            raise TypeError("Collaborators must be a list.")
