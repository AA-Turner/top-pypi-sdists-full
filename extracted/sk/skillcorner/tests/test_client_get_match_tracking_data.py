from xml.etree import ElementTree

import httpx
import pytest
import respx
from defusedxml.ElementTree import fromstring
from fitrequest.errors import UnrecognizedParametersError

from skillcorner.client import SkillcornerClient


@respx.mock
def test_get_match_tracking_data():
    content = b'{"frame": 1}\n{"frame": 2}\n{"frame": 3}\n'
    match_id = 42
    expected = [{'frame': 1}, {'frame': 2}, {'frame': 3}]

    response = httpx.Response(
        200,
        content=content,
        headers={'Content-Type': 'application/json-l'},
    )
    respx.get(f'https://skillcorner.com/api/match/{match_id}/tracking').mock(return_value=response)

    response = SkillcornerClient().get_match_tracking_data(match_id=match_id)
    assert response == expected


@respx.mock
def test_get_match_tracking_data_with_params_file_format_jsonl():
    content = b'{"frame": 1}\n{"frame": 2}\n{"frame": 3}\n'
    match_id = 138
    expected = [{'frame': 1}, {'frame': 2}, {'frame': 3}]

    response = httpx.Response(
        200,
        content=content,
        headers={'Content-Type': 'application/json-l'},
    )
    respx.get(f'https://skillcorner.com/api/match/{match_id}/tracking').mock(return_value=response)

    response = SkillcornerClient().get_match_tracking_data(match_id, params={'file_format': 'jsonl'})
    assert response == expected


@respx.mock
def test_get_match_tracking_data_with_params_file_format_fifa_data():
    content = b'<root><child name="child1">Fifa data</child></root>'
    match_id = 12

    response = httpx.Response(
        200,
        content=content,
        headers={'Content-Type': 'binary/octet-stream'},
    )
    respx.get(f'https://skillcorner.com/api/match/{match_id}/tracking').mock(return_value=response)

    response = SkillcornerClient().get_match_tracking_data(match_id, params={'file_format': 'fifa-data'})
    assert response == content


@respx.mock
def test_get_match_tracking_data_with_params_file_format_fifa_xml():
    content = b'<root><child name="child1">Fifa xml</child></root>'
    match_id = 2006
    expected = fromstring(content)

    response = httpx.Response(
        200,
        content=content,
        headers={'Content-Type': 'application/xml'},
    )
    respx.get(f'https://skillcorner.com/api/match/{match_id}/tracking').mock(return_value=response)

    response = SkillcornerClient().get_match_tracking_data(match_id, params={'file_format': 'fifa-xml'})
    assert ElementTree.tostring(response) == ElementTree.tostring(expected)


@respx.mock
def test_get_match_tracking_data_with_params_file_format_unknown():
    content = b'{"frame": 1}\n{"frame": 2}\n{"frame": 3}\n'
    match_id = 89
    expected = [{'frame': 1}, {'frame': 2}, {'frame': 3}]

    response = httpx.Response(
        200,
        content=content,
        headers={'Content-Type': 'application/json-l'},
    )
    respx.get(f'https://skillcorner.com/api/match/{match_id}/tracking').mock(return_value=response)

    response = SkillcornerClient().get_match_tracking_data(match_id, params={'file_format': 'unknown'})
    assert response == expected


@respx.mock
def test_get_match_tracking_data_with_params_typo_or_unknown():
    content = b'{"frame": 1}\n{"frame": 2}\n{"frame": 3}\n'
    match_id = 2018
    expected = [{'frame': 1}, {'frame': 2}, {'frame': 3}]

    response = httpx.Response(
        200,
        content=content,
        headers={'Content-Type': 'application/json-l'},
    )
    respx.get(f'https://skillcorner.com/api/match/{match_id}/tracking').mock(return_value=response)

    response = SkillcornerClient().get_match_tracking_data(match_id, params={'fileformat': 'any'})
    assert response == expected


@respx.mock
def test_get_match_tracking_data_with_random_kwargs():
    content = b'{"frame": 1}\n{"frame": 2}\n{"frame": 3}\n'
    match_id = 5077

    response = httpx.Response(
        200,
        content=content,
        headers={'Content-Type': 'application/json-l'},
    )
    respx.get(f'https://skillcorner.com/api/match/{match_id}/tracking').mock(return_value=response)

    with pytest.raises(UnrecognizedParametersError):
        SkillcornerClient().get_match_tracking_data(match_id, kwarg_1='kwarg_1', kwarg_2='kwarg_2')


@respx.mock
def test_get_match_tracking_data_with_unknown_arg():
    with pytest.raises(TypeError):
        match_id = 1998
        SkillcornerClient().get_match_tracking_data(
            match_id, {'unused_param': 'foo'}, 'raise_for_status_arg', 'unknown_arg'
        )
