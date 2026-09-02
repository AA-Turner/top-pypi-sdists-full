"""Kind for the context-write tool family (KIND_TOOL_LEDGER, agent ``lead-w2d``).

ONE implementation, MANY names. All ten ``widget_*`` tools are thin wrappers
over ``ctx_write.context_patch`` / ``ctx_write.ctx_create`` (see
``implementations/widgets.py``): the widget tool renames ``tool_name`` on the
forwarded ``ToolResult`` and the payload rides through untouched. So the family
is ONE kind — the receipt of one write against one context object — exactly the
``bundle:list_*`` precedent, not ten near-duplicate slugs.

WHY ONE KIND AND NOT patch/create TWINS. ``widget_attach_media`` and
``widget_create_artifact`` return the PATCH branch when the context object
exists and the CREATE branch when they had to create it — one tool, two
branches. ``TOOL_RESULT_KINDS`` declares one model per tool and the executor
enforces it, so the branches must be one shape: the union, with each branch's
extra receipt fields optional (the ``fs_*`` union rule — declare every key any
branch can emit). ``command`` is ``"create"`` on the create branch, which is a
true statement about the write that happened.

PLACEHOLDER tier: the receipt envelope is fully captured; there is no rich
provider data here — the payload IS six scalars.
"""

from __future__ import annotations

from pydantic import JsonValue

from matrx_graph.content_ir.model import KindModel, KindSubModel
from matrx_graph.content_ir.sdk import kind


@kind(
    "context_write_result",
    label="Context Write",
    family="conversation_context",
    example={
        "key": "widget_content",
        "command": "append",
        "persist": "client",
        "matched_at_pass": None,
        "new_size_chars": 1204,
        "type": None,
        "label": None,
        "size_hint": None,
        "mutable": None,
    },
    maturity="placeholder",
)
class ContextWriteResult(KindModel):
    """Receipt for one write to a request context object (patch or create)."""

    #: The context object written.
    key: str = ""
    #: The patch command applied (``str_replace``, ``append``, ``json_merge``,
    #: ...); ``"create"`` when the write created the object.
    command: str = ""
    #: The object's persist mode after the write (``never``/``client``/...).
    persist: str = ""
    #: Text commands only: which fuzzy-match pass ``str_replace`` matched on
    #: (``exact``, ``whitespace``, ...); None for non-matching commands.
    matched_at_pass: str | None = None
    #: Text commands only: size of the content after the write.
    new_size_chars: int | None = None
    #: Create branch only: the created object's type (``text``/``json``/...).
    type: str | None = None
    #: Create branch only: the created object's display label.
    label: str | None = None
    #: Create branch only: the human-readable size hint (e.g. "1.2k chars").
    size_hint: str | None = None
    #: Create branch only: whether the created object is editable.
    mutable: bool | None = None


class ContextBatchEntry(KindSubModel):
    """One sub-request's outcome inside a ``context`` batch read."""

    #: The requested key (echoed even when the sub-request failed).
    key: str | None = None
    success: bool = False
    #: The sub-read's payload (a serialized ContextToolResult) on success.
    output: dict[str, JsonValue] | None = None
    #: The sub-failure's ToolError dump (error_type/message/...) on failure.
    error: dict[str, JsonValue] | None = None


@kind(
    "context_tool_result",
    label="Context Tool Result",
    family="conversation_context",
    example={
        "key": "route_brief",
        "type": "text",
        "label": "Route Brief",
        "content": "The northbound route departs at 06:40...",
        "total_chars": 1204,
    },
    maturity="placeholder",
)
class ContextToolResult(KindModel):
    """Union result of the ``context`` dispatcher (actions get | batch | create).

    ONE union kind, not three, because the executor enforces exactly one
    declared kind per tool (the ``cms_*`` / ``value_store`` action-dispatcher
    precedent). The create branch mirrors ``context_write_result``'s receipt
    fields — the shared ``_create_from_patch`` funnel still returns that kind
    for ``context_patch`` and every ``widget_*`` tool; the ``context``
    dispatcher re-wraps the receipt into THIS kind so all three of its actions
    speak one declared shape.
    """

    # -- shared identity of the object read/created ------------------------
    key: str | None = None
    type: str | None = None
    label: str | None = None

    # -- get: full / page reads --------------------------------------------
    #: Native dict/list when the object is structured JSON, else the text.
    content: JsonValue | None = None
    #: Lazy source reads only: which representation the resolver returned.
    representation: str | None = None
    offset: int | None = None
    chars_returned: int | None = None
    total_chars: int | None = None
    has_more: bool | None = None
    next_offset: int | None = None
    #: Lazy document reads only: the physical page range of the slice.
    page_range: str | None = None

    # -- get: summary mode --------------------------------------------------
    #: "summary" (or "page" when the summary fell back to the first page).
    mode: str | None = None
    #: "agent" (AI summary) or "descriptor" (precomputed ToC/size).
    summary_kind: str | None = None
    summary: str | None = None
    fell_back_from: str | None = None
    note: str | None = None

    # -- processed-document continuation (rides every doc-backed read) ------
    processed_document_id: str | None = None
    #: Ready-made follow-up calls (document_search / document_content).
    document_tools: dict[str, JsonValue] | None = None
    physical_page_validation: str | None = None

    # -- batch ---------------------------------------------------------------
    count: int | None = None
    requested: int | None = None
    results: list[ContextBatchEntry] | None = None

    # -- create receipt (mirrors context_write_result's create branch) -------
    command: str | None = None
    persist: str | None = None
    size_hint: str | None = None
    mutable: bool | None = None
    matched_at_pass: str | None = None
    new_size_chars: int | None = None

    #: Alias-coercion / arg-decode notice the model must learn from.
    arg_coercion_notice: str | None = None
