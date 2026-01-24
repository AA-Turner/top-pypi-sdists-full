import logging
from typing import Literal

from pydantic import Field

from fitrequest.client import FitRequest
from fitrequest.decorators import fit

logger = logging.getLogger(__name__)


class TestApiClient(FitRequest):
    client_name = 'test'
    base_url = 'https://test.skillcorner.fr'

    @fit(endpoint='/details')
    def get_item_details(
        self,
        item_id: str = Field(alias='itemId'),
        tags: list[str] = Field(default_factory=lambda: ['test', 'item']),
        lang: Literal['en', 'fr'] = Field(alias='language', default='en'),
        debug: bool = False,
    ) -> dict:
        """Get item details."""


client_params_alias = TestApiClient()
