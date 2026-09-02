"""Kind declarations for tool RESULTS — the tools family sweep.

Each submodule declares one domain's tool-result kinds via
``matrx_graph.content_ir.sdk.kind``. Publish with
``scripts/publish_kind_catalog.py matrx_ai.tools.kinds.<domain> --apply``.

WHY THESE LIVE IN THE PACKAGE, NOT IN ``aidream/kinds/``
--------------------------------------------------------
The node army's kinds sit in ``aidream/kinds/`` because the nodes they describe
are aidream's own graph actions. These describe results produced by tool
implementations that ship INSIDE matrx-ai, and a package never imports aidream
(``scripts/check_package_boundaries.py`` fails the build on it). The declaration
must be importable by the code that returns the shape, so it lives here.

Ledger: ``aidream/docs/workflow/KIND_TOOL_LEDGER.md``.
Authority: ``common-docs/systems/content-ir-system/KINDS_EVERYWHERE_PLAN.md`` §10d-C.
"""


# ── THE DECLARATION: which tool returns which result kind ────────────────────
#
# RECONCILED 2026-08-23 (KINDS_EVERYWHERE_PLAN §10g GAP 3). Two instruments were
# measuring "does this tool speak kinds" and disagreeing 50 vs 0:
#
#   * the LEDGER counted the RUNTIME half — the implementation returns a
#     ``KindModel``, so ``__kind`` is in the payload the caller receives;
#   * the COVERAGE BOARD counted the SCHEMA half — the stored
#     ``tool.definition.output_schema`` declares ``__kind``, so bindings, forms
#     and the registry can see the shape WITHOUT running the tool.
#
# Both are real and neither is sufficient: a runtime-only tool is invisible to
# every reader that does not execute it, and a schema-only tool is a promise
# nothing keeps. **A tool speaks kinds when BOTH are true**, and this map is
# what makes them ONE fact rather than two hand-maintained lists:
#
#   * ``scripts/backfill_tool_output_schemas.py`` writes the stored schema FROM
#     the model here (``model_json_schema()``) — the schema is never hand-written,
#     so it cannot drift from the shape the tool actually returns;
#   * ``ToolExecutor.execute`` ENFORCES it — a tool declared here whose result
#     carries no ``__kind`` (or the wrong one) screams, so this map cannot
#     quietly become a lie about code that stopped returning its KindModel;
#   * ``scripts/kind_coverage_board.py`` reads it for the runtime half.
#
# Adding a row here is the LAST step of a conversion, after the implementation
# returns the model and a real dispatch was verified.

from collections.abc import Iterable  # noqa: E402

from matrx_graph.content_ir.model import KindModel  # noqa: E402

from matrx_graph.nodes.text.regex import RegexExtractOutput  # noqa: E402

