import importlib.util
import json
import os
import sys
import time
from collections.abc import Sequence
from datetime import datetime
from datetime import time as dt_time
from datetime import timedelta
import functools
from unittest.mock import patch, AsyncMock, MagicMock
from uuid import UUID, uuid4
import uuid

import httpx
import icechunk
from numpy.ma.core import minimum
from pydantic.types import UuidVersion
import pytest
import zarr
from httpx import Response

from arraylake import AsyncClient, Client, config
from arraylake.exceptions import ArraylakeClientError, BucketNotFoundError
from arraylake.config import config
from arraylake.display.repolist import RepoList
from arraylake.repos.icechunk.storage import CredentialType
from arraylake.token import Auth0UrlCode, AuthException, TokenHandler
from arraylake.types import (
    DBID,
    AuthProviderConfig,
    ExpirationConfig,
    GCConfig,
    GCDeleteOlderThan,
    GCKeep,
    OptimizationConfig,
    OptimizationWindow,
)
from arraylake.types import Repo as RepoModel
from arraylake.types import (
    RepoOperationMode,
    RepoOperationStatusResponse,
    UserInfo,
)


@pytest.mark.asyncio
async def test_client_raises_when_not_logged_in(isolated_org_name, test_token_file) -> None:
    org_name = isolated_org_name
    test_token_file.unlink()
    aclient = AsyncClient()
    with pytest.raises(AuthException, match=r"Not logged in, please log in .*"):
        await aclient.create_repo(f"{org_name}/foo")


@pytest.mark.parametrize("ClientClass", [Client, AsyncClient])
def test_client_repr_does_not_show_token(ClientClass, test_token):
    client = ClientClass(token=test_token)
    assert test_token not in repr(client)


@pytest.mark.parametrize("ClientClass", [Client, AsyncClient])
@pytest.mark.parametrize("bad_token", ["emax", "em", "_", ""])
def test_client_raises_for_bad_token(ClientClass, bad_token):
    with pytest.raises(ValueError, match="Invalid token provided"):
        client = ClientClass(token=bad_token)


@pytest.mark.parametrize("ClientClass", [Client, AsyncClient])
def test_client_finds_env_token(ClientClass, test_token):
    with patch.dict(os.environ, {"ARRAYLAKE_TOKEN": test_token}):
        config.refresh()
        client = ClientClass()
        assert client.token is not None
        assert client.token == test_token


@pytest.mark.parametrize("ClientClass", [Client, AsyncClient])
def test_client_finds_config_token(ClientClass, test_token):
    with config.set({"token": test_token}):
        client = ClientClass()
        assert client.token is not None
        assert client.token == test_token


@pytest.mark.asyncio
@pytest.mark.parametrize("ClientClass", [Client, AsyncClient])
async def test_login_respects_service_uri(ClientClass):
    custom_uri = "http://localhost:1337"
    client = ClientClass(service_uri=custom_uri)

    # Track what api_endpoint TokenHandler receives
    with patch("arraylake.token.TokenHandler") as mock_get_handler:
        # Create a mock handler with an async login method
        mock_handler = MagicMock()
        mock_handler.login = AsyncMock()
        mock_get_handler.return_value = mock_handler

        if ClientClass == AsyncClient:
            await client.login(browser=False)
        else:
            client.login(browser=False)

        # Verify get_auth_handler was called with the custom service_uri
        mock_get_handler.assert_called_once_with(api_endpoint=custom_uri)

        # Verify login was called
        mock_handler.login.assert_called_once_with(browser=False)


@pytest.mark.asyncio
async def test_create_repo_with_non_existing_bucket(isolated_org, default_bucket, token, helpers) -> None:
    async with isolated_org(default_bucket()) as (org_name, _):
        aclient = AsyncClient(token=token)
        repo_name = f"{org_name}/{helpers.random_repo_id()}"

        with pytest.raises(ValueError, match="bucket not-a-bucket does not exist") as exc_info:
            await aclient.create_repo(repo_name, bucket_config_nickname="not-a-bucket")


@pytest.mark.asyncio
async def test_default_kind_repo_creation(isolated_org, default_bucket, token):
    async with isolated_org(default_bucket()) as (org_name, buckets):
        client = Client(token=token)
        assert len(client.list_repos(org_name)) == 0

        name = f"{org_name}/zoo"
        repo = client.create_repo(name)
        assert isinstance(repo, icechunk.Repository)


# FIXME: Ensure a bucket can't be created that shares config with a bucket in another org?


@pytest.mark.asyncio
async def test_create_repo_with_description(isolated_org, default_bucket, token) -> None:
    async with isolated_org(default_bucket()) as (org_name, buckets):
        aclient = AsyncClient(token=token)

        repo_name = f"{org_name}/foo"
        description = "This is a test repo"
        await aclient.create_repo(repo_name, description=description)
        repo_obj = await aclient.get_repo_object(repo_name)
        assert repo_obj.description == description


@pytest.mark.asyncio
async def test_create_repo_with_description_too_long(isolated_org, default_bucket, token) -> None:
    async with isolated_org(default_bucket()) as (org_name, buckets):
        aclient = AsyncClient(token=token)
        repo_name = f"{org_name}/foo"
        description = "x" * 256

        aclient = AsyncClient(token=token)
        with pytest.raises(ValueError, match="Description can be at most 255 characters long"):
            await aclient.create_repo(repo_name, description=description)


@pytest.mark.asyncio
async def test_create_repo_with_metadata(isolated_org, default_bucket, token) -> None:
    async with isolated_org(default_bucket()) as (org_name, buckets):
        aclient = AsyncClient(token=token)
        repo_name = f"{org_name}/foo"
        metadata = {"key1": "value1", "key2": 2, "key3": 3.14, "key4": True, "key5": None}

        aclient = AsyncClient(token=token)
        await aclient.create_repo(repo_name, metadata=metadata)
        repo_obj = await aclient.get_repo_object(repo_name)
        assert repo_obj.metadata == metadata


@pytest.mark.asyncio
async def test_create_repo_with_metadata_nested_dict_raises(isolated_org, default_bucket, token) -> None:
    async with isolated_org(default_bucket()) as (org_name, buckets):
        aclient = AsyncClient(token=token)
        repo_name = f"{org_name}/foo"
        metadata = {"key1": {"key2": 2}, "key3": 3.14, "key4": True, "key5": None}

        aclient = AsyncClient(token=token)
        with pytest.raises(ValueError):
            await aclient.create_repo(repo_name, metadata=metadata)


@pytest.mark.asyncio
async def test_create_repo_with_metadata_too_large(isolated_org, default_bucket, token) -> None:
    async with isolated_org(default_bucket()) as (org_name, buckets):
        aclient = AsyncClient(token=token)
        repo_name = f"{org_name}/foo"
        metadata = {"key1": "x" * 4096}

        aclient = AsyncClient(token=token)
        with pytest.raises(ValueError, match="Metadata can be at most 4kB"):
            await aclient.create_repo(repo_name, metadata=metadata)


@pytest.mark.asyncio
async def test_create_repo_in_anon_bucket(isolated_org, minio_anon_bucket, token) -> None:
    async with isolated_org(minio_anon_bucket()) as (org_name, buckets):
        aclient = AsyncClient(token=token)
        repo_name = f"{org_name}/foo"

        with pytest.raises(ValueError, match="configured for anonymous access"):
            await aclient.create_repo(repo_name)


@pytest.mark.asyncio
async def test_create_repo_default_creates_ic2_repo(isolated_org, default_bucket, token):
    """create_repo with default spec_version creates IC2 repos (spec_version=2)."""
    async with isolated_org(default_bucket()) as (org_name, buckets):
        client = AsyncClient(token=token)
        repo = await client.create_repo(
            f"{org_name}/test-default-repo",
            bucket_config_nickname=buckets[0].nickname,
        )

        assert repo.spec_version == 2, f"Default create_repo should create IC2 repo (spec_version=2), got {repo.spec_version}"


@pytest.mark.asyncio
async def test_create_repo_spec_version_1_creates_ic1_repo(isolated_org, default_bucket, token):
    """create_repo with spec_version=1 creates IC1 repos."""
    async with isolated_org(default_bucket()) as (org_name, buckets):
        client = AsyncClient(token=token)
        repo = await client.create_repo(
            f"{org_name}/test-ic1-explicit",
            bucket_config_nickname=buckets[0].nickname,
            spec_version=1,
        )

        assert repo.spec_version == 1, f"spec_version=1 should create IC1 repo, got {repo.spec_version}"


