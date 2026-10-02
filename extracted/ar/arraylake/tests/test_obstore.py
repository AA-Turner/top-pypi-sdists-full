import importlib.util
from datetime import UTC, datetime, timedelta
from uuid import uuid4

import pytest

from arraylake import AsyncClient
from arraylake.obstore import maybe_get_credential_provider
from arraylake.types import BucketResponse, GSCredentials, S3Credentials


def _bucket_response(*, platform, auth_config, nickname="a-bucket", extra_config=None) -> BucketResponse:
    return BucketResponse(
        id=uuid4(),
        name="a-bucket",
        nickname=nickname,
        platform=platform,
        extra_config=extra_config if extra_config is not None else {},
        auth_config=auth_config,
        is_default=False,
    )


DELEGATED_S3_AUTH = {
    "method": "aws_customer_managed_role",
    "external_customer_id": "12345678",
    "external_role_name": "my_external_role",
    "shared_secret": "our-shared-secret",
}
DELEGATED_GCS_AUTH = {"method": "gcp_customer_managed_role", "target_service_account": "sa@project.iam.gserviceaccount.com"}
DELEGATED_AZURE_AUTH = {"method": "azure_credential_delegation", "tenant_id": "a-tenant", "storage_account": "acct"}


class TestObstoreCredentialRefresh:
    """The store handed back by ``get_obstore_for_bucket`` must re-vend credentials before
    they expire, so operations that outlive one credential lifetime don't die mid-flight."""

    @pytest.fixture
    def aclient(self, test_token):
        return AsyncClient("https://test-arraylake-service.bar", token=test_token)

    @pytest.mark.parametrize(
        "platform,auth_config",
        [
            ("s3", DELEGATED_S3_AUTH),
            ("gs", DELEGATED_GCS_AUTH),
        ],
    )
    def test_provider_built_for_delegated_buckets(self, aclient, platform, auth_config):
        bucket = _bucket_response(platform=platform, auth_config=auth_config)
        provider = maybe_get_credential_provider(aclient, bucket, "an-org", "read", None)
        assert provider is not None

    @pytest.mark.parametrize(
        "platform,auth_config",
        [
            # HMAC and anonymous credentials are static — there is nothing to re-vend.
            ("s3", {"method": "hmac", "access_key_id": "abc", "secret_access_key": "def"}),
            ("s3", {"method": "anonymous"}),
            ("s3", None),
            # Delegated, but obstore's AzureStore has no credential provider hook.
            ("azure", DELEGATED_AZURE_AUTH),
        ],
    )
    def test_no_provider_for_non_refreshable_buckets(self, aclient, platform, auth_config):
        bucket = _bucket_response(platform=platform, auth_config=auth_config)
        assert maybe_get_credential_provider(aclient, bucket, "an-org", "read", None) is None

    def test_provider_returns_initial_credentials_then_revends(self, aclient, monkeypatch):
        """The first call reuses the credentials already vended when the store was built;
        only once they lapse does obstore's callback cost another round trip."""
        vends = []

        async def fake_vend(org, nickname, access="read"):
            vends.append((org, nickname, access))
            return S3Credentials(
                aws_access_key_id=f"fresh-key-{len(vends)}",
                aws_secret_access_key="fresh-secret",
                aws_session_token="fresh-token",
                expiration=datetime.now(UTC) + timedelta(hours=1),
            )

        monkeypatch.setattr(aclient, "_get_s3_delegated_credentials_from_bucket", fake_vend)

        initial = S3Credentials(
            aws_access_key_id="initial-key",
            aws_secret_access_key="initial-secret",
            aws_session_token="initial-token",
            expiration=datetime.now(UTC) + timedelta(hours=1),
        )
        bucket = _bucket_response(platform="s3", auth_config=DELEGATED_S3_AUTH, nickname="delegated")
        provider = maybe_get_credential_provider(aclient, bucket, "an-org", "write", initial)

        first = provider()
        assert first["access_key_id"] == "initial-key"
        assert first["token"] == "initial-token"
        assert vends == []

        second = provider()
        assert second["access_key_id"] == "fresh-key-1"
        # The refresh must re-request the same access scope the store was built with.
        assert vends == [("an-org", "delegated", "write")]

    def test_provider_revends_immediately_when_initial_credentials_expired(self, aclient, monkeypatch):
        """A store built long ago (or unpickled on a worker) must not hand obstore a
        credential that is already dead."""

        async def fake_vend(org, nickname, access="read"):
            return S3Credentials(
                aws_access_key_id="fresh-key",
                aws_secret_access_key="fresh-secret",
                aws_session_token=None,
                expiration=datetime.now(UTC) + timedelta(hours=1),
            )

        monkeypatch.setattr(aclient, "_get_s3_delegated_credentials_from_bucket", fake_vend)

        expired = S3Credentials(
            aws_access_key_id="stale-key",
            aws_secret_access_key="stale-secret",
            aws_session_token="stale-token",
            expiration=datetime.now(UTC) - timedelta(minutes=5),
        )
        bucket = _bucket_response(platform="s3", auth_config=DELEGATED_S3_AUTH)
        provider = maybe_get_credential_provider(aclient, bucket, "an-org", "read", expired)

        cred = provider()
        assert cred["access_key_id"] == "fresh-key"
        # No session token means obstore must not be handed an empty one.
        assert "token" not in cred

    def test_gcs_provider_returns_bearer_token_with_aware_expiry(self, aclient, monkeypatch):
        """google-auth hands back naive datetimes; obstore requires them timezone-aware."""
        naive_expiry = datetime.now(UTC).replace(tzinfo=None) + timedelta(hours=1)

        async def fake_vend(org, nickname, access="read"):
            return GSCredentials(access_token="fresh-bearer", expiration=naive_expiry, principal="sa@project.iam.gserviceaccount.com")

        monkeypatch.setattr(aclient, "_get_gcs_delegated_credentials_from_bucket", fake_vend)

        bucket = _bucket_response(platform="gs", auth_config=DELEGATED_GCS_AUTH)
        provider = maybe_get_credential_provider(aclient, bucket, "an-org", "read", None)

        cred = provider()
        assert cred["token"] == "fresh-bearer"
        assert cred["expires_at"] == naive_expiry.replace(tzinfo=UTC)

    @pytest.mark.skipif(importlib.util.find_spec("obstore") is None, reason="obstore extra not installed")
    @pytest.mark.asyncio
    async def test_store_for_delegated_bucket_carries_provider(self, aclient, monkeypatch):
        """End to end: the store returned to the user is wired to the refreshing provider
        rather than to baked-in static keys."""
        import obstore as obs

        bucket = _bucket_response(
            platform="s3",
            auth_config=DELEGATED_S3_AUTH,
            nickname="delegated",
            extra_config={"region_name": "us-west-2"},
        )

        async def fake_get_bucket_config(*, org, nickname):
            return bucket

        async def fake_vend(org, nickname, access="read"):
            return S3Credentials(
                aws_access_key_id="key",
                aws_secret_access_key="secret",
                aws_session_token="token",
                expiration=datetime.now(UTC) + timedelta(hours=1),
            )

        monkeypatch.setattr(aclient, "get_bucket_config", fake_get_bucket_config)
        monkeypatch.setattr(aclient, "_get_s3_delegated_credentials_from_bucket", fake_vend)

        store = await aclient.get_obstore_for_bucket(org="an-org", nickname="delegated")

        assert isinstance(store, obs.store.S3Store)
        assert store.credential_provider is not None
        # Static keys must not also be baked into the store config.
        assert "access_key_id" not in store.config
        assert store.config["region"] == "us-west-2"
