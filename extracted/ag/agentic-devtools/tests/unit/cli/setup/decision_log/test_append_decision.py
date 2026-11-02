"""Tests for append_decision in agentic_devtools.cli.setup.decision_log."""

from pathlib import Path
from unittest.mock import patch

import pytest

from agentic_devtools.cli.setup.decision_log import (
    DecisionEntry,
    append_decision,
)


def _make_entry(**kwargs: object) -> DecisionEntry:
    """Create a valid DecisionEntry with defaults overridden by kwargs."""
    defaults: dict[str, object] = {
        "step": "install-deps",
        "question": "npm unreachable?",
        "decision": "Skip optional packages",
        "rationale": "Registry timeout after 30s",
        "auto_resolved": True,
    }
    defaults.update(kwargs)
    return DecisionEntry(**defaults)  # type: ignore[arg-type]


class TestAppendDecisionValidation:
    """Negative/edge-case validation tests for append_decision."""

    def test_empty_step_raises_valueerror(self, tmp_path: Path) -> None:
        """Empty required field raises ValueError."""
        with patch(
            "agentic_devtools.cli.setup.decision_log.get_state_dir",
            return_value=tmp_path,
        ):
            with pytest.raises(ValueError, match="step must not be empty"):
                append_decision(_make_entry(step=""))

    def test_whitespace_step_raises_valueerror(self, tmp_path: Path) -> None:
        """Whitespace-only field raises ValueError."""
        with patch(
            "agentic_devtools.cli.setup.decision_log.get_state_dir",
            return_value=tmp_path,
        ):
            with pytest.raises(ValueError, match="step must not be empty"):
                append_decision(_make_entry(step="   "))

    def test_field_exceeds_max_bytes_raises_valueerror(self, tmp_path: Path) -> None:
        """Field > 2000 UTF-8 bytes raises ValueError."""
        long_value = "a" * 2001
        with patch(
            "agentic_devtools.cli.setup.decision_log.get_state_dir",
            return_value=tmp_path,
        ):
            with pytest.raises(ValueError, match="exceeds maximum"):
                append_decision(_make_entry(question=long_value))

    def test_field_with_newline_raises_valueerror(self, tmp_path: Path) -> None:
        """Field containing newline raises ValueError."""
        with patch(
            "agentic_devtools.cli.setup.decision_log.get_state_dir",
            return_value=tmp_path,
        ):
            with pytest.raises(ValueError, match="must not contain newline"):
                append_decision(_make_entry(decision="line1\nline2"))

    def test_field_with_carriage_return_raises_valueerror(self, tmp_path: Path) -> None:
        """Field containing carriage return raises ValueError."""
        with patch(
            "agentic_devtools.cli.setup.decision_log.get_state_dir",
            return_value=tmp_path,
        ):
            with pytest.raises(ValueError, match="must not contain newline"):
                append_decision(_make_entry(rationale="line1\rline2"))

    def test_field_with_start_marker_raises_valueerror(self, tmp_path: Path) -> None:
        """Field containing start marker substring raises ValueError."""
        with patch(
            "agentic_devtools.cli.setup.decision_log.get_state_dir",
            return_value=tmp_path,
        ):
            with pytest.raises(ValueError, match="must not contain marker"):
                append_decision(_make_entry(step="<!-- agdt-decision-entry:start id:1 -->"))

    def test_field_with_end_marker_raises_valueerror(self, tmp_path: Path) -> None:
        """Field containing end marker substring raises ValueError."""
        with patch(
            "agentic_devtools.cli.setup.decision_log.get_state_dir",
            return_value=tmp_path,
        ):
            with pytest.raises(ValueError, match="must not contain marker"):
                append_decision(_make_entry(question="<!-- agdt-decision-entry:end -->"))

    def test_field_with_partial_end_marker_raises_valueerror(self, tmp_path: Path) -> None:
        """Field containing partial end marker substring raises ValueError."""
        with patch(
            "agentic_devtools.cli.setup.decision_log.get_state_dir",
            return_value=tmp_path,
        ):
            with pytest.raises(ValueError, match="must not contain marker"):
                append_decision(_make_entry(question="<!-- agdt-decision-entry:end"))

    def test_auto_resolved_not_bool_raises_typeerror(self, tmp_path: Path) -> None:
        """auto_resolved not bool raises TypeError."""
        entry = DecisionEntry(
            step="s",
            question="q",
            decision="d",
            rationale="r",
            auto_resolved="yes",  # type: ignore[arg-type]
        )
        with patch(
            "agentic_devtools.cli.setup.decision_log.get_state_dir",
            return_value=tmp_path,
        ):
            with pytest.raises(TypeError, match="auto_resolved must be a bool"):
                append_decision(entry)

    def test_non_string_field_raises_valueerror(self, tmp_path: Path) -> None:
        """Non-string text field raises ValueError."""
        entry = DecisionEntry(
            step=123,  # type: ignore[arg-type]
            question="q",
            decision="d",
            rationale="r",
            auto_resolved=True,
        )
        with patch(
            "agentic_devtools.cli.setup.decision_log.get_state_dir",
            return_value=tmp_path,
        ):
            with pytest.raises(ValueError, match="step must be a string"):
                append_decision(entry)


