# File: matrx_graph/db/db_requirements.py
# Declarative manifest of the host DB artifacts matrx-graph needs. Data only —
# imports nothing, names no host module paths. Consumed by matrx-orm's
# package_wiring generator (python db/generate.py), which resolves every table
# against the host's freshly-generated inventory and emits the aidream-side
# wiring module that calls matrx_graph.db.configure_db(...). Keep this in sync
# with what matrx_graph.db._registry.get_model/get_base/get_instance look up.
#
# matrx-graph consumes 5 of the workflow.* tables plus the platform kind
# registry (content_ir.kind_definition — node I/O declared as kinds, see
# matrx_graph/kinds.py). Every workflow registry key is Wf-prefixed (a rename
# of the plain generated class name), so all entries are explicit rather than
# a whole-schema rule.

DB_REQUIREMENTS = {
    "target": {
        "configure_import": "matrx_graph.db",
        "configure_call": "configure_db",
        "models_kwarg": "models",
        "bases_kwarg": "bases",
        "instances_kwarg": "instances",
        "extras_kwarg": "extras",
    },
    "models": [
        {"key": "WfDefinition", "table": "workflow.definition"},
        {"key": "WfDefinitionVersion", "table": "workflow.definition_version"},
        {"key": "WfRun", "table": "workflow.run"},
        {"key": "WfCheckpoint", "table": "workflow.checkpoint"},
        {"key": "WfNodeOutcome", "table": "workflow.node_outcome"},
        # Large checkpoint values stored once per run, by sha256 (MKT-111;
        # matrx_graph/checkpoint/values.py). Written/read only by the
        # Postgres checkpointer.
        {"key": "WfCheckpointValue", "table": "workflow.checkpoint_value"},
        # The USER's diagnostic log (log.record). A ledger table: SELECT-only
        # for users, written by the server. Never the platform system_error
        # queue — workflows are authored by users.
        {"key": "WfRunLog", "table": "workflow.run_log"},
        # Review flags grouped into ONE issue per (workflow, step, connection, label)
        # by the run_log trigger (0117). The engine only reads it.
        {"key": "WfReviewIssue", "table": "workflow.review_issue"},
        {"key": "WfTrigger", "table": "workflow.trigger"},
        {"key": "WfTriggerEvent", "table": "workflow.trigger_event"},
        {"key": "WfJob", "table": "workflow.job"},
        {"key": "WfNodeEvents", "table": "workflow.node_events"},
        {"key": "WfNodeDataSlot", "table": "workflow.node_data_slot"},
        {"key": "WfWorkItem", "table": "workflow.work_item"},
        # Run once per key (data.once, matrx_graph/once.py): claims + reusable step results.
        {"key": "WfStepResult", "table": "workflow.step_result"},
        {"key": "WfPlan", "table": "workflow.plan"},
        {"key": "WfPlanSample", "table": "workflow.plan_sample"},
        {"key": "WfPlanEvent", "table": "workflow.plan_event"},
        {"key": "KindDefinition", "table": "content_ir.kind_definition"},
        {"key": "KindExample", "table": "content_ir.kind_example"},
        # Declared kind composition (parent field -> child kind). The
        # Kind Availability Index reads it as its FIRST nesting source:
        # most registered kinds predate KindModel and their schemas do not
        # pin __kind on nested positions, so kind_edge is the only place
        # their interiors are declared at all.
        {"key": "KindEdge", "table": "content_ir.kind_edge"},
    ],
    "bases": [
        {"key": "WfDefinitionBase", "table": "workflow.definition"},
        {"key": "WfDefinitionVersionBase", "table": "workflow.definition_version"},
        {"key": "WfRunBase", "table": "workflow.run"},
        {"key": "WfCheckpointBase", "table": "workflow.checkpoint"},
        {"key": "WfNodeOutcomeBase", "table": "workflow.node_outcome"},
    ],
    "instances": [
        {"keys": ["wf_definition_manager"], "table": "workflow.definition"},
        {"keys": ["wf_definition_version_manager"], "table": "workflow.definition_version"},
        {"keys": ["wf_run_manager"], "table": "workflow.run"},
        {"keys": ["wf_checkpoint_manager"], "table": "workflow.checkpoint"},
        {"keys": ["wf_node_outcome_manager"], "table": "workflow.node_outcome"},
        {"keys": ["wf_trigger_manager"], "table": "workflow.trigger"},
        {"keys": ["wf_trigger_event_manager"], "table": "workflow.trigger_event"},
        {"keys": ["wf_job_manager"], "table": "workflow.job"},
        {"keys": ["wf_node_events_manager"], "table": "workflow.node_events"},
        {"keys": ["wf_node_data_slot_manager"], "table": "workflow.node_data_slot"},
        {"keys": ["wf_work_item_manager"], "table": "workflow.work_item"},
        {"keys": ["wf_step_result_manager"], "table": "workflow.step_result"},
        {"keys": ["wf_plan_manager"], "table": "workflow.plan"},
        {"keys": ["wf_plan_sample_manager"], "table": "workflow.plan_sample"},
        {"keys": ["wf_plan_event_manager"], "table": "workflow.plan_event"},
        {"keys": ["kind_definition_manager"], "table": "content_ir.kind_definition"},
        {"keys": ["kind_example_manager"], "table": "content_ir.kind_example"},
        {"keys": ["kind_edge_manager"], "table": "content_ir.kind_edge"},
    ],
}
