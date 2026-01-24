import inspect
import json
from enum import Enum
from typing import Literal
from unittest.mock import MagicMock, mock_open, patch

import httpx
import pytest
import respx
from pydantic import Field
from typer.testing import CliRunner

from fitrequest.cli_utils import add_httpx_args, literal_to_enum, transform_field_info, transform_literals
from fitrequest.errors import HTTPStatusError, UnexpectedLiteralTypeError
from tests.demo_cli import RestApiClient, client_cli

runner = CliRunner()


@pytest.fixture
def cli_database() -> dict:
    return {
        'version': '1.2.3',
        'items': {
            1: {'item_id': 1, 'item_name': 'ball', 'detail_id': 11},
            2: {'item_id': 2, 'item_name': 'gloves', 'detail_id': 22},
        },
        'details': {
            11: {
                'detail_id': 11,
                'detail': 'Durable ball made from soft synthetic leather with wider seams and bright colors',
            },
            22: {
                'detail_id': 22,
                'detail': (
                    'Small, light, made from soft material that fits snugly. Textured fingertips provide excellent grip'
                ),
            },
        },
    }


def mock_requests(cli_database):
    item_list = list(cli_database['items'].values())
    respx.get(
        f'{client_cli.base_url}/version/',
    ).mock(return_value=httpx.Response(200, json={'version': cli_database['version']}))

    respx.get(
        f'{client_cli.base_url}/items/',
    ).mock(return_value=httpx.Response(200, json=item_list))

    for item in cli_database['items'].values():
        item_id = item['item_id']
        detail_id = item['detail_id']
        detail = cli_database['details'][detail_id]

        respx.get(
            f'{client_cli.base_url}/items/{item_id}',
        ).mock(return_value=httpx.Response(200, json=item))

        respx.get(
            f'{client_cli.base_url}/items/{item_id}/details/{detail_id}',
        ).mock(return_value=httpx.Response(200, json=item | detail))


@respx.mock
def test_get_items(cli_database):
    mock_requests(cli_database)

    # Test methods
    assert [elem.model_dump() for elem in client_cli.get_items()] == [
        {'item_id': 1, 'item_name': 'ball', 'detail_id': 11},
        {'item_id': 2, 'item_name': 'gloves', 'detail_id': 22},
    ]

    # Test CLI
    result = runner.invoke(client_cli.cli_app(), ['get-items'])
    assert result.exit_code == 0
    assert 'ball' in result.stdout
    assert 'gloves' in result.stdout


@respx.mock
def test_get_version(cli_database):
    mock_requests(cli_database)

    # Private methods
    assert client_cli._get_version() == {'version': cli_database['version']}

    # But cli command doesn't exists (command is not public)
    result = runner.invoke(client_cli.cli_app(), ['get-version'])
    assert result.exit_code != 0

    result = runner.invoke(client_cli.cli_app(), ['_get-version'])
    assert result.exit_code != 0

    result = runner.invoke(client_cli.cli_app(), ['-get-version'])
    assert result.exit_code != 0


@respx.mock
def test_get_item(cli_database):
    mock_requests(cli_database)

    # Test methods
    assert client_cli.get_item(item_id=1).model_dump() == {'item_id': 1, 'item_name': 'ball', 'detail_id': 11}
    assert client_cli.get_item(item_id=2).model_dump() == {'item_id': 2, 'item_name': 'gloves', 'detail_id': 22}

    # Test CLI
    result = runner.invoke(client_cli.cli_app(), ['get-item', '1'])
    assert result.exit_code == 0
    assert 'ball' in result.stdout

    result = runner.invoke(client_cli.cli_app(), ['get-item', '2'])
    assert result.exit_code == 0
    assert 'gloves' in result.stdout


@respx.mock
def test_get_item_details(cli_database):
    mock_requests(cli_database)

    # Test methods
    assert client_cli.get_item_details(item_id=1, detail_id=11).model_dump() == {
        'item_id': 1,
        'item_name': 'ball',
        'detail_id': 11,
        'detail': 'Durable ball made from soft synthetic leather with wider seams and bright colors',
    }
    assert client_cli.get_item_details(item_id=2, detail_id=22).model_dump() == {
        'item_id': 2,
        'item_name': 'gloves',
        'detail_id': 22,
        'detail': 'Small, light, made from soft material that fits snugly. Textured fingertips provide excellent grip',
    }

    # Test CLI
    result = runner.invoke(client_cli.cli_app(), ['get-item-details', '1', '11'])
    cleaned_output = result.stdout.replace('\n', ' ').replace('  ', ' ')

    assert result.exit_code == 0
    assert 'ball' in cleaned_output
    assert 'Durable ball made from soft synthetic leather with wider seams and bright colors' in cleaned_output

    result = runner.invoke(client_cli.cli_app(), ['get-item-details', '2', '22'])
    cleaned_output = result.stdout.replace('\n', ' ').replace('  ', ' ')

    assert result.exit_code == 0
    assert 'gloves' in cleaned_output
    assert (
        'Small, light, made from soft material that fits snugly. Textured fingertips provide excellent grip'
        in cleaned_output
    )


