"""A DEFINITION THAT SAVES IS A DEFINITION THAT CAN START (W68, 2026-09-12).

The defect, live: the Masterwork Conductor authored an ``ai.agent.tool_calling``
node with ``model`` / ``user_input`` / ``system_instruction`` / ``tools`` /
``max_iterations`` under ``data.config``. The config schema forbids extras, so
the save gate answered nothing but "Extra inputs are not permitted" — once per
key. The agent did the only thing that message suggests: it DELETED the keys one
at a time until the node read ``{"id": "primary_care_agent", "type":
"ai.agent.tool_calling", "data": {"label": "…"}}``. That saved
(``saved: true``), and workflow ``805c1a98-e64c-43a0-b8a8-eca94b78236a`` died at
step 1 with ``missing_input`` on ``model``. Two separate holes, both closed
here:

1. every REQUIRED field of a node's registered ``input_schema`` must have a
   source at save time — a literal under ``data.inputs``, an inbound connection
   that maps it, or (for an entry node) a name on the compiled input surface.
   A gap the definition PROVES (the step is fired by connections that carry
   nothing) is an error; an entry node's gap is a warning, because a host- or
   trigger-started run may broadcast inputs no definition can declare;
2. a config key rejected as an extra that IS a field of the node's
   ``input_schema`` is told where it belongs, instead of being told only that it
   is not allowed.

The third hole the same conductor found the same day: ``{{sealed_case_id}}``
authored inside an agent node's ``user_input``. Nothing but ``text.template``
renders placeholders, so the tool received those 18 characters verbatim and the
run died on "invalid input syntax for type uuid".

The node below MIRRORS the contract that W68 node had (``AgentLoopInput`` of the
since-deleted ``ai.agent.tool_calling``, tombstoned 2026-10-29) — same required
fields, same closed config — under a test-only type name, registered into a local
registry.
"""

from __future__ import annotations

from typing import Any, ClassVar

from matrx_graph import NodeRegistry, register_builtin_nodes
from matrx_graph.types.context import NodeExecutionContext
from matrx_graph.types.handle import HandleDirection, HandleSpec
from matrx_graph.types.node_spec import NodeSpec
from matrx_graph.types.primitives import ActionTier, NodeCategory
from matrx_graph.types.result import NodeResult, success
from matrx_graph.validation import validate_definition
from pydantic import BaseModel, ConfigDict, Field


class _AgentLoopInput(BaseModel):
    """Mirror of matrx_ai's AgentLoopInput (the W68 node's real contract)."""

    model_config = ConfigDict(extra="allow")

    model: str = Field(min_length=1)
    user_input: str = Field(min_length=1)
    system_instruction: str | None = None
    tools: list[str] = Field(default_factory=list)
    max_iterations: int = 100


class _AgentOutput(BaseModel):
    model_config = ConfigDict(extra="allow")

    final_text: str = ""


class _AgentConfig(BaseModel):
    model_config = ConfigDict(extra="forbid")


class _ToolCallingAgentExecutor:
    spec: ClassVar[NodeSpec] = NodeSpec(
        type="test.agent_loop",
        category=NodeCategory.AGENT,
        display_name="Agent with Tools",
        input_schema=_AgentLoopInput,
        output_schema=_AgentOutput,
        config_schema=_AgentConfig,
        handles=(
            HandleSpec(id="in", direction=HandleDirection.INPUT),
            HandleSpec(id="out", direction=HandleDirection.OUTPUT),
        ),
        determinism=ActionTier.NON_DETERMINISTIC,
    )

    async def execute(
        self,
        ctx: NodeExecutionContext,
        inputs: _AgentLoopInput,
        config: BaseModel,
    ) -> NodeResult[_AgentOutput]:
        _ = ctx, config
        return success(_AgentOutput(final_text=inputs.user_input))


def _registry() -> NodeRegistry:
    reg = NodeRegistry()
    register_builtin_nodes(reg)
    reg.register(_ToolCallingAgentExecutor())
    return reg


def _defn(nodes: list[dict], edges: list[dict] | None = None) -> dict:
    return {"version": "1", "nodes": nodes, "edges": edges or []}


def _agent(node_id: str = "primary_care_agent", data: dict[str, Any] | None = None) -> dict:
    return {
        "id": node_id,
        "type": "test.agent_loop",
        "position": {"x": 0, "y": 0},
        "data": data if data is not None else {"label": "Primary care agent"},
    }


_FIVE = {
    "model": "gpt-5",
    "user_input": "Review the sealed case.",
    "system_instruction": "You are a careful reviewer.",
    "tools": ["read_case"],
    "max_iterations": 12,
}


# ---------------------------------------------------------------------------
# (a) the exact W68 shape — a node with nothing but a label
# ---------------------------------------------------------------------------