class TestAppendDecisionHappyPath:
    """Happy-path tests for append_decision."""

    def test_first_entry_creates_file_with_id_1(self, tmp_path: Path) -> None:
        """First entry on missing log creates file with id 1."""
        with patch(
            "agentic_devtools.cli.setup.decision_log.get_state_dir",
            return_value=tmp_path,
        ):
            result = append_decision(_make_entry())
            assert result == 1
            log_path = tmp_path / "setup" / "run-setup-decision-log.md"
            assert log_path.exists()
            content = log_path.read_text(encoding="utf-8")
            assert "<!-- agdt-decision-entry:start id:1 -->" in content
            assert "<!-- agdt-decision-entry:end -->" in content

    def test_append_to_existing_assigns_next_id(self, tmp_path: Path) -> None:
        """Append to log with N entries assigns id N+1."""
        setup_dir = tmp_path / "setup"
        setup_dir.mkdir(parents=True)
        existing = (
            "<!-- agdt-decision-entry:start id:1 -->\n"
            "### Decision #1 (2026-07-08T18:30:00+00:00)\n"
            "- Step: step1\n"
            "- Question: q1\n"
            "- Decision: d1\n"
            "- Rationale: r1\n"
            "- Auto-resolved: true\n"
            "<!-- agdt-decision-entry:end -->\n"
        )
        (setup_dir / "run-setup-decision-log.md").write_text(existing, encoding="utf-8")

        with patch(
            "agentic_devtools.cli.setup.decision_log.get_state_dir",
            return_value=tmp_path,
        ):
            result = append_decision(_make_entry())
            assert result == 2
            content = (setup_dir / "run-setup-decision-log.md").read_text(encoding="utf-8")
            assert "<!-- agdt-decision-entry:start id:2 -->" in content

    def test_ten_sequential_appends(self, tmp_path: Path) -> None:
        """10 sequential appends produce correct ids with no corruption."""
        with patch(
            "agentic_devtools.cli.setup.decision_log.get_state_dir",
            return_value=tmp_path,
        ):
            for i in range(1, 11):
                result = append_decision(_make_entry(step=f"step-{i}"))
                assert result == i

            log_path = tmp_path / "setup" / "run-setup-decision-log.md"
            content = log_path.read_text(encoding="utf-8")
            for i in range(1, 11):
                assert f"<!-- agdt-decision-entry:start id:{i} -->" in content
                assert f"### Decision #{i}" in content

    def test_auto_resolved_false_renders_correctly(self, tmp_path: Path) -> None:
        """auto_resolved=False is rendered as 'false'."""
        with patch(
            "agentic_devtools.cli.setup.decision_log.get_state_dir",
            return_value=tmp_path,
        ):
            append_decision(_make_entry(auto_resolved=False))
            log_path = tmp_path / "setup" / "run-setup-decision-log.md"
            content = log_path.read_text(encoding="utf-8")
            assert "- Auto-resolved: false" in content

    def test_append_to_file_not_ending_with_newline(self, tmp_path: Path) -> None:
        """Append to file that does not end with newline adds separator."""
        setup_dir = tmp_path / "setup"
        setup_dir.mkdir(parents=True)
        existing = (
            "<!-- agdt-decision-entry:start id:1 -->\n"
            "### Decision #1 (2026-07-08T18:30:00+00:00)\n"
            "- Step: step1\n"
            "- Question: q1\n"
            "- Decision: d1\n"
            "- Rationale: r1\n"
            "- Auto-resolved: true\n"
            "<!-- agdt-decision-entry:end -->"  # no trailing newline
        )
        (setup_dir / "run-setup-decision-log.md").write_text(existing, encoding="utf-8")

        with patch(
            "agentic_devtools.cli.setup.decision_log.get_state_dir",
            return_value=tmp_path,
        ):
            result = append_decision(_make_entry())
            assert result == 2
            content = (setup_dir / "run-setup-decision-log.md").read_text(encoding="utf-8")
            # Should have newline separating old and new entry
            assert "<!-- agdt-decision-entry:end -->\n<!-- agdt-decision-entry:start id:2 -->" in content


