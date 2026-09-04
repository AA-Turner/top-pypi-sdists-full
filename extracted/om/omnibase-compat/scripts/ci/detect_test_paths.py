# SPDX-FileCopyrightText: 2025 OmniNode.ai Inc.
# SPDX-License-Identifier: MIT
"""Change-aware test path resolution for omnibase_compat CI."""

from __future__ import annotations

import argparse
import sys
import tomllib
from pathlib import Path

from scripts.ci.test_selection_loader import (
    ModelAdjacencyMap,
    load_adjacency_map,
)
from scripts.ci.test_selection_models import (
    EnumFullSuiteReason,
    ModelTestSelection,
)

SRC_PREFIX = "src/omnibase_compat/"
TEST_UNIT_PREFIX = "src/omnibase_compat/tests/"

FULL_SUITE_BRANCHES = {"main"}

REPO_ROOT = Path(__file__).resolve().parents[2]


def collected_test_roots(repo_root: Path = REPO_ROOT) -> list[str]:
    """Return ``[tool.pytest.ini_options] testpaths``, POSIX with trailing slash.

    OMN-15541. This repo has TWO test roots — ``src/omnibase_compat/tests`` and
    ``tests`` — and before this function existed three surfaces each named a
    different subset of them:

    * ``pyproject.toml`` ``testpaths``: both
    * ``ci.yml`` step "Run pytest (full suite)": ``src/omnibase_compat/tests/``
    * :func:`_full_suite`: ``["tests/"]``

    The workflow's positional path silently overrode ``testpaths``, so every
    fail-closed escalation collected 141 tests and ZERO of the 277 under
    ``tests/`` — including the OMN-15373 policy gate landed by OMN-15523. The
    escalation collected strictly LESS than the narrow fallback it was supposed
    to be the safety net for.

    ``testpaths`` is now the single source of truth: the full-suite CI step
    passes no positional path (so pytest inherits this list verbatim) and this
    function feeds the selector from the same key. Adding a root is a ONE-place
    edit. ``scripts/validation/validate_test_root_collection.py`` fails closed
    on both halves of that seam.

    Fails closed: a missing ``pyproject.toml``, a missing ``testpaths`` key, or
    an empty list all raise rather than degrade to a default. An empty
    ``testpaths`` is especially dangerous now that the full-suite step relies on
    it — bare ``pytest`` would collect from the rootdir, i.e. the whole
    repository including ``.venv``.
    """
    pyproject = repo_root / "pyproject.toml"
    if not pyproject.is_file():
        raise FileNotFoundError(
            f"{pyproject} does not exist; cannot determine collected test roots (OMN-15541)"
        )
    data = tomllib.loads(pyproject.read_text(encoding="utf-8"))
    paths = data.get("tool", {}).get("pytest", {}).get("ini_options", {}).get("testpaths")
    if not paths:
        raise ValueError(
            f"{pyproject} declares no [tool.pytest.ini_options] testpaths; bare "
            "`pytest` would collect the whole repository (OMN-15541)"
        )
    return [str(p).rstrip("/") + "/" for p in paths]


def resolve_test_paths(
    changed_files: list[str],
    adjacency_path: Path,
) -> list[str]:
    """Map changed file paths to deterministic unit test directories.

    Behavior:
      - Source changes under src/omnibase_compat/<module>: include
        src/omnibase_compat/tests/<module>/.
      - Test-only changes under src/omnibase_compat/tests/: include
        the changed test directory.
      - Files outside src/: no contribution; caller decides whether to
        escalate to full suite.
    """
    config = load_adjacency_map(adjacency_path)
    return _resolve(changed_files, config)


def _resolve(changed_files: list[str], config: ModelAdjacencyMap) -> list[str]:
    direct_modules: set[str] = set()
    selected: set[str] = set()

    for path in changed_files:
        if path.startswith(SRC_PREFIX):
            remainder = path[len(SRC_PREFIX) :]
            # Skip test files themselves — they map directly below
            if remainder.startswith("tests/"):
                parts = remainder.split("/")
                if len(parts) >= 2 and parts[1] not in ("", "__init__.py"):
                    selected.add(f"{TEST_UNIT_PREFIX}{parts[1]}/")
                continue
            module = remainder.split("/", 1)[0]
            if module in config.adjacency:
                direct_modules.add(module)

    expanded: set[str] = set(direct_modules)
    for module in direct_modules:
        expanded.update(config.adjacency[module].reverse_deps)

    for module in expanded:
        selected.add(f"{TEST_UNIT_PREFIX}{module}/")

    return sorted(selected)


