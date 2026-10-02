import pytest
import json
import time
from tmo import TmoClient


@pytest.fixture
def pat_tmo_client(mocker):
    mock_client = TmoClient.__new__(TmoClient)
    mock_client.ssl_verify = False
    mock_client.vmo_url = "https://awsmodelops.review.innovationlabs.teradata.com/api/accounts/mock_account/modelops/core"
    mock_client.auth_mode = "pat"
    mock_client._TmoClient__user = "pat_user"
    mock_client._TmoClient__pat = "pat_test_value"
    mock_client.session = mocker.MagicMock()
    mock_client.session.headers = {}
    mock_client.logger = mocker.Mock()

    return mock_client


def test_pat_authentication_sets_token(mocker, pat_tmo_client):
    mocker.patch.object(
        pat_tmo_client,
        "_TmoClient__create_self_signed_jwt",
        return_value="mock_auth_token",
    )
    mocker.patch("os.path.exists", return_value=False)

    pat_tmo_client._TmoClient__create_auth_session_pat()  # noqa

    assert pat_tmo_client.session.headers["Authorization"] == "Bearer mock_auth_token"


def test_token_is_reused_when_not_expired(mocker, pat_tmo_client):
    valid_token = {"token": "cached_token", "exp": time.time() + 180}
    m = mocker.mock_open(read_data=json.dumps(valid_token))
    mocker.patch("builtins.open", m)
    mocker.patch("os.path.exists", return_value=True)

    pat_tmo_client._TmoClient__create_auth_session_pat()  # noqa

    assert pat_tmo_client.session.headers["Authorization"] == "Bearer cached_token"


def test_token_is_refreshed_when_expired(mocker, pat_tmo_client):
    expired_token = {"token": "expired_token", "exp": time.time() - 10}
    m = mocker.mock_open(read_data=json.dumps(expired_token))
    mocker.patch("builtins.open", m)
    mocker.patch("os.path.exists", return_value=True)
    mocker.patch.object(pat_tmo_client, "_TmoClient__remove_cached_token")
    mocker.patch.object(
        pat_tmo_client,
        "_TmoClient__create_self_signed_jwt",
        return_value="new_mock_token",
    )

    pat_tmo_client._TmoClient__create_auth_session_pat()  # noqa

    assert pat_tmo_client.session.headers["Authorization"] == "Bearer new_mock_token"


def test_missing_pat_raises_exception(mocker, pat_tmo_client):
    pat_tmo_client._TmoClient__pat = None  # Simulate missing PAT

    with pytest.raises(Exception) as exc_info:
        pat_tmo_client._TmoClient__create_auth_session_pat()  # noqa

    assert "Missing CLI configuration" in str(exc_info.value)
