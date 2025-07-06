from typing import Any, Dict, Optional

from .._reports import _Reports


class ReportsInfo:
    """
    Class which provides metadata about available reports from the Tempo Reports tab
    """

    def __init__(self, reports: _Reports):
        self.__reports = reports

    def get_all_available_reports(self, search_string: Optional[str] = None, locust_request_label: Optional[str] = None) -> Dict[str, Any]:
        """
        Retrieves all the available "reports" and associated metadata from "Appian-Tempo-Reports"

        Returns (dict): List of reports and associated metadata

        Examples:

            >>> reports_info.get_all_available_reports()

        """
        locust_request_label = locust_request_label or "Reports.Available.All"
        return self.__reports.get_all(search_string=search_string, locust_request_label=locust_request_label)

    def get_report_info(self, report_name: str, exact_match: bool = True) -> Dict[str, Any]:
        """
        Get the information about specific report by name.

        Args:
            report_name (str): Name of the action
            exact_match (bool): Should action name match exactly or to be partial match. Default : True

        Returns (dict): Specific Report's info

        Raises: In case of report is not found in the system, it throws an "Exception"

        Example:
            If full name of report is known:

            >>> report_info.get_report_info("report_name", exact_match=True)

            If only the display name is known, or part of the display name:

            >>> report_info.get_report_info("report")

        """
        return self.__reports.get_report(report_name=report_name, exact_match=exact_match)
