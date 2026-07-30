"""Tests for testmu_selenium.resolve_variable — public V3 binding."""
import pytest
import pytest

from testmu_selenium import _config
from testmu_selenium._errors import TestmuConfigError
from testmu_selenium._vars import set_var, clear_state, resolve_variable


@pytest.fixture(autouse=True)
def reset_state():
    """Clear store before/after each test to avoid cross-test leakage."""
    clear_state()
    yield
    clear_state()


API = {"response_body": {"results": [{"name": {"first": "Tamara"}}]}}


class TestResolveVariableTemplatePath:
    """template carries {{...}} / ${...} — delegate directly to var()."""

    def test_dotted_bracket_path_via_template(self):
        """Dotted/bracket path embedded in {{...}} resolves against stored object."""
        set_var("api_x", API)
        result = resolve_variable(
            "api_x.response_body.results[0].name.first",
            "{{api_x.response_body.results[0].name.first}}",
        )
        assert result == "Tamara"

    def test_dollar_brace_template_resolves(self):
        """${...} template form also resolves."""
        set_var("api_x", API)
        result = resolve_variable(
            "api_x.response_body.results[0].name.first",
            "${api_x.response_body.results[0].name.first}",
        )
        assert result == "Tamara"

    def test_native_type_preservation_int(self):
        """When whole template is {{name}} and value is int, returns int not str."""
        set_var("count", 7)
        result = resolve_variable("count", "{{count}}")
        assert result == 7
        assert isinstance(result, int)

    def test_native_type_preservation_dict(self):
        """When whole template is {{name}} and value is dict, returns dict."""
        set_var("data", {"k": "v"})
        result = resolve_variable("data", "{{data}}")
        assert result == {"k": "v"}

    def test_embedded_template_in_string(self):
        """Template with surrounding text — string substitution."""
        set_var("greeting", "world")
        result = resolve_variable("greeting", "hello {{greeting}}")
        assert result == "hello world"


class TestResolveVariablePlainFallback:
    """template is a plain string (no {{ or ${ ) — name-based lookup with fallback."""

    def test_plain_name_hits_store(self):
        """When name is in store and template is plain, returns store value."""
        set_var("foo", "bar")
        result = resolve_variable("foo", "default")
        assert result == "bar"

    def test_plain_name_absent_returns_template(self):
        """When name is missing and template is plain, returns the fallback template unchanged."""
        result = resolve_variable("missing", "fallback")
        assert result == "fallback"

    def test_plain_name_absent_none_template_returns_none(self):
        """When name absent and template is None (default), returns None."""
        result = resolve_variable("missing")
        assert result is None

    def test_plain_name_empty_string_returns_template(self):
        """When name is empty/falsy, returns template unchanged."""
        result = resolve_variable("", "keep_this")
        assert result == "keep_this"

    def test_plain_name_store_value_int(self):
        """Store value of int type is returned as-is (not cast to str)."""
        set_var("num", 42)
        result = resolve_variable("num", "0")
        assert result == 42
        assert isinstance(result, int)


class TestResolveVariableNamespaceFallback:
    """Reserved-namespace resolvers raise TestmuConfigError on hard failure.

    Bug-D2 fix: resolve_variable no longer swallows TestmuConfigError and
    returns the raw literal/default — that caused false-passes (test looked
    green but the variable was never resolved). Hard failures now propagate
    so the test aborts loudly rather than silently using an unresolved value.
    """

    @pytest.fixture
    def no_lt_auth(self, monkeypatch):
        monkeypatch.setattr(_config, "lt_auth", False)
        monkeypatch.delenv("TESTMU_VAR_lt_email", raising=False)

    def test_plain_default_when_global_namespace_raises(self, no_lt_auth):
        """V3 emit shape: resolve_variable("global.lt_email", "user@example.com")
        raises when no creds + no env override (no false-pass from swallowing)."""
        with pytest.raises(TestmuConfigError):
            resolve_variable("global.lt_email", "user@example.com")

    def test_embedded_template_default_when_global_namespace_raises(self, no_lt_auth):
        """Embedded {{global.x}} in template raises rather than returning the literal."""
        tmpl = "prefix-{{global.lt_email}}-suffix"
        with pytest.raises(TestmuConfigError):
            resolve_variable("global.lt_email", tmpl)


class TestResolveVariableStateIsolation:
    """Verify clear_state() prevents cross-test pollution."""

    def test_store_cleared_between_tests_a(self):
        set_var("isolated", "value_a")
        assert resolve_variable("isolated", "fallback") == "value_a"

    def test_store_cleared_between_tests_b(self):
        # "isolated" should NOT be in store (cleared by fixture)
        assert resolve_variable("isolated", "fallback") == "fallback"
