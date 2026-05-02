from datetime import datetime, timezone

from connector.generated import AuthCredential, OAuthCredential
from {name}.settings import {pascal}Settings

VALID_AUTH = AuthCredential(
    oauth=OAuthCredential(access_token="valid"),  # noqa: S105
)
INVALID_AUTH = AuthCredential(
    oauth=OAuthCredential(access_token="invalid"),  # noqa: S105
)
SETTINGS = {pascal}Settings(account_id="test-account-id").model_dump()
TEST_MAX_PAGE_SIZE = 100

DATETIME_NOW = datetime.now(tz=timezone.utc)
