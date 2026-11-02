"""Tests for legacy-entry reconciliation with structured findings."""

import agentic_devtools.cli.github.ccr_finding_recovery as ccr_finding_recovery


def test_immediate_alias_deduplication_preserves_legacy_resolution_status() -> None:
    body = (
        "<details><summary>Suppressed comments (1)</summary>\n"
        "### [P1] Guard the response\n"
        "**File:** `src/\u200ba.py`\n"
        "**Line:** 10\n"
        "The response must be guarded.\n"
        "**src/a.py:10**: The response must be guarded.\n"
        "Resolved since the previous review.\n"
        "</details>"
    )

    result = ccr_finding_recovery.extract_ccr_findings(body)

    assert len(result.findings) == 1
    assert result.findings[0].path == "src/\u200ba.py"
    assert result.findings[0].explicitly_resolved is True
    assert result.shortfalls == ()


def test_deferred_alias_deduplication_preserves_legacy_resolution_status() -> None:
    body = (
        "<details><summary>Suppressed comments (2)</summary>\n"
        "### [P1] Guard the response\n"
        "**File:** `src/\u200ba.py`\n"
        "**Line:** 10\n"
        "The response must be guarded.\n"
        "**src/a.py:10**: The response must be guarded.\n"
        "Resolved since the previous review.\n"
        "**src/other.py:20**: The other finding remains outstanding.\n"
        "</details>"
    )

    result = ccr_finding_recovery.extract_ccr_findings(body)

    assert [(finding.path, finding.explicitly_resolved) for finding in result.findings] == [
        ("src/\u200ba.py", True),
        ("src/other.py", False),
    ]
    assert result.shortfalls == ()


def test_does_not_transfer_resolution_status_between_retained_path_aliases() -> None:
    body = (
        "<details><summary>Suppressed comments (2)</summary>\n"
        "### [P1] Guard the response\n"
        "**File:** `src/\u200ba.py`\n"
        "**Line:** 10\n"
        "The response must be guarded.\n"
        "**src/a.py:10**: The response must be guarded.\n"
        "Resolved since the previous review.\n"
        "</details>"
    )

    result = ccr_finding_recovery.extract_ccr_findings(body)

    assert [(finding.path, finding.explicitly_resolved) for finding in result.findings] == [
        ("src/\u200ba.py", False),
        ("src/a.py", True),
    ]
    assert result.shortfalls == ()


def test_resolution_status_does_not_cross_severity_levels() -> None:
    body = (
        "<details><summary>Suppressed comments (2)</summary>\n"
        "### [P1] Guard the response\n"
        "**File:** `src/a.py`\n"
        "**Line:** 10\n"
        "Guard the response.\n"
        "**src/a.py:10**\n"
        "* [P2] Independent resolved finding\n"
        "Guard the response.\n"
        "Resolved since the previous review.\n"
        "</details>"
    )

    result = ccr_finding_recovery.extract_ccr_findings(body)

    assert [(finding.severity, finding.explicitly_resolved) for finding in result.findings] == [
        ("P1", False),
        ("P2", True),
    ]
    assert result.shortfalls == ()
