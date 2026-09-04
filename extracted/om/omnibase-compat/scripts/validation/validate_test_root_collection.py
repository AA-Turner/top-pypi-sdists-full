#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2025 OmniNode.ai Inc.
# SPDX-License-Identifier: MIT

"""OMN-15541: fail closed on a test root that no CI pytest invocation collects.

Why this exists
----------------
``omnibase_compat`` has TWO pytest roots (``src/omnibase_compat/tests`` and
``tests``) and, before this guard, three surfaces that each named a different
subset of them:

======================================  ================================
surface                                 roots it named
======================================  ================================
``pyproject.toml`` ``testpaths``        both
``ci.yml`` "Run pytest (full suite)"    ``src/omnibase_compat/tests/``
``detect_test_paths.py::_full_suite``   ``["tests/"]``
======================================  ================================

The workflow's roots and the selector's roots were DISJOINT, and the workflow
won, because a positional path to ``pytest`` overrides ``testpaths`` entirely.
Consequence: every fail-closed full-suite escalation collected 141 tests and
ZERO of the 277 under the top-level ``tests/`` tree — among them the OMN-15373
ungated-Linear-Done policy gate landed hours earlier by OMN-15523, and the
``test_no_infra_edge.py`` layering guard. The escalation that exists precisely
to be the safety net when narrowing cannot be proven safe was collecting
strictly LESS than the narrow fallback. That is the worst possible polarity:
the gate reported success while testing nothing it was added to test.

The fix makes ``testpaths`` the single source of truth. This guard is the
mechanism that keeps it one (``feedback_a_rule_is_not_a_mechanism``) — a
comment saying "do not hardcode a path here" is not enforcement.

What this checks
-----------------
1. **Roots exist** (:func:`check_testpaths_exist`). A ``testpaths`` entry that
   is not a directory aborts collection with pytest exit 5 ("no tests ran"),
   reddening the whole suite for a bookkeeping error. Caught here, not in CI.

2. **Reachability** (:func:`check_uncollected_roots`). Every directory named
   ``tests`` that contains at least one ``test_*.py`` must sit under a
   ``testpaths`` root. A root outside that list cannot be run by any pytest
   invocation in this repo — the OMN-15378 / OMN-15410 class.

3. **The ci.yml seam** (:func:`check_full_suite_invocation`). ``testpaths``
   only governs if CI lets it. The full-suite step must pass NO positional
   path. This is the exact check that would have caught the original defect.

4. **The selector seam** (:func:`check_selector_parity`). The full suite is
   only one of two pytest steps. The change-aware selector's own full-suite
   selection must equal ``testpaths``, so the artifact it publishes and the
   local pre-push path that consumes it describe what CI actually runs.

Ported from ``omnibase_infra/scripts/validation/validate_test_root_collection.py``
(OMN-15410), trimmed to this repo's shape: compat has no standalone sub-project
test roots, so the ``STANDALONE_PROJECT_ROOTS`` / ``KNOWN_UNCOLLECTED_DEBT``
escape hatches are deliberately NOT ported. There is no allowlist here — wire
the root's collection instead.
"""

from __future__ import annotations

import re
import shlex
import sys
import tomllib
from pathlib import Path
from typing import Any

import yaml

REPO_ROOT = Path(__file__).resolve().parents[2]

CI_WORKFLOW = ".github/workflows/ci.yml"

# The ci.yml step whose pytest invocation defines the full suite. A rename
# here without a rename there is itself a failure (LookupError below), not a
# silent skip.
FULL_SUITE_STEP_NAME = "Run pytest (full suite)"

_IGNORED_DIR_PARTS = (".git", "__pycache__", ".venv", "node_modules", ".mypy_cache")

# GitHub Actions expressions are substituted out before shell tokenization:
# `--junitxml=junit-${{ matrix.split }}.xml` would otherwise tokenize into
# three words, one of which looks like a positional argument.
_GH_EXPRESSION = re.compile(r"\$\{\{.*?\}\}", re.DOTALL)
_GH_EXPRESSION_PLACEHOLDER = "GH_EXPR"

