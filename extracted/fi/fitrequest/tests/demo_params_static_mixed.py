import logging
from typing import Literal

from pydantic import Field

from fitrequest.client import FitRequest
from fitrequest.decorators import fit

logger = logging.getLogger(__name__)


class TestApiClient(FitRequest):
    client_name = 'test'
    base_url = 'https://test.skillcorner.fr'

    @fit(endpoint='/details?debug=false&lang=fr')
    def get_item_details(
        self,
        item_id: str = Field(alias='itemId'),
        tags: list[str] = Field(default_factory=lambda: ['test', 'item']),
        env='staging',
        verbose=False,
    ) -> dict:
        """Get item details."""


client_params_static_mixed = TestApiClient()
