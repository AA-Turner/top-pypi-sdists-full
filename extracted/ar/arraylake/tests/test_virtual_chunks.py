import json
from contextlib import asynccontextmanager
from datetime import UTC, datetime
from types import SimpleNamespace
from unittest.mock import AsyncMock, MagicMock, patch
from uuid import uuid4

import icechunk
import pytest
from packaging.version import Version

from arraylake import AsyncClient, Client

# Check if icechunk 2 is available
ICECHUNK_VERSION = Version(icechunk.__version__)
IS_IC2 = ICECHUNK_VERSION.major >= 2
from arraylake.api_utils import ArraylakeHttpClient
from arraylake.exceptions import ArraylakeClientError
from arraylake.types import (
    Author,
    AzureCredentials,
    BucketResponse,
    ExplicitVirtualChunkAccessPolicyResponse,
    GSCredentials,
    OpenRepoResponse,
    S3Credentials,
    VirtualChunkCredentials,
)

from tests.test_subscriptions import (
    create_filtered_subscription_repo,
    create_marketplace_listing,
    create_subscription_repo,
)


@asynccontextmanager
async def vcap_for_bucket(client: AsyncClient, org_name, bucket, subprefix="", public=False):
    """Create a VCAP covering the given bucket, clean up after."""
    vcap = await client.set_virtual_chunk_access_policy(
        org_name,
        bucket_nickname=bucket.nickname,
        subprefix=subprefix,
        public=public,
    )
    try:
        yield vcap
    finally:
        await client.delete_virtual_chunk_access_policy(
            org_name,
            bucket_nickname=bucket.nickname,
            subprefix=subprefix,
            public=public,
        )


@pytest.fixture(
    params=[
        "anonymous",
        pytest.param("delegated_creds", marks=pytest.mark.skip(reason="requires real STS credentials")),
    ]
)
def virtual_chunk_bucket(request, minio_anon_bucket, delegated_creds_bucket):
    """Parametrized fixture — runs tests with both anonymous and delegated-creds virtual chunk buckets."""
    if request.param == "anonymous":
        return minio_anon_bucket
    else:

        def constructor(*, prefix=None):
            return delegated_creds_bucket(name="delegatedbucket", nickname="delegatedbucket", prefix=prefix)

        return constructor


