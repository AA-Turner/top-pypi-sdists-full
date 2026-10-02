from arraylake.config import config
from arraylake.types import BucketResponse, HmacAuth, S3Credentials


def _is_r2_bucket(bucket: BucketResponse | None) -> bool:
    """Check if the bucket is an R2 bucket."""
    if not isinstance(bucket, BucketResponse) or bucket.platform != "s3-compatible":
        return False

    endpoint_url = bucket.extra_config.get("endpoint_url")
    if endpoint_url is not None and isinstance(endpoint_url, str) and ".r2." in endpoint_url:
        return True
    return False


def _use_delegated_credentials(bucket: BucketResponse | None) -> bool:
    """Check if the bucket is using delegated credentials."""
    if (
        isinstance(bucket, BucketResponse)
        and bucket.auth_config
        and bucket.auth_config.method
        in (
            "customer_managed_role",
            "aws_customer_managed_role",
            "gcp_customer_managed_role",
            "r2_customer_managed_role",
            "azure_credential_delegation",
        )
        and (bucket.platform in ("s3", "gs", "azure") or _is_r2_bucket(bucket))
        and config.get("chunkstore.use_delegated_credentials", True)
    ):
        return True
    return False


def _use_hmac_credentials(bucket: BucketResponse | None) -> bool:
    """Check if the bucket is using HMAC credentials."""
    if isinstance(bucket, BucketResponse) and isinstance(bucket.auth_config, HmacAuth) and bucket.platform != "gs":
        return True
    return False


def _use_anonymous_credentials(bucket: BucketResponse | None) -> bool:
    """Check if the bucket is using anonymous credentials."""
    if isinstance(bucket, BucketResponse) and bucket.auth_config and bucket.auth_config.method == "anonymous":
        return True
    return False


async def _get_hmac_credentials(bucket: BucketResponse) -> S3Credentials:
    """Get HMAC credentials for a object store bucket.

    Args:
        bucket: BucketResponse object containing the bucket nickname.

    Returns:
        S3Credentials: HMAC credentials for the S3 bucket.
    """
    # We must check these again or else mypy freaks out
    assert isinstance(bucket, BucketResponse)
    assert isinstance(bucket.auth_config, HmacAuth)
    return S3Credentials(
        aws_access_key_id=bucket.auth_config.access_key_id,
        aws_secret_access_key=bucket.auth_config.secret_access_key,
        aws_session_token=None,
        expiration=None,
    )
