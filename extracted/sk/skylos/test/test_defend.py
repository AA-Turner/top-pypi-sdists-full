"""Tests for the AI Defense Engine (Phase 1B, 1C, 2, 3)."""

import json
import tempfile
from pathlib import Path

import pytest

from skylos.discover.detector import detect_integrations
from skylos.discover.integration import LLMIntegration, ToolDef
from skylos.discover.graph import AIIntegrationGraph
from skylos.defend.engine import run_defense_checks
from skylos.defend.result import DefenseResult, DefenseScore, OpsScore
from skylos.defend.scoring import compute_defense_score, compute_ops_score, SEVERITY_WEIGHTS
from skylos.defend.report import format_defense_table, format_defense_json
from skylos.defend.policy import (
    load_policy,
    DefensePolicy,
    compute_owasp_coverage,
    _parse_policy,
    OWASP_LLM_MAPPING,
)
from skylos.defend.plugins import ALL_PLUGINS
from skylos.defend.plugins.no_dangerous_sink import NoDangerousSinkPlugin
from skylos.defend.plugins.tool_scope import ToolScopePlugin
from skylos.defend.plugins.tool_schema_present import ToolSchemaPresentPlugin
from skylos.defend.plugins.prompt_delimiter import PromptDelimiterPlugin
from skylos.defend.plugins.output_validation import OutputValidationPlugin
from skylos.defend.plugins.model_pinned import ModelPinnedPlugin
from skylos.defend.plugins.input_length_limit import InputLengthLimitPlugin
from skylos.defend.plugins.untrusted_input_to_prompt import UntrustedInputToPromptPlugin
from skylos.defend.plugins.rag_context_isolation import RagContextIsolationPlugin
from skylos.defend.plugins.output_pii_filter import OutputPiiFilterPlugin
from skylos.defend.plugins.logging_present import LoggingPresentPlugin
from skylos.defend.plugins.cost_controls import CostControlsPlugin
from skylos.defend.plugins.rate_limiting import RateLimitingPlugin


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _make_integration(**kwargs) -> LLMIntegration:
    """Create a test LLMIntegration with sensible defaults."""
    defaults = {
        "provider": "OpenAI",
        "location": "test.py:10",
        "integration_type": "chat",
    }
    defaults.update(kwargs)
    return LLMIntegration(**defaults)


def _empty_graph() -> AIIntegrationGraph:
    return AIIntegrationGraph()


# ---------------------------------------------------------------------------
# Plugin tests
# ---------------------------------------------------------------------------


class TestNoDangerousSinkPlugin:
    plugin = NoDangerousSinkPlugin()

    def test_passes_when_no_sinks(self):
        integ = _make_integration(output_sinks=[])
        result = self.plugin.check(integ, _empty_graph())
        assert result.passed is True

    def test_fails_when_sinks_present(self):
        integ = _make_integration(output_sinks=["eval (L45)", "subprocess.run (L50)"])
        result = self.plugin.check(integ, _empty_graph())
        assert result.passed is False
        assert "eval" in result.message
        assert result.severity == "critical"
        assert result.owasp_llm == "LLM02"


class TestToolScopePlugin:
    plugin = ToolScopePlugin()

    def test_not_applicable_to_non_agent(self):
        integ = _make_integration(integration_type="chat", tools=[])
        assert self.plugin.applies_to(integ) is False

    def test_passes_when_tools_safe(self):
        tool = ToolDef(name="search", location="t.py:1", dangerous_calls=[])
        integ = _make_integration(integration_type="agent", tools=[tool])
        result = self.plugin.check(integ, _empty_graph())
        assert result.passed is True

    def test_fails_when_tools_dangerous(self):
        tool = ToolDef(
            name="shell",
            location="t.py:1",
            dangerous_calls=["subprocess.run (L5)"],
        )
        integ = _make_integration(integration_type="agent", tools=[tool])
        result = self.plugin.check(integ, _empty_graph())
        assert result.passed is False
        assert "shell" in result.message


class TestToolSchemaPresentPlugin:
    plugin = ToolSchemaPresentPlugin()

    def test_not_applicable_to_non_agent(self):
        integ = _make_integration(integration_type="chat", tools=[])
        assert self.plugin.applies_to(integ) is False

    def test_passes_when_all_typed(self):
        tool = ToolDef(name="search", location="t.py:1", has_typed_schema=True)
        integ = _make_integration(integration_type="agent", tools=[tool])
        result = self.plugin.check(integ, _empty_graph())
        assert result.passed is True

    def test_fails_when_untyped(self):
        tool = ToolDef(name="search", location="t.py:1", has_typed_schema=False)
        integ = _make_integration(integration_type="agent", tools=[tool])
        result = self.plugin.check(integ, _empty_graph())
        assert result.passed is False


class TestPromptDelimiterPlugin:
    plugin = PromptDelimiterPlugin()

    def test_not_applicable_without_inputs(self):
        integ = _make_integration(input_sources=[], prompt_sites=[])
        assert self.plugin.applies_to(integ) is False

    def test_passes_when_delimited(self):
        integ = _make_integration(
            input_sources=["request.json (L5)"],
            prompt_sites=["test.py:10"],
            has_prompt_delimiter=True,
        )
        result = self.plugin.check(integ, _empty_graph())
        assert result.passed is True

    def test_fails_when_not_delimited(self):
        integ = _make_integration(
            input_sources=["request.json (L5)"],
            prompt_sites=["test.py:10"],
            has_prompt_delimiter=False,
        )
        result = self.plugin.check(integ, _empty_graph())
        assert result.passed is False


