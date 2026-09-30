"""the step end hook reports the values the step ran with.

The instance view previously showed only variable NAMES; a failing step gave no
way to see what it actually read or wrote. Every variable read or written between
a step's start and end hook is buffered and shipped on the end hook as
``variables`` — except the two credential namespaces.
"""
import json
from unittest.mock import MagicMock, patch

import pytest

from testmu_selenium import _vars
from testmu_selenium._step import step
from testmu_selenium._step_variables import (
    _json_safe,
    pop_step_variables,
    record_variable,
    reset_step_variables,
)


@pytest.fixture(autouse=True)
def _clean():
    reset_step_variables()
    _vars.clear_state()
    yield
    reset_step_variables()
    _vars.clear_state()


class TestBuffer:
    def test_records_and_drains(self):
        record_variable("a", 1)
        record_variable("b", "two")
        assert pop_step_variables() == {"a": 1, "b": "two"}
        assert pop_step_variables() == {}

    def test_last_write_wins(self):
        record_variable("a", 1)
        record_variable("a", 2)
        assert pop_step_variables() == {"a": 2}

    def test_empty_name_is_ignored(self):
        record_variable("", "x")
        assert pop_step_variables() == {}

    def test_unserializable_value_degrades_to_its_repr(self):
        class Widget:
            def __repr__(self):
                return "<Widget>"

        record_variable("w", Widget())
        drained = pop_step_variables()
        assert drained == {"w": "<Widget>"}
        json.dumps(drained)  # the whole payload must stay serializable

    @pytest.mark.parametrize("value", [1, 1.5, "s", True, None, [1, 2], {"k": "v"}])
    def test_json_native_values_are_preserved_as_is(self, value):
        assert _json_safe(value) == value


class TestWritesAreRecorded:
    def test_set_var_is_recorded(self):
        _vars.set_var("order_id", "A-1")
        assert pop_step_variables() == {"order_id": "A-1"}

    def test_global_write_is_recorded_under_its_bare_name(self):
        # set_var("global.X") stores under the BARE key, and reads use {{X}} —
        # the buffer must agree with the read name, not the write name.
        with patch.object(_vars, "_update_session_variable_value"), \
             patch("testmu_selenium._config.lt_auth", False):
            _vars.set_var("global.token", "t-1")
        assert pop_step_variables() == {"token": "t-1"}


class TestReadsAreRecorded:
    def test_whole_string_read_is_recorded(self):
        _vars.set_var("qty", 3)
        pop_step_variables()  # drop the write
        assert _vars.var("{{qty}}") == 3
        assert pop_step_variables() == {"qty": 3}

    def test_embedded_read_is_recorded(self):
        _vars.set_var("name", "Ada")
        pop_step_variables()
        assert _vars.var("hello {{name}}") == "hello Ada"
        assert pop_step_variables() == {"name": "Ada"}

    def test_dotted_path_is_recorded_under_the_path_it_was_read_by(self):
        _vars.set_var("api", {"body": {"id": 7}})
        pop_step_variables()
        assert _vars.var("{{api.body.id}}") == 7
        assert pop_step_variables() == {"api.body.id": 7}

    def test_test_param_read_is_recorded(self):
        _vars._test_params["env"] = "staging"
        pop_step_variables()
        assert _vars.var("${env}") == "staging"
        assert pop_step_variables() == {"env": "staging"}

    def test_smart_variable_read_is_recorded(self):
        assert _vars.var("{{smart.country}}") == "India"
        assert pop_step_variables() == {"smart.country": "India"}

    def test_unresolved_template_records_nothing(self):
        assert _vars.var("{{nope}}") == "{{nope}}"
        assert pop_step_variables() == {}

    def test_a_defaulted_miss_records_nothing(self):
        # The default is a literal in the template, not a variable value.
        assert _vars.var("{{missing|fallback}}") == "fallback"
        assert pop_step_variables() == {}


class TestCredentialsAreNeverRecorded:
    """The buffer is shipped to the hub and written into the run's artefacts."""

    def test_secrets_are_not_recorded(self, monkeypatch):
        monkeypatch.setenv("API_KEY", "super-secret")
        assert _vars.var("{{secrets.vault.API_KEY}}") == "super-secret"
        assert pop_step_variables() == {}

    def test_secrets_embedded_in_a_string_are_not_recorded(self, monkeypatch):
        monkeypatch.setenv("API_KEY", "super-secret")
        assert _vars.var("key=({{secrets.vault.API_KEY}})") == "key=(super-secret)"
        assert pop_step_variables() == {}

    def test_totp_codes_are_not_recorded(self, monkeypatch):
        monkeypatch.setenv("TESTMU_TOTP_login", "JBSWY3DPEHPK3PXP")
        monkeypatch.setattr("testmu_selenium._config.lt_auth", False)
        code = _vars.var("{{totp.login}}")
        assert code.isdigit()
        assert pop_step_variables() == {}


class TestEndHookPayload:
    def _emitted(self, calls, verb):
        return [c.args[1] for c in calls if c.args[0] == verb]

    def test_variables_ride_the_end_hook(self):
        with patch("testmu_selenium._step._emit_step_hook") as emit:
            with step("place the order"):
                _vars.set_var("order_id", "A-1")
        end = self._emitted(emit.call_args_list, "lambda-testCase-end")[0]
        assert end["name"] == "place the order"
        assert end["status"] == "passed"
        assert end["variables"] == {"order_id": "A-1"}

    def test_start_hook_carries_no_variables(self):
        with patch("testmu_selenium._step._emit_step_hook") as emit:
            with step("s"):
                _vars.set_var("x", 1)
        start = self._emitted(emit.call_args_list, "lambda-testCase-start")[0]
        assert "variables" not in start

    def test_key_is_absent_when_the_step_touched_nothing(self):
        with patch("testmu_selenium._step._emit_step_hook") as emit:
            with step("no variables here"):
                pass
        end = self._emitted(emit.call_args_list, "lambda-testCase-end")[0]
        assert "variables" not in end

    def test_a_failing_step_still_reports_its_variables(self):
        with patch("testmu_selenium._step._emit_step_hook") as emit:
            with pytest.raises(RuntimeError):
                with step("boom"):
                    _vars.set_var("attempted", "yes")
                    raise RuntimeError("boom")
        end = self._emitted(emit.call_args_list, "lambda-testCase-end")[0]
        assert end["status"] == "failed"
        assert end["variables"] == {"attempted": "yes"}

    def test_each_step_reports_only_its_own_variables(self):
        with patch("testmu_selenium._step._emit_step_hook") as emit:
            with step("first"):
                _vars.set_var("a", 1)
            with step("second"):
                _vars.set_var("b", 2)
        ends = self._emitted(emit.call_args_list, "lambda-testCase-end")
        assert ends[0]["variables"] == {"a": 1}
        assert ends[1]["variables"] == {"b": 2}

    def test_the_payload_is_json_serializable(self):
        with patch("testmu_selenium._step._emit_step_hook") as emit:
            with step("s"):
                _vars.set_var("obj", object())
        end = self._emitted(emit.call_args_list, "lambda-testCase-end")[0]
        json.dumps(end)
