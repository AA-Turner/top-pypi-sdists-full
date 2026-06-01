"""
Note: There is considerable code duplication between `_get_icechunk_storage_obj` and `create_icechunk_store_config`.
Until this is fixed any changes to one function likely mean the other function should be updated in a similar way.
It's not trivial to de-duplicate as a lot of the complexity comes from IC's inconsistent classes,
or just inherent complexity of not-quite equivalent cloud provider APIs.
"""

from __future__ import annotations

from collections.abc import Callable
from datetime import UTC
from enum import Enum
from uuid import UUID

import icechunk

from arraylake.log_util import get_logger
from arraylake.types import (
    AzureCredentials,
    AzureDelegatedCredentialsAuth,
    BucketResponse,
    GSCredentials,
    S3Credentials,
    StorageOptions,
    TempCredentials,
)

logger = get_logger(__name__)


ICECHUNK_REQUIRED_ENV_VARS = ["AWS_ACCESS_KEY_ID", "AWS_SECRET_ACCESS_KEY"]


class CredentialType(Enum):
    ANONYMOUS = "anonymous"
    PROVIDED = "provided"


def _get_credential_type(
    credentials: TempCredentials | icechunk.AnyCredential | None, credential_refresh_func: Callable | None
) -> CredentialType:
    """Determines the credential type based on the given credentials and refresh function.

    Args:
        credentials: Optional S3Credentials or GSCredentials for data access
        credential_refresh_func:
            Optional function to refresh S3 credentials.

    Returns:
        CredentialType enum
    """
    if credentials is not None or credential_refresh_func is not None:
        return CredentialType.PROVIDED
    else:
        return CredentialType.ANONYMOUS


