"""Tests for synthesize_spec in retro_spec/synthesis.py."""

from __future__ import annotations

import json
import subprocess
from unittest.mock import patch

from agentic_devtools.cli.speckit.retro_spec import synthesis
from agentic_devtools.cli.speckit.retro_spec.artifact_collector import PRArtifact
from agentic_devtools.cli.speckit.retro_spec.synthesis import synthesize_spec


class TestSynthesizeSpec:
    """Tests for the synthesize_spec function."""

    def test_returns_llm_generated_content_when_available(self) -> None:
        """Test that a successful Copilot response returns the generated content."""
        payload = {
            "choices": [
                {
                    "message": {
                        "content": "\n".join(
                            [
                                "## User Scenarios & Testing",
                                "### User Story 1 - Test (Priority: P1)",
                                "**Why this priority**: because",
                                "**Independent Test**: check",
                                "**Acceptance Scenarios**: case",
                                "### Edge Cases",
                                "none",
                                "## Requirements",
                                "### Functional Requirements",
                                "- FR",
                                "### Non-Functional Requirements",
                                "- NFR",
                                "## Success Criteria",
                                "- SC",
                                "**Summary**",
                                "Brief description",
                                "**PR References**",
                                "- #1",
                                "**Key Changes**",
                                "- change A",
                            ]
                        )
                    }
                }
            ]
        }
        with patch(
            "agentic_devtools.cli.speckit.retro_spec.synthesis.subprocess.run",
            return_value=subprocess.CompletedProcess([], 0, json.dumps(payload), ""),
        ):
            assert "## User Scenarios & Testing" in synthesize_spec("context", "system prompt")

    def test_falls_back_when_llm_content_missing_required_structure(self) -> None:
        """LLM output that omits required template markers triggers fallback synthesis."""
        payload = {"choices": [{"message": {"content": "## Summary\nGenerated"}}]}
        with (
            patch(
                "agentic_devtools.cli.speckit.retro_spec.synthesis.subprocess.run",
                return_value=subprocess.CompletedProcess([], 0, json.dumps(payload), ""),
            ),
            patch(
                "agentic_devtools.cli.speckit.retro_spec.synthesis._generate_fallback_spec",
                return_value="fallback",
            ) as mock_fallback,
        ):
            assert synthesize_spec("context", "system prompt") == "fallback"

        mock_fallback.assert_called_once_with(
            "context",
            has_implementation_artifacts=True,
            pr_artifacts=None,
            diff_entries=None,
            commit_messages=None,
        )

    def test_falls_back_when_response_cannot_be_parsed(self) -> None:
        """Test that malformed JSON triggers the fallback generator."""
        with (
            patch(
                "agentic_devtools.cli.speckit.retro_spec.synthesis.subprocess.run",
                return_value=subprocess.CompletedProcess([], 0, "{bad json", ""),
            ),
            patch(
                "agentic_devtools.cli.speckit.retro_spec.synthesis._generate_fallback_spec",
                return_value="fallback",
            ) as mock_fallback,
        ):
            result = synthesize_spec("context", "system prompt")

        assert result == "fallback"
        mock_fallback.assert_called_once_with(
            "context",
            has_implementation_artifacts=True,
            pr_artifacts=None,
            diff_entries=None,
            commit_messages=None,
        )

    def test_passes_structured_artifacts_to_fallback(self) -> None:
        """Structured artifact kwargs are forwarded when fallback synthesis is used."""
        pr = PRArtifact(number=101, title="Title", body="", state="merged", merged_at="2025-01-01T00:00:00Z")
        with (
            patch(
                "agentic_devtools.cli.speckit.retro_spec.synthesis.subprocess.run",
                return_value=subprocess.CompletedProcess([], 1, "", "boom"),
            ),
            patch(
                "agentic_devtools.cli.speckit.retro_spec.synthesis._generate_fallback_spec",
                return_value="fallback",
            ) as mock_fallback,
        ):
            result = synthesize_spec(
                "context",
                "system prompt",
                has_implementation_artifacts=False,
                pr_artifacts=[pr],
                diff_entries=["--- src/file.py ---\n+1"],
                commit_messages=["commit summary"],
            )

        assert result == "fallback"
        mock_fallback.assert_called_once_with(
            "context",
            has_implementation_artifacts=False,
            pr_artifacts=[pr],
            diff_entries=["--- src/file.py ---\n+1"],
            commit_messages=["commit summary"],
        )

    def test_falls_back_when_command_fails(self) -> None:
        """Test that failed LLM execution falls back to a template spec."""
        with (
            patch(
                "agentic_devtools.cli.speckit.retro_spec.synthesis.subprocess.run",
                return_value=subprocess.CompletedProcess([], 1, "", "boom"),
            ),
            patch(
                "agentic_devtools.cli.speckit.retro_spec.synthesis._generate_fallback_spec",
                return_value="fallback",
            ),
        ):
            assert synthesize_spec("context", "system prompt") == "fallback"

    def test_falls_back_when_response_has_no_choices(self) -> None:
        """Test that empty choice lists also use the fallback generator."""
        with (
            patch(
                "agentic_devtools.cli.speckit.retro_spec.synthesis.subprocess.run",
                return_value=subprocess.CompletedProcess([], 0, json.dumps({"choices": []}), ""),
            ),
            patch(
                "agentic_devtools.cli.speckit.retro_spec.synthesis._generate_fallback_spec",
                return_value="fallback",
            ) as mock_fallback,
        ):
            assert synthesize_spec("context", "system prompt") == "fallback"

        mock_fallback.assert_called_once_with(
            "context",
            has_implementation_artifacts=True,
            pr_artifacts=None,
            diff_entries=None,
            commit_messages=None,
        )

    def test_falls_back_when_gh_is_not_installed(self) -> None:
        """Test that FileNotFoundError (gh not installed) triggers the fallback generator."""
        with (
            patch(
                "agentic_devtools.cli.speckit.retro_spec.synthesis.subprocess.run",
                side_effect=FileNotFoundError("No such file or directory: 'gh'"),
            ),
            patch(
                "agentic_devtools.cli.speckit.retro_spec.synthesis._generate_fallback_spec",
                return_value="fallback",
            ) as mock_fallback,
        ):
            result = synthesize_spec("context", "system prompt")

        assert result == "fallback"
        mock_fallback.assert_called_once_with(
            "context",
            has_implementation_artifacts=True,
            pr_artifacts=None,
            diff_entries=None,
            commit_messages=None,
        )

    def test_falls_back_when_subprocess_raises_oserror(self) -> None:
        """Test that a generic OSError from subprocess also triggers the fallback generator."""
        with (
            patch(
                "agentic_devtools.cli.speckit.retro_spec.synthesis.subprocess.run",
                side_effect=OSError("permission denied"),
            ),
            patch(
                "agentic_devtools.cli.speckit.retro_spec.synthesis._generate_fallback_spec",
                return_value="fallback",
            ) as mock_fallback,
        ):
            result = synthesize_spec("context", "system prompt")

        assert result == "fallback"
        mock_fallback.assert_called_once_with(
            "context",
            has_implementation_artifacts=True,
            pr_artifacts=None,
            diff_entries=None,
            commit_messages=None,
        )

    def test_falls_back_when_llm_content_is_whitespace_only(self) -> None:
        """Test that a whitespace-only LLM response triggers the fallback generator."""
        payload = {"choices": [{"message": {"content": "   \n\t  "}}]}
        with (
            patch(
                "agentic_devtools.cli.speckit.retro_spec.synthesis.subprocess.run",
                return_value=subprocess.CompletedProcess([], 0, json.dumps(payload), ""),
            ),
            patch(
                "agentic_devtools.cli.speckit.retro_spec.synthesis._generate_fallback_spec",
                return_value="fallback",
            ) as mock_fallback,
        ):
            assert synthesize_spec("context", "system prompt") == "fallback"

        mock_fallback.assert_called_once_with(
            "context",
            has_implementation_artifacts=True,
            pr_artifacts=None,
            diff_entries=None,
            commit_messages=None,
        )

    def test_caps_oversized_llm_content_preserving_required_structure(self) -> None:
        """Oversized LLM output is capped while preserving required structure markers."""
        # All required markers come before the oversized block so they survive capping.
        oversized_body = "\n".join(
            [
                "## User Scenarios & Testing",
                "### User Story 1 - Big Output (Priority: P1)",
                "**Why this priority**: because",
                "**Independent Test**: check",
                "**Acceptance Scenarios**: case",
                "scenario body",
                "### Edge Cases",
                "none",
                "## Requirements",
                "### Functional Requirements",
                "- FR",
                "### Non-Functional Requirements",
                "- NFR",
                "## Success Criteria",
                "- SC",
                "**Summary**",
                "Brief description",
                "**PR References**",
                "- #1",
                "**Key Changes**",
                "- change A",
                "x" * 12000,
            ]
        )
        payload = {"choices": [{"message": {"content": oversized_body}}]}

        with patch(
            "agentic_devtools.cli.speckit.retro_spec.synthesis.subprocess.run",
            return_value=subprocess.CompletedProcess([], 0, json.dumps(payload), ""),
        ):
            result = synthesize_spec("context", "system prompt")

        assert len(result) <= synthesis._MAX_BODY_CHARS
        assert "This spec was summarized due to extensive artifacts." in result

    def test_falls_back_when_capped_llm_content_loses_required_structure(self) -> None:
        """LLM content that passes structure validation before capping but not after triggers fallback."""
        import json

        # Content passes pre-cap structure check but mocked to fail post-cap check.
        valid_content = "\n".join(
            [
                "## User Scenarios & Testing",
                "### User Story 1 - Scenario (Priority: P1)",
                "**Why this priority**: high",
                "**Independent Test**: yes",
                "**Acceptance Scenarios**: pass",
                "### Edge Cases",
                "none",
                "## Requirements",
                "### Functional Requirements",
                "- FR-001: does something",
                "### Non-Functional Requirements",
                "- NFR-001: resilient",
                "## Success Criteria",
                "- SC-001: works",
            ]
        )
        payload = {"choices": [{"message": {"content": valid_content}}]}
        # Simulate: pre-cap check passes, post-cap check fails.
        with (
            patch(
                "agentic_devtools.cli.speckit.retro_spec.synthesis.subprocess.run",
                return_value=subprocess.CompletedProcess([], 0, json.dumps(payload), ""),
            ),
            patch(
                "agentic_devtools.cli.speckit.retro_spec.synthesis._has_required_synthesis_structure",
                side_effect=[True, False],
            ),
            patch(
                "agentic_devtools.cli.speckit.retro_spec.synthesis._generate_fallback_spec",
                return_value="fallback",
            ) as mock_fallback,
        ):
            result = synthesize_spec("context", "system prompt")

        assert result == "fallback"
        mock_fallback.assert_called_once()

    def _make_valid_llm_content(self, *, omit_marker: str = "") -> str:
        """Build full valid LLM content, optionally omitting one required marker."""
        lines = [
            "## User Scenarios & Testing",
            "### User Story 1 - Test (Priority: P1)",
            "**Why this priority**: because",
            "**Independent Test**: check",
            "**Acceptance Scenarios**: case",
            "### Edge Cases",
            "none",
            "## Requirements",
            "### Functional Requirements",
            "- FR",
            "### Non-Functional Requirements",
            "- NFR",
            "## Success Criteria",
            "- SC",
            "**Summary**",
            "Brief description",
            "**PR References**",
            "- #1",
            "**Key Changes**",
            "- change A",
        ]
        return "\n".join(line for line in lines if line != omit_marker)

    def test_falls_back_when_llm_output_missing_summary(self) -> None:
        """LLM output omitting the Summary subsection triggers fallback."""
        payload = {"choices": [{"message": {"content": self._make_valid_llm_content(omit_marker="**Summary**")}}]}
        with (
            patch(
                "agentic_devtools.cli.speckit.retro_spec.synthesis.subprocess.run",
                return_value=subprocess.CompletedProcess([], 0, json.dumps(payload), ""),
            ),
            patch(
                "agentic_devtools.cli.speckit.retro_spec.synthesis._generate_fallback_spec",
                return_value="fallback",
            ) as mock_fallback,
        ):
            assert synthesize_spec("context", "system prompt") == "fallback"
        mock_fallback.assert_called_once()

    def test_falls_back_when_llm_output_missing_pr_references(self) -> None:
        """LLM output omitting the PR References subsection triggers fallback."""
        payload = {"choices": [{"message": {"content": self._make_valid_llm_content(omit_marker="**PR References**")}}]}
        with (
            patch(
                "agentic_devtools.cli.speckit.retro_spec.synthesis.subprocess.run",
                return_value=subprocess.CompletedProcess([], 0, json.dumps(payload), ""),
            ),
            patch(
                "agentic_devtools.cli.speckit.retro_spec.synthesis._generate_fallback_spec",
                return_value="fallback",
            ) as mock_fallback,
        ):
            assert synthesize_spec("context", "system prompt") == "fallback"
        mock_fallback.assert_called_once()

    def test_falls_back_when_llm_output_missing_key_changes(self) -> None:
        """LLM output omitting the Key Changes subsection triggers fallback."""
        payload = {"choices": [{"message": {"content": self._make_valid_llm_content(omit_marker="**Key Changes**")}}]}
        with (
            patch(
                "agentic_devtools.cli.speckit.retro_spec.synthesis.subprocess.run",
                return_value=subprocess.CompletedProcess([], 0, json.dumps(payload), ""),
            ),
            patch(
                "agentic_devtools.cli.speckit.retro_spec.synthesis._generate_fallback_spec",
                return_value="fallback",
            ) as mock_fallback,
        ):
            assert synthesize_spec("context", "system prompt") == "fallback"
        mock_fallback.assert_called_once()