class TestOutputValidationPlugin:
    plugin = OutputValidationPlugin()

    def test_passes_when_validated(self):
        integ = _make_integration(
            has_output_validation=True,
            output_validation_location="test.py:20",
        )
        result = self.plugin.check(integ, _empty_graph())
        assert result.passed is True

    def test_fails_when_not_validated(self):
        integ = _make_integration(has_output_validation=False)
        result = self.plugin.check(integ, _empty_graph())
        assert result.passed is False


class TestModelPinnedPlugin:
    plugin = ModelPinnedPlugin()

    def test_passes_when_pinned(self):
        integ = _make_integration(
            model_value="gpt-4o-2024-08-06", model_pinned=True
        )
        result = self.plugin.check(integ, _empty_graph())
        assert result.passed is True
        assert "gpt-4o-2024-08-06" in result.message

    def test_fails_when_floating(self):
        integ = _make_integration(
            model_value="gpt-4o", model_pinned=False
        )
        result = self.plugin.check(integ, _empty_graph())
        assert result.passed is False
        assert "floating" in result.message.lower()

    def test_fails_when_no_model(self):
        integ = _make_integration(model_value="", model_pinned=False)
        result = self.plugin.check(integ, _empty_graph())
        assert result.passed is False


class TestInputLengthLimitPlugin:
    plugin = InputLengthLimitPlugin()

    def test_not_applicable_without_inputs(self):
        integ = _make_integration(input_sources=[])
        assert self.plugin.applies_to(integ) is False

    def test_passes_when_limited(self):
        integ = _make_integration(
            input_sources=["request.json (L5)"],
            has_input_length_limit=True,
            input_length_limit_location="test.py:8",
        )
        result = self.plugin.check(integ, _empty_graph())
        assert result.passed is True

    def test_fails_when_unbounded(self):
        integ = _make_integration(
            input_sources=["request.json (L5)"],
            has_input_length_limit=False,
        )
        result = self.plugin.check(integ, _empty_graph())
        assert result.passed is False


# ---------------------------------------------------------------------------
# Scoring tests
# ---------------------------------------------------------------------------


class TestScoring:
    def test_perfect_score(self):
        results = [
            DefenseResult("a", True, "t:1", "t:1", "ok", "critical", 8, "defense"),
            DefenseResult("b", True, "t:1", "t:1", "ok", "high", 5, "defense"),
        ]
        score = compute_defense_score(results)
        assert score.score_pct == 100
        assert score.risk_rating == "SECURE"
        assert score.passed == 2
        assert score.total == 2

    def test_zero_score(self):
        results = [
            DefenseResult("a", False, "t:1", "t:1", "bad", "critical", 8, "defense"),
            DefenseResult("b", False, "t:1", "t:1", "bad", "high", 5, "defense"),
        ]
        score = compute_defense_score(results)
        assert score.score_pct == 0
        assert score.risk_rating == "CRITICAL"

    def test_mixed_score(self):
        results = [
            DefenseResult("a", True, "t:1", "t:1", "ok", "critical", 8, "defense"),
            DefenseResult("b", False, "t:1", "t:1", "bad", "critical", 8, "defense"),
            DefenseResult("c", True, "t:1", "t:1", "ok", "low", 1, "defense"),
        ]
        score = compute_defense_score(results)
        # 9/17 = 53%
        assert score.score_pct == 53
        assert score.risk_rating == "MEDIUM"

    def test_empty_results(self):
        score = compute_defense_score([])
        assert score.score_pct == 100
        assert score.risk_rating == "SECURE"

    def test_ops_results_excluded(self):
        results = [
            DefenseResult("a", True, "t:1", "t:1", "ok", "critical", 8, "defense"),
            DefenseResult("b", False, "t:1", "t:1", "bad", "medium", 3, "ops"),
        ]
        score = compute_defense_score(results)
        # Ops result excluded, only defense: 8/8 = 100%
        assert score.score_pct == 100
        assert score.total == 1

    def test_severity_weights(self):
        assert SEVERITY_WEIGHTS["critical"] == 8
        assert SEVERITY_WEIGHTS["high"] == 5
        assert SEVERITY_WEIGHTS["medium"] == 3
        assert SEVERITY_WEIGHTS["low"] == 1

    def test_risk_rating_boundaries(self):
        # < 25% = CRITICAL
        results = [
            DefenseResult("a", True, "t:1", "t:1", "ok", "low", 1, "defense"),
            DefenseResult("b", False, "t:1", "t:1", "bad", "critical", 8, "defense"),
            DefenseResult("c", False, "t:1", "t:1", "bad", "high", 5, "defense"),
        ]
        score = compute_defense_score(results)
        assert score.risk_rating == "CRITICAL"  # 1/14 = 7%


# ---------------------------------------------------------------------------
# Engine tests
# ---------------------------------------------------------------------------


