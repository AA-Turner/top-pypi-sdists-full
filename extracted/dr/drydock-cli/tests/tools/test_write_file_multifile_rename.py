"""write_file must refuse multi-file identifier renames disguised as a full-
file overwrite — the third escape hatch (after search_replace and ``sed -i``)
the model uses to silently rename an identifier in one file and leave it
inconsistent in the rest of the package.

Real-world trigger (operator session, 2026-05-25, slides PRD):
- model tries to rename ``BlockType.LIST_ITEM`` -> ``BlockType.list_item``
- search_replace refuses (correctly) -> redirects to ``mechanical_rename``
- model bypasses by switching to ``write_file llm.py`` with the rename inline
- 5 other files in the package still reference ``LIST_ITEM`` -> silently broken
"""

from __future__ import annotations

import os
from pathlib import Path

import pytest

from drydock.core.tools.builtins.search_replace import SearchReplace


@pytest.fixture(autouse=True)
def _enable_intercept(monkeypatch):
    monkeypatch.setenv("DRYDOCK_MULTIFILE_INTERCEPT", "1")


def _build_slides_pkg(tmp_path: Path) -> Path:
    pkg = tmp_path / "slides"
    pkg.mkdir()
    (pkg / "__init__.py").write_text("")
    (pkg / "models.py").write_text(
        "class BlockType:\n    LIST_ITEM = 'list_item'\n    HEADING = 'heading'\n"
    )
    (pkg / "renderer.py").write_text(
        "from .models import BlockType\nx = BlockType.LIST_ITEM\n"
    )
    (pkg / "refiner.py").write_text(
        "from .models import BlockType\ny = BlockType.LIST_ITEM\n"
    )
    (pkg / "extractor.py").write_text(
        "from .models import BlockType\nz = BlockType.LIST_ITEM\n"
    )
    return pkg


def test_write_file_path_refuses_and_leaves_other_files_alone(tmp_path):
    """auto_apply=False (the write_file path) must REFUSE rather than auto-
    apply the rename, so we don't silently throw away the model's other
    intended changes to the target file."""
    pkg = _build_slides_pkg(tmp_path)
    llm = pkg / "llm.py"
    existing = (
        "from .models import BlockType\n\n"
        "def plan():\n"
        "    return BlockType.LIST_ITEM  # uses the enum value here\n"
    )
    llm.write_text(existing)
    new_content = (
        "from .models import BlockType\n\n"
        "def plan():\n"
        "    return BlockType.list_item  # uses the enum value here\n"
    )

    redirect = SearchReplace._detect_multifile_rename(
        existing, new_content, llm, auto_apply=False,
    )
    assert redirect is not None
    assert redirect.startswith("REFUSED:"), redirect
    assert "LIST_ITEM" in redirect
    assert "mechanical_rename" in redirect
    # Other files must be untouched — auto_apply=False means no side effects.
    assert "LIST_ITEM" in (pkg / "renderer.py").read_text()
    assert "LIST_ITEM" in (pkg / "refiner.py").read_text()
    assert "LIST_ITEM" in (pkg / "extractor.py").read_text()


def test_search_replace_path_still_auto_applies(tmp_path):
    """Default auto_apply=True (the search_replace path) must still walk the
    package and rename the identifier everywhere — this is the regression
    guard that the search_replace happy-path was not changed."""
    pkg = _build_slides_pkg(tmp_path)
    llm = pkg / "llm.py"
    existing = (
        "from .models import BlockType\n\n"
        "def plan():\n"
        "    return BlockType.LIST_ITEM\n"
    )
    llm.write_text(existing)
    new_content = existing.replace("LIST_ITEM", "list_item")

    redirect = SearchReplace._detect_multifile_rename(existing, new_content, llm)
    assert redirect is not None
    assert redirect.startswith("APPLIED:"), redirect
    # The package-wide rename should have landed.
    assert "LIST_ITEM" not in (pkg / "renderer.py").read_text()
    assert "list_item" in (pkg / "renderer.py").read_text()


