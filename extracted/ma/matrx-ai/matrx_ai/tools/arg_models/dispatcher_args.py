"""Per-action wire contracts for the multi-action dispatcher tools that had no
per-action models before (dataset, note, task, seo, picklist, cloud_file).

Each tool is ONE tool_def row with an ``action`` discriminator; the executor
validates the incoming call against the discriminated-union RootModel registered
with @tool, and the engine diffs each variant against ``tool_def.parameters["$variants"]``.
Field set + required-ness per variant mirror the DB exactly. Required-ness comes
from the DB's "Required for action=X" markers (the worker still enforces deeper
rules at runtime). Descriptions live only in the DB (Rule 4) — none here.

Fields whose shape varies per action (e.g. dataset ``data``) are typed ``Any`` so
the variant accepts the real per-action shape; the DB variant entry omits ``type``
to match (canonicalises to "any").

Every object/array field carries a ``mode="before"`` coercion validator from
``_coercion`` so a model that passes the value as a JSON *string* (a very common
small-model mistake) is accepted and parsed instead of rejected with a cryptic
"Input should be a valid list/dictionary" — the failure that drove the
2026-05-25 loop-to-death incident. Validators NEVER change the declared type, so
they don't affect code⟷DB drift.
"""

from __future__ import annotations

from typing import Annotated, Any, Literal

from pydantic import Field, RootModel, field_validator

from matrx_ai.tools.arg_models._coercion import (
    coerce_json_container,
    coerce_list,
    coerce_object,
)
from matrx_ai.tools.declared import ToolArgs


# ── dataset ─────────────────────────────────────────────────────────────────
class DatasetListWire(ToolArgs):
    action: Literal["list"]
    limit: int = 50
    offset: int = 0


class DatasetGetWire(ToolArgs):
    action: Literal["get"]
    dataset_id: str
    limit: int = 50
    offset: int = 0
    include: str = "all"
    sort_by: str | None = None
    sort_order: str = "asc"


class DatasetSearchWire(ToolArgs):
    action: Literal["search"]
    dataset_id: str
    query: str
    limit: int = 50


class DatasetCreateWire(ToolArgs):
    action: Literal["create"]
    dataset_name: str
    data: Any = None
    typed: bool = False
    description: str | None = None

    @field_validator("data", mode="before")
    @classmethod
    def _coerce_data(cls, v: Any) -> Any:
        # `data` is Any (shape varies); best-effort parse a JSON string so the
        # worker receives a real object/array, never raises (Any is permissive).
        return coerce_json_container(v)


class DatasetAddRowsWire(ToolArgs):
    action: Literal["add_rows"]
    dataset_id: str
    rows: list

    @field_validator("rows", mode="before")
    @classmethod
    def _coerce_rows(cls, v: Any) -> Any:
        return coerce_list(v, field="rows", purpose="row objects")


class DatasetUpdateRowWire(ToolArgs):
    action: Literal["update_row"]
    dataset_id: str
    row_id: str
    data: Any = None

    @field_validator("data", mode="before")
    @classmethod
    def _coerce_data(cls, v: Any) -> Any:
        return coerce_json_container(v)


class DatasetDeleteRowWire(ToolArgs):
    action: Literal["delete_row"]
    dataset_id: str
    row_id: str


class DatasetArgs(
    RootModel[
        Annotated[
            DatasetListWire
            | DatasetGetWire
            | DatasetSearchWire
            | DatasetCreateWire
            | DatasetAddRowsWire
            | DatasetUpdateRowWire
            | DatasetDeleteRowWire,
            Field(discriminator="action"),
        ]
    ]
):
    pass


# ── note ────────────────────────────────────────────────────────────────────
class NoteListWire(ToolArgs):
    action: Literal["list"]


class NoteGetWire(ToolArgs):
    action: Literal["get"]
    note_id: str