class TestAuthorization:
    @staticmethod
    def assert_vcc_set(repo: icechunk.Repository, expected_vcc_url_prefix: str) -> None:
        # check the virtual chunk containers have been set
        # TODO annoying that IC doesn't just return an empty dict instead of None if there are no containers
        virtual_chunk_containers = repo.config.virtual_chunk_containers if repo.config.virtual_chunk_containers is not None else {}
        assert set(virtual_chunk_containers) == {expected_vcc_url_prefix}

        # TODO can't easily compare generated icechunk.ObjectStoreConfig objects as that class doesn't implement `__eq__` or even expose access to its attributes :/
        # TODO once we allow virtual chunks to refere to to non-anonymous buckets it will become important to check this!
        # assert virtual_chunk_containers[expected_vcc_prefix].store == expected_storeconfig

    @staticmethod
    def assert_prefixes_authorized(repo: icechunk.Repository, expected_vcc_url_prefixes: set[str]) -> None:
        # check virtual chunk containers are correctly authorized
        # TODO apparently the IC config doesn't round-trip the url_prefix string exactly - it removes any trailing slash.
        authorized_prefixes = {prefix if prefix.endswith("/") else prefix + "/" for prefix in repo.authorized_virtual_container_prefixes}
        assert authorized_prefixes == expected_vcc_url_prefixes

    @staticmethod
    def assert_authorized(repo: icechunk.Repository, expected_vcc_url_prefix: str) -> None:
        TestAuthorization.assert_vcc_set(repo, expected_vcc_url_prefix)
        TestAuthorization.assert_prefixes_authorized(repo, {expected_vcc_url_prefix})

    @pytest.mark.parametrize(
        "authorization",
        [
            pytest.param("explicit", id="explicit-authorization"),
            pytest.param("fetch", id="fetch-containers"),
            pytest.param("automatic", id="automatic-discovery"),
        ],
    )
    @pytest.mark.asyncio
    async def test_get_repo(self, isolated_org, default_bucket, virtual_chunk_bucket, token, authorization):
        repo_bucket = default_bucket()
        virtual_bucket = virtual_chunk_bucket()
        vcc_url_prefix = "s3://" + virtual_bucket.name + virtual_bucket.prefix + "/"

        initial_config = icechunk.RepositoryConfig.default()
        initial_config.inline_chunk_threshold_bytes = 1024

        client = Client(token=token)
        async_client = AsyncClient(token=token)
        async with isolated_org(repo_bucket, virtual_bucket) as (org_name, buckets):
            # Create the repo without virtual chunk containers
            name = f"{org_name}/foo"
            repo = client.create_repo(
                name,
                bucket_config_nickname=repo_bucket.nickname,
                config=initial_config,
            )

            # Manually set a virtual chunk container on the icechunk repo directly
            modified_config = repo.config
            container = icechunk.VirtualChunkContainer(
                url_prefix=vcc_url_prefix,
                store=icechunk.s3_store(),
            )
            modified_config.set_virtual_chunk_container(container)
            repo = repo.reopen(config=modified_config)
            repo.save_config()

            if authorization == "explicit":
                authorize_virtual_chunk_access = {vcc_url_prefix: virtual_bucket.nickname}
            elif authorization == "fetch":
                authorize_virtual_chunk_access = client.get_virtual_chunk_containers(name)
            elif authorization == "automatic":
                authorize_virtual_chunk_access = None

            # Create a VCAP covering the virtual bucket — required for VCC validation
            async with vcap_for_bucket(async_client, org_name, virtual_bucket):
                # Get the repo
                repo = client.get_repo(name, authorize_virtual_chunk_access=authorize_virtual_chunk_access)

                self.assert_authorized(repo, vcc_url_prefix)

                # check that the original repo config has not been altered
                assert repo.config.inline_chunk_threshold_bytes == 1024

    @pytest.mark.asyncio
    @pytest.mark.parametrize(
        ("url_path", "bucket_config_prefix", "expected_path"),
        [
            ("/", "", "/"),
            ("", "", "/"),
            ("/prefix/", "prefix", "/prefix/"),
            ("/prefix", "prefix", "/prefix/"),
            # passing a more specific prefix than that in the bucket config is allowed
            ("/prefix/", "", "/prefix/"),
            ("/prefix", "", "/prefix/"),
            ("/prefix/subprefix/", "prefix", "/prefix/subprefix/"),
            ("/prefix/subprefix", "prefix", "/prefix/subprefix/"),
        ],
    )
    async def test_create_repo_with_auto_containers(
        self, isolated_org, default_bucket, virtual_chunk_bucket, token, url_path, bucket_config_prefix, expected_path
    ):
        repo_bucket = default_bucket()
        virtual_bucket = virtual_chunk_bucket(prefix=bucket_config_prefix)
        user_specified_url = f"s3://{virtual_bucket.name}{url_path}"
        expected_vcc_prefix = f"s3://{virtual_bucket.name}{expected_path}"

        initial_config = icechunk.RepositoryConfig.default()
        initial_config.inline_chunk_threshold_bytes = 1024

        client = Client(token=token)
        async_client = AsyncClient(token=token)
        async with isolated_org(repo_bucket, virtual_bucket) as (org_name, buckets):
            # Create a VCAP covering the virtual bucket — required for VCC validation
            async with vcap_for_bucket(async_client, org_name, virtual_bucket):
                # Create the repo, automatically creating virtual chunk containers
                repo_name = "foo"
                name = f"{org_name}/{repo_name}"
                repo = client.create_repo(
                    name, authorize_virtual_chunk_access={user_specified_url: virtual_bucket.nickname}, config=initial_config
                )

                self.assert_authorized(repo, expected_vcc_prefix)

                # Get the repo
                # Note: it's assumed that the user passes the exact same prefix at get-time. If they don't then IC will raise because it doesn't do the path standardization that AL does.
                repo = client.get_repo(name, authorize_virtual_chunk_access={user_specified_url: virtual_bucket.nickname})

                self.assert_authorized(repo, expected_vcc_prefix)

                # check that the original repo config has not been altered
                assert repo.config.inline_chunk_threshold_bytes == 1024

    @pytest.mark.asyncio
    async def test_import_existing_repo_with_existing_vccs(
        self,
        isolated_org,
        default_bucket,
        virtual_chunk_bucket,
        token,
    ):
        repo_bucket = default_bucket()
        virtual_bucket = virtual_chunk_bucket()
        vcc_url_prefix = "s3://" + virtual_bucket.name + "/"

        initial_config = icechunk.RepositoryConfig.default()
        initial_config.inline_chunk_threshold_bytes = 1024

        client = Client(token=token)
        async_client = AsyncClient(token=token)
        async with isolated_org(repo_bucket, virtual_bucket) as (org_name, buckets):
            repo_name = f"{org_name}/foo"

            # Use icechunk to create the repo outside of the arraylake client
            # IDK a better way to set up the storage for this, hardcoding for now
            repo_prefix = str(uuid4())[:8]
            ic_storage = icechunk.s3_storage(
                bucket=repo_bucket.name,
                prefix=repo_prefix,
                region="us-east-1",
                endpoint_url="http://localhost:9000",
                allow_http=True,
                access_key_id="minio123",
                secret_access_key="minio123",
                force_path_style=True,
            )
            ic_repo = icechunk.Repository.create(storage=ic_storage, config=initial_config)

            # Manually set a virtual chunk container on the icechunk repo directly
            modified_config = icechunk.RepositoryConfig.default()
            container = icechunk.VirtualChunkContainer(
                url_prefix=vcc_url_prefix,
                store=icechunk.s3_store(),
            )
            modified_config.set_virtual_chunk_container(container)
            ic_repo = ic_repo.reopen(config=modified_config)
            ic_repo.save_config()

            # Create a VCAP covering the virtual bucket — required for VCC validation
            async with vcap_for_bucket(async_client, org_name, virtual_bucket):
                # Use arraylake client to import the repo
                repo = client.import_repo(
                    repo_name,
                    repo_bucket.nickname,
                    repo_prefix,
                    authorize_virtual_chunk_access={vcc_url_prefix: virtual_bucket.nickname},
                )
                self.assert_authorized(repo, vcc_url_prefix)

                repo = client.get_repo(repo_name, authorize_virtual_chunk_access={vcc_url_prefix: virtual_bucket.nickname})
                self.assert_authorized(repo, vcc_url_prefix)

                # check that the original repo config has not been altered
                assert repo.config.inline_chunk_threshold_bytes == 1024

    @pytest.mark.asyncio
    async def test_import_existing_repo_without_existing_vccs(
        self,
        isolated_org,
        default_bucket,
        virtual_chunk_bucket,
        token,
    ):
        repo_bucket = default_bucket()
        virtual_bucket = virtual_chunk_bucket()
        vcc_url_prefix = "s3://" + virtual_bucket.name + "/"

        initial_config = icechunk.RepositoryConfig.default()
        initial_config.inline_chunk_threshold_bytes = 1024

        client = Client(token=token)
        async_client = AsyncClient(token=token)
        async with isolated_org(repo_bucket, virtual_bucket) as (org_name, buckets):
            repo_name = f"{org_name}/foo"

            # Use icechunk to create the repo outside of the arraylake client
            # IDK a better way to set up the storage for this, hardcoding for now
            repo_prefix = str(uuid4())[:8]
            ic_storage = icechunk.s3_storage(
                bucket=repo_bucket.name,
                prefix=repo_prefix,
                region="us-east-1",
                endpoint_url="http://localhost:9000",
                allow_http=True,
                access_key_id="minio123",
                secret_access_key="minio123",
                force_path_style=True,
            )
            icechunk.Repository.create(storage=ic_storage, config=initial_config)

            # Create a VCAP covering the virtual bucket — required for VCC validation
            async with vcap_for_bucket(async_client, org_name, virtual_bucket):
                # Use arraylake client to import the repo
                with pytest.warns(UserWarning, match="New virtual chunk containers will not be persisted"):
                    repo = client.import_repo(
                        repo_name,
                        repo_bucket.nickname,
                        repo_prefix,
                        authorize_virtual_chunk_access={vcc_url_prefix: virtual_bucket.nickname},
                    )
                self.assert_authorized(repo, vcc_url_prefix)

                repo = client.get_repo(repo_name, authorize_virtual_chunk_access={vcc_url_prefix: virtual_bucket.nickname})
                # VCCs won't be present as they were not persisted
                self.assert_prefixes_authorized(repo, {vcc_url_prefix})

                # check that the original repo config has not been altered
                assert repo.config.inline_chunk_threshold_bytes == 1024

    @pytest.mark.asyncio
    async def test_modify_via_authorize_access_method(
        self,
        isolated_org,
        default_bucket,
        virtual_chunk_bucket,
        token,
    ):
        repo_bucket = default_bucket()
        virtual_bucket = virtual_chunk_bucket()
        vcc_url_prefix = "s3://" + virtual_bucket.name + "/"

        initial_config = icechunk.RepositoryConfig.default()
        initial_config.inline_chunk_threshold_bytes = 1024

        client = Client(token=token)
        async_client = AsyncClient(token=token)
        async with isolated_org(repo_bucket, virtual_bucket) as (org_name, buckets):
            # Create the repo without virtual chunk containers
            repo_name = f"{org_name}/foo"
            repo = client.create_repo(repo_name, config=initial_config)

            # Create a VCAP covering the virtual bucket — required for VCC validation
            async with vcap_for_bucket(async_client, org_name, virtual_bucket):
                # explicitly set the virtual chunk containers using AL API
                client.authorize_virtual_chunk_access(
                    name=repo_name, authorize_virtual_chunk_access={vcc_url_prefix: virtual_bucket.nickname}
                )

                # Get the repo
                # Note: it's assumed that the user passes the exact same prefix at get-time. If they don't then IC will raise.
                repo = client.get_repo(repo_name, authorize_virtual_chunk_access={vcc_url_prefix: virtual_bucket.nickname})

                self.assert_authorized(repo, vcc_url_prefix)

                # check that the original repo config has not been altered
                assert repo.config.inline_chunk_threshold_bytes == 1024

    @pytest.mark.asyncio
    @pytest.mark.parametrize(
        ("invalid_user_specified_url", "bucket_config_prefix", "expected_err_msg"),
        [
            # we're not currently auto-inferring anything, including which bucket the user is referring to
            (None, "prefix", "must provide a bucket url"),
            ("prefix/", "prefix", "must be a complete url"),
            ("prefix", "prefix", "must be a complete url"),
            # various ways in which it could be inconsistent
            ("malformed", "prefix", "must be a complete url"),
            (2, "prefix", "must be a valid string url, but got type <class 'int'>"),
            ("gs://anonbucket/", "prefix", "Provided bucket url must be consistent with bucket config"),
            ("gs://anonbucket", "prefix", "Provided bucket url must be consistent with bucket config"),
            ("s3://differentbucket/", "prefix", "Provided bucket url must be consistent with bucket config"),
            ("s3://differentbucket", "prefix", "Provided bucket url must be consistent with bucket config"),
            ("s3://anonbucket/differentprefix/", "prefix", "Provided prefix must be consistent with prefix in bucket config"),
            ("s3://anonbucket/differentprefix", "prefix", "Provided prefix must be consistent with prefix in bucket config"),
            ("s3://anonbucket/prefixwhichisdifferent", "prefix", "Provided prefix must be consistent with prefix in bucket config"),
        ],
    )
    async def test_raise_on_create_repo_with_inconsistent_virtual_chunk_container(
        self,
        isolated_org,
        default_bucket,
        minio_anon_bucket,
        token,
        invalid_user_specified_url,
        bucket_config_prefix,
        expected_err_msg,
    ) -> None:
        repo_bucket = default_bucket()
        virtual_bucket = minio_anon_bucket(prefix=bucket_config_prefix)

        client = Client(token=token)
        async with isolated_org(repo_bucket, virtual_bucket) as (org_name, buckets):
            repo_name = f"{org_name}/foo"
            with pytest.raises(ValueError, match=expected_err_msg):
                client.create_repo(repo_name, authorize_virtual_chunk_access={invalid_user_specified_url: virtual_bucket.nickname})

            assert not any(repo.name == "foo" for repo in client.list_repos(org_name))

    async def test_requires_writer_authorization(
        self,
        isolated_org,
        default_bucket,
        minio_anon_bucket,
        token,
    ):
        repo_bucket = default_bucket()
        virtual_bucket = minio_anon_bucket()
        vcc_url_prefix = "s3://" + virtual_bucket.name + "/"

        client = Client(token=token)
        async with isolated_org(repo_bucket, virtual_bucket) as (org_name, buckets):
            # Create the repo without virtual chunk containers
            repo_name = f"{org_name}/foo"
            repo = client.create_repo(repo_name)

            # the repo writer never sets the VCCs

            # Get the repo
            repo = client.get_repo(repo_name, authorize_virtual_chunk_access={vcc_url_prefix: virtual_bucket.nickname})

            # the reader will not be able to access the virtual chunks
            assert repo.config.virtual_chunk_containers == None

    async def test_requires_writer_authorization_even_with_custom_config(
        self,
        isolated_org,
        default_bucket,
        minio_anon_bucket,
        token,
    ):
        """
        If a user tries to read a repo that has no VCCs set in the repo config,
        but they explicitly pass authorize_virtual_chunk_access AND a custom
        repo config that contains VCCs, a specific error should be raised
        telling them that VCCs must be authorized by the repo writer.
        """
        repo_bucket = default_bucket()
        virtual_bucket = minio_anon_bucket()
        vcc_url_prefix = "s3://" + virtual_bucket.name + "/"

        client = Client(token=token)
        async with isolated_org(repo_bucket, virtual_bucket) as (org_name, buckets):
            # Create the repo without virtual chunk containers
            repo_name = f"{org_name}/foo"
            client.create_repo(repo_name)

            # the repo writer never sets the VCCs

            # Create a custom config with VCCs
            custom_config = icechunk.RepositoryConfig.default()
            container = icechunk.VirtualChunkContainer(
                url_prefix=vcc_url_prefix,
                store=icechunk.s3_store(),
            )
            custom_config.set_virtual_chunk_container(container)

            # Try to get the repo with both authorize_virtual_chunk_access and custom config
            with pytest.raises(ValueError, match="repo writer"):
                client.get_repo(
                    repo_name,
                    config=custom_config,
                    authorize_virtual_chunk_access={vcc_url_prefix: virtual_bucket.nickname},
                )


