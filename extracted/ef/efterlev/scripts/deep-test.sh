#!/usr/bin/env bash
# deep-test.sh — deterministic deep-test smoke (no LLM, <60s, $0 cost).
#
# Replaces the deterministic-tier portion of the old human deep-test
# prompt with a pytest-driven runner. Use this BEFORE tagging a release
# to catch user-flow regressions that unit tests miss.
#
# What it covers (S1, S2, S3, S4, S5, S6, S7, S8 from the human
# deep-test report shape — see tests/test_deep_smoke.py for per-test
# rationale):
#   S1 install + version + help
#   S2 doctor against uninitialized dir (no traceback, all checks present)
#   S3 init flow + force semantics + manifests-only directory (v0.1.39 fix)
#   S4 scan idempotency + broken-HCL handling
#   S5 friendly error on invalid ANTHROPIC_API_KEY (v0.1.38 fix)
#   S6 manifests starter pack — 26 templates
#   S7 detectors list — 51 detectors via CLI surface
#   S8 init --force preserves customer-authored manifests
#
# What it does NOT cover (separate tiers):
#   - Real LLM calls (gap/document/remediate agent runs) — `pytest -m e2e`
#   - Container smoke — release-smoke.yml matrix
#   - Post-tag PyPI/cosign verification — scripts/verify-release.sh
#
# Exit code mirrors pytest's: 0 on success, non-zero on any failure.

set -euo pipefail

cd "$(dirname "$0")/.."

# Pass through any extra args (e.g. -k, -v, --pdb).
exec uv run pytest -m deep "$@"
