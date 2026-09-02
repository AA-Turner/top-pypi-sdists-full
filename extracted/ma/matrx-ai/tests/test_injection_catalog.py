"""Tests for the hardcoded auto-injection tool catalogue."""

from __future__ import annotations

from matrx_ai.injection_catalog import (
    collect_hardcoded_injection_tool_names,
    find_repo_root,
    hardcoded_injection_tool_names,
    validate_injection_tool_catalog,
)


def test_find_repo_root_has_aidream_and_packages() -> None:
    root = find_repo_root()
    assert (root / "aidream").is_dir()
    assert (root / "packages" / "matrx-ai").is_dir()


def test_collect_includes_structured_input_and_context_tools() -> None:
    by_source = collect_hardcoded_injection_tool_names()
    si = by_source["packages/matrx-ai/matrx_ai/config/structured_input_config.py"]
    ctx = by_source["aidream/services/conversation_context/context_utils.py"]
    assert "usertable_get_all" not in si
    assert "dataset" in si
    assert "context" in ctx
    assert "context_patch" in ctx


def test_hardcoded_union_is_superset_of_structured_input_runtime() -> None:
    from matrx_ai.config.structured_input_config import structured_input_editable_tool_names

    runtime = structured_input_editable_tool_names()
    ast_names = collect_hardcoded_injection_tool_names()[
        "packages/matrx-ai/matrx_ai/config/structured_input_config.py"
    ]
    assert runtime == ast_names


def test_validate_ok_when_live_catalog_covers_checked_names() -> None:
    all_names = hardcoded_injection_tool_names()
    result = validate_injection_tool_catalog(set(all_names), emit=False)
    assert result.ok


def test_empty_source_screams_instead_of_silently_going_blind(monkeypatch, tmp_path) -> None:
    """The layer-2 backstop: if an INJECTION_SOURCES file EXISTS but yields zero
    names (gutted to a shim in a service-layer move — exactly what happened to
    context_utils/tool_merge/realtime_tools on 2026-07-06), the guard must FAIL
    loudly (empty_sources) rather than pass with a silently-shrunken catalogue."""
    import matrx_ai.injection_catalog as ic

    # A source file that exists but has no extractable tool names (a shim body).
    shim = tmp_path / "gutted_source.py"
    shim.write_text('"""Shim — moved elsewhere."""\nimport sys\n', encoding="utf-8")
    monkeypatch.setattr(
        ic,
        "INJECTION_SOURCES",
        {"gutted_source.py": lambda p: frozenset()},
    )
    result = ic.validate_injection_tool_catalog(set(), repo_root=tmp_path, emit=False)
    assert "gutted_source.py" in result.empty_sources
    assert not result.ok  # a blind source is never "ok"
    # A file that is simply ABSENT is the standalone case — reported separately,
    # never conflated with a live-but-empty (blind) source.
    assert "gutted_source.py" not in result.missing_source_files