# These tests check that creating potentially malicious IC repos via AL is forbidden,
# and that any potentially malicious IC repos that are created directly via IC are detected at import-time or open-time by AL.


@pytest.mark.parametrize(
    "unsafe_url_prefix, ic_store_type",
    [
        pytest.param(
            "file:///home/",
            "local_filesystem",
        ),
        pytest.param(
            "memory://some-location/",
            "in_memory",
        ),
        pytest.param(
            "http://server/",
            "http",
        ),
    ],
)
@pytest.mark.asyncio
class TestForbidUnsafeVirtualChunkContainers:
    """Check that any method of creating an AL repo with virtual chunks detects any potentially malicious virtual chunk containers."""

    # TODO also check upon modify_repo?

    @pytest.fixture
    def ic_store(self, ic_store_type, tmp_path):
        """Create the appropriate ic_store based on the parameterized type."""
        if ic_store_type == "local_filesystem":
            return icechunk.local_filesystem_store(str(tmp_path))
        elif ic_store_type == "in_memory":
            return icechunk.ObjectStoreConfig.InMemory()
        elif ic_store_type == "http":
            return icechunk.http_store()
        else:
            raise ValueError(f"Unknown ic_store_type: {ic_store_type}")

    async def test_create_repo(
        self,
        isolated_org,
        default_bucket,
        minio_anon_bucket,
        token,
        unsafe_url_prefix,
        ic_store_type,
    ):
        repo_bucket = default_bucket()
        virtual_bucket = minio_anon_bucket()

        client = Client(token=token)
        async with isolated_org(repo_bucket, virtual_bucket) as (org_name, buckets):
            repo_name = f"{org_name}/foo"

            # attempt to create the repo, forbidding automatically creating unsafe virtual chunk containers
            with pytest.raises(ValueError, match="Forbidden virtual chunk container url_prefix"):
                client.create_repo(repo_name, authorize_virtual_chunk_access={unsafe_url_prefix: virtual_bucket.nickname})

            assert not any(repo.name == "foo" for repo in client.list_repos(org_name))

    async def test_get_repo(self, isolated_org, default_bucket, minio_anon_bucket, token, unsafe_url_prefix, ic_store, ic_store_type):
        if ic_store_type == "in_memory":
            pytest.xfail("in_memory store not implemented in Icechunk")
        repo_bucket = default_bucket()
        virtual_bucket = minio_anon_bucket()

        client = Client(token=token)
        async with isolated_org(repo_bucket, virtual_bucket) as (org_name, buckets):
            # Create the repo without virtual chunk containers
            repo_name = f"{org_name}/foo"
            repo = client.create_repo(repo_name, bucket_config_nickname=repo_bucket.nickname)

            # Manually set a virtual chunk container on the icechunk repo directly
            # We will also separately forbid doing this with the Arraylake client, but we can't stop a canny bad guy doing it using IC manually
            config = repo.config
            container = icechunk.VirtualChunkContainer(
                url_prefix=unsafe_url_prefix,
                store=ic_store,
            )
            config.set_virtual_chunk_container(container)
            repo = repo.reopen(config=config)
            repo.save_config()

            # attempt to get unsafe repo
            # Server-side validation in open_repo catches the unsafe VCC prefix
            with pytest.raises((ValueError, ArraylakeClientError), match="Forbidden virtual chunk container prefix"):
                client.get_repo(repo_name, authorize_virtual_chunk_access={unsafe_url_prefix: virtual_bucket.nickname})

    async def test_import_existing_repo(
        self,
        isolated_org,
        default_bucket,
        minio_anon_bucket,
        token,
        unsafe_url_prefix,
        ic_store,
        ic_store_type,
    ):
        if ic_store_type == "in_memory":
            pytest.xfail("in_memory store not implemented in Icechunk")

        repo_bucket = default_bucket()
        virtual_bucket = minio_anon_bucket()

        client = Client(token=token)
        async with isolated_org(repo_bucket, virtual_bucket) as (org_name, buckets):
            repo_name = f"{org_name}/foo"

            # Use icechunk to create the repo outside of the arraylake client
            # IDK a better way to set up the storage for this, hardcoding for now
            repo_prefix = str(uuid4())[:8]
            ic_storage = icechunk.s3_storage(
                bucket=repo_bucket.name,
                prefix=repo_prefix,
                region="us-east-1",
                endpoint_url="http://localhost:9000",
                allow_http=True,
                access_key_id="minio123",
                secret_access_key="minio123",
                force_path_style=True,
            )
            ic_repo = icechunk.Repository.create(storage=ic_storage)

            # Manually set a virtual chunk container on the icechunk repo directly
            config = icechunk.RepositoryConfig.default()
            container = icechunk.VirtualChunkContainer(
                url_prefix=unsafe_url_prefix,
                store=ic_store,
            )
            config.set_virtual_chunk_container(container)
            ic_repo = ic_repo.reopen(config=config)
            ic_repo.save_config()

            # attempt to import existing unsafe repo
            with pytest.raises(ValueError, match="Forbidden virtual chunk container url_prefix"):
                # TODO also detect the unsafe containers when auto-discovery is implemented?
                client.import_repo(
                    repo_name,
                    repo_bucket.nickname,
                    repo_prefix,
                    authorize_virtual_chunk_access={unsafe_url_prefix: virtual_bucket.nickname},
                )

            assert not any(repo.name == "foo" for repo in client.list_repos(org_name))


