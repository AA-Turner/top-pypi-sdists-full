"""The census of every delete-class tool action — and what each one does to its table.

Arman's law: soft-delete everything important — archive, never delete; a
person's data is never destroyed by an agent. Every tool action that removes
something is listed here ONCE with the table it touches and how:

* ``soft``          — archives through the table's soft-delete column. The guard
                      walks ``impl`` and fails on any reachable hard-delete call,
                      and requires the ``soft_via`` marker to be present.
* ``per_table``     — a generic path over many tables (``data``, ``sql``, ``db_*``).
                      It must archive every table that HAS a soft-delete column
                      and may remove only rows of a table without one; the guard
                      drives it with a recording fake model (``probe``).
* ``hard``          — the table has NO soft-delete column, so removal is the only
                      thing possible. The guard fails the day the model grows one.
* ``no_row``        — removes no table row at all (e.g. a node inside a versioned
                      definition document); the reason says what it removes.
* ``waived``        — hard on a soft-deletable table, with an explicit reason.
* ``owner_pending`` — hard on a soft-deletable table, owned by another lane. The
                      guard asserts it is STILL hard; when the owner fixes it, the
                      guard goes red and says: flip this row to ``soft``.
* ``soft_pending``  — the code already ARCHIVES, but the table's soft-delete column
                      arrives with a named, not-yet-applied migration (``migration``).
                      Until then the path REFUSES loudly and removes nothing. The
                      guard walks it exactly like ``soft`` (no reachable hard delete,
                      the ``soft_via`` marker present) and asserts the generated
                      model does NOT have the column yet; the day it does, the guard
                      goes red and says: flip this row to ``soft``.

The guard (``aidream/tools/tests/test_delete_actions_archive.py``) derives the
delete-class action list from the registered tools themselves — every action
classified ``_REMOVES`` in ``surface_write.NOT_SURFACE_WRITES`` plus every
action whose name says delete/remove/forget/purge/clear/trash — and fails on
one that is not in this map. A new delete action cannot slip in unseen.

Soft-delete columns and the one archive primitive: ``matrx_ai.tools.soft_delete``.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Literal

Mode = Literal["soft", "per_table", "hard", "no_row", "waived", "owner_pending", "soft_pending"]

#: An action whose NAME reads as a removal is delete-class even if nobody
#: classified it that way.
DELETE_NAME = re.compile(r"(^|[:_])(delete|remove|forget|purge|clear|trash|destroy|erase|wipe|drop)", re.I)


@dataclass(frozen=True)
class DeletePath:
    table: str
    mode: Mode
    reason: str
    #: "module:qualname" of every function on the delete path the guard walks.
    impl: tuple[str, ...] = ()
    #: "module:Class" of the generated model — its columns are the live truth.
    model: str | None = None
    #: A call name / string argument / keyword that proves the archive happens.
    soft_via: str | None = None
    #: per_table only: the name of the guard's probe that drives it.
    probe: str | None = None
    #: soft_pending only: the migration that adds the soft-delete column.
    migration: str | None = None


_CMS_SOFT = (
    "sets deleted_at (CMS 0041, applied 2026-09-28); restore clears it. "
)

DELETE_CENSUS: dict[str, DeletePath] = {
    # ── fixed in this pass (were hard deletes on soft-deletable tables) ─────────
    "note:delete": DeletePath(
        "workbench.notes", "soft",
        "archives via deleted_at (was a hard delete — verifier 2026-09-26)",
        impl=(
            "matrx_ai.tools.implementations.notes:note_delete",
            "matrx_ai.db.content_types._notes_impl:NotesManager.delete_note",
        ),
        model="db.models.workbench:Notes",
        soft_via="archive_where",
    ),
    "cloud_file:delete": DeletePath(
        "files.files", "soft",
        "always archives (public.soft_delete_file sets deleted_at); an agent's hard=true is refused "
        "with a notice — permanent purge stays a person's act in the Files trash",
        impl=(
            "matrx_ai.tools.implementations.cloud_files:cloud_file",
            "matrx_ai.tools.implementations.cloud_files:_soft_delete",
        ),
        model="matrx_files.db.models_files:Files",
        soft_via="soft_delete_file_async",
    ),
    "cloud_file:batch_delete": DeletePath(
        "files.files", "soft", "see cloud_file:delete — every file archived, hard=true refused with a notice",
        impl=(
            "matrx_ai.tools.implementations.cloud_files:cloud_file",
            "matrx_ai.tools.implementations.cloud_files:_soft_delete",
        ),
        model="matrx_files.db.models_files:Files",
        soft_via="soft_delete_file_async",
    ),
    "data:delete": DeletePath(
        "<every data-tool resource>", "per_table",
        "archives every resource whose table has a soft-delete column; removes only on a table without one",
        impl=("aidream.services.agent_data.writes:delete_resource",),
        probe="data",
    ),
    "sql:delete": DeletePath(
        "<any writable table>", "per_table",
        "archives on a table with a soft-delete column; removes only on a table without one",
        impl=("matrx_ai.tools.implementations.database:_sql_delete",),
        probe="sql",
    ),
    "db_admin:delete": DeletePath(
        "<granted tables>", "per_table",
        "archives on a table with a soft-delete column; removes only on a table without one",
        impl=("aidream.services.db_grants.engine:op_delete",),
        probe="db_grants",
    ),
    "db_user:delete": DeletePath(
        "<granted tables>", "per_table",
        "archives on a table with a soft-delete column; removes only on a table without one",
        impl=("aidream.services.db_grants.engine:op_delete",),
        probe="db_grants",
    ),
    # ── already soft ──────────────────────────────────────────────────────────
    "records:record_delete": DeletePath(
        "custom.* (records store)", "soft",
        "custom.record_delete sets deleted_at (checked live); undo restores",
        impl=("matrx_records.store.client:RecordStore.record_delete",),
        soft_via="record_delete",
    ),
    "instance_delete": DeletePath(
        "content_ir.kind_instance", "soft",
        "sets deleted_at (platform tombstone); an organization whose kind records live in the "
        "record store archives through the store arm, whose delete is the store's soft delete "
        "(matrx_records gateway: 'The soft delete, and its undo')",
        impl=(
            "matrx_ai.tools.implementations.kind_instance:instance_delete",
            "aidream.services.kind_records.routed:KindRecordToolArm.delete",
        ),
        model="db.models.content_ir:KindInstance",
        soft_via="deleted_at",
    ),
    "cms_data:delete": DeletePath(
        "public.site_collection_items (CMS db)", "soft", "sets deleted_at",
        impl=("aidream.services.cms.collection_items:CmsCollectionItemService.delete",),
        model="matrx_cms.db.models:SiteCollectionItems",
        soft_via="deleted_at",
    ),
    "cms_collection:delete": DeletePath(
        "public.site_collections (CMS db)", "soft", "sets deleted_at and cascades it to the items",
        impl=("aidream.services.cms.collections:CmsCollectionService.delete",),
        model="matrx_cms.db.models:SiteCollections",
        soft_via="deleted_at",
    ),
    "cms_collection:archive": DeletePath(
        "public.site_collections (CMS db)", "soft", "lifecycle: status='archived'; nothing removed",
        impl=("aidream.services.cms.collections:CmsCollectionService.archive",),
        model="matrx_cms.db.models:SiteCollections",
        soft_via="status",
    ),
    "content_plan:delete_node": DeletePath(
        "plan.node", "soft", "sets deleted_at; refuses a node with live children",
        impl=("aidream.services.content_plan.service:delete_node",),
        model="db.models.plan:Node",
        soft_via="deleted_at",
    ),
    # ── CMS content: archives through deleted_at (CMS 0041, applied 2026-09-28) ──
    "cms_asset:delete": DeletePath(
        "public.client_assets (CMS db)", "soft",
        _CMS_SOFT + "The underlying cld_files file is never touched; this row is library membership.",
        impl=("aidream.services.cms_assets.service:CmsAssetService.delete",),
        model="matrx_cms.db.models:ClientAssets",
        soft_via="archive_where",
    ),
    "cms_component:delete": DeletePath(
        "public.client_components (CMS db)", "soft", _CMS_SOFT,
        impl=("aidream.services.cms.components:CmsComponentService.delete",),
        model="matrx_cms.db.models:ClientComponents",
        soft_via="archive_where",
    ),
    "cms_page:delete": DeletePath(
        "public.client_pages (CMS db)", "soft",
        _CMS_SOFT + "cms_archive_page archives the page and its live sub-pages with one stamp.",
        impl=("aidream.services.cms.pages:CmsPageService.delete",),
        model="matrx_cms.db.models:ClientPages",
        soft_via="cms_archive_page",
    ),
    "cms_site:delete": DeletePath(
        "public.client_sites + every child table (CMS db)", "soft",
        _CMS_SOFT + "cms_archive_site archives the site and every live page, component, asset, "
        "redirect, collection and item with one stamp; cms_site restore brings exactly that set back.",
        impl=("aidream.services.cms.sites:CmsSiteService.delete",),
        model="matrx_cms.db.models:ClientSites",
        soft_via="cms_archive_site",
    ),
    "cms_site:redirect_delete": DeletePath(
        "public.client_redirects (CMS db)", "soft",
        _CMS_SOFT + "An archived redirect never redirects; the archive is logged to the activity log.",
        impl=("aidream.services.cms.redirects:CmsRedirectService.delete",),
        model="matrx_cms.db.models:ClientRedirects",
        soft_via="archive_where",
    ),
    "html_page:delete": DeletePath(
        "public.html_pages (CMS db)", "soft", _CMS_SOFT,
        impl=("aidream.services.cms.html_pages:HtmlPageService.delete",),
        model="matrx_cms.db.models:HtmlPages",
        soft_via="archive_where",
    ),
    "dictionary:delete_entries": DeletePath(
        "dictionary.dict_entries", "soft",
        "public.dict_delete_entries_for ARCHIVES (sets deleted_at; migration 1355, applied 2026-09-28). "
        "Re-adding an archived term through upsert_entries revives it; restore_entries brings entries back.",
        impl=("matrx_ai.tools.implementations.dictionary:dictionary",),
        model="db.models.dictionary:DictEntries",
        soft_via="dictionary_archive_live",
    ),
    # ── removes no row ────────────────────────────────────────────────────────
    "workflow_plan:retire": DeletePath(
        "workflow definition document (one canvas node)", "no_row",
        "removes an AGENT-drafted, settled, replaced, unwired Plan anchor node from the workflow "
        "definition via a RemoveNodeOp patch; the workflow.plan row, its notes and samples are never "
        "deleted and the definition keeps its version history. A person-made step is refused.",
        impl=("aidream.services.workflow_plans.service:retire_plan_anchor",),
    ),
    "seo_keywords:remove_saved": DeletePath(
        "seo keyword tag associations", "no_row",
        "removes selected facet associations (or clears all tags) through keyword_facet_set; "
        "it never deletes the saved keyword or its market row.",
        impl=("aidream.tools.seo_keywords_tool:_remove_saved",),
    ),
    # ── waived ────────────────────────────────────────────────────────────────
    "tasks:remove": DeletePath(
        "chat.agent_task", "soft",
        "archives via deleted_at (archive_where). The tool's own list skips archived rows, and so does "
        "every matrx-frontend reader (agent-task.service.ts listTasks, ListsHubView, the realtime "
        "handler drops a row once deleted_at is set); the frontend's own remove/clear archive too.",
        impl=("aidream.tools.agent_tasks_tool:_tasks",),
        model="db.models.chat:AgentTask",
        soft_via="archive_where",
    ),
    "tasks:clear_completed": DeletePath(
        "chat.agent_task", "soft", "see tasks:remove",
        impl=("aidream.tools.agent_tasks_tool:_tasks",), model="db.models.chat:AgentTask",
        soft_via="archive_where",
    ),
    "tasks:clear_all": DeletePath(
        "chat.agent_task", "soft", "see tasks:remove",
        impl=("aidream.tools.agent_tasks_tool:_tasks",), model="db.models.chat:AgentTask",
        soft_via="archive_where",
    ),
    # ── hard on a soft-deletable table; another lane owns the file ──────────────
    "task:delete": DeletePath(
        "projects.tasks", "soft",
        "TasksManager.delete_task stamps deleted_at (fixed by the tasks lane 2026-09-26; lists read live rows only)",
        impl=("matrx_ai.db.content_types._tasks_impl:TasksManager.delete_task",),
        model="db.models.projects:Tasks",
        soft_via="deleted_at",
    ),
    "dataset:delete_row": DeletePath(
        "custom.* (records store)", "soft",
        "the table's row is a record of the store; custom.record_delete sets deleted_at and /trash restores it",
        impl=(
            "matrx_ai.tools.implementations.datasets_tools:usertable_delete_row",
            "matrx_records.agent.dataset_arm:DatasetStoreArm.delete_row",
        ),
        soft_via="record_delete",
    ),
    "memory:forget": DeletePath(
        "chat.agent_memory", "soft",
        "archives via deleted_at (queue_agent_memory_update); every memory read skips archived rows and "
        "storing the key again revives the archived row (the key index is unique across archived rows)",
        impl=("matrx_ai.tools.implementations.memory:memory_forget",),
        model="db.models.chat:AgentMemory",
        soft_via="deleted_at",
    ),
}
