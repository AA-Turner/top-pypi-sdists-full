import httpx
import pytest
import respx

from tests.demo import (
    RestApiConfig,
    client_default,
    client_from_dict,
    client_from_json,
    client_from_yaml,
    client_with_specific_args,
)
from tests.demo_custom_init_session import (
    RestApiConfig,
    client_default_custom_init_session,
    client_from_dict_custom_init_session,
    client_from_json_custom_init_session,
    client_from_yaml_custom_init_session,
    client_with_specific_args_custom_init_session,
)
from tests.demo_decorator import client_decorated
from tests.demo_decorator_custom_init_session import client_decorated_custom_init_session
from tests.demo_decorator_pydantic_return import client_pydantic_return
from tests.demo_decorator_request_params import client_decorated_request_params
from tests.demo_decorator_with_username_password_init import client_decorated_with_username_password_init
from tests.demo_lazy_config import client_lazy_config
from tests.demo_lazy_config_custom_init_session import client_lazy_config_custom_init_session
from tests.demo_lazy_config_custom_init_session_base_url import client_lazy_config_custom_init_session_base_url
from tests.demo_lazy_config_request_params import client_lazy_config_request_params
from tests.demo_mix import client_mix
from tests.demo_mix_custom_init_session import client_mix_custom_init_session


@pytest.mark.parametrize(
    'client',
    [
        client_default,
        client_with_specific_args,
        client_from_json,
        client_from_yaml,
        client_from_dict,
        client_lazy_config,
        client_decorated,
        client_mix,
        client_pydantic_return,
        client_decorated_request_params,
        client_lazy_config_request_params,
    ],
)
def test_methods(client):
    """
    Verifies that every fit method is available across various fitrequest syntaxes
    and ensures that all generated methods include a 'fit_method' attribute set to True.
    """
    for method in ('get_items', 'async_get_items', 'get_item', 'get_item_details'):
        assert hasattr(client, method)
        assert hasattr(getattr(client, method), 'fit_method')
        assert getattr(client, method).fit_method


@pytest.mark.parametrize(
    'client',
    [
        client_default,
        client_with_specific_args,
        client_from_json,
        client_from_yaml,
        client_from_dict,
        client_lazy_config,
        client_decorated,
        client_mix,
        client_pydantic_return,
        client_decorated_request_params,
        client_lazy_config_request_params,
    ],
)
def test_independent_sessions_between_instances(client):
    client2 = client.__class__()
    assert client.session is not client2.session


@pytest.mark.parametrize(
    'client_to_compare',
    [
        client_default,
        client_from_json,
        client_from_yaml,
        client_from_dict,
        client_lazy_config,
        client_decorated,
        client_mix,
        client_default_custom_init_session,
        client_from_json_custom_init_session,
        client_from_yaml_custom_init_session,
        client_from_dict_custom_init_session,
    ],
)
def test_clients_properties(client_to_compare):
    client = RestApiConfig().fit_class()
    assert client.client_name == client_to_compare.client_name
    assert client.version == client_to_compare.version
    assert client.base_url == client_to_compare.base_url


@pytest.mark.parametrize(
    'client_to_compare',
    [
        client_default,
        client_from_json,
        client_from_yaml,
        client_from_dict,
        client_lazy_config,
        client_decorated,
        client_mix,
    ],
)
def test_clients_auth(client_to_compare):
    client = RestApiConfig().fit_class()
    assert client.auth == client_to_compare.auth


@pytest.mark.parametrize(
    'client_to_compare',
    [
        client_default_custom_init_session,
        client_from_json_custom_init_session,
        client_from_yaml_custom_init_session,
        client_from_dict_custom_init_session,
    ],
)
def test_clients_custom_init_auth(client_to_compare):
    assert client_to_compare.auth == {
        'password': {'env_name': 'API_PASSWORD', 'init_value': '1234'},
        'username': {'env_name': 'API_USERNAME', 'init_value': 'toto'},
    }