@pytest.mark.asyncio
class TestVcapValidation:
    """Test that VCC-to-VCAP validation works correctly."""

    async def test_get_repo_without_vcap_fails(self, isolated_org, default_bucket, virtual_chunk_bucket, token):
        """VCC exists but no matching VCAP→ get_repo() raises."""
        repo_bucket = default_bucket()
        virtual_bucket = virtual_chunk_bucket()
        vcc_url_prefix = "s3://" + virtual_bucket.name + "/"

        client = Client(token=token)
        async with isolated_org(repo_bucket, virtual_bucket) as (org_name, buckets):
            repo_name = f"{org_name}/foo"
            repo = client.create_repo(repo_name, bucket_config_nickname=repo_bucket.nickname)

            # Manually set a virtual chunk container on the icechunk repo directly
            config = repo.config
            container = icechunk.VirtualChunkContainer(
                url_prefix=vcc_url_prefix,
                store=icechunk.s3_store(),
            )
            config.set_virtual_chunk_container(container)
            repo = repo.reopen(config=config)
            repo.save_config()

            # No VCAP created — get_repo should fail
            with pytest.raises(ValueError, match="not covered by any Virtual Chunk Access Policy"):
                client.get_repo(repo_name)

    async def test_vcap_prefix_must_cover_vcc_prefix(self, isolated_org, default_bucket, virtual_chunk_bucket, token):
        """VCAP exists but for a different prefix than the VCC → still fails."""
        repo_bucket = default_bucket()
        virtual_bucket = virtual_chunk_bucket()
        vcc_url_prefix = "s3://" + virtual_bucket.name + "/data/"

        client = Client(token=token)
        async_client = AsyncClient(token=token)
        async with isolated_org(repo_bucket, virtual_bucket) as (org_name, buckets):
            repo_name = f"{org_name}/foo"
            repo = client.create_repo(repo_name, bucket_config_nickname=repo_bucket.nickname)

            # Manually set a VCC pointing to /data/
            config = repo.config
            container = icechunk.VirtualChunkContainer(
                url_prefix=vcc_url_prefix,
                store=icechunk.s3_store(),
            )
            config.set_virtual_chunk_container(container)
            repo = repo.reopen(config=config)
            repo.save_config()

            # Create a VCAP for a different subprefix (/other/) — does not cover /data/
            async with vcap_for_bucket(async_client, org_name, virtual_bucket, subprefix="other/"):
                with pytest.raises(ValueError, match="not covered by any Virtual Chunk Access Policy"):
                    client.get_repo(repo_name)

    async def test_vcap_creation_rejected_for_hmac_bucket(self, isolated_org, default_bucket, token):
        """VCAP creation is rejected for HMAC buckets (you can never authorize HMAC virtual chunks)."""
        repo_bucket = default_bucket()
        hmac_bucket = default_bucket(name="hmacbucket", nickname="hmacbucket")

        async_client = AsyncClient(token=token)
        async with isolated_org(repo_bucket, hmac_bucket) as (org_name, buckets):
            with pytest.raises(ArraylakeClientError, match="HMAC authentication"):
                await async_client.set_virtual_chunk_access_policy(
                    org_name,
                    bucket_nickname=hmac_bucket.nickname,
                    subprefix="",
                    public=False,
                )