class TestEngine:
    def test_runs_all_plugins(self):
        integ = _make_integration(
            model_value="gpt-4o",
            model_pinned=False,
            has_output_validation=False,
            input_sources=["request.json (L5)"],
            prompt_sites=["test.py:10"],
        )
        results, score, _ops = run_defense_checks([integ], _empty_graph())
        assert len(results) > 0
        plugin_ids = {r.plugin_id for r in results}
        # At minimum these should run for a chat integration with input sources
        assert "model-pinned" in plugin_ids
        assert "output-validation" in plugin_ids

    def test_severity_filter(self):
        integ = _make_integration(
            model_value="gpt-4o",
            model_pinned=False,
            input_sources=["request.json (L5)"],
            prompt_sites=["test.py:10"],
        )
        results, score, _ops = run_defense_checks(
            [integ], _empty_graph(), min_severity="high"
        )
        # Should not include low/medium checks
        for r in results:
            assert r.severity in ("critical", "high")

    def test_owasp_filter(self):
        integ = _make_integration(
            model_value="gpt-4o",
            model_pinned=False,
            input_sources=["request.json (L5)"],
            prompt_sites=["test.py:10"],
        )
        results, score, _ops = run_defense_checks(
            [integ], _empty_graph(), owasp_filter=["LLM01"]
        )
        for r in results:
            # Plugins with owasp_llm=None pass through the filter (ops plugins)
            assert r.owasp_llm == "LLM01" or r.owasp_llm is None

    def test_policy_disables_plugin(self):
        integ = _make_integration(model_value="gpt-4o", model_pinned=False)
        policy = DefensePolicy(rules={"model-pinned": {"enabled": False}})
        results, score, _ops = run_defense_checks([integ], _empty_graph(), policy=policy)
        plugin_ids = {r.plugin_id for r in results}
        assert "model-pinned" not in plugin_ids

    def test_policy_overrides_severity(self):
        integ = _make_integration(model_value="gpt-4o", model_pinned=False)
        policy = DefensePolicy(rules={"model-pinned": {"severity": "critical"}})
        results, score, _ops = run_defense_checks([integ], _empty_graph(), policy=policy)
        mp_results = [r for r in results if r.plugin_id == "model-pinned"]
        assert len(mp_results) == 1
        assert mp_results[0].severity == "critical"
        assert mp_results[0].weight == 8


# ---------------------------------------------------------------------------
# Report tests
# ---------------------------------------------------------------------------


class TestReport:
    def test_table_format(self):
        results = [
            DefenseResult(
                "model-pinned", True, "t.py:10", "t.py:10",
                "Model pinned to gpt-4o-2024-08-06", "medium", 3, "defense",
                owasp_llm="LLM03",
            ),
            DefenseResult(
                "no-dangerous-sink", False, "t.py:10", "t.py:10",
                "LLM output flows to eval()", "critical", 8, "defense",
                owasp_llm="LLM02",
            ),
        ]
        score = compute_defense_score(results)
        output = format_defense_table(results, score, 1, 10)
        assert "Skylos AI Defense Report" in output
        assert "model-pinned" in output
        assert "no-dangerous-sink" in output

    def test_json_format(self):
        results = [
            DefenseResult(
                "model-pinned", True, "t.py:10", "t.py:10",
                "ok", "medium", 3, "defense",
            ),
        ]
        score = compute_defense_score(results)
        output = format_defense_json(results, score, 1, 10)
        data = json.loads(output)
        assert data["version"] == "1.0"
        assert data["summary"]["total_checks"] == 1
        assert data["summary"]["passed"] == 1
        assert len(data["findings"]) == 1


# ---------------------------------------------------------------------------
# Policy tests (Phase 2)
# ---------------------------------------------------------------------------


class TestPolicy:
    def test_parse_valid_policy(self):
        raw = {
            "rules": {
                "model-pinned": {"severity": "high"},
                "input-length-limit": {"enabled": False},
            },
            "gate": {
                "min_score": 70,
                "fail_on": "high",
            },
        }
        policy = _parse_policy(raw)
        assert policy.rules["model-pinned"]["severity"] == "high"
        assert policy.rules["input-length-limit"]["enabled"] is False
        assert policy.gate_min_score == 70
        assert policy.gate_fail_on == "high"

    def test_parse_unknown_plugin_raises(self):
        raw = {"rules": {"nonexistent-plugin": {"severity": "high"}}}
        with pytest.raises(ValueError, match="Unknown plugin"):
            _parse_policy(raw)

    def test_parse_invalid_severity_raises(self):
        raw = {"rules": {"model-pinned": {"severity": "extreme"}}}
        with pytest.raises(ValueError, match="Invalid severity"):
            _parse_policy(raw)

    def test_parse_invalid_gate_score_raises(self):
        raw = {"gate": {"min_score": 150}}
        with pytest.raises(ValueError, match="min_score must be 0-100"):
            _parse_policy(raw)

    def test_parse_invalid_gate_fail_on_raises(self):
        raw = {"gate": {"fail_on": "extreme"}}
        with pytest.raises(ValueError, match="Invalid gate.fail_on"):
            _parse_policy(raw)

    def test_load_policy_file(self):
        try:
            import yaml
        except ImportError:
            pytest.skip("PyYAML not installed")

        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".yaml", delete=False
        ) as f:
            yaml.dump(
                {
                    "rules": {"model-pinned": {"severity": "high"}},
                    "gate": {"min_score": 60},
                },
                f,
            )
            f.flush()
            policy = load_policy(f.name)
            assert policy is not None
            assert policy.rules["model-pinned"]["severity"] == "high"
            assert policy.gate_min_score == 60

    def test_load_policy_file_not_found(self):
        with pytest.raises(FileNotFoundError):
            load_policy("/nonexistent/path.yaml")

    def test_load_policy_returns_none_when_no_file(self):
        with tempfile.TemporaryDirectory() as d:
            import os
            orig = os.getcwd()
            os.chdir(d)
            try:
                result = load_policy()
                assert result is None
            finally:
                os.chdir(orig)


