"""Tests for flat-kind source selection and planning."""

import warnings
from pathlib import Path

import pytest

from agentic_devtools.skill_injector_prepare_flat import _prepare_flat_kind


def _source_file(root: Path, name: str, content: str = "---\ndescription: item\n---\n") -> Path:
    path = root / name
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    return path


def test_unfiltered_selection_skips_unmanaged_and_manifest_files(tmp_path: Path) -> None:
    source = tmp_path / "source"
    source.mkdir()
    _source_file(source, "agdt.agent.md")
    _source_file(source, "custom.md")
    _source_file(source, "speckit.plan.agent.md")
    _source_file(source, "agdt.README.md")

    plan, origins, cache, pruned = _prepare_flat_kind(
        "agents", source, tmp_path / "target", issue_adapter=None, code_hosting=None
    )

    assert plan.added == ("agdt.agent.md",)
    assert set(origins) == {"agdt.agent.md"}
    assert cache == {}
    assert pruned == 0


def test_filtering_keeps_matching_and_binary_files_and_counts_pruned(tmp_path: Path) -> None:
    source = tmp_path / "source"
    source.mkdir()
    _source_file(source, "agdt.keep.agent.md", "---\nagdt:\n  requires:\n    issue_adapter: github\n---\n")
    _source_file(source, "agdt.drop.agent.md", "---\nagdt:\n  requires:\n    issue_adapter: jira\n---\n")
    (source / "agdt.binary.agent.md").write_bytes(b"\xff")

    reported_counts: list[tuple[int, int]] = []
    _plan, origins, cache, pruned = _prepare_flat_kind(
        "agents",
        source,
        tmp_path / "target",
        issue_adapter="github",
        code_hosting=None,
        on_counts=lambda injected, pruned_count: reported_counts.append((injected, pruned_count)),
    )

    assert set(origins) == {"agdt.keep.agent.md", "agdt.binary.agent.md"}
    assert cache == {source / "agdt.keep.agent.md": {"agdt": {"requires": {"issue_adapter": "github"}}}}
    assert pruned == 1
    assert reported_counts == [(0, 1), (2, 0)]


def test_exact_flat_name_collision_warns_and_last_source_wins(tmp_path: Path) -> None:
    source = tmp_path / "source"
    _source_file(source, "sub-1/agdt.duplicate.md", "first")
    _source_file(source, "sub_1/agdt.duplicate.md", "second")

    with pytest.warns(RuntimeWarning, match="duplicate flat filename"):
        _plan, origins, _cache, _pruned = _prepare_flat_kind(
            "agents", source, tmp_path / "target", issue_adapter=None, code_hosting=None
        )

    assert len(origins) == 1
    assert next(iter(origins.values())).read_text(encoding="utf-8") == "second"


def test_casefold_collision_warns_and_replaces_prior_spelling(tmp_path: Path) -> None:
    source = tmp_path / "source"
    _source_file(source, "Sub/agdt.collision.md", "upper")
    _source_file(source, "sub/agdt.collision.md", "lower")

    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter("always")
        _plan, origins, _cache, _pruned = _prepare_flat_kind(
            "agents", source, tmp_path / "target", issue_adapter=None, code_hosting=None
        )

    assert len(caught) == 1
    assert "case-insensitive" in str(caught[0].message)
    assert tuple(origins) == ("agdt.sub.agdt.collision.md",)
    assert next(iter(origins.values())).read_text(encoding="utf-8") == "lower"