def test_the_w68_node_with_no_inputs_at_all_is_named_at_save_time():
    """The W68 node exactly as it was saved: nothing but a label.

    It is an ENTRY node, and a host- or trigger-started run may broadcast run
    ``inputs`` the definition cannot declare (``fire_from_event_watcher`` builds
    them from the changed row), so refusing the save outright would reject
    definitions that DO run — five shipped aidream workflows among them
    (``meet_intelligence_v1``, ``rag_ingestion``, ``vision_interview_v1``). The gap is therefore named as a WARNING that
    says exactly what will happen and who would have to supply the values — and
    the author tool returns warnings on a successful save, so it is never
    invisible. The provable case (a node fired by connections that do not carry
    the field) is the error below."""
    result = validate_definition(
        _defn([_agent(data={"label": "Primary care agent"})]), registry=_registry()
    )
    # Other warnings (a deprecated step type, for one) can ride on the same node; this test is
    # about the inputs gap, so pick that issue by path.
    issue = next(
        i for i in result.issues
        if i.node_id == "primary_care_agent" and i.path == "nodes[primary_care_agent].data.inputs"
    )
    assert issue.severity == "warning"
    assert "model" in issue.message and "user_input" in issue.message
    assert "missing_input" in issue.message
    assert "data.inputs" in issue.message
    assert issue.path == "nodes[primary_care_agent].data.inputs"


def test_a_step_fired_by_connections_that_carry_nothing_is_refused():
    """W71, live run 533fda6f: every desk connection authored as kind 'control'
    (which delivers an EMPTY payload) with mappings on it. The save passed and
    the agent step died on missing_input for user_input."""
    result = validate_definition(
        _defn(
            [
                {
                    "id": "src",
                    "type": "data.transform",
                    "position": {"x": 0, "y": 0},
                    "data": {"config": {"expression": "{'text': 'hi'}"}},
                },
                _agent(data={"label": "Agent"}),
            ],
            [
                {
                    "id": "e1",
                    "source": "src",
                    "target": "primary_care_agent",
                    "data": {"kind": "control", "mappings": {"user_input": "text"}},
                }
            ],
        ),
        registry=_registry(),
    )
    assert not result.valid

    inert = next(i for i in result.issues if i.edge_id == "e1")
    assert inert.severity == "error"
    assert "control" in inert.message and "mappings" in inert.message
    assert "data.kind='data'" in inert.message

    starved = next(
        i for i in result.issues if i.path == "nodes[primary_care_agent].data.inputs"
    )
    assert starved.severity == "error"
    assert "model" in starved.message and "user_input" in starved.message
    assert "control connection" in starved.message


def test_the_same_connection_as_data_is_accepted():
    result = validate_definition(
        _defn(
            [
                {
                    "id": "src",
                    "type": "data.transform",
                    "position": {"x": 0, "y": 0},
                    "data": {"config": {"expression": "{'text': 'hi', 'model': 'gpt-5'}"}},
                },
                _agent(data={"label": "Agent"}),
            ],
            [
                {
                    "id": "e1",
                    "source": "src",
                    "target": "primary_care_agent",
                    "data": {
                        "kind": "data",
                        "mappings": {"user_input": "result.text", "model": "result.model"},
                    },
                }
            ],
        ),
        registry=_registry(),
    )
    assert result.valid, [i.message for i in result.issues]


def test_a_bare_control_connection_with_no_mappings_is_still_legal():
    # Sequencing two steps is what a control connection IS for.
    result = validate_definition(
        _defn(
            [
                {
                    "id": "src",
                    "type": "data.transform",
                    "position": {"x": 0, "y": 0},
                    "data": {"config": {"expression": "{'v': 1}"}},
                },
                _agent(data={"label": "Agent", "inputs": dict(_FIVE)}),
            ],
            [
                {
                    "id": "e1",
                    "source": "src",
                    "target": "primary_care_agent",
                    "data": {"kind": "control"},
                }
            ],
        ),
        registry=_registry(),
    )
    assert result.valid, [i.message for i in result.issues]


# ---------------------------------------------------------------------------
# (b) the five keys under data.config — the message must say they are INPUTS
# ---------------------------------------------------------------------------


def test_inputs_put_under_config_are_named_as_inputs_not_just_rejected():
    result = validate_definition(
        _defn([_agent(data={"label": "Agent", "config": dict(_FIVE)})]),
        registry=_registry(),
    )
    assert not result.valid
    for key in ("model", "user_input", "system_instruction", "tools", "max_iterations"):
        issue = next(
            i for i in result.issues if i.path == f"nodes[primary_care_agent].data.config.{key}"
        )
        assert f"'{key}' is an INPUT of test.agent_loop, not config" in issue.message
        assert "data.inputs" in issue.message
        # The node type accepts NO config keys at all — say so rather than
        # printing an empty list the author has to interpret.
        assert "accepts no config keys at all" in issue.message


