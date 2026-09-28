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

Mode = Literal["soft", "per_table", "hard", "no_row", "waived", "owner_pending"]

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


_CMS_NO_COLUMN = (
    "the CMS table has no soft-delete column (checked live 2026-09-26), so removal is the only "
    "thing possible. It holds a person's site content and SHOULD get deleted_at — DDL is out of "
    "this lane's scope; recorded for the CMS owner."
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
        "content_ir.kind_instance", "soft", "sets deleted_at (platform tombstone)",
        impl=("matrx_ai.tools.implementations.kind_instance:instance_delete",),
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
    # ── tables with no soft-delete column ───────────────────────────────────────
    "cms_asset:delete": DeletePath(
        "public.client_assets (CMS db)", "hard",
        _CMS_NO_COLUMN + " The underlying cld_files file is NOT destroyed; this row is library membership.",
        impl=("aidream.services.cms_assets.service:CmsAssetService.delete",),
        model="matrx_cms.db.models:ClientAssets",
    ),
    "cms_component:delete": DeletePath(
        "public.client_components (CMS db)", "hard", _CMS_NO_COLUMN,
        impl=("aidream.services.cms.components:CmsComponentService.delete",),
        model="matrx_cms.db.models:ClientComponents",
    ),
    "cms_page:delete": DeletePath(
        "public.client_pages (CMS db)", "hard", _CMS_NO_COLUMN + " Version history survives in cms versions.",
        impl=("aidream.services.cms.pages:CmsPageService.delete",),
        model="matrx_cms.db.models:ClientPages",
    ),
    "cms_site:delete": DeletePath(
        "public.client_sites + public.client_pages (CMS db)", "hard",
        _CMS_NO_COLUMN + " With force=true it also removes every page of the site — the widest hard "
        "delete an agent can reach; highest priority for a deleted_at column.",
        impl=("aidream.services.cms.sites:CmsSiteService.delete",),
        model="matrx_cms.db.models:ClientSites",
    ),
    "cms_site:redirect_delete": DeletePath(
        "public.client_redirects (CMS db)", "hard",
        "a redirect ledger row; no soft-delete column (checked live) and the removal is logged to the activity log",
        impl=("aidream.services.cms.redirects:CmsRedirectService.delete",),
        model="matrx_cms.db.models:ClientRedirects",
    ),
    "html_page:delete": DeletePath(
        "public.html_pages (CMS db)", "hard", _CMS_NO_COLUMN,
        impl=("aidream.services.cms.html_pages:HtmlPageService.delete",),
        model="matrx_cms.db.models:HtmlPages",
    ),
    "dictionary:delete_entries": DeletePath(
        "dictionary.dict_entries", "hard",
        "public.dict_delete_entries_for runs DELETE FROM; the table has no soft-delete column (checked live). "
        "Dictionary entries are a person's vocabulary and SHOULD get deleted_at — DDL is out of this lane's scope.",
        impl=("matrx_ai.tools.implementations.dictionary:dictionary",),
        model="db.models.dictionary:DictEntries",
    ),
    # ── removes no row ────────────────────────────────────────────────────────
    "workflow_plan:retire": DeletePath(
        "workflow definition document (one canvas node)", "no_row",
        "removes an AGENT-drafted, settled, replaced, unwired Plan anchor node from the workflow "
        "definition via a RemoveNodeOp patch; the workflow.plan row, its notes and samples are never "
        "deleted and the definition keeps its version history. A person-made step is refused.",
        impl=("aidream.services.workflow_plans.service:retire_plan_anchor",),
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
        "workspace.tasks", "soft",
        "TasksManager.delete_task stamps deleted_at (fixed by the tasks lane 2026-09-26; lists read live rows only)",
        impl=("matrx_ai.db.content_types._tasks_impl:TasksManager.delete_task",),
        model="db.models.workspace:Tasks",
        soft_via="deleted_at",
    ),
    "dataset:delete_row": DeletePath(
        "workbench.udt_dataset_rows", "soft",
        "usertable_delete_row archives through deleted_at (archive_where; fixed 2026-09-26); a moved table "
        "goes through the records store's own soft delete. The server readers skip archived rows. The grid's "
        "Postgres readers and its own delete doors are made to match by the draft "
        "matrx-frontend/migrations/udt_dataset_rows_delete_archives_and_trash_restores.sql, which also lists "
        "archived rows in /trash.",
        impl=(
            "matrx_ai.tools.implementations.datasets_tools:usertable_delete_row",
            "matrx_records.agent.dataset_arm:DatasetStoreArm.delete_row",
        ),
        model="db.models.workbench:UdtDatasetRows",
        soft_via="archive_where",
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
