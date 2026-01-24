from unittest import mock

import aiofiles
import httpx
import orjson
import pytest
import respx
from fixtures import (
    config_with_async_methods,
    config_with_default_docstring,
    config_with_default_docstring_and_variables,
    config_with_methods,
)

from fitrequest.errors import HTTPStatusError, UnrecognizedParametersError

aiofiles.threadpool.wrap.register(mock.MagicMock)(
    lambda *args, **kwargs: aiofiles.threadpool.AsyncBufferedIOBase(*args, **kwargs)
)


@pytest.mark.asyncio
async def test_methods_missing_url_params(config_with_methods):
    client = config_with_methods.fit_class()

    with pytest.raises(TypeError):
        await client.async_get_item()
    with pytest.raises(TypeError):
        await client.async_get_with_multiple_params()
    with pytest.raises(TypeError):
        await client.async_get_with_multiple_params(team_id=2, user_id=6)


@respx.mock
@pytest.mark.asyncio
async def test_methods_binding_call_method(config_with_async_methods):
    expected = {
        'items': [
            {'item_id': 1, 'item_name': 'ball'},
            {'item_id': 2, 'item_name': 'gloves'},
        ]
    }
    respx.get(
        'https://test.skillcorner.fr/items/',
    ).mock(return_value=httpx.Response(200, json=expected))
    response = await config_with_async_methods.fit_class().async_get_items()
    assert response == expected


@respx.mock
@pytest.mark.asyncio
async def test_methods_custom_url(config_with_async_methods):
    custom_url = 'https://custom.skillcorner.fr/items/'
    expected = {
        'items': [
            {'item_id': 1, 'item_name': 'ball'},
            {'item_id': 2, 'item_name': 'gloves'},
        ]
    }
    respx.get(custom_url).mock(return_value=httpx.Response(200, json=expected))
    response = await config_with_async_methods.fit_class().async_get_items(url=custom_url)
    assert response == expected


@respx.mock
@pytest.mark.asyncio
async def test_methods_custom_method(config_with_async_methods):
    expected = {
        'items': [
            {'item_id': 1, 'item_name': 'ball'},
            {'item_id': 2, 'item_name': 'gloves'},
        ]
    }
    respx.post(
        'https://test.skillcorner.fr/items/',
    ).mock(return_value=httpx.Response(200, json=expected))
    response = await config_with_async_methods.fit_class().async_get_items(method='POST')
    assert response == expected


@respx.mock
@pytest.mark.asyncio
async def test_methods_custom_url_and_method(config_with_async_methods):
    custom_url = 'https://custom.skillcorner.fr/items/'
    expected = {
        'items': [
            {'item_id': 1, 'item_name': 'ball'},
            {'item_id': 2, 'item_name': 'gloves'},
        ]
    }
    respx.put(custom_url).mock(return_value=httpx.Response(200, json=expected))
    response = await config_with_async_methods.fit_class().async_get_items(url=custom_url, method='PUT')
    assert response == expected


def test_methods_binding_with_default_docstring(config_with_default_docstring):
    expected = 'Template of docstring used in every method.'
    value_1 = config_with_default_docstring.fit_class().async_get_item.__doc__
    value_2 = config_with_default_docstring.fit_class().async_get_items.__doc__
    assert value_1 == value_2 == expected


def test_methods_binding_with_default_docstring_ignored(
    config_with_default_docstring,
):
    expected = 'Template is ignored if set.'
    value = config_with_default_docstring.fit_class().async_get_dosctring_set.__doc__
    assert value == expected


def test_methods_binding_with_docstring_and_variables_template(
    config_with_default_docstring_and_variables,
):
    expected = 'Calling endpoint: /items/\nDocs URL anchor: /items/items_list'
    value = config_with_default_docstring_and_variables.fit_class().async_get_items.__doc__
    assert value == expected


def test_methods_binding_with_default_docstring_and_variables_template_ignored(
    config_with_default_docstring_and_variables,
):
    expected = 'Template is ignored if set.'
    value = config_with_default_docstring_and_variables.fit_class().async_get_item.__doc__
    assert value == expected


