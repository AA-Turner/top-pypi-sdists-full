"""A held ("Ask me first") workflow_author result must fit its declared kind (feedback 681d4e9e)."""
from matrx_ai.tools.kinds.workflow_tools import WorkflowAuthorResult


def test_held_proposal_receipt_fits_workflow_author_result() -> None:
    payload = {
        "saved": False,
        "valid": True,
        "pending_approval": True,
        "proposal_id": "p-1",
        "batch_id": "b-1",
        "id": "wf-1",
        "version": 3,
        "changes": ["Connect a to b"],
        "hint": "NOT SAVED YET",
    }
    model = WorkflowAuthorResult.model_validate(payload)
    assert model.pending_approval is True and model.proposal_id == "p-1"
