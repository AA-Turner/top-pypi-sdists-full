"""Contract tests for structured-input editability (tri-state) + read-only locks.

Editability is a tri-state signal on every input_* block:

  - editable=True  -> inject the type's full CRUD tool set (wins over agent
    exclusions);
  - editable=False -> EXPLICIT read-only: inject nothing, append a READ-ONLY
    notice to the resolved context, and lock the live id so the tool layer
    hard-blocks any write to it;
  - editable=None (unspecified, the default) -> inject nothing, lock nothing,
    say nothing — the agent's own tools are left untouched.

Originally (2026-06-15) a reference attach auto-injected a "workable" subset.
That was reverted once the FE moved to lean id references + an explicit editable
default, because auto-inject-on-reference would make every attachment editable
and defeat the server's "default to NOT editable" contract.
"""

from __future__ import annotations

from matrx_ai.config.message_config import MessageList, UnifiedMessage
from matrx_ai.config.read_only_resources import (
    READ_ONLY_RESOURCE_IDS_KEY,
    is_resource_read_only,
    set_read_only_resource_ids,
)
from matrx_ai.config.structured_input_config import (
    ListInputContent,
    NotesInputContent,
    TableInputContent,
    TaskInputContent,
    _read_only_notice_xml,
)

_NOTE_ID = "0dbd9901-2128-4793-8bf8-b24635701987"
_TASK_ID = "11111111-2222-3333-4444-555555555555"


# ── Tool injection (tri-state) ───────────────────────────────────────────────


def test_explicit_editable_note_injects_grouped_tool() -> None:
    block = NotesInputContent(note_ids=[_NOTE_ID], editable=True)
    assert block.editable_tools() == frozenset({"note"})


def test_explicit_editable_task_injects_grouped_tool() -> None:
    block = TaskInputContent(task_ids=[_TASK_ID], editable=True)
    assert block.editable_tools() == frozenset({"task"})


def test_unspecified_note_injects_nothing() -> None:
    # The default (None) is neutral — no tools added, nothing removed.
    block = NotesInputContent(note_ids=[_NOTE_ID])
    assert block.editable is None
    assert block.editable_tools() == frozenset()


def test_read_only_note_injects_nothing() -> None:
    block = NotesInputContent(note_ids=[_NOTE_ID], editable=False)
    assert block.editable_tools() == frozenset()


def test_reference_object_shape_does_not_auto_inject() -> None:
    # The historical FE shape (whole note object) must NOT auto-grant tools.
    block = NotesInputContent(note_ids=[{"id": _NOTE_ID, "label": "L", "content": "# body"}])
    assert block.editable_tools() == frozenset()


def test_snapshot_note_with_explicit_editable_still_injects_note() -> None:
    block = NotesInputContent(note_ids=[{"mode": "snapshot", "content": "frozen"}], editable=True)
    assert block.editable_tools() == frozenset({"note"})


def test_default_empty_block_injects_nothing() -> None:
    # The default (unspecified) block — the common "nothing attached / nothing
    # signalled" case — never injects.
    assert NotesInputContent(note_ids=[]).editable_tools() == frozenset()
    assert TaskInputContent(task_ids=[]).editable_tools() == frozenset()


def test_structured_input_editable_tool_names_includes_workbook_and_document() -> None:
    from matrx_ai.config.structured_input_config import structured_input_editable_tool_names

    names = structured_input_editable_tool_names()
    assert "workbook" in names
    assert "document" in names
    assert "dataset" in names
    assert "picklist" in names


def test_injection_catalog_exempts_realtime_native_builtins() -> None:
    from matrx_ai.injection_catalog import validate_injection_tool_catalog

    result = validate_injection_tool_catalog({"context", "web"}, emit=False)
    assert "web" not in result.missing
    assert "x_search" not in result.missing  # realtime native builtin — exempt


def test_injection_catalog_flags_unknown_names() -> None:
    from matrx_ai.injection_catalog import validate_injection_tool_catalog

    result = validate_injection_tool_catalog({"note", "task"}, emit=False)
    assert "context" in result.missing
    assert "note" not in result.missing


# ── Read-only id locking ─────────────────────────────────────────────────────


def test_read_only_note_locks_reference_id() -> None:
    block = NotesInputContent(note_ids=[_NOTE_ID], editable=False)
    assert block.read_only_resource_ids() == frozenset({_NOTE_ID})


def test_read_only_task_locks_reference_id() -> None:
    block = TaskInputContent(task_ids=[_TASK_ID], editable=False)
    assert block.read_only_resource_ids() == frozenset({_TASK_ID})


def test_read_only_object_shape_locks_extracted_id() -> None:
    block = NotesInputContent(
        note_ids=[{"id": _NOTE_ID, "label": "L", "content": "# body"}], editable=False
    )
    assert block.read_only_resource_ids() == frozenset({_NOTE_ID})


