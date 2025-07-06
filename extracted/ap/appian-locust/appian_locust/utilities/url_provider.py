from uritemplate import expand
from urllib.parse import urlparse
from typing import Dict, Any

from ..objects.page import Page, PageType

URL_PATTERN_V0 = {
    "x-data-request-site-nav-top-level-page": "https://pattern.net/suite/rest/a/sites/latest/{siteUrlStub}/page/{pageUrlStub}/nav",
    "x-data-request-site-top-level-record-instance-page": "https://pattern.net/suite/rest/a/sites/latest/{siteUrlStub}/page/{pageUrlStub}/record/{opaqueRecordReference}/view/{viewUrlStub}",
    "x-data-request-site-top-level-report-link": "https://pattern.net/suite/rest/a/sites/latest/{siteUrlStub}/pages/p.{pageUrlStub}/report{/reportUrlStub}/reportlink",
    "x-data-request-site-top-level-interface-page": "https://pattern.net/suite/rest/a/sites/latest/{siteUrlStub}/page/p.{pageUrlStub}",
    "x-data-request-site-top-level-record-type-page": "https://pattern.net/suite/rest/a/sites/latest/{siteUrlStub}/pages/{pageUrlStub}/recordType",
    "x-data-request-site-top-level-action-page": "https://pattern.net/suite/rest/a/sites/latest/{siteUrlStub}/pages/{pageUrlStub}/action",
    "x-data-request-site-top-level-report-page": "https://pattern.net/suite/rest/a/sites/latest/{siteUrlStub}/pages/{pageUrlStub}/report",
    "x-data-request-task-attributes": "https://pattern.net/suite/rest/a/task/latest/{taskId}/attributes",
    "x-data-request-task-status": "https://pattern.net/suite/rest/a/task/latest/{taskId}/status",
    "x-data-request-task-form": "https://pattern.net/suite/rest/a/task/latest/{taskId}/form",
    "x-data-request-site-page-redirect": "https://pattern.net/suite/rest/a/applications/latest/legacy/sites/{siteUrlStub}/page/{pageUrlStub}",
    "x-data-request-site-top-level-start-process-page": "https://pattern.net/suite/rest/a/sites/latest/{siteUrlStub}/page/p.{pageUrlStub}/startProcess/{processModelOpaqueId}?cacheKey={cacheKey}",
    "x-data-request-site-nav": "https://pattern.net/suite/rest/a/sites/latest/{siteUrlStub}/nav",
}

URL_PATTERN_V1 = {
    "x-data-request-site-nav-top-level-page": "https://pattern.net/suite/rest/a/sites/latest/{siteUrlStub}/page/p.{pageUrlStub}/nav",
    "x-data-request-site-nav-nested-page": "https://pattern.net/suite/rest/a/sites/latest/{siteUrlStub}/page/g.{groupUrlStub}.p.{pageUrlStub}/nav",
    "x-data-request-site-top-level-record-instance-page": "https://pattern.net/suite/rest/a/sites/latest/{siteUrlStub}/page/p.{pageUrlStub}/record/{opaqueRecordReference}/view/{viewUrlStub}",
    "x-data-request-site-nested-record-instance-page": "https://pattern.net/suite/rest/a/sites/latest/{siteUrlStub}/page/g.{groupUrlStub}.p.{pageUrlStub}/record/{opaqueRecordReference}/view/{viewUrlStub}",
    "x-data-request-site-top-level-report-link": "https://pattern.net/suite/rest/a/sites/latest/{siteUrlStub}/pages/p.{pageUrlStub}/report{/reportUrlStub}/reportlink",
    "x-data-request-site-nested-interface-page": "https://pattern.net/suite/rest/a/sites/latest/{siteUrlStub}/page/g.{groupUrlStub}.p.{pageUrlStub}",
    "x-data-request-site-top-level-interface-page": "https://pattern.net/suite/rest/a/sites/latest/{siteUrlStub}/page/p.{pageUrlStub}",
    "x-data-request-site-top-level-record-type-page": "https://pattern.net/suite/rest/a/sites/latest/{siteUrlStub}/pages/{pageUrlStub}/recordType",
    "x-data-request-site-top-level-action-page": "https://pattern.net/suite/rest/a/sites/latest/{siteUrlStub}/pages/{pageUrlStub}/action",
    "x-data-request-site-top-level-report-page": "https://pattern.net/suite/rest/a/sites/latest/{siteUrlStub}/pages/{pageUrlStub}/report",
    "x-data-request-task-attributes": "https://pattern.net/suite/rest/a/task/latest/{taskId}/attributes",
    "x-data-request-task-status": "https://pattern.net/suite/rest/a/task/latest/{taskId}/status",
    "x-data-request-task-form": "https://pattern.net/suite/rest/a/task/latest/{taskId}/form",
    "x-data-request-site-page-redirect": "https://pattern.net/suite/rest/a/applications/latest/legacy/sites/{siteUrlStub}/page/{pageUrlStub}",
    "x-data-request-site-top-level-start-process-page": "https://pattern.net/suite/rest/a/sites/latest/{siteUrlStub}/page/p.{pageUrlStub}/startProcess/{processModelOpaqueId}?cacheKey={cacheKey}",
    "x-data-request-site-nested-start-process-page": "https://pattern.net/suite/rest/a/sites/latest/{siteUrlStub}/page/g.{groupUrlStub}.p.{pageUrlStub}/startProcess/{processModelOpaqueId}?cacheKey={cacheKey}",
    "x-data-request-site-nav": "https://pattern.net/suite/rest/a/sites/latest/{siteUrlStub}/nav",
    "x-data-request-site-group-page": "https://pattern.net/suite/rest/a/sites/latest/{siteUrlStub}/page/g.{groupUrlStub}",
    "x-data-request-site-nav-group-page": "https://pattern.net/suite/rest/a/sites/latest/{siteUrlStub}/page/g.{groupUrlStub}/nav",
    "x-data-request-site-nested-report-link": "https://pattern.net/suite/rest/a/sites/latest/{siteUrlStub}/pages/g.{groupUrlStub}.p.{pageUrlStub}/report{/reportUrlStub}/reportlink",
}


