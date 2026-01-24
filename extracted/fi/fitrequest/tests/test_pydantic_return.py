import httpx
import pytest
import respx
from pydantic import ValidationError

from fitrequest.client import FitRequest
from fitrequest.decorators import fit
from fitrequest.errors import InvalidResponseTypeError
from tests.demo_decorator_pydantic_return import client_pydantic_return


@respx.mock
def test_method_get_items_pydantic():
    client = client_pydantic_return
    expected = {
        'items': [
            {'item_id': 1, 'item_name': 'ball'},
            {'item_id': 2, 'item_name': 'gloves'},
        ]
    }
    respx.get('https://test.skillcorner.fr').mock(return_value=httpx.Response(200, json=expected))
    response = client.get_items()
    assert [elem.model_dump() for elem in response] == expected['items']


@respx.mock
def test_method_get_item_pydantic():
    client = client_pydantic_return
    item_id = 1
    expected = {'item_id': item_id, 'item_name': 'ball'}

    respx.get(f'https://test.skillcorner.fr/items/{item_id}').mock(return_value=httpx.Response(200, json=expected))
    response = client.get_item(item_id=item_id)
    assert response.model_dump() == expected


@respx.mock
def test_method_get_item_details_pydantic():
    client = client_pydantic_return
    item_id = 1
    detail_id = 7
    expected = {'item_id': item_id, 'detail_id': detail_id, 'item_name': 'ball', 'detail': 'color white'}

    respx.get(f'https://test.skillcorner.fr/items/{item_id}/details/{detail_id}').mock(
        return_value=httpx.Response(200, json=expected)
    )
    response = client.get_item_details(item_id=item_id, detail_id=detail_id)
    assert response.model_dump() == expected


@respx.mock
@pytest.mark.asyncio
async def test_method_async_get_items_pydantic():
    client = client_pydantic_return
    expected = {
        'items': [
            {'item_id': 1, 'item_name': 'ball'},
            {'item_id': 2, 'item_name': 'gloves'},
        ]
    }
    respx.get('https://test.skillcorner.fr').mock(return_value=httpx.Response(200, json=expected))
    response = await client.async_get_items()
    assert [elem.model_dump() for elem in response] == expected['items']


def test_response_invalid_model_type():
    with pytest.raises(ValidationError) as err:

        class RestApiClient(FitRequest):
            client_name = 'rest_api'
            base_url = 'https://test.skillcorner.fr'
            method_config_list = [
                {
                    'name': 'get_item',
                    'endpoint': '/items/{item_id}',
                    'response_model': 1234,
                }
            ]

    assert isinstance(err.value.errors()[0]['ctx']['error'], InvalidResponseTypeError)


def test_none_type_with_fit_decorator():
    # No error raised
    class RestApiClient(FitRequest):
        client_name = 'rest_api'
        base_url = 'https://test.skillcorner.fr'

        @fit(endpoint='/items/{item_id}')
        def get_item(self, item_id: str) -> None: ...
