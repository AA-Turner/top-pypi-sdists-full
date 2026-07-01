"""Test the variable store + template substitution."""
import re
import pytest
from datetime import datetime

import pyotp

from testmu_selenium import _config
from testmu_selenium._vars import (
    _variable_store, _test_params, set_var, var, clear_state, resolve_variable,
)
from testmu_selenium._errors import TestmuConfigError


@pytest.fixture(autouse=True)
def reset_state():
    """Clear store before each test to avoid cross-test leakage."""
    clear_state()
    yield
    clear_state()


class TestSetVar:
    def test_set_var_writes_to_store(self):
        set_var("name", "Alice")
        assert _variable_store["name"] == "Alice"

    def test_set_var_overwrites(self):
        set_var("x", 1)
        set_var("x", 2)
        assert _variable_store["x"] == 2

    def test_set_var_accepts_complex_types(self):
        set_var("data", {"nested": [1, 2, 3]})
        assert _variable_store["data"] == {"nested": [1, 2, 3]}


class TestVarBraceTemplate:
    def test_var_returns_value_for_known_key(self):
        set_var("name", "Alice")
        assert var("{{name}}") == "Alice"

    def test_var_substitutes_within_string(self):
        set_var("name", "Alice")
        assert var("hello {{name}}") == "hello Alice"

    def test_var_dollar_brace_syntax(self):
        set_var("name", "Bob")
        assert var("${name}") == "Bob"

    def test_var_with_default_fallback(self):
        assert var("{{missing|fallback}}") == "fallback"

    def test_var_known_key_takes_precedence_over_default(self):
        set_var("present", "real")
        assert var("{{present|fallback}}") == "real"

    def test_var_returns_input_when_no_template(self):
        assert var("plain string") == "plain string"

    def test_var_handles_multiple_templates(self):
        set_var("a", "1")
        set_var("b", "2")
        assert var("{{a}}-{{b}}") == "1-2"

    def test_var_preserves_native_type_when_template_is_whole_string(self):
        """If the template is the entire input, return native type instead of str-coercing."""
        set_var("count", 42)
        assert var("{{count}}") == 42


class TestVarDottedTraversal:
    """var() resolves dotted / bracket-indexed paths into a stored object when the
    flat key is absent. An API_CALL/STORE step writes the whole response under one
    root key (set_var("api_x", <response>)); a templated field then references
    {{api_x.response_body.results[0].name.first}} and must resolve to the nested
    value rather than returning the literal template.
    """

    API = {"response_body": {"results": [{"name": {"first": "Tamara"}}]}}

    def test_dotted_index_path_into_stored_object(self):
        set_var("api_variablebdf1", self.API)
        assert var("{{api_variablebdf1.response_body.results[0].name.first}}") == "Tamara"

    def test_dotted_path_preserves_native_type(self):
        set_var("obj", {"count": 7})
        assert var("{{obj.count}}") == 7

    def test_embedded_dotted_path_substitutes(self):
        set_var("api_variablebdf1", self.API)
        assert var("hi {{api_variablebdf1.response_body.results[0].name.first}}!") == "hi Tamara!"

    def test_unresolved_dotted_path_returns_literal(self):
        assert var("{{missing.a.b}}") == "{{missing.a.b}}"

    def test_flat_key_with_dots_takes_precedence(self):
        set_var("a.b", "flat")
        set_var("a", {"b": "nested"})
        assert var("{{a.b}}") == "flat"

    def test_json_string_value_is_parsed_for_traversal(self):
        import json
        set_var("api_variablebdf1", json.dumps(self.API))
        assert var("{{api_variablebdf1.response_body.results[0].name.first}}") == "Tamara"

    def test_dollar_brace_dotted_path(self):
        set_var("obj", {"k": "v"})
        assert var("${obj.k}") == "v"


class TestTestParams:
    def test_test_params_separate_namespace(self):
        _test_params["env"] = "stage"
        assert _test_params["env"] == "stage"
        assert "env" not in _variable_store


class TestDollarTestParams:
    """${name} resolves from _test_params FIRST, then _variable_store. {{name}}
    behavior is unchanged (never reads _test_params)."""

    def test_dollar_whole_string_from_test_params(self):
        _test_params["p"] = "zeeshan"
        assert var("${p}") == "zeeshan"

    def test_dollar_embedded_from_test_params(self):
        _test_params["p"] = "zeeshan"
        assert var("x ${p} y") == "x zeeshan y"

    def test_dollar_test_params_takes_precedence_over_store(self):
        _test_params["k"] = "from_params"
        set_var("k", "from_store")
        assert var("${k}") == "from_params"

    def test_dollar_falls_back_to_store_when_not_in_params(self):
        set_var("k", "from_store")
        assert var("${k}") == "from_store"

    def test_mustache_does_not_read_test_params(self):
        _test_params["k"] = "from_params"
        set_var("k", "from_store")
        assert var("{{k}}") == "from_store"

    def test_resolve_variable_dollar_from_test_params(self):
        _test_params["p"] = "zeeshan"
        assert resolve_variable("p", "${p}") == "zeeshan"


