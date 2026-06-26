import json
import os
import pathlib
import random
import secrets
import shutil
import string
import time
from collections.abc import AsyncGenerator, Iterable
from contextlib import asynccontextmanager
from pathlib import Path
from typing import Literal
from unittest import mock
from uuid import UUID, uuid4
import asyncio
import httpx

import pytest
import yaml

from arraylake import AsyncClient, config
from arraylake._credential_cache import clear as clear_credential_cache
from arraylake.api_utils import ArraylakeHttpClient
from arraylake.token import TokenHandler
from arraylake.types import (
    ApiTokenInfo,
    Author,
    AuthProviderConfig,
    BucketPrefix,
    BucketNickname,
    BucketName,
    BucketResponse,
    NewBucket,
    NewRepoOperationStatus,
    OauthTokens,
    OrgName,
    RepoOperationMode,
    UserInfo,
)


@pytest.fixture(autouse=True)
def reset_credential_cache():
    """The delegated-credential cache is process-wide module state; reset it around every
    test so cached credentials never leak between tests."""
    clear_credential_cache()
    yield
    clear_credential_cache()


# Configured not to run slow tests by default
# https://stackoverflow.com/questions/52246154/python-using-pytest-to-skip-test-unless-specified
def pytest_configure(config):
    config.addinivalue_line("markers", "runslow: run slow tests")


def pytest_addoption(parser):
    parser.addoption("--runslow", action="store_true", default=False, help="run slow tests")


def pytest_collection_modifyitems(config, items):
    if config.getoption("--runslow"):
        # --runslow given in cli: do not skip slow tests
        return
    skip_slow = pytest.mark.skip(reason="need --runslow option to run")
    for item in items:
        if "slow" in item.keywords:
            item.add_marker(skip_slow)


@pytest.fixture()
def temp_config_file(tmp_path):
    template_file = pathlib.Path(__file__).resolve().parent / "config.yaml"
    test_file = tmp_path / "config.yaml"
    shutil.copy(template_file, test_file)
    return test_file


@pytest.fixture(autouse=True)
def clean_config():
    template_file = pathlib.Path(__file__).resolve().parent / "config.yaml"
    with template_file.open() as f:
        c = yaml.safe_load(f)
    config.update(c)


@pytest.fixture(scope="function", autouse=True)  # perhaps autouse is too aggressive here?
def test_token_file(tmp_path):
    contents = {
        "access_token": "access-123",
        "id_token": "id-456",
        "refresh_token": "refresh-789",
        "expires_in": 86400,
        "token_type": "Bearer",
    }
    fname = tmp_path / "token.json"

    with fname.open(mode="w") as f:
        json.dump(contents, f)

    with config.set({"service.token_path": str(fname)}):
        yield fname


@pytest.fixture(scope="function")
def test_user():
    return UserInfo(
        id=uuid4(),
        sub=UUID("aeeb8bfa-e8f4-4724-9427-c3d5af66190e"),
        email="abc@earthmover.io",
        first_name="TestFirst",
        family_name="TestFamily",
    )


@pytest.fixture(scope="function")
def test_api_token():
    id = uuid4()
    email = "svc-email@some-earthmover-org.service.earthmover.io"
    return ApiTokenInfo(id=id, client_id=id.hex, email=email, expiration=int(time.time() + 10000))


@pytest.fixture()
def test_token():
    return "ema_token-123456789"


@pytest.fixture(
    params=["machine", "user"],
)
def token(request, test_token, test_token_file):
    if request.param == "machine":
        return test_token
    else:
        return None


def get_platforms_to_test(request):
    platforms = ("s3",)
    mark = request.node.get_closest_marker("add_object_store")
    if mark is not None:
        platforms += mark.args
    return platforms


@pytest.fixture(params=["s3", "gs"], scope="session")
def object_store_platform(request) -> Literal["s3", "gs"]:
    return request.param


