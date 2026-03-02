import json
import os
import time

import aia
import oauthlib.oauth2.rfc6749.errors
import pandas as pd
import pytest
import requests

from tmo.api_client import TmoClient, ConfigurationError


def make_client(mocker):
    client = TmoClient.__new__(TmoClient)
    client.logger = mocker.Mock()
    client.ssl_verify = False
    client.vmo_url = None
    client.auth_mode = None
    client._TmoClient__client_id = None
    client._TmoClient__client_secret = None
    client._TmoClient__token_url = None
    client._TmoClient__device_auth_url = None
    client._TmoClient__bearer_token = None
    client._TmoClient__pat = None
    client._TmoClient__user = None
    client.project_id = None
    return client


def test_strip_url():
    assert (
        TmoClient._TmoClient__strip_url("https://example.com/")  # noqa
        == "https://example.com"
    )
    assert (
        TmoClient._TmoClient__strip_url("https://example.com")  # noqa
        == "https://example.com"
    )


def test_validate_and_extract_body_401_calls_remove_and_raises(mocker):
    client = make_client(mocker)
    # patch remove cached token to observe call
    mock_remove = mocker.patch.object(TmoClient, "_TmoClient__remove_cached_token")

    # response that simulates 401 and HTTPError on raise_for_status
    class Resp:
        status_code = 401
        text = "bad token text"

        def raise_for_status(self):
            raise requests.exceptions.HTTPError("original")

        def json(self):
            return {}

    resp = Resp()
    with pytest.raises(requests.exceptions.HTTPError) as exc:
        client._TmoClient__validate_and_extract_body(resp)  # noqa
    assert "Error message: bad token text" in str(exc.value)
    mock_remove.assert_called_once()


def test_create_self_signed_jwt_reads_key_and_saves(mocker, tmp_path):
    client = make_client(mocker)
    client.vmo_url = "https://org123.some.host"
    client._TmoClient__pat = "PATVALUE"
    client._TmoClient__user = "user1"

    pk_path = tmp_path / "pat.pem"
    pk_path.write_text("PRIVATE_KEY_CONTENT")
    # override default path so open reads our temp file
    client.DEFAULT_PAT_PRIVATE_KEY_PATH = str(pk_path)

    # patch jwt.encode and save method
    mock_encode = mocker.patch("tmo.api_client.jwt.encode", return_value="SIGNED_JWT")
    mock_save = mocker.patch.object(TmoClient, "_TmoClient__save_signed_jwt")

    signed = client._TmoClient__create_self_signed_jwt()  # noqa
    assert signed == "SIGNED_JWT"
    mock_encode.assert_called_once()
    # __create_self_signed_jwt should call __save_signed_jwt with signed jwt and exp
    mock_save.assert_called_once()
    args = mock_save.call_args[0]
    assert args[0] == "SIGNED_JWT"
    assert isinstance(args[1], int)


def test_remove_cached_token_deletes_file(tmp_path):
    # set class path to a temp file and ensure removal
    token_path = tmp_path / ".token"
    token_path.write_text("dummy")
    TmoClient.DEFAULT_TOKEN_CACHE_FILE_PATH = str(token_path)
    # call static method
    TmoClient._TmoClient__remove_cached_token()  # noqa
    assert not token_path.exists()


def test_validate_stored_token_no_file_generates_token_and_updates_session(mocker):
    client = make_client(mocker)
    # ensure no file exists
    mock_exists = mocker.patch("os.path.exists", return_value=False)
    # patch method that creates signed jwt
    mock_create_jwt = mocker.patch.object(
        TmoClient, "_TmoClient__create_self_signed_jwt", return_value="NEW_JWT"
    )
    # avoid TLS chase side effects by providing a dummy session class later
    if hasattr(client, "session"):
        del client.session

    client._TmoClient__validate_stored_token()  # noqa
    # after call, session and header should be present
    assert hasattr(client, "session")
    assert client.session.headers["Authorization"] == "Bearer NEW_JWT"
    mock_create_jwt.assert_called_once()


