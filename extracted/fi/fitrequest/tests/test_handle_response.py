from unittest.mock import patch
from xml.etree.ElementTree import Element as XmlElement

import defusedxml.ElementTree as XmlTree
import httpx
import orjson
import pytest
from pydantic import BaseModel
from pydantic_core import ValidationError

from fitrequest.client import FitRequest
from fitrequest.errors import HTTPStatusError, InvalidResponseTypeError
from fitrequest.response import Response


def test_handle_response_empty_response():
    httpx_response = httpx.Response(200)

    with patch.object(httpx_response, '_request'):
        assert Response(httpx_response=httpx_response).data is None


def test_handle_response_csv_response():
    csv_bytes = b'A,B\r\n1,2\r\n3,4\r\n'
    httpx_response = httpx.Response(200, content=csv_bytes)

    with patch.object(httpx_response, '_request'):
        resp_data = Response(httpx_response=httpx_response).data

    assert isinstance(resp_data, bytes)
    assert csv_bytes == resp_data


def test_handle_response_jsonlines_response():
    expected = [{'key1': '1', 'key2': 2}, {'key3': '3', 'key4': 4}]
    headers = {'Content-Type': 'application/jsonlines'}
    content = b'{"key1":"1","key2":2}\r\n{"key3":"3","key4":4}'
    httpx_response = httpx.Response(200, headers=headers, content=content)

    with patch.object(httpx_response, '_request'):
        assert Response(httpx_response=httpx_response).data == expected


def test_handle_response_html():
    expected = 'nice html response'
    headers = {'Content-Type': 'text/html'}
    content = b'nice html response'
    httpx_response = httpx.Response(200, headers=headers, content=content)

    with patch.object(httpx_response, '_request'):
        assert Response(httpx_response=httpx_response).data == expected


def test_handle_response_html_no_content_type():
    expected = b'nice html response'
    content = b'nice html response'
    httpx_response = httpx.Response(200, content=content)

    with patch.object(httpx_response, '_request'):
        assert Response(httpx_response=httpx_response).data == expected


def test_handle_response_json():
    expected = {'key1': '1', 'key2': 2}
    headers = {'Content-Type': 'application/json'}
    content = b'{"key1":"1","key2":2}'
    httpx_response = httpx.Response(200, headers=headers, content=content)

    with patch.object(httpx_response, '_request'):
        assert Response(httpx_response=httpx_response).data == expected


def test_handle_response_json_204():
    headers = {'Content-Type': 'application/json'}
    httpx_response = httpx.Response(204, headers=headers)

    with patch.object(httpx_response, '_request'):
        assert Response(httpx_response=httpx_response).data is None


def test_handle_response_json_no_content_type():
    expected = orjson.dumps({'key1': '1', 'key2': 2})
    content = b'{"key1":"1","key2":2}'
    httpx_response = httpx.Response(200, content=content)

    with patch.object(httpx_response, '_request'):
        assert Response(httpx_response=httpx_response).data == expected


def test_handle_response_raise_for_status():
    httpx_response = httpx.Response(400)

    with patch.object(httpx_response, '_request'), pytest.raises(HTTPStatusError):
        Response(httpx_response=httpx_response).data


def test_handle_response_raise_for_status_false():
    httpx_response = httpx.Response(400)

    with patch.object(httpx_response, '_request'):
        assert Response(httpx_response=httpx_response, raise_for_status=False).data is None


def test_handle_response_txt():
    expected = 'foo bar'
    headers = {'Content-Type': 'text/plain'}
    content = b'foo bar'
    httpx_response = httpx.Response(200, headers=headers, content=content)

    with patch.object(httpx_response, '_request'):
        assert Response(httpx_response=httpx_response).data == expected


def test_handle_response_txt_no_content_type():
    expected = b'foo bar'
    content = b'foo bar'
    httpx_response = httpx.Response(200, content=content)

    with patch.object(httpx_response, '_request'):
        assert Response(httpx_response=httpx_response).data == expected


def test_handle_response_unknown_content_type():
    expected = b'foo bar'
    headers = {'Content-Type': 'application/unknown'}
    content = b'foo bar'
    httpx_response = httpx.Response(200, headers=headers, content=content)

    with patch.object(httpx_response, '_request'):
        assert Response(httpx_response=httpx_response).data == expected