@pytest.fixture(scope="session")
def object_store_config(object_store_platform):
    if object_store_platform == "s3":
        config_params = {
            "service.uri": "http://0.0.0.0:8000",
            "chunkstore.uri": "s3://testbucket",
            "s3.endpoint_url": "http://localhost:9000",
        }
    elif object_store_platform == "gs":
        config_params = {
            "service.uri": "http://0.0.0.0:8000",
            "chunkstore.uri": "gs://arraylake-test",
            "gs.endpoint_url": "http://127.0.0.1:4443",
            "gs.token": "anon",
            "gs.project": "test",
        }
    return config_params


@pytest.fixture
def client_config(object_store_platform, object_store_config, request):
    if object_store_platform not in get_platforms_to_test(request):
        pytest.skip()
    with config.set(object_store_config):
        yield


@pytest.fixture
def user():
    return Author(name="Test User", email="foo@icechunk.io")


@pytest.fixture(scope="session", autouse=True)
def aws_config():
    credentials_env = {
        "AWS_ACCESS_KEY_ID": "minio123",
        "AWS_SECRET_ACCESS_KEY": "minio123",
    }
    with mock.patch.dict(os.environ, credentials_env):
        yield


@pytest.fixture
async def org_name(client_config, test_token):
    # This fixture should be used by all client-level tests.
    # It makes things more resilient by making sure there are no repos
    # under the specified org and cleaning up any repos that might be left over.
    # But warning: if there are errors in the list / delete logic, they
    # will show up here first!
    org = "my-org"
    async_client = AsyncClient(token=test_token)
    for repo in await async_client.list_repos(org):
        await async_client.delete_repo(f"{org}/{repo.name}", imsure=True, imreallysure=True)
    yield org
    for repo in await async_client.list_repos(org):
        await async_client.delete_repo(f"{org}/{repo.name}", imsure=True, imreallysure=True)


@pytest.fixture
async def isolated_org_name(client_config, test_token):
    # This fixture should be used by all client-level tests.
    # It makes things more resilient by making sure there are no repos
    # under the specified org and cleaning up any repos that might be left over.
    # But warning: if there are errors in the list / delete logic, they
    # will show up here first!
    org_name = "".join(random.choices(string.ascii_uppercase + string.digits, k=8))
    body = {
        "name": org_name,
        "status": "active",
    }
    client = ArraylakeHttpClient("http://localhost:8000", token=test_token)
    resp = await client._request("POST", "/orgs_test_create", content=json.dumps(body))
    assert resp.is_success, f"Failed to create isolated org {org_name}: {resp.status_code} {resp.content}"
    yield org_name

    # TODO shouldn't this delete the org after?


# TODO this doesn't need to be a fixture, it's a pure function
@pytest.fixture
def default_bucket():
    def default_bucket_request_constructor(
        *,
        nickname="test_bucket",
        name="testbucket",
        prefix: BucketPrefix = None,
        platform="minio",
        extra_config={
            "use_ssl": False,
            "endpoint_url": "http://localhost:9000",
        },
        auth_config={"method": "hmac", "access_key_id": "minio123", "secret_access_key": "minio123"},
    ):
        new_bucket_obj = NewBucket(
            nickname=nickname,
            name=name,
            platform=platform,
            extra_config=extra_config,
            auth_config=auth_config,
        )

        if prefix:
            new_bucket_obj.prefix = "prefix"

        return new_bucket_obj

    return default_bucket_request_constructor


@pytest.fixture
def anon_bucket(default_bucket):
    return default_bucket(
        auth_config={"method": "anonymous"},
        nickname="anon_bucket",
        name="name",
        prefix="prefix",
        extra_config={"region_name": "us-west-2"},
    )


@pytest.fixture
def minio_anon_bucket(default_bucket):
    """Anonymous access bucket on local MinIO for testing virtual chunks."""

    def minio_anon_bucket_request_constructor(
        *,
        prefix: BucketPrefix = None,
    ):
        return default_bucket(
            auth_config={"method": "anonymous"},
            nickname="minio_anon_bucket",
            name="anonbucket",
            prefix=prefix,
            platform="minio",
            extra_config={
                "use_ssl": False,
                "endpoint_url": "http://localhost:9000",
            },
        )

    return minio_anon_bucket_request_constructor