def test_validate_stored_token_expired_calls_remove_and_refresh(mocker, tmp_path):
    client = make_client(mocker)
    # create a token file with expired timestamp
    token_path = tmp_path / ".token"
    token_data = {"token": "OLD", "exp": int(time.time()) - 10}
    token_path.write_text(json.dumps(token_data))
    # patch DEFAULT_TOKEN_CACHE_FILE_PATH to point to this file
    TmoClient.DEFAULT_TOKEN_CACHE_FILE_PATH = str(token_path)

    mock_remove = mocker.patch.object(TmoClient, "_TmoClient__remove_cached_token")
    mock_create_jwt = mocker.patch.object(
        TmoClient, "_TmoClient__create_self_signed_jwt", return_value="REFRESHED"
    )
    # call validate
    client._TmoClient__validate_stored_token()  # noqa
    mock_remove.assert_called_once()
    assert client.session.headers["Authorization"] == "Bearer REFRESHED"
    mock_create_jwt.assert_called_once()


def test_validate_stored_token_valid_file_uses_existing_token(mocker, tmp_path):
    client = make_client(mocker)
    token_path = tmp_path / ".token"
    token_data = {"token": "GOOD", "exp": int(time.time()) + 3600}
    token_path.write_text(json.dumps(token_data))
    TmoClient.DEFAULT_TOKEN_CACHE_FILE_PATH = str(token_path)

    # no creation should happen
    mock_create_jwt = mocker.patch.object(
        TmoClient, "_TmoClient__create_self_signed_jwt"
    )
    client._TmoClient__validate_stored_token()  # noqa
    assert client.session.headers["Authorization"] == "Bearer GOOD"
    mock_create_jwt.assert_not_called()


def test_chase_tls_cert_chain_raises_when_no_vmo_url(mocker):
    client = make_client(mocker)
    # ensure vmo_url not set or falsy
    if hasattr(client, "vmo_url"):
        del client.vmo_url
    with pytest.raises(ConfigurationError):
        client._TmoClient__chase_tls_cert_chain()  # noqa


def test_set_session_tls_disables_warnings_when_ssl_false(mocker, monkeypatch):
    client = make_client(mocker)
    client.session = requests.Session()
    client.ssl_verify = False
    # make env var to something other than 'true' to trigger potential warning path
    monkeypatch.setenv("CALLED_FROM_TEST", "true")
    # patch disable_warnings
    disable_warnings = mocker.patch("requests.packages.urllib3.disable_warnings")
    # call method
    client._TmoClient__set_session_tls()  # noqa
    assert client.session.verify is False
    disable_warnings.assert_called_once()


def test_set_project_id_warns_if_project_not_found(mocker):
    client = make_client(mocker)
    client.logger = mocker.Mock()

    class FakeProjects:
        def find_by_id(self, project_id):
            return None

    mocker.patch.object(client, "projects", return_value=FakeProjects())
    client.set_project_id("nonexistent")
    # logger.warning should be called because project not found
    client.logger.warning.assert_called()


def test_create_auth_session_pat_raises_when_missing_credentials(mocker):
    # create instance and ensure pat/user are None
    client = TmoClient.__new__(TmoClient)
    client.logger = mocker.Mock()
    client._TmoClient__pat = None
    client._TmoClient__user = None
    with pytest.raises(ConfigurationError):
        client._TmoClient__create_auth_session_pat()  # noqa


def test_parse_kwargs_sets_attributes():
    client = TmoClient.__new__(TmoClient)
    client.vmo_url = None
    client.ssl_verify = True
    client.auth_mode = None
    client._TmoClient__client_id = None
    client._TmoClient__client_secret = None
    client._TmoClient__token_url = None
    client._TmoClient__device_auth_url = None
    client._TmoClient__bearer_token = None
    client._TmoClient__pat = None
    client._TmoClient__user = None
    kwargs = {
        "vmo_url": "https://test.com",
        "ssl_verify": False,
        "auth_mode": "pat",
        "pat": "PAT",
        "user": "user",
    }
    client._TmoClient__parse_kwargs(**kwargs)  # noqa
    assert client.vmo_url == "https://test.com"
    assert client.ssl_verify is False
    assert client.auth_mode == "pat"
    assert client._TmoClient__pat == "PAT"
    assert client._TmoClient__user == "user"


