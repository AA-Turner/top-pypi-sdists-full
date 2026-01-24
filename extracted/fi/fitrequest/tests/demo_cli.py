import json
from typing import Literal

from pydantic import BaseModel

from fitrequest.client import FitRequest
from fitrequest.decorators import cli_method, fit


class Item(BaseModel):
    item_id: int
    item_name: str
    detail_id: int


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

    @fit(endpoint='/version/')
    def _get_version(self) -> dict: ...

    @fit(endpoint='/items/')
    def get_items(
        self,
        limit: int | None = None,
        sort: Literal['name', 'date'] = 'name',
        order: Literal['asc', 'desc'] = 'asc',
    ) -> list[Item]: ...

    @fit(endpoint='/items/{item_id}')
    def get_item(self, item_id: str) -> Item: ...

    @fit(endpoint='/items/{item_id}/details/{detail_id}')
    def get_item_details(self, item_id: str, detail_id: str) -> ItemDetails: ...

    @cli_method
    def get_details(self) -> list[ItemDetails]:
        """Return list of ItemDetails."""
        return [self.get_item_details(item.item_id, item.detail_id) for item in self.get_items()]

    @cli_method
    def get_inputs(
        self,
        item_id: int,
        limit: int | None = None,
        sort: Literal['name', 'date'] = 'name',
        order: Literal['asc', 'desc'] = 'asc',
    ) -> str:
        """Simple method that returns typer input data as a json string."""
        return json.dumps(
            {
                'item_id': item_id,
                'limit': limit,
                'sort': sort,
                'order': order,
            }
        )


client_cli = RestApiClient()
