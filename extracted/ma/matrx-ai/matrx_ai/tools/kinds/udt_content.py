"""Kind for the ``workbook`` tool result (KIND_TOOL_LEDGER, ``lead-w2f``).
Implementation: ``aidream/services/udt_content/tools.py`` (Univer workbook
create/read/edit over ``udt_content`` snapshots).

Sibling ``document`` (same module) is NOT declared here — its ledger row is
unclaimed; add its kind to this module when that row is worked.

WHY NOT ``office_spreadsheet``: that registered kind is the AI-authorable
.xlsx SPEC (``{sheets: [{name, rows, columns, freeze_header}]}``) — an input
shape for file generation, not this tool's create/read/edit receipts.

PLACEHOLDER tier union: create receipt, the overview + first-sheet read, the
range read (its grid keys spread at top level — kept as-is, live shape), and
the edit receipt.
"""

from __future__ import annotations

from pydantic import JsonValue

from matrx_graph.content_ir.model import KindModel
from matrx_graph.content_ir.sdk import kind


@kind(
    "workbook_result",
    label="Workbook Result",
    family="udt_content",
    example={
        "action": "read",
        "workbook_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
        "name": "Budget",
        "sheet_id": "sheet-01",
        "sheet_name": "Sheet1",
        "range": "A1:B2",
        "rows": 2,
        "cols": 2,
        "values": [["a", 1], ["b", 2]],
    },
    maturity="placeholder",
)
class WorkbookResult(KindModel):
    action: str = ""
    #: ``create`` — the created resource record + flag.
    workbook: dict | None = None
    created: bool | None = None
    #: ``read`` / ``edit`` — which workbook.
    workbook_id: str | None = None
    #: The workbook's name (snapshot-internal on overview reads, so nullable).
    name: str | None = None
    #: ``read`` overview — per-sheet dimensions + the first sheet's grid.
    sheets: list[dict] | None = None
    first_sheet: dict | None = None
    #: ``read`` with sheet/range — the grid, spread at top level.
    sheet_id: str | None = None
    sheet_name: str | None = None
    range: str | None = None
    rows: int | None = None
    cols: int | None = None
    values: list[list[JsonValue]] | None = None
    #: ``edit`` — per-op receipts + the saved snapshot.
    applied: list[dict] | None = None
    saved: dict | None = None


__all__ = ["WorkbookResult"]
