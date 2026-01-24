import copy

from typing import Iterator

import pytest

from snowflake.core import CreateMode
from snowflake.core.exceptions import ConflictError
from snowflake.core.secret import (
    CloudProviderTokenSecret,
    GenericStringSecret,
    JwtKeyPairSecret,
    Oauth2Secret,
    PasswordSecret,
    SymmetricKeySecret,
)
from tests.integ.utils import MASKED_VALUE, random_string

from .conftest import (
    test_cloud_provider_token_secret_template,
    test_generic_string_secret_template,
    test_jwt_key_pair_secret_template,
    test_oauth2_auth_code_secret_template,
    test_oauth2_client_secret_template,
    test_password_secret_template,
    test_symmetric_key_secret_template,
)


@pytest.fixture(scope="module")
def oauth_security_integration(connection) -> Iterator[str]:
    name = random_string(10, "test_oauth_security_integration_")
    with connection.cursor() as cur:
        cur.execute(
            f"""
        CREATE SECURITY INTEGRATION {name}
          TYPE = API_AUTHENTICATION
          AUTH_TYPE = OAUTH2
          OAUTH_CLIENT_ID = 'client_id_value'
          OAUTH_CLIENT_SECRET = 'client_secret_value'
          OAUTH_ALLOWED_SCOPES = ('read', 'write')
          ENABLED = true
          COMMENT = 'Created by secret/test_create_and_fetch'
        """
        )
        try:
            yield name
        finally:
            cur.execute(f"DROP SECURITY INTEGRATION IF EXISTS {name}")


@pytest.fixture(scope="module")
def cloud_security_integration(connection) -> Iterator[str]:
    name = random_string(10, "test_cloud_security_integration_")
    with connection.cursor() as cur:
        cur.execute(
            f"""
        CREATE SECURITY INTEGRATION {name}
          TYPE = API_AUTHENTICATION
          AUTH_TYPE = AWS_IAM
          AWS_ROLE_ARN = 'arn:aws:iam::123456789012:role/SnowflakeRole'
          ENABLED = true
          COMMENT = 'Created by secret/test_create_and_fetch'
        """
        )
        try:
            yield name
        finally:
            cur.execute(f"DROP SECURITY INTEGRATION IF EXISTS {name}")


def test_create_and_fetch_cloud_provider_token_secret(secrets, cloud_security_integration: str):
    name = random_string(10, "test_secret_create_and_fetch_")
    secret_handle = secrets[name]

    try:
        secret = copy.deepcopy(test_cloud_provider_token_secret_template)
        secret.name = name
        secret.api_authentication = cloud_security_integration
        secrets.create(secret)

        fetched_secret = secret_handle.fetch()

        assert isinstance(fetched_secret, CloudProviderTokenSecret)
        assert fetched_secret.name == name.upper()
        assert fetched_secret.api_authentication == cloud_security_integration.upper()
        assert fetched_secret.comment == "Test cloud provider token secret"
        assert fetched_secret.database_name == secrets.database.name
        assert fetched_secret.schema_name == secrets.schema.name
    finally:
        secret_handle.drop(if_exists=True)


def test_create_and_fetch_generic_string_secret(secrets):
    name = random_string(10, "test_secret_create_and_fetch_")
    secret_handle = secrets[name]

    try:
        secret = copy.deepcopy(test_generic_string_secret_template)
        secret.name = name
        secrets.create(secret)

        fetched_secret = secret_handle.fetch()

        assert isinstance(fetched_secret, GenericStringSecret)
        assert fetched_secret.name == name.upper()
        assert fetched_secret.secret_string == MASKED_VALUE
        assert fetched_secret.comment == "Test generic string secret"
        assert fetched_secret.database_name == secrets.database.name
        assert fetched_secret.schema_name == secrets.schema.name
    finally:
        secret_handle.drop(if_exists=True)


def test_create_and_fetch_jwt_key_pair_secret(secrets):
    name = random_string(10, "test_secret_create_and_fetch_")
    secret_handle = secrets[name]

    try:
        secret = copy.deepcopy(test_jwt_key_pair_secret_template)
        secret.name = name
        secrets.create(secret)

        fetched_secret = secret_handle.fetch()

        assert isinstance(fetched_secret, JwtKeyPairSecret)
        assert fetched_secret.name == name.upper()
        assert fetched_secret.algorithm == "RSA"
        assert fetched_secret.key_length == 4096
        assert fetched_secret.comment == "Test JWT key pair secret"
        assert fetched_secret.database_name == secrets.database.name
        assert fetched_secret.schema_name == secrets.schema.name
    finally:
        secret_handle.drop(if_exists=True)