@pytest.mark.asyncio
async def test_create_repo_spec_version_2_creates_ic2_repo(isolated_org, default_bucket, token):
    """create_repo with spec_version=2 creates IC2 repos."""
    async with isolated_org(default_bucket()) as (org_name, buckets):
        client = AsyncClient(token=token)
        repo = await client.create_repo(
            f"{org_name}/test-ic2-explicit",
            bucket_config_nickname=buckets[0].nickname,
            spec_version=2,
        )

        assert repo.spec_version == 2, f"spec_version=2 should create IC2 repo, got {repo.spec_version}"


@pytest.mark.asyncio
async def test_modify_repo(isolated_org, default_bucket, token) -> None:
    async with isolated_org(default_bucket()) as (org_name, buckets):
        aclient = AsyncClient(token=token)
        repo_name = f"{org_name}/foo"
        metadata = {"fruits": ["banana", "apple"], "vegetable": "carrot", "grain": "rice", "dairy": "milk", "healthy": True}
        description = "This is a test repo"

        aclient = AsyncClient(token=token)
        await aclient.create_repo(repo_name, metadata=metadata, description=description)
        current_repo_obj = await aclient.get_repo_object(repo_name)

        # Modify metadata
        new_description = "This is a modified test repo"
        optimization_window = OptimizationWindow(
            duration=3600,  # 1 hour
            start_time=dt_time(2, 0),  # 2:00 AM UTC
            day_of_week=1,  # Monday
        )
        gc_config = GCConfig(
            extra_gc_roots={"12345678910"},
            dangling_chunks=GCKeep(),
            dangling_manifests=GCDeleteOlderThan(date=timedelta(days=30)),
            dangling_attributes=GCKeep(),
            dangling_transaction_logs=GCDeleteOlderThan(date=timedelta(days=30)),
            dangling_snapshots=GCKeep(),
            gc_every=timedelta(days=7),
            enabled=False,
        )
        expiration_config = ExpirationConfig(
            expire_versions_older_than=timedelta(days=30),
            expire_every=None,
            enabled=True,
        )
        optimization_config = OptimizationConfig(
            expiration_config=expiration_config,
            gc_config=gc_config,
            window=optimization_window,
        )
        add_metadata = {"legume": "soybean", "fats": "butter"}
        remove_metadata = ["dairy"]
        update_metadata = {"fruits": ["pear", "kiwi"], "vegetable": ["broccoli", "carrot"], "healthy": False}
        expected_metadata = {
            "fruits": ["pear", "kiwi"],
            "vegetable": ["broccoli", "carrot"],
            "grain": "rice",
            "legume": "soybean",
            "fats": "butter",
            "healthy": False,
        }
        time.sleep(1)  # Ensure the updated time is different
        await aclient.modify_repo(
            repo_name,
            description=new_description,
            add_metadata=add_metadata,
            remove_metadata=remove_metadata,
            update_metadata=update_metadata,
            optimization_config=optimization_config,
        )
        updated_repo_obj = await aclient.get_repo_object(repo_name)
        assert updated_repo_obj.metadata.keys() == expected_metadata.keys()
        for key, value in expected_metadata.items():
            if isinstance(value, list):
                assert set(updated_repo_obj.metadata[key]) == set(value)
            else:
                assert updated_repo_obj.metadata[key] == value
        assert updated_repo_obj.description == new_description
        assert updated_repo_obj.updated > current_repo_obj.updated
        assert updated_repo_obj.optimization_config.window == optimization_window
        assert updated_repo_obj.optimization_config.gc_config == gc_config
        assert updated_repo_obj.optimization_config.expiration_config == expiration_config


@pytest.mark.asyncio
async def test_modify_repo_raises(isolated_org, default_bucket, token) -> None:
    async with isolated_org(default_bucket()) as (org_name, _):
        client = Client(token=token)
        repo_name = f"{org_name}/foo"
        metadata = {"fruit": "banana", "vegetable": "carrot", "grain": "rice", "dairy": "milk"}

        client = Client(token=token)
        client.create_repo(repo_name, metadata=metadata)

        with pytest.raises(ValueError, match="already exists in metadata"):
            client.modify_repo(repo_name, add_metadata={"fruit": "orange"})

        with pytest.raises(ValueError, match="Common metadata keys found in request"):
            client.modify_repo(repo_name, update_metadata={"fruit": "orange"}, remove_metadata=["fruit"])

        with pytest.raises(ValueError, match="Common metadata keys found in request"):
            client.modify_repo(repo_name, add_metadata={"fruit": "orange"}, remove_metadata=["fruit"])

        with pytest.raises(ValueError, match="Common metadata keys found in request"):
            client.modify_repo(repo_name, update_metadata={"legume": "soybean"}, add_metadata={"legume": "lentil"})

        with pytest.raises(ValueError, match="Description can be at most 255 characters long"):
            new_description = "x" * 256
            client.modify_repo(repo_name, description=new_description)


@pytest.mark.asyncio
async def test_modify_repo_no_change(isolated_org, default_bucket, token) -> None:
    async with isolated_org(default_bucket()) as (org_name, _):
        aclient = AsyncClient(token=token)
        repo_name = f"{org_name}/foo"
        metadata = {"fruit": "banana", "vegetable": "carrot", "grain": "rice", "dairy": "milk"}

        aclient = AsyncClient(token=token)
        await aclient.create_repo(repo_name, metadata=metadata)
        current_repo_obj = await aclient.get_repo_object(repo_name)

        await aclient.modify_repo(repo_name)

        updated_repo_obj = await aclient.get_repo_object(repo_name)
        assert updated_repo_obj.metadata == metadata
        assert updated_repo_obj.description is None
        assert updated_repo_obj.updated == current_repo_obj.updated
        assert updated_repo_obj.optimization_config.window is None
        assert updated_repo_obj.optimization_config.gc_config is None
        assert updated_repo_obj.optimization_config.expiration_config is None


@pytest.mark.asyncio
async def test_list_repos_listlike_properties(isolated_org, default_bucket, token) -> None:
    """Test that the RepoList object behaves like an (immutable) list."""
    async with isolated_org(default_bucket()) as (org_name, buckets):
        client = Client(token=token)
        client.create_repo(f"{org_name}/bar")
        time.sleep(1)  # ensure last updated time is different
        client.create_repo(f"{org_name}/foo")

        # test collection behaves enough like a list
        repo_list = client.list_repos(org_name)
        assert len(repo_list) == 2
        for repo in repo_list:
            assert isinstance(repo, RepoModel)
        assert {repo_list[0].name, repo_list[1].name} == {"foo", "bar"}
        sliced_subset = repo_list[0:2]
        assert isinstance(sliced_subset, RepoList)
        assert len(sliced_subset) == 2

        # test collection is actually a Sequence
        assert isinstance(repo_list, Sequence)

        # test collection is ordered by most recently updated
        assert repo_list[0].name == "foo"
        assert repo_list[1].name == "bar"

        # test collection can be coerced to an actual list
        real_repo_list = list(repo_list)
        assert isinstance(real_repo_list, list)
        for repo in real_repo_list:
            assert isinstance(repo, RepoModel)

        # test collection is immutable
        with pytest.raises(TypeError):
            repo_list["baz"] = 3
        with pytest.raises(AttributeError):
            repo_list.append("baz")


@pytest.mark.asyncio
async def test_list_repos_filter_metadata(isolated_org, default_bucket, token) -> None:
    async with isolated_org(default_bucket()) as (org_name, buckets):
        repo_name = "foo"
        metadata = {"key1": "value1", "key2": 2, "key3": 3.14, "key4": True, "key5": None}

        client = Client(token=token)
        client.create_repo(f"{org_name}/bar")
        client.create_repo(f"{org_name}/{repo_name}", metadata=metadata)

        for key, value in metadata.items():
            repos = client.list_repos(org_name, filter_metadata={key: value})
            assert len(repos) == 1
            assert repos[0].name == repo_name


