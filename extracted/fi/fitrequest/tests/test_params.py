from typing import Literal

import httpx
import pytest
import respx
from pydantic import BaseModel
from pydantic_core import ValidationError

from fitrequest.client import FitRequest
from fitrequest.errors import InvalidParamsTypeError, MissingRequiredArgumentError
from fitrequest.request_params import extract_params
from tests.demo_decorator_request_params import client_decorated_request_params
from tests.demo_lazy_config_request_params import client_lazy_config_request_params
from tests.demo_params_alias import client_params_alias
from tests.demo_params_static_mixed import client_params_static_mixed
from tests.demo_params_without_type import client_params_without_type
from tests.fixtures import client_complex_from_json, client_complex_from_yaml


def test_request_invalid_params_type():
    with pytest.raises(ValidationError) as err:

        class RestApiClient(FitRequest):
            client_name = 'rest_api'
            base_url = 'https://test.skillcorner.fr'
            method_config_list = [
                {
                    'name': 'get_item',
                    'endpoint': '/items/{item_id}',
                    'params_model': 1234,
                }
            ]

    assert isinstance(err.value.errors()[0]['ctx']['error'], InvalidParamsTypeError)


@pytest.mark.parametrize(
    'client',
    [
        client_decorated_request_params,
        client_lazy_config_request_params,
        client_complex_from_json,
        client_complex_from_yaml,
    ],
)
@respx.mock
def test_method_get_items(client):
    expected = {
        'items': [
            {'item_id': 1, 'item_name': 'ball'},
            {'item_id': 2, 'item_name': 'gloves'},
        ]
    }
    params = {'page': 1, 'limit': 2, 'sort': 'item_id', 'order': 'asc', 'lang': 'eng'}
    respx.get('https://test.skillcorner.fr', params=params).mock(return_value=httpx.Response(200, json=expected))
    response = client.get_items(**params)
    assert [elem.model_dump() for elem in response] == expected['items']


@pytest.mark.parametrize(
    'client',
    [
        client_decorated_request_params,
        client_lazy_config_request_params,
        client_complex_from_json,
        client_complex_from_yaml,
    ],
)
@respx.mock
def test_method_get_item(client):
    item_id = 1
    expected = {'item_id': item_id, 'item_name': 'ball'}
    params = {'lang': 'eng', 'resp_format': 'json'}

    respx.get(f'https://test.skillcorner.fr/items/{item_id}', params=params).mock(
        return_value=httpx.Response(200, json=expected)
    )
    response = client.get_item(item_id=item_id, **params)
    assert response.model_dump() == expected


@pytest.mark.parametrize(
    'client',
    [
        client_decorated_request_params,
        client_lazy_config_request_params,
        client_complex_from_json,
        client_complex_from_yaml,
    ],
)
@respx.mock
def test_method_get_item_details(client):
    item_id = 1
    detail_id = 7
    expected = {'item_id': item_id, 'detail_id': detail_id, 'item_name': 'ball', 'detail': 'color white'}
    params = {'lang': 'eng', 'resp_format': 'json'}

    respx.get(f'https://test.skillcorner.fr/items/{item_id}/details/{detail_id}', params=params).mock(
        return_value=httpx.Response(200, json=expected)
    )
    response = client.get_item_details(item_id=item_id, detail_id=detail_id, **params)
    assert response.model_dump() == expected


@pytest.mark.parametrize(
    'client',
    [
        client_decorated_request_params,
        client_lazy_config_request_params,
        client_complex_from_json,
        client_complex_from_yaml,
    ],
)
@respx.mock
@pytest.mark.asyncio
async def test_method_async_get_items(client):
    expected = {
        'items': [
            {'item_id': 1, 'item_name': 'ball'},
            {'item_id': 2, 'item_name': 'gloves'},
        ]
    }
    params = {'page': 1, 'limit': 2, 'sort': 'item_id', 'order': 'asc', 'lang': 'eng'}

    respx.get('https://test.skillcorner.fr', params=params).mock(return_value=httpx.Response(200, json=expected))
    response = await client.async_get_items(**params)
    assert [elem.model_dump() for elem in response] == expected['items']


def test_extract_params():
    def toto(name: str, age: int = 33, formats: Literal['json', 'xml'] = 'json', **kwargs) -> list[dict]: ...

    new_model = extract_params(toto, {})
    assert new_model(name='coucou').model_dump() == {'name': 'coucou', 'age': 33, 'formats': 'json'}

    new_model = extract_params(toto, {'name'})
    assert new_model().model_dump() == {'age': 33, 'formats': 'json'}


