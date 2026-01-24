from typing import Literal

from fitrequest.client import FitRequest
from fitrequest.decorators import fit, retry
from tests.fixtures import Item, ItemDetails


class RestApiClient(FitRequest):
    """Awesome class generated with fitrequest."""

    client_name = 'rest_api'
    base_url = 'https://test.skillcorner.fr'
    method_docstring = 'Calling endpoint: {endpoint}'

    @fit(endpoint='/items/', json_path='[*].items')
    def get_items(
        self,
        page: int | None = None,
        limit: int | None = None,
        sort: Literal['name', 'date'] = 'name',
        order: Literal['asc', 'desc'] = 'asc',
        lang: Literal['en', 'fr', 'es'] = 'en',
    ) -> list[Item]: ...

    @fit(endpoint='/items/', json_path='[*].items')
    async def async_get_items(
        self,
        page: int | None = None,
        limit: int | None = None,
        sort: Literal['name', 'date'] = 'name',
        order: Literal['asc', 'desc'] = 'asc',
        lang: Literal['en', 'fr', 'es'] = 'en',
    ) -> list[Item]: ...

    @retry(max_retries=3, on_status='500-600')
    @fit(endpoint='/items/{item_id}')
    def get_item(self, item_id: str, lang: str | None = None, resp_format: str | None = None) -> Item: ...

    @retry(max_retries=2, on_status='507')
    @fit(endpoint='/items/{item_id}/details/{detail_id}')
    def get_item_details(
        self, item_id: str, detail_id: str, lang: str | None = None, resp_format: str | None = None
    ) -> ItemDetails: ...


client_decorated_request_params = RestApiClient()