def test_clients_properties_diff():
    client = RestApiConfig().fit_class()
    assert client.client_name == client_with_specific_args.client_name
    assert client.version == client_with_specific_args.version
    assert client.base_url != client_with_specific_args.base_url
    assert client.auth == client_with_specific_args.auth


@pytest.mark.parametrize(
    'client',
    [
        client_default,
        client_from_json,
        client_from_yaml,
        client_from_dict,
        client_lazy_config,
        client_decorated,
        client_mix,
    ],
)
@respx.mock
def test_method_get_items(client):
    expected = {
        'items': [
            {'item_id': 1, 'item_name': 'ball'},
            {'item_id': 2, 'item_name': 'gloves'},
        ]
    }
    respx.get('https://test.skillcorner.fr').mock(return_value=httpx.Response(200, json=expected))
    response = client.get_items()
    assert response == expected


@pytest.mark.parametrize(
    'client',
    [
        client_default,
        client_from_json,
        client_from_yaml,
        client_from_dict,
        client_lazy_config,
        client_decorated,
        client_mix,
    ],
)
@respx.mock
def test_method_get_item(client):
    item_id = 1
    expected = {'item_id': item_id, 'item_name': 'ball'}
    respx.get(f'https://test.skillcorner.fr/items/{item_id}').mock(return_value=httpx.Response(200, json=expected))
    response = client.get_item(item_id=item_id)
    assert response == expected


@pytest.mark.parametrize(
    'client',
    [
        client_default,
        client_from_json,
        client_from_yaml,
        client_from_dict,
        client_lazy_config,
        client_decorated,
        client_mix,
    ],
)
@respx.mock
def test_method_get_item_details(client):
    item_id = 1
    detail_id = 7
    expected = {'item_id': item_id, 'detail_id': detail_id, 'item_name': 'ball', 'detail': 'color white'}
    respx.get(f'https://test.skillcorner.fr/items/{item_id}/details/{detail_id}').mock(
        return_value=httpx.Response(200, json=expected)
    )
    response = client.get_item_details(item_id=item_id, detail_id=detail_id)
    assert response == expected


@pytest.mark.parametrize(
    'client',
    [
        client_default,
        client_from_json,
        client_from_yaml,
        client_from_dict,
        client_lazy_config,
        client_decorated,
        client_mix,
    ],
)
@respx.mock
@pytest.mark.asyncio
async def test_method_async_get_items(client):
    expected = {
        'items': [
            {'item_id': 1, 'item_name': 'ball'},
            {'item_id': 2, 'item_name': 'gloves'},
        ]
    }
    respx.get('https://test.skillcorner.fr').mock(return_value=httpx.Response(200, json=expected))
    response = await client.async_get_items()
    assert response == expected


@pytest.mark.parametrize(
    'client',
    [
        client_default,
        client_with_specific_args,
        client_from_json,
        client_from_yaml,
        client_from_dict,
        client_lazy_config,
        client_decorated,
        client_mix,
        client_pydantic_return,
        client_decorated_request_params,
        client_lazy_config_request_params,
    ],
)
def test_docstring(client):
    docstring = 'Calling endpoint: {endpoint}'

    assert client.get_items.__doc__ == docstring.format(endpoint='/items/')
    assert client.get_items.__doc__ == client.async_get_items.__doc__
    assert client.get_item.__doc__ == docstring.format(endpoint='/items/{item_id}')
    assert client.get_item_details.__doc__ == docstring.format(endpoint='/items/{item_id}/details/{detail_id}')


