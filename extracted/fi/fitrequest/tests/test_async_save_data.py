from pathlib import Path
from unittest import mock

import aiofiles
import httpx
import orjson
import pytest
from pydantic import BaseModel

from fitrequest.response import Response

aiofiles.threadpool.wrap.register(mock.MagicMock)(
    lambda *args, **kwargs: aiofiles.threadpool.AsyncBufferedIOBase(*args, **kwargs)
)


@pytest.mark.asyncio
async def test_save_data_bytes():
    filepath = 'bytes_saved.txt'
    expected = b'test data'
    httpx_response = httpx.Response(200, content=expected)

    mock_file_stream = mock.MagicMock(read=lambda: next(iter(expected)))
    default_open_args = {
        'buffering': -1,
        'encoding': None,
        'errors': None,
        'newline': None,
        'closefd': True,
        'opener': None,
    }

    with (
        mock.patch('aiofiles.threadpool.sync_open', return_value=mock_file_stream) as open_mock,
        mock.patch.object(httpx_response, '_request'),
    ):
        await Response(httpx_response=httpx_response).async_save_data(filepath)
        open_mock.assert_called_with(filepath, mode='xb', **default_open_args)
        open_mock.return_value.write.assert_called_once_with(expected)


@pytest.mark.asyncio
async def test_save_none_data():
    filepath = 'bytes_saved.txt'
    expected = b''
    httpx_response = httpx.Response(200, content=None)

    mock_file_stream = mock.MagicMock(read=lambda: next(iter(expected)))
    default_open_args = {
        'buffering': -1,
        'encoding': None,
        'errors': None,
        'newline': None,
        'closefd': True,
        'opener': None,
    }

    with (
        mock.patch('aiofiles.threadpool.sync_open', return_value=mock_file_stream) as open_mock,
        mock.patch.object(httpx_response, '_request'),
    ):
        await Response(httpx_response=httpx_response).async_save_data(filepath)
        open_mock.assert_called_with(filepath, mode='xb', **default_open_args)
        open_mock.return_value.write.assert_called_once_with(expected)


@pytest.mark.asyncio
async def test_save_data_json():
    filepath = 'test.json'
    data = {'id': 35, 'area': 'AFC', 'name': 'Asian Cup'}
    expected = orjson.dumps(data, option=orjson.OPT_INDENT_2)
    httpx_response = httpx.Response(200, json=data)

    mock_file_stream = mock.MagicMock(read=lambda: next(iter(expected)))
    default_open_args = {
        'buffering': -1,
        'encoding': None,
        'errors': None,
        'newline': None,
        'closefd': True,
        'opener': None,
    }

    with (
        mock.patch('aiofiles.threadpool.sync_open', return_value=mock_file_stream) as open_mock,
        mock.patch.object(httpx_response, '_request'),
    ):
        await Response(httpx_response=httpx_response).async_save_data(filepath)
        open_mock.assert_called_with(filepath, mode='xb', **default_open_args)
        open_mock.return_value.write.assert_called_once_with(expected)


@pytest.mark.asyncio
async def test_save_data_json_pydantic():
    class Cup(BaseModel):
        id: int
        area: str
        name: str

    filepath = 'test.json'
    data = {'id': 35, 'area': 'AFC', 'name': 'Asian Cup'}
    expected = orjson.dumps(data, option=orjson.OPT_INDENT_2)
    httpx_response = httpx.Response(200, json=data)

    mock_file_stream = mock.MagicMock(read=lambda: next(iter(expected)))
    default_open_args = {
        'buffering': -1,
        'encoding': None,
        'errors': None,
        'newline': None,
        'closefd': True,
        'opener': None,
    }

    with (
        mock.patch('aiofiles.threadpool.sync_open', return_value=mock_file_stream) as open_mock,
        mock.patch.object(httpx_response, '_request'),
    ):
        await Response(httpx_response=httpx_response, response_model=Cup).async_save_data(filepath)
        open_mock.assert_called_with(filepath, mode='xb', **default_open_args)
        open_mock.return_value.write.assert_called_once_with(expected)


@pytest.mark.asyncio
async def test_save_data_json_list_pydantic():
    class Cup(BaseModel):
        id: int
        area: str
        name: str

    filepath = 'test.json'
    data = [
        {'id': 35, 'area': 'AFC', 'name': 'Asian Cup'},
        {'id': 36, 'area': 'EFC', 'name': 'European Cup'},
    ]
    expected = orjson.dumps(data, option=orjson.OPT_INDENT_2)
    httpx_response = httpx.Response(200, json=data)

    mock_file_stream = mock.MagicMock(read=lambda: next(iter(expected)))
    default_open_args = {
        'buffering': -1,
        'encoding': None,
        'errors': None,
        'newline': None,
        'closefd': True,
        'opener': None,
    }

    with (
        mock.patch('aiofiles.threadpool.sync_open', return_value=mock_file_stream) as open_mock,
        mock.patch.object(httpx_response, '_request'),
    ):
        await Response(httpx_response=httpx_response, response_model=Cup).async_save_data(filepath)
        open_mock.assert_called_with(filepath, mode='xb', **default_open_args)
        open_mock.return_value.write.assert_called_once_with(expected)


@pytest.mark.asyncio
async def test_save_data_element():
    filepath = 'test.xml'
    raw_data = '<root>data</root>'
    expected = bytes(f"<?xml version='1.0' encoding='utf-8'?>\n{raw_data}", encoding='utf-8')
    httpx_response = httpx.Response(200, text=raw_data, headers={'Content-Type': 'xml'})

    mock_file_stream = mock.MagicMock(read=lambda: next(iter(expected)))
    default_open_args = {
        'buffering': -1,
        'encoding': None,
        'errors': None,
        'newline': None,
        'closefd': True,
        'opener': None,
    }

    with (
        mock.patch('aiofiles.threadpool.sync_open', return_value=mock_file_stream) as open_mock,
        mock.patch.object(httpx_response, '_request'),
    ):
        await Response(httpx_response=httpx_response).async_save_data(filepath)
        open_mock.assert_called_with(filepath, mode='xb', **default_open_args)
        open_mock.return_value.write.assert_called_once_with(expected)


@pytest.mark.asyncio
async def test_save_data_invalid_path():
    httpx_response = httpx.Response(200, content='awesome content')

    with mock.patch.object(httpx_response, '_request'), pytest.raises(FileNotFoundError):
        await Response(httpx_response=httpx_response).async_save_data('/invalid/unknown/path/test/test.json')


@pytest.mark.asyncio
async def test_save_data_file_already_exists():
    filepath = Path('test_file.toto')
    httpx_response = httpx.Response(200, content='awesome content')

    async with aiofiles.open(str(filepath), mode='w') as new_file:
        await new_file.write('erase this test file')

    with mock.patch.object(httpx_response, '_request'), pytest.raises(FileExistsError):
        await Response(httpx_response=httpx_response).async_save_data(str(filepath))

    filepath.unlink()