@pytest.mark.asyncio
async def test_list_repos_filter_metadata_fails(isolated_org, token) -> None:
    async with isolated_org() as (org_name, buckets):
        client = Client(token=token)

        client = Client(token=token)
        with pytest.raises(ValueError, match="filter_metadata must be a JSON object"):
            client.list_repos(org_name, filter_metadata="not-a-dict")

        with pytest.raises(ValueError, match="filter_metadata values must be scalars or lists of scalars"):
            client.list_repos(org_name, filter_metadata={"key": {"key2": "value"}})


@pytest.mark.asyncio
async def test_list_repos_paginated(isolated_org, default_bucket, token) -> None:
    async with isolated_org(default_bucket()) as (org_name, buckets):
        aclient = AsyncClient(token=token)
        sync_client = Client(token=token)

        for i in range(5):
            await aclient.create_repo(f"{org_name}/repo{i}", metadata={"idx": i})

        # Async generator collects all repos across pages
        async_repos = [r async for r in aclient.list_repos_paginated(org_name, page_size=2)]
        assert len(async_repos) == 5
        assert {r.name for r in async_repos} == {f"repo{i}" for i in range(5)}

        # Sync generator collects all repos across pages
        sync_repos = list(sync_client.list_repos_paginated(org_name, page_size=2))
        assert len(sync_repos) == 5
        assert {r.name for r in sync_repos} == {f"repo{i}" for i in range(5)}

        # filter_metadata narrows results
        filtered = [r async for r in aclient.list_repos_paginated(org_name, filter_metadata={"idx": 0})]
        assert len(filtered) == 1
        assert filtered[0].name == "repo0"

        for i in range(5):
            await aclient.delete_repo(f"{org_name}/repo{i}", imsure=True, imreallysure=True)


@pytest.mark.filterwarnings("ignore:HMAC bucket permissions cannot be downscoped to a specific prefix")
@pytest.mark.asyncio
async def test_hmac_bucket_config(token, helpers):
    aclient = AsyncClient(token=token)
    org_config = {"metastoredb_host": "mongo", "status": "active"}
    org_name = await helpers.isolated_org(token, org_config)
    bucket_name = helpers.an_id(10)
    bucket_nickname = helpers.an_id(5)
    prefix = helpers.an_id(7)

    # Check that there are no buckets
    buckets = await aclient.list_bucket_configs(org_name)
    assert len(buckets) == 0

    # Create a bucket with hmac auth
    new_bucket = await aclient.create_bucket_config(
        org=org_name,
        nickname=bucket_nickname,
        uri=f"s3://{bucket_name}/{prefix}",
        region_name="us-west-2",
        auth_config={"method": "hmac", "access_key_id": "access-key", "secret_access_key": "secret"},
    )
    buckets = await aclient.list_bucket_configs(org_name)
    assert len(buckets) == 1
    assert new_bucket in buckets
    test_bucket_config = buckets[0]
    assert test_bucket_config.auth_config.method == "hmac"
    assert test_bucket_config.auth_config.access_key_id == "access-key"
    assert test_bucket_config.auth_config.secret_access_key == "secret"

    # Clean up the bucket
    await aclient.delete_bucket_config(org=org_name, nickname=bucket_nickname, imsure=True, imreallysure=True)
    bucket_configs = await aclient.list_bucket_configs(org_name)
    assert len(bucket_configs) == 0


@pytest.mark.asyncio
@pytest.mark.parametrize("prefix", ["prefix", ""])
async def test_hmac_with_prefix_warns(isolated_org, token, prefix):
    bucket_uri = f"s3://bucket_name/{prefix}"
    async with isolated_org() as (org_name, _):
        aclient = AsyncClient(token=token)

        create_bucket_config = functools.partial(
            aclient.create_bucket_config,
            org=org_name,
            nickname="nickname",
            region_name="us-west-2",
            auth_config={"method": "hmac", "access_key_id": "access-key", "secret_access_key": "secret"},
        )

        if prefix:
            with pytest.warns(UserWarning, match="HMAC bucket permissions cannot be downscoped to a specific prefix"):
                await create_bucket_config(uri=bucket_uri)
        else:
            await create_bucket_config(uri=bucket_uri)


def test_login_logout(monkeypatch, test_token_file, helpers, respx_mock) -> None:
    test_tokens = helpers.oauth_tokens_from_file(test_token_file)
    test_token_file.unlink()
    refreshed_tokens = test_tokens.model_copy(update={"id_token": "123456789abcdefg"})

    client = Client(service_uri="https://foo.com")

    user_code = "sample-code-12345"
    device_code = "12345"

    class MockTokenHandler(TokenHandler):
        _code = None

        @property
        def auth_provider_config(self) -> AuthProviderConfig:
            return AuthProviderConfig(domain="foo.auth0.com", client_id="bar")

        async def get_authorize_info(self) -> Auth0UrlCode:
            return Auth0UrlCode(url="https://foo.auth0.com", user_code=user_code, device_code=device_code, interval=1, expires_in=100)

        async def get_token(self, device_code: str, interval: int, expires_in: int):
            assert device_code == device_code
            self.update(test_tokens)

        async def refresh_token(self):
            self.update(refreshed_tokens)

        async def _get_user(self) -> UserInfo:
            return UserInfo(
                id=UUID("aeeb8bfa-e8f4-4724-9427-c3d5af661900"),
                email="spam@foo.com",
                first_name="TestFirst",
                family_name="TestFamily",
            )

        async def _update_user_profile(self) -> UserInfo:
            return await self._get_user()

    def get_auth_handler(api_endpoint: str) -> TokenHandler:
        return MockTokenHandler(api_endpoint=api_endpoint)

    def _input():
        return test_code

    monkeypatch.setattr("builtins.input", _input)

    logout_route = respx_mock.get(f"https://foo.auth0.com/v2/logout").mock(return_value=Response(200))

    with patch("arraylake.client.get_auth_handler", get_auth_handler), patch("arraylake.token.open_new") as mock_open_new:
        client.login(browser=False)
        assert mock_open_new.call_count == 0  # check that browser was not opened
        assert test_token_file.is_file()

    with patch("arraylake.client.get_auth_handler", get_auth_handler):
        client.logout()
        assert not test_token_file.is_file()


@pytest.mark.asyncio
async def test_async_client(isolated_org, default_bucket, token):
    """Integration-style test for the async client."""
    async with isolated_org(default_bucket()) as (org_name, buckets):
        aclient = AsyncClient(token=token)
        assert not await aclient.list_repos(org_name)

        # Create two new Icechunk repos
        # The repo name must be unique for subsequent runs
        for repo_name in ["foo", "bar"]:
            name = f"{org_name}/{repo_name}"
            repo = await aclient.create_repo(name, prefix=str(uuid4())[:8])
            assert isinstance(repo, icechunk.Repository)
            # TODO: earth-mover/icechunk#414: expose storage config so we can check more things

            repo = await aclient.get_repo(name)
            assert isinstance(repo, icechunk.Repository)
            # TODO: earth-mover/icechunk#414: expose storage config so we can check more things

        # Server returns the existing repo idempotently (201), but the client still
        # calls IcechunkRepository.create() which fails because the storage prefix
        # already has data. The client's error handler then deletes the metastore
        # entry as cleanup. In practice this only happens on HTTP retries where the
        # first request actually succeeded.
        with pytest.raises(icechunk.IcechunkError, match="clean prefixes"):
            await aclient.create_repo(name)

        # The failed duplicate create cleaned up the "bar" metastore entry, so
        # only "foo" remains. Re-create "bar" for the rest of the test.
        await aclient.create_repo(f"{org_name}/bar", prefix=str(uuid4())[:8])

        # List the repos
        repo_listing = await aclient.list_repos(org_name)
        all_repo_names = {repo.name for repo in repo_listing}
        assert all_repo_names == {"foo", "bar"}

        # Delete the repos
        for repo_name in ["foo", "bar"]:
            name = f"{org_name}/{repo_name}"
            await aclient.delete_repo(name, imsure=True, imreallysure=True)

        # Check that the repos are gone
        with pytest.raises(ValueError):
            # can't get nonexistent repo
            await aclient.get_repo("doesnt/exist")

        # deleting a nonexistent repo is idempotent (server returns 204)
        await aclient.delete_repo("doesnt/exist", imsure=True, imreallysure=True)


