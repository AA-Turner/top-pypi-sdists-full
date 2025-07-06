from typing import Optional, Dict, Any

from ._interactor import _Interactor

DATA_FABRIC_URI_PATH = "/suite/rest/a/applications/latest/app/process-hq"
DATA_FABRIC_DASHBOARD_URI_PATH = "/suite/rest/a/applications/latest/app/process-hq/dashboard/"


class _DataFabric:
    def __init__(self, interactor: _Interactor):
        self.interactor = interactor

    def fetch_data_fabric_json(self, locust_request_label: Optional[str] = None) -> Dict[str, Any]:
        headers = self.interactor.setup_sail_headers()
        headers['X-Client-Mode'] = 'DESIGN'
        label = locust_request_label or "DataFabric.Ui"
        response = self.interactor.get_page(DATA_FABRIC_URI_PATH, headers=headers, label=label)
        response.raise_for_status()
        return response.json()

    def fetch_data_fabric_dashboard_json(self, encoded_uri_stub: str = "new", locust_request_label: Optional[str] = None) -> Dict[str, Any]:
        headers = self.interactor.setup_sail_headers()
        headers['X-Client-Mode'] = 'DESIGN'
        label = locust_request_label or "DataFabricDashboard.Ui"
        response = self.interactor.get_page(f"{DATA_FABRIC_DASHBOARD_URI_PATH}{encoded_uri_stub}", headers=headers,
                                            label=label)
        response.raise_for_status()
        return response.json()