def test_parse_env_variables_sets_attributes(monkeypatch):
    client = TmoClient.__new__(TmoClient)
    monkeypatch.setenv("VMO_URL", "https://env.com")
    monkeypatch.setenv("VMO_SSL_VERIFY", "false")
    monkeypatch.setenv("VMO_API_AUTH_MODE", "bearer")
    monkeypatch.setenv("VMO_API_AUTH_BEARER_TOKEN", "TOKEN")
    client.vmo_url = None
    client.ssl_verify = True
    client.auth_mode = None
    client._TmoClient__bearer_token = None
    client._TmoClient__parse_env_variables()  # noqa
    assert client.vmo_url == "https://env.com"
    assert client.ssl_verify is False
    assert client.auth_mode == "bearer"
    assert client._TmoClient__bearer_token == "TOKEN"


def test_check_legacy_mode_oauth_cc():
    client = TmoClient.__new__(TmoClient)
    client.auth_mode = "oauth-cc"
    client._TmoClient__check_legacy_mode()  # noqa
    assert client.auth_mode == "client_credentials"


def test_check_legacy_mode_oauth():
    client = TmoClient.__new__(TmoClient)
    client.auth_mode = "oauth"
    client._TmoClient__check_legacy_mode()  # noqa
    assert client.auth_mode == "device_code"


def test_validate_url_raises():
    client = TmoClient.__new__(TmoClient)
    client.vmo_url = None
    with pytest.raises(ValueError):
        client._TmoClient__validate_url()  # noqa


def test_select_header_accept_none():
    assert TmoClient.select_header_accept([]) is None


def test_select_header_accept_list():
    result = TmoClient.select_header_accept(["application/json", "text/plain"])
    assert result == "application/json, text/plain"


def test_get_current_project():
    client = TmoClient.__new__(TmoClient)
    client.project_id = "abc123"
    assert client.get_current_project() == "abc123"


def test_init_raises_for_none(monkeypatch):
    monkeypatch.setattr(TmoClient, "_TmoClient__rename_tmo_config", lambda self: None)
    monkeypatch.setattr(
        TmoClient, "_TmoClient__parse_tmo_config", lambda self, **kwargs: None
    )
    with pytest.raises(ConfigurationError):
        TmoClient(auth_mode=None)


def test_init_raises_for_invalid(monkeypatch):
    monkeypatch.setattr(TmoClient, "_TmoClient__rename_tmo_config", lambda self: None)

    def _fake_parse(self, **kwargs):
        if "auth_mode" in kwargs:
            setattr(self, "auth_mode", kwargs.get("auth_mode"))

    monkeypatch.setattr(TmoClient, "_TmoClient__parse_tmo_config", _fake_parse)
    with pytest.raises(ValueError):
        TmoClient(auth_mode="invalid_mode")


def test_init_with_invalid_auth_mode():
    with pytest.raises(ValueError):
        TmoClient(auth_mode="invalid_mode")


def test_get_request_404_returns_none(mocker):
    client = make_client(mocker)
    client.vmo_url = "https://example.com"
    client.session = mocker.Mock()
    resp = mocker.Mock()
    resp.status_code = 404
    client.session.get.return_value = resp
    assert client.get_request("/path", {}, {}) is None


def test_get_request_retries_on_connection_error_then_success(mocker):
    client = make_client(mocker)
    client.vmo_url = "https://example.com"
    client.session = mocker.Mock()
    resp = mocker.Mock()
    resp.status_code = 200
    resp.json.return_value = {"ok": True}
    client.session.get.side_effect = [
        requests.exceptions.ConnectionError(),
        requests.exceptions.ConnectionError(),
        resp,
    ]
    result = client.get_request("/path", {}, {})
    assert result == {"ok": True}


def test_get_request_max_retries_logs_error_returns_none(mocker):
    client = make_client(mocker)
    client.vmo_url = "https://example.com"
    client.session = mocker.Mock()
    client.MAX_RETRIES = 2
    client.session.get.side_effect = requests.exceptions.ConnectionError()
    client.logger = mocker.Mock()
    ret = client.get_request("/path", {}, {})
    assert ret is None
    client.logger.error.assert_called()


