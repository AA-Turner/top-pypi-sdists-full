"""Tests for _resolve_project_block_mapping (project-config layer)."""

from __future__ import annotations

import warnings

import pytest

from agentic_devtools.cli.issue_template.exceptions import TemplateValidationError
from agentic_devtools.cli.issue_template.mapping_resolver import _resolve_project_block_mapping


def _patch_config(monkeypatch: pytest.MonkeyPatch, config: dict) -> None:
    monkeypatch.setattr(
        "agentic_devtools.cli.config.project_config.load_effective_project_config",
        lambda *, git_root=None: config,
    )


def test_empty_config_returns_empty(monkeypatch: pytest.MonkeyPatch) -> None:
    _patch_config(monkeypatch, {})
    with warnings.catch_warnings():
        warnings.simplefilter("error")
        assert _resolve_project_block_mapping() == {}


def test_canonical_block(monkeypatch: pytest.MonkeyPatch) -> None:
    _patch_config(
        monkeypatch,
        {"issueTemplate": {"property_section_mapping": {"description": "omit"}}},
    )
    assert _resolve_project_block_mapping() == {"description": "omit"}


def test_alias_only_warns(monkeypatch: pytest.MonkeyPatch) -> None:
    _patch_config(
        monkeypatch,
        {"issue_template": {"property_section_mapping": {"url": "frontmatter"}}},
    )
    with pytest.warns(DeprecationWarning):
        assert _resolve_project_block_mapping() == {"url": "frontmatter"}


def test_invalid_block_raises(monkeypatch: pytest.MonkeyPatch) -> None:
    _patch_config(monkeypatch, {"issueTemplate": "not-an-object"})
    with pytest.raises(TemplateValidationError):
        _resolve_project_block_mapping()