from matrx_ai.tools.kinds.cms import CMS_TOOL_RESULT_KINDS  # noqa: E402
from matrx_ai.tools.kinds.context_tools import (  # noqa: E402
    ContextToolResult,
    ContextWriteResult,
)
from matrx_ai.tools.kinds.kind_authoring import (  # noqa: E402
    KindActivationResult,
    KindContentBlockResult,
    KindCreateResult,
    KindDefinitionDetail,
    KindExampleResult,
    KindSchemaUpdateResult,
    KindSkillResult,
)
from matrx_ai.tools.kinds.kind_components import (  # noqa: E402
    KindComponentCode,
    KindComponentContext,
    KindComponentCreateResult,
    KindComponentIncidentResolution,
    KindComponentPatchResult,
    KindComponentUpdateResult,
)
from matrx_ai.tools.kinds.kind_instances import (  # noqa: E402
    KindInstanceDetail,
    KindInstancePage,
    KindInstanceWriteResult,
)
from matrx_ai.tools.kinds.database_tools import DATABASE_TOOL_RESULT_KINDS  # noqa: E402
from matrx_ai.tools.kinds.scope_tools import ScopeSystemResult  # noqa: E402
from matrx_ai.tools.kinds.value_store import ValueStoreResult  # noqa: E402
from matrx_ai.tools.kinds.code_docs import CodeTreeResult, LlmsTxtDocument  # noqa: E402
from matrx_ai.tools.kinds.tool_components import (  # noqa: E402
    ToolComponentCode,
    ToolComponentContext,
    ToolComponentCreateResult,
    ToolComponentIncidentDetail,
    ToolComponentIncidentResolution,
    ToolComponentListing,
    ToolComponentPatchResult,
    ToolComponentSample,
    ToolComponentUpdateResult,
)
from matrx_ai.tools.kinds.tool_loading import (  # noqa: E402
    ChromeToolsLoadResult,
    DesktopToolsLoadResult,
)
from matrx_ai.tools.kinds.execution import (  # noqa: E402
    CalculationResult,
    ShellExecution,
)
from matrx_ai.tools.kinds.filesystem import (  # noqa: E402
    DirectoryCreateResult,
    DirectoryListing,
    FileEditResult,
    FilePatchResult,
    FileReadResult,
    FileSearchResults,
    FileWriteResult,
)
from matrx_ai.tools.kinds.tool_traces import (  # noqa: E402
    ToolTraceCallDetail,
    ToolTraceEventPage,
    ToolTraceFileListing,
    ToolTraceFileWindow,
    ToolTraceIncidentList,
    ToolTraceIncidentReport,
)
from matrx_ai.tools.kinds.ide import IdeStateFields  # noqa: E402
from matrx_ai.tools.kinds.agent_ops import (  # noqa: E402
    OfficeToolResult,
    ResearchRunState,
    RulebookToolResult,
    SelfPromptResult,
)
from matrx_ai.tools.kinds.agent_tasks import AgentTaskList  # noqa: E402
from matrx_ai.tools.kinds.workbench import (  # noqa: E402
    PicklistToolResult,
    SkillToolResult,
    TaskToolResult,
)
from matrx_ai.tools.kinds.udt_content import WorkbookResult  # noqa: E402
from matrx_ai.tools.kinds.user_secrets import UserSecretReceipt  # noqa: E402
from matrx_ai.tools.kinds.workflow_tools import (  # noqa: E402
    WorkflowAuthorResult,
    WorkflowCatalogResult,
    WorkflowNodeResult,
    WorkflowPlanResult,
    WorkflowRunStatus,
)
from matrx_ai.tools.kinds.text_tools import TextAnalysis  # noqa: E402
from matrx_ai.tools.kinds.tooling import ToolBundleListing  # noqa: E402
from matrx_ai.tools.kinds.wheel import WheelSpinResult  # noqa: E402