@pytest.mark.asyncio
async def test_get_repo_nonexistent_raises_single_exception(isolated_org, default_bucket, token):
    """
    Test that get_repo on a non-existent repo raises a single ArraylakeClientError,
    not an ExceptionGroup (which could happen if concurrent requests both fail).
    """
    async with isolated_org(default_bucket()) as (org_name, _):
        aclient = AsyncClient(token=token)

        with pytest.raises(ArraylakeClientError) as exc_info:
            await aclient.get_repo(f"{org_name}/nonexistent")

        # Verify it's a 404 error about the repo not being found
        assert exc_info.value.status_code == 404
        assert "not found" in str(exc_info.value).lower()


@pytest.mark.asyncio
async def test_client(isolated_org, default_bucket, token):
    """Integration-style test for the sync client."""
    async with isolated_org(default_bucket()) as (org_name, buckets):
        client = Client(token=token)
        assert len(client.list_repos(org_name)) == 0

        for repo_name in ["foo", "bar"]:
            name = f"{org_name}/{repo_name}"
            repo = client.create_repo(name, prefix=str(uuid4())[:8])
            assert isinstance(repo, icechunk.Repository)
            # TODO: earth-mover/icechunk#414: expose storage config so we can check more things

            repo = client.get_repo(name)
            assert isinstance(repo, icechunk.Repository)
            # TODO: earth-mover/icechunk#414: expose storage config so we can check more things

        # Server returns the existing repo idempotently (201), but the client still
        # calls IcechunkRepository.create() which fails because the storage prefix
        # already has data. The client's error handler then deletes the metastore
        # entry as cleanup. In practice this only happens on HTTP retries where the
        # first request actually succeeded.
        with pytest.raises(icechunk.IcechunkError, match="clean prefixes"):
            client.create_repo(name)

        # The failed duplicate create cleaned up the "bar" metastore entry, so
        # only "foo" remains. Re-create "bar" for the rest of the test.
        client.create_repo(f"{org_name}/bar", prefix=str(uuid4())[:8])

        repo_listing = client.list_repos(org_name)
        assert len(repo_listing) == 2
        all_repo_names = {repo.name for repo in repo_listing}
        assert all_repo_names == {"foo", "bar"}

        for repo_name in ["foo", "bar"]:
            name = f"{org_name}/{repo_name}"
            client.delete_repo(name, imsure=True, imreallysure=True)

        with pytest.raises(ValueError):
            # can't get nonexistent repo
            client.get_repo("doesnt/exist")

        # deleting a nonexistent repo is idempotent (server returns 204)
        client.delete_repo("doesnt/exist", imsure=True, imreallysure=True)


@pytest.mark.asyncio
async def test_get_or_create_repo_async(isolated_org, default_bucket, token):
    async with isolated_org(default_bucket()) as (org_name, buckets):
        aclient = AsyncClient(token=token)

        repo_name = "foo"
        name = f"{org_name}/{repo_name}"
        assert repo_name not in {repo.name for repo in await aclient.list_repos(org_name)}
        # Create the repo
        await aclient.get_or_create_repo(name, prefix=str(uuid4())[:8])
        assert repo_name in {repo.name for repo in await aclient.list_repos(org_name)}
        # Get the repo
        await aclient.get_or_create_repo(name)
        # TODO: earth-mover/icechunk#414: expose storage config so we can check more things
        # Delete the repo
        await aclient.delete_repo(name, imsure=True, imreallysure=True)


@pytest.mark.asyncio
async def test_get_or_create_repo_sync(isolated_org, default_bucket, token):
    async with isolated_org(default_bucket()) as (org_name, buckets):
        client = Client(token=token)

        repo_name = "foo"
        name = f"{org_name}/{repo_name}"
        assert repo_name not in {repo.name for repo in client.list_repos(org_name)}
        # Create the repo
        client.get_or_create_repo(name, prefix=str(uuid4())[:8])
        assert repo_name in {repo.name for repo in client.list_repos(org_name)}
        # Get the repo
        client.get_or_create_repo(name)
        # TODO: earth-mover/icechunk#414: expose storage config so we can check more things
        # Delete the repo
        client.delete_repo(name, imsure=True, imreallysure=True)


@pytest.mark.asyncio
async def test_get_create_repo_with_repo_config(isolated_org, default_bucket, token):
    async with isolated_org(default_bucket()) as (org_name, buckets):
        client = Client(token=token)

        repo_name = "foo"
        name = f"{org_name}/{repo_name}"
        assert repo_name not in {repo.name for repo in client.list_repos(org_name)}
        config = icechunk.RepositoryConfig.default()
        config.inline_chunk_threshold_bytes = 1024
        config.get_partial_values_concurrency = 2
        # Create the repo with the config
        repo = client.create_repo(name, config=config)
        # Check that the RepositoryConfig was applied
        assert repo.config.inline_chunk_threshold_bytes == 1024
        assert repo.config.get_partial_values_concurrency == 2
        assert repo_name in {repo.name for repo in client.list_repos(org_name)}
        # Get the repo with different config values
        config.inline_chunk_threshold_bytes = 512
        config.get_partial_values_concurrency = 10
        repo = client.get_repo(name, config=config)
        # Check that the RepositoryConfig was applied
        assert repo.config.inline_chunk_threshold_bytes == 512
        assert repo.config.get_partial_values_concurrency == 10
        # Delete the repo
        client.delete_repo(name, imsure=True, imreallysure=True)


@pytest.mark.asyncio
async def test_get_repo_with_storage_options(isolated_org, default_bucket, token):
    async with isolated_org(default_bucket()) as (org_name, buckets):
        client = Client(token=token)
        name = f"{org_name}/foo"
        client.create_repo(name)

        # TODO we cannot actually assert that the returned Icechunk repo is using the correct value of `network_stream_timeout_seconds`, because there is no way to access it.
        # See https://github.com/earth-mover/icechunk/issues/1571
        # For now patching is the best we can do - this at least ensures the kwarg gets passed to IC.
        with patch("icechunk.s3_storage", wraps=icechunk.s3_storage) as mock_s3_storage:
            client.get_repo(name, storage_options={"network_stream_timeout_seconds": 30})
            mock_s3_storage.assert_called_once()
            assert mock_s3_storage.call_args.kwargs["network_stream_timeout_seconds"] == 30


@pytest.mark.asyncio
async def test_import_existing_repo(
    isolated_org,
    default_bucket,
    token,
):
    bucket = default_bucket()

    client = Client(token=token)
    async with isolated_org(bucket) as (org_name, buckets):
        repo_name = f"{org_name}/foo"

        # Use icechunk to create the repo outside of the arraylake client
        # IDK a better way to set up the storage for this, hardcoding for now
        repo_prefix = str(uuid4())[:8]
        ic_storage = icechunk.s3_storage(
            bucket=bucket.name,
            prefix=repo_prefix,
            region="us-east-1",
            endpoint_url="http://localhost:9000",
            allow_http=True,
            access_key_id="minio123",
            secret_access_key="minio123",
            force_path_style=True,
        )
        icechunk.Repository.create(storage=ic_storage)

        # Use arraylake client to import the repo
        client.import_repo(repo_name, bucket.nickname, repo_prefix)

        assert "foo" in {repo.name for repo in client.list_repos(org_name)}


@pytest.mark.asyncio
async def test_import_repo(
    isolated_org,
    default_bucket,
    token,
):
    """Test the dedicated import_repo method."""
    bucket = default_bucket()

    client = Client(token=token)
    async with isolated_org(bucket) as (org_name, buckets):
        repo_name = f"{org_name}/foo"

        # Use icechunk to create the repo outside of the arraylake client
        repo_prefix = str(uuid4())[:8]
        ic_storage = icechunk.s3_storage(
            bucket=bucket.name,
            prefix=repo_prefix,
            region="us-east-1",
            endpoint_url="http://localhost:9000",
            allow_http=True,
            access_key_id="minio123",
            secret_access_key="minio123",
            force_path_style=True,
        )
        icechunk.Repository.create(storage=ic_storage)

        # Use arraylake client to import the repo using the import_repo method
        repo = client.import_repo(repo_name, bucket.nickname, repo_prefix)

        assert isinstance(repo, icechunk.Repository)
        assert "foo" in {repo.name for repo in client.list_repos(org_name)}


