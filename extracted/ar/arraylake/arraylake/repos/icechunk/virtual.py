from collections.abc import Callable, Iterable, Mapping
from urllib.parse import urlparse

import icechunk

from arraylake.repos.icechunk.storage import create_icechunk_store_config
from arraylake.types import (
    ICECHUNK_ANY_CREDENTIAL,
    URI,
    UUID,
    BucketNickname,
    BucketPrefix,
    BucketResponse,
    GSCredentials,
    HmacAuth,
    S3Credentials,
)

FORBIDDEN_VIRTUAL_CHUNK_PREFIXES = {"file://", "memory://", "http://"}


def get_icechunk_container_credentials(
    bucket_platform: str,
    credentials: S3Credentials | GSCredentials | None,
    credential_refresh_func: Callable | None,
) -> ICECHUNK_ANY_CREDENTIAL:
    """Gets the icechunk virtual chunk container credentials
    from the given bucket config and credentials.

    Args:
        bucket_platform: The platform of the bucket. Supported platforms are "s3", "s3c", and "minio".
        credentials: Optional S3Credentials or GSCredentials to use for the virtual chunk container.
        credential_refresh_func (Callable[[], S3StaticCredentials | GcsBearerCredential]):
            Optional function to refresh S3 or GCS credentials. This function must
            be synchronous, cannot take in any args, and return a
            icechunk.S3StaticCredentials or icechunk.GcsBearerCredential object.

    Returns:
        icechunk.Credentials.S3 or icechunk.Credentials.Gcs:
            The virtual chunk container credentials for the bucket.
    """
    if credential_refresh_func and credentials:
        raise ValueError("Cannot provide both static credentials and a credential refresh function.")

    # Check the if the bucket is an S3 or S3-compatible bucket
    if bucket_platform in ("s3", "s3c", "s3-compatible", "minio"):
        if credential_refresh_func:
            return icechunk.s3_refreshable_credentials(credential_refresh_func)
        elif credentials:
            assert isinstance(credentials, S3Credentials)
            return icechunk.s3_static_credentials(
                access_key_id=credentials.aws_access_key_id,
                secret_access_key=credentials.aws_secret_access_key,
                session_token=credentials.aws_session_token,
                expires_after=credentials.expiration,
            )
        else:
            return icechunk.S3Credentials.Anonymous()
    elif bucket_platform in ("gs"):
        if credential_refresh_func:
            return icechunk.gcs_refreshable_credentials(credential_refresh_func)
        elif credentials:
            assert isinstance(credentials, GSCredentials)
            return icechunk.GcsCredentials.Static(icechunk.GcsStaticCredentials.BearerToken(credentials.access_token))
        else:
            return icechunk.GcsCredentials.Anonymous()
    else:
        raise ValueError(f"Unsupported bucket platform for virtual chunk container credentials: {bucket_platform}")


def create_virtual_chunk_container(
    bucket_config: BucketResponse,
    *,
    prefix: BucketPrefix | None = None,
    user_id: UUID,
) -> icechunk.VirtualChunkContainer:
    """
    Infer what Icechunk virtual chunk container would be needed to access data in this bucket.

    Optionally specify a prefix within that bucket - only data within that prefix will be accessible.
    If an explicit prefix is not provided, the default prefix for that bucket configuration will be used.

    Args:
        bucket_config: Bucket configuration object.
        prefix: The URL prefix within the bucket to authorize access to.
            Must be equal to or more specific than the prefix of the bucket config.
        user_id:
            user_id: The arraylake user ID of the principal that will be accessing the storage object.

    Returns:
        Icechunk virtual chunk container needed to access data in this bucket prefix.
    """

    forbid_unsafe_virtual_bucket_configs(bucket=bucket_config, bucket_nickname=bucket_config.nickname)

    # derive the store config based on the platform etc.
    store_config = create_icechunk_store_config(
        bucket_config,
        user_id=user_id,
    )

    # handle passing prefixes that are more specific than the same prefix stored in the bucket config
    full_prefix = validate_prefix_for_virtual_chunks(bucket=bucket_config, given_url=prefix)

    container = icechunk.VirtualChunkContainer(
        url_prefix=full_prefix,
        store=store_config,
    )

    return container