def test_validate_and_extract_body_raises_original_http_error(mocker):
    client = make_client(mocker)

    class Resp:
        status_code = 500
        text = ""

        def raise_for_status(self):
            raise requests.exceptions.HTTPError("original")

        def json(self):
            return {}

    with pytest.raises(requests.exceptions.HTTPError) as exc:
        client._TmoClient__validate_and_extract_body(Resp())  # type: ignore
    assert "original" in str(exc.value)


def test_validate_and_extract_body_json_error_returns_text(mocker):
    client = make_client(mocker)

    class Resp:
        status_code = 200
        text = "plain text"

        def raise_for_status(self):
            return None

        def json(self):
            raise ValueError("no json")

    res = client._TmoClient__validate_and_extract_body(Resp())  # type: ignore
    assert res == "plain text"


def test_chase_tls_cert_chain_uses_aia_and_sets_verify(tmp_path, mocker):
    client = make_client(mocker)
    client.vmo_url = "https://org.example"
    client.session = requests.Session()
    mocker.patch("requests.get", side_effect=requests.exceptions.SSLError("ssl"))

    class FakeAIASession:
        def cadata_from_url(self, url):
            return "CERTDATA\n"

    mocker.patch("aia.AIASession", FakeAIASession)
    client._TmoClient__chase_tls_cert_chain()  # noqa
    assert isinstance(client.session.verify, str)
    assert os.path.exists(client.session.verify)
    os.remove(client.session.verify)


def test_chase_tls_cert_chain_invalid_ca_raises(tmp_path, mocker):
    client = make_client(mocker)
    client.vmo_url = "https://org.example"
    client.session = requests.Session()
    mocker.patch("requests.get", side_effect=requests.exceptions.SSLError("ssl"))

    class FakeAIASession:
        def cadata_from_url(self, url):
            raise aia.InvalidCAError("invalid ca")

    mocker.patch("aia.AIASession", FakeAIASession)
    with pytest.raises(requests.exceptions.SSLError):
        client._TmoClient__chase_tls_cert_chain()  # type: ignore


def test_set_session_tls_logs_warning_when_ssl_disabled(mocker):
    client = make_client(mocker)
    client.session = requests.Session()
    client.ssl_verify = False
    mocker.patch.dict(os.environ, {"CALLED_FROM_TEST": "false"}, clear=False)
    disable_warnings = mocker.patch("requests.packages.urllib3.disable_warnings")
    client._TmoClient__set_session_tls()  # type: ignore
    assert client.session.verify is False
    disable_warnings.assert_called_once()
    client.logger.warning.assert_called()


def test_create_oauth_session_client_credentials_missing_raises(mocker):
    client = make_client(mocker)
    client._TmoClient__client_id = None
    client._TmoClient__client_secret = None
    client._TmoClient__token_url = None
    with pytest.raises(ValueError):
        client._TmoClient__create_oauth_session_client_credentials()  # type: ignore


def test_create_oauth_session_bearer_sets_header(mocker):
    client = make_client(mocker)
    client._TmoClient__bearer_token = "Bearer TOKENX"
    client._TmoClient__create_oauth_session_bearer()  # type: ignore
    assert client.session.headers["Authorization"] == "Bearer TOKENX"


def test_get_device_code_non_200_raises(mocker):
    client = make_client(mocker)
    client._TmoClient__client_id = "cid"
    client._TmoClient__client_secret = None
    client._TmoClient__device_auth_url = "https://device"
    client._TmoClient__token_url = "https://token"
    client.session = mocker.Mock()
    resp = mocker.Mock()
    resp.status_code = 400
    resp.json.return_value = {}
    client.session.post.return_value = resp
    with pytest.raises(ValueError):
        client._TmoClient__get_device_code()  # type: ignore


