"""Tests for ``resolve_parent_spec_context()`` in ``request_artifact_fix``."""

from pathlib import Path

from agentic_devtools.cli.speckit.request_artifact_fix import resolve_parent_spec_context


def _make_task_spec(tmp_path: Path, parent_value: str = "1859") -> tuple[Path, Path]:
    spec_base = tmp_path / "specs"
    spec_dir = spec_base / "1900-task"
    spec_dir.mkdir(parents=True)
    (spec_dir / "hierarchy.yml").write_text(f"parent: {parent_value}\n", encoding="utf-8")
    return spec_dir, spec_base


class TestResolveParentSpecContext:
    """Resolves the parent feature's ``spec.md`` for task-level specs."""

    def test_returns_parent_spec_when_resolvable(self, tmp_path: Path) -> None:
        spec_dir, spec_base = _make_task_spec(tmp_path)
        parent_dir = spec_base / "1859-feature"
        parent_dir.mkdir()
        parent_spec = parent_dir / "spec.md"
        parent_spec.write_text("# Spec\n", encoding="utf-8")
        assert resolve_parent_spec_context(spec_dir, spec_base) == parent_spec

    def test_returns_none_without_hierarchy_file(self, tmp_path: Path) -> None:
        spec_dir = tmp_path / "specs" / "1900-task"
        spec_dir.mkdir(parents=True)
        assert resolve_parent_spec_context(spec_dir, tmp_path / "specs") is None

    def test_returns_none_when_parent_value_invalid(self, tmp_path: Path) -> None:
        spec_dir, spec_base = _make_task_spec(tmp_path, parent_value="none")
        assert resolve_parent_spec_context(spec_dir, spec_base) is None

    def test_returns_none_when_parent_dir_missing(self, tmp_path: Path) -> None:
        spec_dir, spec_base = _make_task_spec(tmp_path)
        assert resolve_parent_spec_context(spec_dir, spec_base) is None

    def test_returns_none_when_parent_dir_has_no_spec(self, tmp_path: Path) -> None:
        spec_dir, spec_base = _make_task_spec(tmp_path)
        (spec_base / "1859-feature").mkdir()
        assert resolve_parent_spec_context(spec_dir, spec_base) is None
