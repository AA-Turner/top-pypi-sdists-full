"""Tests for resolve_effective_mapping (wrapper-layer merge + precedence)."""

from __future__ import annotations

import warnings

import pytest

from agentic_devtools.cli.issue_template import mapping_resolver
from agentic_devtools.cli.issue_template.exceptions import TemplateValidationError
from agentic_devtools.cli.issue_template.mapping_resolver import resolve_effective_mapping


def _patch_config(monkeypatch: pytest.MonkeyPatch, config: dict) -> None:
    monkeypatch.setattr(
        "agentic_devtools.cli.config.project_config.load_effective_project_config",
        lambda *, git_root=None: config,
    )


def test_no_project_and_no_explicit_returns_empty(monkeypatch: pytest.MonkeyPatch) -> None:
    _patch_config(monkeypatch, {})
    assert resolve_effective_mapping() == {}


def test_project_only(monkeypatch: pytest.MonkeyPatch) -> None:
    _patch_config(
        monkeypatch,
        {"issueTemplate": {"property_section_mapping": {"description": "omit"}}},
    )
    assert resolve_effective_mapping() == {"description": "omit"}


def test_explicit_none_returns_project(monkeypatch: pytest.MonkeyPatch) -> None:
    _patch_config(
        monkeypatch,
        {"issueTemplate": {"property_section_mapping": {"url": "frontmatter"}}},
    )
    assert resolve_effective_mapping(None) == {"url": "frontmatter"}


def test_explicit_merges_over_project(monkeypatch: pytest.MonkeyPatch) -> None:
    _patch_config(
        monkeypatch,
        {"issueTemplate": {"property_section_mapping": {"description": "omit", "url": "frontmatter"}}},
    )
    merged = resolve_effective_mapping({"url": "body:Links"})
    assert merged == {"description": "omit", "url": "body:Links"}


def test_explicit_only(monkeypatch: pytest.MonkeyPatch) -> None:
    _patch_config(monkeypatch, {})
    assert resolve_effective_mapping({"description": "body:Overview"}) == {"description": "body:Overview"}


def test_alias_emits_deprecation_warning(monkeypatch: pytest.MonkeyPatch) -> None:
    _patch_config(
        monkeypatch,
        {"issue_template": {"property_section_mapping": {"description": "omit"}}},
    )
    with pytest.warns(DeprecationWarning, match="issue_template"):
        assert resolve_effective_mapping() == {"description": "omit"}


def test_canonical_wins_over_alias(monkeypatch: pytest.MonkeyPatch) -> None:
    _patch_config(
        monkeypatch,
        {
            "issueTemplate": {"property_section_mapping": {"description": "frontmatter"}},
            "issue_template": {"property_section_mapping": {"description": "omit"}},
        },
    )
    with pytest.warns(DeprecationWarning):
        # Canonical value wins even though the alias is still present (and warns).
        assert resolve_effective_mapping() == {"description": "frontmatter"}


def test_null_canonical_falls_back_to_alias(monkeypatch: pytest.MonkeyPatch) -> None:
    _patch_config(
        monkeypatch,
        {
            "issueTemplate": None,
            "issue_template": {"property_section_mapping": {"url": "omit"}},
        },
    )
    with pytest.warns(DeprecationWarning):
        assert resolve_effective_mapping() == {"url": "omit"}


def test_null_alias_is_absent(monkeypatch: pytest.MonkeyPatch) -> None:
    _patch_config(
        monkeypatch,
        {
            "issueTemplate": {"property_section_mapping": {"url": "omit"}},
            "issue_template": None,
        },
    )
    with warnings.catch_warnings():
        warnings.simplefilter("error")
        assert resolve_effective_mapping() == {"url": "omit"}


def test_invalid_explicit_mapping_raises(monkeypatch: pytest.MonkeyPatch) -> None:
    _patch_config(monkeypatch, {})
    with pytest.raises(TemplateValidationError):
        resolve_effective_mapping({"description": "sidebar"})


def test_git_root_forwarded(monkeypatch: pytest.MonkeyPatch) -> None:
    captured: dict[str, object] = {}

    def fake_load(*, git_root=None):
        captured["git_root"] = git_root
        return {}

    monkeypatch.setattr("agentic_devtools.cli.config.project_config.load_effective_project_config", fake_load)
    resolve_effective_mapping(git_root=mapping_resolver.Path("/tmp/x"))
    assert captured["git_root"] == mapping_resolver.Path("/tmp/x")
