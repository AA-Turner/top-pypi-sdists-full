"""Integration tests — golden parity between the legacy Bash scaffold and the native Python scaffold.

These tests execute the real ``create-new-feature.sh`` as a subprocess and compare the
output and side-effects against ``prepare_new_feature`` to guard the migration contract.
"""

import json
import os
import shutil
import subprocess
from collections.abc import Generator
from pathlib import Path
from unittest.mock import patch

import pytest
import yaml

from agentic_devtools.cli.speckit.scaffold_new_feature import prepare_new_feature


def _repository_root() -> Path | None:
    for candidate in Path(__file__).resolve().parents:
        if (candidate / "pyproject.toml").is_file() and (candidate / ".specify").is_dir():
            return candidate
    return None


REPOSITORY_ROOT = _repository_root()
LEGACY_SCRIPT_RELATIVE_PATH = (
    Path(".specify") / "extensions" / "agdt-workflows" / "scripts" / "bash" / "create-new-feature.sh"
)
LEGACY_SCRIPT = REPOSITORY_ROOT / LEGACY_SCRIPT_RELATIVE_PATH if REPOSITORY_ROOT is not None else None


@pytest.fixture(autouse=True)
def _restore_env() -> Generator[None, None, None]:
    """Snapshot and restore os.environ to prevent env leaks between tests."""
    snapshot = os.environ.copy()
    try:
        yield
    finally:
        os.environ.clear()
        os.environ.update(snapshot)


def _run_legacy_scaffold(repo_root: Path, args: list[str], *, force_no_flock: bool = False) -> dict[str, str | None]:
    legacy_script = LEGACY_SCRIPT
    if legacy_script is None or not legacy_script.is_file():
        pytest.skip(f"Legacy scaffold script is unavailable: {LEGACY_SCRIPT}")
    script = repo_root / LEGACY_SCRIPT_RELATIVE_PATH
    script.parent.mkdir(parents=True, exist_ok=True)
    script_bytes = legacy_script.read_bytes().replace(b"\r\n", b"\n")
    if force_no_flock:
        script_bytes = script_bytes.replace(
            b"if command -v flock >/dev/null 2>&1; then",
            b"if false; then",
            1,
        )
    script.write_bytes(script_bytes)
    script_argument = script.relative_to(repo_root).as_posix()
    completed = subprocess.run(
        ["bash", script_argument, "--json", *args],
        cwd=repo_root,
        capture_output=True,
        text=True,
        check=False,
        shell=False,
    )
    assert completed.returncode == 0, completed.stderr
    payload = json.loads(completed.stdout)
    assert isinstance(payload, dict)
    return payload


def _relative_path(value: str, repo_root: Path) -> str:
    shell_path = value
    if os.name == "nt":
        if len(shell_path) >= 7 and shell_path.startswith("/mnt/") and shell_path[5].isalpha() and shell_path[6] == "/":
            shell_path = f"{shell_path[5].upper()}:{shell_path[6:]}"
        elif len(shell_path) >= 4 and shell_path[0] == "/" and shell_path[2] == "/" and shell_path[1].isalpha():
            shell_path = f"{shell_path[1].upper()}:{shell_path[2:]}"
    resolved = Path(shell_path).resolve()
    try:
        return resolved.relative_to(repo_root.resolve()).as_posix()
    except ValueError as exc:
        raise AssertionError(f"Scaffold output path is outside the test repository: {value}") from exc