class NoteCreateWire(ToolArgs):
    action: Literal["create"]
    label: str
    content: str | None = None
    tags: list | None = None
    is_public: bool = False
    folder_name: str | None = None

    @field_validator("tags", mode="before")
    @classmethod
    def _coerce_tags(cls, v: Any) -> Any:
        return coerce_list(v, field="tags", purpose="tag strings")


class NoteUpdateWire(ToolArgs):
    action: Literal["update"]
    note_id: str
    label: str | None = None
    content: str | None = None
    tags: list | None = None
    is_public: bool = False
    folder_name: str | None = None

    @field_validator("tags", mode="before")
    @classmethod
    def _coerce_tags(cls, v: Any) -> Any:
        return coerce_list(v, field="tags", purpose="tag strings")


class NotePatchWire(ToolArgs):
    action: Literal["patch"]
    note_id: str
    search_text: str
    replacement_text: str


class NoteDeleteWire(ToolArgs):
    action: Literal["delete"]
    note_id: str


class NoteArgs(
    RootModel[
        Annotated[
            NoteListWire
            | NoteGetWire
            | NoteCreateWire
            | NoteUpdateWire
            | NotePatchWire
            | NoteDeleteWire,
            Field(discriminator="action"),
        ]
    ]
):
    pass


# ── task ────────────────────────────────────────────────────────────────────
class TaskListWire(ToolArgs):
    action: Literal["list"]
    project_id: str | None = None
    parent_task_id: str | None = None


class TaskGetWire(ToolArgs):
    action: Literal["get"]
    task_id: str


class TaskCreateWire(ToolArgs):
    action: Literal["create"]
    title: str
    status: str = "incomplete"
    due_date: str | None = None
    priority: str | None = None
    is_public: bool = False
    project_id: str | None = None
    assignee_id: str | None = None
    description: str | None = None
    parent_task_id: str | None = None


class TaskUpdateWire(ToolArgs):
    action: Literal["update"]
    task_id: str
    title: str | None = None
    status: str = "incomplete"
    due_date: str | None = None
    priority: str | None = None
    is_public: bool = False
    project_id: str | None = None
    assignee_id: str | None = None
    description: str | None = None
    parent_task_id: str | None = None


class TaskDeleteWire(ToolArgs):
    action: Literal["delete"]
    task_id: str


class TaskArgs(
    RootModel[
        Annotated[
            TaskListWire | TaskGetWire | TaskCreateWire | TaskUpdateWire | TaskDeleteWire,
            Field(discriminator="action"),
        ]
    ]
):
    pass


# ── seo ─────────────────────────────────────────────────────────────────────
class SeoCheckTitlesWire(ToolArgs):
    action: Literal["check_titles"]
    titles: list

    @field_validator("titles", mode="before")
    @classmethod
    def _coerce_titles(cls, v: Any) -> Any:
        return coerce_list(v, field="titles", purpose="title strings")


class SeoCheckDescriptionsWire(ToolArgs):
    action: Literal["check_descriptions"]
    descriptions: list

    @field_validator("descriptions", mode="before")
    @classmethod
    def _coerce_descriptions(cls, v: Any) -> Any:
        return coerce_list(v, field="descriptions", purpose="description strings")


class SeoCheckBatchWire(ToolArgs):
    action: Literal["check_batch"]
    meta_data: list

    @field_validator("meta_data", mode="before")
    @classmethod
    def _coerce_meta_data(cls, v: Any) -> Any:
        return coerce_list(v, field="meta_data", purpose="meta-tag objects")


class SeoKeywordDataWire(ToolArgs):
    action: Literal["keyword_data"]
    keywords: list
    date_from: str
    date_to: str
    sort_by: str = "search_volume"
    language_code: str = "en"
    location_code: int = 2840
    search_partners: bool = True

    @field_validator("keywords", mode="before")
    @classmethod
    def _coerce_keywords(cls, v: Any) -> Any:
        return coerce_list(v, field="keywords", purpose="keyword strings")