class TestAppendDecisionIntegrity:
    """Integrity validation tests for append_decision."""

    def test_incomplete_trailing_entry_raises_valueerror(self, tmp_path: Path) -> None:
        """Incomplete trailing entry (missing end marker) raises ValueError."""
        setup_dir = tmp_path / "setup"
        setup_dir.mkdir(parents=True)
        incomplete = (
            "<!-- agdt-decision-entry:start id:1 -->\n### Decision #1 (2026-07-08T18:30:00+00:00)\n- Step: step1\n"
        )
        log_path = setup_dir / "run-setup-decision-log.md"
        log_path.write_text(incomplete, encoding="utf-8")
        original_bytes = log_path.read_bytes()

        with patch(
            "agentic_devtools.cli.setup.decision_log.get_state_dir",
            return_value=tmp_path,
        ):
            with pytest.raises(ValueError, match="Incomplete trailing entry"):
                append_decision(_make_entry())
            # File unchanged
            assert log_path.read_bytes() == original_bytes

    def test_duplicate_ids_raises_valueerror(self, tmp_path: Path) -> None:
        """Duplicate ids raises ValueError."""
        setup_dir = tmp_path / "setup"
        setup_dir.mkdir(parents=True)
        content = (
            "<!-- agdt-decision-entry:start id:1 -->\n"
            "### Decision #1\n"
            "<!-- agdt-decision-entry:end -->\n"
            "<!-- agdt-decision-entry:start id:1 -->\n"
            "### Decision #1 again\n"
            "<!-- agdt-decision-entry:end -->\n"
        )
        log_path = setup_dir / "run-setup-decision-log.md"
        log_path.write_text(content, encoding="utf-8")
        original_bytes = log_path.read_bytes()

        with patch(
            "agentic_devtools.cli.setup.decision_log.get_state_dir",
            return_value=tmp_path,
        ):
            with pytest.raises(ValueError, match="Duplicate entry IDs"):
                append_decision(_make_entry())
            assert log_path.read_bytes() == original_bytes

    def test_stray_end_marker_raises_valueerror(self, tmp_path: Path) -> None:
        """Stray end marker (end_count > start_count) raises ValueError and leaves file unchanged."""
        setup_dir = tmp_path / "setup"
        setup_dir.mkdir(parents=True)
        content = "<!-- agdt-decision-entry:end -->\n"
        log_path = setup_dir / "run-setup-decision-log.md"
        log_path.write_text(content, encoding="utf-8")
        original_bytes = log_path.read_bytes()

        with patch(
            "agentic_devtools.cli.setup.decision_log.get_state_dir",
            return_value=tmp_path,
        ):
            with pytest.raises(ValueError, match="stray end marker"):
                append_decision(_make_entry())
            # File unchanged
            assert log_path.read_bytes() == original_bytes

    def test_gap_in_ids_raises_valueerror(self, tmp_path: Path) -> None:
        """Gap in id sequence raises ValueError."""
        setup_dir = tmp_path / "setup"
        setup_dir.mkdir(parents=True)
        content = (
            "<!-- agdt-decision-entry:start id:1 -->\n"
            "### Decision #1\n"
            "<!-- agdt-decision-entry:end -->\n"
            "<!-- agdt-decision-entry:start id:3 -->\n"
            "### Decision #3\n"
            "<!-- agdt-decision-entry:end -->\n"
        )
        log_path = setup_dir / "run-setup-decision-log.md"
        log_path.write_text(content, encoding="utf-8")
        original_bytes = log_path.read_bytes()

        with patch(
            "agentic_devtools.cli.setup.decision_log.get_state_dir",
            return_value=tmp_path,
        ):
            with pytest.raises(ValueError, match="Gap in entry ID sequence"):
                append_decision(_make_entry())
            assert log_path.read_bytes() == original_bytes

    def test_malformed_start_marker_raises_valueerror(self, tmp_path: Path) -> None:
        """Malformed marker-like start substring raises ValueError and leaves file unchanged."""
        setup_dir = tmp_path / "setup"
        setup_dir.mkdir(parents=True)
        content = "<!-- agdt-decision-entry:start id:\n"
        log_path = setup_dir / "run-setup-decision-log.md"
        log_path.write_text(content, encoding="utf-8")
        original_bytes = log_path.read_bytes()

        with patch(
            "agentic_devtools.cli.setup.decision_log.get_state_dir",
            return_value=tmp_path,
        ):
            with pytest.raises(ValueError, match="Malformed marker sequence"):
                append_decision(_make_entry())
            assert log_path.read_bytes() == original_bytes

    def test_malformed_start_marker_with_closed_delimiter_raises_valueerror(
        self,
        tmp_path: Path,
    ) -> None:
        """Malformed marker with closing delimiter raises ValueError and leaves file unchanged."""
        setup_dir = tmp_path / "setup"
        setup_dir.mkdir(parents=True)
        content = "<!-- agdt-decision-entry:start id: -->\n"
        log_path = setup_dir / "run-setup-decision-log.md"
        log_path.write_text(content, encoding="utf-8")
        original_bytes = log_path.read_bytes()

        with patch(
            "agentic_devtools.cli.setup.decision_log.get_state_dir",
            return_value=tmp_path,
        ):
            with pytest.raises(ValueError, match="Malformed marker sequence"):
                append_decision(_make_entry())
            assert log_path.read_bytes() == original_bytes

    def test_truncated_end_marker_alone_raises_valueerror(self, tmp_path: Path) -> None:
        """Truncated end marker (missing closing -->) with no other markers raises ValueError."""
        setup_dir = tmp_path / "setup"
        setup_dir.mkdir(parents=True)
        content = "<!-- agdt-decision-entry:end\n"
        log_path = setup_dir / "run-setup-decision-log.md"
        log_path.write_text(content, encoding="utf-8")
        original_bytes = log_path.read_bytes()

        with patch(
            "agentic_devtools.cli.setup.decision_log.get_state_dir",
            return_value=tmp_path,
        ):
            with pytest.raises(ValueError, match="Malformed marker sequence"):
                append_decision(_make_entry())
            assert log_path.read_bytes() == original_bytes

    def test_truncated_end_marker_after_complete_entry_raises_valueerror(self, tmp_path: Path) -> None:
        """Truncated end marker after a complete entry raises ValueError and leaves file unchanged."""
        setup_dir = tmp_path / "setup"
        setup_dir.mkdir(parents=True)
        content = (
            "<!-- agdt-decision-entry:start id:1 -->\n"
            "### Decision #1\n"
            "<!-- agdt-decision-entry:end -->\n"
            "<!-- agdt-decision-entry:end\n"
        )
        log_path = setup_dir / "run-setup-decision-log.md"
        log_path.write_text(content, encoding="utf-8")
        original_bytes = log_path.read_bytes()

        with patch(
            "agentic_devtools.cli.setup.decision_log.get_state_dir",
            return_value=tmp_path,
        ):
            with pytest.raises(ValueError, match="Malformed marker sequence"):
                append_decision(_make_entry())
            assert log_path.read_bytes() == original_bytes

    def test_nested_start_markers_raises_valueerror(self, tmp_path: Path) -> None:
        """Nested start markers are rejected and file remains unchanged."""
        setup_dir = tmp_path / "setup"
        setup_dir.mkdir(parents=True)
        content = (
            "<!-- agdt-decision-entry:start id:1 -->\n"
            "<!-- agdt-decision-entry:start id:2 -->\n"
            "<!-- agdt-decision-entry:end -->\n"
            "<!-- agdt-decision-entry:end -->\n"
        )
        log_path = setup_dir / "run-setup-decision-log.md"
        log_path.write_text(content, encoding="utf-8")
        original_bytes = log_path.read_bytes()

        with patch(
            "agentic_devtools.cli.setup.decision_log.get_state_dir",
            return_value=tmp_path,
        ):
            with pytest.raises(ValueError, match="nested start marker"):
                append_decision(_make_entry())
            assert log_path.read_bytes() == original_bytes

    def test_end_marker_before_first_start_raises_valueerror(self, tmp_path: Path) -> None:
        """End marker before first start marker is rejected and file remains unchanged."""
        setup_dir = tmp_path / "setup"
        setup_dir.mkdir(parents=True)
        content = "<!-- agdt-decision-entry:end -->\n<!-- agdt-decision-entry:start id:1 -->\n"
        log_path = setup_dir / "run-setup-decision-log.md"
        log_path.write_text(content, encoding="utf-8")
        original_bytes = log_path.read_bytes()

        with patch(
            "agentic_devtools.cli.setup.decision_log.get_state_dir",
            return_value=tmp_path,
        ):
            with pytest.raises(ValueError, match="stray end marker"):
                append_decision(_make_entry())
            assert log_path.read_bytes() == original_bytes