#: tool name → the KindModel its implementation returns.
TOOL_RESULT_KINDS: dict[str, type[KindModel]] = {
    # fs_* — the workspace filesystem (claude-tools-01)
    "fs_read": FileReadResult,
    "fs_write": FileWriteResult,
    "fs_list": DirectoryListing,
    "fs_search": FileSearchResults,
    "fs_edit": FileEditResult,
    "fs_patch": FilePatchResult,
    "fs_mkdir": DirectoryCreateResult,
    # trace debugging — the tool system observing itself (claude-tools-02).
    # Three of the four query tools share ONE page shape; debug_traces_by_call
    # does NOT (it is a single call with a joined cx_tool_call record), which
    # the ledger's generated guess got wrong until the implementation was read.
    "debug_traces_recent": ToolTraceEventPage,
    "debug_traces_failures_since": ToolTraceEventPage,
    "debug_traces_by_conv": ToolTraceEventPage,
    "debug_traces_by_call": ToolTraceCallDetail,
    "debug_traces_list_files": ToolTraceFileListing,
    "debug_traces_get_file": ToolTraceFileWindow,
    "report_trace_incident": ToolTraceIncidentReport,
    "get_open_trace_incidents": ToolTraceIncidentList,
    # execution + text + IDE + wheel (lead-w2b).
    # THREE TOOLS, ONE SHAPE: every "a process ran" result is shell_execution.
    "shell_execute": ShellExecution,
    "shell_python": ShellExecution,
    "code_execute_python": ShellExecution,
    "math_calculate": CalculationResult,
    "text_analyze": TextAnalysis,
    # REUSE, not a mint: the tool now returns matrx-graph's RegexExtractOutput,
    # the model behind the registered `regex_extract_result` workflow kind —
    # a `regex_extraction` twin slug would be the NOMENCLATURE defect.
    "text_regex_extract": RegexExtractOutput,
    "vsc_get_state": IdeStateFields,
    "random_wheel": WheelSpinResult,
    # widget_* — ONE implementation, MANY names (lead-w2d). Every widget tool
    # forwards to ctx_write.context_patch / ctx_create and returns its receipt,
    # so the family is ONE kind (see kinds/context_tools.py for why the patch
    # and create branches are one union shape, not twins).
    "widget_text_replace": ContextWriteResult,
    "widget_text_insert_before": ContextWriteResult,
    "widget_text_insert_after": ContextWriteResult,
    "widget_text_prepend": ContextWriteResult,
    "widget_text_append": ContextWriteResult,
    "widget_text_patch": ContextWriteResult,
    "widget_update_field": ContextWriteResult,
    "widget_update_record": ContextWriteResult,
    # …including the two dual-branch widget tools: they return the PATCH branch
    # when the context object exists and the CREATE branch when they create it —
    # one union kind covers both (kinds/context_tools.py).
    "widget_attach_media": ContextWriteResult,
    "widget_create_artifact": ContextWriteResult,
    # toolcomp_* — the tool-component authoring surface, read/create half
    # (lead-w2d). tool_component_sample and tool_component_listing are branch
    # unions; toolcomp_get_code keeps its fenced-block prompt text via
    # provider_content while output carries the kind (kinds/tool_components.py).
    "toolcomp_get_context": ToolComponentContext,
    "toolcomp_get_code": ToolComponentCode,
    "toolcomp_get_sample_detail": ToolComponentSample,
    "toolcomp_get_incident_detail": ToolComponentIncidentDetail,
    "toolcomp_list_tools": ToolComponentListing,
    "toolcomp_create_component": ToolComponentCreateResult,
    # …and the write half (lead-w2d, batch 3). update_code and update_settings
    # are one union receipt (branch-only fields optional).
    "toolcomp_update_code": ToolComponentUpdateResult,
    "toolcomp_update_settings": ToolComponentUpdateResult,
    "toolcomp_patch_code": ToolComponentPatchResult,
    "toolcomp_resolve_incident": ToolComponentIncidentResolution,
    # client-tool loaders — TWO kinds, not one: chrome reports tools LOADED,
    # desktop reports tools QUEUED for the turn-boundary drain
    # (kinds/tool_loading.py).
    "load_chrome_tools": ChromeToolsLoadResult,
    "load_desktop_tools": DesktopToolsLoadResult,
    # code-docs fetchers (kinds/code_docs.py). code_fetch_tree does NOT reuse
    # `file_tree_result` — that kind is exactly {tree, file_count} and this
    # tool reports scoping + the file-type census; the ledger's reuse candidate
    # was a guess, and the shapes genuinely differ.
    "llms_txt_fetch": LlmsTxtDocument,
    "code_fetch_tree": CodeTreeResult,
    # cms_* — the agent-facing CMS surface (lead-w2a). The implementations live
    # in aidream/tools/cms_*_tool.py; the models live HERE because this map may
    # never import aidream (see matrx_ai/tools/kinds/cms.py's docstring).
    **CMS_TOOL_RESULT_KINDS,
    # database group (lead-w2c): data/data_action live in aidream
    # (aidream/tools/data_tool.py), db_admin/db_user in
    # aidream/services/db_grants/tools.py (TWO TOOLS, ONE SHAPE — the same
    # dispatcher), sql in implementations/database.py. The ledger's
    # `sql_query_result` reuse candidate was REJECTED after reading the
    # implementations (kinds/database_tools.py's docstring).
    **DATABASE_TOOL_RESULT_KINDS,
    # scope_system (aidream/services/scope_system/tools.py): render actions
    # reshaped from a bare string into `context` (a scalar cannot carry __kind).
    "scope_system": ScopeSystemResult,
    # value_store (aidream/tools/value_store.py): one union across
    # list/describe/get/put/groom; the paging cap keys are part of the shape.
    "value_store": ValueStoreResult,
    # conversation-context read/write surface (lead-w2e). `context` is the
    # get|batch|create action dispatcher — ONE union kind (the cms precedent);
    # its create branch re-wraps the shared funnel's context_write_result into
    # the union (implementations/ctx.py `_stamp_context_kind`). `context_patch`
    # rides the same funnel as the widget_* tools and shares their kind.
    "context": ContextToolResult,
    "context_patch": ContextWriteResult,
    # instance_* — saved kind instances (lead-w2e). THREE TOOLS, ONE SHAPE for
    # the writes: create/update/delete are one union receipt
    # (kinds/kind_instances.py).
    "instance_create": KindInstanceWriteResult,
    "instance_update": KindInstanceWriteResult,
    "instance_delete": KindInstanceWriteResult,
    "instance_list": KindInstancePage,
    "instance_get": KindInstanceDetail,
    # kind_* authoring surface, read half (lead-w2e batch 1).
    "kind_get": KindDefinitionDetail,
    # kind_* authoring surface, write half + kindcomp read half (lead-w2e
    # batch 2). The tool_component_* reuse candidates were REJECTED after
    # reading both implementations (kinds/kind_components.py docstring).
    "kind_create": KindCreateResult,
    "kind_update_schema": KindSchemaUpdateResult,
    "kind_add_example": KindExampleResult,
    "kind_create_skill": KindSkillResult,
    "kind_create_content_block": KindContentBlockResult,
    "kind_activate": KindActivationResult,
    "kindcomp_get_context": KindComponentContext,
    "kindcomp_get_code": KindComponentCode,
    # kindcomp_* write half (lead-w2e batch 3). update_code and
    # update_settings are one union receipt (the toolcomp precedent).
    "kindcomp_create_component": KindComponentCreateResult,
    "kindcomp_update_code": KindComponentUpdateResult,
    "kindcomp_update_settings": KindComponentUpdateResult,
    "kindcomp_patch_code": KindComponentPatchResult,
    "kindcomp_resolve_incident": KindComponentIncidentResolution,
    # workflow-tool family (lead-w2f): catalog/author/run/node/plan. The
    # `workflow_run_result` reuse candidate was REJECTED — it is the workflow-io
    # SubgraphCallOutput, not this tool's queue/status receipt (see
    # kinds/workflow_tools.py's docstring for the two documented reshapes).
    "workflow_catalog": WorkflowCatalogResult,
    "workflow_author": WorkflowAuthorResult,
    "workflow_run": WorkflowRunStatus,
    "workflow_node": WorkflowNodeResult,
    "workflow_plan": WorkflowPlanResult,
    # tasks (aidream/tools/agent_tasks_tool.py): NOT the content `task_list`
    # kind — these are chat.agent_task rows with ids + a status enum.
    "tasks": AgentTaskList,
    # user_secret_set (implementations/user_secrets_tool.py): package-hosted,
    # stamps inline; the receipt carries only the vault's masked value_hint.
    "user_secret_set": UserSecretReceipt,
    # workbook (aidream/services/udt_content/tools.py): NOT `office_spreadsheet`
    # (the .xlsx generation SPEC) — this is the create/read/edit receipt union.
    "workbook": WorkbookResult,
    # workbench dispatchers (lead-w2f batch 2, package-hosted, no active
    # binding — runtime proven by direct call, the `sql` precedent). `task` is
    # the WORKBENCH project-task surface: not `agent_task_list` (the per-
    # conversation agent tasklist) and not `task_list` (the content checklist).
    "task": TaskToolResult,
    "skill": SkillToolResult,
    "picklist": PicklistToolResult,
    # aidream-hosted agent-ops tools (lead-w2f batch 2). `office` does NOT bind
    # the office_file_result/office_extraction_result node kinds — one declared
    # kind per tool, and its extract branch is a summary (see kinds/agent_ops.py).
    "self_prompt": SelfPromptResult,
    "rulebook": RulebookToolResult,
    "research_run": ResearchRunState,
    "office": OfficeToolResult,
}

#: Generated tool FAMILIES: one implementation serves every member, so the
#: family is declared by its prefix rather than by enumerating names that the
#: registry mints on its own (43 ``bundle:list_*`` listers today, more tomorrow).
TOOL_RESULT_KIND_PREFIXES: tuple[tuple[str, type[KindModel]], ...] = (
    ("bundle:list_", ToolBundleListing),
)


def result_kind_model(tool_name: str) -> type[KindModel] | None:
    """The KindModel ``tool_name``'s implementation is declared to return."""
    model = TOOL_RESULT_KINDS.get(tool_name)
    if model is not None:
        return model
    for prefix, prefixed in TOOL_RESULT_KIND_PREFIXES:
        if tool_name.startswith(prefix):
            return prefixed
    return None


def result_kind_slug(tool_name: str) -> str | None:
    """The registered kind slug ``tool_name``'s result is declared to carry."""
    model = result_kind_model(tool_name)
    return None if model is None else str(model.kind_slug)


def declared_result_kinds(tool_names: Iterable[str]) -> dict[str, str]:
    """``{tool: slug}`` for every declared name in ``tool_names``."""
    resolved = ((name, result_kind_slug(name)) for name in tool_names)
    return {name: slug for name, slug in resolved if slug}
