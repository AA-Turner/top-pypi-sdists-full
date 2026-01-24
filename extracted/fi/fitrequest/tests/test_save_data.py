from pathlib import Path
from unittest.mock import mock_open, patch

import httpx
import orjson
import pytest
from pydantic import BaseModel

from fitrequest.response import Response


def test_save_data_bytes():
    filepath = 'bytes_saved.txt'
    expected = b'test data'
    httpx_response = httpx.Response(200, content=expected)

    open_mock = mock_open()
    with patch('builtins.open', open_mock, create=True), patch.object(httpx_response, '_request'):
        Response(httpx_response=httpx_response).save_data(filepath)
    open_mock.assert_called_with(filepath, mode='xb')
    open_mock.return_value.write.assert_called_once_with(expected)


def test_save_none_data():
    filepath = 'bytes_saved.txt'
    expected = b''
    httpx_response = httpx.Response(200, content=None)

    open_mock = mock_open()
    with patch('builtins.open', open_mock, create=True), patch.object(httpx_response, '_request'):
        Response(httpx_response=httpx_response).save_data(filepath)
    open_mock.assert_called_with(filepath, mode='xb')
    open_mock.return_value.write.assert_called_once_with(expected)


def test_save_data_json():
    filepath = 'test.json'
    data = {'id': 35, 'area': 'AFC', 'name': 'Asian Cup'}
    expected = orjson.dumps(data, option=orjson.OPT_INDENT_2)
    httpx_response = httpx.Response(200, json=data)

    open_mock = mock_open()
    with patch('builtins.open', open_mock, create=True), patch.object(httpx_response, '_request'):
        Response(httpx_response=httpx_response).save_data(filepath)
    open_mock.assert_called_with(filepath, mode='xb')
    open_mock.return_value.write.assert_called_once_with(expected)


def test_save_data_json_pydantic():
    class Cup(BaseModel):
        id: int
        area: str
        name: str

    filepath = 'test.json'
    data = {'id': 35, 'area': 'AFC', 'name': 'Asian Cup'}
    expected = orjson.dumps(data, option=orjson.OPT_INDENT_2)
    httpx_response = httpx.Response(200, json=data)

    open_mock = mock_open()
    with patch('builtins.open', open_mock, create=True), patch.object(httpx_response, '_request'):
        Response(httpx_response=httpx_response, response_model=Cup).save_data(filepath)
    open_mock.assert_called_with(filepath, mode='xb')
    open_mock.return_value.write.assert_called_once_with(expected)


def test_save_data_json_list_pydantic():
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

    open_mock = mock_open()
    with patch('builtins.open', open_mock, create=True), patch.object(httpx_response, '_request'):
        Response(httpx_response=httpx_response, response_model=Cup).save_data(filepath)
    open_mock.assert_called_with(filepath, mode='xb')
    open_mock.return_value.write.assert_called_once_with(expected)


def test_save_data_element():
    filepath = 'test.xml'
    raw_data = '<root>data</root>'
    expected = bytes(f"<?xml version='1.0' encoding='utf-8'?>\n{raw_data}", encoding='utf-8')
    httpx_response = httpx.Response(200, text=raw_data, headers={'Content-Type': 'xml'})

    open_mock = mock_open()
    with patch('builtins.open', open_mock, create=True), patch.object(httpx_response, '_request'):
        Response(httpx_response=httpx_response).save_data(filepath)
    open_mock.assert_called_with(filepath, mode='xb')
    open_mock.return_value.write.assert_called_once_with(expected)


def test_save_data_invalid_path():
    httpx_response = httpx.Response(200, content='awesome content')

    with patch.object(httpx_response, '_request'), pytest.raises(FileNotFoundError):
        Response(httpx_response=httpx_response).save_data('/invalid/unknown/path/test/test.json')


def test_save_data_file_already_exists():
    filepath = Path('test_file.toto')
    httpx_response = httpx.Response(200, content='awesome content')

    with filepath.open(mode='w') as new_file:
        new_file.write('erase this test file')

    with patch.object(httpx_response, '_request'), pytest.raises(FileExistsError):
        Response(httpx_response=httpx_response).save_data(str(filepath))

    filepath.unlink()