@pytest.fixture
def azure_anon_bucket(default_bucket):
    """Anonymous (public) Azure container.

    Mirrors the public NOAA Sea Surface Temperature WHOI dataset that icechunk's
    anonymous-Azure test reads from (earth-mover/icechunk#2173). Azure needs the
    storage account name (the blob endpoint host) supplied via extra_config since
    anonymous buckets carry no delegated-credentials auth config.
    """

    def azure_anon_bucket_request_constructor(
        *,
        prefix: BucketPrefix = None,
    ):
        return default_bucket(
            auth_config={"method": "anonymous", "storage_account": "noaacdr"},
            nickname="azure_anon_bucket",
            name="sea-surface-temp-whoi",
            prefix=prefix,
            platform="azure",
            extra_config={},
        )

    return azure_anon_bucket_request_constructor


@pytest.fixture
def delegated_creds_bucket(default_bucket):
    def delegated_creds_bucket_request_constructor(
        *,
        name: BucketName = "testbucket",
        nickname: BucketNickname = "delegated_creds_bucket",
        prefix: BucketPrefix = None,
    ):
        return default_bucket(
            nickname=nickname,
            platform="s3",
            name=name,
            prefix=prefix,
            auth_config={
                "method": "aws_customer_managed_role",
                "external_customer_id": "12345678",
                "external_role_name": "my_external_role",
                "shared_secret": "our-shared-secret",
            },
            extra_config={"region_name": "us-west-2"},
        )

    return delegated_creds_bucket_request_constructor


@pytest.fixture
def isolated_org(test_token):
    """
    Create an isolated org with zero or more buckets.

    Deletes all the buckets after use.
    """

    @asynccontextmanager
    async def org_constructor(*bucket_requests: NewBucket) -> AsyncGenerator[tuple[OrgName, Iterable[NewBucket]], None, None]:
        # Generate a unique org name for each invocation
        org_name = "".join(random.choices(string.ascii_uppercase + string.digits, k=8))

        # Create the org
        client = ArraylakeHttpClient("http://localhost:8000", token=test_token)
        body = {
            "name": org_name,
            "status": "active",
        }
        resp = await client._request("POST", "/orgs_test_create", content=json.dumps(body))
        assert resp.is_success, f"Failed to create isolated org {org_name}: {resp.status_code} {resp.content}"

        bucket_responses = []

        try:
            for new_bucket_obj in bucket_requests:
                # we cannot use async_client.create_bucket_config because it does not support minio as a platform
                resp = await client._request(
                    "POST", f"/orgs/{org_name}/buckets", content=new_bucket_obj.model_dump_json(context={"reveal_secrets": True})
                )
                assert resp.is_success, f"Failed to create bucket in isolated org {org_name}: {resp.status_code} {resp.content}"
                bucket_responses.append(resp)

            yield org_name, bucket_requests

        finally:
            # delete all the buckets even if something else went wrong
            for resp in bucket_responses:
                try:
                    bucket_id = BucketResponse.model_validate_json(resp.content).id
                    await client._request("DELETE", f"/orgs/{org_name}/buckets/{bucket_id}")
                except Exception as e:
                    print(f"Error deleting bucket {resp.content['id']} in org {org_name}: {e}")

    return org_constructor


@pytest.fixture
def two_isolated_orgs(isolated_org):
    @asynccontextmanager
    async def orgs_constructor(
        bucket_requests_org1: Iterable[NewBucket] = (),
        bucket_requests_org2: Iterable[NewBucket] = (),
    ) -> AsyncGenerator[tuple[tuple[OrgName, Iterable[NewBucket]], tuple[OrgName, Iterable[NewBucket]]], None, None]:
        async with isolated_org(*bucket_requests_org1) as (org1_name, buckets1):
            async with isolated_org(*bucket_requests_org2) as (org2_name, buckets2):
                yield (org1_name, buckets1), (org2_name, buckets2)

    return orgs_constructor


