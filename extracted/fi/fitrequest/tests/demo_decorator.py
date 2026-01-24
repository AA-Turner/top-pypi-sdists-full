from typing import Any

from fitrequest.client import FitRequest
from fitrequest.decorators import fit, retry


class RestApiClient(FitRequest):
    """Awesome class generated with fitrequest."""

    client_name = 'rest_api'
    base_url = 'https://test.skillcorner.fr'
    method_docstring = 'Calling endpoint: {endpoint}'

    @fit(endpoint='/items/')
    def get_items(self) -> Any: ...

    @fit(endpoint='/items/')
    async def async_get_items(self) -> Any: ...

    @retry(max_retries=3, on_status='500-600')
    @fit(endpoint='/items/{item_id}')
    def get_item(self, item_id: str) -> Any: ...

    @retry(max_retries=2, on_status='507')
    @fit(endpoint='/items/{item_id}/details/{detail_id}')
    def get_item_details(self, item_id: str, detail_id: str) -> Any: ...


client_decorated = RestApiClient()
