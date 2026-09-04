# SPDX-FileCopyrightText: 2025 OmniNode.ai Inc.
# SPDX-License-Identifier: MIT
"""OMN-15541: tests for the test-root collection guard.

Every check is exercised against a MUTATED tree that reproduces the real
defect, not only against the (already fixed) repo — a guard asserted green on
the fixed tree alone proves nothing about whether it can go red
(``feedback_prove_red_against_exists_but_wrong``).

The last test in this module runs the guard against the LIVE repository, so a
regression on `dev` reddens CI rather than only reddening a synthetic fixture.
"""

from __future__ import annotations

import textwrap
from pathlib import Path

import pytest

from scripts.validation.validate_test_root_collection import (
    REPO_ROOT,
    check_full_suite_invocation,
    check_selector_parity,
    check_testpaths_exist,
    check_uncollected_roots,
    collected_roots,
    find_test_dirs,
    positional_pytest_args,
)

FULL_SUITE_STEP_TEMPLATE = """\
name: CI
on:
  pull_request:
jobs:
  test-parallel:
    runs-on: ubuntu-latest
    steps:
      - name: Run pytest (full suite)
        run: |
          uv run pytest {args}\\
            --splits 4 \\
            --group 1 \\
            --tb=short \\
            --junitxml=junit-1.xml
"""


def _write_workflow(root: Path, args: str) -> None:
    workflow = root / ".github" / "workflows" / "ci.yml"
    workflow.parent.mkdir(parents=True, exist_ok=True)
    workflow.write_text(FULL_SUITE_STEP_TEMPLATE.format(args=args), encoding="utf-8")


def _write_pyproject(root: Path, testpaths: list[str] | None) -> None:
    body = "[tool.pytest.ini_options]\n"
    if testpaths is not None:
        rendered = ", ".join(f'"{p}"' for p in testpaths)
        body += f"testpaths = [{rendered}]\n"
    (root / "pyproject.toml").write_text(body, encoding="utf-8")


def _make_test_dir(root: Path, rel: str) -> None:
    target = root / rel
    target.mkdir(parents=True, exist_ok=True)
    (target / "test_thing.py").write_text("def test_thing() -> None: ...\n", encoding="utf-8")


# --------------------------------------------------------------------------
# positional_pytest_args — the tokenizer the ci.yml seam check depends on
# --------------------------------------------------------------------------


@pytest.mark.unit
def test_bare_pytest_has_no_positionals() -> None:
    block = "uv run pytest \\\n  --splits 4 \\\n  --group 1 \\\n  --tb=short\n"
    assert positional_pytest_args(block) == []


@pytest.mark.unit
def test_the_original_defect_is_detected_as_a_positional() -> None:
    """The literal pre-OMN-15541 invocation must be seen as a positional path."""
    block = "uv run pytest src/omnibase_compat/tests/ \\\n  --splits 4 \\\n  --tb=short\n"
    assert positional_pytest_args(block) == ["src/omnibase_compat/tests/"]


@pytest.mark.unit
def test_separate_value_options_are_not_mistaken_for_paths() -> None:
    """`--splits 4` must not read as the positional path `4`."""
    block = 'uv run pytest --splits 4 --group 1 -m "not slow" -n 2 --timeout 60\n'
    assert positional_pytest_args(block) == []


@pytest.mark.unit
def test_github_expressions_are_substituted_before_tokenizing() -> None:
    block = "uv run pytest --splits ${{ needs.detect.outputs.n }} --junitxml=j.xml\n"
    assert positional_pytest_args(block) == []


# --------------------------------------------------------------------------
# check_full_suite_invocation — RED against the reintroduced defect
# --------------------------------------------------------------------------


@pytest.mark.unit
def test_full_suite_check_is_red_when_a_positional_path_returns(tmp_path: Path) -> None:
    _write_pyproject(tmp_path, ["tests"])
    _write_workflow(tmp_path, "src/omnibase_compat/tests/ ")
    violations = check_full_suite_invocation(tmp_path)
    assert len(violations) == 1
    assert "src/omnibase_compat/tests/" in violations[0]
    assert "overriding pyproject.toml testpaths" in violations[0]


@pytest.mark.unit
def test_full_suite_check_is_green_with_no_positional_path(tmp_path: Path) -> None:
    _write_pyproject(tmp_path, ["tests"])
    _write_workflow(tmp_path, "")
    assert check_full_suite_invocation(tmp_path) == []


