from snowflake.core.secret import (
    CloudProviderTokenSecret,
    GenericStringSecret,
    JwtKeyPairSecret,
    Oauth2Secret,
    PasswordSecret,
    SymmetricKeySecret,
)


test_cloud_provider_token_secret_template = CloudProviderTokenSecret(
    name="to_be_set",
    api_authentication="to_be_set",
    comment="Test cloud provider token secret",
)

test_generic_string_secret_template = GenericStringSecret(
    name="to_be_set",
    secret_string="test_secret_value_123",
    comment="Test generic string secret",
)

test_jwt_key_pair_secret_template = JwtKeyPairSecret(
    name="to_be_set",
    algorithm="RSA",
    key_length=4096,
    comment="Test JWT key pair secret",
)

test_oauth2_client_secret_template = Oauth2Secret(
    name="to_be_set",
    api_authentication="to_be_set",
    oauth_scopes=["read", "write"],
    comment="Test OAuth2 client flow secret",
)

test_oauth2_auth_code_secret_template = Oauth2Secret(
    name="to_be_set",
    api_authentication="to_be_set",
    oauth_refresh_token="test_refresh_token",
    oauth_refresh_token_expiry_time="2030-01-01 10:00:00",
    comment="Test OAuth2 auth code flow secret",
)

test_password_secret_template = PasswordSecret(
    name="to_be_set",
    username="snowman",
    password="test",
    comment="Test password secret",
)

test_symmetric_key_secret_template = SymmetricKeySecret(
    name="to_be_set",
    algorithm="GENERIC",
    comment="Test symmetric key secret",
)
