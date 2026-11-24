"""Kind for the ``workbook`` tool result (KIND_TOOL_LEDGER, ``lead-w2f``).
Implementation: ``aidream/services/udt_content/tools.py`` (Univer workbook
create/read/edit over ``udt_content`` snapshots).

Sibling ``document`` (same module) is NOT declared here — its ledger row is
unclaimed; add its kind to this module when that row is worked.

WHY NOT ``office_spreadsheet``: that registered kind is the AI-authorable
.xlsx SPEC (``{sheets: [{name, rows, columns, freeze_header}]}``) — an input
shape for file generation, not this tool's create/read/edit receipts.

PLACEHOLDER tier union of every action's answer: create receipt, the overview +
first-sheet read, the range read (its grid keys spread at top level — kept
as-is, live shape), the edit and write_formula receipts (warnings, verify,
collab, live_data), find, describe_sheet and google_push.
"""

from __future__ import annotations

from matrx_graph.content_ir.model import KindModel
from matrx_graph.content_ir.sdk import kind
from pydantic import JsonValue


@kind(
    "workbook_result",
    disposition="record",
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
    #: ``read`` with sheet/range, when the grid was cut to the result budget:
    #: the requested range's full row count, the A1 range still unread, and the
    #: sentence naming the exact next call. (The overview read carries the same
    #: keys inside ``first_sheet``.)
    truncated: bool | None = None
    total_rows: int | None = None
    next_range: str | None = None
    truncation_notice: str | None = None
    #: ``read`` — every formula cell in the grid with what it computes, recalculated on the server with the engine
    #: ``write_formula`` uses: ``{cell, formula, value[, error]}``. The notice says when recalculation failed.
    formula_cells: list[dict] | None = None
    formula_cells_notice: str | None = None
    #: ``edit`` — per-op receipts + the saved snapshot.
    applied: list[dict] | None = None
    saved: dict | None = None
    #: ``read`` / ``edit`` / ``describe_sheet`` — where the people editing it are (``collab_fold`` staleness).
    collab: dict | None = None
    #: ``edit`` / ``write_formula`` — the live-data (``SEO.*`` / ``TABLE.*``) cells resolved as the caller:
    #: ``{evaluated, errors, computed_in_editor_only}``.
    live_data: dict | None = None
    #: ``edit`` / ``read`` — formulas reading numbers stored as text: ``{sheet, cell, ..., message}`` each, the
    #: messages joined in ``warning_hint``; a read also lists the text-held number cells in ``text_numbers``.
    warnings: list[dict] | None = None
    warning_hint: str | None = None
    text_numbers: list[str] | None = None
    #: ``write_formula`` — the server recalculation read-back: ``{recalculated, cells, cells_total, errors, ok,
    #: warnings[, notice][, hint]}``.
    verify: dict | None = None
    #: ``find`` — the matching cells ``{sheet, cell, value, formula}`` (``truncated`` above says the list was cut).
    matches: list[dict] | None = None
    #: ``describe_sheet`` — the sheet's shape (``rows`` above is its used row count).
    sheet: str | None = None
    used_range: str | None = None
    columns_count: int | None = None
    header_row: int | None = None
    columns: list[dict] | None = None
    sample: list[list[JsonValue]] | None = None
    frozen: dict | None = None
    charts: list[dict] | None = None
    conditional_formats: list[dict] | None = None
    validations: list[dict] | None = None
    filter: dict | None = None
    named_ranges: list[dict] | None = None
    #: ``google_push`` — the pushed Google Sheet and what went with it.
    pushed: bool | None = None
    google_file_id: str | None = None
    open_in_google: str | None = None
    notes: list[str] | None = None
    live_formulas: str | None = None
    live_errors: dict | None = None


__all__ = ["WorkbookResult"]
