import httpx
from fixtures import client_with_custom_headers, config_with_basic_credentials, config_with_url


def test_session_is_instanciated(config_with_url):
    client = config_with_url.fit_class()
    assert isinstance(client.session.synchronous, httpx.Client)
    assert isinstance(client.session.asynchronous, httpx.AsyncClient)


def test_session_attribute_is_not_none(config_with_url):
    client = config_with_url.fit_class()
    assert client.session is not None
    assert client.session.synchronous is not None
    assert client.session.asynchronous is not None


def test_session_auth(config_with_url, config_with_basic_credentials):
    client = config_with_url.fit_class()
    client_env = config_with_basic_credentials.fit_class()

    assert client.session.synchronous.auth is None
    assert client.session.asynchronous.auth is None
    assert client_env.session.synchronous.auth is not None
    assert client_env.session.asynchronous.auth is not None


def test_session_headers(config_with_url):
    client = config_with_url.fit_class()
    session_user_agent = client.session.synchronous.headers.get('user-agent')
    async_session_user_agent = client.session.asynchronous.headers.get('user-agent')
    assert session_user_agent == 'fitrequest.client_with_url.{version}'
    assert async_session_user_agent == 'fitrequest.client_with_url.{version}'


def test_session_custom_headers(client_with_custom_headers):
    client = client_with_custom_headers
    sync_headers = client.session.synchronous.headers
    async_headers = client.session.asynchronous.headers

    assert sync_headers.get('user-agent') == 'fitrequest.client_with_custom_headers.{version}'
    assert async_headers.get('user-agent') == 'fitrequest.client_with_custom_headers.{version}'
    assert sync_headers.get('SOME_FIELD') == 'SOME_VALUE'
    assert async_headers.get('SOME_FIELD') == 'SOME_VALUE'
