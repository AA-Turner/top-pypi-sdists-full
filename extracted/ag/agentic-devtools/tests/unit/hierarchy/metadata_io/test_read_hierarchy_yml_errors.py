"""Tests for error parsing paths in read_hierarchy_yml."""

from __future__ import annotations

from pathlib import Path

import pytest


@pytest.fixture
def tmp_yml(tmp_path: Path):
    """Helper to write a hierarchy.yml and return its path."""

    def _write(content: str) -> Path:
        p = tmp_path / "hierarchy.yml"
        p.write_text(content)
        return p

    return _write


class TestReadHierarchyYmlErrors:
    """Cover error branches in read_hierarchy_yml."""

    def test_invalid_parent_non_numeric(self, tmp_yml):
        from agentic_devtools.hierarchy.metadata_io import read_hierarchy_yml

        path = tmp_yml("level: epic\nparent: not-a-number\n")
        with pytest.raises(ValueError, match="Invalid 'parent' value"):
            read_hierarchy_yml(path)

    def test_children_not_list(self, tmp_yml):
        from agentic_devtools.hierarchy.metadata_io import read_hierarchy_yml

        path = tmp_yml("level: epic\nchildren: not-a-list\n")
        with pytest.raises(ValueError, match="'children' must be a list"):
            read_hierarchy_yml(path)

    def test_child_entry_not_dict(self, tmp_yml):
        from agentic_devtools.hierarchy.metadata_io import read_hierarchy_yml

        path = tmp_yml("level: epic\nchildren:\n  - just-a-string\n")
        with pytest.raises(ValueError, match="Each child entry must be a mapping"):
            read_hierarchy_yml(path)

    def test_child_number_none(self, tmp_yml):
        from agentic_devtools.hierarchy.metadata_io import read_hierarchy_yml

        path = tmp_yml("level: epic\nchildren:\n  - title: foo\n")
        with pytest.raises(ValueError, match="Invalid child number"):
            read_hierarchy_yml(path)

    def test_child_number_non_numeric_string(self, tmp_yml):
        from agentic_devtools.hierarchy.metadata_io import read_hierarchy_yml

        path = tmp_yml("level: epic\nchildren:\n  - number: abc\n    title: foo\n")
        with pytest.raises(ValueError, match="Invalid child number"):
            read_hierarchy_yml(path)

    def test_informational_children_not_list(self, tmp_yml):
        from agentic_devtools.hierarchy.metadata_io import read_hierarchy_yml

        path = tmp_yml("level: epic\ninformational_children: not-a-list\n")
        with pytest.raises(ValueError, match="'informational_children' must be a list"):
            read_hierarchy_yml(path)

    def test_informational_child_entry_not_dict(self, tmp_yml):
        from agentic_devtools.hierarchy.metadata_io import read_hierarchy_yml

        path = tmp_yml("level: epic\ninformational_children:\n  - just-a-string\n")
        with pytest.raises(ValueError, match="Each informational_children entry must be a mapping"):
            read_hierarchy_yml(path)

    def test_informational_child_number_none(self, tmp_yml):
        from agentic_devtools.hierarchy.metadata_io import read_hierarchy_yml

        path = tmp_yml("level: epic\ninformational_children:\n  - title: bar\n")
        with pytest.raises(ValueError, match="Invalid informational child number"):
            read_hierarchy_yml(path)

    def test_informational_child_number_non_numeric(self, tmp_yml):
        from agentic_devtools.hierarchy.metadata_io import read_hierarchy_yml

        path = tmp_yml("level: epic\ninformational_children:\n  - number: xyz\n    title: bar\n")
        with pytest.raises(ValueError, match="Invalid informational child number"):
            read_hierarchy_yml(path)

    def test_child_number_numeric_string_converts(self, tmp_yml):
        """A string number like '42' should be accepted and converted."""
        from agentic_devtools.hierarchy.metadata_io import read_hierarchy_yml

        path = tmp_yml("level: epic\nchildren:\n  - number: '42'\n    title: ok\n    order: 1\n")
        meta = read_hierarchy_yml(path)
        assert meta.children[0].number == 42

    def test_informational_child_numeric_string_converts(self, tmp_yml):
        """A string number like '99' should be accepted and converted."""
        from agentic_devtools.hierarchy.metadata_io import read_hierarchy_yml

        path = tmp_yml("level: epic\ninformational_children:\n  - number: '99'\n    title: ok\n")
        meta = read_hierarchy_yml(path)
        assert meta.informational_children[0].number == 99

    def test_parent_bool_rejected(self, tmp_yml):
        """YAML `parent: true` must be rejected — bool is a subclass of int."""
        from agentic_devtools.hierarchy.metadata_io import read_hierarchy_yml

        path = tmp_yml("level: epic\nparent: true\n")
        with pytest.raises(ValueError, match="Invalid 'parent' value"):
            read_hierarchy_yml(path)

    def test_parent_false_rejected(self, tmp_yml):
        """YAML `parent: false` must be rejected."""
        from agentic_devtools.hierarchy.metadata_io import read_hierarchy_yml

        path = tmp_yml("level: feature\nparent: false\n")
        with pytest.raises(ValueError, match="Invalid 'parent' value"):
            read_hierarchy_yml(path)

    def test_parent_float_rejected(self, tmp_yml):
        """YAML `parent: 42.0` must be rejected — floats are not valid issue numbers."""
        from agentic_devtools.hierarchy.metadata_io import read_hierarchy_yml

        path = tmp_yml("level: feature\nparent: 42.0\n")
        with pytest.raises(ValueError, match="Invalid 'parent' value"):
            read_hierarchy_yml(path)

    def test_child_number_bool_rejected(self, tmp_yml):
        """YAML `number: true` in children must be rejected."""
        from agentic_devtools.hierarchy.metadata_io import read_hierarchy_yml

        path = tmp_yml("level: epic\nchildren:\n  - number: true\n    title: foo\n")
        with pytest.raises(ValueError, match="Invalid child number"):
            read_hierarchy_yml(path)

    def test_child_number_float_rejected(self, tmp_yml):
        """YAML `number: 42.0` in children must be rejected — floats are not valid issue numbers."""
        from agentic_devtools.hierarchy.metadata_io import read_hierarchy_yml

        path = tmp_yml("level: epic\nchildren:\n  - number: 42.0\n    title: foo\n")
        with pytest.raises(ValueError, match="Invalid child number"):
            read_hierarchy_yml(path)

    def test_informational_child_number_bool_rejected(self, tmp_yml):
        """YAML `number: false` in informational_children must be rejected."""
        from agentic_devtools.hierarchy.metadata_io import read_hierarchy_yml

        path = tmp_yml("level: epic\ninformational_children:\n  - number: false\n    title: bar\n")
        with pytest.raises(ValueError, match="Invalid informational child number"):
            read_hierarchy_yml(path)

    def test_informational_child_number_float_rejected(self, tmp_yml):
        """YAML `number: 99.0` in informational_children must be rejected — floats are not valid issue numbers."""
        from agentic_devtools.hierarchy.metadata_io import read_hierarchy_yml

        path = tmp_yml("level: epic\ninformational_children:\n  - number: 99.0\n    title: bar\n")
        with pytest.raises(ValueError, match="Invalid informational child number"):
            read_hierarchy_yml(path)

    def test_parent_zero_rejected(self, tmp_yml):
        """parent: 0 must be rejected — issue numbers are 1-based."""
        from agentic_devtools.hierarchy.metadata_io import read_hierarchy_yml

        path = tmp_yml("level: feature\nparent: 0\n")
        with pytest.raises(ValueError, match="must be a positive integer"):
            read_hierarchy_yml(path)

    def test_parent_negative_rejected(self, tmp_yml):
        """parent: -5 must be rejected — issue numbers are 1-based."""
        from agentic_devtools.hierarchy.metadata_io import read_hierarchy_yml

        path = tmp_yml("level: feature\nparent: -5\n")
        with pytest.raises(ValueError, match="must be a positive integer"):
            read_hierarchy_yml(path)

    def test_child_number_zero_rejected(self, tmp_yml):
        """children[].number: 0 must be rejected — issue numbers are 1-based."""
        from agentic_devtools.hierarchy.metadata_io import read_hierarchy_yml

        path = tmp_yml("level: epic\nchildren:\n  - number: 0\n    title: foo\n")
        with pytest.raises(ValueError, match="must be a positive integer"):
            read_hierarchy_yml(path)

    def test_child_number_negative_rejected(self, tmp_yml):
        """children[].number: -3 must be rejected — issue numbers are 1-based."""
        from agentic_devtools.hierarchy.metadata_io import read_hierarchy_yml

        path = tmp_yml("level: epic\nchildren:\n  - number: -3\n    title: foo\n")
        with pytest.raises(ValueError, match="must be a positive integer"):
            read_hierarchy_yml(path)

    def test_informational_child_number_zero_rejected(self, tmp_yml):
        """informational_children[].number: 0 must be rejected — issue numbers are 1-based."""
        from agentic_devtools.hierarchy.metadata_io import read_hierarchy_yml

        path = tmp_yml("level: epic\ninformational_children:\n  - number: 0\n    title: bar\n")
        with pytest.raises(ValueError, match="must be a positive integer"):
            read_hierarchy_yml(path)

    def test_informational_child_number_negative_rejected(self, tmp_yml):
        """informational_children[].number: -7 must be rejected — issue numbers are 1-based."""
        from agentic_devtools.hierarchy.metadata_io import read_hierarchy_yml

        path = tmp_yml("level: epic\ninformational_children:\n  - number: -7\n    title: bar\n")
        with pytest.raises(ValueError, match="must be a positive integer"):
            read_hierarchy_yml(path)

    def test_malformed_yaml_raises_value_error(self, tmp_yml):
        """yaml.YAMLError from malformed YAML is normalized to ValueError."""
        from agentic_devtools.hierarchy.metadata_io import read_hierarchy_yml

        # Tabs are not allowed as indentation in YAML — this triggers yaml.YAMLError
        path = tmp_yml("level: epic\nchildren:\n\t- number: 1\n")
        with pytest.raises(ValueError, match="Malformed YAML"):
            read_hierarchy_yml(path)
