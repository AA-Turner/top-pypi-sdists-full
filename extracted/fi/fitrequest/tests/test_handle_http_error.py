from unittest.mock import patch

import httpx
import pytest

from fitrequest.errors import HTTPStatusError
from fitrequest.response import Response


def test_handle_http_error():
    httpx_response = httpx.Response(200)
    with patch.object(httpx_response, '_request'):
        try:
            Response(httpx_response=httpx_response).handle_http_error()
        except HTTPStatusError:
            pytest.fail('Unexpected HTTPStatusError raised')


def test_handle_response_raise_no_content():
    httpx_response = httpx.Response(404, content=b'')
    mock_url = 'mock.com'

    with (
        patch.object(httpx_response, '_request'),
        patch.object(httpx_response._request, 'url', mock_url),
        pytest.raises(HTTPStatusError) as excinfo,
    ):
        Response(httpx_response=httpx_response).data

    assert excinfo.value.args == (404, b'', None)


def test_handle_response_raise_no_content_and_401():
    httpx_response = httpx.Response(401, content=b'')
    with patch.object(httpx_response, '_request'), pytest.raises(HTTPStatusError) as excinfo:
        Response(client_name='toto_client', httpx_response=httpx_response).data
    assert excinfo.value.args == (
        401,
        b'',
        'Invalid toto_client credentials. '
        'Make sure settings are provided during initialization or set as environment variables.',
    )


def test_handle_response_raise_with_content():
    httpx_response = httpx.Response(400, content=b'Custom error message')
    with patch.object(httpx_response, '_request'), pytest.raises(HTTPStatusError) as excinfo:
        Response(httpx_response=httpx_response).data
    assert excinfo.value.args == (400, b'Custom error message', None)


def test_handle_response_raise_with_content_and_401():
    httpx_response = httpx.Response(401, content=b'Custom error message')

    with patch.object(httpx_response, '_request'), pytest.raises(HTTPStatusError) as excinfo:
        Response(client_name='toto_client', httpx_response=httpx_response).data
    assert excinfo.value.args == (
        401,
        b'Custom error message',
        'Invalid toto_client credentials. '
        'Make sure settings are provided during initialization or set as environment variables.',
    )