def test_no_intercept_when_env_disabled(tmp_path, monkeypatch):
    monkeypatch.setenv("DRYDOCK_MULTIFILE_INTERCEPT", "0")
    pkg = _build_slides_pkg(tmp_path)
    llm = pkg / "llm.py"
    existing = (
        "from .models import BlockType\n\n"
        "def plan():\n"
        "    return BlockType.LIST_ITEM\n"
    )
    llm.write_text(existing)
    new_content = existing.replace("LIST_ITEM", "list_item")
    assert SearchReplace._detect_multifile_rename(
        existing, new_content, llm, auto_apply=False,
    ) is None


def test_no_intercept_on_feature_addition_rewrite(tmp_path):
    """Adding new backends/subcommands/etc. rewrites a file with multiple
    new identifiers. That's not a rename — it's a feature-addition
    rewrite. Caught 2026-05-25 live in session_20260525_173957 where
    'Add storage backend: mongodb' got refused for removing the comment
    word `needed` while the rewrite added 4 unrelated backend classes."""
    pkg = tmp_path / "tool_agent"
    pkg.mkdir()
    (pkg / "__init__.py").write_text("# tool_agent\nneeded = []\n")
    for n in ["a", "b", "c", "d", "e"]:
        (pkg / f"{n}.py").write_text("# needed by this module\n")
    init = pkg / "__init__.py"
    new = (
        "from tool_agent.storage.bolt_storage import BoltStorageBackend\n"
        "from tool_agent.storage.ceph_storage import CephStorageBackend\n"
        "from tool_agent.storage.leveldb_storage import LevelDBStorageBackend\n"
        "from tool_agent.storage.mysql_storage import MySQLStorageBackend\n"
    )
    redirect = SearchReplace._detect_multifile_rename(
        init.read_text(), new, init, auto_apply=False,
    )
    # The diff introduces 4 new identifiers — that's a clear signal it's
    # NOT a rename. Guard must allow the write through.
    assert redirect is None, f"unexpectedly REFUSED: {redirect[:200] if redirect else None}"


def test_no_intercept_on_package_name_removal(tmp_path):
    """The package directory name (e.g. `tool_agent`) appears in every
    file via imports. A rewrite that switches between `from tool_agent.x`
    and `from .x` will trivially "remove" the package name locally even
    though nothing is actually being renamed. Caught 2026-05-25 in
    session_20260525_180113 ('Add storage backend: clickhouse')."""
    pkg = tmp_path / "tool_agent"
    pkg.mkdir()
    (pkg / "__init__.py").write_text("")
    for n in ["a", "b", "c", "d", "e"]:
        (pkg / f"{n}.py").write_text("from tool_agent.x import y\n")
    target = pkg / "clickhouse_storage.py"
    target.write_text("from tool_agent.base import Backend\nclass A: pass\n")
    new = "from .base import Backend\nclass A:\n    def save(self, k, v): pass\n"
    redirect = SearchReplace._detect_multifile_rename(
        target.read_text(), new, target, auto_apply=False,
    )
    assert redirect is None, f"unexpectedly REFUSED: {redirect[:200] if redirect else None}"


def test_no_intercept_when_identifier_is_local(tmp_path):
    """If the removed identifier isn't referenced in any other file, this is
    a single-file edit and must not be refused."""
    pkg = _build_slides_pkg(tmp_path)
    llm = pkg / "llm.py"
    existing = (
        "def helper_internal():\n"
        "    x = 'internal_value_token_xyz'\n"
        "    return x\n"
    )
    llm.write_text(existing)
    new_content = (
        "def helper_internal():\n"
        "    y = 'renamed_value_token_xyz'\n"
        "    return y\n"
    )
    assert SearchReplace._detect_multifile_rename(
        existing, new_content, llm, auto_apply=False,
    ) is None
