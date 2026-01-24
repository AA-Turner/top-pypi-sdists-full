import pytest
from fixtures import ConfigSimple, config_simple

from fitrequest.auth import Auth


def test_client_name(config_simple):
    client = config_simple.fit_class()
    assert client.client_name == 'client'

    client.session.update(client_name='toto')
    assert client.client_name == 'toto'


def test_client_version(config_simple):
    client = config_simple.fit_class()
    assert client.version == '0.0.1'

    client.session.update(version='1.2.3')
    assert client.version == '1.2.3'


def test_client_base_url(config_simple):
    client = config_simple.fit_class()
    assert client.base_url == 'https://skillcorner.test.com/api'

    client.session.update(base_url='www.toto.com')
    assert client.base_url == 'www.toto.com'


def test_property_update_after_session_update():
    auth_init = Auth(username='default_user', password='default_password')
    auth_update = Auth(username='default_user2', password='default_password2')

    auth_init_dump = auth_init.model_dump(exclude_none=True)
    auth_update_dump = auth_update.model_dump(exclude_none=True)

    # Default init authentication
    client = ConfigSimple(auth=auth_init).fit_class()

    assert client.session.raw_auth == auth_init_dump
    assert client.auth == auth_init_dump
    assert client.session.synchronous.auth._auth_header == auth_init.authentication._auth_header
    assert client.session.asynchronous.auth._auth_header == auth_init.authentication._auth_header

    # Update authentication
    client.session.update(auth=auth_update_dump)
    client.session.authenticate()

    assert client.session.raw_auth == auth_update_dump
    assert client.auth == auth_update_dump
    assert client.session.synchronous.auth._auth_header == auth_update.authentication._auth_header
    assert client.session.asynchronous.auth._auth_header == auth_update.authentication._auth_header