@respx.mock
def test_get_details(cli_database):
    mock_requests(cli_database)

    # Test methods
    assert [elem.model_dump() for elem in client_cli.get_details()] == [
        {
            'item_id': 1,
            'item_name': 'ball',
            'detail_id': 11,
            'detail': 'Durable ball made from soft synthetic leather with wider seams and bright colors',
        },
        {
            'item_id': 2,
            'item_name': 'gloves',
            'detail_id': 22,
            'detail': (
                'Small, light, made from soft material that fits snugly. Textured fingertips provide excellent grip'
            ),
        },
    ]

    # Test CLI
    result = runner.invoke(client_cli.cli_app(), ['get-details'])
    cleaned_output = result.stdout.replace('\n', ' ').replace('  ', ' ')

    assert result.exit_code == 0
    assert 'ball' in cleaned_output
    assert 'gloves' in cleaned_output
    assert 'Durable ball made from soft synthetic leather with wider seams and bright colors' in cleaned_output
    assert (
        'Small, light, made from soft material that fits snugly. Textured fingertips provide excellent grip'
        in cleaned_output
    )


@respx.mock
def test_cli_request_error(cli_database):
    err_msg = 'Item not found!'
    err_msg_bytes = b'Item not found!'

    respx.get(
        f'{client_cli.base_url}/items/3',
    ).mock(return_value=httpx.Response(404, text=err_msg))

    mock_requests(cli_database)

    # Test methods
    with pytest.raises(HTTPStatusError) as err:
        client_cli.get_item(item_id=3)

    assert err.value.args == (404, err_msg_bytes, None)

    # Test CLI
    result = runner.invoke(client_cli.cli_app(), ['get-item', '3'])
    assert result.exit_code == 1
    assert err_msg in result.stdout


def test_typer_inputs():
    result = runner.invoke(
        client_cli.cli_app(), ['get-inputs', '1234', '--limit', '2', '--sort', 'name', '--order', 'desc']
    )
    assert result.exit_code == 0

    result_data = json.loads(result.stdout)
    assert result_data == {
        'item_id': 1234,
        'limit': 2,
        'sort': 'name',
        'order': 'desc',
    }


def test_literal_to_enum():
    class VolumeEnum(Enum):
        low = 'low'
        medium = 'medium'
        high = 'high'

    new_enum = literal_to_enum('VolumeEnum', Literal['low', 'medium', 'high'])
    assert [elem.value for elem in VolumeEnum] == [elem.value for elem in new_enum]
    assert new_enum.__name__ == 'VolumeEnum'


def test_literal_to_enum_bad_type():
    with pytest.raises(UnexpectedLiteralTypeError):
        literal_to_enum('VolumeEnum', int)


def test_transform_field_info():
    @transform_field_info
    def toto(
        name: str,
        age: int = Field(alias='HowOld'),
        tags: str = Field(default_factory=lambda: ['test', 'fieldinfo']),
        lang: Literal['en', 'fr'] = Field(alias='language', default='en'),
    ) -> None: ...

    transformed_fields = {param.name: param.default for param in inspect.signature(toto).parameters.values()}
    assert transformed_fields == {
        'name': inspect.Parameter.empty,
        'age': inspect.Parameter.empty,
        'tags': ['test', 'fieldinfo'],
        'lang': 'en',
    }


def test_transform_field_info_with_literals():
    @transform_field_info
    @transform_literals
    def toto(
        name: str,
        age: int = Field(alias='HowOld'),
        tags: str = Field(default_factory=lambda: ['test', 'fieldinfo']),
        lang: Literal['en', 'fr'] = Field(alias='language', default='en'),
    ) -> None: ...

    transformed_fields = {param.name: param.default for param in inspect.signature(toto).parameters.values()}
    assert transformed_fields == {
        'name': inspect.Parameter.empty,
        'age': inspect.Parameter.empty,
        'tags': ['test', 'fieldinfo'],
        'lang': 'en',
    }