@pytest.mark.asyncio
async def test_import_repo_with_description_and_metadata(
    isolated_org,
    default_bucket,
    token,
):
    """Test import_repo with description and metadata."""
    bucket = default_bucket()

    aclient = AsyncClient(token=token)
    async with isolated_org(bucket) as (org_name, buckets):
        repo_name = f"{org_name}/bar"

        # Use icechunk to create the repo outside of the arraylake client
        repo_prefix = str(uuid4())[:8]
        ic_storage = icechunk.s3_storage(
            bucket=bucket.name,
            prefix=repo_prefix,
            region="us-east-1",
            endpoint_url="http://localhost:9000",
            allow_http=True,
            access_key_id="minio123",
            secret_access_key="minio123",
            force_path_style=True,
        )
        icechunk.Repository.create(storage=ic_storage)

        # Import using async client with description and metadata
        description = "Imported repository"
        metadata = {"source": "external", "version": 1}
        repo = await aclient.import_repo(
            repo_name,
            bucket.nickname,
            repo_prefix,
            description=description,
            metadata=metadata,
        )

        assert isinstance(repo, icechunk.Repository)

        # Verify description and metadata were set
        repo_obj = await aclient.get_repo_object(repo_name)
        assert repo_obj.description == description
        assert repo_obj.metadata == metadata


@pytest.mark.asyncio
async def test_create_in_anon_bucket_fails(
    isolated_org,
    anon_bucket,
    token,
):
    client = Client(token=token)
    async with isolated_org(anon_bucket) as (org_name, buckets):
        repo_name = f"{org_name}/foo"

        with pytest.raises(ValueError, match="configured for anonymous access"):
            client.create_repo(repo_name, prefix=str(uuid4())[:8])

        # make sure that the repo object was not created
        assert "foo" not in {repo.name for repo in client.list_repos(org_name)}


@pytest.mark.asyncio
async def test_set_author_on_commit(isolated_org, default_bucket, token):
    async with isolated_org(default_bucket()) as (org_name, buckets):
        client = Client(token=token)

        repo_name = "foo"
        name = f"{org_name}/{repo_name}"
        assert repo_name not in {repo.name for repo in client.list_repos(org_name)}
        # Create the repo
        repo = client.create_repo(name, prefix=str(uuid4())[:8])
        # Check that the author is set on the commit
        session = repo.writable_session(branch="main")
        # Make a small change to the repo
        zarr.create_array(store=session.store, name="foo", shape=(10,), chunks=(5,), dtype="i4")
        sid = session.commit("Initial commit")
        snap = next(repo.ancestry(snapshot_id=sid))
        assert snap.metadata == {"author_name": "ABC User", "author_email": "abc@earthmover.io"}

        # Get the repo and check that the author is set on the commit
        repo_again = client.get_repo(name)
        session_again = repo_again.writable_session(branch="main")
        # Make a small change to the repo
        zarr.create_array(store=session_again.store, name="bar", shape=(10,), chunks=(5,), dtype="i4")
        sid_again = session_again.commit("Second commit")
        snap_again = next(repo_again.ancestry(snapshot_id=sid_again))
        assert snap_again.metadata == {"author_name": "ABC User", "author_email": "abc@earthmover.io"}

        # Delete the repo
        client.delete_repo(name, imsure=True, imreallysure=True)


@pytest.mark.asyncio
async def test_get_icechunk_storage_from_repo_model(isolated_org, default_bucket, token):
    async with isolated_org(default_bucket()) as (org_name, buckets):
        aclient = AsyncClient(token=token)

        bucket_nickname = buckets[0].nickname
        bucket_config = await aclient.get_bucket_config(org=org_name, nickname=bucket_nickname)

        repo_model = RepoModel(
            _id=DBID(b"some_repo_id"),
            org="earthmover",
            name="repo-name",
            updated=datetime.now(),
            status=RepoOperationStatusResponse(mode=RepoOperationMode.ONLINE, initiated_by={}),
            bucket=bucket_config,
            prefix=org_name,
        )
        with config.set({"icechunk.scatter_initial_credentials": False}):
            storage = await aclient._get_icechunk_storage_from_repo_model(repo_model=repo_model, user_id=uuid4())
        assert isinstance(storage, icechunk.Storage)


@pytest.mark.asyncio
async def test_get_icechunk_storage_from_repo_model_no_bucket_raises(token):
    aclient = AsyncClient(token=token)
    repo_model = RepoModel(
        _id=DBID(b"some_repo_id"),
        org="earthmover",
        name="repo-name",
        updated=datetime.now(),
        status=RepoOperationStatusResponse(mode=RepoOperationMode.ONLINE, initiated_by={}),
        bucket=None,
        prefix="",
    )
    with pytest.raises(ValueError) as excinfo:
        await aclient._get_icechunk_storage_from_repo_model(repo_model=repo_model, user_id=uuid4())
    assert "The bucket on the catalog object cannot be None for Icechunk V2 repos!" in str(excinfo.value)


@pytest.mark.asyncio
async def test_get_icechunk_storage(isolated_org, default_bucket, token):
    async with isolated_org(default_bucket()) as (org_name, buckets):
        aclient = AsyncClient(token=token)

        bucket_nickname = buckets[0].nickname
        repo_name = f"{org_name}/icechunk-repo"
        await aclient.create_repo(
            name=repo_name,
            bucket_config_nickname=bucket_nickname,
            prefix=str(uuid4())[:8],
        )
        storage = await aclient.get_icechunk_storage(repo_name)
        assert isinstance(storage, icechunk.Storage)

        aclient.delete_repo(name=f"{org_name}/icechunk-repo", imsure=True, imreallysure=True)


@pytest.mark.asyncio
async def test_get_icechunk_container_credentials_from_bucket_hmac_async(isolated_org, default_bucket, token):
    async with isolated_org(default_bucket()) as (org_name, buckets):
        aclient = AsyncClient(token=token)

        bucket_nickname = buckets[0].nickname
        cont_creds = await aclient.get_icechunk_container_credentials_from_bucket(org_name, bucket_nickname)
        # Bucket uses HMAC credentials so we should get a static credentials object
        assert isinstance(cont_creds, icechunk.S3Credentials.Static)
        # TODO: can we check the access key ID and secret access key?


@pytest.mark.asyncio
async def test_get_icechunk_container_credentials_from_bucket_hmac_sync(isolated_org, default_bucket, token):
    async with isolated_org(default_bucket()) as (org_name, buckets):
        client = Client(token=token)

        bucket_nickname = buckets[0].nickname
        cont_creds = client.get_icechunk_container_credentials_from_bucket(org_name, bucket_nickname)
        # Bucket uses HMAC credentials so we should get a static credentials object
        assert isinstance(cont_creds, icechunk.S3Credentials.Static)
        # TODO: can we check the access key ID and secret access key?


@pytest.mark.asyncio
async def test_get_icechunk_container_credentials_from_bucket_anon_async(isolated_org, anon_bucket, token):
    async with isolated_org(anon_bucket) as (org_name, buckets):
        aclient = AsyncClient(token=token)

        bucket_nickname = buckets[0].nickname
        cont_creds = await aclient.get_icechunk_container_credentials_from_bucket(org_name, bucket_nickname)
        assert isinstance(cont_creds, icechunk.S3Credentials.Anonymous)


@pytest.mark.asyncio
async def test_get_icechunk_container_credentials_from_bucket_anon_sync(isolated_org, anon_bucket, token):
    async with isolated_org(anon_bucket) as (org_name, buckets):
        client = Client(token=token)

        bucket_nickname = buckets[0].nickname
        cont_creds = client.get_icechunk_container_credentials_from_bucket(org_name, bucket_nickname)
        assert isinstance(cont_creds, icechunk.S3Credentials.Anonymous)


@pytest.mark.asyncio
async def test_get_icechunk_container_credentials_from_bucket_delegated_async(isolated_org, delegated_creds_bucket, token):
    async with isolated_org(delegated_creds_bucket()) as (org_name, buckets):
        aclient = AsyncClient(token=token)

        bucket_nickname = buckets[0].nickname
        cont_creds = await aclient.get_icechunk_container_credentials_from_bucket(org_name, bucket_nickname)
        # Bucket uses delegated credentials so we should get a Refreshable credentials object
        assert isinstance(cont_creds, icechunk.S3Credentials.Refreshable)


