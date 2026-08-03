"""Unit tests for the skills catalog injected into the agent system prompt.

Covers PRO-1460: internal skill names must stay loadable (rows intact) but the
note must instruct the agent never to surface them in user-facing output.
"""

from xpander_sdk.modules.backend.frameworks.agno import _build_skills_instructions


def test_empty_skills_returns_empty_string():
    assert _build_skills_instructions(None) == ""
    assert _build_skills_instructions([]) == ""
    # Entries without a name are skipped, yielding no catalog.
    assert _build_skills_instructions([{"description": "no name"}]) == ""


def test_skill_rows_kept_verbatim_for_path_resolution():
    out = _build_skills_instructions(
        [{"name": "xpander-control-plane", "description": "manage the control plane"}]
    )
    # The real name must remain so the agent can open ./skills/<name>/SKILL.md.
    assert '<skill name="xpander-control-plane">manage the control plane</skill>' in out


def test_note_instructs_not_to_mention_skill_names():
    out = _build_skills_instructions([{"name": "secret-skill", "description": "x"}])
    assert "NEVER mention" in out
    assert "internal implementation details" in out


def test_note_routes_authoring_to_local_skills():
    """./skills is read-only; agent-authored skills go to ./local_skills."""
    out = _build_skills_instructions([{"name": "any-skill", "description": "x"}])
    assert "read-only" in out
    assert "local_skills" in out


def test_note_makes_xpload_skill_the_primary_read_path() -> None:
    """One xpload_skill call replaces the SKILL.md-plus-explore workspace round trips, with workspace reads kept as the fallback."""
    out = _build_skills_instructions([{"name": "any-skill", "description": "x"}])
    assert "xpload_skill" in out
    assert "&lt;skill_playbook&gt;" in out
    assert "never load it twice" in out
    assert "xpworkspace-file-read" in out
    assert "xpworkspace-bash" in out
