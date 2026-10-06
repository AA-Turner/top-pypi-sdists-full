"""An answers/interaction remark carries an optional pointer to its block_states row (remarks B6).

WHAT BREAKS: the stored remark loses its rendered answers when a reference is present, the
reference leaks into the model-facing text, or a malformed reference is accepted (the database
trigger that marks the row sent reads exactly ``block_state_ref.id`` / ``.state_version``).
Use case: a homeowner's intake questionnaire for a kitchen remodel. Synthesized.
"""

from __future__ import annotations

import pytest
from pydantic import ValidationError

from matrx_ai.config.remarks import RemarkItem, render_remark

ROW = "9f1c2a9b-4d3e-4f5a-8b6c-7d8e9f0a1b2c"


def _item(ref):
    return RemarkItem.model_validate({
        "kind": "answers",
        "title": "Remodel intake",
        "target": {"message_id": "5d7f0c1e-2b3a-4c5d-8e9f-0a1b2c3d4e5f"},
        "answers": [{"question": "Budget", "answer": "Around $40k, cabinets first", "type": "text"}],
        "block_state_ref": ref,
    })


def test_answers_keep_their_rendered_content_and_the_reference_rides_beside_them():
    item = _item({"id": ROW, "state_version": 3})
    assert item.block_state_ref is not None and item.block_state_ref.state_version == 3
    dumped = item.model_dump(exclude_none=True)
    assert dumped["block_state_ref"] == {"id": ROW, "state_version": 3}
    assert dumped["answers"][0]["answer"] == "Around $40k, cabinets first"
    text = render_remark(item, {"5d7f0c1e-2b3a-4c5d-8e9f-0a1b2c3d4e5f": 1})
    assert "Around $40k, cabinets first" in text
    assert ROW not in text and "state_version" not in text


@pytest.mark.parametrize("bad", [{"id": "nope", "state_version": 1}, {"id": ROW, "state_version": 0},
                                 {"id": ROW, "state_version": 2, "extra": 1}])
def test_a_malformed_reference_is_refused(bad):
    with pytest.raises(ValidationError):
        _item(bad)


def test_the_reference_is_optional():
    assert _item(None).block_state_ref is None
