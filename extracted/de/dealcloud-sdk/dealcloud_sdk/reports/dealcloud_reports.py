"""
Template Reports API operations for DealCloud.

See: https://api.docs.dealcloud.com/docs - Data / Template Reports
- GET reports/template – list templates
- POST reports/generate – start report generation
- GET reports/{requestId} – get report status/result
"""

from typing import Any, Dict, List, Optional

from ..schema.dealcloud_schema import DealCloudSchema
from ..utils.process_response_errors import with_error_handling


class DealCloudReports(DealCloudSchema):
    """
    Template Reports API. One link in the linear inheritance chain.
    Provides get_report_templates(), generate_report(), get_report_status().
    """

    @with_error_handling
    def get_report_templates(
        self,
        page_size: Optional[int] = None,
        page_number: Optional[int] = None,
        id: Optional[int] = None,
    ) -> List[dict]:
        """
        Get available template reports.

        Args:
            page_size: Optional page size for pagination.
            page_number: Optional page number.
            id: Optional template ID to filter by.

        Returns:
            List of template report objects (id, name, reportType, templateSource, reportFormat, etc.).

        Example:
            >>> templates = dc.get_report_templates()
            >>> for t in templates:
            ...     print(t.get("name"), t.get("id"))
        """
        url = f"{self._data_url}/reports/template"
        params: List[str] = []
        if page_size is not None:
            params.append(f"pageSize={page_size}")
        if page_number is not None:
            params.append(f"pageNumber={page_number}")
        if id is not None:
            params.append(f"id={id}")
        if params:
            url = f"{url}?{'&'.join(params)}"
        return self._client.get(url)

    @with_error_handling
    def generate_report(
        self,
        template_id: int,
        remove_empty_table: Optional[bool] = None,
        entries: Optional[List[int]] = None,
        user_ids: Optional[List[int]] = None,
        filters: Optional[Dict[str, Any]] = None,
    ) -> dict:
        """
        Start report generation for a template.

        Args:
            template_id: Template report ID (required).
            remove_empty_table: Optional flag to remove empty tables.
            entries: Optional list of entry IDs to scope the report.
            user_ids: Optional list of user IDs.
            filters: Optional filter terms per swagger GenerateReportRequestVm.

        Returns:
            Dict with requestID (uuid), status, errorMessage (e.g. from GenerateReportResponse).

        Example:
            >>> resp = dc.generate_report(template_id=123)
            >>> request_id = resp.get("requestID")
            >>> status = dc.get_report_status(request_id)
        """
        url = f"{self._data_url}/reports/generate"
        payload: Dict[str, Any] = {"templateId": template_id}
        if remove_empty_table is not None:
            payload["removeEmptyTable"] = remove_empty_table
        if entries is not None:
            payload["entryIds"] = entries
        if user_ids is not None:
            payload["userIds"] = user_ids
        if filters is not None:
            payload["filters"] = filters
        return self._client.post(url, json=payload)

    @with_error_handling
    def get_report_status(self, request_id: str) -> dict:
        """
        Get status or result of a report generation request.

        Args:
            request_id: UUID returned from generate_report() (requestID).

        Returns:
            Report status/result dict (shape per API).

        Example:
            >>> status = dc.get_report_status("550e8400-e29b-41d4-a716-446655440000")
        """
        url = f"{self._data_url}/reports/{request_id}"
        return self._client.get(url)
