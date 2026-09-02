"""Tests for agdt.run-setup.agent.md frontmatter and content validation."""

from __future__ import annotations

from pathlib import Path

import yaml

_REPO_ROOT = Path(__file__).resolve().parents[3]
_AGENT_FILE = _REPO_ROOT / ".github" / "agents" / "agdt.run-setup.agent.md"


def _load_frontmatter() -> dict:
    """Parse YAML frontmatter from the agent file."""
    content = _AGENT_FILE.read_text(encoding="utf-8")
    assert content.startswith("---"), "File must start with YAML frontmatter delimiter"
    lines = content.splitlines()
    close_idx = next(i for i, line in enumerate(lines) if i > 0 and line == "---")
    fm_text = "\n".join(lines[1:close_idx])
    return yaml.safe_load(fm_text)


class TestOrchestratorAgentFrontmatter:
    """Validate agdt.run-setup.agent.md frontmatter."""

    def test_frontmatter_is_parseable(self) -> None:
        """YAML frontmatter parses without error."""
        fm = _load_frontmatter()
        assert isinstance(fm, dict)

    def test_has_description(self) -> None:
        """Frontmatter includes a description field."""
        fm = _load_frontmatter()
        assert "description" in fm
        assert isinstance(fm["description"], str)
        assert len(fm["description"]) > 0

    def test_agdt_always_is_true(self) -> None:
        """Frontmatter has agdt.always set to true (FR-009)."""
        fm = _load_frontmatter()
        assert "agdt" in fm
        assert isinstance(fm["agdt"], dict)
        assert fm["agdt"].get("always") is True


class TestOrchestratorAgentContent:
    """Validate agdt.run-setup.agent.md required sections and content."""

    def test_has_user_input_section(self) -> None:
        """File contains a User Input section."""
        content = _AGENT_FILE.read_text(encoding="utf-8")
        assert "## User Input" in content

    def test_has_purpose_section(self) -> None:
        """File contains a Purpose section."""
        content = _AGENT_FILE.read_text(encoding="utf-8")
        assert "## Purpose" in content

    def test_has_actions_section(self) -> None:
        """File contains an Actions section."""
        content = _AGENT_FILE.read_text(encoding="utf-8")
        assert "## Actions" in content

    def test_references_agdt_setup_invocation(self) -> None:
        """Orchestrator references the canonical agdt-setup command (FR-001)."""
        content = _AGENT_FILE.read_text(encoding="utf-8")
        assert "agdt-setup" in content

    def test_references_fix_loop_caps(self) -> None:
        """Orchestrator references fix-loop caps (NFR-002)."""
        content = _AGENT_FILE.read_text(encoding="utf-8")
        assert "MAX_ATTEMPTS_PER_CLASS" in content
        assert "MAX_TOTAL_ITERATIONS" in content

    def test_references_re_exec(self) -> None:
        """Orchestrator references re_exec handling (FR-002)."""
        content = _AGENT_FILE.read_text(encoding="utf-8")
        assert "re_exec" in content

    def test_re_exec_false_requires_fresh_setup_run(self) -> None:
        """re_exec=false branch instructs a fresh agdt-setup run next iteration."""
        content = _AGENT_FILE.read_text(encoding="utf-8")
        assert "If `re_exec` is false" in content
        assert "run `agdt-setup` first to produce a fresh outcome" in content

    def test_fix_loop_treats_success_error_class_as_terminal(self) -> None:
        """Fix-loop instructions treat ErrorClass.SUCCESS as terminal."""
        content = _AGENT_FILE.read_text(encoding="utf-8")
        assert "If `error_class` is `ErrorClass.SUCCESS`" in content
        assert "skip `fixloop.next_action(...)` for this iteration" in content

    def test_references_decision_log_append(self) -> None:
        """Orchestrator references decision-log append (FR-003)."""
        content = _AGENT_FILE.read_text(encoding="utf-8")
        assert "agdt-setup-decision-log append" in content

    def test_references_decision_log_show(self) -> None:
        """Orchestrator references unconditional decision-log show (FR-003)."""
        content = _AGENT_FILE.read_text(encoding="utf-8")
        assert "agdt-setup-decision-log show" in content

    def test_give_up_rationale_is_concrete(self) -> None:
        """Give-up decision log entry distinguishes cap-reached vs permanent failure."""
        content = _AGENT_FILE.read_text(encoding="utf-8")
        assert '--rationale "{reason}"' not in content
        assert "retry cap reached" in content
        assert "permanent failure: {error_class}" in content
        assert "non-retryable or retry caps were reached" not in content

    def test_bug_reporter_invocation_is_centralized_in_step_6(self) -> None:
        """Give-up branch defers bug reporter invocation to Step 6."""
        content = _AGENT_FILE.read_text(encoding="utf-8")
        assert "Proceed to Step 5 (decision log show), then invoke `/agdt.report-setup-bug`." not in content
        assert "Step 6 handles invoking" in content

    def test_apply_remedy_decision_uses_fixaction_remedy_field(self) -> None:
        """Apply-remedy decision log entry uses the FixAction remedy field."""
        content = _AGENT_FILE.read_text(encoding="utf-8")
        assert '--decision "apply_remedy: {remedy}"' in content
        assert "{remedy_description}" not in content

    def test_tty_detection_example_uses_portable_python_command(self) -> None:
        """TTY detection example uses python instead of python3 for portability."""
        content = _AGENT_FILE.read_text(encoding="utf-8")
        assert 'python -c "import sys; print(sys.stdin.isatty())"' in content
        assert 'python3 -c "import sys; print(sys.stdin.isatty())"' not in content

    def test_references_feature_reporter_gating(self) -> None:
        """Orchestrator references feature reporter gating on satisfaction (FR-006)."""
        content = _AGENT_FILE.read_text(encoding="utf-8")
        assert "agdt.report-setup-feature" in content
        assert "satisfied" in content.lower()

    def test_references_error_class_step_values(self) -> None:
        """Decision log entries record the error class in --step."""
        content = _AGENT_FILE.read_text(encoding="utf-8")
        assert '--step "{error_class}"' in content

    def test_references_bug_reporter(self) -> None:
        """Orchestrator references bug reporter invocation on failure."""
        content = _AGENT_FILE.read_text(encoding="utf-8")
        assert "agdt.report-setup-bug" in content

    def test_step_3_1_uses_canonical_classify_outcome(self) -> None:
        """Step 3.1 uses classify_outcome from fixloop, not ad-hoc parsing (FR-003)."""
        content = _AGENT_FILE.read_text(encoding="utf-8")
        assert "classify_outcome(report, exit_code, stdout)" in content
        assert "agentic_devtools.cli.setup.fixloop" in content

    def test_step_3_1_clarifies_report_shape_for_classification(self) -> None:
        """Step 3.1 clarifies report is optional/classifier-oriented, not raw setup output."""
        content = _AGENT_FILE.read_text(encoding="utf-8")
        assert "small classifier-input dict" in content
        assert "contains `error_class`" in content
        assert "only when available" in content
