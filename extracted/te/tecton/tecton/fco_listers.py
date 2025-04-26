from typing import List

from tecton._internals import metadata_service
from tecton._internals.sdk_decorators import sdk_public_method
from tecton_proto.metadataservice.metadata_service__client_pb2 import ListWorkspacesRequest


@sdk_public_method
def list_workspaces() -> List[str]:
    """
    Returns a list of the names of all registered Workspaces.

    :return: A list of strings.
    """
    request = ListWorkspacesRequest()
    response = metadata_service.instance().ListWorkspaces(request)
    return sorted([workspace.name for workspace in response.workspaces])
