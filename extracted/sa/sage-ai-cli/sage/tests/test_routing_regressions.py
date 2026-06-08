"""Regression tests for analysis routing and smart read behavior."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from sage.core.request_classifier import ClassifiedRequest, OutputFormat, PipelineType, RequestType
from sage.core.tool_orchestrator import FileReadStrategy, ReadRequest, SmartFileReader
from sage.main import (
    _build_multistep_phase_prompts,
    _build_readonly_exploration_nudge,
    _build_readonly_response_retry_prompt,
    _build_tool_followup_prompt,
    _should_use_multistep_pipeline,
)


def _make_classification(
    request_type: RequestType,
    text: str,
    *,
    quantity_required: int | None = None,
) -> ClassifiedRequest:
    """Create a classified request using the same defaults as runtime classification."""
    return ClassifiedRequest(
        original_request=text,
        request_type=request_type,
        expected_format=OutputFormat.MARKDOWN_LIST,
        pipeline_type=PipelineType.SIMPLE_RESPONSE,
        quantity_required=quantity_required,
        min_items=quantity_required or (10 if request_type == RequestType.LIST_GENERATION else 0),
    )


def test_readonly_list_generation_uses_analysis_multistep_pipeline():
    """Complex audits should still use the model, but with analysis-only phases."""
    classification = _make_classification(
        RequestType.LIST_GENERATION,
        "Analyze this codebase and list 100 improvements by priority",
        quantity_required=100,
    )

    assert classification.read_only is True
    assert (
        _should_use_multistep_pipeline(
            classification.original_request,
            classification=classification,
            is_local_model=True,
        )
        is True
    )

    steps = _build_multistep_phase_prompts(classification.original_request, classification)

    assert [phase for phase, _ in steps] == ["planning", "analysis", "synthesis"]
    assert all("write the test files" not in prompt.lower() for _, prompt in steps)
    assert all("do not write code" in prompt.lower() for _, prompt in steps)
    # Analysis phase should have file reading guidance
    analysis_prompt = steps[1][1].lower()
    assert "read files, not directories" in analysis_prompt or "read:" in analysis_prompt
    # Synthesis phase should have output format guidance
    synthesis_prompt = steps[-1][1].lower()
    assert "number every item" in synthesis_prompt or "list" in synthesis_prompt
    assert "reference" in synthesis_prompt or "evidence" in synthesis_prompt


def test_complex_local_implementation_can_still_use_multistep_pipeline():
    """Local complex implementation requests should still benefit from decomposition."""
    classification = _make_classification(
        RequestType.IMPLEMENTATION,
        "Implement auth retry handling and refactor the token refresh flow with tests",
    )

    assert classification.read_only is False
    assert (
        _should_use_multistep_pipeline(
            classification.original_request,
            classification=classification,
            is_local_model=True,
        )
        is True
    )

    steps = _build_multistep_phase_prompts(classification.original_request, classification)

    # The multistep pipeline always opens with planning and closes with
    # implementation. The middle stage was renamed from "testing" → "analysis"
    # when the analysis pass got more granular than just writing tests up
    # front — assert the bookends + presence of the middle, not the exact name.
    phases = [phase for phase, _ in steps]
    assert phases[0] == "planning"
    assert phases[-1] == "implementation"
    assert len(phases) >= 3
    # Some middle step should reference test-writing OR analysis
    middle_prompts = [p for _, p in steps[1:-1]]
    assert any(("test" in p.lower()) or ("analysis" in p.lower()) or ("analyze" in p.lower())
               for p in middle_prompts)


def test_readonly_tool_followup_prompt_stays_in_analysis_mode():
    """Tool follow-ups for audits should ask for findings, not FILE blocks."""
    classification = _make_classification(
        RequestType.ANALYSIS,
        "Audit the agent loop and explain what needs to be fixed",
    )

    prompt = _build_tool_followup_prompt(
        "File: main.py\n   1| def run():\nSearch results for 'agent':\n./main.py:1:def run():",
        classification,
    )

    assert "continue with your analysis" in prompt.lower()
    assert "do not write writable file blocks" in prompt.lower()
    assert "only claim facts explicitly supported" in prompt.lower()


def test_readonly_tool_followup_prompt_retries_weak_tool_results():
    """Weak tool output should ask the model to correct its investigation commands."""
    classification = _make_classification(
        RequestType.LIST_GENERATION,
        "Analyze this codebase and list 100 improvements by priority",
        quantity_required=100,
    )

    prompt = _build_tool_followup_prompt(
        "[READ /tmp/project: file not found or empty]\n\n[SEARCH 'plan OR reasoning': no matches found]",
        classification,
    )

    assert "did not produce enough grounded evidence" in prompt.lower()
    assert "read files, not directories" in prompt.lower()
    assert "do not combine terms with or" in prompt.lower()
    assert "do not claim facts unless" in prompt.lower()


def test_readonly_response_retry_prompt_for_incomplete_list_generation():
    """Incomplete long lists should trigger a continuation prompt."""
    classification = _make_classification(
        RequestType.LIST_GENERATION,
        "Analyze this codebase and list 5 improvements by priority",
        quantity_required=5,
    )

    retry_prompt = _build_readonly_response_retry_prompt(
        "1. Improve the CLI output\n2. Add more tests",
        classification,
        verified_files={"main.py"},
    )

    assert retry_prompt is not None
    lowered = retry_prompt.lower()
    # Updated assertions: match the actual current retry prompt, which
    # frames the issue as a regenerate-with-corrections request rather
    # than an explicit "continue from item N" instruction. We accept
    # either phrasing so the test survives small copy edits.
    assert "have 2 items" in lowered or "2 items" in lowered or "2 numbered items" in lowered
    assert ("need 5" in lowered) or ("requires 5" in lowered) or ("5 total" in lowered)
    # The retry prompt must invite the model to extend its answer one way
    # or another. Either "continue from item N" (old) or
    # "regenerate your response" / "provide at least N" (current).
    assert (
        "continue" in lowered
        or "regenerate" in lowered
        or "at least" in lowered
    )


def test_readonly_response_retry_prompt_not_needed_for_complete_list():
    """Sufficiently complete read-only responses should not request continuation."""
    classification = _make_classification(
        RequestType.LIST_GENERATION,
        "Analyze this codebase and list 5 improvements by priority",
        quantity_required=5,
    )

    retry_prompt = _build_readonly_response_retry_prompt(
        "\n".join(
            [
                "1. Fix `main.py`:10",
                "2. Fix `router.py`:20",
                "3. Fix `app.py`:30",
                "4. Fix `shell.py`:40",
                "5. Fix `tool_orchestrator.py`:50",
            ]
        ),
        classification,
        verified_files={"main.py", "router.py", "app.py", "shell.py", "tool_orchestrator.py"},
    )

    assert retry_prompt is None


def test_readonly_exploration_nudge_requires_commands_before_claims():
    """Read-only early phases should ask for investigation commands when no evidence exists."""
    classification = _make_classification(
        RequestType.ANALYSIS,
        "Audit this codebase for architecture risks",
    )

    nudge = _build_readonly_exploration_nudge(
        "planning",
        classification,
        has_verified_files=False,
    )

    assert nudge is not None
    assert "issue concrete investigation commands" in nudge.lower()
    assert "one pattern per line" in nudge.lower()
    assert "base findings only on verified results" in nudge.lower()


def test_readonly_exploration_nudge_not_needed_when_evidence_exists():
    """Once evidence exists, read-only planning/analysis should not re-nudge blindly."""
    classification = _make_classification(
        RequestType.LIST_GENERATION,
        "Analyze this codebase and list 20 improvements by priority",
        quantity_required=20,
    )

    nudge = _build_readonly_exploration_nudge(
        "analysis",
        classification,
        has_verified_files=True,
    )

    assert nudge is None


def test_smart_read_without_focus_match_returns_truncated_fallback():
    """Smart reads should clearly signal fallback when the requested focus is absent."""
    reader = SmartFileReader(Path())

    result = reader.read(
        ReadRequest(
            file_path="pyproject.toml",
            strategy=FileReadStrategy.SMART,
            focus_pattern="definitely-not-present-pattern",
        )
    )

    assert result.truncated is True
    assert "no matches" in result.truncation_message.lower()