def test_add_httpx_args_no_kwargs():
    @add_httpx_args
    def toto(name: str, age: int) -> None: ...

    # Nothing changed because there is no kwargs in signature.
    assert sorted(inspect.signature(toto).parameters) == sorted(['name', 'age'])


def test_async_add_httpx_args_no_kwargs():
    @add_httpx_args
    async def toto(name: str, age: int) -> None: ...

    # Nothing changed because there is no kwargs in signature.
    assert sorted(inspect.signature(toto).parameters) == sorted(['name', 'age'])


def test_add_httpx_args_kwargs():
    @add_httpx_args
    def toto(name: str, age: int, **kwargs) -> None: ...

    # Added httpx arguments.
    assert sorted(inspect.signature(toto).parameters) == sorted(['name', 'age', 'content', 'data', 'json', 'kwargs'])

    open_mock = mock_open()
    with patch('builtins.open', open_mock), patch('json.load'):
        toto(name='John', age='33', json='/path/json', content='/path/content', data='/path/data')

    # 3 calls
    assert open_mock.call_count == 3
    open_mock.assert_any_call('/path/json')
    open_mock.assert_any_call('/path/data')
    open_mock.assert_any_call('/path/content', mode='rb')

    # 0 call
    open_mock = mock_open()
    with patch('builtins.open', open_mock):
        toto(name='John', age='33')

    assert open_mock.call_count == 0

    # 1 call
    open_mock = mock_open()
    with patch('builtins.open', open_mock), patch('json.load'):
        toto(name='John', age='33', json='/path/json')

    assert open_mock.call_count == 1
    open_mock.assert_called_with('/path/json')


@pytest.mark.asyncio
async def test_async_add_httpx_args_kwargs():
    @add_httpx_args
    async def toto(name: str, age: int, **kwargs) -> None: ...

    # Added httpx arguments.
    assert sorted(inspect.signature(toto).parameters) == sorted(['name', 'age', 'content', 'data', 'json', 'kwargs'])

    open_mock = mock_open()
    with patch('builtins.open', open_mock), patch('json.load'):
        await toto(name='John', age='33', json='/path/json', content='/path/content', data='/path/data')

    assert open_mock.call_count == 3
    open_mock.assert_any_call('/path/json')
    open_mock.assert_any_call('/path/data')
    open_mock.assert_any_call('/path/content', mode='rb')

    # 0 call
    open_mock = mock_open()
    with patch('builtins.open', open_mock):
        await toto(name='John', age='33')

    assert open_mock.call_count == 0

    # 1 call
    open_mock = mock_open()
    with patch('builtins.open', open_mock), patch('json.load'):
        await toto(name='John', age='33', json='/path/json')

    assert open_mock.call_count == 1
    open_mock.assert_called_with('/path/json')


def test_add_httpx_args_with_existing_reserved_names():
    # Added "json" parameters
    @add_httpx_args
    def toto(name: str, age: int, json: str = 'hey!', **kwargs) -> None:
        assert json == 'hey again!'

    # Added httpx arguments, except "json" that already existed in the signature.
    assert sorted(inspect.signature(toto).parameters) == sorted(['name', 'age', 'content', 'data', 'json', 'kwargs'])

    open_mock = mock_open()
    with patch('builtins.open', open_mock), patch('json.load'):
        toto(name='John', age='33', json='hey again!', content='/path/content', data='/path/data')

    assert open_mock.call_count == 2
    open_mock.assert_any_call('/path/data')
    open_mock.assert_any_call('/path/content', mode='rb')


@pytest.mark.asyncio
async def test_async_add_httpx_args_with_existing_reserved_names():
    # Added "json" parameters
    @add_httpx_args
    async def toto(name: str, age: int, json: str = 'hey!', **kwargs) -> None:
        assert json == 'hey again!'

    # Added httpx arguments, except "json" that already existed in the signature.
    assert sorted(inspect.signature(toto).parameters) == sorted(['name', 'age', 'content', 'data', 'json', 'kwargs'])

    open_mock = mock_open()
    with patch('builtins.open', open_mock), patch('json.load'):
        await toto(name='John', age='33', json='hey again!', content='/path/content', data='/path/data')

    assert open_mock.call_count == 2
    open_mock.assert_any_call('/path/data')
    open_mock.assert_any_call('/path/content', mode='rb')


def test_cli_run():
    RestApiClient.cli_app = MagicMock()
    RestApiClient.cli_run()
    RestApiClient.cli_app.assert_called()