def test_handle_device_code_retries_on_invalid_grant(mocker):
    client = make_client(mocker)
    err = oauthlib.oauth2.rfc6749.errors.InvalidGrantError(
        description="Token is not active"
    )
    called = {"count": 0}

    def fake_create(self):
        called["count"] += 1
        if called["count"] == 1:
            raise err
        return None

    mocker.patch.object(
        TmoClient, "_TmoClient__create_oauth_session_device_code", fake_create
    )
    mocker.patch.object(TmoClient, "_TmoClient__remove_cached_token")
    client._TmoClient__handle_device_code()  # type: ignore
    assert called["count"] == 2


def test_handle_device_code_retries_on_invalid_token_error(mocker):
    client = make_client(mocker)
    err = oauthlib.oauth2.rfc6749.errors.InvalidTokenError(description="Invalid token")
    called = {"count": 0}

    def fake_create(self):
        called["count"] += 1
        if called["count"] == 1:
            raise err
        return None

    mocker.patch.object(
        TmoClient, "_TmoClient__create_oauth_session_device_code", fake_create
    )
    mocker.patch.object(TmoClient, "_TmoClient__remove_cached_token")
    client._TmoClient__handle_device_code()  # type: ignore
    assert called["count"] == 2


def test_save_oauth_token_writes_and_sets_bearer(tmp_path, mocker):
    client = make_client(mocker)
    token_path = tmp_path / ".token"
    TmoClient.DEFAULT_TOKEN_CACHE_FILE_PATH = str(token_path)
    token = {"access_token": "abc123", "expires_in": 2}
    client._TmoClient__save_oauth_token(token)  # type: ignore
    with open(TmoClient.DEFAULT_TOKEN_CACHE_FILE_PATH, "r") as f:
        data = json.load(f)
    assert "expires_at" in data
    assert client._TmoClient__bearer_token == "Bearer abc123"  # type: ignore


def test_remove_cached_token_deletes_if_exists(tmp_path):
    path = tmp_path / ".token"
    path.write_text("x")
    TmoClient.DEFAULT_TOKEN_CACHE_FILE_PATH = str(path)
    TmoClient._TmoClient__remove_cached_token()  # type: ignore
    assert not path.exists()


# Additional tests merged from tests/api_client.py


def test_post_put_delete_request_calls_session_and_returns_page(mocker):
    client = make_client(mocker)
    client.vmo_url = "https://example.com/"
    client.auth_mode = "pat"
    client.session = mocker.Mock()
    mock_validate = mocker.patch.object(TmoClient, "_TmoClient__validate_stored_token")
    mock_validate_and_extract = mocker.patch.object(
        TmoClient, "_TmoClient__validate_and_extract_body", return_value={"ok": True}
    )

    body = {"a": 1}
    client.post_request("/p", {}, {}, body)  # type: ignore
    client.session.post.assert_called_once()
    called_args = client.session.post.call_args[1]
    assert called_args["url"] == "https://example.com/p"
    assert json.loads(called_args["data"]) == body

    client.session.post.reset_mock()
    client.put_request("/p2", {"h": "v"}, {"q": "1"}, body)  # type: ignore
    client.session.put.assert_called_once()
    put_args = client.session.put.call_args[1]
    assert put_args["url"] == "https://example.com/p2"
    assert json.loads(put_args["data"]) == body

    client.session.put.reset_mock()
    client.delete_request("/p3", {}, {}, body)  # type: ignore
    client.session.delete.assert_called_once()
    del_args = client.session.delete.call_args[1]
    assert del_args["url"] == "https://example.com/p3"
    assert json.loads(del_args["data"]) == body


def test_get_request_handles_unexpected_exception_and_logs(mocker):
    client = make_client(mocker)
    client.vmo_url = "https://example.com"
    client.session = mocker.Mock()
    client.session.get.side_effect = ValueError("boom")
    mock_log = mocker.patch("logging.error")
    res = client.get_request("/x", {}, {})
    assert res is None
    mock_log.assert_called()


def test_create_self_signed_jwt_raises_when_key_missing(mocker, tmp_path):
    client = make_client(mocker)
    client.vmo_url = "https://org123.something"
    client._TmoClient__pat = "p"
    client._TmoClient__user = "u"
    non_existing = tmp_path / "nope.pem"
    client.DEFAULT_PAT_PRIVATE_KEY_PATH = str(non_existing)
    with pytest.raises(FileNotFoundError):
        client._TmoClient__create_self_signed_jwt()  # type: ignore


