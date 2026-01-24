from typing import Any

from fitrequest.client import FitRequest
from fitrequest.decorators import fit, retry


class RestApiClient(FitRequest):
    """Awesome class generated with fitrequest."""

    client_name = 'rest_api'
    base_url = 'https://test.skillcorner.fr'
    method_docstring = 'Calling endpoint: {endpoint}'

    method_config_list = [
        {
            'base_name': 'items',
            'endpoint': '/items/',
            'add_async_method': True,
        },
    ]

    @retry(max_retries=3, on_status='500-600')
    @fit(endpoint='/items/{item_id}')
    def get_item(self, item_id: str) -> Any: ...

    @retry(max_retries=2, on_status='507')
    @fit(endpoint='/items/{item_id}/details/{detail_id}')
    def get_item_details(self, item_id: str, detail_id: str) -> Any: ...


client_mix = RestApiClient()
