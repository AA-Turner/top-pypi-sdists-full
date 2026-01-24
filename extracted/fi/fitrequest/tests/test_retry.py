from unittest.mock import patch

import httpx
import pytest
import respx
import tenacity

from fitrequest.client import FitRequest
from fitrequest.decorators import fit, retry

retry_count = 4
retry_status = 404


class ClientWithFitDecorator(FitRequest):
    """Awesome class generated with fitrequest."""

    client_name = 'rest_api'
    base_url = 'https://google.fr'
    method_docstring = 'Calling endpoint: {endpoint}'

    method_config_list = [
        {
            'base_name': 'items',
            'endpoint': '/items/',
            'add_async_method': True,
        },
        {
            'name': 'get_item_details',
            'endpoint': '/items/{item_id}/details/{detail_id}',
        },
    ]

    @retry(retry_count, str(retry_status))
    @fit(endpoint='/items/{item_id}')
    def get_item(self, item_id: int) -> dict: ...


class ClientWithoutFitDecorator(FitRequest):
    """Awesome class generated with fitrequest."""

    client_name = 'rest_api'
    base_url = 'https://google.fr'
    method_docstring = 'Calling endpoint: {endpoint}'

    method_config_list = [
        {
            'base_name': 'items',
            'endpoint': '/items/',
            'add_async_method': True,
        },
        {
            'name': 'get_item',
            'endpoint': '/items/{item_id}',
            'decorators': [retry(retry_count, str(retry_status))],
        },
        {
            'name': 'get_item_details',
            'endpoint': '/items/{item_id}/details/{detail_id}',
        },
    ]


@pytest.mark.parametrize(
    'fit_cls',
    [ClientWithFitDecorator, ClientWithoutFitDecorator],
)
@respx.mock
def test_retry(fit_cls):
    item_id = 123
    client = fit_cls()

    respx.get(f'{client.base_url}/items/{item_id}').mock(return_value=httpx.Response(retry_status))

    # https://tenacity.readthedocs.io/en/latest/api.html?highlight=test#tenacity.nap.sleep
    # https://lightrun.com/answers/jd-tenacity-cannot-easily-mock-out-sleep-function-in-order-to-simulate-time-in-tests
    with pytest.raises(tenacity.RetryError), patch('tenacity.nap.time.sleep') as mocked_sleep:
        client.get_item(item_id)
    assert mocked_sleep.call_count == retry_count - 1  # If with retry N times, we sleep N-1 times.
