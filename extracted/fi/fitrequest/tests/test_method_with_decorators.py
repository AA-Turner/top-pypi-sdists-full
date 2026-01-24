from unittest.mock import MagicMock, mock_open, patch

import aiofiles
import httpx
import orjson
import pytest
import respx
from fixtures import (
    client_with_decorators,
    client_with_default_decorators,
    client_with_default_decorators_from_json,
    client_with_default_decorators_from_yaml,
    client_with_default_decorators_string,
)
from pydantic_core import ValidationError

from fitrequest.errors import InvalidMethodDecoratorError
from fitrequest.fit_config import FitConfig

aiofiles.threadpool.wrap.register(MagicMock)(
    lambda *args, **kwargs: aiofiles.threadpool.AsyncBufferedIOBase(*args, **kwargs)
)


@pytest.mark.parametrize(
    'client',
    [
        client_with_decorators,
        client_with_default_decorators,
        client_with_default_decorators_string,
        client_with_default_decorators_from_yaml,
        client_with_default_decorators_from_json,
    ],
)
@respx.mock
def test_decorated_get_index(client):
    data = {'result': 'nothing to see here.'}

    respx.get(f'{client.base_url}/').mock(return_value=httpx.Response(200, json=data))

    response = client.get_index()
    assert response == ('simple_decorator', data)


@pytest.mark.parametrize(
    'client',
    [
        client_with_decorators,
        client_with_default_decorators,
        client_with_default_decorators_string,
        client_with_default_decorators_from_yaml,
        client_with_default_decorators_from_json,
    ],
)
@respx.mock
def test_decorated_get_version(client):
    data = {'result': 'nothing to see here.'}

    respx.get(f'{client.base_url}/version/').mock(return_value=httpx.Response(200, json=data))

    response = client.get_version()
    assert response == ('decorator_with_params', data)


@pytest.mark.parametrize(
    'client',
    [
        client_with_decorators,
        client_with_default_decorators,
        client_with_default_decorators_string,
        client_with_default_decorators_from_yaml,
        client_with_default_decorators_from_json,
    ],
)
@respx.mock
def test_decorated_get_item(client):
    item_id = 5
    data = {'result': f'item of id {item_id}'}

    respx.get(f'{client.base_url}/items/{item_id}').mock(return_value=httpx.Response(200, json=data))

    response = client.get_item(item_id=item_id)
    assert response == ('simple_decorator', ('decorator_with_params', data))


@pytest.mark.parametrize(
    'client',
    [
        client_with_decorators,
        client_with_default_decorators,
        client_with_default_decorators_string,
        client_with_default_decorators_from_yaml,
        client_with_default_decorators_from_json,
    ],
)
@respx.mock
def test_decorated_post_item(client):
    item_id = 5
    data = {'result': f'item of id {item_id}'}

    respx.post(f'{client.base_url}/items/{item_id}').mock(return_value=httpx.Response(200, json=data))

    response = client.post_item(item_id=item_id)
    assert response == ('simple_decorator', ('decorator_with_params', data))


@pytest.mark.parametrize(
    'client',
    [
        client_with_decorators,
        client_with_default_decorators,
        client_with_default_decorators_string,
        client_with_default_decorators_from_yaml,
        client_with_default_decorators_from_json,
    ],
)
@respx.mock
@pytest.mark.asyncio
async def test_decorated_async_get_item(client):
    item_id = 5
    data = {'result': f'item of id {item_id}'}

    respx.get(f'{client.base_url}/items/{item_id}').mock(return_value=httpx.Response(200, json=data))

    response = await client.async_get_item(item_id=item_id)
    assert response == ('simple_decorator', ('decorator_with_params', data))


@pytest.mark.parametrize(
    'client',
    [
        client_with_decorators,
        client_with_default_decorators,
        client_with_default_decorators_string,
        client_with_default_decorators_from_yaml,
        client_with_default_decorators_from_json,
    ],
)
@respx.mock
@pytest.mark.asyncio
async def test_decorated_async_post_item(client):
    item_id = 5
    data = {'result': f'item of id {item_id}'}

    respx.post(f'{client.base_url}/items/{item_id}').mock(return_value=httpx.Response(200, json=data))

    response = await client.async_post_item(item_id=item_id)
    assert response == ('simple_decorator', ('decorator_with_params', data))


