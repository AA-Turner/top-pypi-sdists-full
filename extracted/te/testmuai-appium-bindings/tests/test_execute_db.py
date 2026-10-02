"""execute_db() — SQL query via the automind /db-query endpoint.

The wire contract is shared with the selenium and playwright siblings: base64 SQL
under "query", and Authorization: Basic <base64 user:key>.
"""
import base64
import json

import httpx
import pytest
import respx

from testmu_appium._helpers.execute_db import execute_db
from testmu_appium._vars import _variable_store, clear_state, set_var

_URL = "https://automind.example.test/db-query"


def _b64(text: str) -> str:
    return base64.b64encode(text.encode()).decode()


def _sent_query(route) -> str:
    """The decoded SQL the request actually carried."""
    encoded = json.loads(route.calls[0].request.content)["query"]
    return base64.b64decode(encoded).decode()


@pytest.fixture(autouse=True)
def _env(monkeypatch):
    monkeypatch.setenv("AUTOMIND_URL", "https://automind.example.test")
    monkeypatch.delenv("AUTEUR_AUTOMIND", raising=False)
    monkeypatch.delenv("LT_PROXY_TUNNEL_ID", raising=False)
    monkeypatch.setenv("LT_USERNAME", "u")
    monkeypatch.setenv("LT_ACCESS_KEY", "k")
    clear_state()
    yield
    clear_state()


@respx.mock
def test_returns_the_parsed_result():
    respx.post(_URL).mock(return_value=httpx.Response(200, json={"rows": [{"id": 1}]}))
    result = execute_db(query=_b64("SELECT * FROM widgets"))
    assert result == {"rows": [{"id": 1}]}


@respx.mock
def test_request_uses_basic_auth_from_lt_credentials():
    route = respx.post(_URL).mock(return_value=httpx.Response(200, json={}))
    execute_db(query=_b64("SELECT 1"))
    sent = route.calls[0].request
    assert sent.headers["authorization"] == f"Basic {base64.b64encode(b'u:k').decode()}"


@respx.mock
def test_payload_shape_matches_the_selenium_sibling():
    """Same path, same keys, and the SAME base64 query encoding — automind decodes
    the "query" field, so plaintext SQL arrives as something it cannot read."""
    route = respx.post(_URL).mock(return_value=httpx.Response(200, json={}))
    execute_db(
        query=_b64("SELECT 1"),
        db_id="db-1", db_name="prod", timeout=5000, tunnel_id="tun-1",
    )
    payload = json.loads(route.calls[0].request.content)
    assert payload == {
        "payload": {"id": "db-1", "timeout": 5000, "db_name": "prod", "tunnel_id": "tun-1"},
        "query": _b64("SELECT 1"),
    }


class TestQueryEncoding:
    """decode → resolve → re-encode, mirroring the siblings."""

    @respx.mock
    def test_the_query_stays_base64_on_the_wire(self):
        route = respx.post(_URL).mock(return_value=httpx.Response(200, json={}))
        execute_db(query=_b64("SELECT * FROM widgets"))
        assert json.loads(route.calls[0].request.content)["query"] == _b64(
            "SELECT * FROM widgets"
        )
        assert _sent_query(route) == "SELECT * FROM widgets"

    @respx.mock
    def test_variable_tokens_inside_the_encoded_sql_resolve(self):
        set_var("table", "widgets")
        route = respx.post(_URL).mock(return_value=httpx.Response(200, json={}))
        execute_db(query=_b64("SELECT * FROM {{table}}"))
        assert _sent_query(route) == "SELECT * FROM widgets"

    @respx.mock
    def test_test_param_tokens_inside_the_encoded_sql_resolve(self):
        from testmu_appium._vars import _test_params

        _test_params["env"] = "stage"
        route = respx.post(_URL).mock(return_value=httpx.Response(200, json={}))
        execute_db(query=_b64("SELECT * FROM t WHERE env = '${env}'"))
        assert _sent_query(route) == "SELECT * FROM t WHERE env = 'stage'"

    @respx.mock
    def test_a_query_that_is_not_base64_passes_through_untouched(self):
        """Mangling an uninterpretable payload into base64 would corrupt something
        automind might otherwise have understood."""
        route = respx.post(_URL).mock(return_value=httpx.Response(200, json={}))
        execute_db(query="SELECT * FROM widgets")
        assert json.loads(route.calls[0].request.content)["query"] == (
            "SELECT * FROM widgets"
        )