@pytest.fixture
def new_bucket_obj(
    nickname="test_bucket",
    platform="minio",
    name="testbucket",
    extra_config={
        "use_ssl": False,
        "endpoint_url": "http://localhost:9000",
    },
    auth_config={"method": "hmac", "access_key_id": "minio123", "secret_access_key": "minio123"},
):
    return NewBucket(
        org=isolated_org_name,
        nickname=nickname,
        platform=platform,
        name=name,
        extra_config=extra_config,
        auth_config=auth_config,
    )


@pytest.fixture
def new_bucket_obj_with_prefix(new_bucket_obj):
    new_bucket_obj.prefix = "prefix"
    return new_bucket_obj


class Helpers:
    """Helper functions for tests.

    This class is made available to tests using the helpers fixture.
    """

    @staticmethod
    def random_repo_id() -> str:
        return secrets.token_hex(12)  # Generates a 24-character hex string like ObjectId

    @staticmethod
    def an_id(n: int) -> str:
        return "".join(random.choices(string.hexdigits, k=n))

    @staticmethod
    def oauth_tokens_from_file(file: Path) -> OauthTokens:
        """Utility to read an oauth tokens file"""
        with file.open() as f:
            return OauthTokens.model_validate_json(f.read())

    @staticmethod
    async def isolated_org(token, org_config):
        org_name = "".join(random.choices(string.ascii_uppercase + string.digits, k=8))
        org_config["name"] = org_name
        client = ArraylakeHttpClient("http://localhost:8000", token=token)
        resp = await client._request("POST", "/orgs_test_create", content=json.dumps(org_config))
        return org_name

    @staticmethod
    async def set_repo_system_status(token, org_name, repo_name, mode: RepoOperationMode, message: str, is_user_modifiable: bool):
        """Util to set a system status for client tests.

        System statuses and the user modifiable status are not available in the public API.
        """
        client = ArraylakeHttpClient("http://localhost:8000", token=token)
        body = dict(NewRepoOperationStatus(mode=mode, message=message))
        resp = await client._request(
            "POST",
            f"/repo_status_system/{org_name}/{repo_name}",
            content=json.dumps(body),
            params={"is_user_modifiable": is_user_modifiable},
        )


@pytest.fixture(scope="session")
def helpers():
    """Provide the helpers found in the Helpers class"""
    return Helpers


@pytest.fixture
def mock_auth_provider_config():
    mock_config = AuthProviderConfig(client_id="123456789", domain="auth.foo.com")

    with mock.patch.object(TokenHandler, "auth_provider_config", return_value=mock_config, new_callable=mock.PropertyMock):
        yield mock_config


@pytest.fixture
def sync_isolated_org_with_bucket(isolated_org_name, default_bucket, test_token):
    """Sync fixture that creates an org with a bucket for CLI tests."""

    def create_org_with_bucket():
        import asyncio

        async def _create():
            # Create the bucket config
            bucket_config = default_bucket()

            # Use the async isolated_org fixture logic
            client = ArraylakeHttpClient("http://localhost:8000", token=test_token)

            # Create the bucket
            resp = await client._request(
                "POST", f"/orgs/{isolated_org_name}/buckets", content=bucket_config.model_dump_json(context={"reveal_secrets": True})
            )
            bucket_response = BucketResponse.model_validate_json(resp.content)

            return isolated_org_name, bucket_response.id

        # Run the async function synchronously
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            org_name, bucket_id = loop.run_until_complete(_create())
            return org_name, bucket_id
        finally:
            loop.close()

    return create_org_with_bucket


