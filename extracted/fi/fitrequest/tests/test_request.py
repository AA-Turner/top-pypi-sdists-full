from unittest.mock import patch

import httpx
import pytest
from fixtures import config_with_url

from fitrequest.errors import HTTPStatusError
from fitrequest.method_config import MethodConfig, RequestVerb


@pytest.mark.parametrize('verb', list(RequestVerb))
def test_get_request_default_args(config_with_url, verb):
    response = httpx.Response(200)
    with (
        patch.object(response, '_request'),
        patch.object(httpx.Client, 'request', return_value=response) as mock,
    ):
        config_with_url.fit_class().session.request(
            MethodConfig(base_url=config_with_url.base_url, name='test', request_verb=verb, endpoint='ok/')
        )
    mock.assert_called_once_with(
        method=verb.value,
        url='https://test.skillcorner/ok/',
        params=None,
    )


@pytest.mark.parametrize('verb', list(RequestVerb))
def test_session_base_url(config_with_url, verb):
    response = httpx.Response(200)
    with (
        patch.object(response, '_request'),
        patch.object(httpx.Client, 'request', return_value=response) as mock,
    ):
        client = config_with_url.fit_class()
        client.session.update(base_url='https://staging-env.skillcorner/')
        client.session.request(
            MethodConfig(base_url=config_with_url.base_url, name='test', request_verb=verb, endpoint='ok/')
        )
    mock.assert_called_once_with(
        method=verb.value,
        url='https://staging-env.skillcorner/ok/',
        params=None,
    )


def test_get_request_with_raise_for_status_default(config_with_url):
    response = httpx.Response(500)
    with (
        patch.object(response, '_request'),
        patch.object(httpx.Client, 'request', return_value=response) as mock,
        pytest.raises(HTTPStatusError),
    ):
        config_with_url.fit_class().session.request(
            MethodConfig(
                base_url=config_with_url.base_url,
                name='test',
                request_verb=RequestVerb.get,
                endpoint='raise/',
            )
        )
    mock.assert_called_once_with(
        method='GET',
        url='https://test.skillcorner/raise/',
        params=None,
    )


def test_get_request_with_raise_for_status_false(config_with_url):
    response = httpx.Response(500)
    with (
        patch.object(response, '_request'),
        patch.object(httpx.Client, 'request', return_value=response) as mock,
    ):
        config_with_url.fit_class().session.request(
            MethodConfig(
                base_url=config_with_url.base_url,
                name='test',
                request_verb=RequestVerb.get,
                endpoint='ok/',
                raise_for_status=False,
            )
        )
    mock.assert_called_once_with(
        method='GET',
        url='https://test.skillcorner/ok/',
        params=None,
    )


def test_get_request_with_raise_for_status_true(config_with_url):
    response = httpx.Response(500)
    with (
        patch.object(response, '_request'),
        patch.object(httpx.Client, 'request', return_value=response) as mock,
        pytest.raises(HTTPStatusError),
    ):
        config_with_url.fit_class().session.request(
            MethodConfig(
                base_url=config_with_url.base_url,
                name='test',
                request_verb=RequestVerb.get,
                endpoint='raise/',
                raise_for_status=True,
            )
        )
    mock.assert_called_once_with(
        method='GET',
        url='https://test.skillcorner/raise/',
        params=None,
    )


def test_get_request_with_params(config_with_url):
    response = httpx.Response(200)
    with (
        patch.object(response, '_request'),
        patch.object(httpx.Client, 'request', return_value=response) as mock,
    ):
        config_with_url.fit_class().session.request(
            MethodConfig(
                base_url=config_with_url.base_url,
                name='test',
                request_verb=RequestVerb.get,
                endpoint='ok/',
            ),
            params={'foo': 'bar', 'param_list': [1, 2, 3, 4]},
        )
    mock.assert_called_once_with(
        method='GET',
        url='https://test.skillcorner/ok/',
        params={'foo': 'bar', 'param_list': [1, 2, 3, 4]},
    )


