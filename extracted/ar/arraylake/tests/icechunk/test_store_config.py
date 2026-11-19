from datetime import UTC, datetime
from uuid import uuid4

import pytest

from arraylake.repos.icechunk.store_config import bucket_store_config
from arraylake.types import AzureDelegatedCredentialsAuth, BucketResponse


def _azure_bucket(**fields) -> BucketResponse:
    return BucketResponse(
        id=uuid4(),
        platform="azure",
        nickname="blobs",
        name="container",
        is_default=False,
        extra_config={},
        updated=datetime.now(UTC),
        **fields,
    )


def test_an_azure_bucket_takes_its_storage_account_from_its_auth_config() -> None:
    auth = AzureDelegatedCredentialsAuth(method="azure_credential_delegation", tenant_id="t", storage_account="acct")
    assert bucket_store_config(_azure_bucket(auth_config=auth)) == {"azure": {"account": "acct"}}
    assert bucket_store_config(_azure_bucket(auth_config=auth), azure_account="other") == {"azure": {"account": "other"}}


def test_an_azure_bucket_without_a_storage_account_is_refused() -> None:
    with pytest.raises(ValueError, match="storage account"):
        bucket_store_config(_azure_bucket())
