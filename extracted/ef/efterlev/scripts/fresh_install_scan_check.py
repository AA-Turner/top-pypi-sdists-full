#!/usr/bin/env python3
"""Fresh-install scan smoke: catch dependency-resolution regressions that the
locked CI lanes can't see.

CI runs every test against the pinned `uv.lock`. But a real `pip` / `uv` /
`pipx install efterlev` resolves the *latest* versions allowed by the
pyproject constraints — a resolution no locked lane ever exercises. So a new
breaking release of an allowed transitive (the v0.1.215 case: `python-hcl2`
8.1.2 changed the parser output shape and silently zeroed out detector
matching) is invisible to the entire test suite. The bundled-fixture scan
dropped from ~21 evidence records to ~1, and nothing went red.

This check is meant to run in a venv where efterlev was installed WITHOUT the
lockfile (plain `pip install .`), so its dependency resolution mirrors a real
user's. It runs the keyless `efterlev quickstart` (init + scan on the bundled
fixture, no LLM call) and asserts the scan fired a healthy number of detectors
and evidence records. A dependency regression that breaks parsing collapses
those counts and fails the check.

A/B: revert the `python-hcl2` cap to `<9`, install fresh, and this check fails
(evidence ~1 < the floor) — the exact prod failure mode, caught automatically.
"""

from __future__ import annotations

import os
import re
import subprocess
import sys

# Working scan of the bundled quickstart fixture fires ~21 evidence records
# across ~17 detectors. The python-hcl2-8.1.2-broken case produced 2 / 1.
# Floors sit well above the broken case and well below the healthy case, so
# they catch a catastrophic parsing regression without being brittle to small
# fixture growth/shrink. Raise the fixture, not these floors, if coverage grows.
MIN_EVIDENCE_RECORDS = 10
MIN_DETECTORS_FIRED = 8

_SCANNED_RE = re.compile(
    r"Scanned:\s+(\d+)\s+resources\s+/\s+(\d+)\s+evidence records\s+/\s+(\d+)\s+detectors fired"
)


def main() -> int:
    # Force the keyless path (init + scan only) — no LLM key, deterministic, free.
    env = dict(os.environ)
    for key in ("ANTHROPIC_API_KEY", "OPENAI_API_KEY", "AWS_BEARER_TOKEN_BEDROCK"):
        env.pop(key, None)

    # Invoke via THIS interpreter (`sys.executable -m efterlev`), not a bare
    # `efterlev` on PATH — bare `efterlev` could resolve to a different install
    # (a uv-tool / pipx one) and silently test the wrong dependency set. We must
    # exercise the efterlev installed in the interpreter running this check.
    print("==> running `python -m efterlev quickstart` (keyless) on the fresh-resolved install ...")
    # Fixed argv (no shell, no user input) — safe by construction. Bare
    # `# nosemgrep` per the CLAUDE.md gotcha (targeted suppression needs the
    # full registry-resolved rule_id); same pattern as scripts/e2e_smoke.py.
    proc = subprocess.run(  # nosemgrep
        [sys.executable, "-m", "efterlev", "quickstart"],
        capture_output=True,
        text=True,
        env=env,
        check=False,
    )
    print(proc.stdout)
    if proc.stderr.strip():
        print("--- stderr ---", file=sys.stderr)
        print(proc.stderr, file=sys.stderr)

    if proc.returncode != 0:
        print(
            f"FAIL: `efterlev quickstart` exited {proc.returncode}.",
            file=sys.stderr,
        )
        return 1

    m = _SCANNED_RE.search(proc.stdout)
    if m is None:
        print(
            "FAIL: could not find the 'Scanned: N resources / M evidence records / "
            "K detectors fired' summary line in quickstart output. The output format "
            "may have changed — update _SCANNED_RE here.",
            file=sys.stderr,
        )
        return 1

    resources, evidence, detectors = (int(m.group(1)), int(m.group(2)), int(m.group(3)))
    print(
        f"==> parsed: {resources} resources / {evidence} evidence records / "
        f"{detectors} detectors fired"
    )

    ok = evidence >= MIN_EVIDENCE_RECORDS and detectors >= MIN_DETECTORS_FIRED
    if not ok:
        print(
            f"FAIL: the fresh-install scan is anemic — {evidence} evidence records "
            f"(floor {MIN_EVIDENCE_RECORDS}), {detectors} detectors fired "
            f"(floor {MIN_DETECTORS_FIRED}).\n"
            "This is the signature of a dependency-resolution regression: a freshly "
            "resolved transitive (e.g. python-hcl2) broke detector parsing while the "
            "locked CI lanes stayed green. Check recent releases of the IaC-parsing "
            "deps and the pyproject constraints (see DECISIONS 2026-06-01).",
            file=sys.stderr,
        )
        return 1

    print(
        f"PASS: fresh-install scan healthy ({evidence} >= {MIN_EVIDENCE_RECORDS} evidence, "
        f"{detectors} >= {MIN_DETECTORS_FIRED} detectors)."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