@pytest.mark.parametrize(
    'client',
    [
        client_default,
        client_from_json,
        client_from_yaml,
        client_from_dict,
        client_lazy_config,
        client_decorated,
        client_mix,
        client_pydantic_return,
        client_decorated_request_params,
        client_lazy_config_request_params,
    ],
)
def test_class_attributes(client):
    assert client.client_name == 'rest_api'
    assert client.version == '{version}'
    assert client.base_url == 'https://test.skillcorner.fr'
    assert client.auth is None
    assert not hasattr(client, 'method_docstring')
    assert not hasattr(client, 'method_config_list')

    assert client.session.config == {
        'headers': {
            'User-Agent': 'fitrequest.rest_api.{version}',
        },
        'follow_redirects': True,
        'timeout': 60,
    }
    assert client.session.raw_auth is None


@pytest.mark.parametrize(
    'client',
    [
        client_default_custom_init_session,
        client_from_json_custom_init_session,
        client_from_yaml_custom_init_session,
        client_from_dict_custom_init_session,
        client_lazy_config_custom_init_session,
        client_decorated_custom_init_session,
        client_mix_custom_init_session,
    ],
)
def test_custom_session_config(client):
    raw_auth = client.session.raw_auth
    httpx_auth = client.session.synchronous.auth
    session_base_url = client.session.base_url

    assert client.session.config == {
        'headers': {
            'User-Agent': 'fitrequest.rest_api.{version}',
            'SOME_FIELD': 'SOME_VALUE',
        },
        'follow_redirects': True,
        'timeout': 20,
        'verify': False,
    }
    assert isinstance(httpx_auth, httpx.BasicAuth)
    assert vars(httpx_auth) == {'_auth_header': 'Basic dG90bzoxMjM0'}
    assert raw_auth == {
        'password': {'env_name': 'API_PASSWORD', 'init_value': '1234'},
        'username': {'env_name': 'API_USERNAME', 'init_value': 'toto'},
    }
    assert session_base_url == 'https://test.skillcorner.fr'


def test_custom_session_config_with_config_custom_base_url():
    client = client_with_specific_args_custom_init_session
    raw_auth = client.session.raw_auth
    httpx_auth = client.session.synchronous.auth
    session_base_url = client.session.base_url

    assert client.session.config == {
        'headers': {
            'User-Agent': 'fitrequest.rest_api.{version}',
            'SOME_FIELD': 'SOME_VALUE',
        },
        'follow_redirects': True,
        'timeout': 20,
        'verify': False,
    }
    assert isinstance(httpx_auth, httpx.BasicAuth)
    assert vars(httpx_auth) == {'_auth_header': 'Basic dG90bzoxMjM0'}
    assert raw_auth == {
        'password': {'env_name': 'API_PASSWORD', 'init_value': '1234'},
        'username': {'env_name': 'API_USERNAME', 'init_value': 'toto'},
    }
    assert session_base_url == 'https://staging.skillcorner.fr:8080'


def test_custom_session_base_url():
    client = client_lazy_config_custom_init_session_base_url
    raw_auth = client.session.raw_auth
    httpx_auth = client.session.synchronous.auth
    session_base_url = client.session.base_url

    assert client.session.config == {
        'headers': {
            'User-Agent': 'fitrequest.rest_api.{version}',
        },
        'follow_redirects': True,
        'timeout': 60,
    }
    assert isinstance(httpx_auth, httpx.BasicAuth)
    assert vars(httpx_auth) == {'_auth_header': 'Basic dG90bzoxMjM0'}
    assert raw_auth == {
        'password': {'env_name': 'API_PASSWORD', 'init_value': '1234'},
        'username': {'env_name': 'API_USERNAME', 'init_value': 'toto'},
    }
    assert session_base_url == 'https://test.skillcorner.fr'


def test_authenticate_with_init_username_password():
    username = 'toto'
    password = '1234'
    expected = httpx.BasicAuth(username, password)
    client = client_decorated_with_username_password_init

    assert client.session.synchronous.auth is not None
    assert client.session.asynchronous.auth is not None
    assert vars(client.session.synchronous.auth) == vars(expected)
    assert vars(client.session.asynchronous.auth) == vars(expected)