@pytest.mark.parametrize(
    'client',
    [
        client_with_decorators,
        client_with_default_decorators,
        client_with_default_decorators_string,
        client_with_default_decorators_from_yaml,
        client_with_default_decorators_from_json,
    ],
)
@respx.mock
def test_decorated_get_items(client):
    data = {'result': 'a lot of items'}

    respx.get(f'{client.base_url}/items/').mock(return_value=httpx.Response(200, json=data))
    response = client.get_items()

    assert response == ('decorator_with_params', ('simple_decorator', data))


@pytest.mark.parametrize(
    'client',
    [
        client_with_decorators,
        client_with_default_decorators,
        client_with_default_decorators_string,
        client_with_default_decorators_from_yaml,
        client_with_default_decorators_from_json,
    ],
)
@respx.mock
@pytest.mark.asyncio
async def test_decorated_async_get_items(client):
    data = {'result': 'a lot of items'}

    respx.get(f'{client.base_url}/items/').mock(return_value=httpx.Response(200, json=data))
    response = await client.async_get_items()

    assert response == ('decorator_with_params', ('simple_decorator', data))


@pytest.mark.parametrize(
    'client',
    [
        client_with_decorators,
        client_with_default_decorators,
        client_with_default_decorators_string,
        client_with_default_decorators_from_yaml,
        client_with_default_decorators_from_json,
    ],
)
@respx.mock
def test_decorated_get_and_save_items(client):
    data = {'result': 'a lot of items'}
    json_data = orjson.dumps(data, option=orjson.OPT_INDENT_2)
    filepath = 'test.json'

    open_mock = mock_open()
    respx.get(f'{client.base_url}/items/').mock(return_value=httpx.Response(200, json=data))

    with patch('builtins.open', open_mock, create=True):
        response = client.get_and_save_items(filepath=filepath)

    open_mock.assert_called_with(filepath, mode='xb')
    open_mock.return_value.write.assert_called_once_with(json_data)

    assert response == ('decorator_with_params', ('simple_decorator', None))


@pytest.mark.parametrize(
    'client',
    [
        client_with_decorators,
        client_with_default_decorators,
        client_with_default_decorators_string,
        client_with_default_decorators_from_yaml,
        client_with_default_decorators_from_json,
    ],
)
@respx.mock
@pytest.mark.asyncio
async def test_decorated_async_get_and_save_items(client):
    data = {'result': 'a lot of items'}
    json_data = orjson.dumps(data, option=orjson.OPT_INDENT_2)
    filepath = 'test.json'

    respx.get(f'{client.base_url}/items/').mock(return_value=httpx.Response(200, json=data))

    mock_file_stream = MagicMock(read=lambda: next(iter(json_data)))
    default_open_args = {
        'buffering': -1,
        'encoding': None,
        'errors': None,
        'newline': None,
        'closefd': True,
        'opener': None,
    }

    with patch('aiofiles.threadpool.sync_open', return_value=mock_file_stream) as open_mock:
        response = await client.async_get_and_save_items(filepath=filepath)
        open_mock.assert_called_with(filepath, mode='xb', **default_open_args)
        open_mock.return_value.write.assert_called_once_with(json_data)

    assert response == ('decorator_with_params', ('simple_decorator', None))


def test_bad_decorator_type():
    with pytest.raises(ValidationError) as err:
        FitConfig.from_dict(
            base_url='https://test.skillcorner',
            client_name='client_with_default_decorators',
            method_decorators=[None],
            method_config_list=[
                {
                    'name': 'get_index',
                    'endpoint': '/',
                }
            ],
        )
    assert isinstance(err.value.errors()[0]['ctx']['error'], InvalidMethodDecoratorError)


def test_unknown_decorator_string():
    with pytest.raises(ValidationError) as err:
        FitConfig.from_dict(
            base_url='https://test.skillcorner',
            client_name='client_with_default_decorators',
            method_decorators=["fake_auth(user='toto')"],
            method_config_list=[
                {
                    'name': 'get_index',
                    'endpoint': '/',
                }
            ],
        )
    assert isinstance(err.value.errors()[0]['ctx']['error'], InvalidMethodDecoratorError)
