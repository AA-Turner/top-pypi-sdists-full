"""The receipt card accepts the ``pending`` outcome (AF-D door #3) and still rejects unknown ones."""

import pytest
from pydantic import ValidationError

from matrx_connect.context.data_render_blocks import DirectiveReceiptRenderData


def test_pending_outcome_is_accepted() -> None:
    card = DirectiveReceiptRenderData(
        directive="create_agent",
        outcome="pending",
        message="Build started",
        resource_kind="agent_factory_build",
        resource_ids=["b1"],
    )
    assert card.outcome == "pending"


def test_unknown_outcome_is_still_rejected() -> None:
    with pytest.raises(ValidationError):
        DirectiveReceiptRenderData(directive="d", outcome="running", message="m")