def test_a_genuine_config_typo_still_gets_the_plain_extra_key_message():
    # data.filter's config declares `predicate`; `predicat` is a typo, not an
    # input — the input-not-config hint must NOT fire on it.
    result = validate_definition(
        _defn(
            [
                {
                    "id": "f",
                    "type": "data.filter",
                    "position": {"x": 0, "y": 0},
                    "data": {
                        "config": {"predicate": "True", "predicat": "True"},
                        "inputs": {"items": []},
                    },
                }
            ]
        ),
        registry=_registry(),
    )
    issue = next(i for i in result.issues if i.path.endswith("data.config.predicat"))
    assert "is an INPUT of" not in issue.message


# ---------------------------------------------------------------------------
# (c) the correct node — keys under data.inputs
# ---------------------------------------------------------------------------


def test_the_same_node_with_its_inputs_under_data_inputs_is_valid():
    result = validate_definition(
        _defn([_agent(data={"label": "Agent", "inputs": dict(_FIVE)})]),
        registry=_registry(),
    )
    assert result.valid, [i.message for i in result.issues]


def test_the_studio_singular_input_key_is_accepted_too():
    result = validate_definition(
        _defn([_agent(data={"label": "Agent", "input": dict(_FIVE)})]),
        registry=_registry(),
    )
    assert result.valid, [i.message for i in result.issues]


# ---------------------------------------------------------------------------
# (d) a required input that arrives by EDGE is not a finding
# ---------------------------------------------------------------------------


def test_required_inputs_supplied_by_an_edge_mapping_are_not_flagged():
    result = validate_definition(
        _defn(
            [
                {
                    "id": "src",
                    "type": "data.transform",
                    "position": {"x": 0, "y": 0},
                    "data": {"config": {"expression": "{'model': 'gpt-5', 'q': 'hi'}"}},
                },
                _agent(data={"label": "Agent"}),
            ],
            [
                {
                    "id": "e1",
                    "source": "src",
                    "target": "primary_care_agent",
                    "data": {"mappings": {"model": "result.model", "user_input": "result.q"}},
                }
            ],
        ),
        registry=_registry(),
    )
    assert result.valid, [i.message for i in result.issues]


def test_a_broadcast_edge_silences_the_check_rather_than_guessing():
    # No mappings = the whole upstream payload lands, and its keys are only
    # known once the upstream runs. An unprovable case is never a finding.
    result = validate_definition(
        _defn(
            [
                {
                    "id": "src",
                    "type": "data.transform",
                    "position": {"x": 0, "y": 0},
                    "data": {"config": {"expression": "{'model': 'gpt-5'}"}},
                },
                _agent(data={"label": "Agent"}),
            ],
            [{"id": "e1", "source": "src", "target": "primary_care_agent", "data": {}}],
        ),
        registry=_registry(),
    )
    assert result.valid, [i.message for i in result.issues]


def test_an_edge_that_maps_only_one_of_the_two_still_names_the_other():
    result = validate_definition(
        _defn(
            [
                {
                    "id": "src",
                    "type": "data.transform",
                    "position": {"x": 0, "y": 0},
                    "data": {"config": {"expression": "{'model': 'gpt-5'}"}},
                },
                _agent(data={"label": "Agent"}),
            ],
            [
                {
                    "id": "e1",
                    "source": "src",
                    "target": "primary_care_agent",
                    "data": {"mappings": {"model": "result.model"}},
                }
            ],
        ),
        registry=_registry(),
    )
    assert not result.valid
    issue = next(i for i in result.issues if i.path.endswith("data.inputs"))
    assert "user_input" in issue.message and "model" not in issue.message.split("required input")[1]


# ---------------------------------------------------------------------------
# (e) an entry node fed from the run's INPUT SURFACE is not a false positive
# ---------------------------------------------------------------------------


def test_an_io_user_input_entry_node_is_valid_on_its_own():
    result = validate_definition(
        _defn(
            [
                {
                    "id": "ask",
                    "type": "io.user_input",
                    "position": {"x": 0, "y": 0},
                    "data": {
                        "config": {
                            "fields": [{"key": "topic", "label": "Topic", "required": True}]
                        }
                    },
                }
            ]
        ),
        registry=_registry(),
    )
    assert result.valid, [i.message for i in result.issues]


