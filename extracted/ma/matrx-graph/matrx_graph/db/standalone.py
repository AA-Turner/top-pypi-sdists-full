"""Standalone matrx-orm models for matrx-graph's workflow schema."""

from __future__ import annotations

from typing import Any

_MODEL_CACHE: dict[str, dict[str, Any]] = {}


def _matrx_orm() -> Any:
    try:
        import matrx_orm
    except ImportError as exc:
        raise RuntimeError(
            "matrx_graph.db.standalone requires matrx-orm. "
            "Install with `pip install matrx-graph[postgres]`."
        ) from exc
    return matrx_orm


def build_standalone_models(
    database: str = "supabase_automation_matrix",
) -> dict[str, Any]:
    """Build Models matching ``0100_baseline_post_reorg.sql`` exactly."""
    cached = _MODEL_CACHE.get(database)
    if cached is not None:
        return cached

    m = _matrx_orm()

    class WfDefinition(m.Model):
        id = m.UUIDField(primary_key=True, null=False)
        name = m.TextField(null=False)
        description = m.TextField()
        nodes = m.JSONBField(null=False, default=[])
        edges = m.JSONBField(null=False, default=[])
        viewport = m.JSONBField(null=False, default={"x": 0, "y": 0, "zoom": 1})
        channels = m.JSONBField(null=False, default=[])
        strict_channels = m.BooleanField(null=False, default=False)
        entry_nodes = m.JSONBField(null=False, default=[])
        variables = m.JSONBField(null=False, default=[])
        metadata = m.JSONBField(null=False, default={})
        version = m.IntegerField(null=False, default=1)
        is_active = m.BooleanField(null=False, default=True)
        is_archived = m.BooleanField(null=False, default=False)
        visibility = m.TextField(null=False, default="internal")
        shown_to = m.TextField()
        published_to_web = m.BooleanField(null=False, default=False)
        published_to_web_at = m.DateTimeField()
        published_to_web_by = m.UUIDField()
        # 'user' | 'builtin' | 'generated' (mirrors agent.definition.agent_type)
        workflow_type = m.TextField(null=False, default="user")
        is_favorite = m.BooleanField(null=False, default=False)
        tags = m.TextArrayField(null=False, default=[])
        category = m.TextField()
        created_by = m.UUIDField(null=False)
        organization_id = m.UUIDField()
        project_id = m.UUIDField()
        task_id = m.UUIDField()
        source_definition_id = m.UUIDField()
        source_snapshot_at = m.DateTimeField()
        max_concurrent_runs = m.IntegerField()
        # SPEC-workflow-ui-contract §2.1 — the author-declared IO contract.
        input_kind = m.TextField()
        output_kind = m.TextField()
        deleted_at = m.DateTimeField()
        created_at = m.DateTimeField(null=False)
        updated_at = m.DateTimeField(null=False)
        _database = database
        _table_name = "definition"
        _db_schema = "workflow"

    class WfDefinitionVersion(m.Model):
        id = m.UUIDField(primary_key=True, null=False)
        definition_id = m.UUIDField(null=False)
        version_number = m.IntegerField(null=False)
        name = m.TextField()
        description = m.TextField()
        nodes = m.JSONBField()
        edges = m.JSONBField()
        viewport = m.JSONBField()
        channels = m.JSONBField()
        strict_channels = m.BooleanField()
        entry_nodes = m.JSONBField()
        variables = m.JSONBField(null=False, default=[])
        metadata = m.JSONBField()
        tags = m.TextArrayField()
        category = m.TextField()
        is_active = m.BooleanField()
        change_note = m.TextField()
        changed_by_user_id = m.UUIDField()
        # SPEC §2.1 — snapshot of the declaration at publish time.
        input_kind = m.TextField()
        output_kind = m.TextField()
        changed_at = m.DateTimeField(null=False)
        _database = database
        _table_name = "definition_version"
        _db_schema = "workflow"

    class WfRun(m.Model):
        id = m.UUIDField(primary_key=True, null=False)
        thread_id = m.UUIDField(null=False)
        parent_run_id = m.UUIDField()
        definition_id = m.UUIDField(null=False)
        definition_version_id = m.UUIDField()
        definition_hash = m.TextField(null=False)
        status = m.TextField(null=False, default="pending")
        input = m.JSONBField(null=False, default={})
        output = m.JSONBField()
        error = m.JSONBField()
        interrupt_payload = m.JSONBField()
        steps_executed = m.IntegerField(null=False, default=0)
        last_checkpoint_id = m.UUIDField()
        created_by = m.UUIDField(null=False)
        organization_id = m.UUIDField()
        project_id = m.UUIDField()
        task_id = m.UUIDField()
        conversation_id = m.UUIDField()
        agent_id = m.UUIDField()
        agent_version_id = m.UUIDField()
        metadata = m.JSONBField(null=False, default={})
        max_recovery_retries = m.IntegerField(null=False, default=25)
        recovery_retry_count = m.IntegerField(null=False, default=0)
        event_seq = m.BigIntegerField(null=False, default=0)
        request_attribution_complete = m.BooleanField(null=False, default=False)
        deleted_at = m.DateTimeField()
        created_at = m.DateTimeField(null=False)
        started_at = m.DateTimeField()
        completed_at = m.DateTimeField()
        _database = database
        _table_name = "run"
        _db_schema = "workflow"

    class WfCheckpoint(m.Model):
        id = m.UUIDField(primary_key=True, null=False)
        run_id = m.UUIDField(null=False)
        thread_id = m.UUIDField(null=False)
        parent_checkpoint_id = m.UUIDField()
        step = m.IntegerField(null=False)
        channel_values = m.JSONBField(null=False, default={})
        pending_bindings = m.JSONBField(null=False, default={})
        next_invocations = m.JSONBField(null=False, default=[])
        interrupt_payload = m.JSONBField()
        metadata = m.JSONBField(null=False, default={})
        created_at = m.DateTimeField(null=False)
        organization_id = m.UUIDField()
        _database = database
        _table_name = "checkpoint"
        _db_schema = "workflow"

    class WfCheckpointValue(m.Model):
        id = m.UUIDField(primary_key=True, null=False)
        run_id = m.UUIDField(null=False)
        organization_id = m.UUIDField()
        value_hash = m.TextField(null=False)
        value = m.JSONBField(null=False, strings_are_values=True)  # agent answers are often JSON text
        size_bytes = m.IntegerField(null=False, default=0)
        created_at = m.DateTimeField(null=False)
        _database = database
        _table_name = "checkpoint_value"
        _db_schema = "workflow"

    class WfNodeOutcome(m.Model):
        id = m.UUIDField(primary_key=True, null=False)
        run_id = m.UUIDField(null=False)
        step = m.IntegerField(null=False)
        node_id = m.TextField(null=False)
        attempt = m.IntegerField(null=False, default=1)
        dispatch_id = m.TextField(null=False, default="")
        item_index = m.IntegerField(null=False, default=0)
        output = m.JSONBField(null=False, default={})
        channel_writes = m.JSONBField(null=False, default=[])
        sends = m.JSONBField(null=False, default=[])
        emissions = m.JSONBField(null=False, default={})
        duration_ms = m.IntegerField(null=False, default=0)
        error = m.JSONBField()
        source = m.TextField(null=False, default="executor")
        output_kind = m.TextField()
        output_kind_ok = m.BooleanField()
        output_kind_errors = m.JSONBField()
        output_kind_version = m.IntegerField()
        output_kind_degraded = m.TextField()
        completed_at = m.DateTimeField(null=False)
        organization_id = m.UUIDField()
        _database = database
        _table_name = "node_outcome"
        _db_schema = "workflow"

    class WfWorkItem(m.Model):
        id = m.UUIDField(primary_key=True, null=False)
        organization_id = m.UUIDField(null=False)
        run_id = m.UUIDField(null=False)
        set_name = m.TextField(null=False, default="default")
        seq = m.BigIntegerField()
        canonical_key = m.TextField(null=False)
        payload = m.JSONBField(null=False, default={})
        state = m.TextField(null=False, default="pending")
        attempts = m.IntegerField(null=False, default=0)
        max_attempts = m.IntegerField(null=False, default=3)
        wave = m.IntegerField(null=False, default=0)
        discovered_by = m.TextField(null=False, default="")
        claim_holder = m.TextField()
        claimed_at = m.DateTimeField()
        lease_expires_at = m.DateTimeField()
        error = m.JSONBField()
        created_at = m.DateTimeField(null=False)
        completed_at = m.DateTimeField()
        _database = database
        _table_name = "work_item"
        _db_schema = "workflow"

    class WfNodeEvents(m.Model):
        id = m.UUIDField(primary_key=True, null=False)
        run_id = m.UUIDField(null=False)
        event_type = m.TextField(null=False)
        step = m.IntegerField()
        node_id = m.TextField()
        spec_type = m.TextField()
        attempt = m.IntegerField()
        duration_ms = m.IntegerField()
        checkpoint_id = m.UUIDField()
        error_type = m.TextField()
        error_message = m.TextField()
        payload = m.JSONBField(null=False)
        seq = m.BigIntegerField()
        event_ts = m.DateTimeField(null=False)
        created_at = m.DateTimeField(null=False)
        _database = database
        _table_name = "node_events"
        _db_schema = "workflow"

    class WfJob(m.Model):
        id = m.UUIDField(primary_key=True, null=False)
        run_id = m.UUIDField(null=False)
        kind = m.TextField(null=False)
        checkpoint_id = m.UUIDField()
        resume_value = m.JSONBField()
        inputs = m.JSONBField(null=False, default={})
        max_steps = m.IntegerField(null=False, default=1000)
        priority = m.IntegerField(null=False, default=0)
        visible_at = m.DateTimeField(null=False)
        claimed_at = m.DateTimeField()
        claimed_by = m.TextField()
        attempt = m.IntegerField(null=False, default=0)
        max_attempts = m.IntegerField(null=False, default=3)
        last_error = m.JSONBField()
        created_at = m.DateTimeField(null=False)
        updated_at = m.DateTimeField(null=False)
        _database = database
        _table_name = "job"
        _db_schema = "workflow"

    class WfTrigger(m.Model):
        id = m.UUIDField(primary_key=True, null=False)
        definition_id = m.UUIDField(null=False)
        definition_version_id = m.UUIDField()
        name = m.TextField(null=False)
        description = m.TextField()
        kind = m.TextField(null=False)
        cron_expression = m.TextField()
        timezone = m.TextField(null=False, default="UTC")
        webhook_secret = m.TextField()
        default_inputs = m.JSONBField(null=False, default={})
        max_steps = m.IntegerField(null=False, default=1000)
        callback_url = m.TextField()
        is_active = m.BooleanField(null=False, default=True)
        last_fired_at = m.DateTimeField()
        last_run_id = m.UUIDField()
        next_run_at = m.DateTimeField()
        fire_count = m.IntegerField(null=False, default=0)
        created_by = m.UUIDField(null=False)
        organization_id = m.UUIDField()
        project_id = m.UUIDField()
        task_id = m.UUIDField()
        deleted_at = m.DateTimeField()
        created_at = m.DateTimeField(null=False)
        updated_at = m.DateTimeField(null=False)
        _database = database
        _table_name = "trigger"
        _db_schema = "workflow"

    class WfNodeDataSlot(m.Model):
        id = m.UUIDField(primary_key=True, null=False)
        definition_id = m.UUIDField(null=False)
        node_id = m.TextField(null=False)
        slot = m.TextField(null=False)
        value = m.JSONBField(null=False)
        emissions = m.JSONBField(null=False, default={})
        output_kind = m.TextField()
        source = m.TextField(null=False)
        captured_at = m.DateTimeField(null=False)
        captured_by = m.UUIDField()
        created_by = m.UUIDField(null=False)
        _database = database
        _table_name = "node_data_slot"
        _db_schema = "workflow"

    models = {
        model.__name__: model
        for model in (
            WfDefinition,
            WfDefinitionVersion,
            WfRun,
            WfCheckpoint,
            WfCheckpointValue,
            WfNodeOutcome,
            WfNodeEvents,
            WfJob,
            WfTrigger,
            WfNodeDataSlot,
            WfWorkItem,
        )
    }
    _MODEL_CACHE[database] = models
    return models


def configure_standalone_db(
    database: str = "supabase_automation_matrix",
) -> dict[str, Any]:
    """Register baseline-compatible Models and generic managers."""
    from matrx_graph.db._registry import configure_db

    m = _matrx_orm()
    models = build_standalone_models(database)
    manager_keys = {
        "wf_definition_manager": "WfDefinition",
        "wf_definition_version_manager": "WfDefinitionVersion",
        "wf_run_manager": "WfRun",
        "wf_checkpoint_manager": "WfCheckpoint",
        "wf_checkpoint_value_manager": "WfCheckpointValue",
        "wf_node_outcome_manager": "WfNodeOutcome",
        "wf_trigger_manager": "WfTrigger",
        "wf_job_manager": "WfJob",
        "wf_node_events_manager": "WfNodeEvents",
        "wf_node_data_slot_manager": "WfNodeDataSlot",
        "wf_work_item_manager": "WfWorkItem",
    }
    configure_db(
        models=models,
        instances={
            key: m.BaseManager(models[model_key]) for key, model_key in manager_keys.items()
        },
    )
    return models