class TestAuth:
    @respx.mock
    def test_an_explicit_auth_header_is_sent_with_the_basic_prefix(self):
        """auth_header is the base64 CREDENTIAL, not a full header value — the
        siblings both send it as `Basic <auth_header>`."""
        route = respx.post(_URL).mock(return_value=httpx.Response(200, json={}))
        execute_db(query=_b64("SELECT 1"), auth_header="Y3VzdG9tOmNyZWQ=")
        assert route.calls[0].request.headers["authorization"] == "Basic Y3VzdG9tOmNyZWQ="

    @respx.mock
    def test_an_explicit_auth_header_wins_over_lt_credentials(self):
        route = respx.post(_URL).mock(return_value=httpx.Response(200, json={}))
        execute_db(query=_b64("SELECT 1"), auth_header="Y3VzdG9tOmNyZWQ=")
        assert route.calls[0].request.headers["authorization"] != (
            f"Basic {base64.b64encode(b'u:k').decode()}"
        )

    @respx.mock
    def test_an_explicit_auth_header_works_without_lt_credentials(self, monkeypatch):
        monkeypatch.delenv("LT_USERNAME", raising=False)
        monkeypatch.delenv("LT_ACCESS_KEY", raising=False)
        route = respx.post(_URL).mock(return_value=httpx.Response(200, json={}))
        execute_db(query=_b64("SELECT 1"), auth_header="Y3VzdG9tOmNyZWQ=")
        assert route.called

    def test_missing_lt_credentials_raises(self, monkeypatch):
        monkeypatch.delenv("LT_USERNAME", raising=False)
        monkeypatch.delenv("LT_ACCESS_KEY", raising=False)
        with pytest.raises(RuntimeError) as exc:
            execute_db(query=_b64("SELECT 1"))
        assert "LT_USERNAME" in str(exc.value) or "LT_ACCESS_KEY" in str(exc.value)

    @pytest.mark.parametrize("absent", ["LT_USERNAME", "LT_ACCESS_KEY"])
    def test_half_a_credential_pair_is_no_credential(self, monkeypatch, absent):
        monkeypatch.delenv(absent, raising=False)
        with pytest.raises(RuntimeError):
            execute_db(query=_b64("SELECT 1"))


@respx.mock
def test_missing_connection_fields_default_to_empty():
    route = respx.post(_URL).mock(return_value=httpx.Response(200, json={}))
    execute_db(query=_b64("SELECT 1"))
    payload = json.loads(route.calls[0].request.content)
    assert payload["payload"] == {"id": "", "timeout": 10000, "db_name": "", "tunnel_id": ""}


@respx.mock
def test_tunnel_id_falls_back_to_the_env_var(monkeypatch):
    monkeypatch.setenv("LT_PROXY_TUNNEL_ID", "tun-env")
    route = respx.post(_URL).mock(return_value=httpx.Response(200, json={}))
    execute_db(query=_b64("SELECT 1"))
    payload = json.loads(route.calls[0].request.content)
    assert payload["payload"]["tunnel_id"] == "tun-env"


@respx.mock
def test_non_200_response_raises():
    respx.post(_URL).mock(return_value=httpx.Response(500, text="db unreachable"))
    with pytest.raises(RuntimeError) as exc:
        execute_db(query=_b64("SELECT 1"))
    assert "500" in str(exc.value) or "db-query" in str(exc.value)


@respx.mock
def test_error_key_in_result_raises():
    respx.post(_URL).mock(return_value=httpx.Response(200, json={"error": "syntax error"}))
    with pytest.raises(RuntimeError) as exc:
        execute_db(query=_b64("SELECT 1"))
    assert "syntax error" in str(exc.value)


@respx.mock
def test_output_variable_is_written():
    respx.post(_URL).mock(return_value=httpx.Response(200, json={"rows": []}))
    result = execute_db(query=_b64("SELECT 1"), output_variable="db_result")
    assert _variable_store["db_result"] == result


@respx.mock
def test_automind_url_falls_back_to_prod_default(monkeypatch):
    monkeypatch.delenv("AUTOMIND_URL", raising=False)
    monkeypatch.delenv("AUTEUR_AUTOMIND", raising=False)
    route = respx.post("https://kaneai-api.lambdatest.com/db-query").mock(
        return_value=httpx.Response(200, json={})
    )
    execute_db(query=_b64("SELECT 1"))
    assert route.called


@respx.mock
def test_auteur_automind_env_takes_priority_over_automind_url(monkeypatch):
    monkeypatch.setenv("AUTEUR_AUTOMIND", "https://auteur.example.test")
    route = respx.post("https://auteur.example.test/db-query").mock(
        return_value=httpx.Response(200, json={})
    )
    execute_db(query=_b64("SELECT 1"))
    assert route.called


@respx.mock
def test_explicit_automind_url_argument_wins():
    route = respx.post("https://explicit.example.test/db-query").mock(
        return_value=httpx.Response(200, json={})
    )
    execute_db(query=_b64("SELECT 1"), automind_url="https://explicit.example.test")
    assert route.called
