import uuid
from typing import Callable

import icechunk
import pytest

from arraylake import __version__ as arraylake_version
from arraylake.repos.icechunk.storage import (
    ICECHUNK_REQUIRED_ENV_VARS,
    CredentialType,
    _get_credential_type,
    _get_icechunk_storage_obj,
)
from arraylake.types import DBID, BucketResponse, GSCredentials, S3Credentials

repo_id = DBID(b"some_repo_id")


def test_get_credential_type(
    s3_credentials: S3Credentials,
    gs_credentials: GSCredentials,
    credential_refresh_func: Callable,
):
    assert _get_credential_type(s3_credentials, None) == CredentialType.PROVIDED
    assert _get_credential_type(gs_credentials, None) == CredentialType.PROVIDED
    assert _get_credential_type(None, credential_refresh_func) == CredentialType.PROVIDED
    assert _get_credential_type(None, None) == CredentialType.ANONYMOUS


def test_get_icechunk_storage_obj_s3_credentials(
    s3_bucket_config: BucketResponse,
    s3_credentials: S3Credentials,
):
    storage = _get_icechunk_storage_obj(
        bucket_config=s3_bucket_config,
        prefix=None,
        credentials=s3_credentials,
        credential_type=CredentialType.PROVIDED,
        credential_refresh_func=None,
        scatter_initial_credentials=False,
        arraylake_version=arraylake_version,
        user_id=uuid.uuid4(),
    )
    assert isinstance(storage, icechunk.Storage)


def test_get_icechunk_storage_obj_gcs_credentials(
    gcs_bucket_config: BucketResponse,
    gs_credentials: GSCredentials,
):
    storage = _get_icechunk_storage_obj(
        bucket_config=gcs_bucket_config,
        prefix=None,
        credentials=gs_credentials,
        credential_type=CredentialType.PROVIDED,
        credential_refresh_func=None,
        scatter_initial_credentials=False,
        arraylake_version=arraylake_version,
        user_id=uuid.uuid4(),
    )
    assert isinstance(storage, icechunk.Storage)


def test_get_icechunk_storage_obj_s3_no_credentials(s3_bucket_config: BucketResponse):
    storage = _get_icechunk_storage_obj(
        bucket_config=s3_bucket_config,
        prefix=None,
        credentials=None,
        credential_type=CredentialType.ANONYMOUS,
        credential_refresh_func=None,
        scatter_initial_credentials=False,
        arraylake_version=arraylake_version,
        user_id=uuid.uuid4(),
    )
    assert isinstance(storage, icechunk.Storage)


def test_get_icechunk_storage_obj_tigris_no_credentials(
    tigris_bucket_config: BucketResponse,
):
    storage = _get_icechunk_storage_obj(
        bucket_config=tigris_bucket_config,
        prefix=None,
        credentials=None,
        credential_type=CredentialType.ANONYMOUS,
        credential_refresh_func=None,
        scatter_initial_credentials=False,
        arraylake_version=arraylake_version,
        user_id=uuid.uuid4(),
    )
    assert isinstance(storage, icechunk.Storage)


def test_get_icechunk_storage_obj_tigris_no_region(
    tigris_bucket_config: BucketResponse,
):
    tigris_bucket_config = tigris_bucket_config.copy(deep=True)
    tigris_bucket_config.extra_config.pop("region_name")
    with pytest.raises(ValueError) as e:
        _get_icechunk_storage_obj(
            bucket_config=tigris_bucket_config,
            prefix=None,
            credentials=None,
            credential_type=CredentialType.ANONYMOUS,
            credential_refresh_func=None,
            scatter_initial_credentials=False,
            arraylake_version=arraylake_version,
            user_id=uuid.uuid4(),
        )
    assert "Region cannot be None for Tigris buckets" in str(e.value)


def test_get_icechunk_storage_obj_tigris_auto_region(
    tigris_bucket_config: BucketResponse,
):
    tigris_bucket_config = tigris_bucket_config.copy(deep=True)
    tigris_bucket_config.extra_config["region_name"] = "auto"
    with pytest.raises(ValueError) as e:
        _get_icechunk_storage_obj(
            bucket_config=tigris_bucket_config,
            prefix=None,
            credentials=None,
            credential_type=CredentialType.ANONYMOUS,
            credential_refresh_func=None,
            scatter_initial_credentials=False,
            arraylake_version=arraylake_version,
            user_id=uuid.uuid4(),
        )
    assert "Region cannot be auto for Tigris buckets" in str(e.value)


def test_get_icechunk_storage_obj_gcs_anonymous_credentials(gcs_bucket_config: BucketResponse):
    if icechunk.__version__ < "1.1.9":
        pytest.skip("Requires icechunk version >= 1.1.9")

    storage = _get_icechunk_storage_obj(
        bucket_config=gcs_bucket_config,
        prefix=None,
        credentials=None,
        credential_type=CredentialType.ANONYMOUS,
        credential_refresh_func=None,
        scatter_initial_credentials=False,
        arraylake_version=arraylake_version,
        user_id=uuid.uuid4(),
    )
    assert isinstance(storage, icechunk.Storage)


def test_get_icechunk_storage_obj_invalid_credential_input(
    s3_bucket_config: BucketResponse,
    s3_credentials: S3Credentials,
    credential_refresh_func: Callable,
):
    with pytest.raises(ValueError) as e:
        _get_icechunk_storage_obj(
            bucket_config=s3_bucket_config,
            prefix=None,
            credentials=s3_credentials,
            credential_type=CredentialType.PROVIDED,
            credential_refresh_func=credential_refresh_func,
            scatter_initial_credentials=True,
            arraylake_version=arraylake_version,
            user_id=uuid.uuid4(),
        )
    assert "Cannot provide both static credentials and a credential refresh function" in str(e.value)


def test_get_icechunk_storage_obj_anonymous_minio_bucket(
    anon_minio_bucket_config,
):
    # Create storage object with anonymous credentials
    storage = _get_icechunk_storage_obj(
        bucket_config=anon_minio_bucket_config,
        prefix=f"test-{uuid.uuid4().hex}",
        credentials=None,
        credential_type=CredentialType.ANONYMOUS,
        credential_refresh_func=None,
        scatter_initial_credentials=False,
        arraylake_version=arraylake_version,
        user_id=uuid.uuid4(),
    )
    assert isinstance(storage, icechunk.Storage)