# pytest options that take their value as a SEPARATE token, so that
# `--splits 4` is not misread as the positional path `4`. Options written
# `--opt=value` need no entry here.
_PYTEST_VALUE_OPTIONS = frozenset(
    {
        "-c",
        "-k",
        "-m",
        "-n",
        "-o",
        "-p",
        "--deselect",
        "--dist",
        "--group",
        "--ignore",
        "--junitxml",
        "--maxfail",
        "--rootdir",
        "--splits",
        "--timeout",
        "--timeout-method",
    }
)


def collected_roots(repo_root: Path = REPO_ROOT) -> tuple[str, ...]:
    """Return ``testpaths`` from pyproject.toml, POSIX with trailing slash.

    Fails closed: a missing pyproject.toml, a missing ``testpaths`` key, or an
    empty list all raise. An empty ``testpaths`` is especially dangerous now
    that the full-suite CI step relies on it — bare ``pytest`` would collect
    from the rootdir, i.e. the entire repository including ``.venv``.
    """
    pyproject = repo_root / "pyproject.toml"
    if not pyproject.is_file():
        raise FileNotFoundError(
            f"{pyproject} does not exist; cannot determine collected test roots"
        )
    data = tomllib.loads(pyproject.read_text(encoding="utf-8"))
    paths = data.get("tool", {}).get("pytest", {}).get("ini_options", {}).get("testpaths")
    if not paths:
        raise ValueError(
            f"{pyproject} declares no [tool.pytest.ini_options] testpaths; bare "
            "`pytest` would collect the whole repository (OMN-15541)"
        )
    return tuple(str(p).rstrip("/") + "/" for p in paths)


def find_test_dirs(repo_root: Path = REPO_ROOT) -> list[str]:
    """Return every repo-relative directory named ``tests`` (POSIX, trailing
    slash) that contains at least one ``test_*.py`` at any depth below it.

    Scoped to directories literally named ``tests`` rather than "any file
    matching ``test_*.py`` anywhere", because this repo ships PRODUCT modules
    named ``test_selection_models.py`` / ``test_selection_loader.py`` (the
    change-aware selector itself); a bare ``test_*.py`` glob false-positives on
    those.
    """
    found: set[str] = set()
    for tests_dir in repo_root.rglob("tests"):
        if not tests_dir.is_dir():
            continue
        rel = tests_dir.relative_to(repo_root)
        if any(part in _IGNORED_DIR_PARTS for part in rel.parts):
            continue
        if any(tests_dir.rglob("test_*.py")):
            found.add(rel.as_posix() + "/")
    return sorted(found)


def check_testpaths_exist(repo_root: Path = REPO_ROOT) -> list[str]:
    """Every ``testpaths`` entry must be a real directory (pytest exit 5)."""
    return [
        f"{root}: listed in pyproject.toml testpaths but is not a directory on "
        "disk — pytest would abort collection with exit 5 and redden the whole "
        "suite. Remove the entry or restore the directory."
        for root in collected_roots(repo_root)
        if not (repo_root / root).is_dir()
    ]


def check_uncollected_roots(repo_root: Path = REPO_ROOT) -> list[str]:
    """Every tests/ dir holding tests must sit under a ``testpaths`` root."""
    roots = collected_roots(repo_root)
    return [
        f"{test_dir}: contains test_*.py but is not under any pyproject.toml "
        f"testpaths root ({', '.join(roots)}) — no pytest invocation in this "
        "repo can ever run these tests (OMN-15378/OMN-15410/OMN-15541 class). "
        "Add it to testpaths. There is deliberately no allowlist."
        for test_dir in find_test_dirs(repo_root)
        if not any(test_dir.startswith(root) for root in roots)
    ]


