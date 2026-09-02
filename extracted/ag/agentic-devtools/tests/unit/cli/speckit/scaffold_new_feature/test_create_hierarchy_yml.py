"""Tests for ``create_hierarchy_yml``."""

from pathlib import Path

import pytest

from agentic_devtools.cli.speckit.scaffold_new_feature import create_hierarchy_yml


def test_create_hierarchy_yml_raises_on_invalid_yaml(tmp_path: Path) -> None:
    parent_dir = tmp_path / "specs" / "001-parent"
    parent_dir.mkdir(parents=True)
    (parent_dir / "hierarchy.yml").write_text("not-valid: [", encoding="utf-8")
    with pytest.raises(ValueError, match="invalid YAML"):
        create_hierarchy_yml(parent_dir, "Parent", child_name="002-child", level="feature")


def test_create_hierarchy_yml_original_file_untouched_on_invalid_yaml(tmp_path: Path) -> None:
    parent_dir = tmp_path / "specs" / "001-parent"
    parent_dir.mkdir(parents=True)
    bad_content = "not-valid: ["
    (parent_dir / "hierarchy.yml").write_text(bad_content, encoding="utf-8")
    with pytest.raises(ValueError):
        create_hierarchy_yml(parent_dir, "Parent", child_name="002-child", level="feature")
    assert (parent_dir / "hierarchy.yml").read_text(encoding="utf-8") == bad_content


def test_create_hierarchy_yml_rejects_nonlist_children(tmp_path: Path) -> None:
    parent_dir = tmp_path / "specs" / "001-parent"
    parent_dir.mkdir(parents=True)
    (parent_dir / "hierarchy.yml").write_text("title: Parent\nchildren: bad\n", encoding="utf-8")
    with pytest.raises(ValueError, match="malformed 'children' field"):
        create_hierarchy_yml(parent_dir, "Parent", child_name="002-child", level="feature")
    # Original file must be untouched
    assert (parent_dir / "hierarchy.yml").read_text(encoding="utf-8") == "title: Parent\nchildren: bad\n"


def test_create_hierarchy_yml_rejects_non_mapping_root(tmp_path: Path) -> None:
    parent_dir = tmp_path / "specs" / "001-parent"
    parent_dir.mkdir(parents=True)
    (parent_dir / "hierarchy.yml").write_text("- child\n", encoding="utf-8")
    with pytest.raises(ValueError, match="malformed root node"):
        create_hierarchy_yml(parent_dir, "Parent", child_name="002-child", level="feature")


def test_create_hierarchy_yml_treats_yaml_null_children_as_empty(tmp_path: Path) -> None:
    parent_dir = tmp_path / "specs" / "001-parent"
    parent_dir.mkdir(parents=True)
    (parent_dir / "hierarchy.yml").write_text("title: Parent\nchildren: null\n", encoding="utf-8")
    created = create_hierarchy_yml(parent_dir, "Parent", child_name="002-child", level="feature")
    text = created.read_text(encoding="utf-8")
    assert "002" in text


def test_create_hierarchy_yml_handles_non_numeric_child_key(tmp_path: Path) -> None:
    parent_dir = tmp_path / "specs" / "001-parent"
    parent_dir.mkdir(parents=True)
    created = create_hierarchy_yml(parent_dir, "Parent", child_name="child-only", level="feature")
    text = created.read_text(encoding="utf-8")
    assert "key: child" in text
    assert "order:" not in text


def test_create_hierarchy_yml_rejects_non_regular_hierarchy_path(tmp_path: Path) -> None:
    parent_dir = tmp_path / "specs" / "001-parent"
    parent_dir.mkdir(parents=True)
    hierarchy_dir = parent_dir / "hierarchy.yml"
    hierarchy_dir.mkdir()
    with pytest.raises(ValueError, match="not a regular file"):
        create_hierarchy_yml(parent_dir, "Parent", child_name="002-child", level="feature")
    # The pre-existing directory must be left untouched
    assert hierarchy_dir.is_dir()
