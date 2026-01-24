from unittest import TestCase

import boto3
import httpx
import pytest
import respx
from fixtures import (
    ConfigWithURL,
    config_with_basic_credentials,
    config_with_custom_auth,
    config_with_custom_creds_from_env,
    config_with_custom_header_token,
    config_with_custom_header_token_from_aws,
    config_with_custom_params_token,
    config_with_custom_params_token_from_aws,
    config_with_url,
    set_env_credentials,
)
from moto import mock_aws
from pydantic_core import ValidationError

from fitrequest.auth import Auth
from fitrequest.aws_var import AWSSecretTypeEnum, AWSVar
from fitrequest.errors import MultipleAuthenticationError
from fitrequest.fit_var import FitVar
from fitrequest.token_auth import HeaderTokenAuth, ParamsTokenAuth


def test_authenticate_basic(config_with_url, config_with_basic_credentials):
    client_url = config_with_url.fit_class()
    client_env = config_with_basic_credentials.fit_class()

    assert client_url.session.synchronous.auth is None
    assert client_url.session.asynchronous.auth is None
    assert client_env.session.synchronous.auth is not None
    assert client_env.session.asynchronous.auth is not None


def test_authenticate_with_bad_args():
    config = ConfigWithURL(auth=Auth())
    assert config.auth is not None
    assert config.auth.authentication is None


def test_authenticate_with_init_username_password(config_with_url):
    username = 'awesome_dev'
    password = 'secret_password'
    expected = httpx.BasicAuth(username, password)
    client = config_with_url.fit_class(username=username, password=password)

    assert client.session.synchronous.auth is not None
    assert client.session.asynchronous.auth is not None
    assert vars(client.session.synchronous.auth) == vars(expected)
    assert vars(client.session.asynchronous.auth) == vars(expected)


def test_authenticate_on_init():
    default_auth = Auth(username='default_user', password='default_password')
    default_auth_dump = default_auth.model_dump(exclude_none=True)

    client = ConfigWithURL(auth=default_auth).fit_class()

    assert client.auth == default_auth_dump
    assert client.session.raw_auth == default_auth_dump

    assert client.session.synchronous.auth._auth_header == default_auth.authentication._auth_header
    assert client.session.asynchronous.auth._auth_header == default_auth.authentication._auth_header


def test_authenticate_with_env(set_env_credentials, config_with_custom_creds_from_env):
    expected = httpx.BasicAuth('skcr', 'goal')
    config = config_with_custom_creds_from_env
    client = config.fit_class()

    assert config.auth is not None
    assert client.session.synchronous.auth is not None
    assert client.session.asynchronous.auth is not None
    assert vars(client.session.synchronous.auth) == vars(expected)
    assert vars(client.session.asynchronous.auth) == vars(expected)


def test_authenticate_with_params_token(config_with_custom_params_token):
    config = config_with_custom_params_token
    client = config.fit_class()

    assert config.auth is not None
    assert isinstance(client.session.synchronous.auth, ParamsTokenAuth)
    assert isinstance(client.session.asynchronous.auth, ParamsTokenAuth)
    assert client.session.synchronous.auth.token == 'CUSTOM_PARAMS_TOKEN'
    assert client.session.asynchronous.auth.token == 'CUSTOM_PARAMS_TOKEN'


@respx.mock
def test_authenticate_call_method_with_params_token(config_with_custom_params_token):
    expected = {
        'items': [
            {'item_id': 1, 'item_name': 'ball'},
            {'item_id': 2, 'item_name': 'gloves'},
        ]
    }
    respx.get(
        'https://test.skillcorner.fr/items/',
        params={'token': 'CUSTOM_PARAMS_TOKEN'},
    ).mock(return_value=httpx.Response(200, json=expected))
    response = config_with_custom_params_token.fit_class().get_items()
    assert response == expected