def _full_suite_run_block(repo_root: Path = REPO_ROOT) -> str:
    """Return the shell body of ci.yml's full-suite pytest step."""
    workflow_path = repo_root / CI_WORKFLOW
    if not workflow_path.is_file():
        raise FileNotFoundError(f"{CI_WORKFLOW} does not exist")
    workflow: dict[str, Any] = yaml.safe_load(workflow_path.read_text(encoding="utf-8"))
    for job in (workflow.get("jobs") or {}).values():
        for step in job.get("steps") or []:
            if isinstance(step, dict) and step.get("name") == FULL_SUITE_STEP_NAME:
                return str(step.get("run", ""))
    raise LookupError(
        f"{CI_WORKFLOW} has no step named {FULL_SUITE_STEP_NAME!r}; the "
        "full-suite invocation cannot be verified. Renaming the step does not "
        "retire this guard — update FULL_SUITE_STEP_NAME (OMN-15541)."
    )


def positional_pytest_args(run_block: str) -> list[str]:
    """Return the positional (non-option) arguments a run block passes pytest.

    GitHub expressions are replaced with a placeholder first, then the block is
    tokenized as shell so a quoted marker expression stays a single token.
    """
    text = _GH_EXPRESSION.sub(_GH_EXPRESSION_PLACEHOLDER, run_block)
    text = text.replace("\\\n", " ")
    tokens = shlex.split(text)
    if "pytest" not in tokens:
        return []
    positionals: list[str] = []
    skip_next = False
    for token in tokens[tokens.index("pytest") + 1 :]:
        if skip_next:
            skip_next = False
            continue
        if token.startswith("-"):
            skip_next = token in _PYTEST_VALUE_OPTIONS
            continue
        positionals.append(token)
    return positionals


def check_full_suite_invocation(repo_root: Path = REPO_ROOT) -> list[str]:
    """Fail closed when ci.yml's full suite names its own paths (OMN-15541).

    A positional path there silently overrides ``testpaths``. This is the check
    that catches the original defect: ``pytest src/omnibase_compat/tests/``
    made the workflow the real definition of the suite, so 277 tests never ran
    on any escalation while pyproject.toml looked correct.
    """
    positionals = positional_pytest_args(_full_suite_run_block(repo_root))
    if not positionals:
        return []
    return [
        f"{CI_WORKFLOW} step {FULL_SUITE_STEP_NAME!r} passes positional path(s) "
        f"{positionals} to pytest, overriding pyproject.toml testpaths. The full "
        "suite must pass NO positional path so it inherits every collected root "
        "(OMN-15541); use --ignore to exclude, never a positional include."
    ]


def check_selector_parity(repo_root: Path = REPO_ROOT) -> list[str]:
    """Assert the selector's full-suite paths equal ``testpaths`` (OMN-15541).

    The full suite is only one of ci.yml's two pytest steps. If
    ``detect_test_paths.py`` reverts to a hardcoded list, its published
    ``selection.json`` and the local pre-push path that consumes it start
    describing a suite CI does not run — the two-lists-that-must-agree shape
    this ticket removed.
    """
    sys.path.insert(0, str(repo_root))
    try:
        from scripts.ci.detect_test_paths import _full_suite
        from scripts.ci.test_selection_models import EnumFullSuiteReason
    finally:
        sys.path.remove(str(repo_root))

    declared = list(collected_roots(repo_root))
    selected = list(_full_suite(EnumFullSuiteReason.MAIN_BRANCH).selected_paths)
    if selected == declared:
        return []
    return [
        "scripts/ci/detect_test_paths.py::_full_suite() returns selected_paths "
        f"{selected}, which differs from pyproject.toml testpaths {declared}. "
        "The selector must derive its roots from testpaths via "
        "collected_test_roots() — two lists that must agree by convention is "
        "the exact defect OMN-15541 removed."
    ]


def main() -> int:
    violations = (
        check_testpaths_exist()
        + check_uncollected_roots()
        + check_full_suite_invocation()
        + check_selector_parity()
    )
    if violations:
        print("FAIL: test-collection defect(s) detected (OMN-15541 class):")
        for violation in violations:
            print(f"  - {violation}")
        return 1
    print(
        "OK: every tests/ directory is under a pyproject testpaths root, the "
        "ci.yml full suite inherits testpaths with no positional path, and the "
        "selector's full-suite roots match testpaths."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
