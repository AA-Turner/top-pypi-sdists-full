# Copyright (c) 2025 Airbyte, Inc., all rights reserved.
"""The `run_regression_tests` tool's contract with the workflow it dispatches."""

from __future__ import annotations

from pathlib import Path
from typing import Any
from unittest.mock import patch

import pytest
import yaml

from airbyte_ops_mcp.github_actions import WorkflowDispatchResult
from airbyte_ops_mcp.mcp import connector_qa
from airbyte_ops_mcp.mcp.connector_qa import (
    REGRESSION_TEST_WORKFLOW_FILE,
    ConnectorRepo,
    run_regression_tests,
)

pytestmark = pytest.mark.unit

WORKFLOW_PATH = (
    Path(__file__).resolve().parents[1]
    / ".github/workflows"
    / REGRESSION_TEST_WORKFLOW_FILE
)


def _declared_inputs() -> set[str]:
    """The inputs the dispatched workflow actually accepts.

    GitHub rejects a dispatch carrying an input the workflow does not declare,
    so a name that drifts here fails at trigger time, in someone else's session.

    The *intersection* of both trigger blocks, because the workflow is both
    dispatched and called as a sub-workflow, and the two input lists are edited
    by hand. An input declared only under `workflow_dispatch` satisfies the tool
    that dispatches it and fails whoever calls the workflow as a sub-workflow, so
    a union here would pass on exactly the drift this test exists to catch.
    """
    workflow = yaml.safe_load(WORKFLOW_PATH.read_text())
    # `on:` parses as the boolean True in YAML 1.1.
    triggers = workflow[True] if True in workflow else workflow["on"]

    return set.intersection(
        *(
            set(triggers[trigger]["inputs"])
            for trigger in ("workflow_dispatch", "workflow_call")
        )
    )


def _dispatch(**kwargs: Any) -> dict[str, str]:
    """Run the tool with the dispatch stubbed; return the inputs it sent."""
    sent: dict[str, str] = {}

    def _fake_dispatch(*, inputs: dict[str, str], **_kwargs: Any):
        sent.update(inputs)
        return WorkflowDispatchResult(workflow_url="https://example.com/workflow")

    with patch.object(
        connector_qa, "trigger_workflow_dispatch", _fake_dispatch
    ), patch.object(connector_qa, "resolve_ci_trigger_github_token", lambda: "token"):
        run_regression_tests(
            connector_name="source-pokeapi",
            pr=1,
            repo=ConnectorRepo.AIRBYTE,
            **kwargs,
        )

    return sent


def test_disable_http_replay_reaches_the_workflow() -> None:
    assert _dispatch(disable_http_replay=True)["disable_http_replay"] == "true"


def test_replay_is_left_on_by_default() -> None:
    """Omitted rather than sent as "false": the workflow default is already off."""
    assert "disable_http_replay" not in _dispatch()


def test_every_input_the_tool_sends_is_declared_by_the_workflow() -> None:
    """The two sides are edited independently and only meet at dispatch time.

    A name that exists on one side and not the other is not a test failure
    anywhere else -- it is a rejected dispatch for whoever calls the tool next.
    """
    sent = _dispatch(
        connection_id="00000000-0000-0000-0000-000000000000",
        skip_compare=True,
        skip_read_action=True,
        override_test_image="airbyte/source-pokeapi:1.0.0",
        override_control_image="airbyte/source-pokeapi:0.9.0",
        selected_streams=["pokemon"],
        enable_debug_logs=True,
        with_state=True,
        disable_http_replay=True,
    )

    assert sent, "the tool sent no inputs, so this asserts nothing"
    assert set(sent) <= _declared_inputs()
