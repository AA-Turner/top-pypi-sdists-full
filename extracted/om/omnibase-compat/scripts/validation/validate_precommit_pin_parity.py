#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2025 OmniNode.ai Inc.
# SPDX-License-Identifier: MIT

"""
CI/pre-commit check: pin-parity ratchet between .pre-commit-config.yaml and
.github/workflows/ci.yml (OMN-14669, WS7 fan-out #6 of OMN-14655; DRIFT-3
recurrence guard).

The problem this guards: a pre-commit hook pins an omnibase_core SHA that clones
the validator at one commit, while the SAME validator's CI job pins a DIFFERENT
SHA. Both surfaces then enforce a DIFFERENT frozen baseline, so a change that is
green locally can be red in CI (or vice-versa) purely because the two pins
drifted -- staleness by construction. This gate fails closed the moment a pinned
pair diverges, on either side.

Adaptation from the omnimarket/omniclaude/omnibase_infra ports: in
omnibase_compat the shared omnibase_core validator (`no-noncanonical-lifecycle-classes`,
OMN-14350) is a `repo: local`, `language: python` pre-commit hook that pins core
via `additional_dependencies` (NOT a remote `repo:` block with a top-level
`rev:`), because compat's no-infra-edge invariant forbids a real omnibase_core
dependency edge in pyproject/uv.lock. So `_find_hook_pin` extracts the pinned
SHA from the hook's `additional_dependencies` git-URL rather than from
`repo.rev`. The CI counterpart is compat's single `.github/workflows/ci.yml`
`no-noncanonical-lifecycle-classes` job, which pins the same validator via
`uv run --with 'omnibase-core @ git+...@<sha>'`. Both must resolve to the
identical SHA.

Note the two surfaces spell the git URL slightly differently (`omnibase_core.git@`
in the pre-commit additional_dependencies vs `omnibase_core@` in ci.yml); the
extraction regex tolerates the optional `.git` suffix so a real SHA match is
never masked by that cosmetic difference.

PIN_PAIRS below is a small, explicitly-verified table -- add a new pair only
after confirming (by hand, via `git diff <old-rev> <new-rev>` in omnibase_core)
that both sides really do reference the same validator, not two independently
pinned tools that happen to share an upstream repo.

Intentionally NOT enforced here: the `normalization-symmetry` pre-commit hook
also pins an omnibase_core SHA via `additional_dependencies`, but compat's ci.yml
has NO CI counterpart job for it (it is a pre-commit-only orphan), so there is no
second pin to compare against -- adding it to PIN_PAIRS would false-fail on a
missing CI pin. It stays out until a CI counterpart exists.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path
from typing import Any

import yaml

REPO_ROOT = Path(__file__).resolve().parents[2]
CONFIG_PATH = REPO_ROOT / ".pre-commit-config.yaml"
CI_WORKFLOW_PATH = REPO_ROOT / ".github" / "workflows" / "ci.yml"

# (pre-commit hook id, validator module the pair references [for humans/audit
#  only]) -> the SHA the hook pins in `additional_dependencies` and the SHA
# ci.yml pins for the same validator must be identical.
PIN_PAIRS: tuple[tuple[str, str], ...] = (
    (
        "no-noncanonical-lifecycle-classes",
        "no_noncanonical_lifecycle_classes",
    ),
)

# Matches an omnibase_core git-pin on either surface. The `.git` suffix is
# optional (pre-commit writes `omnibase_core.git@<sha>`, ci.yml writes
# `omnibase_core@<sha>`); both resolve to the same 40-hex SHA.
_CORE_PIN_RE = re.compile(
    r"omnibase[-_]core\s*@\s*git\+https://github\.com/OmniNode-ai/omnibase_core"
    r"(?:\.git)?@([0-9a-f]{40})"
)


def _find_hook_pin(config: dict[str, Any], hook_id: str) -> str | None:
    """Extract the omnibase_core SHA a `repo: local` hook pins via
    `additional_dependencies`. Returns None if the hook or a core pin is
    absent."""
    for repo in config.get("repos", []):
        if repo.get("repo") != "local":
            continue
        for hook in repo.get("hooks", []):
            if hook.get("id") != hook_id:
                continue
            for dep in hook.get("additional_dependencies") or []:
                m = _CORE_PIN_RE.search(str(dep))
                if m is not None:
                    return m.group(1)
    return None


def _find_ci_pins(ci_text: str) -> list[str]:
    return [m.group(1) for m in _CORE_PIN_RE.finditer(ci_text)]


def main() -> int:
    if not CONFIG_PATH.is_file():
        print(f"ERROR: {CONFIG_PATH} not found", file=sys.stderr)
        return 1
    if not CI_WORKFLOW_PATH.is_file():
        print(f"ERROR: {CI_WORKFLOW_PATH} not found", file=sys.stderr)
        return 1

    config = yaml.safe_load(CONFIG_PATH.read_text(encoding="utf-8"))
    ci_text = CI_WORKFLOW_PATH.read_text(encoding="utf-8")

    violations: list[str] = []

    for hook_id, validator in PIN_PAIRS:
        precommit_pin = _find_hook_pin(config, hook_id)
        if precommit_pin is None:
            violations.append(
                f"pin-parity: no omnibase_core additional_dependencies pin found "
                f"for hook id={hook_id!r} (validator {validator!r}) in "
                f"{CONFIG_PATH.name} -- update PIN_PAIRS or the config."
            )
            continue

        ci_pins = _find_ci_pins(ci_text)
        if not ci_pins:
            violations.append(
                f"pin-parity: no CI-pinned omnibase_core SHA found in "
                f"{CI_WORKFLOW_PATH.name} (hook {hook_id!r}, validator "
                f"{validator!r}) -- update PIN_PAIRS or restore the CI pin."
            )
            continue

        mismatched = sorted({p for p in ci_pins if p != precommit_pin})
        if mismatched:
            violations.append(
                f"pin-parity: hook {hook_id!r} pins {precommit_pin} in "
                f"{CONFIG_PATH.name}, but {CI_WORKFLOW_PATH.name} pins "
                f"{mismatched} for the same validator ({validator}). These must "
                "match -- bump whichever side is stale."
            )

    if violations:
        print(f"FAIL: {len(violations)} pin-parity violation(s):\n")
        for v in violations:
            print(f"  {v}\n")
        return 1

    print("OK: all pinned SHAs in PIN_PAIRS match their CI-pinned counterpart.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
