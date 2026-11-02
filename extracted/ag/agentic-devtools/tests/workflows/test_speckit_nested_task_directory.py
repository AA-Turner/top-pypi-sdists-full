"""Behavioral tests for inherited Task directory collision validation."""

import shutil
import subprocess
from pathlib import Path

import pytest
import yaml

REPO_ROOT = Path(__file__).resolve().parents[2]
SPEC_DIRECTORY_HELPERS = REPO_ROOT / ".github" / "scripts" / "speckit-trigger" / "lib" / "spec-directory.sh"
BASH_PATH = shutil.which("bash")


def _reconcile_task_parent_metadata(hierarchy_file: Path, parent_number: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(  # noqa: S603
        [
            BASH_PATH or "bash",
            "-c",
            'source "$1"; reconcile_task_parent_metadata "$2" "$3"',
            "bash",
            str(SPEC_DIRECTORY_HELPERS),
            str(hierarchy_file),
            parent_number,
        ],
        check=False,
        capture_output=True,
        text=True,
    )


def _find_issue_spec_directories(specs_dir: Path, issue_number: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(  # noqa: S603
        [
            BASH_PATH or "bash",
            "-c",
            'source "$1"; find_issue_spec_directories "$2" "$3"',
            "bash",
            str(SPEC_DIRECTORY_HELPERS),
            str(specs_dir),
            issue_number,
        ],
        check=False,
        capture_output=True,
        text=True,
    )


def _is_verified_inherited_task_directory(
    existing_dir: Path,
    repo_root: Path,
    issue_number: str,
    hierarchy_level: str,
    spec_context: str,
    resolved_spec_dir: str = "",
) -> bool:
    result = subprocess.run(  # noqa: S603
        [
            BASH_PATH or "bash",
            "-c",
            'source "$1"; is_verified_inherited_task_directory "$2" "$3" "$4" "$5" "$6" "$7"',
            "bash",
            str(SPEC_DIRECTORY_HELPERS),
            str(existing_dir),
            str(repo_root),
            issue_number,
            hierarchy_level,
            spec_context,
            resolved_spec_dir,
        ],
        check=False,
        capture_output=True,
        text=True,
    )
    return result.returncode == 0


@pytest.mark.skipif(BASH_PATH is None, reason="bash is required for SpecKit shell helper tests")
def test_directory_collector_returns_numeric_and_prefixed_layouts_together(tmp_path: Path) -> None:
    specs_dir = tmp_path / "specs"
    numeric_dir = specs_dir / "10-parent" / "123"
    prefixed_dir = specs_dir / "10-parent" / "123-stale"
    numeric_dir.mkdir(parents=True)
    prefixed_dir.mkdir()

    result = _find_issue_spec_directories(specs_dir, "123")

    assert result.returncode == 0
    assert result.stdout.splitlines() == [str(numeric_dir), str(prefixed_dir)]


@pytest.mark.skipif(BASH_PATH is None, reason="bash is required for SpecKit shell helper tests")
def test_accepts_existing_nested_task_directory_without_local_artifacts(tmp_path: Path) -> None:
    parent_dir = tmp_path / "specs" / "10-parent"
    task_dir = parent_dir / "123-task"
    parent_dir.mkdir(parents=True)
    task_dir.mkdir()
    (parent_dir / "spec.md").write_text("# Parent spec\n", encoding="utf-8")

    assert not (task_dir / "spec.md").exists()
    assert not (task_dir / "tasks.md").exists()
    assert _is_verified_inherited_task_directory(
        task_dir,
        tmp_path,
        "123",
        "task",
        "specs/10-parent/spec.md",
    )


@pytest.mark.skipif(BASH_PATH is None, reason="bash is required for SpecKit shell helper tests")
def test_rejects_unrelated_flat_three_digit_directory(tmp_path: Path) -> None:
    parent_dir = tmp_path / "specs" / "10-parent"
    unrelated_dir = tmp_path / "specs" / "123-legacy"
    parent_dir.mkdir(parents=True)
    unrelated_dir.mkdir()
    (parent_dir / "spec.md").write_text("# Parent spec\n", encoding="utf-8")

    assert not _is_verified_inherited_task_directory(
        unrelated_dir,
        tmp_path,
        "123",
        "task",
        "specs/10-parent/spec.md",
    )


@pytest.mark.skipif(BASH_PATH is None, reason="bash is required for SpecKit shell helper tests")
def test_resolver_identity_does_not_verify_flat_three_digit_task_directory(tmp_path: Path) -> None:
    parent_dir = tmp_path / "specs" / "10-parent"
    task_dir = tmp_path / "specs" / "123-task"
    parent_dir.mkdir(parents=True)
    task_dir.mkdir()
    (parent_dir / "spec.md").write_text("# Parent spec\n", encoding="utf-8")
    (task_dir / "hierarchy.yml").write_text("level: task\nparent: 10\n", encoding="utf-8")
    (task_dir / "tasks.md").write_text("# Tasks\n", encoding="utf-8")

    assert not _is_verified_inherited_task_directory(
        task_dir,
        tmp_path,
        "123",
        "task",
        "specs/10-parent/spec.md",
        "specs/123-task",
    )


@pytest.mark.skipif(BASH_PATH is None, reason="bash is required for SpecKit shell helper tests")
def test_rejects_flat_task_directory_when_resolver_identity_does_not_match(tmp_path: Path) -> None:
    parent_dir = tmp_path / "specs" / "10-parent"
    task_dir = tmp_path / "specs" / "123-legacy"
    parent_dir.mkdir(parents=True)
    task_dir.mkdir()
    (parent_dir / "spec.md").write_text("# Parent spec\n", encoding="utf-8")

    assert not _is_verified_inherited_task_directory(
        task_dir,
        tmp_path,
        "123",
        "task",
        "specs/10-parent/spec.md",
        "specs/123-verified-task",
    )


@pytest.mark.skipif(BASH_PATH is None, reason="bash is required for SpecKit shell helper tests")
def test_reconciles_relocated_task_parent_metadata(tmp_path: Path) -> None:
    hierarchy_file = tmp_path / "hierarchy.yml"
    hierarchy_file.write_text("level: task\nparent: 20\n", encoding="utf-8")

    result = _reconcile_task_parent_metadata(hierarchy_file, "0012")

    assert result.returncode == 0
    assert hierarchy_file.read_text(encoding="utf-8") == 'level: task\nparent: "0012"\n'
    assert yaml.safe_load(hierarchy_file.read_text(encoding="utf-8"))["parent"] == "0012"


@pytest.mark.skipif(BASH_PATH is None, reason="bash is required for SpecKit shell helper tests")
def test_rejects_symlinked_hierarchy_file_without_changing_target(tmp_path: Path) -> None:
    target = tmp_path / "parent-spec.md"
    hierarchy_file = tmp_path / "task" / "hierarchy.yml"
    hierarchy_file.parent.mkdir()
    target.write_text("# Parent spec\n", encoding="utf-8")
    hierarchy_file.symlink_to(target)

    result = _reconcile_task_parent_metadata(hierarchy_file, "10")

    assert result.returncode != 0
    assert target.read_text(encoding="utf-8") == "# Parent spec\n"


@pytest.mark.skipif(BASH_PATH is None, reason="bash is required for SpecKit shell helper tests")
def test_adds_missing_task_parent_metadata(tmp_path: Path) -> None:
    hierarchy_file = tmp_path / "hierarchy.yml"
    hierarchy_file.write_text("level: task\n", encoding="utf-8")

    result = _reconcile_task_parent_metadata(hierarchy_file, "0012")

    assert result.returncode == 0
    assert hierarchy_file.read_text(encoding="utf-8") == 'level: task\nparent: "0012"\n'
    assert yaml.safe_load(hierarchy_file.read_text(encoding="utf-8"))["parent"] == "0012"