@pytest.mark.asyncio
class TestCrossOrgVcapValidation:
    """Test that VCAPs on one org do NOT authorize virtual chunks for repos in another org.

    Org A has the virtual chunk bucket + VCAP.
    Org B has the repo bucket + repo with VCCs pointing to Org A's bucket.

    Cross-org virtual chunk access is only intended for subscription repos (not yet implemented).
    Until then, VCAPs are resolved from the repo's own org only.
    """

    @pytest.mark.parametrize("public", [True, False], ids=["public-vcap", "private-vcap"])
    async def test_vcap_on_other_org_does_not_authorize(self, two_isolated_orgs, default_bucket, virtual_chunk_bucket, token, public):
        """A VCAP in Org A (public or private) does NOT authorize virtual chunks for a repo in Org B."""
        repo_bucket = default_bucket()
        virtual_bucket = virtual_chunk_bucket()
        vcc_url_prefix = "s3://" + virtual_bucket.name + "/"

        client = Client(token=token)
        async_client = AsyncClient(token=token)
        async with two_isolated_orgs(
            bucket_requests_org1=(virtual_bucket,),
            bucket_requests_org2=(repo_bucket,),
        ) as ((org_a, _), (org_b, _)):
            repo_name = f"{org_b}/foo"
            repo = client.create_repo(repo_name, bucket_config_nickname=repo_bucket.nickname)

            # Manually set a VCC pointing to Org A's bucket
            config = repo.config
            container = icechunk.VirtualChunkContainer(
                url_prefix=vcc_url_prefix,
                store=icechunk.s3_store(),
            )
            config.set_virtual_chunk_container(container)
            repo = repo.reopen(config=config)
            repo.save_config()

            # VCAP on Org A should not help Org B's repo regardless of public flag
            async with vcap_for_bucket(async_client, org_a, virtual_bucket, public=public):
                with pytest.raises(ValueError, match="not covered by any Virtual Chunk Access Policy"):
                    client.get_repo(repo_name)


@pytest.mark.asyncio
class TestForbidHmacBucketForVccs:
    """Check that HMAC bucket configs are rejected for virtual chunks.

    Without a VCAP, VCAP validation rejects the VCC before the HMAC check is reached.
    HMAC-specific rejection (even with a VCAP) is tested separately in TestVcapValidation.
    """

    async def test_create_repo(
        self,
        isolated_org,
        default_bucket,
        token,
    ):
        repo_bucket = default_bucket()
        virtual_bucket = default_bucket(name="unsafebucket", nickname="myunsafebucket")
        vcc_url_prefix = "s3://" + virtual_bucket.name + "/"

        client = Client(token=token)
        async with isolated_org(repo_bucket, virtual_bucket) as (org_name, buckets):
            repo_name = f"{org_name}/foo"

            with pytest.raises(ValueError, match="HMAC credentials"):
                client.create_repo(repo_name, authorize_virtual_chunk_access={vcc_url_prefix: virtual_bucket.nickname})

            assert not any(repo.name == "foo" for repo in client.list_repos(org_name))

    async def test_get_repo(self, isolated_org, default_bucket, token):
        repo_bucket = default_bucket()
        virtual_bucket = default_bucket(name="unsafebucket", nickname="unsafebucket")
        url_prefix = "s3://" + virtual_bucket.name + virtual_bucket.prefix + "/"

        client = Client(token=token)
        async with isolated_org(repo_bucket, virtual_bucket) as (org_name, buckets):
            # Create the repo without virtual chunk containers
            repo_name = f"{org_name}/foo"
            repo = client.create_repo(repo_name, bucket_config_nickname=repo_bucket.nickname)

            # Manually set a virtual chunk container on the icechunk repo directly
            config = repo.config
            container = icechunk.VirtualChunkContainer(
                url_prefix=url_prefix,
                store=icechunk.s3_store(),
            )
            config.set_virtual_chunk_container(container)
            repo = repo.reopen(config=config)
            repo.save_config()

            # Cannot set a VCAP for HMAC, and without a VCAP, VCAP validation rejects the VCC
            with pytest.raises(ValueError, match="not covered by any Virtual Chunk Access Policy"):
                client.get_repo(repo_name, authorize_virtual_chunk_access={url_prefix: virtual_bucket.nickname})

    async def test_import_existing_repo(self, isolated_org, default_bucket, token):
        repo_bucket = default_bucket()
        virtual_bucket = default_bucket(name="unsafebucket", nickname="unsafebucket")
        url_prefix = "s3://" + virtual_bucket.name + virtual_bucket.prefix + "/"

        client = Client(token=token)
        async with isolated_org(repo_bucket, virtual_bucket) as (org_name, buckets):
            repo_name = f"{org_name}/foo"

            # Use icechunk to create the repo outside of the arraylake client
            repo_prefix = str(uuid4())[:8]
            ic_storage = icechunk.s3_storage(
                bucket=repo_bucket.name,
                prefix=repo_prefix,
                region="us-east-1",
                endpoint_url="http://localhost:9000",
                allow_http=True,
                access_key_id="minio123",
                secret_access_key="minio123",
                force_path_style=True,
            )
            ic_repo = icechunk.Repository.create(storage=ic_storage)

            # Manually set a virtual chunk container on the icechunk repo directly
            config = icechunk.RepositoryConfig.default()
            container = icechunk.VirtualChunkContainer(
                url_prefix=url_prefix,
                store=icechunk.s3_store(),
            )
            config.set_virtual_chunk_container(container)
            ic_repo = ic_repo.reopen(config=config)
            ic_repo.save_config()

            # Client-side HMAC check rejects before VCAP validation
            with pytest.raises(ValueError, match="HMAC credentials"):
                client.import_repo(
                    repo_name,
                    repo_bucket.nickname,
                    repo_prefix,
                    authorize_virtual_chunk_access={url_prefix: virtual_bucket.nickname},
                )

            assert not any(repo.name == "foo" for repo in client.list_repos(org_name))