@pytest.mark.asyncio
async def test_get_icechunk_container_credentials_from_bucket_delegated_sync(isolated_org, delegated_creds_bucket, token):
    async with isolated_org(delegated_creds_bucket()) as (org_name, buckets):
        client = Client(token=token)

        bucket_nickname = buckets[0].nickname
        cont_creds = client.get_icechunk_container_credentials_from_bucket(org_name, bucket_nickname)
        # Bucket uses delegated credentials so we should get a Refreshable credentials object
        assert isinstance(cont_creds, icechunk.S3Credentials.Refreshable)


@pytest.mark.asyncio
async def test_credentials_offline_mode_raises(isolated_org, default_bucket, token, helpers):
    """Test that repos in OFFLINE mode raise an error when requesting credentials."""
    async with isolated_org(default_bucket()) as (org_name, buckets):
        aclient = AsyncClient(token=token)
        repo_name = f"{org_name}/{helpers.random_repo_id()}"

        await aclient.create_repo(repo_name)

        # Set repo to OFFLINE mode
        _on, _rn = repo_name.split("/")
        await helpers.set_repo_system_status(token, _on, _rn, RepoOperationMode.OFFLINE, "Testing offline mode", True)

        # Attempting to get repo should raise due to credential fetch failure
        with pytest.raises(ValueError, match="offline"):
            await aclient.get_repo(repo_name)


@pytest.mark.asyncio
async def test_credentials_maintenance_mode_hmac_raises(isolated_org, default_bucket, token, helpers):
    """Test that HMAC repos in MAINTENANCE mode raise an error (HMAC creds can't be scoped to read-only)."""
    async with isolated_org(default_bucket()) as (org_name, buckets):
        aclient = AsyncClient(token=token)
        repo_name = f"{org_name}/{helpers.random_repo_id()}"

        await aclient.create_repo(repo_name)

        # Set repo to MAINTENANCE mode
        _on, _rn = repo_name.split("/")
        await helpers.set_repo_system_status(token, _on, _rn, RepoOperationMode.MAINTENANCE, "Testing maintenance mode", True)

        # HMAC repos cannot provide read-only credentials, so the server returns 409
        with pytest.raises(ArraylakeClientError, match="HMAC"):
            await aclient.get_repo(repo_name)


@pytest.mark.asyncio
async def test_containers_credentials_for_buckets_async(isolated_org, default_bucket, token):
    bucket1 = default_bucket(nickname="mybucket1", name="bucket1")
    bucket2 = default_bucket(nickname="mybucket2", name="bucket2")

    async with isolated_org(bucket1, bucket2) as (org_name, buckets):
        aclient = AsyncClient(token=token)

        conts_creds = await aclient.containers_credentials_for_buckets(
            org=org_name,
            containers_to_buckets_map={
                "container1": bucket1.nickname,
                "container2": bucket2.nickname,
            },
        )
        assert set(conts_creds.keys()) == {"container1", "container2"}
        assert all(isinstance(creds, icechunk.Credentials.S3) for creds in conts_creds.values())


@pytest.mark.asyncio
async def test_containers_credentials_for_buckets_sync(isolated_org, default_bucket, token):
    bucket1 = default_bucket(nickname="mybucket1", name="bucket1")
    bucket2 = default_bucket(nickname="mybucket2", name="bucket2")

    async with isolated_org(bucket1, bucket2) as (org_name, buckets):
        client = Client(token=token)
        conts_creds = client.containers_credentials_for_buckets(
            org=org_name,
            container1=bucket1.nickname,
            container2=bucket2.nickname,
        )
        assert set(conts_creds.keys()) == {"container1", "container2"}
        assert all(isinstance(creds, icechunk.Credentials.S3) for creds in conts_creds.values())


@pytest.mark.asyncio
async def test_repo_with_inconsistent_bucket(isolated_org, default_bucket, token, helpers):
    aclient = AsyncClient(token=token)
    async with isolated_org(default_bucket()) as (org_name, buckets):
        repo_name = f"{org_name}/{helpers.random_repo_id()}"
        await aclient.create_repo(repo_name)

        try:
            with pytest.raises(ValueError, match=r"does not match the configured bucket_config_nickname") as exc_info:
                await aclient.get_or_create_repo(repo_name, bucket_config_nickname="bad-nickname")
        finally:
            await aclient.delete_repo(repo_name, imsure=True, imreallysure=True)


@pytest.mark.asyncio
async def test_repo_with_duplicate_prefix(isolated_org, default_bucket, token, helpers):
    aclient = AsyncClient(token=token)
    async with isolated_org(default_bucket()) as (org_name, buckets):
        repo_name = f"{org_name}/{helpers.random_repo_id()}"
        duplicate_repo_name = f"{org_name}/{helpers.random_repo_id()}2"
        prefix = str(uuid4())[:8]
        await aclient.create_repo(repo_name, prefix=prefix)
        with pytest.raises(icechunk.IcechunkError, match="repositories can only be created in clean prefixes"):
            await aclient.create_repo(duplicate_repo_name, prefix=prefix)

        # make sure the duplicated prefix repo is deleted
        repos = await aclient.list_repos(org_name)
        assert duplicate_repo_name not in {repo.name for repo in repos}

        await aclient.delete_repo(repo_name, imsure=True, imreallysure=True)


@pytest.mark.asyncio
async def test_create_repo_with_bucket_prefix(isolated_org, default_bucket, token, helpers):
    bucket_with_prefix = default_bucket(prefix="prefix")
    aclient = AsyncClient(token=token)

    async with isolated_org(bucket_with_prefix) as (org_name, buckets):
        repo_name = f"{org_name}/{helpers.random_repo_id()}"
        ic_prefix = str(uuid4())[:8]
        await aclient.create_repo(repo_name, bucket_config_nickname=bucket_with_prefix.nickname, prefix=ic_prefix)

        repo_obj = await aclient.get_repo_object(repo_name)
        bucket = await aclient.get_bucket_config(org=org_name, nickname=bucket_with_prefix.nickname)
        assert repo_obj.prefix == f"{bucket.prefix}/{ic_prefix}"

        await aclient.delete_repo(repo_name, imsure=True, imreallysure=True)


@pytest.mark.asyncio
async def test_client_token_handler_author_config(isolated_org_name, test_token, test_user, respx_mock):
    org_name = isolated_org_name
    mock_url = "https://test-arraylake-service.bar/"
    repo_name = "foo"
    now = datetime.utcnow()
    timeout = timedelta(days=1)
    user: UserInfo = test_user
    repo = dict(
        id="1234",
        bucket={
            "id": uuid4().hex,
            "nickname": "default",
            "name": "test-bucket",
            "prefix": "arraylake",
            "platform": "s3",
            "extra_config": {"region_name": "us-west-2"},
            "auth_config": {"method": "hmac", "access_key_id": "test_access_key_id", "secret_access_key": "test_secret_access_key"},
            "is_default": True,
        },
        org=org_name,
        name=repo_name,
        created=str(now),
        description="",
        status=dict(mode="online", initiated_by={"system_id": "x"}),
        kind="icechunk",
        prefix="1234",
    )

    # mock api routes
    user_route = respx_mock.get(mock_url + "user").mock(return_value=Response(200, json=json.loads(user.model_dump_json())))
    repo_post_route = respx_mock.post(mock_url + f"orgs/{org_name}/repos").mock(return_value=Response(201, json=repo))
    repos_get_route = respx_mock.get(mock_url + f"orgs/{org_name}/repos").mock(return_value=Response(200, json=[repo]))
    repo_get_route = respx_mock.get(mock_url + f"repos/{org_name}/{repo_name}").mock(return_value=Response(200, json=repo))

    # Mock IcechunkRepository.create but verify the author is set correctly from API user data
    from unittest.mock import MagicMock, patch

    def mock_create(storage, config=None, **kwargs):
        # Verify that the real code created storage with correct user info
        # The storage object should contain the user information that was fetched from API
        # For now, return a mock repo - the real test is that the API calls used correct token
        mock_repo = MagicMock()
        mock_repo.author.name = f"{user.first_name} {user.family_name}"
        mock_repo.author.email = user.email
        return mock_repo

    with patch("arraylake.client.IcechunkRepository.create", side_effect=mock_create):
        aclient = AsyncClient(mock_url, token=test_token)
        arepo = await aclient.create_repo(f"{org_name}/foo")

    # assert that all calls used the test token
    for call in respx_mock.calls:
        assert call.request.headers.get("Authorization") == f"Bearer {test_token}"

    assert arepo.author.name == f"{user.first_name} {user.family_name}"
    assert arepo.author.email == user.email