def test_get_request_with_url_params(config_with_url):
    response = httpx.Response(200)
    with (
        patch.object(response, '_request'),
        patch.object(httpx.Client, 'request', return_value=response) as mock,
    ):
        config_with_url.fit_class().session.request(
            MethodConfig(
                base_url=config_with_url.base_url,
                name='test',
                request_verb=RequestVerb.get,
                endpoint='ok?lang=fr&country=canada',
            ),
        )
    mock.assert_called_once_with(
        method='GET',
        url='https://test.skillcorner/ok',
        params={'lang': ['fr'], 'country': ['canada']},
    )


def test_post_request_with_data(config_with_url):
    data = {'key': 'value'}
    response = httpx.Response(200)
    with (
        patch.object(response, '_request'),
        patch.object(httpx.Client, 'request', return_value=response) as mock,
    ):
        config_with_url.fit_class().session.request(
            MethodConfig(
                base_url=config_with_url.base_url,
                name='test',
                request_verb=RequestVerb.post,
                endpoint='ok/',
            ),
            data=data,
        )
    mock.assert_called_once_with(
        method='POST',
        url='https://test.skillcorner/ok/',
        params=None,
        data={'key': 'value'},
    )


def test_post_request_with_json(config_with_url):
    _json = [1, 2, 3]
    response = httpx.Response(200)
    with (
        patch.object(response, '_request'),
        patch.object(httpx.Client, 'request', return_value=response) as mock,
    ):
        config_with_url.fit_class().session.request(
            MethodConfig(
                base_url=config_with_url.base_url,
                name='test',
                request_verb=RequestVerb.post,
                endpoint='ok/',
            ),
            json=_json,
        )
    mock.assert_called_once_with(
        method='POST',
        url='https://test.skillcorner/ok/',
        params=None,
        json=[1, 2, 3],
    )


def test_get_request_with_custom_url(config_with_url):
    response = httpx.Response(200)
    with (
        patch.object(response, '_request'),
        patch.object(httpx.Client, 'request', return_value=response) as mock,
    ):
        config_with_url.fit_class().session.request(
            MethodConfig(
                base_url=config_with_url.base_url,
                name='test',
                request_verb=RequestVerb.get,
                endpoint='ok/',
            ),
            url='www.toto.com',
        )
    mock.assert_called_once_with(
        method='GET',
        url='www.toto.com',
        params=None,
    )


def test_get_request_with_custom_url_and_hardcoded_params(config_with_url):
    response = httpx.Response(200)
    with (
        patch.object(response, '_request'),
        patch.object(httpx.Client, 'request', return_value=response) as mock,
    ):
        config_with_url.fit_class().session.request(
            MethodConfig(
                base_url=config_with_url.base_url,
                name='test',
                request_verb=RequestVerb.get,
                endpoint='ok/',
            ),
            url='www.toto.com?token=1234&lang=fr',
        )
        mock.assert_called_once_with(
            method='GET',
            url='www.toto.com',
            params={'token': ['1234'], 'lang': ['fr']},
        )


def test_get_request_with_custom_url_and_request_params(config_with_url):
    response = httpx.Response(200)
    with (
        patch.object(response, '_request'),
        patch.object(httpx.Client, 'request', return_value=response) as mock,
    ):
        config_with_url.fit_class().session.request(
            MethodConfig(
                base_url=config_with_url.base_url,
                name='test',
                request_verb=RequestVerb.get,
                endpoint='ok/',
            ),
            url='www.toto.com',
            params={'token': ['5678'], 'lang': ['en']},
        )
        mock.assert_called_once_with(
            method='GET',
            url='www.toto.com',
            params={'token': ['5678'], 'lang': ['en']},
        )


def test_get_request_with_custom_url_and_multiple_params_sources(config_with_url):
    response = httpx.Response(200)
    with (
        patch.object(response, '_request'),
        patch.object(httpx.Client, 'request', return_value=response) as mock,
    ):
        config_with_url.fit_class().session.request(
            MethodConfig(
                base_url=config_with_url.base_url,
                name='test',
                request_verb=RequestVerb.get,
                endpoint='ok/',
            ),
            url='www.toto.com?token=1234&lang=fr&page=1',
            params={'token': ['5678'], 'lang': ['en'], 'id': ['10']},
        )
        # URL parameters and argument parameters are combined,
        # with URL parameters taking precedence over argument parameters.
        mock.assert_called_once_with(
            method='GET',
            url='www.toto.com',
            params={'token': ['1234'], 'lang': ['fr'], 'page': ['1'], 'id': ['10']},
        )
