"""AgentInstructions renders only the non-empty role/goal blocks."""
from xpander_sdk.modules.agents.models.agent import AgentInstructions


def test_empty_role_and_goal_render_nothing():
    ins = AgentInstructions(role=[], goal=[], general="Everything is in general now.")
    assert ins.instructions == ""
    assert "<instructions>" not in ins.instructions
    assert "<goals>" not in ins.instructions


def test_full_with_only_general_has_description_only():
    ins = AgentInstructions(role=[], goal=[], general="Base prompt.")
    full = ins.full
    assert "<description>" in full
    assert "Base prompt." in full
    assert "<instructions>" not in full
    assert "<goals>" not in full


def test_populated_role_and_goal_still_render():
    ins = AgentInstructions(role=["Support agent"], goal=["Resolve tickets"], general="Base.")
    text = ins.instructions
    assert "<instructions>" in text
    assert "Support agent" in text
    assert "<goals>" in text
    assert "Resolve tickets" in text


def test_role_only_omits_goals_block():
    ins = AgentInstructions(role=["Analyst"], goal=[], general="")
    text = ins.instructions
    assert "<instructions>" in text
    assert "<goals>" not in text


def test_all_empty_full_is_empty():
    assert AgentInstructions(role=[], goal=[], general="").full == ""
