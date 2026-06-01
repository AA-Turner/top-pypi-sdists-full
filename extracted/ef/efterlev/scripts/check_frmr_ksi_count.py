"""FRMR KSI-count drift gate (v0.1.164 / #369).

Re-fetches the live FRMR JSON from the canonical FedRAMP repo and
counts the KSIs across all themes. Fails if the count diverges from
the constant we publish (`EXPECTED_KSI_COUNT` below).

Why this exists: in May 2026 we shipped CLI output saying "60 KSIs"
in many places. The authoritative source is
`github.com/FedRAMP/docs/FRMR.documentation.json`. Without a CI
gate, a future FRMR bump (Phase 3 finalization is expected Q3 2026)
could land 61 / 63 / something else and we'd find out from a
customer instead of from CI.

This script:
  1. Fetches the live FRMR JSON via the GitHub API
  2. Counts KSIs across all themes
  3. Compares to EXPECTED_KSI_COUNT
  4. Exits 0 on match, 1 on drift with a diff-friendly summary

Run by `.github/workflows/frmr-drift.yml` on a daily cron (or via
manual workflow_dispatch when a maintainer wants to check).

No third-party dependencies — pure stdlib so the workflow doesn't
need `uv sync`.
"""

from __future__ import annotations

import json
import sys
import urllib.error
import urllib.request

FRMR_URL = "https://raw.githubusercontent.com/FedRAMP/docs/main/FRMR.documentation.json"
"""Canonical source. Raw URL bypasses the GitHub API rate limit
(unauthenticated requests are 60/hour; CI cron + ad-hoc runs add up).
"""

# Pinned expected count. Bump here when FedRAMP bumps the FRMR
# catalog AND we've updated our vendored copy + CLI strings.
# As of 2026-05-19 the live FRMR is v0.9.43-beta with 60 KSIs.
EXPECTED_KSI_COUNT = 60
EXPECTED_FRMR_VERSION_PREFIX = "0.9."


def _fetch_frmr() -> dict:
    """Fetch the live FRMR JSON. Raises SystemExit on network failure
    so CI surfaces the upstream outage clearly (don't mask it as
    drift)."""
    try:
        # FRMR_URL is a module-level constant pinned to the canonical
        # FedRAMP raw URL; nothing user-controlled flows in. The
        # nosemgrep comment uses the rule's fully-qualified id —
        # semgrep does NOT accept short-form suppressions.
        # nosemgrep: python.lang.security.audit.dynamic-urllib-use-detected.dynamic-urllib-use-detected  # noqa: E501
        with urllib.request.urlopen(FRMR_URL, timeout=30) as response:
            return json.loads(response.read().decode("utf-8"))
    except (urllib.error.URLError, TimeoutError) as e:
        print(f"::error::failed to fetch FRMR JSON from {FRMR_URL}: {e}", file=sys.stderr)
        # Exit 0 on network failure so transient infra issues don't
        # block PRs. The drift check itself is the value; an unreachable
        # FedRAMP repo is not actionable from our side.
        sys.exit(0)


def main() -> int:
    doc = _fetch_frmr()
    info = doc.get("info", {})
    version = info.get("version", "<unknown>")
    last_updated = info.get("last_updated", "<unknown>")

    ksi = doc.get("KSI", {})
    if not isinstance(ksi, dict):
        print(f"::error::KSI section missing or malformed in FRMR; got: {type(ksi)}")
        return 1

    per_theme: dict[str, int] = {}
    total = 0
    for theme_key, theme in ksi.items():
        if not isinstance(theme, dict):
            continue
        indicators = theme.get("indicators", {})
        n = len(indicators) if isinstance(indicators, (dict, list)) else 0
        per_theme[theme_key] = n
        total += n

    print(f"FRMR version: {version} (last_updated: {last_updated})")
    print(f"Live KSI count: {total}")
    print(f"Per-theme: {per_theme}")
    print(f"Expected: {EXPECTED_KSI_COUNT}")

    if total != EXPECTED_KSI_COUNT:
        print(
            f"::error::FRMR drift detected: live catalog reports {total} KSIs, "
            f"we pin EXPECTED_KSI_COUNT={EXPECTED_KSI_COUNT}. "
            f"Either (a) FedRAMP bumped the catalog and we need to "
            f"refresh the vendored FRMR + all CLI strings, or (b) FRMR "
            f"emit changed shape. Investigate {FRMR_URL} and update "
            f"scripts/check_frmr_ksi_count.py once the new count is "
            f"baked into the codebase."
        )
        return 1

    if not version.startswith(EXPECTED_FRMR_VERSION_PREFIX):
        # Soft warn — version bumps within the 0.9.x series ship
        # without a count change frequently (cosmetic/standardization
        # tweaks). Major-version bumps (1.0+) deserve attention.
        print(
            f"::warning::FRMR version {version} is outside the "
            f"expected {EXPECTED_FRMR_VERSION_PREFIX}x prefix. "
            f"Check the CHANGELOG to confirm no breaking changes."
        )

    print("OK: live FRMR KSI count matches pinned expectation.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
