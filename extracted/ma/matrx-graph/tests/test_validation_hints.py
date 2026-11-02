"""Did-you-mean hints on the "Unknown node type" validation issue.

Guards the contract that a typo'd node type in a Definition comes back with a
``Did you mean …?`` suggestion plus a bounded, closest-first list of the
registry's registered spec types (via ``matrx_utils.suggest``), so a builder —
human or agent — can self-correct without a registry dump.
"""

from __future__ import annotations

import logging

import pytest

from matrx_graph import Definition, NodeRegistry, compile_graph, register_builtin_nodes
from matrx_graph.errors import CompilationError
from matrx_graph.nodes.control.branch import BranchExecutor
from matrx_graph.nodes.data.transform import TransformExecutor
from matrx_graph.validation import validate_definition


def _definition_with_type(node_type: str) -> dict:
    return {
        "version": "1",
        "nodes": [
            {
                "id": "n1",
                "type": node_type,
                "position": {"x": 0, "y": 0},
                "data": {"config": {}},
            }
        ],
        "edges": [],
    }


def _registry() -> NodeRegistry:
    reg = NodeRegistry()
    reg.register(BranchExecutor())
    reg.register(TransformExecutor())
    return reg


def test_unknown_node_type_gets_did_you_mean_and_closest_first_list():
    result = validate_definition(_definition_with_type("data.transfrom"), registry=_registry())
    assert not result.valid
    issue = next(i for i in result.issues if "Unknown node type" in i.message)
    assert issue.node_id == "n1"
    assert "Did you mean node type 'data.transform'?" in issue.message
    assert "Registered types (closest first):" in issue.message
    # Closest-first: the near-miss must lead the list, ahead of control.branch.
    listing = issue.message.split("Registered types (closest first):", 1)[1]
    assert listing.index("data.transform") < listing.index("control.branch")


def test_unknown_node_type_far_miss_still_lists_registered_types():
    result = validate_definition(_definition_with_type("zzz.zzz"), registry=_registry())
    assert not result.valid
    issue = next(i for i in result.issues if "Unknown node type" in i.message)
    assert "Did you mean" not in issue.message
    assert "Registered types (closest first):" in issue.message
    assert "data.transform" in issue.message and "control.branch" in issue.message


def test_known_node_type_produces_no_unknown_type_issue():
    result = validate_definition(_definition_with_type("data.transform"), registry=_registry())
    assert not any("Unknown node type" in i.message for i in result.issues)


def test_invalid_config_emits_one_safe_structured_warning(caplog):
    """Expected draft errors are one warning, never five ERROR payload dumps."""
    raw_config = {"untrusted_config_value": "do-not-log"}
    node_data = {"config": raw_config, "secret": "do-not-log"}
    registry = NodeRegistry()
    register_builtin_nodes(registry)
    definition = {
        "version": "1",
        "nodes": [
            {
                "id": "regex-node",
                "type": "text.regex_extract",
                "position": {"x": 0, "y": 0},
                "data": node_data,
            }
        ],
        "edges": [],
    }
    with caplog.at_level(logging.WARNING, logger="matrx_graph.diagnostics.compile_validation"):
        result = validate_definition(definition, registry=registry)
    assert any(
        issue.path == "nodes[regex-node].data.config.pattern" and issue.message == "Field required"
        for issue in result.issues
    )

    records = [
        record
        for record in caplog.records
        if record.name == "matrx_graph.diagnostics.compile_validation"
    ]
    assert len(records) == 1
    record = records[0]
    assert record.levelno == logging.WARNING
    assert record.getMessage() == "workflow_config_invalid"
    assert record.event == "workflow_config_invalid"
    assert record.node_id == "regex-node"
    assert record.spec_type == "text.regex_extract"
    assert record.field_errors == [
        {"field": "pattern", "error_type": "missing"},
        {"field": "untrusted_config_value", "error_type": "extra_forbidden"},
    ]
    assert "do-not-log" not in str(record.__dict__)


def test_compile_invalid_draft_emits_only_the_safe_validation_warning(caplog):
    """Compile preserves issues but must not add raw snapshots or ERROR fan-out."""
    sentinel = "COMPILE_SNAPSHOT_SENTINEL"
    registry = NodeRegistry()
    register_builtin_nodes(registry)
    definition = Definition.model_validate(
        {
            "version": "1",
            "nodes": [
                {
                    "id": "regex-node",
                    "type": "text.regex_extract",
                    "position": {"x": 0, "y": 0},
                    "data": {"config": {"untrusted_config_value": sentinel}, "secret": sentinel},
                }
            ],
            "edges": [],
        }
    )

    with caplog.at_level(logging.WARNING, logger="matrx_graph"):
        with pytest.raises(CompilationError) as raised:
            compile_graph(definition, registry=registry)

    issues = raised.value.issues
    assert any(
        issue.path == "nodes[regex-node].data.config.pattern" and issue.message == "Field required"
        for issue in issues
    )
    records = [record for record in caplog.records if record.name.startswith("matrx_graph")]
    assert len(records) == 1
    record = records[0]
    assert record.name == "matrx_graph.diagnostics.compile_validation"
    assert record.levelno == logging.WARNING
    assert record.getMessage() == "workflow_config_invalid"
    assert record.field_errors == [
        {"field": "pattern", "error_type": "missing"},
        {"field": "untrusted_config_value", "error_type": "extra_forbidden"},
    ]
    assert sentinel not in str(record.__dict__)
    assert sentinel not in str(raised.value)
