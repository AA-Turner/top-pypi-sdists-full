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
    def get_item_details(  # noqa: PLR0913
        self,
        item_id=Field(alias='itemId'),
        tags=Field(default_factory=lambda: ['test', 'item']),
        lang='en',
        debug=False,
        env='dev',
        verbose=False,
        logs=None,
    ) -> dict:
        """Get item details."""


client_params_without_type = TestApiClient()