def test_an_entry_node_whose_required_input_is_on_the_input_surface_is_valid():
    # The surface's `text` lands on this entry node at run start; the field is
    # declared, so the check must stay silent.
    result = validate_definition(
        _defn(
            [
                {
                    "id": "ask",
                    "type": "io.user_input",
                    "position": {"x": 0, "y": 0},
                    "data": {
                        "config": {"fields": [{"key": "text", "label": "Text", "required": True}]}
                    },
                },
                {
                    "id": "hash",
                    "type": "crypto.hash",
                    "position": {"x": 0, "y": 0},
                    "data": {"config": {}},
                },
            ]
        ),
        registry=_registry(),
    )
    assert result.valid, [i.message for i in result.issues]


def test_a_declared_variable_reference_counts_as_a_source():
    result = validate_definition(
        {
            "version": "1",
            "variables": [{"name": "topic"}],
            "nodes": [
                _agent(
                    data={
                        "label": "Agent",
                        "inputs": {"model": "gpt-5", "user_input": {"$input": "topic"}},
                    }
                )
            ],
            "edges": [],
        },
        registry=_registry(),
    )
    assert result.valid, [i.message for i in result.issues]


# ---------------------------------------------------------------------------
# Engine-assembled inputs: named exclusions, never a silent pass
# ---------------------------------------------------------------------------


def test_a_dispatch_target_is_excluded_because_ctx_send_builds_its_inputs():
    result = validate_definition(
        _defn(
            [
                {
                    "id": "fan",
                    "type": "control.map",
                    "position": {"x": 0, "y": 0},
                    "data": {
                        "config": {"target_node_id": "primary_care_agent"},
                        "inputs": {"items": []},
                    },
                },
                _agent(data={"label": "Agent"}),
            ]
        ),
        registry=_registry(),
    )
    assert result.valid, [i.message for i in result.issues]


def test_a_mocked_node_is_excluded_because_the_scheduler_skips_its_input_gate():
    result = validate_definition(
        _defn(
            [
                _agent(
                    data={
                        "label": "Agent",
                        "mock_response": {"enabled": True, "output": {"final_text": "mocked"}},
                    }
                )
            ]
        ),
        registry=_registry(),
    )
    assert result.valid, [i.message for i in result.issues]


# ---------------------------------------------------------------------------
# THE UNRENDERED-PLACEHOLDER GATE
# ---------------------------------------------------------------------------


def test_a_placeholder_in_an_agent_input_names_the_template_step():
    result = validate_definition(
        _defn(
            [
                _agent(
                    data={
                        "label": "Agent",
                        "inputs": {
                            "model": "gpt-5",
                            "user_input": "Review case {{sealed_case_id}} now.",
                        },
                    }
                )
            ]
        ),
        registry=_registry(),
    )
    assert not result.valid
    issue = next(i for i in result.issues if "placeholder" in i.message)
    assert "{{sealed_case_id}}" in issue.message
    assert "text.template" in issue.message
    assert "$input" in issue.message
    assert issue.path == "nodes[primary_care_agent].data.inputs.user_input"


def test_a_single_brace_placeholder_is_caught_too_but_a_regex_quantifier_is_not():
    result = validate_definition(
        _defn(
            [
                _agent(
                    data={
                        "label": "Agent",
                        "inputs": {"model": "gpt-5", "user_input": "Case {case_id}"},
                    }
                ),
                {
                    "id": "re",
                    "type": "text.regex_extract",
                    "position": {"x": 0, "y": 0},
                    "data": {
                        "config": {"pattern": r"\d+"},
                        "inputs": {"text": r"zip codes look like \d{5}"},
                    },
                },
            ]
        ),
        registry=_registry(),
    )
    messages = [i.message for i in result.issues if "placeholder" in i.message]
    assert len(messages) == 1
    assert "{case_id}" in messages[0]


def test_text_template_may_carry_placeholders_in_its_input():
    result = validate_definition(
        _defn(
            [
                {
                    "id": "fill",
                    "type": "text.template",
                    "position": {"x": 0, "y": 0},
                    "data": {
                        "config": {},
                        "inputs": {
                            "template": "Review case {{sealed_case_id}}.",
                            "variables": {"sealed_case_id": "abc"},
                        },
                    },
                }
            ]
        ),
        registry=_registry(),
    )
    assert result.valid, [i.message for i in result.issues]


def test_an_input_marker_is_not_mistaken_for_a_placeholder():
    result = validate_definition(
        {
            "version": "1",
            "variables": [{"name": "sealed_case_id"}],
            "nodes": [
                _agent(
                    data={
                        "label": "Agent",
                        "inputs": {
                            "model": "gpt-5",
                            "user_input": {"$input": "sealed_case_id"},
                        },
                    }
                )
            ],
            "edges": [],
        },
        registry=_registry(),
    )
    assert result.valid, [i.message for i in result.issues]
