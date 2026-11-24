"""A change held for the person's approval rides the stream whole (``pending_approval``): the client keeps the
proposal drawn the moment the call completes; a result left for a read by id arrived after the turn had ended and
the proposal was rolled back as abandoned (one-graph live walk 2026-11-17)."""

from matrx_ai.tools.pinned_tools import is_pinned


def test_a_held_proposal_is_pinned_whatever_the_tool():
    assert is_pinned("workflow_author", {"saved": False, "pending_approval": True, "proposal_id": "p"})
    assert is_pinned("workflow_node", {"applied": False, "pending_approval": True})


def test_an_ordinary_result_is_not_pinned():
    assert not is_pinned("workflow_author", {"saved": True, "pending_approval": False})
    assert not is_pinned("workflow_author", "text")
    assert is_pinned("workflow_author", {"awaiting_approval": True})
    assert not is_pinned("workflow_author", {"awaiting_approval": True, "applied": True})
