"""Canonical skip-set invariants: the find crawl and the agent walk can't drift."""

from __future__ import annotations

from runlayer_cli.scan.skip_dirs import (
    CONTENT_SKIP_DIRS,
    SKIP_DIR_NAMES,
    SKIP_DIR_PATH_SUFFIXES,
    find_excluded_directories,
)


def test_content_skip_dirs_is_subset_of_skip_dir_names():
    # Artifact-content pruning must never skip more than the tree walk; otherwise
    # a skill/plugin payload could lose files the walk would have kept.
    assert CONTENT_SKIP_DIRS <= SKIP_DIR_NAMES


def test_find_excludes_drop_config_bearing_dirs():
    # The tree walk prunes .vscode, but the find crawl must descend into it
    # because client MCP configs live there (e.g. .vscode/mcp.json).
    assert ".vscode" in SKIP_DIR_NAMES
    assert ".vscode" not in find_excluded_directories()


def test_find_excludes_keep_dependency_and_vcs_dirs():
    excludes = set(find_excluded_directories())
    # Dependency/build/VCS junk from the canonical set carries over to the find
    # crawl (only the config-bearing dot-dirs and generic-name build dirs drop).
    assert {"node_modules", ".git", "dist", "build", "__pycache__", "venv"} <= excludes


def test_find_excludes_drop_generic_build_env_dirs():
    # These basenames double as real project directory names, and find -prune on
    # a bare basename drops the whole subtree -- so the config/skill crawl must
    # keep descending into them even though the agent-source walk prunes them.
    excludes = set(find_excluded_directories())
    for name in ("bin", "env", "out", "obj", "wheels"):
        assert name in SKIP_DIR_NAMES, name
        assert name not in excludes, name


def test_find_excludes_keep_tool_specific_newcomers_pruned():
    # Only bare/ambiguous names are carved out; tool-specific dot-dirs and
    # dependency caches are unambiguous junk and stay pruned by the crawl.
    excludes = set(find_excluded_directories())
    assert {".tox", ".mypy_cache", ".gradle", "bower_components"} <= excludes


def test_mintlify_is_a_canonical_basename_exclude():
    assert ".mintlify" in SKIP_DIR_NAMES
    assert ".mintlify" in find_excluded_directories()


def test_shared_path_suffixes_are_exact_find_excludes():
    expected = {
        (".cursor", "extensions"),
        (".vscode", "extensions"),
        ("tests", "fixtures", "agent_detection"),
    }
    excludes = set(find_excluded_directories())

    assert expected <= SKIP_DIR_PATH_SUFFIXES
    assert {"/".join(parts) for parts in expected} <= excludes
    assert {"extensions", "fixtures"}.isdisjoint(SKIP_DIR_NAMES)
    assert {"extensions", "fixtures"}.isdisjoint(excludes)


def test_find_excludes_add_find_only_paths():
    excludes = set(find_excluded_directories())
    # Multi-segment OS caches + the plugin-install marker are find-only: the
    # os.walk basename set can't express them.
    assert {
        "Library/Caches",
        "Library/Application Support",
        "AppData",
        "installed-plugins",
    } <= excludes


def test_find_excludes_container_filesystem_bridges():
    assert "OrbStack" in find_excluded_directories()


def test_find_excludes_are_sorted_for_stable_commands():
    excludes = find_excluded_directories()
    assert excludes == sorted(excludes)
