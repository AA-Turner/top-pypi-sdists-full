from uuid import uuid4

import pytest

from arraylake.types import BucketResponse, GSCredentials, S3Credentials


@pytest.fixture
def s3_bucket_config() -> BucketResponse:
    return BucketResponse(
        id=uuid4(),
        platform="s3",
        nickname="test-s3-bucket-nickname",
        name="s3-test",
        is_default=False,
        extra_config={
            "use_ssl": True,
            "endpoint_url": "http://foo.com",
            "region_name": "us-west-1",
        },
    )


@pytest.fixture
def s3_credentials() -> S3Credentials:
    return S3Credentials(
        aws_access_key_id="aws_access_key_id",
        aws_secret_access_key="aws_secret_access_key",
        aws_session_token="aws_session_token",
        expiration=None,
    )


@pytest.fixture
def tigris_bucket_config() -> BucketResponse:
    return BucketResponse(
        id=uuid4(),
        platform="s3-compatible",
        nickname="test-tigris-bucket-nickname",
        name="tigris-test",
        is_default=False,
        extra_config={
            "use_ssl": False,
            "endpoint_url": "https://t3.storage.dev",
            "region_name": "iad",
        },
    )


@pytest.fixture
def gs_credentials() -> GSCredentials:
    return GSCredentials(
        access_token="access_token",
        principal="principal",
        expiration=None,
    )


def refresh_func():
    return None


@pytest.fixture
def credential_refresh_func():
    return refresh_func


@pytest.fixture
def gcs_bucket_config() -> BucketResponse:
    return BucketResponse(
        id=uuid4(),
        platform="gs",
        nickname="test-gcs-bucket-nickname",
        name="gcs-test",
        is_default=False,
        extra_config={},
    )


@pytest.fixture
def anon_minio_bucket_config() -> BucketResponse:
    return BucketResponse(
        id=uuid4(),
        platform="minio",
        nickname="test-minio-anon",
        name="anonbucket",
        auth_config={"method": "anonymous"},
        is_default=False,
        extra_config={
            "use_ssl": False,
            "endpoint_url": "http://localhost:9000",
        },
    )