class TestClearState:
    def test_clear_state_empties_store(self):
        set_var("a", "1")
        clear_state()
        assert _variable_store == {}

    def test_clear_state_empties_test_params(self):
        _test_params["x"] = "y"
        clear_state()
        assert _test_params == {}


class TestNamespaceDispatch:
    """Namespace dispatch: smart/secrets/global/environment/totp. Tests are TDD — written
    before implementation (RED), then verified green after implementation."""

    # ------------------------------------------------------------------
    # 1. Smart deterministic
    # ------------------------------------------------------------------
    @pytest.mark.parametrize("smart_name,fmt", [
        ("current_year", "%Y"),
        ("current_month_number", "%m"),
        ("current_date", "%Y-%m-%d"),
    ])
    def test_smart_deterministic(self, smart_name, fmt):
        expected = datetime.now().strftime(fmt)
        assert var(f"{{{{smart.{smart_name}}}}}") == expected

    # ------------------------------------------------------------------
    # 2. smart.random_email
    # ------------------------------------------------------------------
    EMAIL_RE = re.compile(r"^[a-z0-9]{10}@example\.com$")

    def test_smart_random_email_var(self):
        result = var("{{smart.random_email}}")
        assert self.EMAIL_RE.match(result), f"got {result!r}"
        assert result != "{{smart.random_email}}"

    def test_smart_random_email_resolve_variable(self):
        result = resolve_variable("smart.random_email", "{{smart.random_email}}")
        assert self.EMAIL_RE.match(result), f"got {result!r}"

    # ------------------------------------------------------------------
    # 3. smart.random_int
    # ------------------------------------------------------------------
    def test_smart_random_int(self):
        result = var("{{smart.random_int}}")
        assert re.match(r"^\d{3}$", result), f"got {result!r}"

    # ------------------------------------------------------------------
    # 4. secrets namespace
    # ------------------------------------------------------------------
    def test_secrets_resolves_from_env(self, monkeypatch):
        monkeypatch.setenv("MY_SECRET_X", "sekret")
        assert var("{{secrets.cat.MY_SECRET_X}}") == "sekret"

    def test_secrets_unknown_returns_empty(self, monkeypatch):
        monkeypatch.delenv("TOTALLY_UNKNOWN_KEY_ZZZ99", raising=False)
        assert var("{{secrets.cat.TOTALLY_UNKNOWN_KEY_ZZZ99}}") == ""

    # ------------------------------------------------------------------
    # 5. global env-fallback (lt_auth=False)
    # ------------------------------------------------------------------
    def test_global_env_fallback(self, monkeypatch):
        monkeypatch.setattr(_config, "lt_auth", False)
        monkeypatch.setenv("TESTMU_VAR_token", "abc")
        assert var("{{global.token}}") == "abc"

    # ------------------------------------------------------------------
    # 6. global raises when lt_auth=False and no env var
    # ------------------------------------------------------------------
    def test_global_raises_when_unresolvable(self, monkeypatch):
        monkeypatch.setattr(_config, "lt_auth", False)
        monkeypatch.delenv("TESTMU_VAR_missing", raising=False)
        with pytest.raises(TestmuConfigError):
            var("{{global.missing}}")

    # ------------------------------------------------------------------
    # 7. environment env-fallback (lt_auth=False)
    # ------------------------------------------------------------------
    def test_environment_env_fallback(self, monkeypatch):
        monkeypatch.setattr(_config, "lt_auth", False)
        monkeypatch.setenv("TESTMU_VAR_y", "env_val")
        assert var("{{environment.y}}") == "env_val"

    # ------------------------------------------------------------------
    # 8. totp env-fallback (lt_auth=False)
    # ------------------------------------------------------------------
    TOTP_SEED = "JBSWY3DPEHPK3PXP"

    def test_totp_env_fallback(self, monkeypatch):
        monkeypatch.setattr(_config, "lt_auth", False)
        monkeypatch.setenv("TESTMU_TOTP_login", self.TOTP_SEED)
        expected_before = pyotp.TOTP(self.TOTP_SEED).now()
        result = var("{{totp.login}}")
        expected_after = pyotp.TOTP(self.TOTP_SEED).now()
        assert result in {expected_before, expected_after}
        assert re.match(r"^\d{6}$", result)

    # ------------------------------------------------------------------
    # 9. Embedded namespace ref
    # ------------------------------------------------------------------
    def test_embedded_smart_in_string(self):
        result = var("year={{smart.current_year}}")
        assert result.startswith("year=")
        assert datetime.now().strftime("%Y") in result

    # ------------------------------------------------------------------
    # 10. Regression: plain stored var resolves; unknown plain → literal
    # ------------------------------------------------------------------
    def test_regression_plain_var_resolves(self):
        set_var("foo", "bar")
        assert var("{{foo}}") == "bar"

    def test_regression_unknown_plain_name_returns_literal(self):
        assert var("{{nope}}") == "{{nope}}"
