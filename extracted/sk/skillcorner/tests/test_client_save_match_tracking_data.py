from unittest.mock import mock_open, patch

import httpx
import orjson
import pytest
import respx

from skillcorner.client import SkillcornerClient


@respx.mock
def test_save_match_tracking_data():
    expected = orjson.dumps([{'frame': 1}, {'frame': 2}, {'frame': 3}], option=orjson.OPT_INDENT_2)
    content = b'{"frame": 1}\n{"frame": 2}\n{"frame": 3}\n'
    match_id = 42
    filepath = f'match_{match_id}_tracking_data.json'

    response = httpx.Response(
        200,
        content=content,
        headers={'Content-Type': 'application/json-l'},
    )
    respx.get(f'https://skillcorner.com/api/match/{match_id}/tracking').mock(return_value=response)

    open_mock = mock_open()
    with patch('builtins.open', open_mock, create=True):
        SkillcornerClient().save_match_tracking_data(match_id=match_id, filepath=filepath)

    open_mock.assert_called_with(filepath, mode='xb')
    open_mock.return_value.write.assert_called_once_with(expected)


@respx.mock
def test_save_match_tracking_data_with_params_file_format_jsonl():
    content = b'{"frame": 1}\n{"frame": 2}\n'
    match_id = 421
    filepath = f'match_{match_id}_tracking_data.json'
    expected = orjson.dumps([{'frame': 1}, {'frame': 2}], option=orjson.OPT_INDENT_2)

    response = httpx.Response(
        200,
        content=content,
        headers={'Content-Type': 'application/json-l'},
    )
    respx.get(f'https://skillcorner.com/api/match/{match_id}/tracking').mock(return_value=response)

    open_mock = mock_open()
    with patch('builtins.open', open_mock, create=True):
        SkillcornerClient().save_match_tracking_data(
            match_id=match_id, filepath=filepath, params={'file_format': 'jsonl'}
        )

    open_mock.assert_called_with(filepath, mode='xb')
    open_mock.return_value.write.assert_called_once_with(expected)


@respx.mock
def test_save_match_tracking_data_with_params_file_format_fifa_data():
    content = b'<root><child name="child1">Fifa data</child></root>'
    match_id = 421
    filepath = f'match_{match_id}_tracking_data.txt'

    response = httpx.Response(
        200,
        content=content,
        headers={'Content-Type': 'binary/octet-stream'},
    )
    respx.get(f'https://skillcorner.com/api/match/{match_id}/tracking').mock(return_value=response)

    open_mock = mock_open()
    with patch('builtins.open', open_mock, create=True):
        SkillcornerClient().save_match_tracking_data(
            match_id=match_id, filepath=filepath, params={'file_format': 'fifa-data'}
        )

    open_mock.assert_called_with(filepath, mode='xb')
    open_mock.return_value.write.assert_called_once_with(content)


@respx.mock
def test_save_match_tracking_data_with_params_file_format_fifa_xml():
    expected = b"<?xml version='1.0' encoding='utf-8'?>\n<root><child name=\"child1\">Fifa xml</child></root>"

    content = b'<root><child name="child1">Fifa xml</child></root>'
    match_id = 4321
    filepath = f'match_{match_id}_tracking_data.xml'

    response = httpx.Response(
        200,
        content=content,
        headers={'Content-Type': 'application/xml'},
    )
    respx.get(f'https://skillcorner.com/api/match/{match_id}/tracking').mock(return_value=response)

    open_mock = mock_open()
    with patch('builtins.open', open_mock, create=True):
        SkillcornerClient().save_match_tracking_data(
            match_id=match_id, filepath=filepath, params={'file_format': 'fifa-xml'}
        )

    open_mock.assert_called_with(filepath, mode='xb')
    open_mock.return_value.write.assert_called_once_with(expected)


@respx.mock
def test_get_and_save_match_tracking_data():
    with pytest.raises(
        AttributeError,
        match="'SkillcornerClient' object has no attribute 'get_and_save_match_tracking_data'",  # noqa: E501
    ):
        SkillcornerClient().get_and_save_match_tracking_data(match_id=10, filepath='test.json')