def compute_selection(
    changed_files: list[str],
    adjacency_path: Path,
    ref_name: str,
    event_name: str = "pull_request",
    feature_flag_enabled: bool = True,
) -> ModelTestSelection:
    config = load_adjacency_map(adjacency_path)

    # 0. Feature flag short-circuit: off → legacy single-split full suite.
    if not feature_flag_enabled:
        return _full_suite(EnumFullSuiteReason.FEATURE_FLAG_OFF)

    # 1. Branch / event escalation.
    if ref_name in FULL_SUITE_BRANCHES:
        return _full_suite(EnumFullSuiteReason.MAIN_BRANCH)
    if event_name == "merge_group":
        return _full_suite(EnumFullSuiteReason.MERGE_GROUP)
    if event_name == "schedule":
        return _full_suite(EnumFullSuiteReason.SCHEDULED)

    # 2. Test infrastructure escalation.
    for changed in changed_files:
        if any(
            changed == infra or changed.startswith(infra.rstrip("/") + "/")
            for infra in config.test_infrastructure_paths
        ):
            return _full_suite(EnumFullSuiteReason.TEST_INFRASTRUCTURE)

    # 3. Shared module escalation.
    changed_modules = {
        path[len(SRC_PREFIX) :].split("/", 1)[0]
        for path in changed_files
        if path.startswith(SRC_PREFIX) and not path[len(SRC_PREFIX) :].startswith("tests/")
    } & set(config.adjacency.keys())
    if changed_modules & set(config.shared_modules):
        return _full_suite(EnumFullSuiteReason.SHARED_MODULE)

    # 4. Threshold escalation: too many distinct modules.
    if len(changed_modules) >= config.thresholds.modules_changed_for_full_suite:
        return _full_suite(EnumFullSuiteReason.THRESHOLD_MODULES)

    # 5. Smart selection.
    selected = _resolve(changed_files, config)
    if not selected:
        # Conservative fallback over the full tests tree. Fires for changes
        # that have no unit-test mapping (doc-only, workflow-only).
        #
        # OMN-15541: this used to be the hardcoded `["tests/"]`, which covered
        # only 277 of the repo's 418 tests — the prose called it "the full tests
        # tree" while silently omitting every test under
        # src/omnibase_compat/tests/. Sourced from pyproject `testpaths` now, so
        # "conservative" means what it says.
        selected = collected_test_roots()
    split_count = _split_count_for(selected)

    return ModelTestSelection(
        selected_paths=selected,
        split_count=split_count,
        is_full_suite=False,
        full_suite_reason=None,
        matrix=list(range(1, split_count + 1)),
    )


def _full_suite(reason: EnumFullSuiteReason) -> ModelTestSelection:
    # compat is small — 4 splits is ample for the full suite.
    #
    # OMN-15541: `selected_paths` is derived from pyproject `testpaths`, never
    # hardcoded. ci.yml's full-suite step passes NO positional path (it inherits
    # the same key directly from pytest), so this value is what the escalation
    # actually runs rather than a second list that has to be remembered.
    return ModelTestSelection(
        selected_paths=collected_test_roots(),
        split_count=4,
        is_full_suite=True,
        full_suite_reason=reason,
        matrix=[1, 2, 3, 4],
    )


def _split_count_for(selected_paths: list[str]) -> int:
    n = len(selected_paths)
    if n <= 3:
        return 1
    if n <= 6:
        return 2
    return 3


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Resolve change-aware test paths")
    parser.add_argument(
        "--changed-files-from",
        type=Path,
        required=True,
        help="Path to a file with one changed-file path per line.",
    )
    parser.add_argument("--ref-name", required=True)
    parser.add_argument("--event-name", default="pull_request")
    parser.add_argument(
        "--adjacency",
        type=Path,
        default=Path(__file__).parent / "test_selection_adjacency.yaml",
    )
    parser.add_argument(
        "--feature-flag",
        choices=("on", "off"),
        default="on",
        help="When 'off', emit a FEATURE_FLAG_OFF full-suite selection.",
    )
    args = parser.parse_args(argv)

    changed = [
        line.strip() for line in args.changed_files_from.read_text().splitlines() if line.strip()
    ]
    selection = compute_selection(
        changed_files=changed,
        adjacency_path=args.adjacency,
        ref_name=args.ref_name,
        event_name=args.event_name,
        feature_flag_enabled=(args.feature_flag == "on"),
    )
    sys.stdout.write(selection.model_dump_json())
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