def test_handle_response_xml():
    expected = XmlTree.fromstring('<root><child name="child1">Content 1</child></root>')
    headers = {'Content-Type': 'application/xml'}
    content = '<root><child name="child1">Content 1</child></root>'
    httpx_response = httpx.Response(200, headers=headers, content=content)

    with patch.object(httpx_response, '_request'):
        response = Response(httpx_response=httpx_response)
        assert isinstance(response.data, XmlElement)
        assert XmlTree.tostring(response.data) == XmlTree.tostring(expected)


def test_handle_response_xml_no_content_type():
    expected = b'<root><child name="child1">Content 1</child></root>'
    content = b'<root><child name="child1">Content 1</child></root>'
    httpx_response = httpx.Response(200, content=content)

    with patch.object(httpx_response, '_request'):
        assert Response(httpx_response=httpx_response).data == expected


def test_handle_response_json_with_json_path():
    expected = ['goubet', 'doe']
    content = b"""[
        {"first_name": "lucien", "last_name": "goubet"},
        {"first_name": "john", "last_name": "doe"}
    ]"""
    headers = {'Content-Type': 'application/json'}
    httpx_response = httpx.Response(200, headers=headers, content=content)

    with patch.object(httpx_response, '_request'):
        assert Response(httpx_response=httpx_response, json_path='[*].last_name').data == expected


def test_handle_response_json_with_pydantic_model():
    class Person(BaseModel):
        first_name: str
        last_name: str

    content = b"""{"first_name": "lucien", "last_name": "goubet"}"""
    headers = {'Content-Type': 'application/json'}
    httpx_response = httpx.Response(200, headers=headers, content=content)

    with patch.object(httpx_response, '_request'):
        lg = Response(httpx_response=httpx_response, response_model=Person).data

    assert isinstance(lg, Person)
    assert lg.model_dump() == {'first_name': 'lucien', 'last_name': 'goubet'}


def test_handle_response_json_list_with_pydantic_model():
    class Person(BaseModel):
        first_name: str
        last_name: str

    content = b"""[
        {"first_name": "lucien", "last_name": "goubet"},
        {"first_name": "john", "last_name": "doe"}
    ]"""
    headers = {'Content-Type': 'application/json'}
    httpx_response = httpx.Response(200, headers=headers, content=content)
    expected_list_size = 2

    with patch.object(httpx_response, '_request'):
        person_list = Response(httpx_response=httpx_response, response_model=Person).data

    assert isinstance(person_list, list)
    assert len(person_list) == expected_list_size

    lg, jd = person_list
    assert isinstance(lg, Person)
    assert isinstance(jd, Person)
    assert lg.model_dump() == {'first_name': 'lucien', 'last_name': 'goubet'}
    assert jd.model_dump() == {'first_name': 'john', 'last_name': 'doe'}


def test_handle_response_json_with_bad_pydantic_model():
    # Bad pydantic model
    class Person:
        first_name: str
        last_name: str

    content = b"""{"first_name": "lucien", "last_name": "goubet"}"""
    headers = {'Content-Type': 'application/json'}
    httpx_response = httpx.Response(200, headers=headers, content=content)

    with patch.object(httpx_response, '_request'):
        lg = Response(httpx_response=httpx_response, response_model=Person).data

    # The incorrect pydantic model is ignored
    assert isinstance(lg, dict)
    assert lg == {'first_name': 'lucien', 'last_name': 'goubet'}


def test_handle_response_not_json_with_pydantic_model():
    class Person(BaseModel):
        first_name: str
        last_name: str

    content = b"""{"first_name": "lucien", "last_name": "goubet"}"""
    expected = """{"first_name": "lucien", "last_name": "goubet"}"""

    # Value will be interpreted as plain text
    headers = {'Content-Type': 'text/plain'}
    httpx_response = httpx.Response(200, headers=headers, content=content)

    with patch.object(httpx_response, '_request'):
        lg = Response(httpx_response=httpx_response, response_model=Person).data

    # The string data will not be formated by pydantic model
    assert isinstance(lg, str)
    assert lg == expected


def test_bad_reponse_model_type():
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