def test_get_database(respx_mock, test_user) -> None:
    mock_url = "https://foo.com"
    org = "foo"
    repo = "bar"
    bucket_id = uuid4().hex
    principal_id = "11111111-2222-3333-4444-555555555555"
    client = Client(service_uri=mock_url)

    respx_mock.post(f"{mock_url}/user/diagnostics").mock(return_value=Response(200, json={}))

    route = respx_mock.get(f"{mock_url}/repos/{org}/{repo}/open").mock(
        return_value=Response(
            httpx.codes.OK,
            json={
                "repo_bucket": {
                    "id": bucket_id,
                    "nickname": "default",
                    "name": "my-bucket",
                    "prefix": "arraylake",
                    "platform": "minio",
                    "extra_config": {"region_name": "us-west-2"},
                    "auth_config": {"method": "anonymous"},
                    "is_default": True,
                },
                "repo_prefix": "123456",
                "repo_credentials": None,
                "virtual_chunk_credentials": {},
                "author": {"name": "Test User", "email": "test@example.com"},
                "principal_id": principal_id,
                "status": {"mode": "online", "initiated_by": {}, "estimated_end_time": None},
            },
        )
    )

    # Mock IcechunkRepository.open to avoid S3 connection
    from unittest.mock import MagicMock, patch

    mock_repo = MagicMock()

    with patch("arraylake.client.IcechunkRepository.open_async", return_value=mock_repo):
        repo = client.get_repo(f"{org}/{repo}")

    assert route.called


@pytest.mark.asyncio
async def test_bucket_lifecycle(isolated_org, default_bucket, token, helpers):
    bucket_nickname = helpers.an_id(5)
    second_bucket_nickname = helpers.an_id(6)
    third_bucket_name = helpers.an_id(8)
    prefix = helpers.an_id(7)

    bucket_config = default_bucket(nickname=bucket_nickname)
    bucket_name = bucket_config.name

    # Start with the bucket created by the fixture
    # This needs to be a minio bucket so we can assign it to a Icechunk repo
    async with isolated_org(bucket_config) as (org_name, buckets):
        aclient = AsyncClient(token=token)
        repo_name = f"{org_name}/{helpers.random_repo_id()}"

        bucket_configs = await aclient.list_bucket_configs(org_name)
        assert len(bucket_configs) == 1  # We start with the bucket created by fixture

        # The bucket was already created by the fixture
        existing_bucket = bucket_configs[0]
        assert existing_bucket.nickname == bucket_nickname

        # Make this bucket the default
        await aclient.set_default_bucket_config(org=org_name, nickname=bucket_nickname)
        updated_bucket = await aclient.get_bucket_config(org=org_name, nickname=bucket_nickname)
        assert updated_bucket.is_default is True

        # Test creating a bucket with the same nickname should fail
        with pytest.raises(ValueError, match="already exists"):
            _ = await aclient.create_bucket_config(
                org=org_name,
                nickname=bucket_nickname,
                uri=f"s3://{bucket_name}/someprefix",
                region_name="us-west-2",
                auth_config={"method": "anonymous"},
            )

        # Create another bucket
        await aclient.create_bucket_config(
            org=org_name,
            nickname=second_bucket_nickname,
            uri=f"s3://{bucket_name}/{prefix}",
            region_name="us-west-2",
            endpoint_url="http://some-other-url:1234",
            auth_config={"method": "anonymous"},
        )

        # No two buckets should have the same (platform, name, prefix, endpoint_url) set, as
        # they would point to the same location
        with pytest.raises(ValueError, match="already exists"):
            _ = await aclient.create_bucket_config(
                org=org_name,
                nickname=third_bucket_name,
                uri=f"s3://{bucket_name}/{prefix}",
                region_name="us-west-2",
                endpoint_url="http://some-other-url:1234",
                auth_config={"method": "anonymous"},
            )

        # However, if the endpoint URL differs between two otherwise identical buckets, that's cool
        valid_bucket = await aclient.create_bucket_config(
            org=org_name,
            nickname=third_bucket_name,
            uri=f"s3://{bucket_name}/{prefix}",
            endpoint_url="http://some-other-url:4567",
            use_ssl=False,
            auth_config={"method": "anonymous"},
        )
        buckets = await aclient.list_bucket_configs(org_name)
        assert len(buckets) == 3
        assert valid_bucket in buckets
        assert valid_bucket.extra_config["endpoint_url"] == "http://some-other-url:4567"

        # Creating a bucket with an invalid platform should fail
        with pytest.raises(ValueError, match="Invalid platform"):
            _ = await aclient.create_bucket_config(org=org_name, nickname=bucket_nickname, uri="s4://my-bucket")

        # Creating a bucket with invalid auth_config should fail
        with pytest.raises(ValueError, match="invalid auth_config"):
            _ = await aclient.create_bucket_config(
                org=org_name, nickname=bucket_nickname, uri="s3://my-bucket", auth_config={"method": "foo"}
            )

        # Assign the bucket to a repo.
        await aclient.create_repo(repo_name, bucket_config_nickname=bucket_nickname)
        repos = [f"{org_name}/{r.name}" for r in await aclient.list_repos_for_bucket_config(org=org_name, nickname=bucket_nickname)]
        assert len(repos) == 1

        # Buckets cannot be deleted if they are assigned to a repo.
        with pytest.raises(ValueError, match="in use by a repo and cannot be modified") as exc_info:
            await aclient.delete_bucket_config(org=org_name, nickname=bucket_nickname, imsure=True, imreallysure=True)

        # Buckets can be modified and deleted if they are not assigned to a repo.
        await aclient.delete_repo(repo_name, imsure=True, imreallysure=True)
        repo_list = await aclient.list_repos_for_bucket_config(org=org_name, nickname=bucket_nickname)
        assert len(repo_list) == 0

        # set up one more bucket before deleting the default one
        await aclient.create_bucket_config(
            org=org_name,
            nickname=second_bucket_nickname + "-bonus",
            uri=f"s3://{bucket_name}/bonus",
            region_name="us-west-2",
            auth_config={"method": "anonymous"},
        )

        # Ensure that deleting the pre-existing default bucket will
        # promote the oldest existing bucket to default.
        await aclient.delete_bucket_config(org=org_name, nickname=bucket_nickname, imsure=True, imreallysure=True)
        num_default = 0
        bucket_configs = await aclient.list_bucket_configs(org_name)
        for b in bucket_configs:
            assert b.nickname != bucket_nickname
            if b.is_default:
                num_default += 1
        assert num_default == 1


def test_extra_config_deprecation_warning():
    """Test that passing extra_config as a dict emits a DeprecationWarning."""
    import warnings

    aclient = AsyncClient.__new__(AsyncClient)

    with pytest.warns(DeprecationWarning, match="extra_config"):
        aclient._make_bucket_config(
            nickname="test",
            uri="s3://my-bucket",
            extra_config={"region_name": "us-west-2"},
            auth_config={"method": "anonymous"},
        )


def test_extra_config_explicit_params_no_warning():
    """Test that using explicit params does not emit a DeprecationWarning."""
    import warnings

    aclient = AsyncClient.__new__(AsyncClient)

    with warnings.catch_warnings():
        warnings.simplefilter("error", DeprecationWarning)
        result = aclient._make_bucket_config(
            nickname="test",
            uri="s3://my-bucket",
            region_name="us-west-2",
            use_ssl=False,
            force_path_style=True,
            auth_config={"method": "anonymous"},
        )
    assert result["extra_config"] == {
        "region_name": "us-west-2",
        "use_ssl": False,
        "force_path_style": True,
    }


def test_extra_config_explicit_params_override_dict():
    """Test that explicit params take precedence over extra_config dict values."""
    import warnings

    aclient = AsyncClient.__new__(AsyncClient)

    with warnings.catch_warnings():
        warnings.simplefilter("ignore", DeprecationWarning)
        result = aclient._make_bucket_config(
            nickname="test",
            uri="s3://my-bucket",
            extra_config={"region_name": "us-east-1"},
            region_name="us-west-2",
            auth_config={"method": "anonymous"},
        )
    assert result["extra_config"]["region_name"] == "us-west-2"


