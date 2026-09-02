"""Kind for the IDE-state tool result.

Ledger row (KIND_TOOL_LEDGER, agent ``lead-w2b``): ``vsc_get_state``.

THE FIELD SET IS CLOSED, SO DECLARE IT. The tool echoes back only the fields
the caller asked for, from the frozen ``_VALID_FIELDS`` set in
``implementations/vsc.py`` — 14 names, all string-valued. A dynamic-keyed dict
would have been undeclarable (``additionalProperties: false``); the closed set
means every key CAN be declared, each optional. ``None`` means "not requested,
or the IDE snapshot did not carry it" — the caller knows which, because it
wrote the request.

PLACEHOLDER tier: these are the IDE snapshot's own string projections
(``IdeState.to_variables()``), passed through verbatim — nothing richer exists
to distill.
"""

from __future__ import annotations

from matrx_graph.content_ir.model import KindModel
from matrx_graph.content_ir.sdk import kind


@kind(
    "ide_state_fields",
    label="IDE State",
    family="tool_execution",
    example={
        "vsc_active_file_path": "src/app/page.tsx",
        "vsc_active_file_language": "typescriptreact",
        "vsc_selected_text": "export default function Page()",
        "vsc_git_branch": "main",
    },
    maturity="placeholder",
)
class IdeStateFields(KindModel):
    """The requested slice of the caller's live IDE snapshot."""

    vsc_active_file_path: str | None = None
    vsc_active_file_content: str | None = None
    vsc_active_file_language: str | None = None
    vsc_active_file_all: str | None = None
    vsc_selected_text: str | None = None
    vsc_diagnostics: str | None = None
    vsc_workspace_name: str | None = None
    vsc_workspace_folders: str | None = None
    vsc_workspace_all: str | None = None
    vsc_git_branch: str | None = None
    vsc_git_status: str | None = None
    vsc_git_all: str | None = None
    vsc_editor: str | None = None
    vsc_all: str | None = None