class TestRejectUnresolvableVccs:
    @pytest.mark.parametrize(
        ("vccs", "expected"),
        [
            pytest.param({}, {}, id="empty"),
            pytest.param(
                {"s3://bucket/": "mybucket"},
                {"s3://bucket/": "mybucket"},
                id="single-resolvable",
            ),
            pytest.param(
                {"s3://bucket1/": "b1", "s3://bucket2/": "b2"},
                {"s3://bucket1/": "b1", "s3://bucket2/": "b2"},
                id="multiple-resolvable",
            ),
        ],
    )
    def test_returns_resolvable_vccs(self, vccs, expected):
        from arraylake.repos.icechunk.virtual import reject_unresolvable_vccs

        assert reject_unresolvable_vccs(vccs) == expected

    @pytest.mark.parametrize(
        ("vccs", "expected_match"),
        [
            pytest.param(
                {"s3://bucket/": None},
                "s3://bucket/",
                id="single-null",
            ),
            pytest.param(
                {"s3://bucket1/": "b1", "s3://bucket2/": None},
                "s3://bucket2/",
                id="mixed-null-and-resolvable",
            ),
            pytest.param(
                {"s3://bucket1/": None, "s3://bucket2/": None},
                "unresolvable",
                id="all-null",
            ),
        ],
    )
    def test_raises_for_null_nicknames(self, vccs, expected_match):
        from arraylake.repos.icechunk.virtual import reject_unresolvable_vccs

        with pytest.raises(ValueError, match=expected_match):
            reject_unresolvable_vccs(vccs)


@pytest.mark.asyncio
@pytest.mark.parametrize("public", [False, True])
class TestVcapCrud:
    """Test the client's VCAP create/list/delete plumbing."""

    async def test_vcap_lifecycle(self, isolated_org, minio_anon_bucket, token, public):
        virtual_bucket = minio_anon_bucket()
        expected_url_prefix = f"s3://{virtual_bucket.name}/my/data/"

        client = Client(token=token)
        async with isolated_org(virtual_bucket) as (org_name, buckets):
            # Create a VCAP
            vcap = client.set_virtual_chunk_access_policy(
                org_name,
                bucket_nickname=virtual_bucket.nickname,
                subprefix="my/data/",
                public=public,
            )
            assert isinstance(vcap, ExplicitVirtualChunkAccessPolicyResponse)
            assert vcap.subprefix == "my/data"
            assert vcap.public == public
            assert vcap.url_prefix == expected_url_prefix

            # List VCAPs and verify it's there
            vcaps = client.list_virtual_chunk_access_policies(org_name)
            assert len(vcaps) == 1
            assert vcaps[0].url_prefix == expected_url_prefix
            assert vcaps[0].public == public

            # Delete it
            client.delete_virtual_chunk_access_policy(
                org_name,
                bucket_nickname=virtual_bucket.nickname,
                subprefix="my/data/",
                public=public,
            )
            assert len(client.list_virtual_chunk_access_policies(org_name)) == 0

            # Deleting again should be idempotent
            client.delete_virtual_chunk_access_policy(
                org_name,
                bucket_nickname=virtual_bucket.nickname,
                subprefix="my/data/",
                public=public,
            )


def assert_subscription_vcap_resolution(client: Client, sub_repo_name: str, vcc_url_prefixes: set[str], public: bool):
    """Assert that the subscriber repo resolves (or rejects) VCCs based on VCAP visibility."""

    if public:
        sub_repo = client.get_repo(sub_repo_name)
        TestAuthorization.assert_prefixes_authorized(sub_repo, vcc_url_prefixes)
    else:
        with pytest.raises(ValueError, match="not covered by any Virtual Chunk Access Policy"):
            client.get_repo(sub_repo_name)


@pytest.mark.skipif(not IS_IC2, reason="Paid marketplace listings require icechunk 2.x")
async def test_filtered_subscription_implementation(two_isolated_orgs, default_bucket, token):
    """
    Filtered subscription: subscriber has its own bucket, VCC points to provider's chunks.

    This test verifies that:
    1. Creating a filtered subscription automatically creates a SubscriptionVCAP
    2. The server returns runtime_vcc_name so client can create the VCC at runtime
    3. The subscriber can access the provider repo's chunks via the auto-created VCC
    """
    # Provider repo storage — anonymous so the same bucket config can serve as a VCAP
    provider_repo_bucket = default_bucket(
        nickname="provider_repo_bucket",
        name="anonbucket",
        auth_config={"method": "anonymous"},
    )
    # Writable bucket for subscriber repo storage
    subscriber_bucket = default_bucket()

    client = Client(token=token)
    async_client = AsyncClient(token=token)
    async with two_isolated_orgs(
        bucket_requests_org1=(provider_repo_bucket,),
        bucket_requests_org2=(subscriber_bucket,),
    ) as ((org_a, _), (org_b, _)):
        parent_repo_name = f"{org_a}/parent-repo"

        # Create provider repo via server API (anonymous bucket can't use client.create_repo)
        http_client = ArraylakeHttpClient("http://localhost:8000", token=token)
        resp = await http_client._request(
            "POST",
            f"/orgs/{org_a}/repos",
            content=json.dumps({"name": "parent-repo", "bucket_nickname": provider_repo_bucket.nickname}),
        )
        assert resp.is_success, f"Failed to create provider repo: {resp.status_code} {resp.content}"

        parent_repo_obj = await async_client.get_repo_object(parent_repo_name)
        repo_prefix = parent_repo_obj.prefix.strip("/")

        # Create the icechunk repo manually (anonymous bucket config, but MinIO allows writes)
        # Use spec_version=2 since paid marketplace listings require IC2 repos
        ic_storage = icechunk.s3_storage(
            bucket=provider_repo_bucket.name,
            prefix=parent_repo_obj.prefix,
            region="us-east-1",
            endpoint_url="http://localhost:9000",
            allow_http=True,
            access_key_id="minio123",
            secret_access_key="minio123",
            force_path_style=True,
        )
        icechunk.Repository.create(storage=ic_storage, spec_version=2)

        # Construct VCC URL pointing to the provider repo's chunks directory
        vcc_url_prefix = f"s3://{provider_repo_bucket.name}/{repo_prefix}/chunks/"

        # Creating the marketplace listing auto-creates a SubscriptionVCAP for the repo
        # Use paid pricing model to support filtered subscriptions
        listing = await create_marketplace_listing(token, org_a, parent_repo_obj.id, pricing_model="paid")

        await create_filtered_subscription_repo(
            token,
            org_b,
            "sub-repo",
            listing["id"],
            bucket_nickname=subscriber_bucket.nickname,
            target_filter={"nodes": {"include_paths": ["/data"]}},
        )

        # Open the subscriber repo via client.get_repo() - this will:
        # 1. Fetch virtual_chunk_credentials from server (with runtime_vcc_name="__al_source")
        # 2. Automatically create the VCC for the provider's chunks
        sub_repo = client.get_repo(f"{org_b}/sub-repo")

        # Verify the VCC was created and authorized
        TestAuthorization.assert_prefixes_authorized(sub_repo, {vcc_url_prefix})

        # Verify the VCC exists in the config
        vccs = sub_repo.config.virtual_chunk_containers
        assert vcc_url_prefix in vccs, f"Expected VCC for '{vcc_url_prefix}' in config, got: {list(vccs.keys())}"

        # VCC name persistence requires icechunk 2.x
        if icechunk.__version__.startswith("2."):
            assert vccs[vcc_url_prefix].name == "__al_source"