class SeoCollectRankWire(ToolArgs):
    action: Literal["collect_rank"]
    provider: Literal["brave", "serpapi", "dataforseo"]
    keyword: str
    target_domain: str | None = None
    country: str = "US"
    language: str = "en"
    device: Literal["desktop", "mobile"] = "desktop"
    location: str | None = None
    search_type: Literal["organic", "local_pack"] = "organic"
    engine: Literal["chat_gpt", "claude", "gemini", "perplexity"] | None = Field(
        default=None,
        description=(
            "AI answer engine. When set, the keyword is treated as a PROMPT run "
            "through the engine with web search (provider dataforseo); citations "
            "and brand mentions persist as ai_answer rank observations."
        ),
    )
    site_id: str | None = Field(
        default=None,
        description=(
            "The site's canonical web.site id, if known. When omitted and "
            "target_domain is given, the host resolves it from an existing, "
            "accessible site with a matching domain (DEF-26) — it is never "
            "guessed across an ambiguous or inaccessible match, and no new "
            "site is ever created here."
        ),
    )


class SeoArgs(
    RootModel[
        Annotated[
            SeoCheckTitlesWire
            | SeoCheckDescriptionsWire
            | SeoCheckBatchWire
            | SeoKeywordDataWire
            | SeoCollectRankWire,
            Field(discriminator="action"),
        ]
    ]
):
    pass


# ── picklist ────────────────────────────────────────────────────────────────
class PicklistListWire(ToolArgs):
    action: Literal["list"]
    page: int = 1
    page_size: int = 50
    search_term: str | None = None


class PicklistGetWire(ToolArgs):
    action: Literal["get"]
    picklist_id: str
    group_by: bool = False


class PicklistCreateWire(ToolArgs):
    action: Literal["create"]
    picklist_name: str
    items: list
    description: str | None = None
    group_name: str | None = None

    @field_validator("items", mode="before")
    @classmethod
    def _coerce_items(cls, v: Any) -> Any:
        return coerce_list(v, field="items", purpose="picklist item objects")


class PicklistUpdateItemWire(ToolArgs):
    action: Literal["update_item"]
    item_id: str
    label: str | None = None
    help_text: str | None = None
    group_name: str | None = None


class PicklistBatchUpdateWire(ToolArgs):
    action: Literal["batch_update"]
    picklist_id: str
    items: list | None = None

    @field_validator("items", mode="before")
    @classmethod
    def _coerce_items(cls, v: Any) -> Any:
        return coerce_list(v, field="items", purpose="picklist item objects")


class PicklistArgs(
    RootModel[
        Annotated[
            PicklistListWire
            | PicklistGetWire
            | PicklistCreateWire
            | PicklistUpdateItemWire
            | PicklistBatchUpdateWire,
            Field(discriminator="action"),
        ]
    ]
):
    pass


# ── cloud_file ──────────────────────────────────────────────────────────────
class CloudFileListWire(ToolArgs):
    action: Literal["list"]
    limit: int = 50
    offset: int = 0
    folder_id: str | None = None
    mime_prefix: str | None = None


class CloudFileGetWire(ToolArgs):
    action: Literal["get"]
    file_id: str


class CloudFileDeleteWire(ToolArgs):
    action: Literal["delete"]
    file_id: str
    hard: bool = False


class CloudFileBatchGetWire(ToolArgs):
    action: Literal["batch_get"]
    file_ids: list

    @field_validator("file_ids", mode="before")
    @classmethod
    def _coerce_file_ids(cls, v: Any) -> Any:
        return coerce_list(v, field="file_ids", purpose="file id strings")


class CloudFileBatchDeleteWire(ToolArgs):
    action: Literal["batch_delete"]
    file_ids: list
    hard: bool = False

    @field_validator("file_ids", mode="before")
    @classmethod
    def _coerce_file_ids(cls, v: Any) -> Any:
        return coerce_list(v, field="file_ids", purpose="file id strings")


class CloudFileArgs(
    RootModel[
        Annotated[
            CloudFileListWire
            | CloudFileGetWire
            | CloudFileDeleteWire
            | CloudFileBatchGetWire
            | CloudFileBatchDeleteWire,
            Field(discriminator="action"),
        ]
    ]
):
    pass