class TestOWASPCoverage:
    def test_coverage_all_passing(self):
        results = [
            DefenseResult("prompt-delimiter", True, "t:1", "t:1", "ok", "high", 5, "defense", owasp_llm="LLM01"),
            DefenseResult("no-dangerous-sink", True, "t:1", "t:1", "ok", "critical", 8, "defense", owasp_llm="LLM02"),
        ]
        coverage = compute_owasp_coverage(results)
        assert coverage["LLM01"]["status"] == "covered"
        assert coverage["LLM02"]["status"] == "covered"

    def test_coverage_partial(self):
        results = [
            DefenseResult("prompt-delimiter", True, "t:1", "t:1", "ok", "high", 5, "defense", owasp_llm="LLM01"),
            DefenseResult("input-length-limit", False, "t:1", "t:1", "bad", "low", 1, "defense", owasp_llm="LLM01"),
        ]
        coverage = compute_owasp_coverage(results)
        assert coverage["LLM01"]["status"] == "partial"
        assert coverage["LLM01"]["coverage_pct"] == 50

    def test_coverage_not_applicable(self):
        results = []
        coverage = compute_owasp_coverage(results)
        assert coverage["LLM06"]["status"] == "not_applicable"

    def test_all_owasp_ids_present(self):
        coverage = compute_owasp_coverage([])
        for i in range(1, 11):
            key = f"LLM{i:02d}"
            assert key in coverage


# ---------------------------------------------------------------------------
# Integration tests (end-to-end)
# ---------------------------------------------------------------------------


