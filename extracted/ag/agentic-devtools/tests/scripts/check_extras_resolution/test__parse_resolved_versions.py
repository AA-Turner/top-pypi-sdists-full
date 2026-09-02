"""Tests for check_extras_resolution._parse_resolved_versions."""

from __future__ import annotations

from tests.scripts.check_extras_resolution import checker


def test_parse_resolved_versions_extracts_name_and_version() -> None:
    """Lines of the form ' + name==version' are parsed into a name->version mapping."""
    output = " + langgraph==1.2.11\n + requests==2.31.0\n"

    assert checker._parse_resolved_versions(output) == {
        "langgraph": "1.2.11",
        "requests": "2.31.0",
    }


def test_parse_resolved_versions_lowercases_package_names() -> None:
    """Package names are normalized to lowercase for stable comparisons."""
    output = " + PyYAML==6.0.3\n"

    assert checker._parse_resolved_versions(output) == {"pyyaml": "6.0.3"}


def test_parse_resolved_versions_ignores_lines_without_a_version() -> None:
    """Editable/local packages installed without a pinned version are skipped."""
    output = " + agentic-devtools @ file:///repo\n + requests==2.31.0\n"

    assert checker._parse_resolved_versions(output) == {"requests": "2.31.0"}


def test_parse_resolved_versions_ignores_unrelated_lines() -> None:
    """Lines that are not resolved-package lines produce no entries."""
    output = "Resolved 42 packages in 100ms\nAudited 1 package in 5ms\n"

    assert checker._parse_resolved_versions(output) == {}
