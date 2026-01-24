from typing import Any

from fitrequest.client import FitRequest
from fitrequest.decorators import fit, retry


class RestApiClient(FitRequest):
    """Awesome class generated with fitrequest."""

    client_name = 'rest_api'
    base_url = 'https://test.skillcorner.fr'
    method_docstring = 'Calling endpoint: {endpoint}'

    def __init__(self, username: str | None = None, password: str | None = None) -> None:
        self.session.update(
            auth={
                'username': {'env_name': 'API_USERNAME', 'init_value': username},
                'password': {'env_name': 'API_PASSWORD', 'init_value': password},
            },
            headers={'SOME_FIELD': 'SOME_VALUE'},
            verify=False,  # Disable SSL verification
            timeout=20,  # Set request timeout
        )
        self.session.authenticate()

    @fit(endpoint='/items/')
    def get_items(self) -> Any: ...

    @fit(endpoint='/items/')
    async def async_get_items(self) -> Any: ...

    @retry(max_retries=3, on_status='500-600')
    @fit(endpoint='/items/{item_id}')
    def get_item(self, item_id: str) -> Any: ...

    @retry(max_retries=3, on_status='500-600')
    @fit(endpoint='/items/{item_id}/details/{detail_id}')
    def get_item_details(self, item_id: str, detail_id: str) -> Any: ...


client_decorated_custom_init_session = RestApiClient(username='toto', password='1234')