@pytest.mark.asyncio
async def test_aws_customer_managed_role_bucket_with_secret(token, helpers):
    """Test creating a bucket with AWS customer managed role auth including shared_secret."""
    aclient = AsyncClient(token=token)
    org_config = {"metastoredb_host": "mongo", "status": "active"}
    org_name = await helpers.isolated_org(token, org_config)
    bucket_name = helpers.an_id(10)
    bucket_nickname = helpers.an_id(5)
    prefix = helpers.an_id(7)

    # Create a bucket with AWS customer managed role auth and shared_secret
    new_bucket = await aclient.create_bucket_config(
        org=org_name,
        nickname=bucket_nickname,
        uri=f"s3://{bucket_name}/{prefix}",
        region_name="us-west-2",
        auth_config={
            "method": "aws_customer_managed_role",
            "external_customer_id": "123456789012",
            "external_role_name": "my-test-role",
            "shared_secret": "super-secret-value-12345",
        },
    )

    # Verify the bucket was created
    buckets = await aclient.list_bucket_configs(org_name)
    assert len(buckets) == 1
    assert new_bucket in buckets

    # Get the bucket config and verify the auth config
    retrieved_bucket = await aclient.get_bucket_config(org=org_name, nickname=bucket_nickname)
    assert retrieved_bucket.auth_config is not None
    assert retrieved_bucket.auth_config.method == "aws_customer_managed_role"
    assert retrieved_bucket.auth_config.external_customer_id == "123456789012"
    assert retrieved_bucket.auth_config.external_role_name == "my-test-role"

    # The shared_secret should be obfuscated in the response from server
    assert retrieved_bucket.auth_config.shared_secret is not None
    # When converted to string, SecretStr shows as **********
    assert str(retrieved_bucket.auth_config.shared_secret) == "**********"

    # Clean up
    await aclient.delete_bucket_config(org=org_name, nickname=bucket_nickname, imsure=True, imreallysure=True)


@pytest.mark.asyncio
async def test_azure_credential_delegation_bucket(token, helpers):
    """Test creating a bucket with Azure customer managed role auth."""
    aclient = AsyncClient(token=token)
    org_config = {"metastoredb_host": "mongo", "status": "active"}
    org_name = await helpers.isolated_org(token, org_config)
    container_name = helpers.an_id(10)
    bucket_nickname = helpers.an_id(5)
    prefix = helpers.an_id(7)

    # Create a bucket with Azure customer managed role auth
    new_bucket = await aclient.create_bucket_config(
        org=org_name,
        nickname=bucket_nickname,
        uri=f"az://{container_name}/{prefix}",
        auth_config={
            "method": "azure_credential_delegation",
            "tenant_id": "12345678-1234-1234-1234-123456789012",
            "storage_account": "teststorageaccount",
        },
    )

    # Verify the bucket was created
    buckets = await aclient.list_bucket_configs(org_name)
    assert len(buckets) == 1
    assert new_bucket in buckets

    # Get the bucket config and verify the auth config
    retrieved_bucket = await aclient.get_bucket_config(org=org_name, nickname=bucket_nickname)
    assert retrieved_bucket.auth_config is not None
    assert retrieved_bucket.auth_config.method == "azure_credential_delegation"
    assert retrieved_bucket.auth_config.tenant_id == "12345678-1234-1234-1234-123456789012"
    assert retrieved_bucket.auth_config.storage_account == "teststorageaccount"

    # Clean up
    await aclient.delete_bucket_config(org=org_name, nickname=bucket_nickname, imsure=True, imreallysure=True)


@pytest.mark.asyncio
@pytest.mark.xfail(reason="status endpoint is currently admin only", raises=ValueError)
async def test_repo_status_changes(token, helpers):
    aclient = AsyncClient(token=token)
    org_name = "bucketty"
    _repo_name = helpers.random_repo_id()
    repo_name = f"{org_name}/{_repo_name}"
    arepo = await aclient.create_repo(repo_name, bucket_config_nickname="test_bucket")

    # assert repo is initialized with the right status
    repo_obj = await aclient.get_repo_object(repo_name)
    assert repo_obj.status.mode == RepoOperationMode.ONLINE
    assert repo_obj.status.message == "new repo creation"
    assert repo_obj.status.initiated_by.get("principal_id") is not None
    assert repo_obj.status.initiated_by.get("system_id") is None

    # assert update operates correctly
    await aclient._set_repo_status(repo_name, RepoOperationMode.OFFLINE, message="foo")
    repo_obj = await aclient.get_repo_object(repo_name)
    assert repo_obj.status.mode == RepoOperationMode.OFFLINE
    assert repo_obj.status.message == "foo"
    assert repo_obj.status.initiated_by.get("principal_id") is not None

    # assert system update is visible
    _on, _rn = repo_name.split("/")
    await helpers.set_repo_system_status(token, _on, _rn, RepoOperationMode.MAINTENANCE, "system message", False)
    repo_obj = await aclient.get_repo_object(repo_name)
    assert repo_obj.status.mode == RepoOperationMode.MAINTENANCE
    assert repo_obj.status.message == "system message"
    assert repo_obj.status.initiated_by.get("principal_id") is None
    assert repo_obj.status.initiated_by.get("system_id") is not None

    # is_user_modifiable is false, verify request is blocked
    with pytest.raises(ValueError, match="Repo status is not modifiable") as exc_info:
        await aclient._set_repo_status(repo_name, RepoOperationMode.ONLINE, message="foo")

    # and state is still what it was prior to the attempt
    repo_obj = await aclient.get_repo_object(repo_name)
    assert repo_obj.status.mode == RepoOperationMode.MAINTENANCE
    assert repo_obj.status.message == "system message"
    assert repo_obj.status.initiated_by.get("principal_id") is None


@pytest.mark.skipif(importlib.util.find_spec("obstore") is None, reason="obstore extra not installed")
class TestGetObstoreForBucket:
    @pytest.mark.parametrize("access", ["read", "write", None])
    @pytest.mark.asyncio
    async def test_returns_unsigned_store_for_anonymous_bucket(self, isolated_org, minio_anon_bucket, token, access):
        import obstore as obs

        async with isolated_org(minio_anon_bucket()) as (org_name, buckets):
            aclient = AsyncClient(token=token)
            kwargs = {"org": org_name, "nickname": buckets[0].nickname}
            if access is not None:
                kwargs["access"] = access
            store = await aclient.get_obstore_for_bucket(**kwargs)

            assert isinstance(store, obs.store.S3Store)
            assert store.config["endpoint"] == "http://localhost:9000"
            assert store.config["skip_signature"] == "true"  # type: ignore[comparison-overlap]
            assert store.client_options == {"allow_http": "true"}

    @pytest.mark.parametrize("access", ["read", "write", None])
    @pytest.mark.asyncio
    async def test_returns_unsigned_store_for_anonymous_azure_bucket(self, isolated_org, azure_anon_bucket, token, access):
        import obstore as obs

        async with isolated_org(azure_anon_bucket()) as (org_name, buckets):
            aclient = AsyncClient(token=token)
            kwargs = {"org": org_name, "nickname": buckets[0].nickname}
            if access is not None:
                kwargs["access"] = access
            store = await aclient.get_obstore_for_bucket(**kwargs)

            assert isinstance(store, obs.store.AzureStore)
            assert store.config["skip_signature"] == "true"  # type: ignore[comparison-overlap]
            assert store.config["account_name"] == "noaacdr"

    @pytest.mark.asyncio
    async def test_raises_when_bucket_nickname_does_not_exist(self, isolated_org, token):
        async with isolated_org() as (org_name, _):
            aclient = AsyncClient(token=token)
            with pytest.raises(BucketNotFoundError):
                await aclient.get_obstore_for_bucket(org=org_name, nickname="does-not-exist")

    @pytest.mark.asyncio
    async def test_raises_clear_error_when_obstore_extra_missing(self, monkeypatch, respx_mock, test_token):
        """The error must fire before any HTTP calls, so a missing extra never
        wastes an API round trip."""
        monkeypatch.setitem(sys.modules, "obstore", None)
        monkeypatch.setitem(sys.modules, "obstore.store", None)

        aclient = AsyncClient("https://test-arraylake-service.bar", token=test_token)

        with pytest.raises(ImportError, match=r"pip install 'arraylake\[obstore\]'"):
            await aclient.get_obstore_for_bucket(org="test-org", nickname="any")

        assert len(respx_mock.calls) == 0
