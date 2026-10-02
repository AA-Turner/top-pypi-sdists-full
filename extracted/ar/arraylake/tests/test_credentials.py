from uuid import uuid4

import pytest

from arraylake.credentials import _is_r2_bucket
from arraylake.types import BucketResponse


@pytest.fixture
def s3_bucket_config() -> BucketResponse:
    """Fixture for a standard S3 bucket configuration."""
    return BucketResponse(
        id=uuid4(),
        name="s3-bucket",
        nickname="s3-bucket",
        platform="s3",
        extra_config={"endpoint_url": "https://s3.amazonaws.com"},
        is_default=False,
    )


@pytest.fixture
def r2_bucket_config() -> BucketResponse:
    """Fixture for a Cloudflare R2 bucket configuration."""
    return BucketResponse(
        id=uuid4(),
        name="r2-bucket",
        nickname="r2-bucket",
        platform="s3-compatible",
        extra_config={"endpoint_url": "https://123456.r2.cloudflarestorage.com"},
        is_default=False,
    )


def test_is_r2_bucket(s3_bucket_config: BucketResponse, r2_bucket_config: BucketResponse):
    """Test the _is_r2_bucket function."""
    assert not _is_r2_bucket(s3_bucket_config)
    assert _is_r2_bucket(r2_bucket_config)

    # Test with a bucket that has no endpoint_url
    no_endpoint_bucket = BucketResponse(
        id=uuid4(),
        name="no-endpoint-bucket",
        nickname="no-endpoint-bucket",
        platform="s3-compatible",
        extra_config={},
        is_default=False,
    )
    assert not _is_r2_bucket(no_endpoint_bucket)
