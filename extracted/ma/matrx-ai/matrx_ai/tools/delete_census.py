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
        "always archives (files.soft_delete_file sets deleted_at); an agent's hard=true is refused "
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
        "dictionary.dict_delete_entries_for ARCHIVES (sets deleted_at; migration 1355, applied 2026-09-28). "
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
    # ── graph / canvas / mail / cerbo / orchestra deletes (declared 2026-11-17) ──
    "board_remove_tile": DeletePath(
        "the board's own document (one tile)", "no_row",
        "takes a tile and its arrows off the board through edit_board (a versioned board document edit); what the "
        "tile showed (a note, a file) is untouched and no table row is removed",
        impl=("aidream.services.board_door.actions:remove_tile",),
    ),
    "map_delete": DeletePath(
        "the map's own document (a box, section or arrow)", "no_row",
        "removes a box, section or arrow from the map document through the versioned map edit; no table row is removed",
        impl=("aidream.services.map_door.actions:delete",),
    ),
    "mail_campaign_archive": DeletePath(
        "communication.mail_campaign", "soft",
        "stamps metadata.archived_at (unarchive pops it); a live send is refused; the row and its report are kept",
        impl=("aidream.services.mail.audience.campaign_editor:archive",),
        model="db.models.communication:MailCampaign", soft_via="archived_at",
    ),
    "mail_template_archive": DeletePath(
        "agent.message_template", "soft",
        "stamps metadata.archived_at (restore pops it); nothing is destroyed and a template an email uses keeps working",
        impl=("aidream.services.mail.audience.designer:template_archive",),
        model="db.models.agent:MessageTemplate", soft_via="archived_at",
    ),
    "mail_audience_webhooks_archive": DeletePath(
        "an audience's webhook list", "no_row",
        "sets archived_at on one webhook entry inside the audience's own settings; the entry is kept, no row is removed",
        impl=("aidream.services.mail.audience.webhooks:archive_webhook",),
    ),
    "orchestra_archive": DeletePath(
        "agent orchestra marker + member links", "soft",
        "the agent.orchestra_archive door archives the Orchestra with every member link (restore brings back exactly those links)",
        impl=("aidream.services.graph_verbs.orchestra:orchestra_archive",),
        soft_via="orchestra_archive",
    ),
    "orchestra_remove_member": DeletePath(
        "platform.associations (a member link)", "soft",
        "platform.assoc_remove archives the link (TAILS-5: keeps its id and history); the member agent is untouched",
        impl=("aidream.services.graph_verbs.orchestra:orchestra_remove_member",),
        soft_via="assoc_remove",
    ),
    "orchestra_remove_seat": DeletePath(
        "platform.associations (a seated-person link)", "soft",
        "platform.assoc_remove archives the link (TAILS-5: keeps its id and history); the seat stays on the org chart",
        impl=("aidream.services.graph_verbs.orchestra:orchestra_remove_seat",),
        soft_via="assoc_remove",
    ),
    "org_chart_remove_position": DeletePath(
        "agent.position", "soft",
        "stamps deleted_at on the seat (its links stay; org_chart_restore_position brings it back whole)",
        impl=("aidream.services.graph_verbs.org_chart:org_chart_remove_position",),
        model="db.models.agent:Position", soft_via="deleted_at",
    ),
    "cerbo_change:delete_appointment": DeletePath(
        "Cerbo practice record (appointment, outside)", "no_row",
        "sends a DELETE to the person's own connected Cerbo practice; nothing in our database is removed "
        "(writes_or_spends: the platform's apply policy decides whether it runs unasked)",
        impl=("aidream.graph_actions.cerbo:cerbo_change",),
    ),
    "cerbo_describe_change:delete_appointment": DeletePath(
        "none (read-only preview)", "no_row",
        "read-only: shows the body Cerbo expects for delete_appointment; it changes and removes nothing",
        impl=("aidream.graph_actions.cerbo:cerbo_describe_change",),
    ),
    "cerbo_change:delete_encounter": DeletePath(
        "Cerbo practice record (encounter, outside)", "no_row",
        "sends a DELETE to the person's own connected Cerbo practice; nothing in our database is removed "
        "(writes_or_spends: the platform's apply policy decides whether it runs unasked)",
        impl=("aidream.graph_actions.cerbo:cerbo_change",),
    ),
    "cerbo_describe_change:delete_encounter": DeletePath(
        "none (read-only preview)", "no_row",
        "read-only: shows the body Cerbo expects for delete_encounter; it changes and removes nothing",
        impl=("aidream.graph_actions.cerbo:cerbo_describe_change",),
    ),
    "cerbo_change:delete_patient": DeletePath(
        "Cerbo practice record (patient, outside)", "no_row",
        "sends a DELETE to the person's own connected Cerbo practice; nothing in our database is removed "
        "(writes_or_spends: the platform's apply policy decides whether it runs unasked)",
        impl=("aidream.graph_actions.cerbo:cerbo_change",),
    ),
    "cerbo_describe_change:delete_patient": DeletePath(
        "none (read-only preview)", "no_row",
        "read-only: shows the body Cerbo expects for delete_patient; it changes and removes nothing",
        impl=("aidream.graph_actions.cerbo:cerbo_describe_change",),
    ),
    "cerbo_change:delete_patient_facility": DeletePath(
        "Cerbo practice record (patient facility, outside)", "no_row",
        "sends a DELETE to the person's own connected Cerbo practice; nothing in our database is removed "
        "(writes_or_spends: the platform's apply policy decides whether it runs unasked)",
        impl=("aidream.graph_actions.cerbo:cerbo_change",),
    ),
    "cerbo_describe_change:delete_patient_facility": DeletePath(
        "none (read-only preview)", "no_row",
        "read-only: shows the body Cerbo expects for delete_patient_facility; it changes and removes nothing",
        impl=("aidream.graph_actions.cerbo:cerbo_describe_change",),
    ),
    "cerbo_change:delete_patient_specialist": DeletePath(
        "Cerbo practice record (patient specialist, outside)", "no_row",
        "sends a DELETE to the person's own connected Cerbo practice; nothing in our database is removed "
        "(writes_or_spends: the platform's apply policy decides whether it runs unasked)",
        impl=("aidream.graph_actions.cerbo:cerbo_change",),
    ),
    "cerbo_describe_change:delete_patient_specialist": DeletePath(
        "none (read-only preview)", "no_row",
        "read-only: shows the body Cerbo expects for delete_patient_specialist; it changes and removes nothing",
        impl=("aidream.graph_actions.cerbo:cerbo_describe_change",),
    ),
    "cerbo_change:delete_patient_tag": DeletePath(
        "Cerbo practice record (patient tag, outside)", "no_row",
        "sends a DELETE to the person's own connected Cerbo practice; nothing in our database is removed "
        "(writes_or_spends: the platform's apply policy decides whether it runs unasked)",
        impl=("aidream.graph_actions.cerbo:cerbo_change",),
    ),
    "cerbo_describe_change:delete_patient_tag": DeletePath(
        "none (read-only preview)", "no_row",
        "read-only: shows the body Cerbo expects for delete_patient_tag; it changes and removes nothing",
        impl=("aidream.graph_actions.cerbo:cerbo_describe_change",),
    ),
    "cerbo_change:delete_portal_request": DeletePath(
        "Cerbo practice record (portal request, outside)", "no_row",
        "sends a DELETE to the person's own connected Cerbo practice; nothing in our database is removed "
        "(writes_or_spends: the platform's apply policy decides whether it runs unasked)",
        impl=("aidream.graph_actions.cerbo:cerbo_change",),
    ),
    "cerbo_describe_change:delete_portal_request": DeletePath(
        "none (read-only preview)", "no_row",
        "read-only: shows the body Cerbo expects for delete_portal_request; it changes and removes nothing",
        impl=("aidream.graph_actions.cerbo:cerbo_describe_change",),
    ),
    "cerbo_change:delete_tag": DeletePath(
        "Cerbo practice record (tag, outside)", "no_row",
        "sends a DELETE to the person's own connected Cerbo practice; nothing in our database is removed "
        "(writes_or_spends: the platform's apply policy decides whether it runs unasked)",
        impl=("aidream.graph_actions.cerbo:cerbo_change",),
    ),
    "cerbo_describe_change:delete_tag": DeletePath(
        "none (read-only preview)", "no_row",
        "read-only: shows the body Cerbo expects for delete_tag; it changes and removes nothing",
        impl=("aidream.graph_actions.cerbo:cerbo_describe_change",),
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
    "memory:forget": DeletePath(
        "chat.agent_memory", "soft",
        "archives via deleted_at (queue_agent_memory_update); every memory read skips archived rows and "
        "storing the key again revives the archived row (the key index is unique across archived rows)",
        impl=("matrx_ai.tools.implementations.memory:memory_forget",),
        model="db.models.chat:AgentMemory",
        soft_via="deleted_at",
    ),
    # ── delete-class actions added to the census 2026-11-10 (C117) ─────────────
    # Each row was read against its implementation and, where a custom.* door does the work, against the live
    # function body (no hard delete in custom.automation_archive / table_archive / template_uninstall /
    # template_clear_samples / share_revoke / record_delete; every one stamps deleted_at or a revoked/archived mark).
    "tables_automation:archive": DeletePath(
        "custom.* (automation)", "soft",
        "custom.automation_archive archives (checked live: no hard delete); tables_automation:restore brings it back",
        impl=("matrx_records.agent.table_doors:_automation",), soft_via="automation_archive",
    ),
    "tables_shape:archive_table": DeletePath(
        "custom.* (table)", "soft",
        "table.archive Action → schema.archive_table → custom.table_archive (checked live: no hard delete); "
        "tables_shape:restore_table brings it back",
        impl=("aidream.services.table_api.actions:table_archive",),
    ),
    "tables_shape:archive_column": DeletePath(
        "custom.* (column)", "soft",
        "table.column.archive Action → schema.archive_column; the column leaves the table, its values are kept, "
        "and the app restores it",
        impl=("aidream.services.table_api.actions:table_column_archive",),
    ),
    "tables_template:uninstall": DeletePath(
        "custom.* (template install)", "soft",
        "custom.template_uninstall archives what the install made (checked live: no hard delete); "
        "tables_template:restore brings it back",
        impl=("aidream.tools.table_doors_tools:run_tool_action",),
    ),
    "tables_template:clear_samples": DeletePath(
        "custom.* (sample rows)", "soft",
        "custom.template_clear_samples archives the seeded sample rows (checked live: no hard delete)",
        impl=("matrx_records.agent.table_doors:clear_samples",), soft_via="template_clear_samples",
    ),
    "tables_share:remove": DeletePath(
        "custom.* (table share)", "no_row",
        "ends one person's (or the organization's) share through custom.share_revoke (checked live: no hard delete); "
        "the table and every row are untouched",
        impl=("matrx_records.agent.table_doors:_share",),
    ),
    "spaces:archive": DeletePath(
        "content.document (format=spaces)", "soft",
        "stamps deleted_at — the same change the app's Trash button makes; the database carries it to sub-pages",
        impl=("aidream.tools.spaces_tool:_run_in_session",), model="db.models.content:Document", soft_via="deleted_at",
    ),
    "workflow_author:archive": DeletePath(
        "workflow.definition", "soft",
        "archive sets is_archived; permanent=true is DefinitionStore.soft_delete (deleted_at) — never a row delete",
        impl=(
            "matrx_graph.db.definition_store:DefinitionStore.archive",
            "matrx_graph.db.definition_store:DefinitionStore.soft_delete",
        ),
        soft_via="deleted_at",
    ),
    "workflow_author:trigger_delete": DeletePath(
        "workflow.trigger", "soft",
        "TriggerStore.delete stamps deleted_at and deactivates the trigger (was a hard delete_where until 2026-08-10)",
        impl=("matrx_graph.db.trigger_store:TriggerStore.delete",), soft_via="deleted_at",
    ),
    "seo_rank:remove_targets": DeletePath(
        "seo.rank_target", "soft",
        "remove_rank_target stamps deleted_at; an already-removed target is reported, never re-removed",
        impl=("aidream.services.seo.agent_reach:rank_remove_targets",),
    ),
    "seo_site:dismiss_competitor": DeletePath(
        "seo competitor candidate", "no_row",
        "sets tracking_status 'ignored'; the row and its history are kept",
        impl=("aidream.services.seo.agent_reach:dismiss_competitor",),
    ),
    "attention:resolve": DeletePath(
        "platform attention item", "no_row",
        "marks an attention item resolved through platform.attention_write; no row is removed",
        impl=("aidream.tools.attention_tool:attention",),
    ),
    "studio_workspace:remove": DeletePath(
        "the Studio workspace's list field", "no_row",
        "removes one list entry inside the workspace's own document; no table row is removed",
        impl=("aidream.tools.studio_workspace_tool:studio_workspace",),
    ),
    "desktop_schedule:cancel": DeletePath(
        "the person's computer schedule", "no_row",
        "cancels a schedule held by the desktop sidecar (op schedule.cancel); no platform row exists",
        impl=("matrx_ai.tools.implementations.desktop:_schedule_cancel",),
    ),
    "schedule_wakeup:cancel": DeletePath(
        "agent wake-ups", "no_row",
        "cancels pending wake-ups of the running agent; no content row is removed",
        impl=("aidream.tools.agent_harness_tool:schedule_wakeup",),
    ),
    "google_marketing:sitemaps_delete": DeletePath(
        "Google Search Console sitemap", "no_row",
        "removes a sitemap submission at Google through the connected account; nothing in our database is removed",
        impl=("aidream.services.google_integrations.google_marketing:_search_console_control",),
    ),
    "pdf_delete_pages": DeletePath(
        "files.files (a NEW pdf)", "no_row",
        "writes a new PDF without the named pages; the source file is untouched",
        impl=("aidream.tools.pdf_tools:pdf_delete_pages",),
    ),
    "api_connector_delete": DeletePath(
        "api connector + its endpoints", "soft",
        "connector_delete → store.archive_connector stamps deleted_at on the connector and each endpoint; reads skip archived rows",
        impl=("aidream.services.api_connectors.actions:connector_delete",
              "aidream.services.api_connectors.store:archive_connector"),
        soft_via="archive_connector",
    ),
    "api_endpoint_delete": DeletePath(
        "api endpoint", "soft",
        "endpoint_delete saves deleted_at on the endpoint; reads skip archived rows",
        impl=("aidream.services.api_connectors.actions:endpoint_delete",),
        soft_via="deleted_at",
    ),
    "org_section_unplace": DeletePath(
        "iam org section placement", "soft",
        "section_unplace → iam.org_section_unplace (checked live: it never hard-deletes; it ends the placement and "
        "leaves the placed item untouched)",
        impl=("aidream.graph_actions.org_sections:section_unplace",), soft_via="org_section_unplace",
    ),
    # ── Calendar (lane CORE-AMEND-5, 2026-11-16): the event's Delete is Trash — deleted_at stamped, restorable ──
    "calendar_event_delete": DeletePath(
        "communication.calendar_event", "soft",
        "calendar.event.delete moves the event (or one occurrence: an EXDATE plus its changed-occurrence row) to Trash by "
        "stamping deleted_at; calendar.event.restore brings it back; a hard removal never happens (delete forever only "
        "sets trash_cleared_at)",
        impl=("aidream.services.calendar.service:event_delete",),
        model="db.models.communication:CalendarEvent",
        soft_via="deleted_at",
    ),
    # ── delete-class Action tool doors, 2026-11-13: each read against its implementation (Python) or live function body (custom.*, hub.*, iam.*) ──
    "custom_dashboard_delete": DeletePath(
        "custom.* (dashboard)", "soft",
        "custom.dashboard_delete (checked live 2026-11-13: no hard delete; it stamps deleted_at or an archived mark); custom_dashboard_restore brings it back",
        impl=("aidream.services.table_api.screen_doors:_declare_screen_doors",),
    ),
    "custom_doc_render_delete": DeletePath(
        "custom.* (print render)", "soft",
        "custom.doc_render_delete (checked live 2026-11-13: no hard delete; it stamps deleted_at or an archived mark); custom_doc_render_restore brings it back",
        impl=("aidream.services.table_api.screen_doors:_declare_screen_doors",),
    ),
    "custom_doc_template_delete": DeletePath(
        "custom.* (print layout)", "soft",
        "custom.doc_template_delete (checked live 2026-11-13: no hard delete; it stamps deleted_at or an archived mark); custom_doc_template_restore brings it back",
        impl=("aidream.services.table_api.screen_doors:_declare_screen_doors",),
    ),
    "custom_io_import_forget": DeletePath(
        "custom.* (import record)", "soft",
        "custom.io_import_forget (checked live 2026-11-13: no hard delete; it stamps deleted_at or an archived mark); only the import's own bookkeeping is retired; the imported rows stay",
        impl=("aidream.services.table_api.screen_doors:_declare_screen_doors",),
    ),
    "custom_inbox_clear": DeletePath(
        "custom.* (a person's inbox state)", "no_row",
        "custom.inbox_clear (checked live 2026-11-13) writes a cleared_at mark on the person's own inbox state; the item is untouched and comes back when it changes",
        impl=("aidream.services.table_api.screen_doors:_declare_screen_doors",),
    ),
    "table_template_uninstall": DeletePath(
        "custom.* (template install)", "soft",
        "same door as tables_template:uninstall — custom.template_uninstall archives what the install made (checked live 2026-11-13: no hard delete); table_template_restore brings it back",
        impl=("aidream.tools.table_doors_tools:run_tool_action",),
    ),
    "table_template_clear_samples": DeletePath(
        "custom.* (sample rows)", "soft",
        "same door as tables_template:clear_samples — custom.template_clear_samples archives the seeded sample rows (checked live 2026-11-13: no hard delete)",
        impl=("matrx_records.agent.table_doors:clear_samples",),
    ),
    "table_share_remove": DeletePath(
        "custom.* (table share)", "no_row",
        "same door as tables_share:remove — custom.share_revoke ends the grant (checked live 2026-11-13: no hard delete); the table and every row are untouched",
        impl=("matrx_records.agent.table_doors:_share",),
    ),
    "table_synced_delete_row": DeletePath(
        "an outside database or sheet row", "no_row",
        "deletes the row at its outside source first (the person's own connected source); the copy here is archived afterwards through the records store's one door",
        impl=("aidream.services.table_api.related_actions:synced_delete_row",),
    ),
    "hub_page_unplace": DeletePath(
        "hub.* (page placement)", "no_row",
        "hub.page_unplace (checked live 2026-11-13: no hard delete) takes a page out of its section and keeps it in Drafts or Standalone; the page itself is untouched",
        impl=("aidream.graph_actions.company_hub:page_unplace_action",),
    ),
    "hub_page_unfile": DeletePath(
        "hub.* (page filing)", "no_row",
        "hub.page_unfile (checked live 2026-11-13: no hard delete) returns pages to Unsorted; the page itself is never changed",
        impl=("aidream.graph_actions.company_hub:page_unfile_action",),
    ),
    "org_member_remove": DeletePath(
        "iam.memberships", "soft",
        "iam.org_admin_remove_member stamps deleted_at and status removed on the membership (live body read 2026-11-13); only the member's own control-settings row is deleted, nothing they made is deleted",
        impl=("aidream.graph_actions.org_members:member_remove",),
    ),
    "org_team_member_remove": DeletePath(
        "iam.* (team membership)", "soft",
        "iam.team_member_remove (checked live 2026-11-13: no hard delete); the person stays in the organization",
        impl=("aidream.graph_actions.org_teams:team_member_remove",),
    ),
    "mail_audience_contact_note_delete": DeletePath(
        "platform.comments (a contact note)", "soft",
        "stamps deleted_at on the note",
        impl=("aidream.services.mail.audience.contacts:note_delete",),
    ),
    "mail_audience_contacts_delete": DeletePath(
        "crm.outreach_list_member + notes", "soft",
        "sets deleted_at and blanks the contact's personal data on the audience member, and stamps deleted_at on the notes filed there (the Mail screen's own permanent-delete wording); a departure record stays",
        impl=("aidream.services.mail.audience.contacts:contacts_delete",),
    ),
    "mail_audience_tags_delete": DeletePath(
        "an audience's tag list", "no_row",
        "takes the tag name off each member and out of the audience's list; no row is removed",
        impl=("aidream.services.mail.audience.audience_admin:tags_delete",),
    ),
    "mail_audience_fields_delete": DeletePath(
        "an audience's field list", "no_row",
        "removes the field from the audience's settings and blanks its values on its contacts (the Mail screen's own Delete a field); no row is removed, and the values are not kept",
        impl=("aidream.services.mail.audience.audience_admin:fields_delete",),
    ),
    "mail_campaign_delete": DeletePath(
        "communication.mail_campaign", "soft",
        "stamps deleted_at on the campaign (refused while it is sending)",
        impl=("aidream.services.mail.audience.campaign_editor:delete",),
    ),
    "mail_campaign_folder_delete": DeletePath(
        "platform.categories (a campaign folder)", "soft",
        "stamps deleted_at on the folder; the campaigns in it stay, unfiled",
        impl=("aidream.services.mail.audience.folders:delete",),
    ),
    "mail_template_folder_delete": DeletePath(
        "platform.categories (a template folder)", "soft",
        "stamps deleted_at on the folder; the templates in it stay, unfiled",
        impl=("aidream.services.mail.audience.folders:delete",),
    ),
    "mail_flow_delete": DeletePath(
        "communication.mail_flow", "soft",
        "stops live runs and stamps deleted_at on the flow (refused while it is live)",
        impl=("aidream.services.mail.flows.builder:delete",),
    ),
    "mail_flow_remove_contacts": DeletePath(
        "communication.mail_flow_run", "no_row",
        "ends chosen contacts' runs through the walker's stop; no row is removed",
        impl=("aidream.services.mail.flows.builder:remove_contacts",),
    ),
    "mail_manager_delete": DeletePath(
        "marketing.initiative", "soft",
        "stamps deleted_at on the campaign and on its tasks",
        impl=("aidream.services.mail.audience.manager:delete",),
    ),
    "mail_manager_touchpoint_delete": DeletePath(
        "marketing.initiative (a touchpoint)", "soft",
        "takes the touchpoint out of the campaign's details and stamps deleted_at on its task",
        impl=("aidream.services.mail.audience.manager:delete_touchpoint",),
    ),
    "mail_segment_delete": DeletePath(
        "communication.mail_segment", "soft",
        "stamps deleted_at on each saved segment; contacts are never removed",
        impl=("aidream.services.mail.audience.segments_ui:segment_delete",),
    ),
}