class TestAppendDecisionDeterminism:
    """Tests for deterministic ID assignment (US3)."""

    def test_three_appends_produce_sequential_ids(self, tmp_path: Path) -> None:
        """Append 3 entries to empty log → ids 1, 2, 3."""
        with patch(
            "agentic_devtools.cli.setup.decision_log.get_state_dir",
            return_value=tmp_path,
        ):
            assert append_decision(_make_entry(step="a")) == 1
            assert append_decision(_make_entry(step="b")) == 2
            assert append_decision(_make_entry(step="c")) == 3

    def test_append_to_log_with_five_entries(self, tmp_path: Path) -> None:
        """Append to log with 5 entries → id 6."""
        setup_dir = tmp_path / "setup"
        setup_dir.mkdir(parents=True)
        entries = ""
        for i in range(1, 6):
            entries += (
                f"<!-- agdt-decision-entry:start id:{i} -->\n"
                f"### Decision #{i} (2026-07-08T18:30:00+00:00)\n"
                f"- Step: step{i}\n"
                f"- Question: q{i}\n"
                f"- Decision: d{i}\n"
                f"- Rationale: r{i}\n"
                f"- Auto-resolved: true\n"
                f"<!-- agdt-decision-entry:end -->\n"
            )
        (setup_dir / "run-setup-decision-log.md").write_text(entries, encoding="utf-8")

        with patch(
            "agentic_devtools.cli.setup.decision_log.get_state_dir",
            return_value=tmp_path,
        ):
            assert append_decision(_make_entry()) == 6

    def test_freeform_text_between_entries_counted_correctly(self, tmp_path: Path) -> None:
        """Freeform text between entries does not confuse marker counting."""
        setup_dir = tmp_path / "setup"
        setup_dir.mkdir(parents=True)
        content = (
            "# Decision Log\n\n"
            "Some freeform text here.\n\n"
            "<!-- agdt-decision-entry:start id:1 -->\n"
            "### Decision #1 (2026-07-08T18:30:00+00:00)\n"
            "- Step: step1\n"
            "- Question: q1\n"
            "- Decision: d1\n"
            "- Rationale: r1\n"
            "- Auto-resolved: true\n"
            "<!-- agdt-decision-entry:end -->\n"
            "\nMore freeform text.\n\n"
            "<!-- agdt-decision-entry:start id:2 -->\n"
            "### Decision #2 (2026-07-08T18:31:00+00:00)\n"
            "- Step: step2\n"
            "- Question: q2\n"
            "- Decision: d2\n"
            "- Rationale: r2\n"
            "- Auto-resolved: false\n"
            "<!-- agdt-decision-entry:end -->\n"
        )
        (setup_dir / "run-setup-decision-log.md").write_text(content, encoding="utf-8")

        with patch(
            "agentic_devtools.cli.setup.decision_log.get_state_dir",
            return_value=tmp_path,
        ):
            assert append_decision(_make_entry()) == 3
