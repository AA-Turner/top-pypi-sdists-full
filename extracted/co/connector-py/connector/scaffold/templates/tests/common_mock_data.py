from connector.generated.models.auth_credential import AuthCredential
from connector.generated.models.o_auth_credential import OAuthCredential
from {name}.settings import {pascal}Settings

VALID_AUTH = AuthCredential(
    oauth=OAuthCredential(access_token="valid"),  # noqa: S105
)
INVALID_AUTH = AuthCredential(
    oauth=OAuthCredential(access_token="invalid"),  # noqa: S105
)
SETTINGS = {pascal}Settings(account_id="test-account-id").model_dump()
TEST_MAX_PAGE_SIZE = 100