def test_extract_forbiddent_params():
    def toto(  # noqa: PLR0913
        self,
        name: str,
        age: int = 33,
        formats: Literal['json', 'xml'] = 'json',
        timeout: int = 10,
        raise_for_status: bool = False,
        params: dict | None = None,
        proxy: str | None = None,
        filepath: str | None = None,
        **kwargs,
    ) -> list[dict]: ...

    # Forbidden params are ignored (fitrequest and httpx reserver names)
    new_model = extract_params(toto, {})
    assert new_model(name='coucou').model_dump() == {'name': 'coucou', 'age': 33, 'formats': 'json'}

    new_model = extract_params(toto, {'name'})
    assert new_model().model_dump() == {'age': 33, 'formats': 'json'}


@respx.mock
def test_params_priority():
    """
    Test params priority.
    The generated keyword arguments in the signature can be combined with the classic params field in kwargs,
    using the following priority

    1. (Pydantic model) runtime method argument
    2. (``kwargs``) runtime ``params`` argument.

    It is not recommended to mix statically declared parameters in the endpoint
    with either of the two methods described, as this can lead to unexpected behaviour.
    """

    class Params(BaseModel):
        lang: Literal['fr', 'en', 'es'] = 'fr'
        rformat: Literal['xml', 'json', 'yaml'] = 'xml'
        debug: bool = False

    class ComplexApiClient(FitRequest):
        client_name = 'complex_api'
        base_url = 'https://test.skillcorner.fr'
        method_config_list = [
            {
                'name': 'get_item',
                'endpoint': '/items/{item_id}?notify={notify}',
                'params_model': Params,
            }
        ]

    client = ComplexApiClient()

    item_id = 1
    expected_data = {'item_id': item_id, 'item_name': 'ball'}
    expected_params = {
        'lang': 'es',
        'debug': True,
        'rformat': 'xml',
        'env': 'prod',
    }

    respx.get(f'https://test.skillcorner.fr/items/{item_id}', params=expected_params).mock(
        return_value=httpx.Response(200, json=expected_data)
    )
    response = client.get_item(
        item_id=item_id, lang='es', debug=True, notify=False, params={'env': 'prod', 'lang': 'en'}
    )
    assert response == expected_data


@respx.mock
def test_field_alias():
    client = client_params_alias
    item_id = 1
    detail_id = 7
    expected = {'item_id': item_id, 'detail_id': detail_id, 'item_name': 'ball', 'detail': 'color white'}

    method_params = {'lang': 'en', 'item_id': item_id}
    url_params = {'language': 'en', 'itemId': item_id, 'tags': ['test', 'item'], 'debug': False}

    respx.get('https://test.skillcorner.fr/details', params=url_params).mock(
        return_value=httpx.Response(200, json=expected)
    )
    response = client.get_item_details(**method_params)
    assert response == expected


@respx.mock
def test_field_alias_missing_required_field():
    client = client_params_alias
    params = {'lang': 'eng'}

    respx.get('https://test.skillcorner.fr/details', params=params).mock(return_value=httpx.Response(200, json={}))

    with pytest.raises(MissingRequiredArgumentError):
        client.get_item_details(**params)


@respx.mock
def test_params_without_types():
    client = client_params_without_type
    item_id = 1
    detail_id = 7
    expected = {'item_id': item_id, 'detail_id': detail_id, 'item_name': 'ball', 'detail': 'color white'}

    method_params = {'lang': 'en', 'item_id': item_id}
    url_params = {
        'lang': 'en',
        'itemId': item_id,
        'tags': ['test', 'item'],
        'debug': False,
        'env': 'dev',
        'verbose': False,
    }

    respx.get('https://test.skillcorner.fr/details', params=url_params).mock(
        return_value=httpx.Response(200, json=expected)
    )
    response = client.get_item_details(**method_params)
    assert response == expected


@respx.mock
def test_params_static_mixed():
    client = client_params_static_mixed
    item_id = 1
    detail_id = 7
    expected = {'item_id': item_id, 'detail_id': detail_id, 'item_name': 'ball', 'detail': 'color white'}

    method_params = {'item_id': item_id}
    url_params = {
        'lang': 'fr',
        'itemId': item_id,
        'tags': ['test', 'item'],
        'debug': False,
        'env': 'staging',
        'verbose': False,
    }

    respx.get('https://test.skillcorner.fr/details', params=url_params).mock(
        return_value=httpx.Response(200, json=expected)
    )
    response = client.get_item_details(**method_params)
    assert response == expected