def test_describe_current_project_returns_dataframe_when_project_found(mocker):
    client = make_client(mocker)
    client.project_id = "proj1"

    class FakeProjects:
        def find_by_id(self, project_id, expand=None):
            return {"id": project_id, "name": "P", "_links": {}, "userAttributes": {}}

    mocker.patch.object(client, "projects", return_value=FakeProjects())
    df = client.describe_current_project()
    assert isinstance(df, pd.DataFrame)
    assert "attribute" in df.columns and "value" in df.columns


def test_describe_current_project_returns_none_when_no_project_or_not_found(mocker):
    client = make_client(mocker)
    client.project_id = None
    assert client.describe_current_project() is None
    client.project_id = "p"

    class FakeProjects2:
        def find_by_id(self, project_id, expand=None):
            return None

    mocker.patch.object(client, "projects", return_value=FakeProjects2())
    assert client.describe_current_project() is None


def test_get_default_connection_id_variants(mocker):
    client = make_client(mocker)

    class UA:
        def get_default_connection(self):
            return {"value": {"defaultDatasetConnectionId": "cid123"}}

    mocker.patch.object(client, "user_attributes", return_value=UA())
    assert client.get_default_connection_id() == "cid123"

    class UA2:
        def get_default_connection(self):
            return None

    mocker.patch.object(client, "user_attributes", return_value=UA2())
    assert client.get_default_connection_id() is None

    class UA3:
        def get_default_connection(self):
            raise RuntimeError("boom")

    mocker.patch.object(client, "user_attributes", return_value=UA3())
    assert client.get_default_connection_id() is None


def test_api_wrapper_methods_return_clients(mocker):
    client = make_client(mocker)
    for method in (
        "projects",
        "datasets",
        "dataset_templates",
        "dataset_connections",
        "deployments",
        "feature_engineering",
        "jobs",
        "job_events",
        "messages",
        "models",
        "trained_models",
        "trained_model_artefacts",
        "trained_model_events",
        "user_attributes",
    ):
        func = getattr(client, method)
        obj = func()
        assert hasattr(obj, "tmo_client")
        assert obj.tmo_client is client


def test_get_device_code_successful_flow(mocker, monkeypatch):
    client = make_client(mocker)
    client._TmoClient__client_id = "cid"
    client._TmoClient__client_secret = None
    client._TmoClient__device_auth_url = "https://device"
    client._TmoClient__token_url = "https://token"
    client.session = mocker.Mock()

    device_resp = mocker.Mock()
    device_resp.status_code = 200
    device_resp.json.return_value = {
        "device_code": "DC",
        "user_code": "UC",
        "verification_uri_complete": "https://verify",
        "interval": 0,
    }

    token_pending = mocker.Mock()
    token_pending.status_code = 400
    token_pending.json.return_value = {"error": "authorization_pending"}

    token_ok = mocker.Mock()
    token_ok.status_code = 200
    token_ok.json.return_value = {"access_token": "ATOKEN", "expires_in": 3600}

    client.session.post.side_effect = [device_resp, token_pending, token_ok]

    monkeypatch.setattr("tmo.api_client.spin_it", lambda func, msg, speed: func())

    res = client._TmoClient__get_device_code()  # type: ignore
    assert isinstance(res, dict)
    assert res.get("access_token") == "ATOKEN"


def test_create_oauth_session_device_code_refreshes_with_refresh_token(
    mocker, tmp_path, monkeypatch
):
    client = make_client(mocker)
    client._TmoClient__client_id = "cid"
    client._TmoClient__client_secret = "secret"
    client._TmoClient__token_url = "https://token"
    client._TmoClient__device_auth_url = "https://device"
    client.ssl_verify = False

    token_path = tmp_path / ".token"
    expired = int(time.time()) - 3600
    token_file = {
        "expires_at": expired,
        "refresh_token": "RTOKEN",
        "access_token": "OLD",
    }
    token_path.write_text(json.dumps(token_file))
    client.DEFAULT_TOKEN_CACHE_FILE_PATH = str(token_path)

    class FakeOAuth2Session:
        def __init__(self, client_id=None):
            pass

        def refresh_token(
            self, token_url=None, refresh_token=None, auth=None, verify=None
        ):
            return {
                "access_token": "NEWAT",
                "expires_in": 3600,
                "refresh_token": "NEWRT",
            }

    monkeypatch.setattr("tmo.api_client.OAuth2Session", FakeOAuth2Session)
    monkeypatch.setattr("tmo.api_client.HTTPBasicAuth", lambda a, b: None)

    client._TmoClient__create_oauth_session_device_code()  # type: ignore

    assert client._TmoClient__bearer_token == "Bearer NEWAT"  # type: ignore