@pytest.mark.unit
def test_renaming_the_step_raises_rather_than_silently_passing(tmp_path: Path) -> None:
    """A guard that cannot find its target must fail, never report OK."""
    _write_pyproject(tmp_path, ["tests"])
    workflow = tmp_path / ".github" / "workflows" / "ci.yml"
    workflow.parent.mkdir(parents=True, exist_ok=True)
    workflow.write_text(
        textwrap.dedent(
            """\
            name: CI
            on:
              pull_request:
            jobs:
              t:
                runs-on: ubuntu-latest
                steps:
                  - name: Run pytest (everything)
                    run: uv run pytest tests/
            """
        ),
        encoding="utf-8",
    )
    with pytest.raises(LookupError):
        check_full_suite_invocation(tmp_path)


# --------------------------------------------------------------------------
# collected_roots / check_testpaths_exist — fail-closed on a bad testpaths
# --------------------------------------------------------------------------


@pytest.mark.unit
def test_missing_testpaths_key_raises(tmp_path: Path) -> None:
    _write_pyproject(tmp_path, None)
    with pytest.raises(ValueError, match="testpaths"):
        collected_roots(tmp_path)


@pytest.mark.unit
def test_empty_testpaths_raises(tmp_path: Path) -> None:
    _write_pyproject(tmp_path, [])
    with pytest.raises(ValueError, match="testpaths"):
        collected_roots(tmp_path)


@pytest.mark.unit
def test_missing_pyproject_raises(tmp_path: Path) -> None:
    with pytest.raises(FileNotFoundError):
        collected_roots(tmp_path)


@pytest.mark.unit
def test_testpaths_entry_absent_from_disk_is_red(tmp_path: Path) -> None:
    _write_pyproject(tmp_path, ["tests", "does/not/exist"])
    _make_test_dir(tmp_path, "tests")
    violations = check_testpaths_exist(tmp_path)
    assert len(violations) == 1
    assert "does/not/exist/" in violations[0]
    assert "exit 5" in violations[0]


# --------------------------------------------------------------------------
# check_uncollected_roots — the OMN-15378/15410 class
# --------------------------------------------------------------------------


@pytest.mark.unit
def test_a_test_root_outside_testpaths_is_red(tmp_path: Path) -> None:
    """Exactly the live shape: two roots on disk, only one in testpaths."""
    _write_pyproject(tmp_path, ["tests"])
    _make_test_dir(tmp_path, "tests")
    _make_test_dir(tmp_path, "src/omnibase_compat/tests")
    violations = check_uncollected_roots(tmp_path)
    assert len(violations) == 1
    assert violations[0].startswith("src/omnibase_compat/tests/")


@pytest.mark.unit
def test_both_roots_declared_is_green(tmp_path: Path) -> None:
    _write_pyproject(tmp_path, ["tests", "src/omnibase_compat/tests"])
    _make_test_dir(tmp_path, "tests")
    _make_test_dir(tmp_path, "src/omnibase_compat/tests")
    assert check_uncollected_roots(tmp_path) == []


@pytest.mark.unit
def test_nested_test_files_count_toward_their_root(tmp_path: Path) -> None:
    """A test one level below the `tests` dir still makes that dir a root."""
    _write_pyproject(tmp_path, ["tests"])
    _make_test_dir(tmp_path, "tests/unit/contracts")
    assert "tests/" in find_test_dirs(tmp_path)


@pytest.mark.unit
def test_empty_tests_dir_is_not_a_root(tmp_path: Path) -> None:
    _write_pyproject(tmp_path, ["tests"])
    _make_test_dir(tmp_path, "tests")
    (tmp_path / "docs" / "tests").mkdir(parents=True)
    assert find_test_dirs(tmp_path) == ["tests/"]


@pytest.mark.unit
def test_venv_and_cache_dirs_are_ignored(tmp_path: Path) -> None:
    _write_pyproject(tmp_path, ["tests"])
    _make_test_dir(tmp_path, "tests")
    _make_test_dir(tmp_path, ".venv/lib/site-packages/somepkg/tests")
    assert find_test_dirs(tmp_path) == ["tests/"]


# --------------------------------------------------------------------------
# Live repository — a regression on dev must redden CI, not just a fixture
# --------------------------------------------------------------------------


@pytest.mark.unit
def test_live_repo_declares_both_real_roots() -> None:
    assert set(collected_roots(REPO_ROOT)) == {"src/omnibase_compat/tests/", "tests/"}


@pytest.mark.unit
def test_live_repo_passes_every_check() -> None:
    violations = (
        check_testpaths_exist()
        + check_uncollected_roots()
        + check_full_suite_invocation()
        + check_selector_parity()
    )
    assert violations == [], "\n".join(violations)
