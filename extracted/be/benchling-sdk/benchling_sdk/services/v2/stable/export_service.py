from benchling_api_client.v2.stable.api.exports import export_item

from benchling_sdk.helpers.decorators import api_method
from benchling_sdk.helpers.task_helpers import TaskHelper
from benchling_sdk.models import ExportItemRequest, ExportsAsyncTaskResponse
from benchling_sdk.services.v2.base_service import BaseService


class ExportService(BaseService):
    """
    Exports.

    Export a Notebook Entry.

    See https://benchling.com/api/reference#/Exports
    """

    @api_method
    def export(self, export_request: ExportItemRequest) -> TaskHelper[ExportsAsyncTaskResponse]:
        """
        Export a Notebook Entry.

        This endpoint launches a long-running task and returns the Task ID of the launched task.
        The task response contains a link to download the exported item from Amazon S3.
        The download is a ZIP file that contains the exported PDFs.

        See https://benchling.com/api/reference#/Exports/exportItem
        """
        response = export_item.sync_detailed(client=self.client, json_body=export_request)
        return self._task_helper_from_response(response, ExportsAsyncTaskResponse)
