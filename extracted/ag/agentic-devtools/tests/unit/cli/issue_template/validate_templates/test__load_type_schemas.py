"""Tests for _load_type_schemas()."""

from __future__ import annotations

import json
from pathlib import Path

from agentic_devtools.cli.issue_template.validate_templates import _load_type_schemas


def _write_project_json(tmp_path: Path, payload: object) -> None:
    config_dir = tmp_path / ".agdt" / "config"
    config_dir.mkdir(parents=True, exist_ok=True)
    (config_dir / "project.json").write_text(json.dumps(payload), encoding="utf-8")


class TestLoadTypeSchemas:
    """Tests for loading cached issue-type schemas from project.json."""

    def test_no_config_returns_none(self, tmp_path: Path) -> None:
        """Missing issue_types_metadata yields None."""
        assert _load_type_schemas(tmp_path) is None

    def test_metadata_not_dict_returns_none(self, tmp_path: Path) -> None:
        """Non-dict issue_types_metadata yields None."""
        _write_project_json(tmp_path, {"issue_types_metadata": "nope"})
        assert _load_type_schemas(tmp_path) is None

    def test_non_dict_entries_and_bad_shapes_skipped(self, tmp_path: Path) -> None:
        """Malformed project/type/name shapes are skipped without error."""
        _write_project_json(
            tmp_path,
            {
                "issue_types_metadata": {
                    "BADPROJ": "not-a-dict",
                    "NOTYPES": {"issue_types": "not-a-list"},
                    "MIXED": {
                        "issue_types": [
                            "not-a-dict",
                            {"name": "  "},
                            {"name": 123},
                            {
                                "name": "Bug",
                                "properties": [
                                    {"name": "severity", "required": True},
                                    {"name": "notes", "required": False},
                                ],
                            },
                        ]
                    },
                }
            },
        )
        schemas = _load_type_schemas(tmp_path)
        assert schemas is not None
        assert schemas["bug"] == ({"severity", "notes"}, {"severity"})

    def test_union_across_projects(self, tmp_path: Path) -> None:
        """The same slug across projects is unioned."""
        _write_project_json(
            tmp_path,
            {
                "issue_types_metadata": {
                    "P1": {"issue_types": [{"name": "Bug", "properties": [{"name": "a", "required": True}]}]},
                    "P2": {"issue_types": [{"name": "Bug", "properties": [{"name": "b", "required": False}]}]},
                }
            },
        )
        schemas = _load_type_schemas(tmp_path)
        assert schemas is not None
        assert schemas["bug"] == ({"a", "b"}, {"a"})