def test_methods_binding_with_default_docstring_and_docstring_but_no_variables(
    config_with_default_docstring_and_variables,
):
    config = config_with_default_docstring_and_variables
    expected = 'Its own docstring.'
    value = config.fit_class().async_get_with_no_docstring_variable_but_dosctring_set.__doc__
    assert value == expected


@respx.mock
@pytest.mark.asyncio
async def test_methods_binding_call_method_with_id(config_with_async_methods):
    expected = {'item_id': 1, 'item_name': 'ball'}
    item_id = 32
    respx.get(f'https://test.skillcorner.fr/items/{item_id}').mock(return_value=httpx.Response(200, json=expected))
    response = await config_with_async_methods.fit_class().async_get_item(item_id=item_id)
    assert response == expected


@pytest.mark.asyncio
async def test_methods_binding_call_method_with_endpoint_arg(config_with_async_methods):
    with pytest.raises(UnrecognizedParametersError):
        await config_with_async_methods.fit_class().async_get_item(32, endpoint='gitlab.com/test-project')


@pytest.mark.asyncio
async def test_methods_binding_call_method_with_request_verb_arg(
    config_with_async_methods,
):
    with pytest.raises(UnrecognizedParametersError):
        await config_with_async_methods.fit_class().async_get_item(25, request_verb='PUT')


def test_methods_binding_docstring_none(config_with_async_methods):
    value = config_with_async_methods.fit_class().async_get_default_args.__doc__
    assert not value


def test_methods_binding_docstring_empty(config_with_async_methods):
    value = config_with_async_methods.fit_class().async_get_doc_none_if_empty.__doc__
    assert not value


def test_methods_binding_docstring(config_with_async_methods):
    expected = 'Here is a description of the method.'
    value = config_with_async_methods.fit_class().async_get_docstring.__doc__
    assert value == expected


@respx.mock
@pytest.mark.asyncio
async def test_methods_binding_with_json_path(config_with_async_methods):
    expected = [
        {'user_id': 1, 'user_name': 'Motta'},
        {'user_id': 2, 'user_name': 'Busquets'},
    ]
    respx.get('https://test.skillcorner.fr/json-path/').mock(
        return_value=httpx.Response(
            200,
            json={
                'data': expected,
                'metadata': {'total_count': 2},
            },
        )
    )
    response = await config_with_async_methods.fit_class().async_get_value_in_json_path()
    assert response == expected


@respx.mock
@pytest.mark.asyncio
async def test_methods_binding_with_json_path_but_not_dict(
    config_with_async_methods,
):
    expected = [
        {
            'data': [
                {'user_id': 1, 'user_name': 'Motta'},
                {'user_id': 2, 'user_name': 'Busquets'},
            ]
        }
    ]
    respx.get('https://test.skillcorner.fr/json-path/').mock(return_value=httpx.Response(200, json=expected))
    response = await config_with_async_methods.fit_class().async_get_value_in_json_path()
    assert response == expected[0]['data']


@respx.mock
@pytest.mark.asyncio
async def test_methods_binding_with_json_path_with_multiple_elems_in_jsonpath(config_with_async_methods):
    data = [
        {
            'data': [
                {'user_id': 1, 'user_name': 'Motta'},
                {'user_id': 2, 'user_name': 'Busquets'},
            ]
        },
        {
            'data': [
                {'user_id': 3, 'user_name': 'John'},
                {'user_id': 4, 'user_name': 'Doe'},
            ]
        },
    ]
    expected = [
        [
            {'user_id': 1, 'user_name': 'Motta'},
            {'user_id': 2, 'user_name': 'Busquets'},
        ],
        [
            {'user_id': 3, 'user_name': 'John'},
            {'user_id': 4, 'user_name': 'Doe'},
        ],
    ]
    respx.get('https://test.skillcorner.fr/json-path/').mock(return_value=httpx.Response(200, json=data))
    response = await config_with_async_methods.fit_class().async_get_value_in_json_path()
    assert response == expected


@respx.mock
@pytest.mark.asyncio
async def test_methods_binding_with_json_path_but_missing_jsonpath(
    config_with_async_methods,
):
    expected = [
        {
            'no_data_field': [
                {'user_id': 1, 'user_name': 'Motta'},
                {'user_id': 2, 'user_name': 'Busquets'},
            ]
        }
    ]
    respx.get('https://test.skillcorner.fr/json-path/').mock(return_value=httpx.Response(200, json=expected))
    response = await config_with_async_methods.fit_class().async_get_value_in_json_path()
    assert response is None