@respx.mock
def test_authenticate_call_method_with_header_token(config_with_custom_header_token):
    expected = {
        'items': [
            {'item_id': 1, 'item_name': 'ball'},
            {'item_id': 2, 'item_name': 'gloves'},
        ]
    }
    respx.get(
        'https://test.skillcorner.fr/items/',
    ).mock(return_value=httpx.Response(200, json=expected))
    response = config_with_custom_header_token.fit_class().get_items()
    assert response == expected


@mock_aws
def test_authenticate_with_params_token_from_aws(config_with_custom_params_token_from_aws):
    ssm = boto3.client('ssm', region_name='eu-central-1')
    ssm_value = 'CUSTOM_PARAMS_TOKEN_FROM_AWS'
    secret_path = '/dont_look_here'
    username_path = f'{secret_path}/params_token'

    ssm.put_parameter(
        Name=username_path,
        Description='A test parameter',
        Value=ssm_value,
        Type='SecureString',
    )
    config = config_with_custom_params_token_from_aws
    client = config.fit_class()

    assert config.auth is not None
    assert isinstance(client.session.synchronous.auth, ParamsTokenAuth)
    assert isinstance(client.session.asynchronous.auth, ParamsTokenAuth)
    assert client.session.synchronous.auth.token == 'CUSTOM_PARAMS_TOKEN_FROM_AWS'
    assert client.session.asynchronous.auth.token == 'CUSTOM_PARAMS_TOKEN_FROM_AWS'


def test_authenticate_with_header_token(config_with_custom_header_token):
    config = config_with_custom_header_token
    client = config.fit_class()

    assert config.auth is not None
    assert isinstance(client.session.synchronous.auth, HeaderTokenAuth)
    assert isinstance(client.session.asynchronous.auth, HeaderTokenAuth)
    assert client.session.synchronous.auth.token == 'CUSTOM_HEADER_TOKEN'
    assert client.session.asynchronous.auth.token == 'CUSTOM_HEADER_TOKEN'


def test_authenticate_with_custom_auth(config_with_custom_auth):
    config = config_with_custom_auth
    client = config.fit_class()

    assert config.auth is not None
    assert isinstance(client.session.synchronous.auth, httpx.DigestAuth)
    assert isinstance(client.session.asynchronous.auth, httpx.DigestAuth)


def test_authenticate_with_custom_init(config_with_custom_header_token):
    class RestApiClient(config_with_custom_header_token.fit_class):
        def __init__(self) -> None:
            self.session.update(timeout=55)
            self.session.authenticate()

    client = RestApiClient()
    assert isinstance(client.session.synchronous.auth, HeaderTokenAuth)
    assert isinstance(client.session.asynchronous.auth, HeaderTokenAuth)
    assert client.session.synchronous.auth.token == 'CUSTOM_HEADER_TOKEN'
    assert client.session.asynchronous.auth.token == 'CUSTOM_HEADER_TOKEN'


def test_authenticate_force_raw_auth_to_none(config_with_custom_header_token):
    class RestApiClient(config_with_custom_header_token.fit_class):
        def __init__(self) -> None:
            self.session.raw_auth = None
            self.session.authenticate()

    # raw_auth was forced to None, so on authentication nothing is done.
    client = RestApiClient()
    assert client.session.synchronous.auth is None
    assert client.session.asynchronous.auth is None


@mock_aws
def test_authenticate_with_header_token_from_aws(config_with_custom_header_token_from_aws):
    ssm = boto3.client('ssm', region_name='eu-central-1')
    ssm_value = 'CUSTOM_HEADER_TOKEN_FROM_AWS'
    secret_path = '/dont_look_here'
    username_path = f'{secret_path}/header_token'

    ssm.put_parameter(
        Name=username_path,
        Description='A test parameter',
        Value=ssm_value,
        Type='SecureString',
    )
    config = config_with_custom_header_token_from_aws
    client = config.fit_class()

    assert config.auth is not None
    assert isinstance(client.session.synchronous.auth, HeaderTokenAuth)
    assert isinstance(client.session.asynchronous.auth, HeaderTokenAuth)
    assert client.session.synchronous.auth.token == 'CUSTOM_HEADER_TOKEN_FROM_AWS'
    assert client.session.asynchronous.auth.token == 'CUSTOM_HEADER_TOKEN_FROM_AWS'


