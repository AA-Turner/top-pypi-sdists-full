from datetime import datetime, timezone

import icechunk
import pytest

from arraylake.repos.icechunk.virtual import _ensure_utc, get_icechunk_container_credentials
from arraylake.types import S3Credentials


def test_get_icechunk_container_credentials_s3_credentials(s3_credentials):
    con_creds = get_icechunk_container_credentials("s3", s3_credentials, None)
    assert isinstance(con_creds, icechunk.S3Credentials.Static)
    # TODO: can we check the access key ID and secret access key?


def test_get_icechunk_container_credentials_naive_expiration_does_not_raise():
    """Regression: a tz-naive expiration was passed straight to icechunk, whose Rust layer
    requires a tz-aware UTC datetime and raised 'expected datetime.timezone.utc', 500ing the
    marketplace dataset-node endpoint."""
    creds = S3Credentials(
        aws_access_key_id="AKIA",
        aws_secret_access_key="secret",
        aws_session_token="token",
        expiration=datetime(2030, 1, 1, 0, 0, 0),
    )
    con_creds = get_icechunk_container_credentials("s3", creds, None)
    assert isinstance(con_creds, icechunk.S3Credentials.Static)


def test_ensure_utc():
    naive = datetime(2030, 1, 1, 12, 0, 0)
    assert _ensure_utc(naive) == datetime(2030, 1, 1, 12, 0, 0, tzinfo=timezone.utc)
    aware = datetime(2030, 1, 1, 12, 0, 0, tzinfo=timezone.utc)
    assert _ensure_utc(aware) is aware
    assert _ensure_utc(None) is None


def test_get_icechunk_container_credentials_credential_refresh(credential_refresh_func):
    con_creds = get_icechunk_container_credentials("s3", None, credential_refresh_func)
    assert isinstance(con_creds, icechunk.S3Credentials.Refreshable)
    # TODO: can we check the refresh function?


def test_get_icechunk_container_credentials_anonymous():
    con_creds = get_icechunk_container_credentials("s3", None, None)
    assert isinstance(con_creds, icechunk.S3Credentials.Anonymous)


def test_get_icechunk_container_credentials_gcs_static(gs_credentials):
    con_creds = get_icechunk_container_credentials("gs", gs_credentials, None)
    assert isinstance(con_creds, icechunk.GcsCredentials.Static)


def test_get_icechunk_container_credentials_gcs_credential_refresh(credential_refresh_func):
    con_creds = get_icechunk_container_credentials("gs", None, credential_refresh_func)
    assert isinstance(con_creds, icechunk.GcsCredentials.Refreshable)


def test_get_icechunk_container_credentials_gcs_anonymous():
    con_creds = get_icechunk_container_credentials("gs", None, None)
    assert isinstance(con_creds, icechunk.GcsCredentials.Anonymous)


def test_get_icechunk_container_credentials_gcs_raises():
    with pytest.raises(ValueError) as e:
        get_icechunk_container_credentials("gcs", None, None)
    assert "Unsupported bucket platform for virtual chunk container credentials" in str(e.value)


def test_get_icechunk_container_credentials_creds_and_refresh_raises(s3_credentials, credential_refresh_func):
    with pytest.raises(ValueError) as e:
        get_icechunk_container_credentials("s3", s3_credentials, credential_refresh_func)
    assert "Cannot provide both static credentials and a credential refresh function" in str(e.value)


def test_get_icechunk_container_credentials_invalid_platform():
    with pytest.raises(ValueError) as e:
        get_icechunk_container_credentials("foo", None, None)
    assert "Unsupported bucket platform for virtual chunk container credentials" in str(e.value)
