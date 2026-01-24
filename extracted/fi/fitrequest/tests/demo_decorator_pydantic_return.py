from pydantic import BaseModel

from fitrequest.client import FitRequest
from fitrequest.decorators import fit, retry


class Item(BaseModel):
    item_id: int
    item_name: str


class ItemDetails(BaseModel):
    detail_id: int
    detail: str
    item_id: int
    item_name: str


class RestApiClient(FitRequest):
    """Awesome class generated with fitrequest."""

    client_name = 'rest_api'
    base_url = 'https://test.skillcorner.fr'
    method_docstring = 'Calling endpoint: {endpoint}'

    @fit(endpoint='/items/', json_path='[*].items')
    def get_items(self) -> list[Item]: ...

    @fit(endpoint='/items/', json_path='[*].items')
    async def async_get_items(self) -> list[Item]: ...

    @retry(max_retries=3, on_status='500-600')
    @fit(endpoint='/items/{item_id}')
    def get_item(self, item_id: str) -> Item: ...

    @retry(max_retries=2, on_status='507')
    @fit(endpoint='/items/{item_id}/details/{detail_id}')
    def get_item_details(self, item_id: str, detail_id: str) -> ItemDetails: ...


client_pydantic_return = RestApiClient()
