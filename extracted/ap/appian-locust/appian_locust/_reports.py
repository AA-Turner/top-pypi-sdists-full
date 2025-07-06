from typing import Any, Dict, Optional
from urllib.parse import quote

from ._base import _Base
from ._interactor import _Interactor
from .objects import TEMPO_REPORTS_PAGE
from .utilities import format_label, logger

ALL_REPORTS_URI = "/suite/rest/a/uicontainer/latest/reports"
REPORTS_INTERFACE_PATH = "/suite/rest/a/sites/latest/D6JMim/pages/reports/interface"

log = logger.getLogger(__name__)


class _Reports(_Base):
    def __init__(self, interactor: _Interactor) -> None:
        """
        Reports class wrapping list of possible activities can be performed with Appian-Tempo-Reports.

        Warnings: This class is internal and should not be accessed by tests directly. It can be accessed via the "appian" object

        Note: "appian" is created as part of ``AppianTaskSet``'s ``on_start`` function

        Args:
            session: Locust session/client object
            host (str): Host URL

        """
        self.interactor = interactor

        # When Get All functions called, these variables will be used to cache the values
        self._reports: Dict[str, Any] = dict()
        self._errors: int = 0

    def get_report_form_uri(self, report_name: str, exact_match: bool = True) -> str:
        report_resp: dict = self.get_report(report_name, exact_match)
        report_url_stub = report_resp['links'][1]['href'].rsplit(
            '/', 1)[1]
        uri = self.interactor.get_url_provider().get_report_link_path(TEMPO_REPORTS_PAGE, report_url_stub)
        return uri

    def get_reports_interface(self, locust_request_label: str = "Reports") -> Dict[str, Any]:
        uri = self.interactor.host + REPORTS_INTERFACE_PATH
        headers = self.interactor.setup_sail_headers()
        resp = self.interactor.get_page(uri, headers, f'{locust_request_label}.Interface')
        return resp.json()

    def get_reports_nav(self, locust_request_label: str = "Reports") -> Dict[str, Any]:
        uri = self.interactor.get_url_provider().get_page_nav_path(TEMPO_REPORTS_PAGE)
        headers = self.interactor.setup_sail_headers()
        resp = self.interactor.get_page(uri, headers, f'{locust_request_label}.Nav')
        return resp.json()

    def get_all(self, search_string: Optional[str] = None, locust_request_label: str = "Reports.Feed") -> Dict[str, Any]:
        """
        Retrieves all the available "reports" and associated metadata from "Appian-Tempo-Reports"

        Note: All the retrieved data about reports is stored in the private variable self._reports

        Returns (dict): List of reports and associated metadata

        Examples:

            >>> self.appian.reports.get_all()

        """
        try:
            self.get_reports_interface(locust_request_label=locust_request_label)
            self.get_reports_nav(locust_request_label=locust_request_label)
        except Exception as e:
            log.error(e)

        uri = ALL_REPORTS_URI
        if search_string:
            # Format search string to be compatible with URLs
            search_string = quote(search_string)
            uri = f"{uri}?q={search_string}"

        self._reports = dict()
        error_key_string = "ERROR::"
        error_key_count = 0

        response = self.interactor.get_page(uri=uri, label=locust_request_label)

        try:
            for current_item in response.json()['feed']['entries']:
                try:
                    title = current_item['title'].strip()
                    report_url_stub = current_item['links'][1]['href'].rsplit(
                        '/', 1)[1]
                    key = title + "::" + report_url_stub
                    self._reports[key] = current_item
                except Exception as e:
                    error_key_count += 1
                    self._reports[error_key_string + str(error_key_count)] = {}
                    log.error(f"Corrupt Report Error: {current_item}")
            self._errors = error_key_count
        except Exception as e:
            log.info("No Reports Returned")
            return self._reports
        return self._reports

    def get_report(self, report_name: str, exact_match: bool = True) -> Dict[str, Any]:
        """
        Get the information about specific report by name.

        Args:
            report_name (str): Name of the report
            exact_match (bool): Should report name match exactly or to be partial match. Default : True

        Returns (dict): Specific Report's info

        Raises: In case of report is not found in the system, it throws an "Exception"

        Example:
            If full name of report is known,

            >>> self.appian.reports.get("report_name")

            If only partial name is known,

            >>> self.appian.reports.get("report_name", exact_match=False)

        """
        _, current_report = super().get(self._reports, report_name, exact_match)
        if not current_report:
            _, current_report = super().get(self._reports, report_name, exact_match, search_string=report_name)
        if not current_report:
            raise (Exception("There is no report with name {} in the system under test (Exact match = {})".format(
                report_name, exact_match)))
        return current_report

    def fetch_report_json(self, report_name: str, exact_match: bool = True, locust_request_label: Optional[str] = None) -> Dict[str, Any]:
        """
        This function calls the API for the specific report to get its "form" data

        Args:
            report_name (str): Name of the report to be called.
            exact_match (bool, optional): Should report name match exactly or to be partial match. Default : True
            locust_request_label (str, optional): Label locust should associate this request with

        Returns (dict): Response of report's Get UI call in dictionary

        Examples:

            If full name of report is known,

            >>> self.appian.reports.fetch_report_json("report_name")

            If only partial name is known,

            >>> self.appian.reports.fetch_report_json("report_name", exact_match=False)

        """
        form_uri = self.get_report_form_uri(report_name, exact_match)
        headers = self.interactor.setup_request_headers()
        headers["Accept"] = "application/vnd.appian.tv.ui+json"

        # navigation request
        uri = self.interactor.get_url_provider().get_page_nav_path(TEMPO_REPORTS_PAGE)
        if locust_request_label:
            nav_label = f"{locust_request_label}.Nav"
        else:
            nav_label = "Reports.Nav." + format_label(report_name, "::", 0)
        self.interactor.get_page(uri=uri, headers=headers, label=nav_label)  # report request
        label = locust_request_label or "Reports.GetUi." + format_label(report_name, "::", 0)
        resp = self.interactor.get_page(uri=form_uri, headers=headers, label=label)
        resp.raise_for_status()
        return resp.json()
