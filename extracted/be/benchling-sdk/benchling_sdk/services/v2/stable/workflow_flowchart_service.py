import datetime
from typing import Iterable, List, Optional

from benchling_api_client.v2.stable.api.workflow_flowcharts import (
    get_workflow_flowchart,
    list_workflow_flowcharts,
)
from benchling_api_client.v2.types import Response

from benchling_sdk.errors import raise_for_status
from benchling_sdk.helpers.decorators import api_method
from benchling_sdk.helpers.pagination_helpers import NextToken, PageIterator
from benchling_sdk.helpers.response_helpers import model_from_detailed
from benchling_sdk.helpers.serialization_helpers import none_as_unset, optional_array_query_param
from benchling_sdk.models import ListWorkflowFlowchartsSort, WorkflowFlowchart, WorkflowFlowchartPaginatedList
from benchling_sdk.services.v2.base_service import BaseService


class WorkflowFlowchartService(BaseService):
    """
    Workflow Flowcharts.

    Workflow flowcharts represent the nodes and edges that a flowchart is comprised of.

    See https://benchling.com/api/reference#/Workflow%20Flowcharts
    """

    @api_method
    def get_by_id(self, workflow_flowchart_id: str) -> WorkflowFlowchart:
        """
        Get a workflow flowchart.

        See https://benchling.com/api/reference#/Workflow%20Flowcharts/getWorkflowFlowchart
        """
        response = get_workflow_flowchart.sync_detailed(
            client=self.client, workflow_flowchart_id=workflow_flowchart_id
        )
        return model_from_detailed(response)

    @api_method
    def _workflow_tasks_page(
        self,
        sort: Optional[ListWorkflowFlowchartsSort] = None,
        ids: Optional[Iterable[str]] = None,
        created_at: Optional[datetime.date] = None,
        page_size: Optional[int] = None,
        next_token: Optional[NextToken] = None,
    ) -> Response[WorkflowFlowchartPaginatedList]:
        response = list_workflow_flowcharts.sync_detailed(
            client=self.client,
            ids=none_as_unset(optional_array_query_param(ids)),
            created_at=none_as_unset(created_at),
            next_token=none_as_unset(next_token),
            page_size=none_as_unset(page_size),
            sort=none_as_unset(sort),
        )
        raise_for_status(response)
        return response  # type: ignore

    def list(
        self,
        sort: Optional[ListWorkflowFlowchartsSort] = None,
        ids: Optional[Iterable[str]] = None,
        created_at: Optional[datetime.date] = None,
        page_size: Optional[int] = None,
    ) -> PageIterator[WorkflowFlowchart]:
        """
        List workflow flowcharts.

        See https://benchling.com/api/reference#/Workflow%20Tasks/listWorkflowFlowcharts
        """

        def api_call(next_token: NextToken) -> Response[WorkflowFlowchartPaginatedList]:
            return self._workflow_tasks_page(
                sort=sort,
                ids=ids,
                created_at=created_at,
                page_size=page_size,
                next_token=next_token,
            )

        def results_extractor(body: WorkflowFlowchartPaginatedList) -> Optional[List[WorkflowFlowchart]]:
            return body.workflow_flowcharts

        return PageIterator(api_call, results_extractor)
