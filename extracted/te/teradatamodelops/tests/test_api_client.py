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

        def json(self):  # noqa
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
    mock_exists = mocker.patch("os.path.exists", return_value=False)  # noqa
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
        def find_by_id(self, project_id):  # noqa
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

        def json(self):  # noqa
            return {}

    with pytest.raises(requests.exceptions.HTTPError) as exc:
        client._TmoClient__validate_and_extract_body(Resp())  # type: ignore
    assert "original" in str(exc.value)


def test_validate_and_extract_body_json_error_returns_text(mocker):
    client = make_client(mocker)

    class Resp:
        status_code = 200
        text = "plain text"

        def raise_for_status(self):  # noqa
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
        def cadata_from_url(self, url):  # noqa
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
        def cadata_from_url(self, url):  # noqa
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

    def fake_create(self):  # noqa
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

    def fake_create(self):  # noqa
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
    mock_validate = mocker.patch.object(  # noqa
        TmoClient, "_TmoClient__validate_stored_token"
    )
    mock_validate_and_extract = mocker.patch.object(  # noqa
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
        def find_by_id(self, project_id, expand=None):  # noqa
            return {"id": project_id, "name": "P", "_links": {}, "userAttributes": {}}

    mocker.patch.object(client, "projects", return_value=FakeProjects())
    df = client.describe_current_project()
    assert isinstance(df, pd.DataFrame)
    assert "attribute" in df.columns and "value" in df.columns  # noqa


def test_describe_current_project_returns_none_when_no_project_or_not_found(mocker):
    client = make_client(mocker)
    client.project_id = None
    assert client.describe_current_project() is None
    client.project_id = "p"

    class FakeProjects2:
        def find_by_id(self, project_id, expand=None):  # noqa
            return None

    mocker.patch.object(client, "projects", return_value=FakeProjects2())
    assert client.describe_current_project() is None


def test_get_default_connection_id_variants(mocker):
    client = make_client(mocker)

    class UA:
        def get_default_connection(self):  # noqa
            return {"value": {"defaultDatasetConnectionId": "cid123"}}

    mocker.patch.object(client, "user_attributes", return_value=UA())
    assert client.get_default_connection_id() == "cid123"

    class UA2:
        def get_default_connection(self):  # noqa
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
        def __init__(self, client_id=None):  # noqa
            pass

        def refresh_token(  # noqa
            self, token_url=None, refresh_token=None, auth=None, verify=None  # noqa
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

    res = client._TmoClient__get_device_code()  # noqa
    assert isinstance(res, dict)
    assert res.get("access_token") == "ATOKEN"
    sleep_mock.assert_called()


class TestRenametmoConfig:
    """Tests for __rename_tmo_config method."""

    def test_rename_tmo_config_renames_and_converts_aoa_keys(self, mocker, tmp_path):
        """Test that old config is renamed and aoa_ keys are converted to tmo_."""
        client = make_client(mocker)

        old_config_dir = tmp_path / ".aoa"
        new_config_dir = tmp_path / ".tmo"
        old_config_dir.mkdir()

        old_config_path = old_config_dir / "config.yaml"
        new_config_path = new_config_dir / "config.yaml"

        # Create old config with aoa_ prefixes
        import yaml

        old_config = {
            "aoa_url": "https://old.url",
            "aoa_auth_mode": "pat",
            "other_key": "value",
        }
        with open(old_config_path, "w") as f:
            yaml.safe_dump(old_config, f)

        # Override paths
        client.DEFAULT_OLD_CONFIG_FILE_PATH = str(old_config_path)
        client.DEFAULT_CONFIG_FILE_PATH = str(new_config_path)

        # Ensure new config dir exists
        new_config_dir.mkdir(exist_ok=True)

        client._TmoClient__rename_tmo_config()  # noqa

        # Verify file was renamed
        assert not old_config_path.exists()
        assert new_config_path.exists()

        # Verify content was converted
        with open(new_config_path, "r") as f:
            new_config = yaml.safe_load(f)

        assert "vmo_url" in new_config
        assert new_config["vmo_url"] == "https://old.url"
        assert "aoa_url" not in new_config
        assert "tmo_auth_mode" in new_config
        assert new_config["tmo_auth_mode"] == "pat"
        assert "aoa_auth_mode" not in new_config

    def test_rename_tmo_config_does_nothing_when_old_config_missing(
        self, mocker, tmp_path
    ):
        """Test that method does nothing when old config doesn't exist."""
        client = make_client(mocker)

        old_config_path = tmp_path / ".aoa" / "config.yaml"
        client.DEFAULT_OLD_CONFIG_FILE_PATH = str(old_config_path)

        # Should not raise
        client._TmoClient__rename_tmo_config()  # noqa


class TestParseTmoConfig:
    """Tests for __parse_tmo_config method."""

    def test_parse_tmo_config_uses_config_file_when_provided(self, mocker, tmp_path):
        """Test that config_file parameter is used when provided."""
        client = make_client(mocker)

        config_file = tmp_path / "custom_config.yaml"
        import yaml

        config = {"vmo_url": "https://custom.url", "auth_mode": "bearer"}
        with open(config_file, "w") as f:
            yaml.safe_dump(config, f)

        mock_parse_yaml = mocker.patch.object(client, "_TmoClient__parse_yaml")
        mock_parse_env = mocker.patch.object(client, "_TmoClient__parse_env_variables")
        mock_parse_kwargs = mocker.patch.object(client, "_TmoClient__parse_kwargs")

        client._TmoClient__parse_tmo_config(config_file=str(config_file))  # noqa

        mock_parse_yaml.assert_called_once_with(str(config_file))
        mock_parse_env.assert_called_once()
        mock_parse_kwargs.assert_called_once()

    def test_parse_tmo_config_uses_default_when_exists(self, mocker, tmp_path):
        """Test that default config file is used when it exists."""
        client = make_client(mocker)

        config_file = tmp_path / "config.yaml"
        import yaml

        with open(config_file, "w") as f:
            yaml.safe_dump({"vmo_url": "https://default.url"}, f)

        client.DEFAULT_CONFIG_FILE_PATH = str(config_file)

        mock_parse_yaml = mocker.patch.object(client, "_TmoClient__parse_yaml")
        mock_parse_env = mocker.patch.object(  # noqa
            client, "_TmoClient__parse_env_variables"
        )
        mock_parse_kwargs = mocker.patch.object(  # noqa
            client, "_TmoClient__parse_kwargs"
        )

        client._TmoClient__parse_tmo_config()  # noqa

        mock_parse_yaml.assert_called_once_with(str(config_file))


class TestParseEnvVariablesDeviceCode:
    """Tests for __parse_env_variables with device_code auth mode."""

    def test_parse_env_variables_device_code_sets_all_params(self, mocker, monkeypatch):
        """Test that all device_code parameters are set from env vars."""
        client = make_client(mocker)
        client.auth_mode = "device_code"

        # Set all env vars including VMO_API_AUTH_MODE to ensure auth_mode stays device_code
        monkeypatch.setenv("VMO_API_AUTH_MODE", "device_code")
        monkeypatch.setenv("VMO_API_AUTH_CLIENT_ID", "env_client_id")
        monkeypatch.setenv("VMO_API_AUTH_CLIENT_SECRET", "env_secret")
        monkeypatch.setenv("VMO_API_AUTH_TOKEN_URL", "https://env.token")
        monkeypatch.setenv("VMO_API_AUTH_DEVICE_AUTH_URL", "https://env.device")

        client._TmoClient__parse_env_variables()  # noqa

        assert client._TmoClient__client_id == "env_client_id"  # noqa
        assert client._TmoClient__client_secret == "env_secret"  # noqa
        assert client._TmoClient__token_url == "https://env.token"  # noqa
        assert client._TmoClient__device_auth_url == "https://env.device"  # noqa


class TestParseEnvVariablesPat:
    """Tests for __parse_env_variables with PAT auth mode."""

    def test_parse_env_variables_pat_sets_user_and_pat(self, mocker, monkeypatch):
        """Test that PAT parameters are set from env vars."""
        client = make_client(mocker)
        client.auth_mode = "pat"

        monkeypatch.setenv("VMO_API_AUTH_MODE", "pat")  # Ensure auth_mode is set to pat
        monkeypatch.setenv("VMO_API_USER", "env_user")
        monkeypatch.setenv("VMO_API_PAT", "env_pat_value")

        client._TmoClient__parse_env_variables()  # noqa

        assert client._TmoClient__user == "env_user"  # noqa
        assert client._TmoClient__pat == "env_pat_value"  # noqa


class TestParseEnvVariablesBearer:
    """Tests for __parse_env_variables with bearer auth mode."""

    def test_parse_env_variables_bearer_sets_token(self, mocker, monkeypatch):
        """Test that bearer token is set from env vars."""
        client = make_client(mocker)
        client.auth_mode = "bearer"

        monkeypatch.setenv(
            "VMO_API_AUTH_MODE", "bearer"
        )  # Ensure auth_mode is set to bearer
        monkeypatch.setenv("VMO_API_AUTH_BEARER_TOKEN", "env_bearer_token")

        client._TmoClient__parse_env_variables()  # noqa

        assert client._TmoClient__bearer_token == "env_bearer_token"  # noqa


class TestParseKwargsVerifyConnection:
    """Tests for __parse_kwargs with verify_connection parameter."""

    def test_parse_kwargs_sets_verify_connection_when_provided(self, mocker):
        """Test that verify_connection is set when provided in kwargs."""
        client = make_client(mocker)

        client._TmoClient__parse_kwargs(verify_connection=False)  # noqa

        assert hasattr(client, "verify_tmo_connection")
        assert client.verify_tmo_connection is False


class TestCreateOauthSessionDeviceCodeEdgeCases:
    """Additional tests for __create_oauth_session_device_code edge cases."""

    def test_create_oauth_session_no_token_file_calls_get_device_code(
        self, mocker, tmp_path
    ):
        """Test that when no cached token exists, __get_device_code is called."""
        client = make_client(mocker)
        client._TmoClient__client_id = "cid"
        client._TmoClient__client_secret = "secret"
        client._TmoClient__token_url = "https://token"
        client._TmoClient__device_auth_url = "https://device"
        client.ssl_verify = True

        # Set token path to non-existent file
        client.DEFAULT_TOKEN_CACHE_FILE_PATH = str(tmp_path / "nonexistent.token")

        mock_get_device = mocker.patch.object(
            client,
            "_TmoClient__get_device_code",
            return_value={"access_token": "AT", "expires_at": int(time.time()) + 3600},
        )
        mock_save = mocker.patch.object(client, "_TmoClient__save_oauth_token")
        mock_set_tls = mocker.patch.object(  # noqa
            client, "_TmoClient__set_session_tls"
        )
        mock_bearer = mocker.patch.object(  # noqa
            client, "_TmoClient__create_oauth_session_bearer"
        )

        client._TmoClient__create_oauth_session_device_code()  # noqa

        mock_get_device.assert_called_once()
        mock_save.assert_called_once()

    def test_create_oauth_session_token_without_expires_at_calculates_expiry(
        self, mocker, tmp_path
    ):
        """Test handling token with expires_in but no expires_at."""
        client = make_client(mocker)
        client._TmoClient__client_id = "cid"
        client._TmoClient__token_url = "https://token.url"  # Required
        client._TmoClient__device_auth_url = "https://device.url"  # Required
        client.ssl_verify = True

        token_file = tmp_path / ".token"
        # Token with expires_in but no expires_at, and expires soon
        current_time = int(time.time())
        token_data = {
            "access_token": "AT",
            "refresh_token": "RT",
            "expires_in": 30,  # Expires in 30 seconds (< REFRESH_BEFORE_EXPIRES=60)
        }
        with open(token_file, "w") as f:
            json.dump(token_data, f)

        client.DEFAULT_TOKEN_CACHE_FILE_PATH = str(token_file)

        # Mock the refresh call
        mock_session = mocker.Mock()
        mock_session.refresh_token.return_value = {
            "access_token": "NEW_AT",
            "expires_at": current_time + 3600,
        }
        mocker.patch("tmo.api_client.OAuth2Session", return_value=mock_session)

        mock_save = mocker.patch.object(client, "_TmoClient__save_oauth_token")  # noqa
        mock_set_tls = mocker.patch.object(  # noqa
            client, "_TmoClient__set_session_tls"
        )
        mock_bearer = mocker.patch.object(  # noqa
            client, "_TmoClient__create_oauth_session_bearer"
        )

        client._TmoClient__create_oauth_session_device_code()  # noqa

        # Should call refresh because token is expiring
        mock_session.refresh_token.assert_called_once()

    def test_create_oauth_session_token_with_access_but_no_refresh_creates_session(
        self, mocker, tmp_path
    ):
        """Test handling token with access_token but no refresh_token and not expired."""
        client = make_client(mocker)
        client._TmoClient__client_id = "cid"
        client._TmoClient__token_url = "https://token.url"  # Required
        client._TmoClient__device_auth_url = "https://device.url"  # Required
        client.ssl_verify = True

        token_file = tmp_path / ".token"
        current_time = int(time.time())
        # Token without refresh_token but not expired
        token_data = {
            "access_token": "AT",
            "expires_at": current_time + 3600,  # Valid for 1 hour
        }
        with open(token_file, "w") as f:
            json.dump(token_data, f)

        client.DEFAULT_TOKEN_CACHE_FILE_PATH = str(token_file)

        mock_session = mocker.Mock()
        mocker.patch("tmo.api_client.OAuth2Session", return_value=mock_session)

        mock_save = mocker.patch.object(client, "_TmoClient__save_oauth_token")  # noqa
        mock_set_tls = mocker.patch.object(  # noqa
            client, "_TmoClient__set_session_tls"
        )
        mock_bearer = mocker.patch.object(  # noqa
            client, "_TmoClient__create_oauth_session_bearer"
        )

        client._TmoClient__create_oauth_session_device_code()  # noqa

        # Should create OAuth session without refresh
        assert client.session == mock_session

    def test_create_oauth_session_token_missing_required_fields_raises(
        self, mocker, tmp_path
    ):
        """Test that token without access_token or refresh_token raises ValueError."""
        client = make_client(mocker)
        client._TmoClient__client_id = "cid"
        client._TmoClient__token_url = "https://token.url"  # Required
        client._TmoClient__device_auth_url = "https://device.url"  # Required

        token_file = tmp_path / ".token"
        # Invalid token - missing both access_token and refresh_token
        token_data = {"expires_at": int(time.time()) + 3600}
        with open(token_file, "w") as f:
            json.dump(token_data, f)

        client.DEFAULT_TOKEN_CACHE_FILE_PATH = str(token_file)

        with pytest.raises(
            ValueError, match="Token does not contain access_token or refresh_token"
        ):
            client._TmoClient__create_oauth_session_device_code()  # noqa

    def test_create_oauth_session_session_already_exists_preserves_verify(
        self, mocker, tmp_path
    ):
        """Test that when session exists, verify setting is preserved."""
        client = make_client(mocker)
        client._TmoClient__client_id = "cid"
        client._TmoClient__token_url = "https://token.url"  # Required
        client._TmoClient__device_auth_url = "https://device.url"  # Required

        token_file = tmp_path / ".token"
        token_data = {"access_token": "AT", "expires_at": int(time.time()) + 3600}
        with open(token_file, "w") as f:
            json.dump(token_data, f)

        client.DEFAULT_TOKEN_CACHE_FILE_PATH = str(token_file)

        # Create existing session with custom verify setting
        existing_session = mocker.Mock()
        existing_session.verify = "/custom/ca/bundle.pem"
        client.session = existing_session

        mock_new_session = mocker.Mock()
        mocker.patch("tmo.api_client.OAuth2Session", return_value=mock_new_session)

        mock_save = mocker.patch.object(client, "_TmoClient__save_oauth_token")  # noqa
        mock_bearer = mocker.patch.object(  # noqa
            client, "_TmoClient__create_oauth_session_bearer"
        )

        client._TmoClient__create_oauth_session_device_code()  # noqa

        # New session should preserve verify from old session
        assert mock_new_session.verify == "/custom/ca/bundle.pem"


class TestSaveOauthToken:
    """Tests for __save_oauth_token method."""

    def test_save_oauth_token_adds_expires_at_when_missing(self, mocker, tmp_path):
        """Test that expires_at is calculated from expires_in when missing."""
        client = make_client(mocker)

        token_file = tmp_path / ".token"
        client.DEFAULT_TOKEN_CACHE_FILE_PATH = str(token_file)

        current_time = int(time.time())
        token = {"access_token": "AT", "expires_in": 3600}

        mocker.patch("tmo.api_client.time.time", return_value=current_time)

        client._TmoClient__save_oauth_token(token)  # noqa

        # Verify file was written with expires_at
        with open(token_file, "r") as f:
            saved = json.load(f)

        assert "expires_at" in saved
        assert saved["expires_at"] == current_time + 3600
        assert client._TmoClient__bearer_token == "Bearer AT"  # noqa

    def test_save_oauth_token_handles_write_failure(self, mocker, tmp_path, caplog):
        """Test that write failures are logged as errors."""
        client = make_client(mocker)

        # Use real logger instead of mock to capture logs
        import logging

        client.logger = logging.getLogger("tmo.api_client")

        # Set to a path that will fail (directory instead of file)
        bad_path = tmp_path / "dir_not_file"
        bad_path.mkdir()
        client.DEFAULT_TOKEN_CACHE_FILE_PATH = str(bad_path)

        token = {"access_token": "AT", "expires_in": 3600}

        client._TmoClient__save_oauth_token(token)  # noqa

        # Should log error
        assert any(
            "Failed to save OAuth token" in record.message for record in caplog.records
        )


class TestValidateStoredTokenEdgeCases:
    """Additional edge case tests for __validate_stored_token."""

    def test_validate_stored_token_creates_session_when_missing(self, mocker, tmp_path):
        """Test that session is created when it doesn't exist."""
        client = make_client(mocker)
        client._TmoClient__pat = "PAT"
        client._TmoClient__user = "user"

        # No cached token
        client.DEFAULT_TOKEN_CACHE_FILE_PATH = str(tmp_path / "nonexistent.token")

        mock_create_jwt = mocker.patch.object(  # noqa
            client, "_TmoClient__create_self_signed_jwt", return_value="NEW_JWT"
        )
        mock_set_tls = mocker.patch.object(client, "_TmoClient__set_session_tls")

        # Ensure client doesn't have session
        if hasattr(client, "session"):
            delattr(client, "session")

        mock_session_class = mocker.patch("tmo.api_client.requests.Session")
        mock_session_instance = mocker.Mock()
        mock_session_class.return_value = mock_session_instance

        client._TmoClient__validate_stored_token()  # noqa

        # Should create new session
        mock_session_class.assert_called_once()
        mock_set_tls.assert_called_once()
        assert mock_session_instance.headers.update.called


class TestChaseTypoCertChainEdgeCases:
    """Additional tests for __chase_tls_cert_chain."""

    def test_chase_tls_with_invalid_vmo_url_raises(self, mocker, monkeypatch):
        """Test that invalid vmo_url raises ConfigurationError."""
        client = make_client(mocker)
        # Use https URL that will fail the regex check inside the try block
        # The regex checks for "http|https" which should match, but we'll mock it to not match
        client.vmo_url = "https://invalid.url"
        client.session = mocker.Mock()

        # Ensure no CA bundle env vars (so code enters the chase block)
        monkeypatch.delenv("REQUESTS_CA_BUNDLE", raising=False)
        monkeypatch.delenv("CURL_CA_BUNDLE", raising=False)

        # Mock requests.get to NOT raise SSLError (so we reach the regex check)
        mock_get = mocker.patch("tmo.api_client.requests.get")
        mock_get.return_value = mocker.Mock(status_code=200)

        # Mock re.search to return None (simulating URL not matching http|https)
        mocker.patch("tmo.api_client.re.search", return_value=None)

        from tmo.types.exceptions import ConfigurationError

        with pytest.raises(ConfigurationError):
            client._TmoClient__chase_tls_cert_chain()  # noqa

    def test_chase_tls_with_ca_bundle_set_skips_chase(self, mocker, monkeypatch):
        """Test that cert chasing is skipped when CA bundle is set."""
        client = make_client(mocker)
        client.vmo_url = "https://example.com"
        client.session = mocker.Mock()

        monkeypatch.setenv("REQUESTS_CA_BUNDLE", "/path/to/bundle.pem")

        # Should not raise or attempt AIA
        client._TmoClient__chase_tls_cert_chain()  # noqa


class TestGetDeviceCodeEdgeCases:
    """Additional edge cases for __get_device_code."""

    def test_get_device_code_with_client_secret_includes_in_request(
        self, mocker, monkeypatch
    ):
        """Test that client_secret is included in request when present."""
        client = make_client(mocker)
        client._TmoClient__client_id = "cid"
        client._TmoClient__client_secret = "secret"
        client._TmoClient__device_auth_url = "https://device"
        client._TmoClient__token_url = "https://token"
        client.session = mocker.Mock()

        device_resp = mocker.Mock()
        device_resp.status_code = 200
        device_resp.json.return_value = {
            "device_code": "DC",
            "user_code": "UC",
            "verification_uri_complete": "https://verify",
            "interval": 1,
        }

        token_resp = mocker.Mock()
        token_resp.status_code = 200
        token_resp.json.return_value = {"access_token": "AT", "expires_in": 3600}

        client.session.post.side_effect = [device_resp, token_resp]

        monkeypatch.setattr("tmo.api_client.spin_it", lambda func, msg, speed: func())

        result = client._TmoClient__get_device_code()  # noqa

        # Verify device code request included client_secret
        first_call_data = client.session.post.call_args_list[0][1]["data"]
        assert "client_secret" in first_call_data
        assert first_call_data["client_secret"] == "secret"


class TestInitProjectId:
    """Tests for project_id initialization in __init__."""

    def test_init_without_project_id_sets_none(self, mocker, monkeypatch):
        """Test that project_id is None when not provided."""
        # Mock all auth setup
        mocker.patch.object(TmoClient, "_TmoClient__rename_tmo_config")

        # Mock __parse_tmo_config to set auth_mode so __init__ doesn't raise
        def mock_parse_config(self, **kwargs):  # noqa
            self.auth_mode = "bearer"
            self.vmo_url = "https://test.url"

        mocker.patch.object(
            TmoClient, "_TmoClient__parse_tmo_config", mock_parse_config
        )
        mocker.patch.object(TmoClient, "_TmoClient__create_oauth_session_bearer")

        monkeypatch.setenv("VMO_URL", "https://test.url")
        monkeypatch.setenv("VMO_API_AUTH_MODE", "bearer")
        monkeypatch.setenv("VMO_API_AUTH_BEARER_TOKEN", "token")

        client = TmoClient()

        assert client.project_id is None


class TestValidateAndExtractBodyEdgeCases:
    """Additional edge cases for __validate_and_extract_body."""

    def test_validate_and_extract_body_returns_text_when_no_json(self, mocker):
        """Test that text is returned when response is not JSON."""
        client = make_client(mocker)

        resp = mocker.Mock()
        resp.status_code = 200
        resp.raise_for_status.return_value = None
        resp.json.side_effect = ValueError("Not JSON")
        resp.text = "plain text response"

        result = client._TmoClient__validate_and_extract_body(resp)  # noqa

        assert result == "plain text response"

    def test_validate_and_extract_body_raises_http_error_without_text(self, mocker):
        """Test that HTTPError is raised without text modification when resp.text is empty."""
        client = make_client(mocker)

        resp = mocker.Mock()
        resp.status_code = 500
        resp.text = ""
        original_error = requests.exceptions.HTTPError("original error")
        resp.raise_for_status.side_effect = original_error

        with pytest.raises(requests.exceptions.HTTPError) as exc:
            client._TmoClient__validate_and_extract_body(resp)  # noqa

        # Should raise original error when no text
        assert "original error" in str(exc.value)


class TestAoaClientDeprecation:
    """Tests for deprecated AoaClient class."""

    def test_aoa_client_shows_deprecation_warning(self, monkeypatch):
        """Test that AoaClient raises DeprecationWarning."""
        from tmo.api_client import AoaClient  # noqa

        # Mock to avoid actual initialization
        monkeypatch.setattr(TmoClient, "__init__", lambda self, **kw: None)  # noqa

        with pytest.warns(DeprecationWarning, match="AoaClient is deprecated"):
            client = AoaClient()  # noqa


class TestApiWrapperMethods:
    """Tests for API wrapper methods that return specific API clients."""

    def test_all_api_methods_return_correct_types(self, mocker):
        """Test that all API wrapper methods return the expected API types."""
        client = make_client(mocker)
        client.project_id = "proj-id"

        # Import all API types
        from tmo import (
            ProjectApi,
            DatasetApi,
            DatasetTemplateApi,
            DatasetConnectionApi,
            DeploymentApi,
            FeatureEngineeringApi,
            JobApi,
            JobEventApi,
            MessageApi,
            ModelApi,
            TrainedModelApi,
            TrainedModelArtefactsApi,
            TrainedModelEventApi,
            UserAttributesApi,
        )

        assert isinstance(client.projects(), ProjectApi)
        assert isinstance(client.datasets(), DatasetApi)
        assert isinstance(client.dataset_templates(), DatasetTemplateApi)
        assert isinstance(client.dataset_connections(), DatasetConnectionApi)
        assert isinstance(client.deployments(), DeploymentApi)
        assert isinstance(client.feature_engineering(), FeatureEngineeringApi)
        assert isinstance(client.jobs(), JobApi)
        assert isinstance(client.job_events(), JobEventApi)
        assert isinstance(client.messages(), MessageApi)
        assert isinstance(client.models(), ModelApi)
        assert isinstance(client.trained_models(), TrainedModelApi)
        assert isinstance(client.trained_model_artefacts(), TrainedModelArtefactsApi)
        assert isinstance(client.trained_model_events(), TrainedModelEventApi)
        assert isinstance(client.user_attributes(), UserAttributesApi)


class TestDescribeCurrentProjectEdgeCases:
    """Additional tests for describe_current_project."""

    def test_describe_current_project_filters_links_and_user_attributes(self, mocker):
        """Test that _links and userAttributes are excluded from output."""
        client = make_client(mocker)
        client.project_id = "proj-123"

        mock_projects = mocker.Mock()
        mock_projects.find_by_id.return_value = {
            "id": "proj-123",
            "name": "Test Project",
            "_links": {"self": "url"},
            "userAttributes": {"key": "value"},
            "description": "A project",
        }
        mocker.patch.object(client, "projects", return_value=mock_projects)

        result = client.describe_current_project()

        # Should return DataFrame
        assert isinstance(result, pd.DataFrame)
        # Should have filtered out _links and userAttributes
        attrs = result["attribute"].tolist()  # noqa
        assert "_links" not in attrs
        assert "userAttributes" not in attrs
        assert "id" in attrs
        assert "name" in attrs


class TestGetDefaultConnectionIdEdgeCases:
    """Additional tests for get_default_connection_id."""

    def test_get_default_connection_id_returns_none_on_exception(self, mocker):
        """Test that exceptions are caught and None is returned."""
        client = make_client(mocker)

        mock_user_attrs = mocker.Mock()
        mock_user_attrs.get_default_connection.side_effect = Exception("DB error")
        mocker.patch.object(client, "user_attributes", return_value=mock_user_attrs)

        result = client.get_default_connection_id()

        assert result is None

    def test_get_default_connection_id_returns_none_when_no_connection(self, mocker):
        """Test that None is returned when get_default_connection returns None."""
        client = make_client(mocker)

        mock_user_attrs = mocker.Mock()
        mock_user_attrs.get_default_connection.return_value = None
        mocker.patch.object(client, "user_attributes", return_value=mock_user_attrs)

        result = client.get_default_connection_id()

        assert result is None


class TestSaveSignedJwt:
    """Tests for __save_signed_jwt method."""

    def test_save_signed_jwt_creates_directory_and_saves(self, mocker, tmp_path):
        """Test that directory is created and JWT is saved."""
        client = make_client(mocker)

        token_dir = tmp_path / "subdir" / "nested"
        token_file = token_dir / ".token"
        client.DEFAULT_TOKEN_CACHE_FILE_PATH = str(token_file)

        exp = int(time.time()) + 3600

        client._TmoClient__save_signed_jwt("SIGNED_JWT", exp)  # noqa

        # Directory should be created
        assert token_dir.exists()

        # Token should be saved
        assert token_file.exists()
        with open(token_file, "r") as f:
            saved = json.load(f)

        assert saved["token"] == "SIGNED_JWT"
        assert saved["exp"] == exp

    def test_save_signed_jwt_handles_exception_and_logs(self, mocker, caplog):
        """Test that exceptions during save are logged."""
        client = make_client(mocker)

        # Use real logger instead of mock to capture logs
        import logging

        client.logger = logging.getLogger("tmo.api_client")

        # Use invalid path that will fail
        client.DEFAULT_TOKEN_CACHE_FILE_PATH = "/invalid/path/that/cannot/exist/.token"

        client._TmoClient__save_signed_jwt("JWT", 12345)  # noqa

        # Should log error
        assert any("Failed to save" in record.message for record in caplog.records)


class TestChaseTypoCertChainInvalidCA:
    """Test for AIA InvalidCAError handling."""

    def test_chase_tls_raises_ssl_error_on_invalid_ca(self, mocker, monkeypatch):
        """Test that InvalidCAError from AIA is caught and SSLError is raised."""
        client = make_client(mocker)
        client.vmo_url = "https://example.com"
        client.session = mocker.Mock()

        # Ensure no CA bundle env vars
        monkeypatch.delenv("REQUESTS_CA_BUNDLE", raising=False)
        monkeypatch.delenv("CURL_CA_BUNDLE", raising=False)

        # Mock requests.get to raise SSLError
        mock_get = mocker.patch("tmo.api_client.requests.get")
        mock_get.side_effect = requests.exceptions.SSLError()

        # Mock AIASession to raise InvalidCAError
        mock_aia = mocker.Mock()
        mock_aia.cadata_from_url.side_effect = aia.InvalidCAError("No trusted root")
        mocker.patch("aia.AIASession", return_value=mock_aia)

        with pytest.raises(
            requests.exceptions.SSLError, match="Attempted to find trusted root"
        ):
            client._TmoClient__chase_tls_cert_chain()  # noqa


class TestSetSessionTlsCalledFromTest:
    """Test for __set_session_tls when CALLED_FROM_TEST is true."""

    def test_set_session_tls_skips_warning_when_called_from_test(
        self, mocker, monkeypatch, caplog
    ):
        """Test that warning is skipped when CALLED_FROM_TEST=true."""
        client = make_client(mocker)
        client.session = mocker.Mock()
        client.ssl_verify = False

        monkeypatch.setenv("CALLED_FROM_TEST", "true")

        mocker.patch("tmo.api_client.requests.packages.urllib3.disable_warnings")

        client._TmoClient__set_session_tls()  # noqa

        # Warning should not be logged
        assert not any(
            "Certificate validation disabled" in record.message
            for record in caplog.records
        )


class TestCreateSelfSignedJwtOrgIdExtraction:
    """Tests for org_id extraction in __create_self_signed_jwt."""

    def test_create_self_signed_jwt_extracts_org_from_url(self, mocker, tmp_path):
        """Test that org_id is correctly extracted from vmo_url."""
        client = make_client(mocker)
        client.vmo_url = "https://myorg.example.com/path"
        client._TmoClient__pat = "PAT"
        client._TmoClient__user = "user"

        pk_path = tmp_path / "pat.pem"
        pk_path.write_text("PRIVATE_KEY")
        client.DEFAULT_PAT_PRIVATE_KEY_PATH = str(pk_path)

        captured_payload = {}

        def mock_encode(payload, key, algorithm, headers):  # noqa
            captured_payload.update(payload)
            return "JWT"

        mocker.patch("tmo.api_client.jwt.encode", side_effect=mock_encode)
        mocker.patch.object(client, "_TmoClient__save_signed_jwt")

        client._TmoClient__create_self_signed_jwt()  # noqa

        # Verify org_id was extracted correctly
        assert captured_payload["org_id"] == "myorg"
        assert captured_payload["sub"] == "user"
        assert captured_payload["pat"] == "PAT"