class TestEndToEnd:
    def test_discover_and_defend_openai(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            (root / "app.py").write_text(
                '''
import openai

client = openai.OpenAI()

def chat(msg):
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": msg}],
    )
    return response.choices[0].message.content
'''
            )

            integrations, graph = detect_integrations(root)
            assert len(integrations) == 1

            results, score, _ops = run_defense_checks(integrations, graph)
            assert len(results) > 0
            assert score.score_pct < 100  # model not pinned, no validation

            # Model-pinned should fail
            mp = [r for r in results if r.plugin_id == "model-pinned"]
            assert len(mp) == 1
            assert mp[0].passed is False

    def test_discover_and_defend_secure_app(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            (root / "app.py").write_text(
                '''
import openai
import json

client = openai.OpenAI()

def chat(msg):
    response = client.chat.completions.create(
        model="gpt-4o-2024-08-06",
        messages=[
            {"role": "system", "content": "You are helpful."},
            {"role": "user", "content": msg},
        ],
    )
    raw = response.choices[0].message.content
    parsed = json.loads(raw)
    return parsed
'''
            )

            integrations, graph = detect_integrations(root)
            assert len(integrations) == 1

            results, score, _ops = run_defense_checks(integrations, graph)

            # Model pinned + output validation should pass
            mp = [r for r in results if r.plugin_id == "model-pinned"]
            assert mp[0].passed is True
            ov = [r for r in results if r.plugin_id == "output-validation"]
            assert ov[0].passed is True

    def test_json_roundtrip(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            (root / "app.py").write_text(
                '''
import openai

client = openai.OpenAI()

def chat(msg):
    return client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": msg}],
    )
'''
            )

            integrations, graph = detect_integrations(root)
            results, score, _ops = run_defense_checks(integrations, graph)

            # JSON output should be valid
            output = format_defense_json(results, score, len(integrations), 1)
            data = json.loads(output)
            assert isinstance(data["summary"]["score_pct"], int)
            assert isinstance(data["findings"], list)

    def test_gating_fail_on_critical(self):
        integ = _make_integration(
            output_sinks=["eval (L45)"],  # triggers no-dangerous-sink (critical)
        )
        results, score, _ops = run_defense_checks([integ], _empty_graph())

        # Check if gating would trigger
        severity_order = {"critical": 4, "high": 3, "medium": 2, "low": 1}
        fail_on = "critical"
        threshold = severity_order[fail_on]
        should_fail = any(
            not r.passed and severity_order.get(r.severity, 0) >= threshold
            for r in results
        )
        assert should_fail is True

    def test_gating_min_score(self):
        integ = _make_integration(
            output_sinks=["eval (L45)"],
            model_value="gpt-4o",
            model_pinned=False,
        )
        results, score, _ops = run_defense_checks([integ], _empty_graph())
        assert score.score_pct < 60  # Should be below threshold

    def test_gating_ignores_ops_results(self):
        """--fail-on should only consider defense results, not ops."""
        integ = _make_integration(
            model_value="gpt-4o-2024-08-06",
            model_pinned=True,
            has_output_validation=True,
            has_logging=False,  # ops failure
            has_max_tokens=False,  # ops failure
        )
        results, score, ops = run_defense_checks([integ], _empty_graph())

        # Ops checks fail
        ops_failures = [r for r in results if r.category == "ops" and not r.passed]
        assert len(ops_failures) > 0

        # But gating on defense only — simulate --fail-on medium
        severity_order = {"critical": 4, "high": 3, "medium": 2, "low": 1}
        threshold = severity_order["medium"]
        should_gate = any(
            r.category == "defense" and not r.passed
            and severity_order.get(r.severity, 0) >= threshold
            for r in results
        )
        # No defense failures at medium+ should exist (model pinned, validation present)
        assert should_gate is False

    def test_policy_does_not_corrupt_plugin_state(self):
        """Verify that policy severity overrides don't mutate shared plugin singletons."""
        integ = _make_integration(model_value="gpt-4o", model_pinned=False)

        # Run with policy that bumps model-pinned to critical
        policy = DefensePolicy(rules={"model-pinned": {"severity": "critical"}})
        results1, _, _ops1 = run_defense_checks([integ], _empty_graph(), policy=policy)
        mp1 = [r for r in results1 if r.plugin_id == "model-pinned"][0]
        assert mp1.severity == "critical"

        # Run WITHOUT policy — should be back to default (medium)
        results2, _, _ops2 = run_defense_checks([integ], _empty_graph())
        mp2 = [r for r in results2 if r.plugin_id == "model-pinned"][0]
        assert mp2.severity == "medium"  # NOT critical

    def test_function_scoped_validation(self):
        """Validation in one function should not affect LLM calls in another function."""
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            (root / "app.py").write_text(
                '''
import openai
import json

client = openai.OpenAI()

def unrelated():
    data = json.loads('{"key": "value"}')
    return data

def chat(msg):
    response = client.chat.completions.create(
        model="gpt-4o-2024-08-06",
        messages=[{"role": "user", "content": msg}],
    )
    return response.choices[0].message.content
'''
            )
            integrations, graph = detect_integrations(root)
            assert len(integrations) == 1
            # json.loads is in unrelated(), not in chat() — should NOT pass
            assert integrations[0].has_output_validation is False

    def test_function_scoped_sinks(self):
        """Sinks in one function should not affect LLM calls in another."""
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            (root / "app.py").write_text(
                '''
import openai
import subprocess

client = openai.OpenAI()

def run_shell(cmd):
    subprocess.run(cmd, shell=True)

def chat(msg):
    response = client.chat.completions.create(
        model="gpt-4o-2024-08-06",
        messages=[{"role": "user", "content": msg}],
    )
    return response.choices[0].message.content
'''
            )
            integrations, graph = detect_integrations(root)
            assert len(integrations) == 1
            # subprocess.run is in run_shell(), not in chat()
            assert len(integrations[0].output_sinks) == 0

    def test_model_pinned_rejects_non_dated_models(self):
        """Models without date suffixes should not be marked as pinned."""
        from skylos.discover.detector import _LLMDetectorVisitor

        visitor = _LLMDetectorVisitor("test.py", "")
        assert visitor._is_model_pinned("llama-3") is False
        assert visitor._is_model_pinned("command-r") is False
        assert visitor._is_model_pinned("mixtral-8x7b") is False
        assert visitor._is_model_pinned("gpt-4o-2024-08-06") is True


# ---------------------------------------------------------------------------
# Phase 3: Extended defense plugin tests
# ---------------------------------------------------------------------------


class TestUntrustedInputToPromptPlugin:
    plugin = UntrustedInputToPromptPlugin()

    def test_not_applicable_without_input_or_prompt(self):
        integ = _make_integration(input_sources=[], prompt_sites=[])
        assert self.plugin.applies_to(integ) is False

    def test_not_applicable_inputs_only(self):
        integ = _make_integration(input_sources=["request.json"], prompt_sites=[])
        assert self.plugin.applies_to(integ) is False

    def test_not_applicable_prompts_only(self):
        integ = _make_integration(input_sources=[], prompt_sites=["t.py:10"])
        assert self.plugin.applies_to(integ) is False

    def test_fails_when_raw_flow(self):
        integ = _make_integration(
            input_sources=["request.json (L5)"],
            prompt_sites=["t.py:10"],
            has_prompt_delimiter=False,
            has_output_validation=False,
            has_input_length_limit=False,
        )
        result = self.plugin.check(integ, _empty_graph())
        assert result.passed is False
        assert result.severity == "critical"
        assert result.owasp_llm == "LLM01"

    def test_passes_with_delimiter(self):
        integ = _make_integration(
            input_sources=["request.json (L5)"],
            prompt_sites=["t.py:10"],
            has_prompt_delimiter=True,
        )
        result = self.plugin.check(integ, _empty_graph())
        assert result.passed is True

    def test_fails_with_only_output_validation(self):
        """Output validation is NOT an input defense — should still fail."""
        integ = _make_integration(
            input_sources=["request.json (L5)"],
            prompt_sites=["t.py:10"],
            has_output_validation=True,
            has_prompt_delimiter=False,
            has_input_length_limit=False,
        )
        result = self.plugin.check(integ, _empty_graph())
        assert result.passed is False

    def test_passes_with_length_limit(self):
        integ = _make_integration(
            input_sources=["request.json (L5)"],
            prompt_sites=["t.py:10"],
            has_input_length_limit=True,
        )
        result = self.plugin.check(integ, _empty_graph())
        assert result.passed is True


class TestRagContextIsolationPlugin:
    plugin = RagContextIsolationPlugin()

    def test_not_applicable_without_rag(self):
        integ = _make_integration(has_rag_context=False)
        assert self.plugin.applies_to(integ) is False

    def test_fails_without_delimiters(self):
        integ = _make_integration(has_rag_context=True, has_prompt_delimiter=False)
        result = self.plugin.check(integ, _empty_graph())
        assert result.passed is False
        assert result.severity == "high"
        assert result.owasp_llm == "LLM01"

    def test_passes_with_delimiters(self):
        integ = _make_integration(has_rag_context=True, has_prompt_delimiter=True)
        result = self.plugin.check(integ, _empty_graph())
        assert result.passed is True


class TestOutputPiiFilterPlugin:
    plugin = OutputPiiFilterPlugin()

    def test_not_applicable_without_input_sources(self):
        integ = _make_integration(input_sources=[])
        assert self.plugin.applies_to(integ) is False

    def test_fails_without_pii_filter(self):
        integ = _make_integration(
            input_sources=["request.json (L5)"],
            has_pii_filter=False,
        )
        result = self.plugin.check(integ, _empty_graph())
        assert result.passed is False
        assert result.severity == "high"
        assert result.owasp_llm == "LLM06"

    def test_passes_with_pii_filter(self):
        integ = _make_integration(
            input_sources=["request.json (L5)"],
            has_pii_filter=True,
        )
        result = self.plugin.check(integ, _empty_graph())
        assert result.passed is True


# ---------------------------------------------------------------------------
# Phase 3: Ops plugin tests
# ---------------------------------------------------------------------------


class TestLoggingPresentPlugin:
    plugin = LoggingPresentPlugin()

    def test_category_is_ops(self):
        assert self.plugin.category == "ops"

    def test_fails_without_logging(self):
        integ = _make_integration(has_logging=False)
        result = self.plugin.check(integ, _empty_graph())
        assert result.passed is False
        assert result.category == "ops"

    def test_passes_with_logging(self):
        integ = _make_integration(has_logging=True)
        result = self.plugin.check(integ, _empty_graph())
        assert result.passed is True


class TestCostControlsPlugin:
    plugin = CostControlsPlugin()

    def test_category_is_ops(self):
        assert self.plugin.category == "ops"

    def test_fails_without_max_tokens(self):
        integ = _make_integration(has_max_tokens=False)
        result = self.plugin.check(integ, _empty_graph())
        assert result.passed is False

    def test_passes_with_max_tokens(self):
        integ = _make_integration(has_max_tokens=True)
        result = self.plugin.check(integ, _empty_graph())
        assert result.passed is True


class TestRateLimitingPlugin:
    plugin = RateLimitingPlugin()

    def test_not_applicable_without_inputs(self):
        integ = _make_integration(input_sources=[])
        assert self.plugin.applies_to(integ) is False

    def test_fails_without_rate_limiting(self):
        integ = _make_integration(
            input_sources=["request.json (L5)"],
            has_rate_limiting=False,
        )
        result = self.plugin.check(integ, _empty_graph())
        assert result.passed is False
        assert result.category == "ops"

    def test_passes_with_rate_limiting(self):
        integ = _make_integration(
            input_sources=["request.json (L5)"],
            has_rate_limiting=True,
        )
        result = self.plugin.check(integ, _empty_graph())
        assert result.passed is True


# ---------------------------------------------------------------------------
# Phase 3: Ops score tests
# ---------------------------------------------------------------------------


class TestOpsScore:
    def test_ops_score_empty(self):
        score = compute_ops_score([])
        assert score.score_pct == 100
        assert score.rating == "EXCELLENT"

    def test_ops_score_all_pass(self):
        results = [
            DefenseResult("logging-present", True, "t:1", "t:1", "ok", "medium", 3, "ops"),
            DefenseResult("cost-controls", True, "t:1", "t:1", "ok", "medium", 3, "ops"),
        ]
        score = compute_ops_score(results)
        assert score.score_pct == 100
        assert score.rating == "EXCELLENT"
        assert score.passed == 2
        assert score.total == 2

    def test_ops_score_mixed(self):
        results = [
            DefenseResult("logging-present", True, "t:1", "t:1", "ok", "medium", 3, "ops"),
            DefenseResult("cost-controls", False, "t:1", "t:1", "bad", "medium", 3, "ops"),
        ]
        score = compute_ops_score(results)
        assert score.score_pct == 50
        assert score.rating == "FAIR"

    def test_ops_score_all_fail(self):
        results = [
            DefenseResult("logging-present", False, "t:1", "t:1", "bad", "medium", 3, "ops"),
            DefenseResult("cost-controls", False, "t:1", "t:1", "bad", "medium", 3, "ops"),
            DefenseResult("rate-limiting", False, "t:1", "t:1", "bad", "medium", 3, "ops"),
        ]
        score = compute_ops_score(results)
        assert score.score_pct == 0
        assert score.rating == "POOR"

    def test_ops_score_excludes_defense(self):
        results = [
            DefenseResult("model-pinned", True, "t:1", "t:1", "ok", "medium", 3, "defense"),
            DefenseResult("logging-present", False, "t:1", "t:1", "bad", "medium", 3, "ops"),
        ]
        score = compute_ops_score(results)
        assert score.total == 1
        assert score.passed == 0

    def test_ops_score_rating_boundaries(self):
        # 80% = EXCELLENT
        results = [
            DefenseResult("a", True, "t:1", "t:1", "ok", "medium", 3, "ops"),
            DefenseResult("b", True, "t:1", "t:1", "ok", "medium", 3, "ops"),
            DefenseResult("c", True, "t:1", "t:1", "ok", "medium", 3, "ops"),
            DefenseResult("d", True, "t:1", "t:1", "ok", "medium", 3, "ops"),
            DefenseResult("e", False, "t:1", "t:1", "bad", "medium", 3, "ops"),
        ]
        score = compute_ops_score(results)
        assert score.rating == "EXCELLENT"  # 4/5 = 80%

        # 60% = GOOD
        results = [
            DefenseResult("a", True, "t:1", "t:1", "ok", "medium", 3, "ops"),
            DefenseResult("b", True, "t:1", "t:1", "ok", "medium", 3, "ops"),
            DefenseResult("c", True, "t:1", "t:1", "ok", "medium", 3, "ops"),
            DefenseResult("d", False, "t:1", "t:1", "bad", "medium", 3, "ops"),
            DefenseResult("e", False, "t:1", "t:1", "bad", "medium", 3, "ops"),
        ]
        score = compute_ops_score(results)
        assert score.rating == "GOOD"  # 3/5 = 60%

        # 40% = FAIR
        results = [
            DefenseResult("a", True, "t:1", "t:1", "ok", "medium", 3, "ops"),
            DefenseResult("b", True, "t:1", "t:1", "ok", "medium", 3, "ops"),
            DefenseResult("c", False, "t:1", "t:1", "bad", "medium", 3, "ops"),
            DefenseResult("d", False, "t:1", "t:1", "bad", "medium", 3, "ops"),
            DefenseResult("e", False, "t:1", "t:1", "bad", "medium", 3, "ops"),
        ]
        score = compute_ops_score(results)
        assert score.rating == "FAIR"  # 2/5 = 40%

        # <40% = POOR
        results = [
            DefenseResult("a", True, "t:1", "t:1", "ok", "medium", 3, "ops"),
            DefenseResult("b", False, "t:1", "t:1", "bad", "medium", 3, "ops"),
            DefenseResult("c", False, "t:1", "t:1", "bad", "medium", 3, "ops"),
            DefenseResult("d", False, "t:1", "t:1", "bad", "medium", 3, "ops"),
            DefenseResult("e", False, "t:1", "t:1", "bad", "medium", 3, "ops"),
        ]
        score = compute_ops_score(results)
        assert score.rating == "POOR"  # 1/5 = 20%


# ---------------------------------------------------------------------------
# Phase 3: Detection integration tests
# ---------------------------------------------------------------------------


class TestPhase3Detection:
    def test_max_tokens_detected(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            (root / "app.py").write_text(
                '''
import openai

client = openai.OpenAI()

def chat(msg):
    response = client.chat.completions.create(
        model="gpt-4o-2024-08-06",
        messages=[{"role": "user", "content": msg}],
        max_tokens=1000,
    )
    return response.choices[0].message.content
'''
            )
            integrations, graph = detect_integrations(root)
            assert len(integrations) == 1
            assert integrations[0].has_max_tokens is True

    def test_max_tokens_not_detected(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            (root / "app.py").write_text(
                '''
import openai

client = openai.OpenAI()

def chat(msg):
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": msg}],
    )
    return response.choices[0].message.content
'''
            )
            integrations, graph = detect_integrations(root)
            assert len(integrations) == 1
            assert integrations[0].has_max_tokens is False

    def test_logging_detected(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            (root / "app.py").write_text(
                '''
import openai
import logging

logger = logging.getLogger(__name__)
client = openai.OpenAI()

def chat(msg):
    logger.info("Processing request")
    response = client.chat.completions.create(
        model="gpt-4o-2024-08-06",
        messages=[{"role": "user", "content": msg}],
    )
    logger.info("Got response")
    return response.choices[0].message.content
'''
            )
            integrations, graph = detect_integrations(root)
            assert len(integrations) == 1
            assert integrations[0].has_logging is True

    def test_logging_not_detected_in_different_function(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            (root / "app.py").write_text(
                '''
import openai
import logging

logger = logging.getLogger(__name__)
client = openai.OpenAI()

def log_stuff():
    logger.info("Logging in a different function")

def chat(msg):
    response = client.chat.completions.create(
        model="gpt-4o-2024-08-06",
        messages=[{"role": "user", "content": msg}],
    )
    return response.choices[0].message.content
'''
            )
            integrations, graph = detect_integrations(root)
            assert len(integrations) == 1
            assert integrations[0].has_logging is False

    def test_rate_limiting_decorator_detected(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            (root / "app.py").write_text(
                '''
import openai
from slowapi import Limiter

limiter = Limiter()
client = openai.OpenAI()

@limiter.limit("10/minute")
def chat(msg):
    response = client.chat.completions.create(
        model="gpt-4o-2024-08-06",
        messages=[{"role": "user", "content": msg}],
    )
    return response.choices[0].message.content
'''
            )
            integrations, graph = detect_integrations(root)
            assert len(integrations) == 1
            assert integrations[0].has_rate_limiting is True

    def test_rag_detection(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            (root / "app.py").write_text(
                '''
import openai
import chromadb

client = openai.OpenAI()
chroma = chromadb.Client()
collection = chroma.get_or_create_collection("docs")

def rag_chat(msg):
    docs = collection.query(query_texts=[msg], n_results=3)
    context = "\\n".join(docs["documents"][0])
    response = client.chat.completions.create(
        model="gpt-4o-2024-08-06",
        messages=[
            {"role": "system", "content": f"Context: {context}"},
            {"role": "user", "content": msg},
        ],
    )
    return response.choices[0].message.content
'''
            )
            integrations, graph = detect_integrations(root)
            assert len(integrations) == 1
            assert integrations[0].has_rag_context is True

    def test_rag_not_detected_in_different_function(self):
        """RAG call in function A should not affect LLM call in function B."""
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            (root / "app.py").write_text(
                '''
import openai
import chromadb

client = openai.OpenAI()
chroma = chromadb.Client()

def index_docs():
    collection = chroma.get_or_create_collection("docs")
    collection.query(query_texts=["test"], n_results=3)

def plain_chat(msg):
    response = client.chat.completions.create(
        model="gpt-4o-2024-08-06",
        messages=[{"role": "user", "content": msg}],
    )
    return response.choices[0].message.content
'''
            )
            integrations, graph = detect_integrations(root)
            assert len(integrations) == 1
            # RAG is in index_docs(), LLM is in plain_chat() — should NOT inherit
            assert integrations[0].has_rag_context is False

    def test_pii_filter_detection(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            (root / "app.py").write_text(
                '''
import openai
from presidio_analyzer import AnalyzerEngine
from presidio_anonymizer import AnonymizerEngine

client = openai.OpenAI()
analyzer = AnalyzerEngine()
anonymizer = AnonymizerEngine()

def chat(msg):
    response = client.chat.completions.create(
        model="gpt-4o-2024-08-06",
        messages=[{"role": "user", "content": msg}],
    )
    text = response.choices[0].message.content
    results = analyzer.analyze(text=text, language="en")
    cleaned = anonymizer.anonymize(text=text, analyzer_results=results)
    return cleaned.text
'''
            )
            integrations, graph = detect_integrations(root)
            assert len(integrations) == 1
            assert integrations[0].has_pii_filter is True

    def test_variable_model_resolution(self):
        """Model stored in a variable should be resolved for pinning check."""
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            (root / "app.py").write_text(
                '''
import openai

MODEL = "gpt-4o-2024-08-06"
client = openai.OpenAI()

def chat(msg):
    response = client.chat.completions.create(
        model=MODEL,
        messages=[{"role": "user", "content": msg}],
    )
    return response.choices[0].message.content
'''
            )
            integrations, graph = detect_integrations(root)
            assert len(integrations) == 1
            assert integrations[0].model_value == "gpt-4o-2024-08-06"
            assert integrations[0].model_pinned is True

    def test_ops_score_in_report(self):
        """Ops score should appear in table output when ops checks exist."""
        results = [
            DefenseResult("model-pinned", True, "t.py:10", "t.py:10", "ok", "medium", 3, "defense", owasp_llm="LLM03"),
            DefenseResult("logging-present", False, "t.py:10", "t.py:10", "no logging", "medium", 3, "ops"),
            DefenseResult("cost-controls", True, "t.py:10", "t.py:10", "ok", "medium", 3, "ops"),
        ]
        score = compute_defense_score(results)
        ops = compute_ops_score(results)
        output = format_defense_table(results, score, 1, 10, ops_score=ops)
        assert "AI Defense Score" in output
        assert "AI Ops Score" in output
        assert "50%" in output  # ops: 1/2 = 50%

    def test_ops_score_in_json(self):
        """Ops score should appear in JSON output."""
        results = [
            DefenseResult("model-pinned", True, "t.py:10", "t.py:10", "ok", "medium", 3, "defense"),
            DefenseResult("logging-present", False, "t.py:10", "t.py:10", "bad", "medium", 3, "ops"),
        ]
        score = compute_defense_score(results)
        ops = compute_ops_score(results)
        output = format_defense_json(results, score, 1, 10, ops_score=ops)
        data = json.loads(output)
        assert "ops_score" in data
        assert data["ops_score"]["passed"] == 0
        assert data["ops_score"]["total"] == 1

    def test_engine_returns_ops_score(self):
        """Engine should return ops score as third element."""
        integ = _make_integration(
            model_value="gpt-4o",
            has_logging=False,
            has_max_tokens=False,
        )
        results, score, ops = run_defense_checks([integ], _empty_graph())
        assert isinstance(ops, OpsScore)
        # At minimum cost-controls and logging-present should run
        ops_results = [r for r in results if r.category == "ops"]
        assert len(ops_results) >= 2

    def test_all_plugins_registered(self):
        """All 13 plugins should be registered."""
        assert len(ALL_PLUGINS) == 13
        ids = {p.id for p in ALL_PLUGINS}
        assert "untrusted-input-to-prompt" in ids
        assert "rag-context-isolation" in ids
        assert "output-pii-filter" in ids
        assert "logging-present" in ids
        assert "cost-controls" in ids
        assert "rate-limiting" in ids

    def test_owasp_mapping_updated(self):
        """OWASP mapping should include Phase 3 plugins."""
        assert "untrusted-input-to-prompt" in OWASP_LLM_MAPPING["LLM01"]["plugins"]
        assert "rag-context-isolation" in OWASP_LLM_MAPPING["LLM01"]["plugins"]
        assert "output-pii-filter" in OWASP_LLM_MAPPING["LLM06"]["plugins"]
        assert "cost-controls" in OWASP_LLM_MAPPING["LLM10"]["plugins"]

    def test_policy_accepts_phase3_plugins(self):
        """Policy parser should accept Phase 3 plugin IDs."""
        raw = {
            "rules": {
                "untrusted-input-to-prompt": {"severity": "high"},
                "logging-present": {"enabled": False},
                "cost-controls": {"severity": "high"},
            },
        }
        policy = _parse_policy(raw)
        assert "untrusted-input-to-prompt" in policy.rules

    def test_end_to_end_full_scan(self):
        """Full scan with all Phase 3 features."""
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            (root / "app.py").write_text(
                '''
import openai
import logging
from flask import request

logger = logging.getLogger(__name__)
client = openai.OpenAI()

def chat():
    msg = request.get_json()["message"]
    if len(msg) > 10000:
        return {"error": "too long"}, 400
    logger.info("Processing chat request")
    prompt = f"""<user_input>{msg}</user_input>
Answer the user's question."""
    response = client.chat.completions.create(
        model="gpt-4o-2024-08-06",
        messages=[
            {"role": "system", "content": "You are helpful."},
            {"role": "user", "content": prompt},
        ],
        max_tokens=2000,
    )
    return response.choices[0].message.content
'''
            )
            integrations, graph = detect_integrations(root)
            assert len(integrations) == 1

            results, score, ops = run_defense_checks(integrations, graph)

            # Defense checks
            defense_results = [r for r in results if r.category == "defense"]
            assert len(defense_results) > 0

            # Model should be pinned
            mp = [r for r in results if r.plugin_id == "model-pinned"]
            assert mp[0].passed is True

            # Ops checks
            ops_results = [r for r in results if r.category == "ops"]
            assert len(ops_results) > 0

            # Logging should pass
            log = [r for r in results if r.plugin_id == "logging-present"]
            assert log[0].passed is True

            # Cost controls should pass (max_tokens set)
            cc = [r for r in results if r.plugin_id == "cost-controls"]
            assert cc[0].passed is True
