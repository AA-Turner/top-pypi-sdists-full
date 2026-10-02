"""SchAgentTask / SchTrigger accept asyncpg-style jsonb strings."""

from __future__ import annotations

import json

from matrx_scheduler.models import SchAgentTask, SchRun, SchTrigger


def test_sch_agent_task_variables_from_json_string():
    task = SchAgentTask(
        id="a7c1e2d3-0000-4e5f-9a00-000000000034",
        prompt="drain",
        variables=json.dumps({"args": {}, "tool_name": "suggestion_sweep_drain"}),
    )
    assert task.variables == {"args": {}, "tool_name": "suggestion_sweep_drain"}


def test_sch_agent_task_variables_from_dict():
    task = SchAgentTask(
        id="a7c1e2d3-0000-4e5f-9a00-000000000034",
        prompt="drain",
        variables={"tool_name": "ping"},
    )
    assert task.variables["tool_name"] == "ping"


def test_sch_trigger_config_from_json_string():
    trigger = SchTrigger(
        id="t1",
        task_id="a7c1e2d3-0000-4e5f-9a00-000000000034",
        user_id="u1",
        type="interval",
        config=json.dumps({"every_seconds": 60}),
    )
    assert trigger.config == {"every_seconds": 60}


def test_sch_run_output_ref_from_json_string():
    from datetime import UTC, datetime

    run = SchRun(
        id="r1",
        task_id="a7c1e2d3-0000-4e5f-9a00-000000000034",
        user_id="u1",
        organization_id="33333333-3333-4333-8333-333333333333",
        status="queued",
        due_at=datetime.now(UTC),
        output_ref=json.dumps({"ok": True}),
    )
    assert run.output_ref == {"ok": True}
