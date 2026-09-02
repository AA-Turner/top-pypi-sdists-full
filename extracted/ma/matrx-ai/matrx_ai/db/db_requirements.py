# File: matrx_ai/db/db_requirements.py
# Declarative manifest of the host DB artifacts matrx-ai needs. Data only —
# imports nothing, names no host module paths. Consumed by matrx-orm's
# package_wiring generator (python db/generate.py), which resolves every table
# against the host's freshly-generated inventory (db/helpers/auto_config_*.py)
# and emits the aidream-side wiring module that calls matrx_ai.configure(...).
# Keep this in sync with what matrx_ai.db._registry.get_model/get_base/
# get_instance/get_extra look up by name.
#
# The registry KEY is the contract, not the class name — matrx-ai's cxm/agx/
# catalog managers do get_model("Conversation") / get_base("ConversationBase")
# and build their own singletons. Most of the chat set is a plain rule; the ai
# catalog + skill/tool aliases are irregular (renames, one-table-N-keys) and are
# spelled out explicitly below.

DB_REQUIREMENTS = {
    "target": {
        "configure_import": "matrx_ai",
        "configure_call": "configure",
        "models_kwarg": "db_models",
        "bases_kwarg": "db_bases",
        "instances_kwarg": "db_instances",
        "extras_kwarg": "db_extras",
    },
    # RULE — every listed chat table -> model(key=Pascal) + base(key=PascalBase).
    # The chat schema has more tables than matrx-ai wires today, so the set is
    # pinned via include_tables for exact parity. To let NEW chat tables auto-
    # flow to matrx-ai in future, delete include_tables[chat] (optionally add
    # exclude_tables[chat] for the non-conversation ones) and regenerate.
    "schemas": ["chat"],
    "include_tables": {
        "chat": [
            "agent_run",
            "agent_run_stage",
            "agent_memory",
            "conversation",
            "media",
            "message",
            "observational_memory",
            "observational_memory_event",
            "pending_injection",
            "request",
            "request_snapshot",
            "tool_call",
            "tool_trace",
            "user_request",
        ],
    },
    "models": [
        # ai catalog — plain keys.
        {"key": "Endpoint", "table": "ai.endpoint"},
        {"key": "Provider", "table": "ai.provider"},
        {"key": "Voices", "table": "ai.voices"},
        # ai catalog — Ai* vocabulary aliases (matrx_ai.catalog).
        {"key": "AiModel", "table": "ai.model_definition"},
        {"key": "AiProvider", "table": "ai.provider"},
        {"key": "AiEndpoint", "table": "ai.endpoint"},
        {"key": "AiApi", "table": "ai.api"},
        {"key": "AiModelAlias", "table": "ai.model_alias"},
        {"key": "AiOffering", "table": "ai.offering"},
        {"key": "AiSetting", "table": "ai.setting"},
        # skill.render_definition — the canonical block table (content_blocks retired).
        {"key": "RenderDefinition", "table": "skill.render_definition"},
        # platform — the judge accuracy ledger (matrx_ai.evaluators.judge).
        {"key": "JudgeVerdict", "table": "platform.judge_verdict"},
        # public.
        {"key": "OpsIssueClass", "table": "ops.ops_issue_class"},
        {"key": "OpsIssueEvent", "table": "ops.ops_issue_event"},
        # users — feedback bridge (tools/implementations/feedback_tools.py).
        {"key": "UserFeedback", "table": "users.user_feedback"},
        # write-failure recovery engine (persistence/replay.py).
        {"key": "SystemWriteFailure", "table": "ops.system_write_failure"},
        # workbench (UDT + notes).
        {"key": "UdtDatasets", "table": "workbench.udt_datasets"},
        {"key": "UdtDatasetFields", "table": "workbench.udt_dataset_fields"},
        {"key": "UdtDatasetRows", "table": "workbench.udt_dataset_rows"},
        {"key": "UdtStructuredLists", "table": "workbench.udt_structured_lists"},
        {"key": "UdtStructuredListItems", "table": "workbench.udt_structured_list_items"},
        {"key": "Notes", "table": "workbench.notes"},
        # DataRef context injection (data_ref.py) — projects + organizations.
        {"key": "Projects", "table": "workspace.projects"},
        {"key": "Organizations", "table": "iam.organizations"},
        # workspace.tasks — three vocabulary keys, one class.
        {"key": "WsTasks", "table": "workspace.tasks"},
        {"key": "CtxTasks", "table": "workspace.tasks"},
        {"key": "Tasks", "table": "workspace.tasks"},
        # agent.
        {"key": "Definition", "table": "agent.definition"},
        {"key": "DefinitionVersion", "table": "agent.definition_version"},
        {"key": "Shortcut", "table": "agent.shortcut"},
        # tool — UI component authoring bridge (tools/implementations/tool_component.py)
        # + the admin `sql`/`db_*` tools' dynamic table access (database.py).
        {"key": "ToolDefinition", "table": "tool.definition"},
        {"key": "ToolUi", "table": "tool.ui"},
        {"key": "ToolTestSample", "table": "tool.test_sample"},
        {"key": "ToolUiIncident", "table": "tool.ui_incident"},
        # content_ir — kind-registry authoring bridge
        # (tools/implementations/kind_component.py + kind_authoring.py).
        {"key": "KindDefinition", "table": "content_ir.kind_definition"},
        {"key": "KindEdge", "table": "content_ir.kind_edge"},
        {"key": "KindExample", "table": "content_ir.kind_example"},
        {"key": "KindComponent", "table": "content_ir.kind_component"},
        {"key": "KindSurface", "table": "content_ir.kind_surface"},
        {"key": "KindComponentIncident", "table": "content_ir.kind_component_incident"},
        {"key": "KindInstance", "table": "content_ir.kind_instance"},
        # skill (+ legacy plural keys) — categories live in platform.categories.
        {"key": "SklDefinition", "table": "skill.definition"},
        {"key": "SklCategory", "table": "platform.categories"},
        {"key": "SklDefinitions", "table": "skill.definition"},
        {"key": "SklCategories", "table": "platform.categories"},
    ],
    "bases": [
        # ai catalog — irregular base keys.
        {"key": "AiEndpointBase", "table": "ai.endpoint"},
        {"key": "AiModelBase", "table": "ai.model_definition"},
        {"key": "ProviderBase", "table": "ai.provider"},
        # workspace.tasks — three base keys, one class.
        {"key": "WsTasksBase", "table": "workspace.tasks"},
        {"key": "CtxTasksBase", "table": "workspace.tasks"},
        {"key": "TasksBase", "table": "workspace.tasks"},
        # workbench.
        {"key": "NotesBase", "table": "workbench.notes"},
        # agent.
        {"key": "DefinitionBase", "table": "agent.definition"},
        {"key": "DefinitionVersionBase", "table": "agent.definition_version"},
        {"key": "ShortcutBase", "table": "agent.shortcut"},
        # tool — ToolDef*/Tool* alias bases.
        {"key": "ToolDefBase", "table": "tool.definition"},
        {"key": "ToolDefinitionBase", "table": "tool.definition"},
        {"key": "ToolBindingBase", "table": "tool.binding"},
        {"key": "ToolExecutorBase", "table": "tool.executor"},
        # skill (+ legacy plural keys).
        {"key": "SklDefinitionBase", "table": "skill.definition"},
        {"key": "SklCategoryBase", "table": "platform.categories"},
        {"key": "SklDefinitionsBase", "table": "skill.definition"},
        {"key": "SklCategoriesBase", "table": "platform.categories"},
    ],
    "instances": [
        {"keys": ["guest_executions_manager"], "table": "users.guest_executions"},
        {"keys": ["guest_execution_log_manager"], "table": "users.guest_execution_log"},
        {"keys": ["skl_definitions_manager"], "table": "skill.definition"},
        {"keys": ["skl_categories_manager"], "table": "platform.categories"},
        {"keys": ["definition_manager_instance", "tool_def_manager_instance"], "table": "tool.definition"},
        {"keys": ["binding_manager_instance", "tool_binding_manager_instance"], "table": "tool.binding"},
        {"keys": ["executor_manager_instance", "tool_executor_manager_instance"], "table": "tool.executor"},
        {"keys": ["bundle_manager_instance", "tool_bundle_manager_instance"], "table": "tool.bundle"},
        # tool.bundle_member retired -> membership lives in platform.associations.
        {"keys": ["associations_manager_instance"], "table": "platform.associations"},
        {"keys": ["surface_defaults_manager_instance", "tool_surface_defaults_manager_instance"], "table": "tool.surface_defaults"},
        {"keys": ["mcp_server_manager_instance", "tool_mcp_server_manager_instance"], "table": "tool.mcp_server"},
        {"keys": ["mcp_config_manager_instance", "tool_mcp_config_manager_instance"], "table": "tool.mcp_config"},
    ],
    "extras": [
        {
            "key": "RenderDefinitionDTO",
            "import_from": "db.managers.skill.render_definition",
            "symbol": "RenderDefinitionDTO",
        },
    ],
}