def test_read_only_snapshot_has_no_live_id_to_lock() -> None:
    # A by-value snapshot has no DB id and is inert text — nothing to lock.
    block = NotesInputContent(note_ids=[{"mode": "snapshot", "content": "frozen"}], editable=False)
    assert block.read_only_resource_ids() == frozenset()


def test_unspecified_and_editable_blocks_lock_nothing() -> None:
    assert NotesInputContent(note_ids=[_NOTE_ID]).read_only_resource_ids() == frozenset()
    assert (
        NotesInputContent(note_ids=[_NOTE_ID], editable=True).read_only_resource_ids()
        == frozenset()
    )


def test_read_only_table_and_list_bookmarks_lock_live_write_targets() -> None:
    table = TableInputContent(
        bookmarks=[
            {"type": "table_cell", "table_id": "table-id", "row_id": "row-id", "column_name": "c"}
        ],
        editable=False,
    )
    picklist = ListInputContent(
        bookmarks=[{"type": "list_item", "list_id": "list-id", "item_id": "item-id"}],
        editable=False,
    )

    assert table.read_only_resource_ids() == frozenset({"table-id", "row-id"})
    assert picklist.read_only_resource_ids() == frozenset({"list-id", "item-id"})


# ── Read-only registry helpers ───────────────────────────────────────────────


def test_set_read_only_ids_writes_and_clears_metadata() -> None:
    meta: dict = {}
    set_read_only_resource_ids(meta, {_NOTE_ID, ""})
    assert meta[READ_ONLY_RESOURCE_IDS_KEY] == {_NOTE_ID}  # falsy id dropped

    # An empty set clears the key so a stale lock never lingers.
    set_read_only_resource_ids(meta, set())
    assert READ_ONLY_RESOURCE_IDS_KEY not in meta


def test_is_resource_read_only_false_without_context() -> None:
    # No AppContext in a bare unit test -> never blocks (safe default).
    assert is_resource_read_only(_NOTE_ID) is False
    assert is_resource_read_only("") is False
    assert is_resource_read_only(None) is False


class _NullEmitter:
    async def send_chunk(self, *_a, **_kw) -> None: ...
    async def send_data(self, *_a, **_kw) -> None: ...
    async def send_tool_event(self, *_a, **_kw) -> None: ...
    async def fatal_error(self, *_a, **_kw) -> None: ...
    async def send_end(self, *_a, **_kw) -> None: ...


def test_is_resource_read_only_reads_active_context() -> None:
    from matrx_connect import AppContext
    from matrx_connect.context.app_context import clear_app_context, set_app_context

    ctx = AppContext(emitter=_NullEmitter(), metadata={READ_ONLY_RESOURCE_IDS_KEY: {_NOTE_ID}})
    token = set_app_context(ctx)
    try:
        assert is_resource_read_only(_NOTE_ID) is True
        assert is_resource_read_only("some-other-id") is False
    finally:
        clear_app_context(token)


def test_latest_explicit_editability_decision_wins_across_turns() -> None:
    from matrx_connect import AppContext
    from matrx_connect.context.app_context import clear_app_context, set_app_context

    from matrx_ai.config.structured_input_resolver import collect_read_only_resource_ids

    messages = MessageList(
        [
            UnifiedMessage(
                role="user", content=[NotesInputContent(note_ids=[_NOTE_ID], editable=False)]
            ),
            UnifiedMessage(
                role="user", content=[NotesInputContent(note_ids=[_NOTE_ID], editable=True)]
            ),
        ]
    )
    ctx = AppContext(emitter=_NullEmitter(), metadata={})
    token = set_app_context(ctx)
    try:
        collect_read_only_resource_ids(messages)
        assert is_resource_read_only(_NOTE_ID) is False

        messages._messages.reverse()
        collect_read_only_resource_ids(messages)
        assert is_resource_read_only(_NOTE_ID) is True
    finally:
        clear_app_context(token)


def test_unspecified_reattachment_does_not_override_prior_explicit_lock() -> None:
    from matrx_connect import AppContext
    from matrx_connect.context.app_context import clear_app_context, set_app_context

    from matrx_ai.config.structured_input_resolver import collect_read_only_resource_ids

    messages = MessageList(
        [
            UnifiedMessage(
                role="user", content=[TaskInputContent(task_ids=[_TASK_ID], editable=False)]
            ),
            UnifiedMessage(role="user", content=[TaskInputContent(task_ids=[_TASK_ID])]),
        ]
    )
    ctx = AppContext(emitter=_NullEmitter(), metadata={})
    token = set_app_context(ctx)
    try:
        collect_read_only_resource_ids(messages)
        assert is_resource_read_only(_TASK_ID) is True
    finally:
        clear_app_context(token)


