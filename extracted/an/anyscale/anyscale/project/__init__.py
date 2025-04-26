from typing import List, Optional

from anyscale._private.anyscale_client import AnyscaleClientInterface
from anyscale._private.sdk import sdk_docs
from anyscale._private.sdk.base_sdk import Timer
from anyscale.cli_logger import BlockLogger
from anyscale.project._private.project_sdk import PrivateProjectSDK
from anyscale.project.commands import (
    _ADD_COLLABORATORS_DOCSTRINGS,
    _ADD_COLLABORATORS_EXAMPLE,
    add_collaborators,
)
from anyscale.project.models import CreateProjectCollaborator


class ProjectSDK:
    def __init__(
        self,
        *,
        client: Optional[AnyscaleClientInterface] = None,
        logger: Optional[BlockLogger] = None,
        timer: Optional[Timer] = None,
    ):
        self._private_sdk = PrivateProjectSDK(client=client, logger=logger, timer=timer)

    @sdk_docs(
        doc_py_example=_ADD_COLLABORATORS_EXAMPLE,
        arg_docstrings=_ADD_COLLABORATORS_DOCSTRINGS,
    )
    def add_collaborators(  # noqa: F811
        self, cloud: str, project: str, collaborators: List[CreateProjectCollaborator],
    ) -> None:
        """Batch add collaborators to a project.
        """
        self._private_sdk.add_collaborators(cloud, project, collaborators)