def validate_prefix_for_virtual_chunks(bucket: BucketResponse, given_url: URI | None) -> URI:
    """
    Validate that the user-supplied bucket prefix to use for virtual chunk access is compatible with the config for this bucket.
    """

    if given_url is None:
        raise ValueError("You must provide a bucket url for virtual chunks explicitly")
    elif not isinstance(given_url, str):
        raise ValueError(f"Provided prefix must be a valid string url, but got type {type(given_url)}")
    else:
        # TODO refactor all this validation to use a `CloudPath` class?

        # TODO also better handled by a `CloudPath` class
        if not given_url.endswith("/"):
            given_url = given_url + "/"

        actual_platform, actual_bucket, actual_prefix, *_ = urlparse(bucket.url)
        given_platform, given_bucket, given_prefix, *_ = urlparse(given_url)

        forbid_unsafe_virtual_chunk_containers([given_url])

        if not (given_platform and given_bucket):
            raise ValueError(f"Provided bucket prefix must be a complete url. However provided url is '{given_url}'")

        buckets_match = (given_platform == actual_platform) and (given_bucket == actual_bucket)
        if not buckets_match:
            raise ValueError(
                "Provided bucket url must be consistent with bucket config. "
                f"However provided url is '{given_url}' whereas bucket in bucket config '{bucket.nickname}' is '{bucket.url}'"
            )

        if not given_prefix.startswith(actual_prefix):
            raise ValueError(
                "Provided prefix must be consistent with prefix in bucket config. "
                f"However provided url is '{given_url}', which is not a prefix within '{bucket.url}'"
            )

        return given_url


def forbid_unsafe_virtual_bucket_configs(bucket: BucketResponse, bucket_nickname: BucketNickname) -> None:
    """
    Raises if bucket config for location of virtual chunks is somehow unsafe.
    """
    auth_method = bucket.auth_config

    # exclude HMAC buckets specifically as these will never be safe
    if isinstance(auth_method, HmacAuth):
        raise ValueError(
            "Cannot use virtual chunk references that refer to a bucket which uses HMAC credentials, "
            f"But bucket {bucket_nickname} uses HMAC credentials."
        )


def forbid_unsafe_virtual_chunk_containers(
    container_prefixes: Iterable[BucketPrefix],
) -> None:
    """
    Raises if any virtual chunk container prefix is somehow unsafe.
    """
    for url_prefix in container_prefixes:
        if any(url_prefix.startswith(forbidden_prefix) for forbidden_prefix in FORBIDDEN_VIRTUAL_CHUNK_PREFIXES):
            raise ValueError(
                f"Forbidden virtual chunk container url_prefix: {url_prefix}. "
                f"The virtual chunk container url_prefixes {FORBIDDEN_VIRTUAL_CHUNK_PREFIXES} are forbidden for use in Arraylake for security reasons."
            )


def reject_unresolvable_vccs(
    fetched_vccs: Mapping[BucketPrefix, BucketNickname | None],
) -> dict[BucketPrefix, BucketNickname]:
    """
    Validate that all fetched VCCs have resolvable bucket config nicknames.

    Raises ValueError if any VCC has a None nickname, meaning the server could not
    resolve it to a bucket config. This can happen when a VCC refers to a bucket config
    that has since been deleted from the organization.

    Returns the same mapping with None values excluded from the type.
    """
    unresolvable = [prefix for prefix, nickname in fetched_vccs.items() if nickname is None]
    if unresolvable:
        raise ValueError(
            f"The following virtual chunk container prefixes are unresolvable "
            f"(no matching bucket config found on the server): {unresolvable}"
        )
    return {prefix: nickname for prefix, nickname in fetched_vccs.items() if nickname is not None}


def match_virtual_chunk_container_prefixes_to_bucket_configs(
    virtual_chunk_container_prefixes: Iterable[BucketPrefix],
    pre_authorized_buckets: Iterable[BucketResponse],
) -> Mapping[BucketPrefix, BucketNickname]:
    """
    Find bucket configs matching virtual chunk container prefixes.

    Args:
        virtual_chunk_container_prefixes: Iterable of virtual chunk container prefixes.
            Prefixes for which to find matching bucket configs.
        pre_authorized_buckets: Iterable of bucket config nicknames.
            These bucket configs are assumed to be "pre-authorized" to access.

    Returns:
        List of bucket config nicknames which are potentially storing virtual chunks that are potentially permitted to be referred to by this repo.
    """

    # Even though we won't fetch creds in this method, better to raise early in the case of unsafe containers
    forbid_unsafe_virtual_chunk_containers(container_prefixes=list(virtual_chunk_container_prefixes))

    # match VCCs to bucket configs by prefix
    virtual_bucket_prefixes_to_configs: dict[BucketPrefix, BucketNickname] = {}
    for vcc_url_prefix in virtual_chunk_container_prefixes:
        # TODO probably need more advanced string matching logic here for cases of partial matches
        matching_buckets = [bucket for bucket in pre_authorized_buckets if bucket.url == vcc_url_prefix]

        if len(matching_buckets) == 1:
            virtual_bucket_prefixes_to_configs[vcc_url_prefix] = matching_buckets[0].nickname
        elif len(matching_buckets) == 0:
            # TODO throw a warning here? It implies the repo contains virtual chunks to which repo writer has not authorized access
            pass
        else:
            # TODO can this happen? what should we do here?
            raise ValueError

    return virtual_bucket_prefixes_to_configs
