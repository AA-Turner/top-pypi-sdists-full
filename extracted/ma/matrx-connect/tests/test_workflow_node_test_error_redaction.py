from __future__ import annotations

import pytest

from matrx_connect.context.data_types import WorkflowNodeTestResultData


@pytest.mark.parametrize(
    ("raw", "expected"),
    [
        (
            "\x1b[91mMatrx ORM  |  UnknownDatabaseError\n"
            "dataset is not available to this account\n"
            "Query: INSERT INTO private_rows VALUES ($1)\n"
            "Args: ['private row']\nTraceback: internal.py",
            "dataset is not available to this account",
        ),
        ("The step needs a required value.", "The step needs a required value."),
    ],
)
def test_node_test_result_redacts_client_bound_error_message(
    raw: str,
    expected: str,
) -> None:
    result = WorkflowNodeTestResultData(
        success=False,
        duration_ms=3,
        node_id="save-row",
        spec_type="data.save_row",
        error_type="UnknownDatabaseError",
        error_message=raw,
    )

    assert result.error_message == expected
    assert "INSERT INTO" not in (result.error_message or "")
    assert "private row" not in (result.error_message or "")