def _get_icechunk_storage_obj(
    bucket_config: BucketResponse,
    prefix: str | None,
    credential_type: CredentialType,
    credentials: TempCredentials | icechunk.AnyCredential | None,
    credential_refresh_func: Callable | None,
    scatter_initial_credentials: bool,
    arraylake_version: str,
    user_id: UUID,
    storage_options: StorageOptions | None = None,
) -> icechunk.Storage:
    """Gets the Icechunk storage object.

    Gets the Icechunk storage object from the arraylake repo and bucket configuration.

    arraylake_version and user_id are currently used for logging to GCS, but may be used for other purposes in the future.

    Args:
        bucket_config: BucketResponse object containing the bucket nickname
        prefix: Prefix to use in the Icechunk storage config.
        credential_type: The type of credentials to use for the storage config
        credentials: Optional S3Credentials or GSCredentials for data access
        credential_refresh_func:
            Optional function to refresh credentials. This function must
            be synchronous, cannot take in any args, and return a
            icechunk.S3StaticCredentials or icechunk.GcsBearerCredential object.
        scatter_initial_credentials:
            Whether to immediately call and store the value returned by get_credentials.
            Ensures that the same set of credentials are available for all workers in a
            distributed setup.
        arraylake_version: The version of Arraylake being used, used for logging purposes.
        user_id: The arraylake user ID of the prinicpal that will be accessing the storage object
        storage_options: Optional storage options to pass to the Icechunk storage creation functions.
            Currently supports `network_stream_timeout_seconds` for S3, Tigris, and R2 storage.

    Returns:
        Icechunk Storage object
    """
    logger.debug(f"Using bucket {bucket_config.name} and prefix {prefix} for Icechunk storage config")

    # Extract storage options
    network_stream_timeout_seconds = storage_options.get("network_stream_timeout_seconds") if storage_options else None

    # Check the if the bucket is an S3 or S3-compatible bucket
    if bucket_config.platform in ("s3", "s3c", "s3-compatible", "minio"):
        if credentials and credential_refresh_func:
            raise ValueError("Cannot provide both static credentials and a credential refresh function.")
        if credentials and not isinstance(credentials, S3Credentials):
            raise ValueError(f"Invalid credentials provided for S3 bucket: {credentials}.")
        assert credentials is None or isinstance(credentials, S3Credentials)
        # Extract the endpoint URL from the bucket config, if it exists
        endpoint_url = bucket_config.extra_config.get("endpoint_url")
        if endpoint_url is not None:
            endpoint_url = str(endpoint_url)  # mypy thinks the endpoint_url could be a bool
        region = bucket_config.extra_config.get("region_name")
        if region is not None:
            region = str(region)  # mypy thinks the region could be a bool
        # Extract the use_ssl flag from the bucket config, if it exists
        use_ssl = bucket_config.extra_config.get("use_ssl", True)
        # Default the force_path_style to True for allow_http and False otherwise
        force_path_style_raw = bucket_config.extra_config.get("force_path_style", False if use_ssl else True)
        force_path_style = bool(force_path_style_raw)
        # Use tigris_storage to create the storage object for tigris buckets
        if endpoint_url and ("fly.storage.tigris.dev" in endpoint_url or "t3.storage.dev" in endpoint_url):
            if region is None or region == "auto":
                raise ValueError(
                    f"Region cannot be {region} for Tigris buckets. "
                    f"A specific Tigris region must be set on the bucket: https://www.tigrisdata.com/docs/concepts/regions/"
                )
            tigris_kwargs: dict = dict(
                bucket=bucket_config.name,
                prefix=prefix,
                region=region,
                endpoint_url=endpoint_url,
                allow_http=not use_ssl,
                access_key_id=credentials.aws_access_key_id if credentials else None,
                secret_access_key=credentials.aws_secret_access_key if credentials else None,
                session_token=credentials.aws_session_token if credentials else None,
                expires_after=credentials.expiration.replace(tzinfo=UTC) if credentials and credentials.expiration else None,
                anonymous=credential_type == CredentialType.ANONYMOUS,
                from_env=False,
                get_credentials=credential_refresh_func,
                scatter_initial_credentials=scatter_initial_credentials,
            )
            if network_stream_timeout_seconds is not None:
                tigris_kwargs["network_stream_timeout_seconds"] = network_stream_timeout_seconds
            return icechunk.tigris_storage(**tigris_kwargs)
        # Use r2_storage to create the storage object for R2 buckets
        elif endpoint_url and ".r2." in endpoint_url:
            r2_kwargs: dict = dict(
                bucket=bucket_config.name,
                prefix=prefix,
                account_id=None,  # Endpoint url will always be provided for R2 buckets
                endpoint_url=endpoint_url,
                region=region,
                allow_http=not use_ssl,
                access_key_id=credentials.aws_access_key_id if credentials else None,
                secret_access_key=credentials.aws_secret_access_key if credentials else None,
                session_token=credentials.aws_session_token if credentials else None,
                expires_after=credentials.expiration.replace(tzinfo=UTC) if credentials and credentials.expiration else None,
                anonymous=credential_type == CredentialType.ANONYMOUS,
                from_env=False,
                get_credentials=credential_refresh_func,
                scatter_initial_credentials=scatter_initial_credentials,
            )
            if network_stream_timeout_seconds is not None:
                r2_kwargs["network_stream_timeout_seconds"] = network_stream_timeout_seconds
            return icechunk.r2_storage(**r2_kwargs)
        # Use s3_storage to create the storage object for s3 or s3-compatible buckets
        s3_kwargs: dict = dict(
            bucket=bucket_config.name,
            prefix=prefix,
            region=region,
            endpoint_url=endpoint_url,
            allow_http=not use_ssl,
            access_key_id=credentials.aws_access_key_id if credentials else None,
            secret_access_key=credentials.aws_secret_access_key if credentials else None,
            session_token=credentials.aws_session_token if credentials else None,
            expires_after=credentials.expiration.replace(tzinfo=UTC) if credentials and credentials.expiration else None,
            anonymous=credential_type == CredentialType.ANONYMOUS,
            from_env=False,
            get_credentials=credential_refresh_func,
            force_path_style=bool(force_path_style),  # mypy thinks force_path_style could be a str
            scatter_initial_credentials=scatter_initial_credentials,
        )
        if network_stream_timeout_seconds is not None:
            s3_kwargs["network_stream_timeout_seconds"] = network_stream_timeout_seconds
        return icechunk.s3_storage(**s3_kwargs)
    # Otherwise, check if the bucket is a GCS bucket
    elif bucket_config.platform in ("gs"):
        if credentials and not isinstance(credentials, GSCredentials):
            raise ValueError(f"Invalid credentials provided for GCS bucket: {credentials}.")

        assert credentials is None or isinstance(credentials, GSCredentials)

        if icechunk.__version__ < "1.1.9":
            if credential_type == CredentialType.ANONYMOUS:
                raise ValueError("Anonymous credentials for GCS are not supported in icechunk version < 1.1.9.")
                # Use gcs_storage to create the storage object for GCS buckets
            return icechunk.gcs_storage(
                bucket=bucket_config.name,
                prefix=prefix,
                service_account_file=None,
                service_account_key=None,
                application_credentials=None,
                bearer_token=credentials.access_token if credentials else None,
                from_env=False,
                config={
                    "user_agent": f"arraylake/{arraylake_version} (uuid={str(user_id)})" if user_id else f"arraylake/{arraylake_version}"
                },
                get_credentials=credential_refresh_func,
                scatter_initial_credentials=scatter_initial_credentials,
            )
        else:
            # Use gcs_storage to create the storage object for GCS buckets
            return icechunk.gcs_storage(
                bucket=bucket_config.name,
                prefix=prefix,
                service_account_file=None,
                service_account_key=None,
                application_credentials=None,
                bearer_token=credentials.access_token if credentials else None,
                from_env=False,
                config={
                    "user_agent": f"arraylake/{arraylake_version} (uuid={str(user_id)})" if user_id else f"arraylake/{arraylake_version}"
                },
                anonymous=credential_type == CredentialType.ANONYMOUS,
                get_credentials=credential_refresh_func,
                scatter_initial_credentials=scatter_initial_credentials,
            )
    # Finally, check if the bucket is an Azure Blob Storage container
    elif bucket_config.platform in ("azure"):
        if credentials and not isinstance(credentials, AzureCredentials):
            raise ValueError(f"Invalid credentials provided for Azure bucket: {credentials}.")

        assert credentials is None or isinstance(credentials, AzureCredentials)

        if not isinstance(bucket_config.auth_config, AzureDelegatedCredentialsAuth):
            raise ValueError(f"Invalid auth config for Azure bucket: {bucket_config.auth_config}")

        return icechunk.azure_storage(
            account=bucket_config.auth_config.storage_account,
            container=bucket_config.name,
            prefix=prefix or "",
            sas_token=credentials.sas_token if credentials else None,
            from_env=False,
        )

    else:
        raise ValueError(f"Unsupported bucket platform: {bucket_config.platform}")


