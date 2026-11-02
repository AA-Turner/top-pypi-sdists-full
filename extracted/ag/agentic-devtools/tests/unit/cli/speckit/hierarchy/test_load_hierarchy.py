"""Tests for load_hierarchy function."""

from datetime import UTC
from unittest.mock import patch

import pytest
import yaml

from agentic_devtools.cli.speckit.hierarchy import (
    HierarchyLevel,
    HierarchyValidationError,
    load_hierarchy,
)


def _write_yaml(path, data):
    """Helper to write a YAML file."""
    path.write_text(
        yaml.safe_dump(data, default_flow_style=False, sort_keys=False),
        encoding="utf-8",
    )


def _valid_data(**overrides):
    """Return a valid hierarchy dict with optional overrides."""
    base = {
        "title": "Test Feature",
        "level": "feature",
        "parent": "42",
        "children": [
            {"key": "100", "title": "Child One", "order": 1},
            {"key": "101", "title": "Child Two", "order": 2},
        ],
        "processed_at": "2024-06-15T10:30:00+00:00",
    }
    base.update(overrides)
    return base


class TestLoadHierarchy:
    """Tests for load_hierarchy function."""

    def test_loads_valid_feature(self, tmp_path):
        """Test loading a valid feature hierarchy file."""
        path = tmp_path / "hierarchy.yml"
        _write_yaml(path, _valid_data())

        node = load_hierarchy(path)

        assert node.title == "Test Feature"
        assert node.level is HierarchyLevel.FEATURE
        assert node.parent == "42"
        assert len(node.children) == 2

    def test_loads_epic_with_null_parent(self, tmp_path):
        """Test loading an epic with parent: null."""
        path = tmp_path / "hierarchy.yml"
        _write_yaml(path, _valid_data(level="epic", parent=None))

        node = load_hierarchy(path)

        assert node.level is HierarchyLevel.EPIC
        assert node.parent is None

    def test_loads_task_level(self, tmp_path):
        """Test loading a task level."""
        path = tmp_path / "hierarchy.yml"
        _write_yaml(path, _valid_data(level="task"))

        node = load_hierarchy(path)
        assert node.level is HierarchyLevel.TASK

    def test_children_order_preserved(self, tmp_path):
        """Test that children ordering is preserved."""
        children = [
            {"key": "3", "title": "Third", "order": 3},
            {"key": "1", "title": "First", "order": 1},
            {"key": "2", "title": "Second", "order": 2},
        ]
        path = tmp_path / "hierarchy.yml"
        _write_yaml(path, _valid_data(children=children))

        node = load_hierarchy(path)

        assert [c.key for c in node.children] == ["3", "1", "2"]
        assert [c.order for c in node.children] == [3, 1, 2]

    def test_integer_parent_normalized_to_string(self, tmp_path):
        """Test that integer parent is normalized to string."""
        path = tmp_path / "hierarchy.yml"
        _write_yaml(path, _valid_data(parent=99))

        node = load_hierarchy(path)
        assert node.parent == "99"

    def test_integer_child_key_normalized_to_string(self, tmp_path):
        """Test that integer child key is normalized to string."""
        path = tmp_path / "hierarchy.yml"
        _write_yaml(path, _valid_data(children=[{"key": 55, "title": "X", "order": 0}]))

        node = load_hierarchy(path)
        assert node.children[0].key == "55"

    def test_processed_at_parsed_as_datetime(self, tmp_path):
        """Test that processed_at is parsed into datetime."""
        from datetime import datetime

        path = tmp_path / "hierarchy.yml"
        _write_yaml(path, _valid_data(processed_at="2024-01-15T08:00:00+00:00"))

        node = load_hierarchy(path)
        assert node.processed_at == datetime(2024, 1, 15, 8, 0, 0, tzinfo=UTC)

    def test_processed_at_z_suffix(self, tmp_path):
        """Test that 'Z' suffix timestamps are handled."""
        from datetime import datetime

        path = tmp_path / "hierarchy.yml"
        data = _valid_data()
        # Write manually to include Z suffix
        data["processed_at"] = "2024-06-01T12:00:00Z"
        path.write_text(
            yaml.safe_dump(data, default_flow_style=False, sort_keys=False),
            encoding="utf-8",
        )

        node = load_hierarchy(path)
        assert node.processed_at == datetime(2024, 6, 1, 12, 0, 0, tzinfo=UTC)

    def test_processed_at_naive_normalized_to_utc(self, tmp_path):
        """Test that naive timestamps are assumed UTC."""
        from datetime import datetime

        path = tmp_path / "hierarchy.yml"
        data = _valid_data()
        data["processed_at"] = "2024-03-20T15:45:00"
        path.write_text(
            yaml.safe_dump(data, default_flow_style=False, sort_keys=False),
            encoding="utf-8",
        )

        node = load_hierarchy(path)
        assert node.processed_at == datetime(2024, 3, 20, 15, 45, 0, tzinfo=UTC)

    def test_processed_at_null(self, tmp_path):
        """Test that null processed_at is None."""
        path = tmp_path / "hierarchy.yml"
        _write_yaml(path, _valid_data(processed_at=None))

        node = load_hierarchy(path)
        assert node.processed_at is None

    def test_empty_children_list(self, tmp_path):
        """Test that empty children list is loaded correctly."""
        path = tmp_path / "hierarchy.yml"
        _write_yaml(path, _valid_data(children=[]))

        node = load_hierarchy(path)
        assert node.children == []

    def test_file_not_found_raises_error(self, tmp_path):
        """Test that non-existent path raises FileNotFoundError."""
        path = tmp_path / "nonexistent.yml"
        with pytest.raises(FileNotFoundError, match="nonexistent.yml"):
            load_hierarchy(path)

    def test_empty_file_raises_validation_error(self, tmp_path):
        """Test that empty file raises HierarchyValidationError."""
        path = tmp_path / "hierarchy.yml"
        path.write_text("", encoding="utf-8")

        with pytest.raises(HierarchyValidationError, match="empty"):
            load_hierarchy(path)

    def test_non_mapping_yaml_raises_validation_error(self, tmp_path):
        """Test that non-mapping YAML raises HierarchyValidationError."""
        path = tmp_path / "hierarchy.yml"
        path.write_text("- item1\n- item2\n", encoding="utf-8")

        with pytest.raises(HierarchyValidationError, match="mapping"):
            load_hierarchy(path)

    def test_missing_level_raises_validation_error(self, tmp_path):
        """Test that missing level field raises validation error."""
        path = tmp_path / "hierarchy.yml"
        data = _valid_data()
        del data["level"]
        _write_yaml(path, data)

        with pytest.raises(HierarchyValidationError) as exc_info:
            load_hierarchy(path)

        assert exc_info.value.field_name == "level"

    def test_invalid_level_raises_validation_error(self, tmp_path):
        """Test that invalid level raises validation error."""
        path = tmp_path / "hierarchy.yml"
        # Write raw YAML to bypass safe_dump treating "milestone" as normal string
        path.write_text("title: Test\nlevel: milestone\nchildren: []\n", encoding="utf-8")

        with pytest.raises(HierarchyValidationError, match="level"):
            load_hierarchy(path)

    def test_non_list_children_raises_validation_error(self, tmp_path):
        """Test that non-list children raises validation error."""
        path = tmp_path / "hierarchy.yml"
        path.write_text("title: Test\nlevel: epic\nchildren: not_a_list\n", encoding="utf-8")

        with pytest.raises(HierarchyValidationError):
            load_hierarchy(path)

    def test_child_missing_key_raises_validation_error(self, tmp_path):
        """Test that child entry missing key raises validation error."""
        path = tmp_path / "hierarchy.yml"
        path.write_text(
            "title: Test\nlevel: epic\nchildren:\n  - title: X\n    order: 1\n",
            encoding="utf-8",
        )

        with pytest.raises(HierarchyValidationError) as exc_info:
            load_hierarchy(path)

        assert exc_info.value.field_name == "children.0.key"

    def test_invalid_timestamp_raises_validation_error(self, tmp_path):
        """Test that invalid timestamp raises validation error."""
        path = tmp_path / "hierarchy.yml"
        path.write_text(
            "title: Test\nlevel: epic\nchildren: []\nprocessed_at: not-a-date\n",
            encoding="utf-8",
        )

        with pytest.raises(HierarchyValidationError):
            load_hierarchy(path)

    def test_invalid_timestamp_passes_schema_but_fails_parse(self, tmp_path):
        """Test timestamp that matches regex but is not a valid date."""
        path = tmp_path / "hierarchy.yml"
        # This matches the schema regex pattern but is not a valid date
        path.write_text(
            "title: Test\nlevel: epic\nchildren: []\nprocessed_at: '2024-99-99T99:99:99+00:00'\n",
            encoding="utf-8",
        )

        with pytest.raises(HierarchyValidationError, match="processed_at"):
            load_hierarchy(path)

    def test_omitted_optional_fields_default_to_none(self, tmp_path):
        """Test that omitted optional fields are treated as None."""
        path = tmp_path / "hierarchy.yml"
        path.write_text("title: Minimal\nlevel: task\nchildren: []\n", encoding="utf-8")

        node = load_hierarchy(path)
        assert node.parent is None
        assert node.processed_at is None

    def test_loads_valid_file_without_jsonschema(self, tmp_path):
        """Test that load_hierarchy works when jsonschema is not installed."""
        path = tmp_path / "hierarchy.yml"
        _write_yaml(path, _valid_data())

        with patch("agentic_devtools.cli.speckit.hierarchy.jsonschema", None):
            node = load_hierarchy(path)

        assert node.title == "Test Feature"
        assert node.level == HierarchyLevel.FEATURE

    def test_missing_required_field_without_jsonschema_raises_validation_error(self, tmp_path):
        """Test required fields are still enforced when jsonschema is unavailable."""
        path = tmp_path / "hierarchy.yml"
        data = _valid_data()
        del data["children"]
        _write_yaml(path, data)

        with patch("agentic_devtools.cli.speckit.hierarchy.jsonschema", None):
            with pytest.raises(HierarchyValidationError) as exc_info:
                load_hierarchy(path)

        assert exc_info.value.field_name == "children"

    def test_missing_child_required_field_without_jsonschema_raises_validation_error(self, tmp_path):
        """Test nested child required fields are enforced without jsonschema."""
        path = tmp_path / "hierarchy.yml"
        _write_yaml(path, _valid_data(children=[{"title": "Child", "order": 1}]))

        with patch("agentic_devtools.cli.speckit.hierarchy.jsonschema", None):
            with pytest.raises(HierarchyValidationError) as exc_info:
                load_hierarchy(path)

        assert exc_info.value.field_name == "children.0.key"

    def test_non_mapping_child_without_jsonschema_raises_validation_error(self, tmp_path):
        """Test malformed child entries raise HierarchyValidationError without jsonschema."""
        path = tmp_path / "hierarchy.yml"
        _write_yaml(path, _valid_data(children=["invalid-child"]))

        with patch("agentic_devtools.cli.speckit.hierarchy.jsonschema", None):
            with pytest.raises(HierarchyValidationError) as exc_info:
                load_hierarchy(path)

        assert exc_info.value.field_name == "children.0"

    def test_invalid_parent_type_without_jsonschema_raises_validation_error(self, tmp_path):
        """Test parent type validation without jsonschema."""
        path = tmp_path / "hierarchy.yml"
        _write_yaml(path, _valid_data(parent=True))

        with patch("agentic_devtools.cli.speckit.hierarchy.jsonschema", None):
            with pytest.raises(HierarchyValidationError) as exc_info:
                load_hierarchy(path)

        assert exc_info.value.field_name == "parent"

    def test_non_list_children_without_jsonschema_raises_validation_error(self, tmp_path):
        """Test children array validation without jsonschema."""
        path = tmp_path / "hierarchy.yml"
        _write_yaml(path, _valid_data(children="invalid"))

        with patch("agentic_devtools.cli.speckit.hierarchy.jsonschema", None):
            with pytest.raises(HierarchyValidationError) as exc_info:
                load_hierarchy(path)

        assert exc_info.value.field_name == "children"

    def test_invalid_child_key_type_without_jsonschema_raises_validation_error(self, tmp_path):
        """Test child key type validation without jsonschema."""
        path = tmp_path / "hierarchy.yml"
        _write_yaml(path, _valid_data(children=[{"key": True, "title": "Child", "order": 1}]))

        with patch("agentic_devtools.cli.speckit.hierarchy.jsonschema", None):
            with pytest.raises(HierarchyValidationError) as exc_info:
                load_hierarchy(path)

        assert exc_info.value.field_name == "children.0.key"

    def test_empty_child_title_without_jsonschema_raises_validation_error(self, tmp_path):
        """Test child title validation without jsonschema."""
        path = tmp_path / "hierarchy.yml"
        _write_yaml(path, _valid_data(children=[{"key": "100", "title": "", "order": 1}]))

        with patch("agentic_devtools.cli.speckit.hierarchy.jsonschema", None):
            with pytest.raises(HierarchyValidationError) as exc_info:
                load_hierarchy(path)

        assert exc_info.value.field_name == "children.0.title"

    def test_invalid_child_order_without_jsonschema_raises_validation_error(self, tmp_path):
        """Test child order validation without jsonschema."""
        path = tmp_path / "hierarchy.yml"
        _write_yaml(path, _valid_data(children=[{"key": "100", "title": "Child", "order": True}]))

        with patch("agentic_devtools.cli.speckit.hierarchy.jsonschema", None):
            with pytest.raises(HierarchyValidationError) as exc_info:
                load_hierarchy(path)

        assert exc_info.value.field_name == "children.0.order"

    def test_empty_title_without_jsonschema_raises_validation_error(self, tmp_path):
        """Test top-level title validation without jsonschema."""
        path = tmp_path / "hierarchy.yml"
        _write_yaml(path, _valid_data(title=""))

        with patch("agentic_devtools.cli.speckit.hierarchy.jsonschema", None):
            with pytest.raises(HierarchyValidationError) as exc_info:
                load_hierarchy(path)

        assert exc_info.value.field_name == "title"

    def test_null_level_without_jsonschema_raises_validation_error(self, tmp_path):
        """Test non-string levels still raise HierarchyValidationError without jsonschema."""
        path = tmp_path / "hierarchy.yml"
        _write_yaml(path, _valid_data(level=None))

        with patch("agentic_devtools.cli.speckit.hierarchy.jsonschema", None):
            with pytest.raises(HierarchyValidationError) as exc_info:
                load_hierarchy(path)

        assert exc_info.value.field_name == "level"

    def test_malformed_yaml_raises_validation_error(self, tmp_path):
        """Test that malformed YAML raises HierarchyValidationError instead of yaml.YAMLError."""
        path = tmp_path / "hierarchy.yml"
        path.write_text("key: [invalid: yaml: {\n", encoding="utf-8")

        with pytest.raises(HierarchyValidationError) as exc_info:
            load_hierarchy(path)

        assert exc_info.value.field_name == "file"
        assert "YAML parse error" in exc_info.value.detail
        assert "\n" not in exc_info.value.detail

    def test_pyyaml_auto_parsed_datetime_processed_at(self, tmp_path):
        """Test that an unquoted ISO-8601 timestamp (parsed as datetime by PyYAML) is accepted."""
        from datetime import datetime

        path = tmp_path / "hierarchy.yml"
        # Write an unquoted timestamp — PyYAML auto-parses this to a datetime object.
        path.write_text(
            "title: Test\nlevel: epic\nchildren: []\nprocessed_at: 2024-06-01T12:00:00Z\n",
            encoding="utf-8",
        )

        node = load_hierarchy(path)
        assert node.processed_at == datetime(2024, 6, 1, 12, 0, 0, tzinfo=UTC)

    def test_required_validation_without_missing_key_falls_back_to_validator(self, tmp_path):
        """Test required-validation fallback when no specific missing key can be derived."""
        jsonschema = pytest.importorskip("jsonschema")
        path = tmp_path / "hierarchy.yml"
        _write_yaml(path, _valid_data())
        exc = jsonschema.ValidationError(
            "'title' is a required property",
            validator="required",
            validator_value=["title"],
            instance={"title": "Test Feature"},
            schema={"required": ["title"]},
        )

        with patch(
            "agentic_devtools.cli.speckit.hierarchy.jsonschema.validate",
            side_effect=exc,
        ):
            with pytest.raises(HierarchyValidationError) as exc_info:
                load_hierarchy(path)

        assert exc_info.value.field_name == "required"

    def test_additional_properties_error_uses_nested_field_path(self, tmp_path):
        """Test additionalProperties validation maps to the unexpected nested key."""
        jsonschema = pytest.importorskip("jsonschema")
        path = tmp_path / "hierarchy.yml"
        _write_yaml(path, _valid_data())
        exc = jsonschema.ValidationError(
            "Additional properties are not allowed ('extra' was unexpected)",
            validator="additionalProperties",
            instance={"key": "100", "title": "Child", "order": 1, "extra": "value"},
            schema={
                "type": "object",
                "properties": {
                    "key": {"type": "string"},
                    "title": {"type": "string"},
                    "order": {"type": "integer"},
                },
                "additionalProperties": False,
            },
            path=["children", 0],
        )

        with patch(
            "agentic_devtools.cli.speckit.hierarchy.jsonschema.validate",
            side_effect=exc,
        ):
            with pytest.raises(HierarchyValidationError) as exc_info:
                load_hierarchy(path)

        assert exc_info.value.field_name == "children.0.extra"

    def test_additional_properties_error_uses_params_when_available(self, tmp_path):
        """Test additionalProperties extraction prefers params.additionalProperties."""
        jsonschema = pytest.importorskip("jsonschema")
        path = tmp_path / "hierarchy.yml"
        _write_yaml(path, _valid_data())
        exc = jsonschema.ValidationError(
            "Additional properties are not allowed ('instance-extra' was unexpected)",
            validator="additionalProperties",
            instance={"key": "100", "title": "Child", "order": 1, "instance-extra": "value"},
            schema={
                "type": "object",
                "properties": {
                    "key": {"type": "string"},
                    "title": {"type": "string"},
                    "order": {"type": "integer"},
                },
                "additionalProperties": False,
            },
            path=["children", 0],
        )
        exc.params = {"additionalProperties": "params-extra"}  # type: ignore[attr-defined]

        with patch(
            "agentic_devtools.cli.speckit.hierarchy.jsonschema.validate",
            side_effect=exc,
        ):
            with pytest.raises(HierarchyValidationError) as exc_info:
                load_hierarchy(path)

        assert exc_info.value.field_name == "children.0.params-extra"

    def test_additional_properties_error_uses_message_fallback(self, tmp_path):
        """Test additionalProperties extraction falls back to message parsing."""
        jsonschema = pytest.importorskip("jsonschema")
        path = tmp_path / "hierarchy.yml"
        _write_yaml(path, _valid_data())
        exc = jsonschema.ValidationError(
            "Additional properties are not allowed ('message-extra' was unexpected)",
            validator="additionalProperties",
            instance="not-a-dict",
            schema="not-a-dict",
            path=["children", 0],
        )
        exc.params = None  # type: ignore[attr-defined]

        with patch(
            "agentic_devtools.cli.speckit.hierarchy.jsonschema.validate",
            side_effect=exc,
        ):
            with pytest.raises(HierarchyValidationError) as exc_info:
                load_hierarchy(path)

        assert exc_info.value.field_name == "children.0.message-extra"

    def test_directory_path_raises_validation_error(self, tmp_path):
        """Test that passing a directory path raises HierarchyValidationError."""
        directory = tmp_path / "hierarchy-dir"
        directory.mkdir()

        with pytest.raises(HierarchyValidationError) as exc_info:
            load_hierarchy(directory)

        assert exc_info.value.field_name == "file"
        assert "Expected a file path" in exc_info.value.detail

    def test_oserror_on_stat_raises_validation_error(self, tmp_path):
        """Test that an OSError from stat() (e.g. PermissionError on unreadable directory)
        is wrapped in HierarchyValidationError instead of raising FileNotFoundError."""
        path = tmp_path / "hierarchy.yml"
        _write_yaml(path, _valid_data())

        with patch.object(
            type(path),
            "stat",
            side_effect=PermissionError("Permission denied"),
        ):
            with pytest.raises(HierarchyValidationError) as exc_info:
                load_hierarchy(path)

        assert exc_info.value.field_name == "file"
        assert "Unable to read file" in exc_info.value.detail
        assert isinstance(exc_info.value.__cause__, PermissionError)

    def test_oserror_while_reading_raises_validation_error(self, tmp_path):
        """Test read failures are wrapped in HierarchyValidationError."""
        path = tmp_path / "hierarchy.yml"
        _write_yaml(path, _valid_data())

        with patch.object(
            type(path),
            "read_text",
            side_effect=PermissionError("Permission denied"),
        ):
            with pytest.raises(HierarchyValidationError) as exc_info:
                load_hierarchy(path)

        assert exc_info.value.field_name == "file"
        assert "Unable to read file" in exc_info.value.detail
        assert isinstance(exc_info.value.__cause__, PermissionError)

    def test_raced_file_disappearance_reraises_filenotfounderror(self, tmp_path):
        """Test read-time FileNotFoundError preserves the documented contract."""
        path = tmp_path / "hierarchy.yml"
        _write_yaml(path, _valid_data())

        with patch.object(type(path), "read_text", side_effect=FileNotFoundError("gone")):
            with pytest.raises(FileNotFoundError, match="gone"):
                load_hierarchy(path)

    def test_non_utf8_file_raises_validation_error(self, tmp_path):
        """Test invalid UTF-8 content is wrapped in HierarchyValidationError."""
        path = tmp_path / "hierarchy.yml"
        _write_yaml(path, _valid_data())

        decode_error = UnicodeDecodeError("utf-8", b"\x80", 0, 1, "invalid start byte")
        with patch.object(type(path), "read_text", side_effect=decode_error):
            with pytest.raises(HierarchyValidationError) as exc_info:
                load_hierarchy(path)

        assert exc_info.value.field_name == "file"
        assert exc_info.value.detail == "File is not valid UTF-8"
        assert isinstance(exc_info.value.__cause__, UnicodeDecodeError)

    def test_additional_properties_error_with_none_params_key_falls_back_to_path(self, tmp_path):
        """Test additionalProperties uses path fallback when params key resolves to None."""
        jsonschema = pytest.importorskip("jsonschema")
        path = tmp_path / "hierarchy.yml"
        _write_yaml(path, _valid_data())
        exc = jsonschema.ValidationError(
            "Additional properties validation failed",
            validator="additionalProperties",
            instance={"key": "100"},
            schema={"type": "object", "properties": {"key": {"type": "string"}}},
            path=["children", 0],
        )
        exc.params = {"additionalProperties": None}  # type: ignore[attr-defined]

        with patch(
            "agentic_devtools.cli.speckit.hierarchy.jsonschema.validate",
            side_effect=exc,
        ):
            with pytest.raises(HierarchyValidationError) as exc_info:
                load_hierarchy(path)

        assert exc_info.value.field_name == "children.0"

    def test_additional_properties_error_with_non_mapping_properties_uses_message_fallback(self, tmp_path):
        """Test additionalProperties falls back to message when schema properties are non-mapping."""
        jsonschema = pytest.importorskip("jsonschema")
        path = tmp_path / "hierarchy.yml"
        _write_yaml(path, _valid_data())
        exc = jsonschema.ValidationError(
            "Additional properties are not allowed ('message-extra' was unexpected)",
            validator="additionalProperties",
            instance={"key": "100"},
            schema={"properties": ["key"]},
            path=["children", 0],
        )
        exc.params = {"additionalProperties": None}  # type: ignore[attr-defined]

        with patch(
            "agentic_devtools.cli.speckit.hierarchy.jsonschema.validate",
            side_effect=exc,
        ):
            with pytest.raises(HierarchyValidationError) as exc_info:
                load_hierarchy(path)

        assert exc_info.value.field_name == "children.0.message-extra"

    def test_unexpected_top_level_key_without_jsonschema_raises_validation_error(self, tmp_path):
        """Test that unexpected top-level keys are rejected in fallback validation."""
        path = tmp_path / "hierarchy.yml"
        data = _valid_data()
        data["unexpected_key"] = "some value"
        _write_yaml(path, data)

        with patch("agentic_devtools.cli.speckit.hierarchy.jsonschema", None):
            with pytest.raises(HierarchyValidationError) as exc_info:
                load_hierarchy(path)

        assert exc_info.value.field_name == "unexpected_key"
        assert "Additional properties are not allowed" in exc_info.value.detail
        assert "unexpected_key" in exc_info.value.detail

    def test_unexpected_child_key_without_jsonschema_raises_validation_error(self, tmp_path):
        """Test that unexpected child keys are rejected in fallback validation."""
        path = tmp_path / "hierarchy.yml"
        data = _valid_data(children=[{"key": "100", "title": "Child One", "order": 1, "unexpected": "value"}])
        _write_yaml(path, data)

        with patch("agentic_devtools.cli.speckit.hierarchy.jsonschema", None):
            with pytest.raises(HierarchyValidationError) as exc_info:
                load_hierarchy(path)

        assert exc_info.value.field_name == "children.0.unexpected"
        assert "Additional properties are not allowed" in exc_info.value.detail
        assert "unexpected" in exc_info.value.detail
