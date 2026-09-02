from __future__ import annotations

import json

from matrx_ai.tools.implementations.datasets_tools import _bounded_dataset_rows
from matrx_ai.tools.result_gate import apply_size_gate


def test_oversized_dataset_page_stays_structured_and_bypasses_blunt_gate() -> None:
    rows = [
        {"row_id": str(i), "data": {"body": "x" * 70_000}, "created_at": "now"} for i in range(10)
    ]

    bounded, cap = _bounded_dataset_rows(rows)
    content = json.dumps({"rows": bounded, "cap": cap})
    gated, truncated = apply_size_gate(
        {"content": content, "call_id": "forced-dataset-cap"},
        output_self_capped=True,
        tool_name="dataset",
        tool_kind="native",
        conversation_id="forced-conversation",
        user_id="forced-user",
    )

    assert len(content) < 50_000
    assert cap["rows_truncated"] is True
    assert cap["truncated_cells"] > 0
    assert bounded[0]["data"]["truncated"] is True
    assert truncated is False
    assert gated["content"] == content