@pytest.mark.parametrize(
    ("args", "feature_number", "parent_feature_number", "flat"),
    [
        (["--issue", "42", "--flat", "Add login flow"], 42, None, True),
        (["--issue", "43", "Standalone feature"], 43, None, False),
        (["--issue", "200", "--parent", "100", "Child feature"], 200, 100, False),
    ],
    ids=["flat", "standalone", "explicit-parent"],
)
def test_matches_legacy_scaffold_golden(
    tmp_path: Path,
    args: list[str],
    feature_number: int,
    parent_feature_number: int | None,
    flat: bool,
) -> None:
    """Native scaffold produces identical paths, metadata, and side-effect files as the legacy script."""
    legacy_root = tmp_path / "legacy"
    native_root = tmp_path / "native"
    if REPOSITORY_ROOT is None:
        pytest.skip("Repository root is unavailable")
    template_relative_path = Path(".specify") / "presets" / "agdt-templates" / "templates" / "spec-template.md"
    source_template = REPOSITORY_ROOT / template_relative_path
    if not source_template.is_file():
        pytest.skip(f"Preset spec template is unavailable: {source_template}")
    for root in (legacy_root, native_root):
        destination = root / template_relative_path
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source_template, destination)
    legacy = _run_legacy_scaffold(legacy_root, args)
    with (
        patch("agentic_devtools.cli.speckit.scaffold_new_feature._create_or_checkout_branch"),
        patch(
            "agentic_devtools.cli.speckit.scaffold_new_feature.detect_parent_hierarchy",
            return_value={"status": "ok"},
        ),
    ):
        native = prepare_new_feature(
            repo_root=native_root,
            feature_description=args[-1],
            feature_number=feature_number,
            parent_feature_number=parent_feature_number,
            flat=flat,
        )
    native_payload = native.to_dict()

    for key in ("BRANCH_NAME", "FEATURE_NUM"):
        assert native_payload[key] == legacy[key]
    native_spec = native_payload["SPEC_FILE"]
    legacy_spec = legacy["SPEC_FILE"]
    assert isinstance(native_spec, str)
    assert isinstance(legacy_spec, str)
    assert _relative_path(native_spec, native_root) == _relative_path(legacy_spec, legacy_root)
    native_parent = native_payload["PARENT_SPEC_DIR"]
    legacy_parent = legacy["PARENT_SPEC_DIR"]
    assert (native_parent is None) == (legacy_parent is None)
    if isinstance(native_parent, str) and isinstance(legacy_parent, str):
        assert _relative_path(native_parent, native_root) == _relative_path(legacy_parent, legacy_root)
    assert native_payload["HIERARCHY_LEVEL"] == legacy["HIERARCHY_LEVEL"]

    legacy_files = {
        path.relative_to(legacy_root).as_posix()
        for path in legacy_root.rglob("*")
        if path.is_file() and path.name in {"spec.md", "hierarchy.yml"}
    }
    native_files = {
        path.relative_to(native_root).as_posix()
        for path in native_root.rglob("*")
        if path.is_file() and path.name in {"spec.md", "hierarchy.yml"}
    }
    assert native_files == legacy_files
    for relative_path in legacy_files:
        native_file = native_root / relative_path
        legacy_file = legacy_root / relative_path
        if native_file.name == "hierarchy.yml":
            assert yaml.safe_load(native_file.read_text(encoding="utf-8")) == yaml.safe_load(
                legacy_file.read_text(encoding="utf-8")
            )
        else:
            assert native_file.read_bytes() == legacy_file.read_bytes()


def test_legacy_mkdir_fallback_reuses_native_lock_file(tmp_path: Path) -> None:
    """The legacy no-flock path can update a parent after a native run leaves a file lock."""
    repo_root = tmp_path / "repo"
    if REPOSITORY_ROOT is None:
        pytest.skip("Repository root is unavailable")
    template_relative_path = Path(".specify") / "presets" / "agdt-templates" / "templates" / "spec-template.md"
    source_template = REPOSITORY_ROOT / template_relative_path
    if not source_template.is_file():
        pytest.skip(f"Preset spec template is unavailable: {source_template}")
    destination = repo_root / template_relative_path
    destination.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source_template, destination)

    parent_dir = repo_root / "specs" / "100-parent"
    parent_dir.mkdir(parents=True)

    with (
        patch("agentic_devtools.cli.speckit.scaffold_new_feature._create_or_checkout_branch"),
        patch("agentic_devtools.cli.speckit.scaffold_new_feature.detect_parent_hierarchy", return_value=None),
    ):
        prepare_new_feature(
            repo_root=repo_root,
            feature_description="First child",
            feature_number=200,
            parent_feature_number=100,
            dry_run=False,
        )

    lock_path = parent_dir / ".hierarchy.yml.lock"
    assert lock_path.is_file()

    _run_legacy_scaffold(
        repo_root,
        ["--issue", "201", "--parent", "100", "Second child"],
        force_no_flock=True,
    )

    parent_hierarchy = yaml.safe_load((parent_dir / "hierarchy.yml").read_text(encoding="utf-8"))
    assert [child["key"] for child in parent_hierarchy["children"]] == ["200", "201"]
