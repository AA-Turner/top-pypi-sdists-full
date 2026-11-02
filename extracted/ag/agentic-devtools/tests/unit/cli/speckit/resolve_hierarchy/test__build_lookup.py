"""Tests for the shared CLI-argument helpers used by both hierarchy-resolution commands."""

import argparse

import pytest

from agentic_devtools.cli.speckit.resolve_hierarchy import GitHubHierarchyLookup, _build_lookup


def test_returns_a_valid_lookup_client() -> None:
    parser = argparse.ArgumentParser()
    lookup = _build_lookup(parser, "owner/repo", "main", "token")
    assert isinstance(lookup, GitHubHierarchyLookup)
    assert lookup.repo == "owner/repo"


def test_routes_invalid_repo_through_parser_error() -> None:
    parser = argparse.ArgumentParser(prog="test")
    with pytest.raises(SystemExit) as exc_info:
        _build_lookup(parser, "invalid", "main", "token")
    assert exc_info.value.code == 2