# ── ctx_patch (discriminator is `command`, and `key` is shared by all) ───────
class CtxPatchStrReplaceWire(ToolArgs):
    command: Literal["str_replace"]
    key: str
    old_str: str | None = None
    new_str: str | None = None


class CtxPatchInsertWire(ToolArgs):
    command: Literal["insert"]
    key: str
    new_str: str | None = None
    insert_line: int | None = None


class CtxPatchAppendWire(ToolArgs):
    command: Literal["append"]
    key: str
    new_str: str | None = None
    separator: str | None = None
    create_if_missing: bool | None = None


class CtxPatchPrependWire(ToolArgs):
    command: Literal["prepend"]
    key: str
    new_str: str | None = None
    separator: str | None = None
    create_if_missing: bool | None = None


class CtxPatchOverwriteWire(ToolArgs):
    command: Literal["overwrite"]
    key: str
    new_str: str | None = None
    create_if_missing: bool | None = None


class CtxPatchJsonPatchWire(ToolArgs):
    command: Literal["json_patch"]
    key: str
    operations: list | None = None

    @field_validator("operations", mode="before")
    @classmethod
    def _coerce_operations(cls, v: Any) -> Any:
        return coerce_list(v, field="operations", purpose="RFC-6902 patch operations")


class CtxPatchJsonMergeWire(ToolArgs):
    command: Literal["json_merge"]
    key: str
    patch: dict | None = None

    @field_validator("patch", mode="before")
    @classmethod
    def _coerce_patch(cls, v: Any) -> Any:
        return coerce_object(v, field="patch", purpose="the RFC-7396 merge-patch fields")


class CtxPatchArgs(
    RootModel[
        Annotated[
            CtxPatchStrReplaceWire
            | CtxPatchInsertWire
            | CtxPatchAppendWire
            | CtxPatchPrependWire
            | CtxPatchOverwriteWire
            | CtxPatchJsonPatchWire
            | CtxPatchJsonMergeWire,
            Field(discriminator="command"),
        ]
    ]
):
    pass


# ``context_patch`` is the consolidated successor name for ``ctx_patch``; the
# per-command contract is byte-identical, so it reuses the same wire union.
ContextPatchArgs = CtxPatchArgs


# ── context (action: get | batch | create) ──────────────────────────────────
class ContextGetWire(ToolArgs):
    action: Literal["get"]
    key: str
    mode: Literal["full", "page", "summary"] | None = None
    chars: int | None = None
    offset: int | None = None


class ContextBatchWire(ToolArgs):
    action: Literal["batch"]
    requests: list
    stop_on_error: bool = False

    @field_validator("requests", mode="before")
    @classmethod
    def _coerce_requests(cls, v: Any) -> Any:
        return coerce_list(v, field="requests", purpose="get-shaped request objects")


class ContextCreateWire(ToolArgs):
    action: Literal["create"]
    key: str
    type: (
        Literal["text", "file_url", "json", "db_ref", "user", "org", "workspace", "project", "task"]
        | None
    ) = None
    label: str | None = None
    content: str
    description: str | None = None
    overwrite_existing: bool | None = None


class ContextArgs(
    RootModel[
        Annotated[
            ContextGetWire | ContextBatchWire | ContextCreateWire,
            Field(discriminator="action"),
        ]
    ]
):
    pass


# ── skill (action: list | get | search) ─────────────────────────────────────
class SkillListWire(ToolArgs):
    action: Literal["list"]
    category: str | None = None
    limit: int = 50


class SkillGetWire(ToolArgs):
    action: Literal["get"]
    skill_id: str
    mode: Literal["full", "page"] = "full"
    offset: int = 0
    chars: int = 4000


class SkillSearchWire(ToolArgs):
    action: Literal["search"]
    query: str
    category: str | None = None
    limit: int = 10


class SkillArgs(
    RootModel[
        Annotated[
            SkillListWire | SkillGetWire | SkillSearchWire,
            Field(discriminator="action"),
        ]
    ]
):
    pass