@asynccontextmanager
async def provider_with_virtual_chunks(two_isolated_orgs, default_bucket, token, public, pricing_model="paid"):
    """Set up a provider org with a repo containing virtual chunks, and a subscriber org.

    Creates:
    - Org A (provider): repo on anonymous "anonbucket", VCC pointing to anonymous "externalbucket",
      VCAP covering the virtual chunk bucket (public or private based on `public` param)
    - Org B (subscriber): writable bucket on "testbucket"

    Args:
        pricing_model: "free" or "paid". Use "free" for direct subscriptions, "paid" for filtered.

    Yields (client, async_client, org_a, org_b, parent_repo_obj,
           provider_repo_bucket, subscriber_bucket, vcc_url_prefix, listing).
    """
    # Provider repo storage — anonymous so the same bucket config can serve as a VCAP
    provider_repo_bucket = default_bucket(
        nickname="provider_repo_bucket",
        name="anonbucket",
        auth_config={"method": "anonymous"},
    )
    # Provider's virtual chunk bucket — anonymous, on a different physical bucket
    virtual_chunk_bucket = default_bucket(
        nickname="virtual_chunk_bucket",
        name="externalbucket",
        auth_config={"method": "anonymous"},
    )
    # Writable bucket for subscriber repo storage
    subscriber_bucket = default_bucket()

    vcc_url_prefix = f"s3://{virtual_chunk_bucket.name}/"

    client = Client(token=token)
    async_client = AsyncClient(token=token)
    async with two_isolated_orgs(
        bucket_requests_org1=(provider_repo_bucket, virtual_chunk_bucket),
        bucket_requests_org2=(subscriber_bucket,),
    ) as ((org_a, _), (org_b, _)):
        parent_repo_name = f"{org_a}/parent-repo"

        # Create provider repo via server API (anonymous bucket can't use client.create_repo)
        http_client = ArraylakeHttpClient("http://localhost:8000", token=token)
        resp = await http_client._request(
            "POST",
            f"/orgs/{org_a}/repos",
            content=json.dumps({"name": "parent-repo", "bucket_nickname": provider_repo_bucket.nickname}),
        )
        assert resp.is_success, f"Failed to create provider repo: {resp.status_code} {resp.content}"

        parent_repo_obj = await async_client.get_repo_object(parent_repo_name)

        # Create the icechunk repo manually (anonymous bucket config, but MinIO allows writes)
        # Use spec_version=2 for paid listings (which require IC2 repos)
        ic_storage = icechunk.s3_storage(
            bucket=provider_repo_bucket.name,
            prefix=parent_repo_obj.prefix,
            region="us-east-1",
            endpoint_url="http://localhost:9000",
            allow_http=True,
            access_key_id="minio123",
            secret_access_key="minio123",
            force_path_style=True,
        )
        create_kwargs = {"storage": ic_storage}
        if pricing_model == "paid":
            create_kwargs["spec_version"] = 2
        provider_ic_repo = icechunk.Repository.create(**create_kwargs)

        # Set VCC for virtual chunks on the provider repo
        config = provider_ic_repo.config
        config.set_virtual_chunk_container(
            icechunk.VirtualChunkContainer(
                url_prefix=vcc_url_prefix,
                store=icechunk.s3_store(),
            )
        )
        provider_ic_repo = provider_ic_repo.reopen(config=config)
        provider_ic_repo.save_config()

        # The subscription VCAP is auto-created when the marketplace listing is created
        async with vcap_for_bucket(async_client, org_a, virtual_chunk_bucket, public=public):
            listing = await create_marketplace_listing(token, org_a, parent_repo_obj.id, pricing_model=pricing_model)

            yield (
                client,
                async_client,
                org_a,
                org_b,
                parent_repo_obj,
                provider_repo_bucket,
                subscriber_bucket,
                vcc_url_prefix,
                listing,
            )


@pytest.mark.asyncio
@pytest.mark.parametrize("public", [True, False], ids=["public-vcap", "private-vcap"])
class TestSubscriptionToRepoContainingVirtualChunks:
    """Test that subscription repos resolve VCCs against the provider org's VCAPs.

    All tests share a common setup via `provider_with_virtual_chunks`:
    - Org A (provider): repo on anonymous bucket with a VCC pointing to a separate
      virtual chunk bucket, and a VCAP covering that bucket.
    - Org B (subscriber): writable bucket for subscriber storage.

    Each test creates a different subscription type and verifies that VCC resolution
    works for public VCAPs and is rejected for private VCAPs.
    """

    async def test_direct_subscription(self, two_isolated_orgs, default_bucket, token, public):
        """Direct subscription: subscriber shares the provider's storage and VCCs."""
        # Direct subscriptions are only allowed on free listings
        async with provider_with_virtual_chunks(two_isolated_orgs, default_bucket, token, public, pricing_model="free") as (
            client,
            _,
            _,
            org_b,
            _,
            _,
            _,
            vcc_url_prefix,
            listing,
        ):
            await create_subscription_repo(token, org_b, "sub-repo", listing["id"])
            assert_subscription_vcap_resolution(client, f"{org_b}/sub-repo", {vcc_url_prefix}, public)

    @pytest.mark.skipif(not IS_IC2, reason="Paid marketplace listings require icechunk 2.x")
    async def test_filtered_subscription_provider_repo_contains_virtual_chunks(self, two_isolated_orgs, default_bucket, token, public):
        """Filtered subscription where the provider repo also contains virtual chunks.

        The subscriber has its own bucket and icechunk repo with two VCCs:
        1. Virtual chunks VCC (from shared setup, covered by the explicit VCAP - public/private)
        2. Provider repo chunks VCC (covered by the auto-created subscription VCAP, with runtime_vcc_name)

        The parametrization tests the explicit VCAP visibility for the virtual chunk bucket.
        When public=False, the repo open should fail because the virtual chunks aren't accessible.
        """
        async with provider_with_virtual_chunks(two_isolated_orgs, default_bucket, token, public) as (
            client,
            async_client,
            _,
            org_b,
            parent_repo_obj,
            provider_repo_bucket,
            subscriber_bucket,
            vcc_url_prefix,
            listing,
        ):
            repo_prefix = parent_repo_obj.prefix.strip("/")
            chunks_vcc_url_prefix = f"s3://{provider_repo_bucket.name}/{repo_prefix}/chunks/"

            # The subscription VCAP (auto-created) covers provider repo chunks
            # The explicit VCAP (public/private) covers the virtual chunk bucket
            await create_filtered_subscription_repo(
                token,
                org_b,
                "sub-repo",
                listing["id"],
                bucket_nickname=subscriber_bucket.nickname,
                target_filter={"nodes": {"include_paths": ["/data"]}},
            )

            # Open the icechunk repo created by the server during filtered subscription creation.
            # We can't use the AL client get_repo/open_repo because setting cross-org VCCs isn't normally allowed.
            sub_repo_obj = await async_client.get_repo_object(f"{org_b}/sub-repo")
            ic_storage = icechunk.s3_storage(
                bucket=subscriber_bucket.name,
                prefix=sub_repo_obj.prefix,
                region="us-east-1",
                endpoint_url="http://localhost:9000",
                allow_http=True,
                access_key_id="minio123",
                secret_access_key="minio123",
                force_path_style=True,
            )
            sub_ic_repo = icechunk.Repository.open(storage=ic_storage)

            # VCC 1: inherited from provider — virtual chunks bucket (explicit VCAP, public/private)
            # This VCC still needs to be set manually as it's not part of the filtered subscription flow
            config = sub_ic_repo.config
            config.set_virtual_chunk_container(
                icechunk.VirtualChunkContainer(
                    url_prefix=vcc_url_prefix,
                    store=icechunk.s3_store(),
                )
            )
            sub_ic_repo = sub_ic_repo.reopen(config=config)
            sub_ic_repo.save_config()

            # VCC 2: provider repo chunks VCC — now created automatically via runtime_vcc_name
            # when client.get_repo() is called (server returns runtime_vcc_name="__al_source")
            assert_subscription_vcap_resolution(client, f"{org_b}/sub-repo", {vcc_url_prefix, chunks_vcc_url_prefix}, public)

            # Verify that the runtime VCC was created with the correct name.
            # When public=False, assert_subscription_vcap_resolution already verified that
            # repo open fails, so we can't (and don't need to) check VCC details.
            if public:
                sub_repo = client.get_repo(f"{org_b}/sub-repo")
                TestAuthorization.assert_prefixes_authorized(sub_repo, {vcc_url_prefix, chunks_vcc_url_prefix})
                vccs = sub_repo.config.virtual_chunk_containers
                assert chunks_vcc_url_prefix in vccs, f"Expected VCC for '{chunks_vcc_url_prefix}' in config"
                # VCC name persistence requires icechunk 2.x
                if icechunk.__version__.startswith("2."):
                    assert vccs[chunks_vcc_url_prefix].name == "__al_source"


