from pathlib import Path

from agentic_devtools.ai_providers.availability import _DEFAULT_EVIDENCE_PATH, render_adoption_note


def test_render_adoption_note_includes_matrix_table() -> None:
    result = render_adoption_note({"claude-opus-5": "available", "gpt-5": "rejected"})

    assert "| claude-opus-5 | available |" in result
    assert "| gpt-5 | rejected |" in result


def test_render_adoption_note_uses_default_evidence_path_when_none() -> None:
    result = render_adoption_note()

    assert str(_DEFAULT_EVIDENCE_PATH) in result


def test_render_adoption_note_uses_custom_evidence_path() -> None:
    custom_path = Path("/tmp/custom/evidence.json")

    result = render_adoption_note(evidence_path=custom_path)

    assert str(custom_path) in result
    assert str(_DEFAULT_EVIDENCE_PATH) not in result


def test_render_adoption_note_renders_custom_evidence_path_in_safe_code_span() -> None:
    custom_path = "/tmp/we``ird\nname.json"

    result = render_adoption_note(evidence_path=custom_path)

    assert "```/tmp/we``ird name.json```" in result


def test_render_adoption_note_ends_with_newline() -> None:
    result = render_adoption_note({"claude-opus-5": "available"})

    assert result.endswith("\n")


def test_render_adoption_note_contains_required_sections() -> None:
    result = render_adoption_note({"claude-opus-5": "available"})

    assert "Agent Tasks model availability matrix" in result
    assert "## Observed inventory" in result
    assert "## Evidence" in result
    assert "model -> custom_agent -> base_ref" in result


def test_render_adoption_note_escapes_markdown_table_cells() -> None:
    result = render_adoption_note({"model|preview\nbeta": "available"})

    assert "| model\\|preview beta | available |" in result
