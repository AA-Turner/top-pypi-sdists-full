"""Tests for load_event_edge_mapping() — JSON paths and error branches."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from agentic_devtools.orchestration.execution.event_edge_mapping import (
    EventEdgeMappingError,
    load_event_edge_mapping,
)


class TestLoadEventEdgeMappingJson:
    """Tests for JSON loading paths in load_event_edge_mapping()."""

    def test_load_valid_json(self, tmp_path: Path) -> None:
        """Loads a valid JSON mapping file."""
        data = {
            "rules": [
                {
                    "event_name": "DONE",
                    "source_node": "node_a",
                    "target_node": "node_b",
                    "agdt_step_name": "step-b",
                }
            ]
        }
        path = tmp_path / "mapping.json"
        path.write_text(json.dumps(data))

        config = load_event_edge_mapping(path)
        assert len(config.rules) == 1
        assert config.rules[0].event_name == "DONE"

    def test_malformed_json_raises(self, tmp_path: Path) -> None:
        """Malformed JSON raises EventEdgeMappingError."""
        path = tmp_path / "bad.json"
        path.write_text("{not valid")

        with pytest.raises(EventEdgeMappingError, match="Failed to parse JSON"):
            load_event_edge_mapping(path)

    def test_rules_not_list_raises(self, tmp_path: Path) -> None:
        """Non-list 'rules' raises EventEdgeMappingError."""
        path = tmp_path / "bad_rules.json"
        path.write_text(json.dumps({"rules": "not_a_list"}))

        with pytest.raises(EventEdgeMappingError, match="'rules' must be a list"):
            load_event_edge_mapping(path)

    def test_rule_not_dict_raises(self, tmp_path: Path) -> None:
        """Non-dict rule entry raises EventEdgeMappingError."""
        path = tmp_path / "bad_rule.json"
        path.write_text(json.dumps({"rules": ["not_a_dict"]}))

        with pytest.raises(EventEdgeMappingError, match="Rule at index 0 must be a dict"):
            load_event_edge_mapping(path)

    def test_rule_missing_field_raises(self, tmp_path: Path) -> None:
        """Missing required field raises EventEdgeMappingError."""
        path = tmp_path / "missing_field.json"
        path.write_text(json.dumps({"rules": [{"event_name": "X", "source_node": "a_node"}]}))

        with pytest.raises(EventEdgeMappingError, match="missing field"):
            load_event_edge_mapping(path)