def create_icechunk_store_config(
    bucket_config: BucketResponse,
    user_id: UUID,
) -> icechunk.AnyObjectStoreConfig:
    """
    Create the Icechunk store configuration needed to access data in this bucket.

    Args:
        bucket_config: BucketResponse object containing the bucket nickname.
        user_id: The arraylake user ID of the principal that will be accessing the storage object.

    Returns:
        icechunk.ObjectStoreConfig instance
    """

    logger.debug(f"Using bucket {bucket_config.name} for Icechunk store config")

    # Check the if the bucket is an S3 or S3-compatible bucket
    if bucket_config.platform in ("s3", "s3c", "s3-compatible", "minio"):
        # Extract the endpoint URL from the bucket config, if it exists
        endpoint_url = bucket_config.extra_config.get("endpoint_url")
        if endpoint_url is not None:
            endpoint_url = str(endpoint_url)  # mypy thinks the endpoint_url could be a bool

        region = bucket_config.extra_config.get("region_name")
        if region is not None:
            region = str(region)  # mypy thinks the region could be a bool

        # Extract the use_ssl flag from the bucket config, if it exists
        use_ssl = bucket_config.extra_config.get("use_ssl", True)
        allow_http = not use_ssl

        # Default the force_path_style to True for allow_http and False otherwise
        force_path_style_raw = bucket_config.extra_config.get("force_path_style", False if use_ssl else True)
        force_path_style = bool(force_path_style_raw)

        if endpoint_url and ("fly.storage.tigris.dev" in endpoint_url or "t3.storage.dev" in endpoint_url):
            if region is None or region == "auto":
                raise ValueError(
                    f"Region cannot be {region} for Tigris buckets. "
                    f"A specific Tigris region must be set on the bucket: https://www.tigrisdata.com/docs/concepts/regions/"
                )

            options = icechunk.S3Options(
                region=region,
                endpoint_url=endpoint_url,
                allow_http=allow_http,
            )
            return icechunk.ObjectStoreConfig.S3Compatible(options)

        elif endpoint_url and ".r2." in endpoint_url:
            options = icechunk.S3Options(
                region=region,
                endpoint_url=endpoint_url,
                allow_http=allow_http,
            )
            return icechunk.ObjectStoreConfig.S3Compatible(options)

        # s3 or s3-compatible buckets
        options = icechunk.S3Options(
            region=region,
            endpoint_url=endpoint_url,
            allow_http=allow_http,
            force_path_style=force_path_style,
        )
        return icechunk.ObjectStoreConfig.S3(options)

    # Otherwise, check if the bucket is a GCS bucket
    elif bucket_config.platform in ("gs"):
        from arraylake import __version__ as arraylake_version

        config = {"user_agent": f"arraylake/{arraylake_version} (uuid={str(user_id)})" if user_id else f"arraylake/{arraylake_version}"}
        return icechunk.ObjectStoreConfig.Gcs(config)

    # Finally, check if the bucket is an Azure Blob Storage container
    elif bucket_config.platform in ("azure"):
        # Icechunk does not currently support any additional config for Azure Blob Storage
        config = {}
        return icechunk.ObjectStoreConfig.Azure(config)

    else:
        raise ValueError(f"Unsupported bucket platform: {bucket_config.platform}")