def test_create_and_fetch_oauth2_client_secret(secrets, oauth_security_integration: str):
    name = random_string(10, "test_secret_create_and_fetch_")
    secret_handle = secrets[name]

    try:
        secret = copy.deepcopy(test_oauth2_client_secret_template)
        secret.name = name
        secret.api_authentication = oauth_security_integration
        secrets.create(secret)

        fetched_secret = secret_handle.fetch()

        assert isinstance(fetched_secret, Oauth2Secret)
        assert fetched_secret.name == name.upper()
        assert fetched_secret.api_authentication == oauth_security_integration.upper()
        assert fetched_secret.oauth_refresh_token is None
        assert fetched_secret.oauth_refresh_token_expiry_time is None
        assert fetched_secret.oauth_scopes == ["read", "write"]
        assert fetched_secret.comment == "Test OAuth2 client flow secret"
        assert fetched_secret.database_name == secrets.database.name
        assert fetched_secret.schema_name == secrets.schema.name
    finally:
        secret_handle.drop(if_exists=True)


def test_create_and_fetch_oauth2_auth_code_secret(secrets, oauth_security_integration: str):
    name = random_string(10, "test_secret_create_and_fetch_")
    secret_handle = secrets[name]

    try:
        secret = copy.deepcopy(test_oauth2_auth_code_secret_template)
        secret.name = name
        secret.api_authentication = oauth_security_integration
        secrets.create(secret)

        fetched_secret = secret_handle.fetch()

        assert isinstance(fetched_secret, Oauth2Secret)
        assert fetched_secret.name == name.upper()
        assert fetched_secret.api_authentication == oauth_security_integration.upper()
        assert fetched_secret.oauth_refresh_token == MASKED_VALUE
        assert fetched_secret.oauth_refresh_token_expiry_time == "2030-01-01 10:00:00"
        assert fetched_secret.oauth_scopes is None
        assert fetched_secret.comment == "Test OAuth2 auth code flow secret"
        assert fetched_secret.database_name == secrets.database.name
        assert fetched_secret.schema_name == secrets.schema.name
    finally:
        secret_handle.drop(if_exists=True)


def test_create_and_fetch_password_secret(secrets):
    name = random_string(10, "test_secret_create_and_fetch_")
    secret_handle = secrets[name]

    try:
        secret = copy.deepcopy(test_password_secret_template)
        secret.name = name
        secrets.create(secret)

        fetched_secret = secret_handle.fetch()

        assert isinstance(fetched_secret, PasswordSecret)
        assert fetched_secret.name == name.upper()
        assert fetched_secret.username == "snowman"
        assert fetched_secret.password == MASKED_VALUE
        assert fetched_secret.comment == "Test password secret"
        assert fetched_secret.database_name == secrets.database.name
        assert fetched_secret.schema_name == secrets.schema.name
    finally:
        secret_handle.drop(if_exists=True)


def test_create_and_fetch_symmetric_key_secret(secrets):
    name = random_string(10, "test_secret_create_and_fetch_")
    secret_handle = secrets[name]

    try:
        secret = copy.deepcopy(test_symmetric_key_secret_template)
        secret.name = name
        secrets.create(secret)

        fetched_secret = secret_handle.fetch()

        assert isinstance(fetched_secret, SymmetricKeySecret)
        assert fetched_secret.name == name.upper()
        assert fetched_secret.algorithm == "GENERIC"
        assert fetched_secret.comment == "Test symmetric key secret"
        assert fetched_secret.database_name == secrets.database.name
        assert fetched_secret.schema_name == secrets.schema.name
    finally:
        secret_handle.drop(if_exists=True)


def test_create_and_fetch_create_modes(secrets):
    name = random_string(10, "test_secret_create_and_fetch_")
    secret_handle = secrets[name]

    try:
        secret = copy.deepcopy(test_generic_string_secret_template)
        secret.name = name
        secret.comment = "First version"
        secrets.create(secret, mode=CreateMode.error_if_exists)
        assert secret_handle.fetch().comment == "First version"

        with pytest.raises(ConflictError):
            secrets.create(secret, mode=CreateMode.error_if_exists)

        secret.comment = "Second version"
        secrets.create(secret, mode=CreateMode.or_replace)
        assert secret_handle.fetch().comment == "Second version"

        secret.comment = "Should not change"
        secrets.create(secret, mode=CreateMode.if_not_exists)
        assert secret_handle.fetch().comment == "Second version"
    finally:
        secret_handle.drop(if_exists=True)
