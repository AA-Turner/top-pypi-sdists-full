"""Tests for get_issue_types_metadata function."""

import json

from agentic_devtools.cli.config.project_config import get_issue_types_metadata


def _make_valid_entry() -> dict:
    """Return a minimal valid issue_types_metadata entry."""
    return {
        "lastDiscovered": "2026-07-12T10:00:00+00:00",
        "lastRefreshed": "2026-07-12T10:00:00+00:00",
        "provider": "jira",
        "issue_types": [],
    }


class TestGetIssueTypesMetadata:
    """Tests for get_issue_types_metadata."""

    def test_returns_none_when_key_absent(self, tmp_path):
        """Returns None when issue_types_metadata key is absent from config."""
        config_file = tmp_path / ".agdt" / "config" / "project.json"
        config_file.parent.mkdir(parents=True)
        config_file.write_text(json.dumps({"other_key": "value"}), encoding="utf-8")

        result = get_issue_types_metadata("MY_PROJECT", git_root=tmp_path)
        assert result is None

    def test_returns_none_when_project_key_absent(self, tmp_path):
        """Returns None when the given project key has no entry."""
        config_file = tmp_path / ".agdt" / "config" / "project.json"
        config_file.parent.mkdir(parents=True)
        config_file.write_text(
            json.dumps({"issue_types_metadata": {"OTHER_PROJECT": _make_valid_entry()}}),
            encoding="utf-8",
        )

        result = get_issue_types_metadata("MY_PROJECT", git_root=tmp_path)
        assert result is None

    def test_returns_none_when_project_entry_not_a_dict(self, tmp_path):
        """Returns None when the project metadata entry is not a dict."""
        config_file = tmp_path / ".agdt" / "config" / "project.json"
        config_file.parent.mkdir(parents=True)
        config_file.write_text(
            json.dumps({"issue_types_metadata": {"MY_PROJECT": ["not", "a", "dict"]}}),
            encoding="utf-8",
        )

        result = get_issue_types_metadata("MY_PROJECT", git_root=tmp_path)
        assert result is None

    def test_returns_none_when_project_entry_fails_schema_validation(self, tmp_path):
        """Returns None when the project metadata entry is a dict with invalid schema."""
        config_file = tmp_path / ".agdt" / "config" / "project.json"
        config_file.parent.mkdir(parents=True)
        config_file.write_text(
            json.dumps({"issue_types_metadata": {"MY_PROJECT": {"provider": "jira"}}}),
            encoding="utf-8",
        )

        result = get_issue_types_metadata("MY_PROJECT", git_root=tmp_path)
        assert result is None

    def test_returns_none_when_project_entry_has_wrong_field_type(self, tmp_path):
        """Returns None when a dict entry fails schema validation due to a wrong field type."""
        config_file = tmp_path / ".agdt" / "config" / "project.json"
        config_file.parent.mkdir(parents=True)
        config_file.write_text(
            json.dumps(
                {
                    "issue_types_metadata": {
                        "MY_PROJECT": {
                            "lastDiscovered": "2026-07-12T10:00:00+00:00",
                            "lastRefreshed": "2026-07-12T10:00:00+00:00",
                            "provider": 123,
                            "issue_types": [],
                        }
                    }
                }
            ),
            encoding="utf-8",
        )

        result = get_issue_types_metadata("MY_PROJECT", git_root=tmp_path)
        assert result is None

    def test_returns_entry_when_present(self, tmp_path):
        """Returns the metadata entry dict when project key exists."""
        entry = _make_valid_entry()
        config_file = tmp_path / ".agdt" / "config" / "project.json"
        config_file.parent.mkdir(parents=True)
        config_file.write_text(
            json.dumps({"issue_types_metadata": {"MY_PROJECT": entry}}),
            encoding="utf-8",
        )

        result = get_issue_types_metadata("MY_PROJECT", git_root=tmp_path)
        assert result == entry

    def test_returns_none_when_metadata_not_a_dict(self, tmp_path):
        """Returns None when issue_types_metadata is not a dict (e.g. a list)."""
        config_file = tmp_path / ".agdt" / "config" / "project.json"
        config_file.parent.mkdir(parents=True)
        config_file.write_text(
            json.dumps({"issue_types_metadata": "not_a_dict"}),
            encoding="utf-8",
        )

        result = get_issue_types_metadata("MY_PROJECT", git_root=tmp_path)
        assert result is None

    def test_returns_none_when_config_file_missing(self, tmp_path):
        """Returns None when config file does not exist."""
        result = get_issue_types_metadata("MY_PROJECT", git_root=tmp_path)
        assert result is None

    def test_timestamps_accessible_as_strings(self, tmp_path):
        """Confirms lastDiscovered and lastRefreshed are accessible as strings (FR-002)."""
        entry = _make_valid_entry()
        entry["lastDiscovered"] = "2026-07-12T10:00:00+00:00"
        entry["lastRefreshed"] = "2026-07-13T14:30:00+00:00"
        config_file = tmp_path / ".agdt" / "config" / "project.json"
        config_file.parent.mkdir(parents=True)
        config_file.write_text(
            json.dumps({"issue_types_metadata": {"PROJ": entry}}),
            encoding="utf-8",
        )

        result = get_issue_types_metadata("PROJ", git_root=tmp_path)
        assert result is not None
        assert result["lastDiscovered"] == "2026-07-12T10:00:00+00:00"
        assert result["lastRefreshed"] == "2026-07-13T14:30:00+00:00"
