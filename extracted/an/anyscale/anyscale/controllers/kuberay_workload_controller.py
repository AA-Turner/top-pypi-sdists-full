from typing import Any, Dict, Optional

from anyscale.cli_logger import BlockLogger
from anyscale.client.openapi_client.models.create_workload_request import (
    CreateWorkloadRequest,
)
from anyscale.client.openapi_client.models.create_workload_response import (
    CreateWorkloadResponse,
)
from anyscale.controllers.base_controller import BaseController


class KuberayWorkloadController(BaseController):
    """Submits KubeRay workloads (RayJob CRs) to the platform via /create."""

    def __init__(
        self,
        log: Optional[BlockLogger] = None,
        initialize_auth_api_client: bool = True,
    ):
        if log is None:
            log = BlockLogger()
        super().__init__(initialize_auth_api_client=initialize_auth_api_client)
        self.log = log

    def apply(
        self,
        *,
        spec: Dict[str, Any],
        cloud_id: str,
        project_id: Optional[str],
        name: Optional[str],
    ) -> CreateWorkloadResponse:
        """Submit a KubeRay CR to run on the platform; returns the accepted workload.

        The CR is recorded PENDING and scheduled asynchronously; the response carries
        its identity (workload_id, name) and initial state.
        """
        request = CreateWorkloadRequest(
            spec=spec, cloud_id=cloud_id, project_id=project_id, name=name,
        )
        response: CreateWorkloadResponse = self.api_client.create_workload_api_v2_kuberay_workloads_create_post(
            request
        ).result
        return response
