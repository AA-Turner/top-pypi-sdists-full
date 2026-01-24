import httpx
import respx

from tests.demo_decorator_verbs import (
    RestApiClient,
    client_decorated_verbs as client,
)


def test_methods():
    for method in ('get_item', 'put_item', 'post_item', 'delete_item'):
        assert hasattr(client, method)
        assert hasattr(getattr(client, method), 'fit_method')
        assert getattr(client, method).fit_method


@respx.mock
def test_method_get_item():
    item_id = 1
    expected = {'item_id': item_id, 'item_name': 'ball'}
    respx.get(f'https://test.skillcorner.fr/items/{item_id}').mock(return_value=httpx.Response(200, json=expected))
    response = client.get_item(item_id=item_id)
    assert response == expected


@respx.mock
def test_method_put_item():
    item_id = 1
    json_data = {'item_id': item_id, 'item_name': 'ball'}
    expected = {'item_id': item_id, 'status': 'updated'}
    respx.put(f'https://test.skillcorner.fr/items/{item_id}', json=json_data).mock(
        return_value=httpx.Response(200, json=expected)
    )
    response = client.put_item(item_id=item_id, json=json_data)
    assert response == expected


@respx.mock
def test_method_post_item():
    item_id = 1
    json_data = {'item_id': item_id, 'item_name': 'ball'}
    expected = {'item_id': item_id, 'status': 'created'}
    respx.post(f'https://test.skillcorner.fr/items/{item_id}', json=json_data).mock(
        return_value=httpx.Response(200, json=expected)
    )
    response = client.post_item(item_id=item_id, json=json_data)
    assert response == expected


@respx.mock
def test_method_patch_item():
    item_id = 1
    json_data = {'item_id': item_id, 'item_name': 'ball'}
    expected = {'item_id': item_id, 'status': 'updated'}
    respx.patch(f'https://test.skillcorner.fr/items/{item_id}', json=json_data).mock(
        return_value=httpx.Response(200, json=expected)
    )
    response = client.patch_item(item_id=item_id, json=json_data)
    assert response == expected


@respx.mock
def test_method_delete_item():
    item_id = 1
    expected = {'item_id': item_id, 'status': 'deleted'}
    respx.delete(f'https://test.skillcorner.fr/items/{item_id}').mock(return_value=httpx.Response(200, json=expected))
    response = client.delete_item(item_id=item_id)
    assert response == expected


def test_docstring():
    docstring = 'Calling endpoint: {verb} {endpoint}'

    assert client.get_item.__doc__ == docstring.format(verb='GET', endpoint='/items/{item_id}')
    assert client.put_item.__doc__ == docstring.format(verb='PUT', endpoint='/items/{item_id}')
    assert client.post_item.__doc__ == docstring.format(verb='POST', endpoint='/items/{item_id}')
    assert client.patch_item.__doc__ == docstring.format(verb='PATCH', endpoint='/items/{item_id}')
    assert client.delete_item.__doc__ == docstring.format(verb='DELETE', endpoint='/items/{item_id}')


def test_class_attributes():
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


def test_authenticate_with_init_username_password():
    username = 'toto'
    password = '1234'
    expected = httpx.BasicAuth(username, password)
    rest_client = RestApiClient(username=username, password=password)

    assert rest_client.session.synchronous.auth is not None
    assert rest_client.session.asynchronous.auth is not None
    assert vars(rest_client.session.synchronous.auth) == vars(expected)
    assert vars(rest_client.session.asynchronous.auth) == vars(expected)