class UrlProvider:

    def __init__(self, url_info: Dict[str, str]) -> None:
        self.url_info = url_info
        # If not on version with full set of endpoints in API response, fall back to V1
        if not "x-data-request-task-attributes" in self.url_info:
            self.url_info = URL_PATTERN_V1
        for key in self.url_info:
            url = self.url_info[key]
            query = urlparse(url).query
            url = urlparse(url).path
            if query:
                url += f"?{query}"
            self.url_info[key] = url

    def get_page_nav_path(self, page: Page) -> str:
        site_nav_key = "x-data-request-site-nav-nested-page" if page.group_name else "x-data-request-site-nav-top-level-page"
        uri_template_variables: Dict[str, Any] = {
            "siteUrlStub": page.site_stub,
            "pageUrlStub": page.page_name,
            "groupUrlStub": page.group_name
        }
        sites_nav_url = expand(self.url_info[site_nav_key], uri_template_variables)
        return sites_nav_url

    def get_record_path(self, page: Page, opaque_id: str, view: str) -> str:
        record_view_key = "x-data-request-site-nested-record-instance-page" if page.group_name else "x-data-request-site-top-level-record-instance-page"
        uri_template_variables: Dict[str, Any] = {
            "siteUrlStub": page.site_stub,
            "pageUrlStub": page.page_name,
            "opaqueRecordReference": opaque_id,
            "viewUrlStub": view,
            "groupUrlStub": page.group_name
        }
        record_view_url = expand(self.url_info[record_view_key], uri_template_variables)
        return record_view_url

    def get_report_link_path(self, page: Page, report_stub: str) -> str:
        report_link_key = "x-data-request-site-top-level-report-link"
        uri_template_variables: Dict[str, Any] = {
            "siteUrlStub": page.site_stub,
            "pageUrlStub": page.page_name,
            "reportUrlStub": report_stub
        }
        report_link_url = expand(self.url_info[report_link_key], uri_template_variables)
        return report_link_url

    def get_page_path(self, page: Page) -> str:
        match page.page_type:
            case PageType.INTERFACE:
                page_key = "x-data-request-site-nested-interface-page" if page.group_name else "x-data-request-site-top-level-interface-page"
            case PageType.RECORD:
                page_key = "x-data-request-site-top-level-record-type-page"
            case PageType.ACTION:
                page_key = "x-data-request-site-top-level-action-page"
            case _:
                page_key = "x-data-request-site-top-level-report-page"
        uri_template_variables: Dict[str, Any] = {
            "siteUrlStub": page.site_stub,
            "pageUrlStub": page.page_name,
            "groupUrlStub": page.group_name
        }
        page_url = expand(self.url_info[page_key], uri_template_variables)
        return page_url

    def get_task_attributes_path(self, task_id: str) -> str:
        task_url = expand(self.url_info["x-data-request-task-attributes"], {"taskId": task_id})
        return task_url

    def get_task_status_path(self, task_id: str) -> str:
        task_url = expand(self.url_info["x-data-request-task-status"], {"taskId": task_id})
        return task_url

    def get_task_form_path(self, task_id: str) -> str:
        task_url = expand(self.url_info["x-data-request-task-form"], {"taskId": task_id})
        return task_url

    def get_site_page_redirect_path(self, site_name: str, page_name: str) -> str:
        page_redirect_key = "x-data-request-site-page-redirect"
        uri_template_variables: Dict[str, Any] = {
            "siteUrlStub": site_name,
            "pageUrlStub": page_name,
        }
        page_redirect_url = expand(self.url_info[page_redirect_key], uri_template_variables)
        return page_redirect_url

    def get_site_start_process_path(self, page: Page, process_model_opaque_id: str, cache_key: str) -> str:
        start_process_key = "x-data-request-site-nested-start-process-page" if page.group_name else "x-data-request-site-top-level-start-process-page"
        uri_template_variables: Dict[str, Any] = {
            "siteUrlStub": page.site_stub,
            "pageUrlStub": page.page_name,
            "processModelOpaqueId": process_model_opaque_id,
            "cacheKey": cache_key,
            "groupUrlStub": page.group_name
        }
        start_process_url = expand(self.url_info[start_process_key], uri_template_variables)
        return start_process_url

    def get_site_nav_path(self, site_name: str) -> str:
        site_nav_key = "x-data-request-site-nav"
        site_nav_path = expand(self.url_info[site_nav_key], {"siteUrlStub": site_name})
        return site_nav_path


URL_PROVIDER_V0 = UrlProvider(URL_PATTERN_V0)
URL_PROVIDER_V1 = UrlProvider(URL_PATTERN_V1)
