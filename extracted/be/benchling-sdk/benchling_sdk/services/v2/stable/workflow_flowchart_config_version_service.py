from benchling_api_client.v2.stable.api.workflow_flowchart_config_versions import (
    get_workflow_flowchart_config_version,
)

from benchling_sdk.helpers.decorators import api_method
from benchling_sdk.helpers.response_helpers import model_from_detailed
from benchling_sdk.models import WorkflowFlowchartConfigVersion
from benchling_sdk.services.v2.base_service import BaseService


class WorkflowFlowchartConfigVersionService(BaseService):
    """
    Workflow Flowchart Config Versions.

    Workflow flowchart config versions are versioned graphs of flowchart configurations.

    See https://benchling.com/api/reference#/Workflow%20Flowchart%20Config%20Versions
    """

    @api_method
    def get_by_id(self, workflow_flowchart_config_version_id: str) -> WorkflowFlowchartConfigVersion:
        """
        Get a workflow flowchart config version.

        If there is a template flowchart, serializes that flowchart in the same format as the workflow_flowcharts service.

        See https://benchling.com/api/reference#/Workflow%20Flowcharts/getWorkflowConfigVersion
        """
        response = get_workflow_flowchart_config_version.sync_detailed(
            client=self.client, workflow_flowchart_config_version_id=workflow_flowchart_config_version_id
        )
        return model_from_detailed(response)