@respx.mock
@pytest.mark.asyncio
async def test_methods_binding_with_no_raise_on_status(config_with_async_methods):
    respx.get('https://test.skillcorner.fr/raise-on-status/false').mock(return_value=httpx.Response(404))
    assert (await config_with_async_methods.fit_class().async_get_no_raise_on_status()) is None


@respx.mock
@pytest.mark.asyncio
async def test_methods_binding_with_raise_on_status_404(config_with_async_methods):
    respx.get('https://test.skillcorner.fr/raise-on-status/true').mock(return_value=httpx.Response(404))
    with pytest.raises(HTTPStatusError):
        await config_with_async_methods.fit_class().async_get_raise_for_status()


@respx.mock
@pytest.mark.asyncio
async def test_methods_binding_with_raise_on_status_500(config_with_async_methods):
    respx.get('https://test.skillcorner.fr/raise-on-status/true').mock(return_value=httpx.Response(500))

    with pytest.raises(HTTPStatusError):
        await config_with_async_methods.fit_class().async_get_raise_for_status()


@respx.mock
@pytest.mark.asyncio
async def test_methods_binding_with_random_kwargs(config_with_async_methods):
    with pytest.raises(UnrecognizedParametersError):
        await config_with_async_methods.fit_class().async_get_default_args(kwarg1='foo', kwarg2='bar')


@respx.mock
@pytest.mark.asyncio
async def test_methods_binding_with_save_method_without_params(
    config_with_async_methods,
):
    body = {'best_team_name': 'Paris Saint-Germain'}
    filepath = 'test_save.json'
    expected = orjson.dumps(body, option=orjson.OPT_INDENT_2)

    respx.get('https://test.skillcorner.fr/save-method/').mock(return_value=httpx.Response(200, json=body))

    file_chunks_iter = iter(expected)
    mock_file_stream = mock.MagicMock(read=lambda: next(file_chunks_iter))
    default_open_args = {
        'buffering': -1,
        'encoding': None,
        'errors': None,
        'newline': None,
        'closefd': True,
        'opener': None,
    }

    with mock.patch('aiofiles.threadpool.sync_open', return_value=mock_file_stream) as mock_open:
        await config_with_async_methods.fit_class().async_get_with_save_method(filepath=filepath)
        mock_open.assert_called_with(filepath, mode='xb', **default_open_args)
        mock_file_stream.write.assert_called_once_with(expected)


@respx.mock
@pytest.mark.asyncio
async def test_methods_binding_with_save_method_with_params(config_with_async_methods):
    body = {'item_id': 17, 'item_name': 'ball'}
    item_id = 17
    filepath = 'test_save_items.json'
    expected = orjson.dumps(body, option=orjson.OPT_INDENT_2)

    respx.get(f'https://test.skillcorner.fr/items/{item_id}').mock(return_value=httpx.Response(200, json=body))

    file_chunks_iter = iter(expected)
    mock_file_stream = mock.MagicMock(read=lambda: next(file_chunks_iter))
    default_open_args = {
        'buffering': -1,
        'encoding': None,
        'errors': None,
        'newline': None,
        'closefd': True,
        'opener': None,
    }

    with mock.patch('aiofiles.threadpool.sync_open', return_value=mock_file_stream) as mock_open:
        await config_with_async_methods.fit_class().async_save_item(item_id=item_id, filepath=filepath)
        mock_open.assert_called_with(filepath, mode='xb', **default_open_args)
        mock_open.return_value.write.assert_called_once_with(expected)


@pytest.mark.asyncio
async def test_methods_binding_without_save_method(config_with_async_methods):
    with pytest.raises(AttributeError):
        await config_with_async_methods.fit_class().async_save_without_save_method()


@pytest.mark.asyncio
async def test_methods_binding_with_unknown_positional_arg(config_with_async_methods):
    with pytest.raises(TypeError):
        await config_with_async_methods.fit_class().async_get_default_args(
            'first_arg_is_params', 'second_arg_is_raise_for_status', 'unknown_arg'
        )