async def test_note_update_tool_hard_blocks_locked_id() -> None:
    # The hard backstop: even if the agent carries note_update, a locked id is
    # refused at the tool boundary BEFORE any DB write — no manager call needed.
    from matrx_connect import AppContext
    from matrx_connect.context.app_context import clear_app_context, set_app_context

    from matrx_ai.tools.implementations.notes import note_update
    from matrx_ai.tools.models import ToolContext

    ctx = AppContext(emitter=_NullEmitter(), metadata={READ_ONLY_RESOURCE_IDS_KEY: {_NOTE_ID}})
    token = set_app_context(ctx)
    try:
        result = await note_update(
            {"note_id": _NOTE_ID, "content": "hacked"}, ToolContext(call_id="c1")
        )
        assert result.success is False
        assert result.error is not None
        assert result.error.error_type == "read_only"
    finally:
        clear_app_context(token)


async def test_dataset_write_tool_hard_blocks_locked_table() -> None:
    from matrx_connect import AppContext
    from matrx_connect.context.app_context import clear_app_context, set_app_context

    from matrx_ai.tools.implementations.datasets_tools import dataset
    from matrx_ai.tools.models import ToolContext

    ctx = AppContext(emitter=_NullEmitter(), metadata={READ_ONLY_RESOURCE_IDS_KEY: {"table-id"}})
    token = set_app_context(ctx)
    try:
        result = await dataset(
            {"action": "add_rows", "dataset_id": "table-id", "rows": [{"name": "blocked"}]},
            ToolContext(call_id="c2"),
        )
        assert result.success is False
        assert result.error is not None
        assert result.error.error_type == "read_only"
    finally:
        clear_app_context(token)


async def test_picklist_write_tool_hard_blocks_locked_item() -> None:
    from matrx_connect import AppContext
    from matrx_connect.context.app_context import clear_app_context, set_app_context

    from matrx_ai.tools.implementations.picklists_tools import picklist
    from matrx_ai.tools.models import ToolContext

    ctx = AppContext(emitter=_NullEmitter(), metadata={READ_ONLY_RESOURCE_IDS_KEY: {"item-id"}})
    token = set_app_context(ctx)
    try:
        result = await picklist(
            {"action": "update_item", "item_id": "item-id", "label": "blocked"},
            ToolContext(call_id="c3"),
        )
        assert result.success is False
        assert result.error is not None
        assert result.error.error_type == "read_only"
    finally:
        clear_app_context(token)


async def test_picklist_item_write_hard_blocks_when_parent_list_is_locked(monkeypatch) -> None:
    from matrx_connect import AppContext
    from matrx_connect.context.app_context import clear_app_context, set_app_context

    from matrx_ai.db import _registry
    from matrx_ai.tools.implementations.picklists_tools import picklist
    from matrx_ai.tools.models import ToolContext

    class _Item:
        list_id = "list-id"

    class _ItemModel:
        @classmethod
        async def get_by_id(cls, item_id: str, use_cache: bool = True) -> _Item:
            del cls, item_id, use_cache
            return _Item()

    monkeypatch.setattr(_registry, "get_model", lambda _key: _ItemModel)
    ctx = AppContext(emitter=_NullEmitter(), metadata={READ_ONLY_RESOURCE_IDS_KEY: {"list-id"}})
    token = set_app_context(ctx)
    try:
        result = await picklist(
            {"action": "update_item", "item_id": "item-id", "label": "blocked"},
            ToolContext(call_id="c4"),
        )
        assert result.success is False
        assert result.error is not None
        assert result.error.error_type == "read_only"
    finally:
        clear_app_context(token)


async def test_picklist_parent_lock_lookup_fails_closed(monkeypatch) -> None:
    from matrx_connect import AppContext
    from matrx_connect.context.app_context import clear_app_context, set_app_context

    from matrx_ai.db import _registry
    from matrx_ai.tools.implementations.picklists_tools import picklist
    from matrx_ai.tools.models import ToolContext

    class _UnavailableItemModel:
        @classmethod
        async def get_by_id(cls, item_id: str, use_cache: bool = True) -> None:
            del cls, item_id, use_cache
            raise RuntimeError("lookup unavailable")

    monkeypatch.setattr(_registry, "get_model", lambda _key: _UnavailableItemModel)
    ctx = AppContext(emitter=_NullEmitter(), metadata={READ_ONLY_RESOURCE_IDS_KEY: {"list-id"}})
    token = set_app_context(ctx)
    try:
        result = await picklist(
            {"action": "update_item", "item_id": "item-id", "label": "blocked"},
            ToolContext(call_id="c5"),
        )
        assert result.success is False
        assert result.error is not None
        assert result.error.error_type == "read_only"
    finally:
        clear_app_context(token)


# ── READ-ONLY notice in resolved context ─────────────────────────────────────


def test_read_only_notice_is_concise_and_actionable() -> None:
    notice = _read_only_notice_xml("note")
    assert "READ ONLY" in notice
    assert "editable" in notice
    # One line — must not balloon the context window.
    assert "\n" not in notice