def test_get_device_code_authorization_declined_raises(mocker, monkeypatch):
    client = make_client(mocker)
    client._TmoClient__client_id = "cid"
    client._TmoClient__client_secret = None
    client._TmoClient__device_auth_url = "https://device"
    client._TmoClient__token_url = "https://token"
    client.session = mocker.Mock()

    device_resp = mocker.Mock()
    device_resp.status_code = 200
    device_resp.json.return_value = {
        "device_code": "DC",
        "user_code": "UC",
        "verification_uri_complete": "https://verify",
        "interval": 0,
    }

    token_declined = mocker.Mock()
    token_declined.status_code = 400
    token_declined.json.return_value = {
        "error": "authorization_declined",
        "error_description": "User declined authorization",
    }

    client.session.post.side_effect = [device_resp, token_declined]

    monkeypatch.setattr("tmo.api_client.spin_it", lambda func, msg, speed: func())

    from tmo.types.exceptions import AuthorizationError

    with pytest.raises(AuthorizationError) as exc:
        client._TmoClient__get_device_code()  # type: ignore
    assert "User declined authorization" in str(exc.value)


def test_get_device_code_bad_response_raises_authorization_error(mocker, monkeypatch):
    client = make_client(mocker)
    client._TmoClient__client_id = "cid"
    client._TmoClient__client_secret = None
    client._TmoClient__device_auth_url = "https://device"
    client._TmoClient__token_url = "https://token"
    client.session = mocker.Mock()

    device_resp = mocker.Mock()
    device_resp.status_code = 200
    device_resp.json.return_value = {
        "device_code": "DC",
        "user_code": "UC",
        "verification_uri_complete": "https://verify",
        "interval": 0,
    }

    token_bad = mocker.Mock()
    token_bad.status_code = 500
    token_bad.json.return_value = {}

    client.session.post.side_effect = [device_resp, token_bad]

    monkeypatch.setattr("tmo.api_client.spin_it", lambda func, msg, speed: func())

    from tmo.types.exceptions import AuthorizationError

    with pytest.raises(AuthorizationError) as exc:
        client._TmoClient__get_device_code()  # type: ignore
    assert "Bad response code 500" in str(exc.value)


def test_get_device_code_slow_down_calls_sleep_then_succeeds(mocker, monkeypatch):
    client = make_client(mocker)
    client._TmoClient__client_id = "cid"
    client._TmoClient__client_secret = None
    client._TmoClient__device_auth_url = "https://device"
    client._TmoClient__token_url = "https://token"
    client.session = mocker.Mock()

    device_resp = mocker.Mock()
    device_resp.status_code = 200
    device_resp.json.return_value = {
        "device_code": "DC",
        "user_code": "UC",
        "verification_uri_complete": "https://verify",
        "interval": 2,
    }

    token_slow = mocker.Mock()
    token_slow.status_code = 400
    token_slow.json.return_value = {"error": "slow_down"}

    token_ok = mocker.Mock()
    token_ok.status_code = 200
    token_ok.json.return_value = {"access_token": "ATOKEN", "expires_in": 3600}

    client.session.post.side_effect = [device_resp, token_slow, token_ok]

    sleep_mock = mocker.patch("tmo.api_client.time.sleep")
    monkeypatch.setattr("tmo.api_client.spin_it", lambda func, msg, speed: func())

    res = client._TmoClient__get_device_code()
    assert isinstance(res, dict)
    assert res.get("access_token") == "ATOKEN"
    sleep_mock.assert_called()