@pytest.fixture(scope="function")
def api_call_counter():
    """
    Fixture for counting HTTP requests at any point in a test.

    Uses monkeypatching on httpx.AsyncHTTPTransport.handle_async_request to track calls.
    Requests pass through to the real service.

    Returns a function that accepts an optional latency_ms parameter (default: 100ms).

    Usage:
        @pytest.mark.asyncio
        async def test_get_repo_call_count(api_call_counter, isolated_org, default_bucket, token):
            async with isolated_org(default_bucket()) as (org_name, buckets):
                aclient = AsyncClient(token=token)

                # Setup (not counted)
                name = f"{org_name}/foo"
                await aclient.create_repo(name, bucket_config_nickname=buckets[0].nickname)

                # Count only get_repo calls with default 100ms latency
                async with api_call_counter() as counter:
                    repo = await aclient.get_repo(name)

                assert len(counter.tracked_calls) <= 3, counter.call_log()

                # Or with custom latency:
                async with api_call_counter(latency_ms=50) as counter:
                    repo = await aclient.get_repo(name)

                # Can also analyze sequential patterns
                sequential_chains = counter.count_sequential_calls()
    """

    def counter_factory(latency_ms: int = 100) -> CallCounter:
        return CallCounter(add_latency_ms=latency_ms)

    return counter_factory


class CallCounter:
    """Track HTTP requests made during a scope using httpx transport monkeypatch"""

    def __init__(self, add_latency_ms: int = 100):
        self.tracked_calls = []
        self._original_handle_async_request = None
        self.add_latency_ms = add_latency_ms

    async def __aenter__(self):
        """Enter async context manager and start tracking requests"""

        # Store the original method
        self._original_handle_async_request = httpx.AsyncHTTPTransport.handle_async_request

        # Create wrapped version that tracks calls
        async def tracked_handle_async_request(transport_self, request: httpx.Request) -> httpx.Response:
            start_time = time.perf_counter()
            response = await self._original_handle_async_request(transport_self, request)

            # Add artificial latency if configured
            if self.add_latency_ms > 0:
                await asyncio.sleep(self.add_latency_ms / 1000.0)

            end_time = time.perf_counter()

            # Track the request and response with timing
            self.tracked_calls.append(
                {
                    "request": request,
                    "response": response,
                    "method": request.method,
                    "url": str(request.url),
                    "start_time": start_time,
                    "end_time": end_time,
                    "duration_ms": (end_time - start_time) * 1000,
                }
            )
            return response

        # Monkeypatch the transport method
        httpx.AsyncHTTPTransport.handle_async_request = tracked_handle_async_request
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Exit async context manager and restore original method"""

        # Restore the original method
        if self._original_handle_async_request is not None:
            httpx.AsyncHTTPTransport.handle_async_request = self._original_handle_async_request
        return False

    def call_log(self) -> str:
        """Return a formatted string of all tracked calls for debugging."""
        lines = [f"\n=== HTTP Requests ({len(self.tracked_calls)} total) ==="]
        for i, call in enumerate(self.tracked_calls, 1):
            duration = call.get("duration_ms", 0)
            lines.append(f"  {i}. {call['method']} {call['url']} ({duration:.2f}ms)")
        return "\n".join(lines)

    def count_sequential_calls(self, overlap_threshold_ms: float = 10.0) -> int:
        """
        Calculate the number of sequential call chains based on timing.

        A new sequential chain starts when a call begins after the previous call
        has ended (with some overlap tolerance).

        Args:
            overlap_threshold_ms: Maximum overlap in milliseconds to consider calls as sequential.
            Default 10ms accounts for timing precision and context switching overhead.

        Returns:
            Number of sequential call chains detected.

        Example:
            If 3 calls are made and all are sequential:
                call1: [0-100ms]
                call2: [100-200ms]
                call3: [200-300ms]
            Returns 3

            If 2 calls overlap significantly (concurrent):
                call1: [0-200ms]
                call2: [50-150ms]
            Returns 1 (counted as part of same chain)
        """
        if not self.tracked_calls:
            return 0

        if len(self.tracked_calls) == 1:
            return 1

        sequential_chains = 1
        overlap_threshold = overlap_threshold_ms / 1000.0

        for i in range(1, len(self.tracked_calls)):
            current_call = self.tracked_calls[i]
            prev_call = self.tracked_calls[i - 1]

            current_start = current_call["start_time"]
            prev_end = prev_call["end_time"]

            # If current call starts after previous call ends (with tolerance),
            # it's assumed to be a new sequential chain
            if current_start > prev_end + overlap_threshold:
                sequential_chains += 1

        return sequential_chains