def test_authenticate_with_multiple_auth_methods():
    with pytest.raises(ValidationError) as err:
        Auth(
            username='CUSTOM_USERNAME_KEY',
            password='CUSTOM_PASSWORD_KEY',
            header_token=FitVar(
                aws_path='/dont_look_here/header_token',
                aws_type=AWSSecretTypeEnum.ssm,
                init_value='CUSTOM_HEADER_TOKEN_DEFAULT',
            ),
        )
    assert isinstance(err.value.errors()[0]['ctx']['error'], MultipleAuthenticationError)


def test_instance_serialization_username_password():
    auth = Auth(
        username='CUSTOM_USERNAME_KEY',
        password='CUSTOM_PASSWORD_KEY',
    )
    assert auth.model_dump(exclude_none=True) == {
        'username': 'CUSTOM_USERNAME_KEY',
        'password': 'CUSTOM_PASSWORD_KEY',
    }
    assert auth.model_dump(exclude_none=False) == {
        'username': 'CUSTOM_USERNAME_KEY',
        'password': 'CUSTOM_PASSWORD_KEY',
        'header_token': None,
        'params_token': None,
        'custom': None,
    }


@mock_aws
def test_authenticate_instance_serialization_tokens():
    ssm = boto3.client('ssm', region_name='eu-central-1')
    ssm_value = 'secret_token'
    secret_path = '/dont_look_here/secret_token'
    ssm.put_parameter(
        Name=secret_path,
        Description='A test parameter',
        Value=ssm_value,
        Type='SecureString',
    )

    assert Auth(
        header_token=FitVar(
            aws_path=secret_path,
            aws_type=AWSSecretTypeEnum.ssm,
            init_value='CUSTOM_HEADER_TOKEN_DEFAULT',
        ),
    ).model_dump(exclude_none=True) == {'header_token': 'CUSTOM_HEADER_TOKEN_DEFAULT'}

    assert Auth(
        params_token=FitVar(
            aws_path=secret_path,
            aws_type=AWSSecretTypeEnum.ssm,
            init_value='CUSTOM_PARAMS_TOKEN_DEFAULT',
        ),
    ).model_dump(exclude_none=True) == {'params_token': 'CUSTOM_PARAMS_TOKEN_DEFAULT'}


class TestSKCRUtilsSecret(TestCase):
    @mock_aws
    def test_get_ssm_username(self):
        ssm = boto3.client('ssm', region_name='eu-central-1')
        ssm_value = 'toto-user'
        secret_path = '/dont_look_here'
        username_path = f'{secret_path}/username'

        ssm.put_parameter(
            Name=username_path,
            Description='A test parameter',
            Value=ssm_value,
            Type='SecureString',
        )
        aws_username = AWSVar(path=username_path, secret_type=AWSSecretTypeEnum.ssm).value
        assert aws_username == ssm_value

    @mock_aws
    def test_get_secretsmanager_secret(self):
        secretsmanager = boto3.client('secretsmanager', region_name='eu-central-1')
        secretsmanager_value = 'this is it!'
        secret_path = '/dont_look_here'
        password_path = f'{secret_path}/password'

        secretsmanager.create_secret(Name=password_path, SecretString=secretsmanager_value)
        aws_password = AWSVar(path=password_path, secret_type=AWSSecretTypeEnum.secretsmanager).value
        assert aws_password == secretsmanager_value

    @mock_aws
    def test_cached_property_session_per_instance(self):
        aws_creds = AWSVar(path='toto', secret_type=AWSSecretTypeEnum.ssm)
        assert id(aws_creds.session) == id(aws_creds.session)
