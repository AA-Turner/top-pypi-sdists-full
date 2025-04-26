from benchling_api_client.v2.beta.api.audit import audit_log
from benchling_api_client.v2.beta.models.audit_log_export import AuditLogExport

from benchling_sdk.helpers.decorators import api_method
from benchling_sdk.helpers.task_helpers import TaskHelper
from benchling_sdk.models import ExportAuditLogAsyncTaskResponse
from benchling_sdk.services.v2.base_service import BaseService


class V2BetaAuditService(BaseService):
    """
    V2-Beta Audit Service.

    Export audit log data for Benchling objects.

    https://benchling.com/api/v2-beta/reference#/Audit
    """

    @api_method
    def get_audit_log(
        self, object_id: str, export: AuditLogExport
    ) -> TaskHelper[ExportAuditLogAsyncTaskResponse]:
        """
        Export an audit log file for a Benchling object.

        This endpoint launches a long-running task and returns a
        :py:class:`benchling_sdk.helpers.task_helpers.TaskHelper`. On success, the task's
        response will be an :py:class:`.ExportAuditLogAsyncTaskResponse` containing a link to
        download the exported audit log file from Amazon S3.

        This endpoint is subject to a rate limit of 500 requests per hour, in conjunction with
        the global request rate limit. Export throughput will additionally be rate limited around
        the scale of 70,000 total audit events exported in csv format or 30,000 total audit events
        exported in pdf format per hour.

        Example of submitting an export request and then getting the download URL from
        the completed task:

            task = benchling.v2.beta.audit.get_audit_log(object_id, export)
            task_result = task.wait_for_response()
            url = task_result.download_url

        See https://benchling.com/api/v2-beta/reference#/Audit/auditLog
        """
        response = audit_log.sync_detailed(client=self.client, object_id=object_id, json_body=export)
        return self._task_helper_from_response(response, ExportAuditLogAsyncTaskResponse)
