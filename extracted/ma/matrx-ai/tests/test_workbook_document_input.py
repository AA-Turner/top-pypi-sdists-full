"""Contract tests for the input_workbook / input_document structured-input blocks
(the attach→agent bridge for spreadsheets and cloud documents).

Unlike notes/tasks these never inline the opaque Univer snapshot. They emit a
canonical record-reference fence for live metadata, inject the read/edit tools
per the tri-state editable signal, tell the model to pull full content through
that tool, and lock the id when editable=False.
"""
from __future__ import annotations

import asyncio

from matrx_ai.config.structured_input_config import (
    DocumentInputContent,
    WorkbookInputContent,
    reconstruct_structured_input,
)

_WB_ID = "aaaaaaaa-1111-2222-3333-444444444444"
_DOC_ID = "bbbbbbbb-5555-6666-7777-888888888888"


def _resolve(block) -> str:
    asyncio.run(block.resolve())
    return block.get_output()


# ── tool injection (tri-state) ───────────────────────────────────────────────


def test_editable_workbook_injects_the_workbook_tool() -> None:
    block = WorkbookInputContent(workbook_ids=[_WB_ID], editable=True)
    assert block.editable_tools() == frozenset({"workbook"})


def test_editable_document_injects_the_document_tool() -> None:
    block = DocumentInputContent(document_ids=[_DOC_ID], editable=True)
    assert block.editable_tools() == frozenset({"document"})


def test_unspecified_injects_nothing() -> None:
    assert WorkbookInputContent(workbook_ids=[_WB_ID]).editable is None
    assert WorkbookInputContent(workbook_ids=[_WB_ID]).editable_tools() == frozenset()
    assert DocumentInputContent(document_ids=[_DOC_ID]).editable_tools() == frozenset()


def test_read_only_injects_no_tools() -> None:
    assert WorkbookInputContent(workbook_ids=[_WB_ID], editable=False).editable_tools() == frozenset()
    assert DocumentInputContent(document_ids=[_DOC_ID], editable=False).editable_tools() == frozenset()


# ── read-only id locking ──────────────────────────────────────────────────────


def test_read_only_locks_the_id() -> None:
    assert WorkbookInputContent(workbook_ids=[_WB_ID], editable=False).read_only_resource_ids() == frozenset({_WB_ID})
    assert DocumentInputContent(document_ids=[_DOC_ID], editable=False).read_only_resource_ids() == frozenset({_DOC_ID})


def test_editable_does_not_lock() -> None:
    assert WorkbookInputContent(workbook_ids=[_WB_ID], editable=True).read_only_resource_ids() == frozenset()
    assert DocumentInputContent(document_ids=[_DOC_ID]).read_only_resource_ids() == frozenset()


# ── reference resolution (metadata reference + on-demand content) ────────────


def test_workbook_pointer_mentions_tool_and_id() -> None:
    text = _resolve(WorkbookInputContent(workbook_ids=[_WB_ID], editable=True))
    # Kind Directives two-key shell: the identity is one __kind slug now.
    assert '"__kind":"directive_v1_reference_workbook"' in text
    assert _WB_ID in text and "edit" in text


def test_read_only_pointer_says_read_only_and_omits_edit() -> None:
    text = _resolve(WorkbookInputContent(workbook_ids=[_WB_ID], editable=False))
    assert "READ ONLY" in text and "edit" not in text


def test_document_pointer_mentions_tool() -> None:
    text = _resolve(DocumentInputContent(document_ids=[_DOC_ID], editable=True))
    assert '"__kind":"directive_v1_reference_document"' in text and _DOC_ID in text


def test_object_ref_shape_is_supported() -> None:
    block = WorkbookInputContent(workbook_ids=[{"id": _WB_ID, "name": "Budget"}], editable=True)
    assert block.read_only_resource_ids() == frozenset()
    assert _WB_ID in _resolve(block)


# ── reconstruct from stored block ─────────────────────────────────────────────


def test_reconstruct_workbook_block() -> None:
    block = reconstruct_structured_input(
        {"type": "input_workbook", "workbook_ids": [_WB_ID], "editable": True}
    )
    assert isinstance(block, WorkbookInputContent)
    assert block.editable is True and block.workbook_ids == [_WB_ID]


def test_reconstruct_document_block() -> None:
    block = reconstruct_structured_input(
        {"type": "input_document", "document_ids": [_DOC_ID], "editable": False}
    )
    assert isinstance(block, DocumentInputContent)
    assert block.editable is False
    assert block.read_only_resource_ids() == frozenset({_DOC_ID})
