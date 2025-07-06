from typing import Any, Dict, Optional

from ._interactor import _Interactor

PAGE_URL_PREFIX = "/_/ui/page/"


class _Portals:

    def __init__(self, interactor: _Interactor):
        self.interactor = interactor

    def fetch_page_json(self, portal_unique_identifier: str, portal_page__unique_identifier: str, locust_request_label: Optional[str] = None) -> Dict[str, Any]:
        """
        Navigates to specific portal's page

        Returns: The response of portal's page
        """
        label = locust_request_label or "Portals.Page"
        self.interactor.client.base_path_override = f"/{portal_unique_identifier}"
        portal_uri_path = self.get_full_url(portal_unique_identifier, portal_page__unique_identifier)
        response = self.interactor.get_page(portal_uri_path, label=label, check_login=False)
        response.raise_for_status()
        return response.json()

    @staticmethod
    def get_full_url(portal_unique_identifier: str, portal_page__unique_identifier: str) -> str:
        return "/" + portal_unique_identifier + PAGE_URL_PREFIX + portal_page__unique_identifier
