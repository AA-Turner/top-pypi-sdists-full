"""Tests for testmu_selenium._helpers.execute_db — sync DB query helper."""
import base64
from unittest.mock import MagicMock, patch

import pytest

from testmu_selenium._helpers.execute_db import execute_db


def _mock_response(status=200, json_body=None, text=""):
    resp = MagicMock()
    resp.status_code = status
    resp.json.return_value = json_body if json_body is not None else {}
    resp.text = text
    return resp


def test_execute_db_returns_query_result():
    fake_resp = _mock_response(status=200, json_body={"rows": [{"id": 1}], "row_count": 1})
    with patch("requests.post", return_value=fake_resp):
        result = execute_db(
            query="c2VsZWN0IDE=",
            db_id="db-1",
            db_name="orders",
            auth_header="dXNlcjpwYXNz",
            automind_url="https://automind.example.com",
        )
    assert result["row_count"] == 1


def test_execute_db_raises_on_non_200():
    fake_resp = _mock_response(status=500, text="boom")
    with patch("requests.post", return_value=fake_resp):
        with pytest.raises(RuntimeError, match="500"):
            execute_db(
                query="c2VsZWN0IDE=",
                db_id="db-1",
                auth_header="dXNlcjpwYXNz",
                automind_url="https://automind.example.com",
            )


def test_execute_db_builds_auth_header_from_lt_creds_env(monkeypatch):
    """When the caller passes an empty auth_header but LT_USERNAME/LT_ACCESS_KEY
    are present in the environment, execute_db builds the Basic header from those
    creds instead of raising. This mirrors the V2 db_query behavior and the
    Playwright bindings — the code generator always emits auth_header="" because
    credentials must not be baked into exported tests.
    """
    monkeypatch.setenv("LT_USERNAME", "user")
    monkeypatch.setenv("LT_ACCESS_KEY", "pass")
    captured = {}

    def _fake_post(url, json=None, headers=None, **kwargs):
        captured["headers"] = headers
        return _mock_response(status=200, json_body={"row_count": 0})

    with patch("requests.post", side_effect=_fake_post):
        result = execute_db(
            query="c2VsZWN0IDE=",
            db_id="db-1",
            db_name="orders",
            auth_header="",
            automind_url="https://automind.example.com",
        )

    expected = base64.b64encode(b"user:pass").decode()
    assert captured["headers"]["Authorization"] == f"Basic {expected}"
    assert result["row_count"] == 0


def test_execute_db_blank_url_honors_auteur_automind(monkeypatch):
    """When automind_url is blank, execute_db reads _config.get("automind_url").

    Inject the expected value directly into _config._config (auto-restored by
    monkeypatch).  The env resolution chain (AUTEUR_AUTOMIND > AUTOMIND_URL > prod)
    is tested in test_config_url_resolution.py; here we verify that the blank-url
    branch delegates to _config.get("automind_url").
    """
    import testmu_selenium._config as _config_mod

    monkeypatch.setitem(_config_mod._config, "automind_url", "https://auteur-automind.example.com")
    monkeypatch.setenv("LT_USERNAME", "user")
    monkeypatch.setenv("LT_ACCESS_KEY", "pass")
    captured = {}

    def _fake_post(url, json=None, headers=None, **kwargs):
        captured["url"] = url
        return _mock_response(status=200, json_body={"row_count": 0})

    with patch("requests.post", side_effect=_fake_post):
        execute_db(
            query="c2VsZWN0IDE=",
            db_id="db-1",
            db_name="orders",
            auth_header="",
            automind_url="",
        )

    assert captured["url"] == "https://auteur-automind.example.com/db-query"


def test_execute_db_requires_auth_header_when_no_creds(monkeypatch):
    """With no auth_header and no LT creds in the environment, there is no way to
    authenticate, so execute_db still raises."""
    monkeypatch.delenv("LT_USERNAME", raising=False)
    monkeypatch.delenv("LT_ACCESS_KEY", raising=False)
    with pytest.raises(RuntimeError, match="auth"):
        execute_db(
            query="c2VsZWN0IDE=",
            db_id="db-1",
            auth_header="",
            automind_url="https://automind.example.com",
        )


# ---------------------------------------------------------------------------
# Variable template resolution in the DB query (RED → GREEN)
# ---------------------------------------------------------------------------

def test_execute_db_resolves_template_in_query():
    """Base64-encoded query containing {{x}} must be decoded, resolved via var(),
    and re-encoded before being sent. The POSTed payload's 'query' field must
    contain the re-encoded resolved query, not the original template literal.

    Mirrors the V2 source (decode → resolve → re-encode).
    """
    from testmu_selenium._vars import set_var, clear_state
    clear_state()
    set_var("x", "abc")

    # Build a query that embeds the template: "SELECT * WHERE val = '{{x}}'"
    raw_query = "SELECT * WHERE val = '{{x}}'"
    encoded_query = base64.b64encode(raw_query.encode("utf-8")).decode("utf-8")

    captured = {}

    def _fake_post(url, json=None, headers=None, **kwargs):
        captured["payload"] = json
        return _mock_response(status=200, json_body={"row_count": 1})

    with patch("requests.post", side_effect=_fake_post):
        execute_db(
            query=encoded_query,
            db_id="db-1",
            auth_header="dXNlcjpwYXNz",
            automind_url="https://automind.example.com",
        )

    clear_state()

    assert "payload" in captured, "requests.post was not called"
    sent_query_b64 = captured["payload"]["query"]
    decoded_sent = base64.b64decode(sent_query_b64).decode("utf-8")
    assert decoded_sent == "SELECT * WHERE val = 'abc'", (
        f"Expected resolved query, got: {decoded_sent!r}"
    )


def test_execute_db_handles_invalid_base64_query_gracefully():
    """When the query is not valid base64, execute_db must not crash — it should
    leave the query unchanged and send it as-is."""
    from testmu_selenium._vars import clear_state
    clear_state()

    not_base64 = "this is not base64!@#$%"
    captured = {}

    def _fake_post(url, json=None, headers=None, **kwargs):
        captured["payload"] = json
        return _mock_response(status=200, json_body={"row_count": 0})

    with patch("requests.post", side_effect=_fake_post):
        execute_db(
            query=not_base64,
            db_id="db-1",
            auth_header="dXNlcjpwYXNz",
            automind_url="https://automind.example.com",
        )

    assert captured["payload"]["query"] == not_base64


def test_execute_db_resolves_dollar_template_in_query():
    """${name} templates in the decoded query must also be resolved."""
    from testmu_selenium._vars import set_var, clear_state, _test_params
    clear_state()
    _test_params["run_id"] = "run-42"

    raw_query = "SELECT * FROM runs WHERE id = '${run_id}'"
    encoded_query = base64.b64encode(raw_query.encode("utf-8")).decode("utf-8")

    captured = {}

    def _fake_post(url, json=None, headers=None, **kwargs):
        captured["payload"] = json
        return _mock_response(status=200, json_body={"row_count": 1})

    with patch("requests.post", side_effect=_fake_post):
        execute_db(
            query=encoded_query,
            db_id="db-1",
            auth_header="dXNlcjpwYXNz",
            automind_url="https://automind.example.com",
        )

    _test_params.clear()

    sent_query_b64 = captured["payload"]["query"]
    decoded_sent = base64.b64decode(sent_query_b64).decode("utf-8")
    assert decoded_sent == "SELECT * FROM runs WHERE id = 'run-42'", (
        f"Expected resolved query, got: {decoded_sent!r}"
    )