REFRESH_PREFIX = "s3://bucket/prefix/"
REFRESH_EXPIRY = datetime(2099, 1, 1, tzinfo=UTC)


def _delegated_s3_vcc(expiration=REFRESH_EXPIRY):
    return VirtualChunkCredentials(
        credentials=S3Credentials(
            aws_access_key_id="key", aws_secret_access_key="secret", aws_session_token="token", expiration=expiration
        ),
        org="myorg",
        bucket_nickname="mybucket",
        platform="s3",
    )


def _delegated_gs_vcc():
    return VirtualChunkCredentials(
        credentials=GSCredentials(access_token="atoken", principal="p", expiration=REFRESH_EXPIRY),
        org="myorg",
        bucket_nickname="mybucket",
        platform="gs",
    )


def _patched_metastore(client, vcc_credentials):
    mstore = MagicMock()
    mstore.open_repo = AsyncMock(return_value=SimpleNamespace(virtual_chunk_credentials=vcc_credentials, repo_credentials=None))
    return patch.object(client, "_metastore_for_org", return_value=mstore), mstore


class TestVirtualChunkCredentialRefresh:
    def test_refresh_func_built_for_delegated_s3(self, test_token):
        client = AsyncClient(token=test_token)
        func = client._maybe_get_vcc_credential_refresh_func(_delegated_s3_vcc(), "myorg", "myrepo", REFRESH_PREFIX)
        assert func is not None
        assert func.func == client._get_icechunk_s3_vcc_credentials_refresh_function
        assert func.args == ("myorg", "myrepo", REFRESH_PREFIX, "s3")

    def test_refresh_func_built_for_delegated_gs(self, test_token):
        client = AsyncClient(token=test_token)
        func = client._maybe_get_vcc_credential_refresh_func(_delegated_gs_vcc(), "myorg", "myrepo", REFRESH_PREFIX)
        assert func is not None
        assert func.func == client._get_icechunk_gcs_vcc_credentials_refresh_function
        assert func.args == ("myorg", "myrepo", REFRESH_PREFIX, "gs")

    def test_no_refresh_func_for_anonymous_creds(self, test_token):
        client = AsyncClient(token=test_token)
        vcc = VirtualChunkCredentials(credentials=None, org="myorg", bucket_nickname="mybucket", platform="s3")
        assert client._maybe_get_vcc_credential_refresh_func(vcc, "myorg", "myrepo", REFRESH_PREFIX) is None

    def test_no_refresh_func_for_non_expiring_creds(self, test_token):
        client = AsyncClient(token=test_token)
        vcc = _delegated_s3_vcc(expiration=None)
        assert client._maybe_get_vcc_credential_refresh_func(vcc, "myorg", "myrepo", REFRESH_PREFIX) is None

    def test_no_refresh_func_for_azure(self, test_token):
        client = AsyncClient(token=test_token)
        vcc = VirtualChunkCredentials(
            credentials=AzureCredentials(sas_token="sas", storage_account="acct", expiration=REFRESH_EXPIRY),
            org="myorg",
            bucket_nickname="mybucket",
            platform="azure",
        )
        assert client._maybe_get_vcc_credential_refresh_func(vcc, "myorg", "myrepo", REFRESH_PREFIX) is None

    def test_s3_refresh_function_reopens_repo(self, test_token):
        client = AsyncClient(token=test_token)
        patcher, mstore = _patched_metastore(client, {REFRESH_PREFIX: _delegated_s3_vcc()})
        with patcher:
            result = client._get_icechunk_s3_vcc_credentials_refresh_function("myorg", "myrepo", REFRESH_PREFIX, "s3")
        assert isinstance(result, icechunk.S3StaticCredentials)
        assert result.access_key_id == "key"
        assert result.session_token == "token"
        mstore.open_repo.assert_awaited_once_with("myrepo")

    def test_gcs_refresh_function_reopens_repo(self, test_token):
        client = AsyncClient(token=test_token)
        patcher, mstore = _patched_metastore(client, {REFRESH_PREFIX: _delegated_gs_vcc()})
        with patcher:
            result = client._get_icechunk_gcs_vcc_credentials_refresh_function("myorg", "myrepo", REFRESH_PREFIX, "gs")
        assert isinstance(result, icechunk.GcsBearerCredential)
        assert result.bearer == "atoken"
        mstore.open_repo.assert_awaited_once_with("myrepo")

    @pytest.mark.asyncio
    async def test_refresh_raises_when_prefix_no_longer_authorized(self, test_token):
        client = AsyncClient(token=test_token)
        patcher, _ = _patched_metastore(client, {})
        with patcher, pytest.raises(ValueError, match="Could not refresh credentials"):
            await client._get_vcc_credentials_from_repo("myorg", "myrepo", REFRESH_PREFIX, "s3")
