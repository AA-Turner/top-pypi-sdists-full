from typing import List, Optional

from anyscale._private.sdk import sdk_command
from anyscale.project._private.project_sdk import PrivateProjectSDK
from anyscale.project.models import CreateProjectCollaborator


_PROJECT_SDK_SINGLETON_KEY = "project_sdk"

_ADD_COLLABORATORS_EXAMPLE = """
import anyscale
from anyscale.project.models import CreateProjectCollaborator, ProjectPermissionLevel

anyscale.project.add_collaborators(
    cloud="cloud_name",
    project="project_name",
    collaborators=[
        CreateProjectCollaborator(
            email="test1@anyscale.com",
            permission_level=ProjectPermissionLevel.OWNER,
        ),
        CreateProjectCollaborator(
            email="test2@anyscale.com",
            permission_level=ProjectPermissionLevel.WRITE,
        ),
        CreateProjectCollaborator(
            email="test3@anyscale.com",
            permission_level=ProjectPermissionLevel.READONLY,
        ),
    ],
)
"""

_ADD_COLLABORATORS_DOCSTRINGS = {
    "cloud": "The cloud that the project belongs to.",
    "project": "The project to add users to.",
    "collaborators": "The list of collaborators to add to the project.",
}


@sdk_command(
    _PROJECT_SDK_SINGLETON_KEY,
    PrivateProjectSDK,
    doc_py_example=_ADD_COLLABORATORS_EXAMPLE,
    arg_docstrings=_ADD_COLLABORATORS_DOCSTRINGS,
)
def add_collaborators(
    cloud: str,
    project: str,
    collaborators: List[CreateProjectCollaborator],
    *,
    _private_sdk: Optional[PrivateProjectSDK] = None
) -> str:
    """Batch add collaborators to a project.
    """
    return _private_sdk.add_collaborators(cloud, project, collaborators)  # type: ignore
