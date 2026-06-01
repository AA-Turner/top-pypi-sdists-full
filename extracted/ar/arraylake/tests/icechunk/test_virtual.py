import icechunk
import pytest

from arraylake.repos.icechunk.virtual import get_icechunk_container_credentials


def test_get_icechunk_container_credentials_s3_credentials(s3_credentials):
    con_creds = get_icechunk_container_credentials("s3", s3_credentials, None)
    assert isinstance(con_creds, icechunk.S3Credentials.Static)
    # TODO: can we check the access key ID and secret access key?


def test_get_icechunk_container_credentials_credential_refresh(credential_refresh_func):
    con_creds = get_icechunk_container_credentials("s3", None, credential_refresh_func)
    assert isinstance(con_creds, icechunk.S3Credentials.Refreshable)
    # TODO: can we check the refresh function?


def test_get_icechunk_container_credentials_anonymous():
    con_creds = get_icechunk_container_credentials("s3", None, None)
    assert isinstance(con_creds, icechunk.S3Credentials.Anonymous)


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
