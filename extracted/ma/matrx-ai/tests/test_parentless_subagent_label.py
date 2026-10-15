"""``subagent`` means "has a parent conversation" at every writer of the label."""

from matrx_ai.agents.conversation_type import derive_conversation_type, honest_lineage_type


def test_explicit_subagent_without_parent_is_auto():
    assert derive_conversation_type(explicit="subagent", parent_conversation_id=None) == "auto"
    assert derive_conversation_type(explicit="subagent", parent_conversation_id="") == "auto"


def test_explicit_subagent_with_parent_stays():
    assert derive_conversation_type(explicit="subagent", parent_conversation_id="p") == "subagent"


def test_honest_lineage_only_touches_subagent():
    assert honest_lineage_type("subagent", None) == "auto"
    assert honest_lineage_type("subagent", "p") == "subagent"
    for t in ("standard", "workflow", "scheduled", "auto", "mandate_candidate"):
        assert honest_lineage_type(t, None) == t
