import pytest
from fitrequest.client import FitRequest
from fitrequest.decorators import fit

from skillcorner.pagination import paginated


class TestClient(FitRequest):
    client_name = 'test_client'
    base_url = 'https://test.skillcorner.fr'

    @paginated
    @fit(endpoint='/items/')
    def get_items(self, **kwargs) -> list[dict]: ...

    @paginated
    @fit(endpoint='/items/')
    async def async_get_items(self, **kwargs) -> list[dict]: ...


@pytest.fixture()
def test_client():
    return TestClient()
